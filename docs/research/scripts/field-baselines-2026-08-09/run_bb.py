#!/usr/bin/env python3
"""Parallel runner for the PRESERVED, VALIDATED besieged-core decoder.

`docs/research/scripts/side-lane-2026-08-09/bb_decode.py` is the exact instrument
that produced the "2.68 adjacent healers" figure (validated there by five checks:
entity bookkeeping 5,470/5,470, the geometric adj<=8 invariant, a heal x 4 HP vs
independent-HP-stream agreement of 0.9941 per-side median, throw counts exact
against `corpus/throws.tsv`, and spawn/death totals against `tl.tsv`).

It is imported UNMODIFIED here.  The only thing this file adds is a process pool
and per-file output buffering, because the original is single-process and the
third-party population is 3x the size of the one it was written for.  Nothing
about the decoding changes, so the re-derived numbers stay comparable to the
originals by construction.

`bb_decode` needs no attribution table at all -- it emits one row per
(file, round, TEAM INDEX) -- so team identity is joined afterwards from
`meta_join.tsv`.

    python run_bb.py <outdir> @<filelist>
"""
from __future__ import annotations

import io
import sys
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "docs/research/scripts/side-lane-2026-08-09"))

import bb_decode  # noqa: E402


def work(p: str):
    out, vout = io.StringIO(), io.StringIO()
    try:
        bb_decode.decode(Path(p), out, vout)
    except Exception as exc:                                   # noqa: BLE001
        return ("ERR", p, repr(exc))
    return ("OK", out.getvalue(), vout.getvalue())


def main(argv):
    outdir = Path(argv[0])
    outdir.mkdir(parents=True, exist_ok=True)
    spec = argv[1]
    files = ([x.strip() for x in open(spec[1:]) if x.strip()]
             if spec.startswith("@") else argv[1:])
    fr = (outdir / "bb.tsv").open("w")
    fv = (outdir / "bbv.tsv").open("w")
    fr.write("\t".join(bb_decode.COLS) + "\n")
    fv.write("\t".join(bb_decode.VCOLS) + "\n")
    bad = 0
    with Pool(8) as pool:
        for i, res in enumerate(pool.imap_unordered(work, files, chunksize=4)):
            if res[0] == "ERR":
                bad += 1
                print("ERR", res[1], res[2], file=sys.stderr)
                continue
            fr.write(res[1])
            fv.write(res[2])
            if (i + 1) % 500 == 0:
                print(f"  ...{i+1}/{len(files)} ({bad} err)", file=sys.stderr, flush=True)
    fr.close()
    fv.close()
    print(f"done {len(files)} files, {bad} errors", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
