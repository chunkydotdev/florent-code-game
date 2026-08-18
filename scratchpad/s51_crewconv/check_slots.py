#!/usr/bin/env python3
"""Guard check for FS_CREW_CONVERT measurement (s51 FS_CREW_CONVERT job).

Verifies whether the appended-override arm construction (mkarm.sh) correctly
propagates FS_CREW_ON=True into every doctrine-level DERIVED default it
should touch, per BUILD-REPORT-v515ecosalt-2026-08-18.md finding 3 ("a
doctrine-level derived default is order-dependent under mkarm.sh -- arm
overrides append AFTER the derivation ran").
"""
import sys

for name, path in [
    ("CARRIER", "scratchpad/s51_v515_build/arms/CARRIER"),
    ("CREWCONV", "scratchpad/s51_v515_build/arms/CREWCONV"),
]:
    sys.path.insert(0, path)
    import doctrine
    print("=== %s (%s) ===" % (name, path))
    print("  FS_CREW_ON       =", doctrine.FS_CREW_ON)
    print("  FS_CREW_CONVERT  =", doctrine.FS_CREW_CONVERT)
    print("  LOKI_FERRY_ON    =", doctrine.LOKI_FERRY_ON)
    print("  FERRY_HOME_ON    =", doctrine.FERRY_HOME_ON,
          " <-- should be False when FS_CREW_ON True + FS_V514_RELAY True")
    print("  FS_SUPP_SLOT     =", doctrine.FS_SUPP_SLOT)
    print("  SLOT_FERRY_ID    =", doctrine.SLOT_FERRY_ID)
    collide = (doctrine.FS_CREW_ON and doctrine.FERRY_HOME_ON
               and doctrine.FS_SUPP_SLOT == doctrine.SLOT_FERRY_ID)
    print("  TWO-WRITER COLLISION ON SLOT %d:" % doctrine.SLOT_FERRY_ID, collide)
    sys.path.remove(path)
    for mod in ("doctrine",):
        del sys.modules[mod]
