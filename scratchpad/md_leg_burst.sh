#!/bin/zsh
# MC burst — _v207apprlaunch must be LIVE (submit-hold leg). Fires 5 pinned
# matches on the APPR set vs MA's minted anchors. Run INSIDE the leg window.
cd /Users/junghard/Projects/Work/florent-code-game
OUT=scratchpad/md_leg_fires.tsv
typeset -a maps; maps=(--map antler --map auroraveil --map frostgate --map royale)
typeset -a names ids pins
names=(U1-Erebus U2-HTTP418 U3-0033 U4-farming U5-kladde)
ids=(9810ba35-66a9-4af3-9a2f-06651aef4109 12fdece5-48c9-4913-9533-6d95b73e22ab 74ae65ff-96ae-4da5-a43e-692eb6fee38f 25288fdb-f3a0-4ae2-964f-2fd7eb9b11d7 c7571c87-f960-4c88-a13d-14340bb3200f)
pins=(6bcb5fdd-afa5-4ce0-b372-c444e8c48871 cea633ec-2a8d-4142-85b1-34e15c974b03 c8683709-175f-4640-bb8b-5b9b1b2f301f eb6f89b1-f5ca-47fd-9dbd-660f05c0ce1a 09c67a4e-4946-4d4a-aaf5-e8bf0e1511d3)   # MB anchors, FULL
# MD pins are full ids
for i in 1 2 3 4 5; do
  r=$(.venv/bin/fcode match unrated "${ids[$i]}" --match "${pins[$i]}" $maps --json 2>&1)
  case "$r" in *matchId*) v=ACCEPT;; *"Rate limit"*) v=RATELIMIT;; *) v=ERROR;; esac
  printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${names[$i]}" "$v" "$(echo "$r" | tr '\n' ' ' | head -c 220)" >> $OUT
done
cat $OUT
