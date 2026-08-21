#!/usr/bin/env python3
"""Rewrite the now-playing line in README.md from ListenBrainz.

Runs on a schedule in CI. A dead API keeps the previous line.
"""

import json
import sys
import urllib.request
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!--live:start-->", "<!--live:end-->"


def get(url: str, timeout: int = 15):
    req = urllib.request.Request(url, headers={"User-Agent": "tempoloss-profile-cron"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


def music() -> str | None:
    d = json.loads(get("https://api.listenbrainz.org/1/user/tempoloss/listens?count=1"))
    listens = d.get("payload", {}).get("listens") or []
    if not listens:
        return None
    tm = listens[0].get("track_metadata") or {}
    artist, track = tm.get("artist_name"), tm.get("track_name")
    if not artist:
        return None
    return f"{artist} - {track}".lower()


def main() -> int:
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print("no live markers in README", file=sys.stderr)
        return 1

    try:
        track = music()
    except Exception as exc:  # noqa: BLE001 - a dead API must not kill the cron
        print(f"listenbrainz failed: {exc}", file=sys.stderr)
        return 0
    if not track:
        print("no listens")
        return 0

    block = f"\n  **{track}**\n"
    new = text[: text.index(START) + len(START)] + block + text[text.index(END) :]
    if new == text:
        print("no change")
        return 0
    README.write_text(new, encoding="utf-8")
    print(f"README updated: {track}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
