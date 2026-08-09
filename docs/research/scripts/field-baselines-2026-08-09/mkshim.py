#!/usr/bin/env python3
"""Build a `join.tsv`-shaped shim so the SHIPPED decoders run unchanged on
third-party replays.

`collar_decode.py` takes a join table with columns `file` and `our_team` and
decodes each replay twice, labelling the rows US / THEM.  Its notion of "us" is
purely an INDEX, so the same decoder answers "how does team A behave" if we hand
it `our_team = 0`.

This shim therefore sets `our_team = 0` for EVERY attributed file, ours and
third-party alike, so:

    side == "US"   ->  replay index 0  ->  meta_join.teamA
    side == "THEM" ->  replay index 1  ->  meta_join.teamB

and team identity comes from `meta_join.tsv` afterwards rather than from the
decoder.  One code path, one geometry, both populations — which is what makes the
within-team against-us / third-party comparison a fair one.

    python mkshim.py <freezedir>/meta_join.tsv <out.tsv> [--third-party-only]
"""
from __future__ import annotations

import csv
import sys


def main(argv):
    src, dst = argv[0], argv[1]
    third_only = "--third-party-only" in argv
    rows = list(csv.DictReader(open(src), delimiter="\t"))
    with open(dst, "w") as fh:
        fh.write("file\tour_team\n")
        n = 0
        for r in rows:
            if third_only and r["us_side"] != "none":
                continue
            fh.write(f"{r['file']}\t0\n")
            n += 1
    print(f"{n} files -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1:])
