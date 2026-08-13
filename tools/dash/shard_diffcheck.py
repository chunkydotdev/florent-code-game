#!/usr/bin/env python3
"""SHARD DIFF CHECK — does the dashboard show what the terminal tool says?

    .venv/bin/python tools/dash/shard_diffcheck.py                 # against :8787
    .venv/bin/python tools/dash/shard_diffcheck.py --port 8799
    .venv/bin/python tools/dash/shard_diffcheck.py --selftest      # drive it to FAIL

⛔ WHY THIS FILE EXISTS. `tools/dash/serve.py` renders shard STATE, ROWS, PCT,
HB_AGE, ETA, rate and band. Every one of those is computed by
`tools/corefill_status.sh`, and on 2026-08-13 the dashboard shipped THREE
disagreements with its sources in one file — 13 STALLED against the tool's
DONE/DEAD, 4 queue rows against the gate's 21, and a negative tape age. A second
copy of a computation is this repo's most-repeated defect, and "I only parsed it"
is a claim, not a check. This is the check.

===== THE THREE COMPARISONS, AND WHY ONE OF THEM IS NOT ENOUGH =====

A. STRICT (must be exact, 0 mismatches). Re-parse the EXACT text the server is
   currently serving with a DIFFERENT implementation, and compare field by field.
   Different in the two places parsers actually break: serve.py selects rows by
   regex shape plus a first-word blocklist, this one anchors on the `SHARD STATE
   … RESULT` header and stops at the blank line that ends the table. Importing
   serve.py's parser and comparing it to itself would validate anything — that is
   the "constant column" defect this repo names in its own standing rules.

B. LIVE (fields must match, or advance by exactly the elapsed time). Run the
   terminal tool FRESH and compare. The server's text is up to 45 s old, so a
   `running` shard has legitimately gained rows in between — that is ADVANCE, not
   disagreement. Without B, the strict check would happily certify a server that
   captured its text yesterday.
   ⛔ AND `hb_age` IS EXEMPTED FROM NOTHING, BECAUSE IT IS A CLOCK. The first
   version of this check flagged all 62 idle shards for `hb_age` drifting by the
   37 s between the two captures, and the tempting fix — "ages change, skip the
   column" — would have deleted the only field that can prove the dashboard's
   numbers are not frozen. A stale-but-plausible age is the exact defect this
   repo has shipped most often (`ship_watch` printing healthy lines off
   seven-minute-old rows). So instead: for a shard whose heartbeat is NOT being
   rewritten, `hb_age` must advance by EXACTLY the gap between the two runs' own
   `COREFILL STATUS` header stamps. Frozen fails, and so does drifting.

C. MAP LABEL vs the tool's RETIRED%. The detail view labels each shard's map set
   from that shard's own tsv rows; `corefill_status.sh` independently counts rows
   played off the live pool. Two derivations of one fact, so they must agree in
   sign: RETIRED>0 ⟺ the label says pre-rotation or MIXED. This is the only check
   that can catch a map label that is confidently wrong, which the brief names as
   worse than no label at all.

===== THE CHECK IS ITSELF AN INSTRUMENT, SO IT IS DRIVEN TO BOTH VERDICTS =====
`--selftest` corrupts one input per comparison and asserts that comparison
REPORTS A MISMATCH. A check that has never produced the other verdict has not
been seen to check. Where a branch cannot be exercised on the current data (no
running shard ⇒ no backwards-rows case) it prints UNTESTED rather than counting
itself as passed.

⛔ Read the printed VERDICT, not the exit code: a crash also exits non-zero and
means UNKNOWN, not FAIL. Exit 0 = pass, 1 = fail, 2 = unknown/not-run.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIELDS = ("state", "rows", "pct", "hb_age", "eta", "result_raw")


# ------------------------------------------------------------ independent parse

def parse_independent(text: str) -> dict[str, dict]:
    """Header-anchored, blank-line-bounded, whitespace-split. NOT serve.py's regex.

    `printf "%-11s %-9s %7s %6s %8s %9s   %s"` cannot be sliced at fixed columns —
    `LAUNCHLATE160` is 13 characters and shifts every field right of it — so the
    split is on whitespace with the RESULT column taken as the unsplit remainder.
    What makes this an independent implementation is ROW SELECTION: it trusts the
    table's own header and terminator instead of a blocklist of first words.
    """
    lines = text.splitlines()
    hdr_i = None
    for i, l in enumerate(lines):
        if l.startswith("SHARD") and "STATE" in l and "RESULT" in l:
            hdr_i = i
            break
    if hdr_i is None:
        raise SystemExit("UNKNOWN: no `SHARD STATE … RESULT` header in the tool "
                         "output — the table shape changed and every parser of it "
                         "here is void")
    out: dict[str, dict] = {}
    for l in lines[hdr_i + 1:]:
        if not l.strip():
            break                                # the blank line ends the table
        p = l.split(None, 6)
        if len(p) < 6:
            raise SystemExit(f"UNKNOWN: unparseable table row: {l!r}")
        out[p[0]] = {"shard": p[0], "state": p[1], "rows": int(p[2]), "pct": p[3],
                     "hb_age": p[4], "eta": p[5],
                     "result_raw": p[6].strip() if len(p) > 6 else ""}
    return out


# ---------------------------------------------------------------------- helpers

def fetch(url: str):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def run_tool() -> str:
    p = subprocess.run(["zsh", str(ROOT / "tools" / "corefill_status.sh")],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=300)
    return p.stdout or p.stderr


HDR_RE = re.compile(r"^COREFILL STATUS\s+(\S+)", re.M)
# States a shard can legitimately leave while we are looking at it. Anything else
# changing is a disagreement, not a transition.
MUTABLE = {"running", "queued", "STALLED"}
HB_TOL_S = 3          # the tool's NOW and its header `date` are separate calls


def header_stamp(text: str):
    m = HDR_RE.search(text)
    if not m:
        raise SystemExit("UNKNOWN: no `COREFILL STATUS <ts>` header — cannot date "
                         "the tool output, and an undated capture proves nothing")
    return datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc)


def _age_s(v: str):
    return int(v[:-1]) if isinstance(v, str) and v.endswith("s") else None


def diff_rows(a: dict, b: dict, la: str, lb: str,
              elapsed_s: int | None = None,
              worklist_edited: str | None = None) -> tuple[list[str], list[str]]:
    """Field by field. Returns (mismatches, transitions).

    `elapsed_s is None` ⇒ the two inputs describe the SAME instant and every field
    must be identical (comparison A). Otherwise `b` was captured `elapsed_s` after
    `a` and each field is checked against what that gap permits (comparison B).

    `worklist_edited` ⇒ the worklist's own mtime is NEWER than capture `a`, so a
    shard present in one capture and not the other is an operator ADD/REMOVE
    rather than a disagreement. ⛔ It is gated on that evidence and not on
    convenience: with the worklist unchanged, a shard appearing or vanishing
    between two runs of the same tool is exactly the kind of silent population
    drift this check exists to catch, and skipping it unconditionally would have
    made the membership comparison a constant column.
    """
    bad, moved = [], []
    for sh in sorted(set(a) | set(b)):
        if sh not in a or sh not in b:
            missing_from, present_in = (la, lb) if sh not in a else (lb, la)
            if worklist_edited:
                moved.append(f"  {sh:<14} in {present_in}, not in {missing_from} — "
                             f"worklist {worklist_edited}")
            else:
                bad.append(f"  {sh:<14} MISSING from {missing_from} (present in "
                           f"{present_in}) and the worklist has NOT been edited "
                           f"since — the population drifted on its own")
            continue
        ra, rb = a[sh], b[sh]
        sa, sb = ra.get("state"), rb.get("state")
        if elapsed_s is not None and sa != sb:
            if sa in MUTABLE:
                moved.append(f"  {sh:<14} {sa} -> {sb} between the two captures "
                             f"(legitimate; its other fields are not compared)")
                continue
            bad.append(f"  {sh:<14} state: {la}={sa!r}  {lb}={sb!r} — {sa} is not "
                       f"a state a shard leaves on its own")
            continue
        live = elapsed_s is not None and sa == "running"
        for f in FIELDS:
            va, vb = ra.get(f), rb.get(f)
            if f == "hb_age" and elapsed_s is not None:
                aa, ab = _age_s(va), _age_s(vb)
                if live:
                    continue                      # heartbeat is being rewritten
                if va == "-" or vb == "-":
                    if va != vb:
                        bad.append(f"  {sh:<14} hb_age: {la}={va!r} {lb}={vb!r} — "
                                   f"a heartbeat cannot appear or vanish here")
                    continue
                if aa is None or ab is None:
                    bad.append(f"  {sh:<14} hb_age unparseable: {la}={va!r} "
                               f"{lb}={vb!r}")
                elif abs((ab - aa) - elapsed_s) > HB_TOL_S:
                    bad.append(f"  {sh:<14} hb_age advanced {ab - aa}s but the two "
                               f"captures are {elapsed_s}s apart ({la}={va}, "
                               f"{lb}={vb}) — the age is not tracking the clock")
                continue
            if va == vb:
                continue
            if live and f != "state":
                if f == "rows" and int(vb) < int(va):
                    bad.append(f"  {sh:<14} rows WENT BACKWARDS "
                               f"{la}={va} -> {lb}={vb}")
                continue
            bad.append(f"  {sh:<14} {f}: {la}={va!r}  {lb}={vb!r}")
    return bad, moved


def diff_maps(rendered: dict, get_detail) -> tuple[list[str], int, int]:
    """RETIRED% from the tool vs the detail view's map label. Sign must agree."""
    bad, checked, skipped = [], 0, 0
    for sh, r in sorted(rendered.items()):
        rp = r.get("retired_pct")
        if rp is None:
            skipped += 1          # tool printed no rate ⇒ it did not measure it
            continue
        d = get_detail(sh)
        label = d["maps"]["label"]
        says_pre = label.startswith("pre-rotation") or label == "MIXED"
        checked += 1
        if (rp > 0) != says_pre:
            bad.append(f"  {sh:<14} tool RETIRED={rp}%  detail label={label!r} "
                       f"({d['maps']['why']})")
    return bad, checked, skipped


def report(name: str, headline: str, bad: list[str], passline: str,
           moved: list[str] | None = None) -> int:
    print(f"\n{name}")
    print(f"   {headline}")
    if moved:
        print(f"   {len(moved)} shard(s) changed state between captures:")
        print("\n".join(moved))
    if bad:
        print("   *** MISMATCH ***")
        print("\n".join(bad))
        return 1
    print(f"   PASS — {passline}")
    return 0


# --------------------------------------------------------------------- fixture

FX_ROWS_HDR = "ts\tshard\tgame\tmap\tseed\tseat\twinner\tcond\tturns"


def _fx_tsv(path: Path, shard: str, n: int, maps: list[str], ts: str) -> None:
    lines = [FX_ROWS_HDR]
    for i in range(n):
        w = "T" if i % 2 == 0 else "C"
        lines.append(f"{ts}\t{shard}\t{i}\t{maps[i % len(maps)]}\t900{i}\t"
                     f"{'A' if i % 2 == 0 else 'B'}\t{w}\tcore_destroyed\t200")
    path.write_text("\n".join(lines) + "\n")


def fixture_check() -> int:
    """Drive the under-400 refusal and every map-set verdict on data WE author.

    ⛔ IN A THROWAWAY DIRECTORY, NEVER `scratchpad/overnight`. `tools/overnight.sh`
    carries a comment about exactly this: a fixture believed isolated by an env var
    instead wrote into the live run, created files beside five live shards and
    launched a stray shard. OUT/STATE are passed explicitly here and the directory
    is a fresh mkdtemp that is removed at the end.

    Both verdicts, per branch: the same fixture is grown past 400 rows and must
    then print a rate; the same shard is rewritten onto each map pool and must
    change label; a tsv with no `map` column must come out "unknown", not guessed.
    """
    import shutil
    import tempfile
    sys_path = str(ROOT / "tools" / "dash")
    if sys_path not in os.sys.path:
        os.sys.path.insert(0, sys_path)
    import serve                                       # the code under test

    pools = serve.map_pools()
    if pools["blind"]:
        print(f"UNKNOWN: {pools['blind']}")
        return 2
    live_only = sorted(pools["live"] - pools["prev"]) or sorted(pools["live"])
    retired = sorted(pools["prev"] - pools["live"])
    if not retired:
        print("UNKNOWN: the previous pool is not recoverable, so the pre-rotation "
              "branch cannot be exercised")
        return 2

    tmp = Path(tempfile.mkdtemp(prefix="dash-shard-fixture-"))
    out, state = tmp / "overnight", tmp / "started"
    out.mkdir(); state.mkdir()
    work = tmp / "work.txt"
    work.write_text(
        "# fixture worklist — never the live one\n"
        "FXSMALL     bots/_fxa   bots/_fxb   5408  1\n"
        "FXBIG       bots/_fxa   bots/_fxb   5408  1\n"
        "FXLIVE      bots/_fxa   bots/_fxb   5408  1\n"
        "FXNOMAP     bots/_fxa   bots/_fxb   5408  1\n"
        "FXABSENT    bots/_fxa   bots/_fxb   5408  1\n")
    old_ts, new_ts = "2026-08-12T00:00:00Z", "2026-08-13T23:00:00Z"
    _fx_tsv(out / "FXSMALL.tsv", "FXSMALL", 41, retired + sorted(pools["prev"])[:4], old_ts)
    _fx_tsv(out / "FXBIG.tsv", "FXBIG", 480, retired + sorted(pools["prev"])[:4], old_ts)
    _fx_tsv(out / "FXLIVE.tsv", "FXLIVE", 480, live_only, new_ts)
    (out / "FXNOMAP.tsv").write_text("ts\tshard\tgame\tseed\twinner\n"
                                     + f"{new_ts}\tFXNOMAP\t0\t1\tT\n")
    for sh in ("FXSMALL", "FXBIG", "FXLIVE", "FXNOMAP"):
        (state / sh).write_text(old_ts + "\n")
        (out / f"{sh}.heartbeat").write_text(f"{old_ts}\t1\t5408\t{sh}\tRUNNING\n")

    env = dict(os.environ, OUT=str(out), STATE=str(state))
    p = subprocess.run(["zsh", str(ROOT / "tools" / "corefill_status.sh"), str(work)],
                       cwd=str(ROOT), capture_output=True, text=True,
                       timeout=300, env=env)
    rows = {r["shard"]: r for r in serve.parse_shard_table(p.stdout)}

    checks: list[tuple[str, bool, str]] = []
    small, big = rows.get("FXSMALL", {}), rows.get("FXBIG", {})
    checks.append(("41 rows  -> tool REFUSES a rate",
                   small.get("refused") is True and small.get("rate") is None,
                   f"refused={small.get('refused')} rate={small.get('rate')} "
                   f"raw={small.get('result_raw')!r}"))
    checks.append(("480 rows -> tool PRINTS a rate (the same branch, other verdict)",
                   big.get("refused") is False and isinstance(big.get("rate"), float),
                   f"refused={big.get('refused')} rate={big.get('rate')} "
                   f"raw={big.get('result_raw')!r}"))

    real_dir = serve.OVERNIGHT
    try:
        serve.OVERNIGHT = out
        m_small = serve.shard_map_set("FXSMALL")
        m_live = serve.shard_map_set("FXLIVE")
        m_nomap = serve.shard_map_set("FXNOMAP")
        m_absent = serve.shard_map_set("FXABSENT")
    finally:
        serve.OVERNIGHT = real_dir
    checks.append(("rows on retired maps  -> 'pre-rotation'",
                   m_small["label"].startswith("pre-rotation"),
                   f"{m_small['label']} :: {m_small['why']}"))
    checks.append(("rows on post-rotation maps -> 'live pool'",
                   m_live["label"] == "live pool",
                   f"{m_live['label']} :: {m_live['why']}"))
    checks.append(("tsv with no `map` column -> 'unknown', not a guess",
                   m_nomap["label"] == "unknown",
                   f"{m_nomap['label']} :: {m_nomap['why']}"))
    checks.append(("no tsv at all -> 'unknown', not a guess",
                   m_absent["label"] == "unknown",
                   f"{m_absent['label']} :: {m_absent['why']}"))

    shutil.rmtree(tmp, ignore_errors=True)
    print("FIXTURE CHECK  (throwaway dir, OUT/STATE overridden, live run untouched)")
    bad = 0
    for name, okc, detail in checks:
        print(f"  [{'PASS' if okc else 'FAIL'}] {name}\n         {detail}")
        bad += 0 if okc else 1
    print()
    print("VERDICT: PASS — every branch driven to both verdicts" if not bad
          else f"VERDICT: FAIL ({bad} fixture check(s) failed)")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8787")))
    ap.add_argument("--selftest", action="store_true",
                    help="corrupt each input and assert the comparison FAILS")
    ap.add_argument("--fixture", action="store_true",
                    help="run the under-400 and map-set branches on authored data "
                         "in a throwaway dir (no server needed)")
    args = ap.parse_args()
    if args.fixture:
        return fixture_check()
    base = f"http://127.0.0.1:{args.port}"

    try:
        served = fetch(base + "/api/shards")
    except urllib.error.URLError as e:
        print(f"UNKNOWN: no dashboard at {base} ({e}). Start one first:\n"
              f"  PORT={args.port} .venv/bin/python tools/dash/serve.py")
        return 2
    if served.get("pending"):
        print("UNKNOWN: the server's first corefill_status.sh run has not "
              "finished. Wait ~10 s and retry.")
        return 2
    text = served.get("text")
    if not text:
        print(f"UNKNOWN: server served no tool text (error={served.get('error')!r})")
        return 2

    rendered = {r["shard"]: r for r in served["rows"]}
    print("SHARD DIFF CHECK")
    print(f"  dashboard : {base}/shards   ({len(rendered)} shard rows)")
    print(f"  tool text : generated {served.get('at')} "
          f"(age {served.get('age_min')}m, cadence {served.get('cadence_min')}m)")
    print(f"  worklist  : {served['worklist']['path']} "
          f"({served['worklist']['n']} lines)")

    fails = 0
    indep = parse_independent(text)
    bad_a, _ = diff_rows(rendered, indep, "dash", "reparse")
    fails += report(
        "A. STRICT  dashboard fields vs an independent re-parse of the same text",
        f"{len(rendered)} vs {len(indep)} rows; fields: {', '.join(FIELDS)}",
        bad_a,
        f"{len(rendered)} shards x {len(FIELDS)} fields identical, 0 mismatches")

    fresh_text = run_tool()
    fresh = parse_independent(fresh_text)
    dash_at = header_stamp(text)
    elapsed = int((header_stamp(fresh_text) - dash_at).total_seconds())
    # The worklist's own mtime decides whether a membership change is an operator
    # ADD ("append a line" is corefill's entire interface) or population drift.
    wl_at = datetime.strptime(served["worklist"]["at"], "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=timezone.utc) if served["worklist"].get("at") else None
    wl_edited = (f"edited {int((wl_at - dash_at).total_seconds())}s AFTER this "
                 f"capture ({served['worklist']['at']})") \
        if wl_at and wl_at > dash_at else None
    n_run = sum(1 for r in fresh.values() if r["state"] == "running")
    bad_b, moved_b = diff_rows(rendered, fresh, "dash", "fresh", elapsed_s=elapsed,
                               worklist_edited=wl_edited)
    fails += report(
        "B. LIVE    dashboard fields vs a fresh `zsh tools/corefill_status.sh`",
        f"{len(rendered)} vs {len(fresh)} rows, captures {elapsed}s apart; "
        f"{n_run} running shards may advance rows/pct/eta/result; every idle "
        f"shard's hb_age must advance by {elapsed}s ±{HB_TOL_S}s; worklist "
        + (wl_edited or f"unchanged since the capture, so the shard population "
                        f"must be identical"),
        bad_b,
        f"every state as expected; no idle field differs; no row count went "
        f"backwards; every idle hb_age tracked the clock to within {HB_TOL_S}s",
        moved_b)

    bad_c, checked, skipped = diff_maps(
        rendered, lambda sh: fetch(base + "/api/shard?id=" + sh))
    fails += report(
        "C. MAPS    detail-view map label vs the tool's own RETIRED% column",
        f"{checked} shards carry a RETIRED reading; {skipped} skipped because the "
        f"tool printed no rate for them (under 400 rows), which is not zero",
        bad_c,
        f"{checked} shards agree in sign (RETIRED>0 <=> pre-rotation/MIXED)")

    if args.selftest:
        print("\nSELFTEST  driving each comparison to its FAILING verdict")
        ok = True
        # A — corrupt the TEXT, so the mutation enters through the parser under test
        victim = sorted(rendered)[0]
        got, _ = diff_rows(rendered,
                           parse_independent(text.replace(victim, victim + "X", 1)),
                           "dash", "reparse")
        print(f"   A  rename {victim} in the tool text        -> {len(got)} "
              f"mismatch(es) {'OK' if got else '*** DID NOT FIRE ***'}")
        ok &= bool(got)
        # A2 — corrupt a rendered field, i.e. the dashboard lying about one shard
        mut = {k: dict(v) for k, v in rendered.items()}
        mut[victim]["state"] = "BOGUS"
        got2, _ = diff_rows(mut, indep, "dash", "reparse")
        print(f"   A2 rendered {victim}.state -> 'BOGUS'      -> {len(got2)} "
              f"mismatch(es) {'OK' if got2 else '*** DID NOT FIRE ***'}")
        ok &= bool(got2)
        # B1 — a FROZEN age must fail: this is the ship_watch defect, so the check
        #      for it has to be seen firing, not assumed.
        idle = next((s for s, r in fresh.items()
                     if r["state"] not in MUTABLE and _age_s(r["hb_age"])), None)
        if idle:
            mut3 = {k: dict(v) for k, v in fresh.items()}
            mut3[idle]["hb_age"] = rendered[idle]["hb_age"]        # frozen
            got3, _ = diff_rows(rendered, mut3, "dash", "fresh", elapsed_s=elapsed)
            print(f"   B1 freeze {idle}.hb_age at the old value -> {len(got3)} "
                  f"mismatch(es) {'OK' if got3 else '*** DID NOT FIRE ***'}")
            ok &= bool(got3)
        else:
            print("   B1 UNTESTED — no idle shard with a numeric hb_age. Not a pass.")
        # B2 — a running shard's rows going backwards must survive the advance rule
        run_sh = next((s for s, r in fresh.items() if r["state"] == "running"), None)
        if run_sh:
            mut2 = {k: dict(v) for k, v in fresh.items()}
            mut2[run_sh]["rows"] = rendered[run_sh]["rows"] - 1
            got4, _ = diff_rows(rendered, mut2, "dash", "fresh", elapsed_s=elapsed)
            print(f"   B2 {run_sh} rows go BACKWARDS -> {len(got4)} "
                  f"mismatch(es) {'OK' if got4 else '*** DID NOT FIRE ***'}")
            ok &= bool(got4)
        else:
            print("   B2 UNTESTED — no running shard right now, so the "
                  "backwards-rows branch was not exercised. Not a pass.")
        # B3 — a shard vanishing with the worklist UNCHANGED must still fail, or
        #      the ADD exemption above would swallow real population drift.
        mut4 = {k: v for k, v in fresh.items() if k != victim}
        got_drift, _ = diff_rows(rendered, mut4, "dash", "fresh",
                                 elapsed_s=elapsed, worklist_edited=None)
        print(f"   B3 drop {victim} with the worklist unchanged -> "
              f"{len(got_drift)} mismatch(es) "
              f"{'OK' if got_drift else '*** DID NOT FIRE ***'}")
        ok &= bool(got_drift)
        # C — flip one label against a real RETIRED reading
        cand = next((s for s, r in rendered.items()
                     if r.get("retired_pct") is not None), None)
        if cand:
            real = fetch(base + "/api/shard?id=" + cand)
            flipped = {"maps": dict(real["maps"])}
            flipped["maps"]["label"] = ("live pool"
                                        if rendered[cand]["retired_pct"] > 0
                                        else "pre-rotation (forced)")
            got5, _, _ = diff_maps({cand: rendered[cand]}, lambda _s: flipped)
            print(f"   C  flip {cand} map label vs RETIRED="
                  f"{rendered[cand]['retired_pct']}% -> {len(got5)} "
                  f"mismatch(es) {'OK' if got5 else '*** DID NOT FIRE ***'}")
            ok &= bool(got5)
        else:
            print("   C  UNTESTED — no shard carries a RETIRED reading. Not a pass.")
        if ok:
            print("   SELFTEST OK — every exercised comparison produced the "
                  "other verdict")
        else:
            print("   *** SELFTEST FAILED — a comparison could not be made to "
                  "fail, so its PASS above means nothing ***")
            fails += 1

    print()
    if fails:
        print(f"VERDICT: FAIL ({fails} comparison(s) mismatched)")
        return 1
    print("VERDICT: PASS — the dashboard's shard values equal the terminal tool's")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
