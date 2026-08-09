#!/usr/bin/env python3
"""FREEZE + GATE for the third-party field-baseline re-derivation.

Snapshots every input into a scratchpad directory the keeper daemon does not
touch, records row counts and md5s, and re-states the attribution gate.

The attribution table itself is NOT re-derived here.  `tools/corpus/meta_attrib.py`
already ships it, already carries the seat/winner reconciliation, and already
ships negative controls (`--selftest=seat|winner`).  This script only runs it into
the freeze directory and records what came out.

    python docs/research/scripts/field-baselines-2026-08-09/freeze.py <freezedir>
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CORPUS = ROOT / "corpus"
TABLES = ["join.tsv", "build_agg.tsv", "builds.tsv", "events.tsv", "econ.tsv",
          "flow.tsv", "throws.tsv", "ladder_games.tsv"]


def md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv):
    fz = Path(argv[0]).resolve()
    fz.mkdir(parents=True, exist_ok=True)
    prov = {"frozen": {}}

    # --- 1. the attribution table, regenerated into the freeze dir ---------
    mj = fz / "meta_join.tsv"
    r = subprocess.run([sys.executable, str(ROOT / "tools/corpus/meta_attrib.py"), str(mj)],
                       capture_output=True, text=True, cwd=ROOT)
    prov["meta_attrib_stdout"] = r.stdout
    prov["meta_attrib_rc"] = r.returncode
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return 1

    # --- 2. negative controls: the gate must be able to fail ---------------
    for mode in ("seat", "winner"):
        rr = subprocess.run([sys.executable, str(ROOT / "tools/corpus/meta_attrib.py"),
                             f"--selftest={mode}", str(fz / "selftest.tsv")],
                            capture_output=True, text=True, cwd=ROOT)
        prov[f"selftest_{mode}"] = rr.stdout.strip().splitlines()[-1]
        prov[f"selftest_{mode}_rc"] = rr.returncode
        print(prov[f"selftest_{mode}"])
    (fz / "selftest.tsv").unlink(missing_ok=True)
    (fz / "selftest.tsv.gz").unlink(missing_ok=True)

    # --- 3. corpus tables -------------------------------------------------
    for t in TABLES:
        src = CORPUS / t
        dst = fz / t
        dst.write_bytes(src.read_bytes())
        n = sum(1 for _ in dst.open()) - 1
        prov["frozen"][t] = {"md5": md5(dst), "rows": n}
        print(f"  frozen {t}: {n} rows md5 {prov['frozen'][t]['md5'][:8]}")
    prov["frozen"]["meta_join.tsv"] = {
        "md5": md5(mj), "rows": sum(1 for _ in mj.open()) - 1}
    prov["manifest"] = json.loads((CORPUS / "manifest.json").read_text())
    prov["git_sha"] = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                     capture_output=True, text=True,
                                     cwd=ROOT).stdout.strip()
    prov["archive_replays"] = len(list((ROOT / "replay_archive").rglob("*.replay26")))

    (fz / "provenance.json").write_text(json.dumps(prov, indent=2))
    print(f"\nfrozen -> {fz}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
