#!/usr/bin/env python3
"""NO NEW DERIVED DEFAULTS: AST-scan doctrine.py for module-level assignments
whose right-hand side reads any v521 flag (v518-v520 inherited, must also be 0).

v515 finding 3: `mkarm.sh` APPENDS arm overrides to the end of doctrine.py, so
any module-level `X = f(FLAG)` is evaluated against the flag value the module
body saw, not the arm's.  The required count for the v519 flags is ZERO.

GUARD (driven both ways, per branch): a synthetic module with one such
assignment MUST be reported, and the same module with the assignment removed
MUST NOT be.  Also re-runs the scan for the v515 flag set, which is documented
to have exactly ONE remaining instance (FERRY_HOME_ON reads FS_CREW_ON) -- that
positive control is what proves the scanner is not blind to the real thing.
"""
from __future__ import annotations

import ast
import sys

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
V517 = {"LOKI_FS_V517", "FS_V517_FIREDISC", "FS_V517_NET_W",
        "FS_V517_NET_EPS", "FS_V517_HOLD_TTL", "FS_V517_NET_STALE",
        "FS_V517_TWIN", "FS_V517_TWIN_TI_FLOOR", "FS_V517_TWIN_REBUY_TI",
        "FS_V517_TWIN_NEEDED_CAP", "FS_V517_TWINBANK", "FS_V517_BANK_TTL",
        "FS_V517_PEER_SHIFT", "FS_V517_VERDICT_SHIFT", "FS_V517_NETCODE_SHIFT",
        "FS_V517_CODE_HELD", "FS_V517_NET_BUCKETS", "FS_V517_STAMP_MOD"}
V516 = {"LOKI_FS_V516", "FS_V516_TEARDOWN", "FS_V516_GLOBALSENT",
        "FS_V516_SENTREACH"}
V515 = {"LOKI_FS_V515", "FS_V515_DOOR_OFF", "FS_V515_GATE_OR", "FS_V515_REACH"}
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
            # a module-level conditional whose TEST reads a flag is the same
            # hazard even if the assignment is nested inside it
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


GUARD_POS = "LOKI_FS_V521 = True\nX = LOKI_FS_V521 and 3\n"
GUARD_NEG = "LOKI_FS_V521 = True\nX = 3\n"
GUARD_IF = "LOKI_FS_V521 = True\nif LOKI_FS_V521:\n    X = 3\n"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else \
        "bots/_v521sync/doctrine.py"
    ok = True
    if not scan(GUARD_POS, V521):
        print("GUARD FAIL: positive control not reported"); ok = False
    if scan(GUARD_NEG, V521):
        print("GUARD FAIL: negative control reported"); ok = False
    if not scan(GUARD_IF, V521):
        print("GUARD FAIL: module-level `if FLAG:` not reported"); ok = False
    print("GUARD: pos=%s neg=%s if=%s" %
          (bool(scan(GUARD_POS, V521)), bool(scan(GUARD_NEG, V521)),
           bool(scan(GUARD_IF, V521))))
    src = open(path).read()
    h521 = scan(src, V521)
    h520 = scan(src, V520)
    h519 = scan(src, V519)
    h518 = scan(src, V518)
    hcrew = scan(src, CREW)
    print("v521 derived defaults: %d %s" % (len(h521), h521))
    print("v520 derived defaults (inherited, must also be 0): %d %s" % (len(h520), h520))
    print("v519 derived defaults (inherited, must also be 0): %d %s" % (len(h519), h519))
    print("v518 derived defaults (inherited, must also be 0): %d %s" % (len(h518), h518))
    print("REAL-CASE CONTROL (FS_CREW_ON readers, the known v515 hazard): "
          "%d %s" % (len(hcrew), hcrew))
    if h521 or h520 or h519 or h518:
        ok = False
    if not hcrew:
        print("GUARD FAIL: the known FERRY_HOME_ON instance was not found -- "
              "the scanner cannot see the real defect class")
        ok = False
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
