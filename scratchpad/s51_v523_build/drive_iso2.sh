#!/bin/bash
# ⛔ ISOLATION LEG 2 -- RUN BECAUSE LEG 1 HAD NO KNOWN-ZERO ARM AND ALL THREE OF
# ITS TREATMENT ARMS MOVED THE SAME WAY, which is the signature of a low
# baseline draw rather than of three real effects.  This leg puts a
# BYTE-IDENTICAL COPY OF THE BASELINE in the same blocks on the same seeds, so
# every contrast is reported twice.
#   parent   -- the v521-verdict parent (baseline)
#   parentB  -- the SAME TREE, second copy: the KNOWN-ZERO arm
#   iNOPHASE -- the parent with FS_V521_PHASE_HONEST OFF (v521 clause 1e, kept
#               on a separability argument and never isolated)
#   v522     -- the fired build, for a second independent read beside a
#               known-zero arm on seeds disjoint from the headline
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export PAR=4
BLOCKS="${BLOCKS:-13}"
rm -rf "$B/arms/parentB"; cp -R "$B/arms/parent" "$B/arms/parentB"
rm -rf "$B/arms/parentB/__pycache__"
rm -rf "$B/arms/v522"; cp -R bots/_v523eyes "$B/arms/v522"; chmod -R u+w "$B/arms/v522"
rm -rf "$B/arms/v522/__pycache__"
for i in $(seq 1 "$BLOCKS"); do
  s1=$((800+i*3-2)); s2=$((800+i*3-1)); s3=$((800+i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/iso2/b$i"
  for a in parent parentB iNOPHASE v522; do
    .venv/bin/python "$B/run_grid.py" "$B/arms/$a" \
        "$B/iso2/b$i/$a.tsv" "$B/iso2/b$i/rep$a" "$B/iso2/b$i/log$a" \
        > "$B/iso2/b$i/$a.log" 2>&1 &
    echo "$! iso2-$a-b$i" >> "$B/PIDS"
  done
  wait
  echo "ISO2 BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "ISO2 DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
