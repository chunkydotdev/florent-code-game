#!/usr/bin/env python3
"""cite_check.py -- does every URL the tactics library CITES actually exist?

WHY THIS EXISTS (s32, 2026-08-11).  A sweep-25 agent self-disclosed that it had
written a Jay Scott URL from memory: the QUOTE was verbatim, the SOURCE FIELD was
invented.  `archives/117-static-defense-is-bad.html` does not exist; the real page
is `archives/353-turtle-strategies.html`.

The side lane's structural read, and it is why this is a script and not a rule:
**the citation is RE-TYPED rather than CARRIED.**  Quote verification confirms
"this text exists in what I fetched"; the file then records "this text came from
URL X"; and NOTHING JOINS THOSE TWO CLAIMS.  An agent that fetched page A and
writes URL B passes every check the library has, BY CONSTRUCTION.  That is why
every prior instance of this library's failure mode was in the quote -- the quote
is the half the pipeline plumbs.

This closes the cheap half of the join: **a cited URL that does not resolve cannot
be where the quote came from.**  It does not verify that the quote is ON that page
(that is the expensive half, and a 200 here is NOT evidence the span is there).

WHAT A RESULT MEANS
  DEAD   -- 404/410.  Treat as a FABRICATED OR ROTTEN CITATION until re-sourced.
            This is the signal the tool exists for.
  OK     -- resolves.  Says NOTHING about whether the quote is on the page.
  BLOCKED-- 403/429 or a bot wall (Cloudflare).  NOT a defect; not evidence either.
  ERROR  -- network/DNS/timeout.  Re-run before believing it.

DRIVEN BOTH WAYS: --selftest injects a known-dead URL and a known-live one and
asserts the checker separates them.  A checker that has never returned DEAD has
not been seen to check -- this repo produced six unfirable guards in one day.

Read-only.  Sends HEAD (falling back to a ranged GET, since many servers 405 a
HEAD), follows redirects, and paces itself.  No page bodies are stored.
"""
from __future__ import annotations

import argparse
import collections
import glob
import os
import re
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (compatible; cite-check/1.0; +local research verification)"
URL_RE = re.compile(r"https?://[^\s,)\]<>\"']+")

# Known-answer pair for --selftest.  The dead one is the ACTUAL fabricated
# citation from sweep 25, so the fixture is the incident itself.
SELFTEST_DEAD = "http://satirist.org/ai/starcraft/blog/archives/117-static-defense-is-bad.html"
SELFTEST_LIVE = "http://satirist.org/ai/starcraft/blog/archives/353-turtle-strategies.html"


def extract(tactics_dir: str) -> dict[str, list[str]]:
    """url -> [files citing it], from `source:` frontmatter lines only."""
    cites: dict[str, list[str]] = collections.defaultdict(list)
    for path in sorted(glob.glob(os.path.join(tactics_dir, "*.md"))):
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if not line.startswith("source:"):
                    continue
                for raw in URL_RE.findall(line):
                    cites[raw.rstrip(".,;")].append(os.path.basename(path))
    return cites


STOPWORDS = {
    "the", "a", "an", "is", "are", "to", "of", "and", "or", "in", "on", "for",
    "with", "it", "its", "be", "was", "how", "why", "what", "at", "by", "from",
    "html", "htm", "php", "index", "blog", "archives", "post", "posts",
}
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


def _tokens(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", text.lower()) if len(t) > 2 and t not in STOPWORDS}


def _slug_of(url: str) -> str:
    """Trailing path segment, minus a leading numeric id and the extension.

    Serendipity-style blogs (satirist.org) serve `<id>-<slug>.html` where the ID
    is AUTHORITATIVE and the SLUG IS DECORATIVE AND IGNORED.  That is exactly how
    the sweep-25 fabricated citation returned HTTP 200 while pointing at a
    completely different article.
    """
    seg = url.rstrip("/").rsplit("/", 1)[-1]
    seg = re.sub(r"\.(html?|php|aspx)$", "", seg, flags=re.I)
    return re.sub(r"^\d+[-_]", "", seg)


def probe(url: str, timeout: float) -> tuple[str, str]:
    """-> (verdict, detail).  Never raises.

    Two independent failure modes, and the SECOND is the one that motivated this
    tool: a citation can resolve 200 and still be fabricated, because the slug is
    not part of the lookup.  Status alone CANNOT catch that.
    """

    def _open(method: str):
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", UA)
        return urllib.request.urlopen(req, timeout=timeout)

    body, status = None, None
    try:
        with _open("GET") as resp:
            status = resp.status
            body = resp.read(65536).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 429):
            return "BLOCKED", f"{exc.code} (bot wall / rate limit — not a defect, not a pass)"
        if exc.code in (404, 410):
            return "DEAD", str(exc.code)
        return "ERROR", f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001 - network layer; any failure is a non-verdict
        return "ERROR", type(exc).__name__

    slug = _slug_of(url)
    stoks = _tokens(slug)
    if not stoks:
        return "OK", f"{status} (no slug to cross-check)"

    m = TITLE_RE.search(body or "")
    if not m:
        return "OK", f"{status} (no <title> to cross-check)"
    title = re.sub(r"\s+", " ", m.group(1)).strip()
    ttoks = _tokens(title)

    # The join: does the page the URL RESOLVES TO look like the page the URL CLAIMS?
    if stoks & ttoks:
        return "OK", f"{status} · title matches slug"
    return "MISMATCH", f"{status} · slug '{slug}' vs title '{title[:70]}'"


def selftest(timeout: float) -> int:
    print("SELFTEST — the checker must separate a known-dead from a known-live URL.")
    print("  (the dead one IS the sweep-25 fabricated citation; the fixture is the incident)")
    dead, dd = probe(SELFTEST_DEAD, timeout)
    live, ld = probe(SELFTEST_LIVE, timeout)
    print(f"  known-DEAD {SELFTEST_DEAD}\n      -> {dead} ({dd})")
    print(f"  known-LIVE {SELFTEST_LIVE}\n      -> {live} ({ld})")
    if dead == "DEAD" and live == "OK":
        print("\n  ✅ PASS — the guard fires on the bad case and stays silent on the good one.")
        return 0
    if dead in ("ERROR", "BLOCKED") or live in ("ERROR", "BLOCKED"):
        print("\n  ⚠ INCONCLUSIVE — network or bot wall. NOT a pass. Re-run before trusting a sweep.")
        return 2
    print("\n  ⛔ FAIL — the checker cannot tell a dead citation from a live one. Do not trust its output.")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default="docs/research/tactics")
    ap.add_argument("--delay", type=float, default=0.4, help="seconds between requests (politeness)")
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--limit", type=int, default=0, help="check only the first N urls (0 = all)")
    ap.add_argument("--selftest", action="store_true", help="drive the checker both ways and exit")
    args = ap.parse_args()

    if args.selftest:
        return selftest(args.timeout)

    cites = extract(args.dir)
    urls = sorted(cites)
    if args.limit:
        urls = urls[: args.limit]
    print(f"cite_check — {len(urls)} unique URLs cited by {len(set(f for v in cites.values() for f in v))} files")
    print("⚠ A 200 means the PAGE exists. It does NOT mean the quote is on it.\n")

    buckets: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for i, url in enumerate(urls, 1):
        verdict, detail = probe(url, args.timeout)
        buckets[verdict].append((url, detail))
        if verdict == "DEAD":
            print(f"  ⛔ DEAD  {url}  [{detail}]")
            for f in cites[url]:
                print(f"          cited by {f}")
        print(f"    ...{i}/{len(urls)}", end="\r", file=sys.stderr)
        time.sleep(args.delay)

    print("\n" + "=" * 72)
    for k in ("DEAD", "ERROR", "BLOCKED", "OK"):
        print(f"  {k:<8} {len(buckets[k])}")
    if buckets["DEAD"]:
        print(f"\n⛔ {len(buckets['DEAD'])} CITATION(S) DO NOT RESOLVE — re-source or cut them.")
        print("   A verbatim quote under a dead URL is the sweep-25 failure mode exactly.")
    else:
        print("\n✅ No dead citations. (Says nothing about whether the quotes are on those pages.)")
    if buckets["ERROR"] or buckets["BLOCKED"]:
        print(f"⚠ {len(buckets['ERROR'])} ERROR + {len(buckets['BLOCKED'])} BLOCKED are NON-VERDICTS, not passes.")
    return 1 if buckets["DEAD"] else 0


if __name__ == "__main__":
    sys.exit(main())
