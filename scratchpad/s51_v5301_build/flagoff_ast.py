#!/usr/bin/env python3
"""NO NEW DERIVED DEFAULTS: AST-scan doctrine.py for module-level assignments
(or module-level `if`/conditional tests) whose right-hand side reads
LOKI_FS_V525 or any v525 constant, plus every inherited flag set back through
v515/CREW (the v515 finding-3 hazard: `mkarm.sh` appends arm overrides to the
end of doctrine.py, so a module-level `X = f(FLAG)` freezes the flag value the
MODULE BODY saw, not the arm's -- `LOKI_FS_V525` must only be read at RUN time
inside `_fs_map_gated`, never at import time).

Copied and extended from scratchpad/s51_v524_build/flagoff_ast.py (same
method, same guard, same inherited flag sets) -- adds V527.

GUARD (driven both ways, per branch): a synthetic module with one such
assignment MUST be reported, and the same module with the assignment removed
MUST NOT be. Also re-runs the scan for the v515 flag set, documented to have
exactly ONE remaining instance (FERRY_HOME_ON reads FS_CREW_ON) -- the
positive control proving the scanner is not blind to the real thing.
"""
from __future__ import annotations

import ast
import sys

V5301 = {"FS_V5301_BOOTFIX", "V5301_MOUTH_SEAT", "V5301_MOUTH_OPEN_AFTER_HARV"}

V530 = {"LOKI_FS_V530", "FS_V530_MOUTH", "V530_MOUTH_MAX_RND",
        "V530_MOUTH_MAX_LINKS", "V530_MOUTH_TTL", "FS_V530_MOUTH_SEATS",
        "FS_V530_CORNERS", "V530_CORNER_MAX_RND", "V530_CORNER_MIN_RND",
        "V530_CORNER_KEEP", "V530_CORNER_TI_FLOOR", "FS_V530_DOORKILL",
        "V530_DOOR_DSQ", "V530_DOOR_PRIO", "V530_DOOR_GUNNER", "FS_V530_LOG"}

V528 = {"LOKI_FS_V528", "FS_V528_CONNCOST", "V528_CONN_W_LINK",
        "V528_CONN_W_WALK", "V528_CONN_CONTEST", "V528_CONN_UNREACH",
        "V528_CONN_REFRESH", "V528_CONN_MAX_CAND", "V528_CONN_NODE_BUDGET",
        "V528_CONN_BAN_RNDS", "FS_V528_WALK", "FS_V528_WIRE",
        "V528_WIRE_MAX_DEFER", "FS_V528_LOG"}

V527 = {"LOKI_FS_V527", "FS_V527_BUNKER", "FS_V527_MAG_SHOTS",
        "FS_V527_BUNKER_NEAR", "FS_V527_BUNKER_MAX", "FS_V527_DEFENDED",
        "FS_V527_DEFENDED_BONUS", "FS_V527_DEFENDED_DSQ", "FS_V527_PSURV",
        "FS_V527_PSURV_LASTSEAT", "FS_V527_PSURV_TFIRST", "FS_V527_PSURV_NEAR",
        "FS_V527_PSURV_DISPATCH", "FS_V527_PSURV_EXTRA", "FS_V527_PSURV_MAXRND",
        "FS_V527_SEALPATH", "FS_V527_PATH_DSQ", "FS_V527_PATH_SWITCH",
        "FS_V527_LOG"}

V526 = {"LOKI_FS_V526", "FS_V526_TEMPO", "FS_V526_CREW_SEAT",
        "FS_V526_MUSTER_WAIT", "FS_V526_RDV", "FS_V526_VETO",
        "FS_V526_RDV_PICKUP_DSQ", "FS_V526_WALK", "FS_V526_LOG"}
V525 = {"LOKI_FS_V525", "FS_V525_CRIPPLE_MAPS", "FS_V525_MIN_MAP_DIM",
        "FS_V525_MIN_CORE_DSQ", "FS_V525_LOG"}
# ⛔ FLAGS ONLY -- AND THE DISTINCTION IS THE WHOLE POINT OF THE SCAN.  The
# v515 finding-3 hazard is a module-level default that reads a FLAG, so
# flipping the flag no longer reaches it.  A module-level value derived from a
# DATA CONSTANT is not that class: `FS_V524_MIDGARD_CODE` /
# `FS_V524_YULERUNE_CODE` are map-code strings that no flag ever changes, and
# `FS_V524_CRIPPLE_GRIDS` decoding them at import is correct and intended.
# ⭐ THIS WAS FOUND BY v527 EXTENDING THE SCAN FROM doctrine.py ALONE TO
# doctrine + siege + main.  The two hits it produced (siege.py:63) are that
# false-positive class, not a defect -- reclassified here rather than
# suppressed, so the scanner keeps its power on the real class.
V524 = {"LOKI_FS_V524", "FS_V524_LOG"}
V524_DATA = {"FS_V524_MIDGARD_CODE", "FS_V524_YULERUNE_CODE",
             "FS_V524_CRIPPLE_GRIDS"}
V522 = {"LOKI_FS_V522", "FS_V522_FLOOR", "FS_V522_NEAR", "FS_V522_FUND_AMMO",
        "FS_V522_SEATS", "FS_V522_FLOOR_CAP", "FS_V522_MAX_RNDS",
        "FS_V522_BIND_IF", "FS_V522_PHASE_ONLY", "FS_V522_MAG_LOG",
        "FS_V522_PH_LOG", "FS_PH_KILL_NEAR"}
V521 = {"LOKI_FS_V521", "FS_V521_SYNC", "FS_V521_SYNC_NEAR",
        "FS_V521_FUND_AMMO", "FS_V521_FWD_DSQ", "FS_V521_NEAR_CLOSE",
        "FS_V521_HOLD", "FS_V521_HOLD_FUNDED", "FS_V521_BUYIN",
        "FS_V521_BUYIN_MAX_RND", "FS_V521_SYNC_LOG", "FS_V521_RUNG_LOG",
        "FS_V521_GATEFIX", "FS_V521_GATEFIX_LOG", "FS_V521_COLLARFIRST", "FS_V521_PHASE_HONEST",
        "FS_V521_COLLAR_BARRIERS", "FS_V521_MAG_LOG", "FS_V521_WHY_LOG"}
V520 = {"LOKI_FS_V520", "FS_V520_PINCER", "FS_V520_CREW", "FS_V520_SPLIT",
        "FS_V520_SPLIT_MAX_RND", "FS_V520_SPLIT_WALK", "FS_V520_TERMSITE",
        "FS_V520_TERM_DSQ", "FS_V520_INRING_FERRY", "FS_V520_TERM_NOTEAR",
        "FS_V520_ARC_PUBLISH", "FS_V520_ARC_SHIFT", "FS_V520_ARC_MASK",
        "FS_V520_ARC_SEAL", "FS_V520_APPT_GUARD", "FS_V520_APPT_LOG",
        "FS_V520_PRESENCE", "FS_V520_PRES_MARGIN", "FS_V520_PRES_TTL",
        "FS_V520_PRES_CAP", "FS_V520_PRES_MAX_RNDS", "FS_V520_PRES_SEATS",
        "FS_V520_PRES_LOG", "FS_V520_GUNNEAR", "FS_V520_GF_DSQ_LO",
        "FS_V520_GF_RING_ONLY", "FS_V520_SPLIT_LOG", "FS_V520_TERM_LOG",
        "FS_V520_ARC_LOG", "FS_V520_COVER_LOG"}
V519 = {"LOKI_FS_V519", "FS_V519_GUNFIRST", "FS_V519_GF_MIN_RND",
        "FS_V519_GF_MAX_RND", "FS_V519_GF_MAX_PLANTS", "FS_V519_GF_TI_FLOOR",
        "FS_V519_GF_LOG", "FS_V519_MODESWITCH", "FS_V519_CRIPPLE_MAPS",
        "FS_V519_MODE_LOG"}
V518 = {"LOKI_FS_V518", "FS_V518_EARLYSITE", "FS_V518_EARLY_MAX_LIVE",
        "FS_V518_EARLY_REACH_FIRST", "FS_V518_EARLY_LOG",
        "FS_V518_TWINRES", "FS_V518_RES_MARGIN", "FS_V518_RES_TTL",
        "FS_V518_RES_LOG", "FS_V518_GAPLOG", "FS_V518_TIWATCH"}
CREW = {"FS_CREW_ON", "LOKI_FS_CREW"}


def scan(src: str, names: set) -> list:
    tree = ast.parse(src)
    hits = []
    for node in tree.body:                       # MODULE LEVEL ONLY
        targets = None
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        elif isinstance(node, (ast.If, ast.Try, ast.For, ast.While)):
            test = getattr(node, "test", None)
            if test is not None:
                for n in ast.walk(test):
                    if isinstance(n, ast.Name) and n.id in names:
                        hits.append((node.lineno, "<conditional block>", n.id))
            continue
        else:
            continue
        for n in ast.walk(value):
            if isinstance(n, ast.Name) and n.id in names:
                tn = [t.id for t in targets if isinstance(t, ast.Name)]
                hits.append((node.lineno, ",".join(tn) or "?", n.id))
    return hits


GUARD_POS = "LOKI_FS_V530 = True\nX = LOKI_FS_V530 and 3\n"
GUARD_POS_5301 = "FS_V5301_BOOTFIX = True\nX = FS_V5301_BOOTFIX and 3\n"
GUARD_NEG_5301 = "FS_V5301_BOOTFIX = True\nX = 3\n"
GUARD_NEG = "LOKI_FS_V530 = True\nX = 3\n"
GUARD_IF = "LOKI_FS_V530 = True\nif LOKI_FS_V530:\n    X = 3\n"


def main():
    paths = sys.argv[1:] or ["bots/_v531fix/doctrine.py"]
    ok = True
    if not scan(GUARD_POS, V530):
        print("GUARD FAIL: positive control not reported"); ok = False
    if scan(GUARD_NEG, V530):
        print("GUARD FAIL: negative control reported"); ok = False
    if not scan(GUARD_IF, V530):
        print("GUARD FAIL: module-level `if FLAG:` not reported"); ok = False
    if not scan(GUARD_POS_5301, V5301):
        print("GUARD FAIL: v530.1 positive control not reported"); ok = False
    if scan(GUARD_NEG_5301, V5301):
        print("GUARD FAIL: v530.1 negative control reported"); ok = False
    print("GUARD v530.1: pos=%s neg=%s" %
          (bool(scan(GUARD_POS_5301, V5301)), bool(scan(GUARD_NEG_5301, V5301))))
    print("GUARD: pos=%s neg=%s if=%s" %
          (bool(scan(GUARD_POS, V530)), bool(scan(GUARD_NEG, V530)),
           bool(scan(GUARD_IF, V530))))

    total = 0
    for path in paths:
        src = open(path).read()
        h5301 = scan(src, V5301)
        h530 = scan(src, V530)
        h528 = scan(src, V528)
        h527 = scan(src, V527)
        h526 = scan(src, V526)
        h525 = scan(src, V525)
        h524 = scan(src, V524)
        h522 = scan(src, V522)
        h521 = scan(src, V521)
        h520 = scan(src, V520)
        h519 = scan(src, V519)
        h518 = scan(src, V518)
        hcrew = scan(src, CREW)
        print(f"\n=== {path} ===")
        print("v530.1 derived defaults: %d %s" % (len(h5301), h5301))
        print("v530 derived defaults (inherited, must also be 0): %d %s" % (len(h530), h530))
        print("v528 derived defaults (inherited, must also be 0): %d %s" % (len(h528), h528))
        print("v527 derived defaults (inherited, must also be 0): %d %s" % (len(h527), h527))
        print("v526 derived defaults (inherited, must also be 0): %d %s" % (len(h526), h526))
        print("v525 derived defaults (inherited, must also be 0): %d %s" % (len(h525), h525))
        print("v524 derived defaults (inherited, must also be 0): %d %s" % (len(h524), h524))
        print("v522 derived defaults (inherited, must also be 0): %d %s" % (len(h522), h522))
        print("v521 derived defaults (inherited, must also be 0): %d %s" % (len(h521), h521))
        print("v520 derived defaults (inherited, must also be 0): %d %s" % (len(h520), h520))
        print("v519 derived defaults (inherited, must also be 0): %d %s" % (len(h519), h519))
        print("v518 derived defaults (inherited, must also be 0): %d %s" % (len(h518), h518))
        if path.endswith("doctrine.py"):
            print("REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard): "
                  "%d %s" % (len(hcrew), hcrew))
            if not hcrew:
                print("GUARD FAIL: the known FERRY_HOME_ON instance was not found -- "
                      "the scanner cannot see the real defect class")
                ok = False
        total += (len(h5301) + len(h530) + len(h528) + len(h527) + len(h526) + len(h525) + len(h524) + len(h522) + len(h521) + len(h520) +
                  len(h519) + len(h518))

    if total:
        ok = False
    print("\nTOTAL derived-default hits across all scanned files:", total)
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
