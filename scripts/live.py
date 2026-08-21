#!/usr/bin/env python3
"""Rewrite the live status block in README.md from public APIs.

Runs on a schedule in CI. Every source is optional: a dead API keeps the
previous line, so the block degrades one line at a time instead of whole.
"""

import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!--live:start-->", "<!--live:end-->"


def get(url: str, timeout: int = 15):
    req = urllib.request.Request(url, headers={"User-Agent": "tempoloss-profile-cron"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


def chess() -> str | None:
    d = json.loads(get("https://api.chess.com/pub/player/an8kk/stats"))
    b = d.get("chess_bullet") or {}
    last, best = b.get("last", {}).get("rating"), b.get("best", {}).get("rating")
    if not last:
        return None
    return f"chess    bullet {last} · peak {best}"


def music() -> str | None:
    d = json.loads(get("https://api.listenbrainz.org/1/user/tempoloss/listens?count=1"))
    listens = d.get("payload", {}).get("listens") or []
    if not listens:
        return None
    tm = listens[0].get("track_metadata") or {}
    artist, track = tm.get("artist_name"), tm.get("track_name")
    if not artist:
        return None
    return f"music    last played: {artist} - {track}".lower()


def tokens() -> str | None:
    d = json.loads(get("https://an8kk.dev/api/tok"))
    n = d.get("llm_tokens")
    if not n:
        return None
    return f"llm      {n:,} tokens"


def shipped() -> str | None:
    t = get(
        "https://raw.githubusercontent.com/duckdb/community-extensions/main/extensions/quackiso/description.yml"
    )
    m = re.search(r"^\s*version:\s*\"?([\d.]+)\"?", t, re.M)
    if not m:
        return None
    return f"shipped  quackiso v{m.group(1)} · duckdb community registry"


def main() -> int:
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("no live markers in README", file=sys.stderr)
        return 1

    current = text[text.index(START) + len(START) : text.index(END)]
    lines = {}
    for line in current.splitlines():
        key = line.split(" ", 1)[0].strip()
        if key:
            lines[key] = line

    for fn in (chess, music, tokens, shipped):
        try:
            line = fn()
        except Exception as exc:  # noqa: BLE001 - a dead API must not kill the block
            print(f"{fn.__name__} failed: {exc}", file=sys.stderr)
            continue
        if line:
            lines[line.split(" ", 1)[0]] = line

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M utc")
    order = ["tmp@astana:~$", "chess", "music", "llm", "shipped", "updated"]
    lines["tmp@astana:~$"] = "tmp@astana:~$ status"
    lines["updated"] = f"updated  {stamp}"
    block = "\n```\n" + "\n".join(lines[k] for k in order if k in lines) + "\n```\n"

    new = text[: text.index(START) + len(START)] + block + text[text.index(END) :]
    if new == text:
        print("no change")
        return 0
    README.write_text(new, encoding="utf-8")
    print("README updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
