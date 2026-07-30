#!/usr/bin/env python3
"""Build the primitives reader: one self-contained HTML file, five repositories.

Every repository in the portfolio carries two committed inputs:

  docs/primitives.md         the entry text (what the mechanism is, where it is
                             used, what breaks if it is wrong, what catches it)
  docs/primitives.code.json  the line-by-line annotations: file, line range,
                             note line numbers, and fingerprints of the code
                             those lines held when the note was written

This script renders both into `tools/primitives/reader.template.html` and writes
one HTML file that opens by double-click and works offline.

The rule that makes the output trustworthy: **no rendered code is stored in any
input.** Every line the reader displays is read from the repository on disk at
build time. An annotation can therefore point at the wrong line, but it can
never show code that does not exist. The fingerprints in
`docs/primitives.code.json` exist to catch exactly the first failure, and each
repository's own `scripts/check_primitives_anchors.py` is run before the build.

Usage:
    python3 tools/primitives/build_reader.py --root .. --out primitives.html
    python3 tools/primitives/build_reader.py --repo moxy=/src/moxy ... --check
"""

from __future__ import annotations

import argparse
import collections
import html
import json
import re
import subprocess
import sys
from pathlib import Path

# The order is the order the reader lists entries in, and it is deliberate:
# queue durability first, then the gateway, the generator, the app, the extension.
DEFAULT_REPOS = ["moxy", "search-gateway", "db-seed", "chessview", "quackiso"]

OWNER = "tempoloss"
TEMPLATE = Path(__file__).with_name("reader.template.html")
DATA_LINE = re.compile(r"^const DATA = .*;$", re.MULTILINE)

# Anchors are written as `path/to/file.ext:12` or `path/to/file.ext:12-20`.
ANCHOR = re.compile(r"^([A-Za-z0-9_./\-]+\.[A-Za-z0-9_+]+):(\d+)(?:-(\d+))?$")
ANCHOR_IN_TEXT = re.compile(r"`([A-Za-z0-9_./\-]+\.[A-Za-z0-9_+]+):(\d+)(?:-(\d+))?`")

LANG = {
    ".go": "go", ".py": "py", ".rs": "rs", ".sql": "sql", ".ts": "ts", ".tsx": "ts",
    ".yml": "yml", ".yaml": "yml", ".test": "sql", ".lua": "lua", ".toml": "toml", ".md": "md",
}
# Only whole-line comments are highlighted. A half-finished tokenizer that
# mis-colours a string containing "//" is worse than no colour at all.
LINE_COMMENT = {"go": "//", "rs": "//", "ts": "//", "py": "#", "yml": "#", "toml": "#",
                "sql": "--", "lua": "--"}

SECTIONS = (
    ("**Where:**", "where"),
    ("**What breaks if it is wrong:**", "breaks"),
    ("**Caught by:**", "caught"),
)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def plural(n: int, one: str, few: str, many: str) -> str:
    if n % 100 in range(11, 15):
        return many
    if n % 10 == 1:
        return one
    if n % 10 in (2, 3, 4):
        return few
    return many


def inline(text: str, repo: str, link_anchors: bool = True) -> str:
    """Render the small markdown subset the entries use: `code`, **bold**, anchors."""
    out = []
    for part in re.split(r"(`[^`]*`)", text):
        if len(part) >= 2 and part.startswith("`") and part.endswith("`"):
            body = part[1:-1]
            match = ANCHOR.match(body)
            if match and link_anchors:
                out.append(blob_link(repo, match.group(1), match.group(2), match.group(3), esc(body)))
            else:
                out.append(f"<code>{esc(body)}</code>")
        else:
            out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc(part)))
    return "".join(out)


def blob_link(repo: str, path: str, start: str | int, end: str | int | None, label: str) -> str:
    fragment = f"#L{start}" + (f"-L{end}" if end else "")
    return (f'<a class="loc" href="https://github.com/{OWNER}/{repo}/blob/main/{path}{fragment}"'
            f' target="_blank" rel="noopener">{label}</a>')


def numbered_items(text: str) -> list[str]:
    """Split "1) a 2) b 3) c" into items.

    Markers are accepted only in sequence, so a sentence ending in "second 29."
    or "returns 400." is not mistaken for the next item.
    """
    spans, expected, pos = [], 1, 0
    while True:
        match = re.compile(rf"(?:(?<=\s)|^){expected}[.)]\s").search(text, pos)
        if match is None:
            break
        spans.append(match.span())
        pos, expected = match.end(), expected + 1
    if not spans:
        return [text.strip()] if text.strip() else []
    items = []
    for index, (_, end) in enumerate(spans):
        stop = spans[index + 1][0] if index + 1 < len(spans) else len(text)
        items.append(text[end:stop].strip())
    return [item for item in items if item]


def parse_entries(repo: str, markdown: str) -> list[dict]:
    """Parse docs/primitives.md into entries. `## ` is an area, `### ` an entry."""
    entries: list[dict] = []
    blocks: list[tuple[dict, list[str]]] = []
    area, current, buffer = None, None, []

    def flush() -> None:
        if buffer and current is not None:
            blocks.append((current, list(buffer)))

    for line in markdown.splitlines():
        if re.match(r"^#{1,3} ", line):
            flush()
            buffer.clear()
            if line.startswith("### "):
                current = {"repo": repo, "area": area, "title": line[4:].strip(),
                           "prose": [], "where": "", "breaks": [], "caught": ""}
                entries.append(current)
            elif line.startswith("## "):
                area = line[3:].strip()
            continue
        if not line.strip():
            flush()
            buffer.clear()
            continue
        buffer.append(line.strip())
    flush()

    for entry, lines in blocks:
        head, rest = lines[0], lines[1:]
        for label, key in SECTIONS:
            if not head.startswith(label):
                continue
            tail = head[len(label):].strip()
            if key == "breaks":
                # Two shapes appear in the corpus: the items inline after the
                # label, or one "N. item" per following line.
                entry["breaks"] = (numbered_items(tail) if tail
                                   else [re.sub(r"^\d+[.)]\s*", "", line) for line in rest])
            else:
                entry[key] = " ".join([tail] + rest).strip()
            break
        else:
            entry["prose"].append(" ".join([head] + rest))
    return entries


def highlight(line: str, lang: str) -> str:
    marker = LINE_COMMENT.get(lang)
    if marker and line.strip().startswith(marker):
        return f'<span class="cmt">{esc(line)}</span>'
    return esc(line)


def render_code_panel(repo: str, card: dict, root: Path, files: dict[str, list[str]]) -> str:
    snippets = card["snippets"]
    n_lines = sum(s["end"] - s["start"] + 1 for s in snippets)
    n_notes = sum(len(s["notes"]) for s in snippets)
    lines_word = plural(n_lines, "строка", "строки", "строк")
    notes_word = plural(n_notes, "пояснение", "пояснения", "пояснений")
    parts = [
        f'<details class="codefld"><summary>код — {n_lines} {lines_word}, {n_notes} {notes_word}</summary>',
        f'<div class="walk">{esc(card["walk"])}</div>',
    ]
    for snippet in snippets:
        path, start, end = snippet["file"], snippet["start"], snippet["end"]
        if path not in files:
            files[path] = (root / path).read_text(encoding="utf-8").splitlines()
        lines = files[path]
        if end > len(lines):
            raise SystemExit(f"{repo}/{path}: snippet claims lines {start}-{end}, file has {len(lines)}")
        lang = LANG.get(Path(path).suffix, "")
        notes: dict[int, list[str]] = collections.defaultdict(list)
        for note in snippet["notes"]:
            notes[note["line"]].append(note["text"])
        header = blob_link(repo, path, start, end, f"{path}:{start}\u2013{end}")
        parts.append(
            f'<div class="snip"><div class="sh">{header}<span class="lang">{lang}</span></div>'
            f'<div class="why">{esc(snippet["why"])}</div><table class="code">'
        )
        for number in range(start, end + 1):
            source = lines[number - 1]
            cell = highlight(source, lang) if source.strip() else "&nbsp;"
            parts.append(f'<tr class="{"hl" if number in notes else ""}">'
                         f'<td class="num">{number}</td><td class="src">{cell}</td></tr>')
            for text in notes[number]:
                parts.append(f'<tr class="ntr"><td class="num">\u21b3</td>'
                             f'<td class="nt">{esc(text)}</td></tr>')
        parts.append("</table></div>")
    parts.append("</details>")
    return "".join(parts)


def build_repo(repo: str, root: Path, index: int) -> list[dict]:
    markdown = (root / "docs/primitives.md").read_text(encoding="utf-8")
    annotations = json.loads((root / "docs/primitives.code.json").read_text(encoding="utf-8"))
    by_title = {card["title"]: card for card in annotations["cards"]}
    files: dict[str, list[str]] = {}
    payload = []
    for entry in parse_entries(repo, markdown):
        card = by_title.get(entry["title"])
        if card is None:
            raise SystemExit(f"{repo}: entry {entry['title']!r} has no annotated code")
        payload.append({
            "id": f"{repo}-{index + len(payload)}",
            "repo": repo,
            "area": entry["area"],
            "h_title": inline(entry["title"], repo, link_anchors=False),
            "h_prose": "".join(f"<p>{inline(p, repo)}</p>" for p in entry["prose"]),
            "h_where": f'<p>{inline(entry["where"], repo)}</p>',
            "h_breaks": "<ol>" + "".join(f"<li>{inline(x, repo)}</li>" for x in entry["breaks"]) + "</ol>",
            "h_caught": f'<p>{inline(entry["caught"], repo)}</p>',
            "h_code": render_code_panel(repo, card, root, files),
        })
    return payload


def run_anchor_check(repo: str, root: Path) -> None:
    script = root / "scripts/check_primitives_anchors.py"
    if not script.is_file():
        raise SystemExit(f"{repo}: {script} is missing, cannot verify the annotations")
    result = subprocess.run([sys.executable, str(script), "--repo-root", str(root)],
                            capture_output=True, text=True, check=False)
    sys.stdout.write(f"[{repo}] {result.stdout.strip()}\n" if result.stdout.strip() else "")
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit(f"{repo}: stale primitives anchors, refusing to build a reader that lies")


def resolve_repos(args: argparse.Namespace) -> list[tuple[str, Path]]:
    overrides = {}
    for spec in args.repo:
        name, _, path = spec.partition("=")
        if not path:
            raise SystemExit(f"--repo expects NAME=PATH, got {spec!r}")
        overrides[name] = Path(path)
    names = list(overrides) if args.repo and args.only_given else DEFAULT_REPOS
    resolved = []
    for name in names:
        root = overrides.get(name, args.root / name)
        if not root.is_dir():
            raise SystemExit(f"{name}: {root} is not a directory (pass --repo {name}=PATH)")
        resolved.append((name, root.resolve()))
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2].parent,
                        help="directory holding the repository clones (default: next to this repository)")
    parser.add_argument("--repo", action="append", default=[], metavar="NAME=PATH",
                        help="path for one repository, repeatable")
    parser.add_argument("--only-given", action="store_true",
                        help="build only the repositories passed with --repo")
    parser.add_argument("--out", type=Path, default=Path("primitives.html"))
    parser.add_argument("--check", action="store_true",
                        help="verify the inputs and report counts without writing the file")
    parser.add_argument("--skip-anchor-check", action="store_true",
                        help="do not run each repository's anchor checker first")
    args = parser.parse_args()

    data: list[dict] = []
    for name, root in resolve_repos(args):
        if not args.skip_anchor_check:
            run_anchor_check(name, root)
        data.extend(build_repo(name, root, len(data)))

    snippets = sum(entry["h_code"].count('<table class="code">') for entry in data)
    notes = sum(entry["h_code"].count('<tr class="ntr">') for entry in data)
    print(f"{len(data)} entries, {snippets} snippets, {notes} notes")

    if args.check:
        return 0

    template = TEMPLATE.read_text(encoding="utf-8")
    # "<" is escaped so no annotation can close the <script> element early.
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    reader, count = DATA_LINE.subn(lambda _: f"const DATA = {payload};", template, count=1)
    if count != 1:
        raise SystemExit(f"{TEMPLATE}: no `const DATA = ...;` line to replace")
    args.out.write_text(reader, encoding="utf-8")
    print(f"wrote {args.out} ({len(reader.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
