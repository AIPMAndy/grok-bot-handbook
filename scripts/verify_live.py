#!/usr/bin/env python3
"""Verify deployed GitHub Pages is actually serving the checked-out main bytes.

A successful commit or deploy job is not evidence of a live website.  This
uses independent public HTTPS reads, not GitHub's branch or API contents.
"""
from __future__ import annotations
import hashlib
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/grok-bot-handbook/"
FILES = (
    "index.html",
    "source-audit.html",
    "data/claims.json",
    "robots.txt",
    "sitemap.xml",
    "pdf/grok-bot-handbook-guide.pdf",
)

def verify():
    for attempt in range(1, 11):
        problems = []
        for path in FILES:
            source = (ROOT / path).read_bytes()
            source_hash = hashlib.sha256(source).hexdigest()
            url = BASE + path
            try:
                req = urllib.request.Request(
                    url, headers={"User-Agent": "Andy-Grok-Source-Live-QA/1.0", "Cache-Control": "no-cache"}
                )
                with urllib.request.urlopen(req, timeout=25) as response:
                    code = response.status
                    live = response.read()
                live_hash = hashlib.sha256(live).hexdigest()
                if code != 200 or source_hash != live_hash:
                    problems.append(f"{path}: HTTP {code}, source {source_hash}, live {live_hash}")
                else:
                    print(f"PASS {path} HTTP 200 SHA-256 {live_hash}", flush=True)
            except (OSError, urllib.error.HTTPError) as exc:
                problems.append(f"{path}: {type(exc).__name__}: {exc}")
        if not problems:
            print(f"PASS {len(FILES)}/{len(FILES)} real public resources identical to checked-out main")
            return 0
        print(f"Attempt {attempt}/10: "+ " | ".join(problems), file=sys.stderr, flush=True)
        if attempt < 10:
            time.sleep(15)
    return 1

if __name__ == "__main__":
    sys.exit(verify())
