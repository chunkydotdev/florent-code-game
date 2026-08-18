#!/bin/bash
# ⛔⛔ THE CHANNEL DECOMPOSITION, run because drive_eq.sh's CHAN control FAILED.
#
# `FS_V522_PHASE_ONLY` (publish FS_PH_KILL_NEAR, never raise the floor) was
# predicted BYTE-IDENTICAL to the parent on the strength of a nine-site
# enumeration of every consumer of the phase channel.  It differed in 5 of 12.
# The prediction was wrong and this leg finds out WHICH HALF of it was wrong,
# rather than explaining it away.
#
# There are exactly two candidate causes and they are separated by a probe:
#   (A) THE TWO EXTRA ENGINE CALLS.  `_v522_near_publish` reads
#       `get_barrier_cost()` and `get_global_ammo()`.  Both are pure, but they
#       cost CPU microseconds and this tree has CPU-BUDGET GATES
#       (FS_SENT_REACH_CPU_US = 6000 aborts the sentinel-reach scan).
#   (B) THE PHASE VALUE ITSELF -- a consumer the enumeration missed.
#
# FOUR ARMS, and each contrast isolates one layer:
#   probe = FS_V522_PROBE_NOPUB  -> every read performed, nothing published
#   chan  = FS_V522_PHASE_ONLY   -> published, floor never raised
#   fired = as shipped
#
#   parent vs probe  ->  (A) alone      : the cost of the reads
#   probe  vs chan   ->  (B) alone      : the cost of the phase VALUE
#   chan   vs fired  ->  THE MECHANISM  : the cost of the FLOOR
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v523_build
mkdir -p "$B/chan"
rm -rf "$B/arms/c_opp" "$B/arms/c_base" "$B/arms/c_probe" "$B/arms/c_chan" "$B/arms/c_fired"
cp -R bots/_v488beltbreak2 "$B/arms/c_opp"; chmod -R u+w "$B/arms/c_opp"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/c_opp/doctrine.py"
cp -R "$B/arms/parent" "$B/arms/c_base"; chmod -R u+w "$B/arms/c_base"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/c_base/doctrine.py"
cp -R bots/_v522floor "$B/arms/c_probe"; chmod -R u+w "$B/arms/c_probe"
{ echo ""; echo "FS_V522_PROBE_NOPUB = True"; echo "NOISE_ON = False"; } >> "$B/arms/c_probe/doctrine.py"
cp -R bots/_v522floor "$B/arms/c_chan"; chmod -R u+w "$B/arms/c_chan"
{ echo ""; echo "FS_V522_PHASE_ONLY = True"; echo "NOISE_ON = False"; } >> "$B/arms/c_chan/doctrine.py"
cp -R bots/_v522floor "$B/arms/c_fired"; chmod -R u+w "$B/arms/c_fired"
{ echo ""; echo "NOISE_ON = False"; } >> "$B/arms/c_fired/doctrine.py"
rm -rf "$B"/arms/c_*/__pycache__

a_n=0; a_d=0; b_n=0; b_d=0; m_n=0; m_d=0
for m in atoll drakkarfjord glacierkeep midgard nordkap yulerune; do
  for seat in A B; do
    for arm in base probe chan fired; do
      T="$B/arms/c_$arm"
      if [ "$seat" = A ]; then F="$T"; S="$B/arms/c_opp"; else F="$B/arms/c_opp"; S="$T"; fi
      .venv/bin/fcode run "$F" "$S" "maps/$m.map26" --seed 7 --tle 10 \
          --replay "$B/chan/${m}_${seat}_${arm}.replay26" >/dev/null 2>&1
    done
    p=$(md5 -q "$B/chan/${m}_${seat}_base.replay26")
    q=$(md5 -q "$B/chan/${m}_${seat}_probe.replay26")
    r=$(md5 -q "$B/chan/${m}_${seat}_chan.replay26")
    t=$(md5 -q "$B/chan/${m}_${seat}_fired.replay26")
    [ "$p" = "$q" ] && a_n=$((a_n+1)) || a_d=$((a_d+1))
    [ "$q" = "$r" ] && b_n=$((b_n+1)) || b_d=$((b_d+1))
    [ "$r" = "$t" ] && m_n=$((m_n+1)) || m_d=$((m_d+1))
    echo "$m $seat  A_reads=$([ "$p" = "$q" ] && echo SAME || echo DIFF)  B_phaseval=$([ "$q" = "$r" ] && echo SAME || echo DIFF)  MECH_floor=$([ "$r" = "$t" ] && echo SAME || echo DIFF)"
  done
done
echo "(A) parent vs PROBE  [extra engine reads]  : identical $a_n / differing $a_d"
echo "(B) PROBE  vs CHAN   [the phase VALUE]     : identical $b_n / differing $b_d"
echo "(M) CHAN   vs FIRED  [THE FLOOR ITSELF]    : identical $m_n / differing $m_d"
