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
  DEAD    -- 404/410.  Rotten or fabricated; re-source it.
  MISMATCH-- resolves, but the page's <title> shares no token with the URL's slug.
             ⛔ THIS IS A TRIAGE FLAG, NOT A VERDICT OF FABRICATION.  Read the
             calibration below before repeating a MISMATCH count to anyone.
  OK      -- resolves and the title matches.  Says NOTHING about whether the QUOTE
             is on the page -- that is the expensive half of the join, not done here.
  BLOCKED -- 403/429 or a bot wall.  NOT a defect and NOT a pass.
  ERROR   -- network/DNS/timeout.  Re-run before believing it.

⛔ CALIBRATION -- MEASURED ON THE FIRST FULL RUN, 2026-08-11, 187 URLs.
Raw output was 17 MISMATCH.  A false-positive guard (numeric ids, commit hashes,
directory URLs) cut that to 5.  **ALL FIVE SURVIVORS WERE THEN TRIAGED BY HAND AND
ALL FIVE WERE CORRECT CITATIONS.**  The heuristic cannot handle:
  * abbreviation      `bc21`        -> "Battlecode 2021 Postmortem"
  * stemming          `defense`     -> "Defending your room | Screeps Documentation"
  * generic titles    `specs-s2`    -> "Lux AI Challenge"
  * compounds         `planetwars`  -> "Planet Wars 2010"
⇒ **TRUE POSITIVES ON THAT RUN: 1 DEAD (link rot) and 0 fabrications beyond the
one already known.  A raw MISMATCH count is NOT a fabrication count, and quoting
it as one would be this repo's standing failure -- a number losing its hedges at
the exit -- committed by the tool built in response to that failure.**

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

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

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
    seg = seg.split("#")[0].split("?")[0]
    seg = re.sub(r"\.(html?|php|aspx|md)$", "", seg, flags=re.I)
    seg = re.sub(r"^\d+[-_]", "", seg)

    # ⛔ FALSE-POSITIVE GUARD, added after the first full-library run flagged 17
    # URLs of which most were NOT fabricated. There is no slug to cross-check when
    # the last path segment is an opaque IDENTIFIER rather than a title:
    #   Discourse/Kaggle end in the topic id  (forum.codingame.com/t/1752)
    #   git hosts end in a commit hash        (.../commit/b0235feefe2e)
    #   directory/index URLs have no slug     (satirist.org/ai/planetwars/)
    # Flagging these as MISMATCH would have reported ordinary citations as
    # fabricated — the exact "a number loses its hedges at the exit" failure this
    # tool was written in response to, committed by the tool itself.
    if re.fullmatch(r"\d+", seg):          # bare numeric id
        return ""
    if re.fullmatch(r"[0-9a-f]{7,40}", seg, flags=re.I):  # commit hash
        return ""
    if seg in ("", "index", "specs"):      # directory / index / generic
        return ""
    return seg


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
    if dead in ("ERROR", "BLOCKED") or live in ("ERROR", "BLOCKED"):
        print("\n  ⚠ INCONCLUSIVE — network or bot wall. NOT a pass. Re-run before trusting a sweep.")
        return 2
    # The known-bad URL resolves 200 (the slug is decorative), so the ONLY verdict
    # that can catch it is MISMATCH. Expecting DEAD here is what made v1 of this
    # selftest fail on the very case the tool was rewritten to detect.
    if dead in ("MISMATCH", "DEAD") and live == "OK":
        print(f"\n  ✅ PASS — the guard fires on the fabricated citation ({dead}) and is silent on the real one.")
        return 0
    print("\n  ⛔ FAIL — the checker cannot separate a fabricated citation from a real one.")
    print("     Do not trust its output until this passes.")
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
        if verdict in ("DEAD", "MISMATCH"):
            mark = "⛔ DEAD    " if verdict == "DEAD" else "⚠ MISMATCH"
            print(f"  {mark} {url}\n              [{detail}]")
            for f in cites[url]:
                print(f"              cited by {f}")
        print(f"    ...{i}/{len(urls)}", end="\r", file=sys.stderr)
        time.sleep(args.delay)

    print("\n" + "=" * 72)
    for k in ("DEAD", "MISMATCH", "ERROR", "BLOCKED", "OK"):
        print(f"  {k:<9} {len(buckets[k])}")
    bad = len(buckets["DEAD"]) + len(buckets["MISMATCH"])
    if bad:
        print(f"\n⛔ {bad} SUSPECT CITATION(S) — re-source or cut them.")
        print("   DEAD     = the page does not exist.")
        print("   MISMATCH = the page EXISTS but is not the page the URL claims. This is the")
        print("              sweep-25 failure mode exactly: the invented slug returned HTTP 200")
        print("              while pointing at a different article, so status alone passes it.")
    else:
        print("\n✅ No dead or mismatched citations.")
        print("   ⚠ Says NOTHING about whether the quoted spans are on those pages —")
        print("     that is the expensive half of the join and this tool does not do it.")
    if buckets["ERROR"] or buckets["BLOCKED"]:
        print(f"⚠ {len(buckets['ERROR'])} ERROR + {len(buckets['BLOCKED'])} BLOCKED are NON-VERDICTS, not passes.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
