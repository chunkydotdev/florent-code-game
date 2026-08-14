#!/bin/zsh
# MC burst — _v207apprlaunch must be LIVE (submit-hold leg). Fires 5 pinned
# matches on the APPR set vs MA's minted anchors. Run INSIDE the leg window.
cd /Users/junghard/Projects/Work/florent-code-game
OUT=scratchpad/mc_leg_fires.tsv
typeset -a maps; maps=(--map antler --map drumlin --map icefloe --map midgard)
typeset -a names ids pins
names=(U1-Erebus U2-HTTP418 U3-0033 U4-farming U5-kladde)
ids=(9810ba35-66a9-4af3-9a2f-06651aef4109 12fdece5-48c9-4913-9533-6d95b73e22ab 74ae65ff-96ae-4da5-a43e-692eb6fee38f 25288fdb-f3a0-4ae2-964f-2fd7eb9b11d7 c7571c87-f960-4c88-a13d-14340bb3200f)
pins=(12b9c98a-c019-4dfe-8d97-234bfac74f6d 2fa40dc6-884d-41ab-821f-dd2498950710 702eec0f-5991-41bd-95f0-e664d3d6dcfb 5404430b-c0bb-4c94-8a0d-35789c38f9eb 120e0610-f1c9-427f-90ec-f7a64017f107)  # MA anchors, FULL, resolved 07:41Z
for i in 1 2 3 4 5; do
  r=$(.venv/bin/fcode match unrated "${ids[$i]}" --match "${pins[$i]}" $maps --json 2>&1)
  case "$r" in *matchId*) v=ACCEPT;; *"Rate limit"*) v=RATELIMIT;; *) v=ERROR;; esac
  printf '%s\t%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${names[$i]}" "$v" "$(echo "$r" | tr '\n' ' ' | head -c 220)" >> $OUT
done
cat $OUT
