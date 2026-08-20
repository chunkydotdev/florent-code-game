# v527 build artifacts (scratchpad/s51_v527_build/)

| what | where |
|---|---|
| parent freeze (v526transit) / child-at-birth / final tree digests | `PARENT_FREEZE.md5`, `CHILD_AT_BIRTH.md5`, `TREE_FINAL.md5` |
| the RDV-only PARENT arm (v526transit, FS_V526_TEMPO=False) | `parent_arm/` |
| the KNOWN-ZERO arm (v527, LOKI_FS_V527=False) | `flagoff_arm/` |
| deterministic byte-identity fixtures (NOISE_ON=False both sides) | `eq_v527/`, `eq_off/`, `eq_parent/`, `eq_opp/`, `byte_check/`, `byte_identity.py` |
| AST derived-default scan (+ FERRY_HOME_ON positive control) | `flagoff_ast.py` |
| M1 guard mutants, in-process, both verdicts per guard | `mutants_m1.py` |
| dose arm (V527 tape + funnel counters) and its games | `dose_arm/`, `dose/` |
| deterministic dose scan (why the mutants are in-process) | `mut_ctl/`, `mutscan/` |
| standdown assertion (archipelago GATED + midgard CRIPPLE) | `standdown/` |
| SEALNT tape injector (asserts every match count) | `instrument527.py` |
| instrumented arms for the M2 signature | `inst_v527/`, `inst_parent/` |
| M2 signature battery + reader (self-tested) | `sealnt/`, `drive_sealnt.sh`, `sealnt_read.py` |
| headline battery (3 arms, 8-map panel, PAR=4) | `head/`, `drive_headline.sh`, `headline.py` |
| failure reel | `reel.py` |
| recorded PIDs (mine + other lanes', left untouched) | `PIDS` |
