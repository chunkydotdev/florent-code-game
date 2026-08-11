#!/usr/bin/env zsh
# HEAD-TO-HEAD vs the previous line iteration. `tools/h2h.sh <botdir> [seeds] [maps]`
#
# WHY THIS EXISTS (Magnus, 2026-08-11): "A good new bot should be showing signs
# early in head to head games." And: "Loki is a type of bot that can be run
# against itself to find improvements."
#
# ⛔ IT EXISTS BECAUSE I HAD DRIFTED OFF LOCAL GAMES ENTIRELY. Both dose checks
# I ran on 2026-08-11 used `bots/_det_opp_v63` -- one of OUR OWN PROBES, the
# fixture `PROGRAMME.md` says lies in a known direction (five probes share a
# `best_core or best_any` short-circuit; ZERO of our forward turrets died in 480
# arena games against 46.9% on the ladder). I read "prototypes go at live teams,
# not at our own probes" as "do not run local games", which is not what it says.
#
# **THE RIGHT LOCAL FIXTURE WAS ALWAYS IN THE PROGRAMME: `COMPARE_AGAINST:
# previous_line_iteration`. v104 is a real, current, competent bot and it does
# NOT have the probe defect.** Self-play against it is free, instant, unlimited,
# and needs no rate-limit slot.
#
# FIRST USE, and it paid for itself immediately: LOKI-22 (the rush flag flipped
# back on) went **16 wins / 64 games = 25%** across 8 maps x both seats x 4
# seeds -- reproducing a 2026-08-09 arena refutation on a fixture without the
# probe bias, and saving the live window I was about to spend on it.
#
# ⭐ THE NULL IS A STANDING ASSET, NOT A PER-LEG ARTEFACT. Build it ONCE at full
# power and every later screen is measured against a settled bar instead of
# re-litigating one. The 64-game null (32/64 = 50.0%) is committed; a 4,096-game
# null is running for the same reason. **A treatment run belongs to its plank and
# dies with it; the null belongs to the harness and outlives every plank.**
#
# ⚠ WHAT IT IS AND IS NOT. This is a PRIORITISATION instrument, not a D12
# closure: deterministic, self-play, and self-play is not the field.
# `FIXTURE_OF_RECORD: live_unrated` is unchanged. A plank that dies here is
# demoted, not retired; a plank that lives here has earned a live window.
# BOTH SEATS ARE ALWAYS PLAYED -- a one-seat result is a seat measurement.
set -u
BOT=${1:?usage: h2h.sh <botdir> [seeds] [maps]}
CTRL=${CTRL:-bots/_v130loki13}
SEEDS=${2:-"7 11 23 41"}
MAPS=${3:-"antler atoll drumlin fjordgate heart hive meander nordkap"}
FC=.venv/bin/fcode
B=$(basename $BOT)
C=$(basename $CTRL)
# ⛔ IDENTICAL BASENAMES ARE UNSCORABLE. `fcode` names the winner by basename, so
# a bot run against itself matches the treatment pattern in EVERY game and reads
# 100%. The self-check caught exactly that on this file's first run. The honest
# null is a RENAMED COPY of the control, which is byte-identical in behaviour and
# distinguishable on the wire.
if [[ $B == $C ]]; then
  print "REFUSING: treatment and control share the basename '$B'."
  print "  fcode reports the winner by basename, so every game would score as a"
  print "  treatment win. Copy the control to a new directory name for a null run."
  print "H2H_RESULT: UNSCORABLE 0/0"
  exit 2
fi
W=0; N=0; KILLW=0; KILLL=0; R1000=0
WA=0; NA=0; WB=0; NB=0
typeset -A MW MN
typeset -a TW_TURNS CW_TURNS
typeset -a TSCORE CSCORE
typeset -a TKR CKR
TKILL=0; CKILL=0; TTIE=0; CTIE=0
for S in ${=SEEDS}; do
  for M in ${=MAPS}; do
    for ORD in A B; do
      if [[ $ORD == A ]]; then OUT=$($FC run $BOT $CTRL maps/$M.map26 --seed $S 2>&1)
      else                     OUT=$($FC run $CTRL $BOT maps/$M.map26 --seed $S 2>&1); fi
      L=$(print -r -- "$OUT" | grep -i "Winner:" | head -1)
      [[ -z $L ]] && { print -r -- "  !! no winner line: $M seed $S seat $ORD"; continue; }
      N=$((N+1))
      if [[ $ORD == A ]]; then NA=$((NA+1)); else NB=$((NB+1)); fi
      MN[$M]=$(( ${MN[$M]:-0} + 1 ))
      case "$L" in *"$B"*) W=$((W+1)); MW[$M]=$(( ${MW[$M]:-0} + 1 )); [[ $ORD == A ]] && WA=$((WA+1)) || WB=$((WB+1))
                          [[ $L == *"Core destroyed"* ]] && KILLW=$((KILLW+1));;
                   *)                 [[ $L == *"Core destroyed"* ]] && KILLL=$((KILLL+1));; esac
      [[ $L == *"turn 1000"* ]] && R1000=$((R1000+1))
      # ⭐ CONTINUOUS OUTCOME. Win/loss is ONE BIT and it is the noisiest thing
      # the engine offers -- at n=64 it can only see a ~12pp swing, so a genuine
      # +2-3pp (worth ~+64 rating over 100 matches) is INVISIBLE to it. The turn
      # number is free, already on the same line, and a kill-round distribution
      # carries far more information per game than a win count. Eleven arms were
      # screened on the one-bit version before this was added.
      TN=${L##*turn }; TN=${TN%%[!0-9]*}
      if [[ -n $TN ]]; then
        case "$L" in *"$B"*) TW_TURNS+=($TN);; *) CW_TURNS+=($TN);; esac
      fi
      # ⛔ THE PRIMARY CURRENCY. `PROGRAMME.md`: PRIMARY_CURRENCY: kill_speed_score
      # and WIN_RATE_IS_VERDICT: no. Nine arms were screened on WIN RATE before
      # this line existed -- D3 on the drift checklist, running all day.
      # Scored with tools/score.py's OWN buckets so the two instruments cannot
      # drift apart. Censoring is not missing data: a game with no kill is a
      # LOSS or a TIEBREAK and both score -10, which is the worst bucket -- the
      # currency already answers the question a kill-round median cannot.
      CONDW="core_destroyed"; [[ $L == *"tiebreak"* ]] && CONDW="tiebreak"
      # DECOMPOSE. kill_speed_score is a deterministic function of
      # (won, cond, turns), so P(core-kill win) and kill-round-given-a-kill are
      # SUFFICIENT for it -- decomposing loses nothing and gains resolution.
      # MEASURED JUSTIFICATION: 94.5% of the score's variance is the BINARY
      # "did we kill at all"; only 5.5% is the speed it exists to reward. The
      # scorecard is a VALUE STATEMENT and is left unchanged; this changes what
      # the SCREEN reports, not what any bar is.
      if [[ $CONDW == core_destroyed ]]; then
        case "$L" in *"$B"*) TKILL=$((TKILL+1)); TKR+=($TN);;
                     *)      CKILL=$((CKILL+1)); CKR+=($TN);; esac
      else
        case "$L" in *"$B"*) TTIE=$((TTIE+1));; *) CTIE=$((CTIE+1));; esac
      fi
      case "$L" in
        *"$B"*) TSCORE+=($(.venv/bin/python -c "import sys;sys.path.insert(0,'tools');import score;print(score.game_score(True,'$CONDW',$TN))"))
                CSCORE+=(-10);;
        *)      CSCORE+=($(.venv/bin/python -c "import sys;sys.path.insert(0,'tools');import score;print(score.game_score(True,'$CONDW',$TN))"))
                TSCORE+=(-10);;
      esac
    done
  done
done
print ""
print "H2H  $B  vs  $C"
print "  games $N   (both seats always played)"
print "  WINS  $W = $(( N ? 100*W/N : 0 ))%"
print "  core kills FOR $KILLW   AGAINST $KILLL   r1000 (a DEFEAT either way) $R1000"
# PER-SEAT, because a pooled rate hides a seat effect and the NULL control read
# 44% rather than 50% on 60 games. If a byte-identical copy wins far more from
# one seat than the other, the engine or the harness is asymmetric and every
# screen verdict is measured against a bent ruler.
print "  seat A (treatment first)  $WA/$NA     seat B (treatment second)  $WB/$NB"
# PER-MAP, because a pooled 8-map rate can be "harmful on short maps, neutral on
# long" and read identically to "harmful everywhere". The rush was measured at
# -35.4pp on SHORT maps (p=0.0005) and NULL on long ones in 2026-08-09's paired
# battery -- so a pooled number hides the only fact that would change its status.
# Free: the split is already in the games we just played.
print -n "  per map: "
for m in ${=MAPS}; do print -n "$m ${MW[$m]:-0}/${MN[$m]:-0}  "; done
print ""
# GATE ON THIS LINE, NEVER ON $? -- the natural `h2h.sh ... | tail` makes $? the
# pipe's, which is always 0. Repo standing rule.
# ⛔ POWER WARNING, AND IT IS NOT DECORATION. At n=24 the smallest count that
# separates from a 50% null at p<0.05 is 7/24 -- so 10/24 (41%) and 14/24 (58%)
# are BOTH indistinguishable from doing nothing. Measured the hard way on
# 2026-08-11: LOKI_FWD_GUN_CAP 3->6 read 14/24 = 58% and was reported as "the
# first thing above the null"; at n=64 it read 32/64 = EXACTLY 50%. The null
# control itself read 44% at n=36 and 50.0% at n=64. **Two false signals from
# the same instrument in one hour, both from small n.**
# ⛔⛔ THE VERDICT IS THE BAND, NOT THE PERCENTAGE. THIS FILE SPENT A DAY
# REPORTING NON-RESULTS AS REFUTATIONS.
#   n=  24 -> detects only >= +28.6pp     n= 256 -> >= +8.8pp
#   n=  64 -> detects only >= +17.5pp     n=4096 -> >= +2.2pp
# **LOKI-13, THE BEST PLANK THIS PROJECT HAS EVER SHIPPED, MEASURED +18.0pp.
# THE n=64 THRESHOLD IS +17.5pp.** A LOKI-13-sized effect is a coin flip to be
# filed as "not distinguishable". **We calibrated a filter to reject everything
# short of our own best-ever result**, and on 2026-08-11 SEVEN OF NINE arms fell
# inside the band and were written up as failures. They produced NO INFORMATION.
# A false POSITIVE costs one window -- 25 games, bounded, visible. A false
# NEGATIVE costs a plank nobody ever learns about -- unbounded, invisible. Seven
# filters were built that day and zero generators.
# ⇒ INSIDE THE BAND RETURNS THE PLANK TO THE POOL. It is NOT a demotion.
BAND=$(print -r -- $N $W | awk '{ n=$1; hw=1.96*sqrt(0.25/n);
  printf "%d %d %.0f %.0f", (0.5-hw)*n, (0.5+hw)*n, (0.5-hw)*100, (0.5+hw)*100 }')
LOC=${BAND[(w)1]}; HIC=${BAND[(w)2]}; LOP=${BAND[(w)3]}; HIP=${BAND[(w)4]}
if (( W <= LOC )); then
  VERDICT="OUTSIDE-BELOW real negative"
elif (( W >= HIC )); then
  VERDICT="OUTSIDE-ABOVE escalate"
else
  VERDICT="NO-INFORMATION back to the pool, NOT demoted"
fi
print ""
print "  informative band at n=$N: <=$LOC or >=$HIC wins  (${LOP}%-${HIP}% is noise)"
print "  VERDICT: $VERDICT"
med() { print -r -- ${(n)@} | tr " " "\n" | awk '{a[NR]=$1} END{if(NR)print (NR%2)?a[(NR+1)/2]:int((a[NR/2]+a[NR/2+1])/2); else print "-"}'; }
mean() { print -r -- $@ | tr " " "\n" | awk '{s+=$1;n++} END{if(n)printf "%.2f",s/n; else print "-"}'; }
print ""
print "  ⭐⭐ SCREENING STATISTICS (the score is DECISION-ONLY, not the screen)"
printf "      P(core-kill win)   %-14s %5.1f%%  (%d/%d)\n" $B $((100*TKILL/N)) $TKILL $N
printf "                         %-14s %5.1f%%  (%d/%d)\n" $C $((100*CKILL/N)) $CKILL $N
printf "      kill round | kill  %-14s median %s   n=%d\n" $B "$(med $TKR)" ${#TKR[@]}
printf "                         %-14s median %s   n=%d\n" $C "$(med $CKR)" ${#CKR[@]}
printf "      tiebreak wins      %-14s %d        %-14s %d   (both score -10 BY DESIGN,\n" $B $TTIE $C $CTIE
print  "                         and they are completely different states — 48.8% of live-era games sit here)"
# ⛔ THE TRAP THE DECOMPOSITION CREATES. "kill round GIVEN a kill" is CONDITIONED
# ON THE OUTCOME. A plank that kills only the EASY games posts a BETTER
# speed-given-kill and a WORSE P(kill) -- a selection effect that looks like an
# improvement on the line just promoted to primary. The pooled score at least
# averaged that trade away; the decomposition ADVERTISES half of it. So the two
# halves must be read together and any opposite movement is flagged.
SEL=$(print -r -- $TKILL $CKILL "$(med $TKR)" "$(med $CKR)" | awk '{
  if ($3=="-" || $4=="-") { print ""; exit }
  pk = ($1 > $2); spd = ($3 < $4);          # lower kill round = faster = better
  if (!pk && spd) print "P(kill) DOWN but speed-given-kill UP -- SELECTION EFFECT: it may be killing only the easy games";
  else if (pk && !spd) print "P(kill) UP but speed-given-kill DOWN -- the two halves disagree";
  else print "" }')
if [[ -n $SEL ]]; then
  print ""
  print "  ⚠⚠ $SEL"
  print "     Read the two halves TOGETHER. Neither alone is the result."
fi
print ""
print "  KILL-SPEED SCORE (DECISION-ONLY — PROGRAMME.md: win rate is NOT the verdict)"
print "      $B  mean $(mean $TSCORE) /game        $C  mean $(mean $CSCORE) /game"
print "      (tools/score.py buckets; a tiebreak win and a loss both score -10)"
print ""
# ⛔ THE PROXY CAN DISAGREE WITH THE GOAL, AND THAT DISAGREEMENT IS THE ONLY
# CASE WHERE IT MISLEADS. Magnus: "The goal for any of this is to climb ELO."
# `PROGRAMME.md` says PRIMARY_CURRENCY: kill_speed_score. They are NOT the same
# objective: **the ladder pays GAME SHARE (delta = 32 x (S - E)), so a plank that
# kills FASTER while winning FEWER games gains kill-speed and LOSES Elo.**
# Both numbers are already computed here, so flagging the divergence is free.
KS_T=$(mean $TSCORE); KS_C=$(mean $CSCORE)
DIVERGE=$(print -r -- $KS_T $KS_C $W $N | awk '{
  ks = ($1 > $2); wr = ($3/$4 > 0.5);
  if (ks && !wr) print "KILL-SPEED UP, WIN RATE DOWN -- the proxy and the goal DISAGREE";
  else if (!ks && wr) print "WIN RATE UP, KILL-SPEED DOWN -- the proxy and the goal DISAGREE";
  else print "" }')
if [[ -n $DIVERGE ]]; then
  print ""
  print "  ⚠⚠ $DIVERGE"
  print "     The ladder pays GAME SHARE. Read the Elo consequence, not the proxy."
fi
print ""
print "  --- secondary, and NOT the verdict ---"
print "  KILL ROUND (continuous, far more power than the win count):"
print "    when $B wins:  n=${#TW_TURNS[@]}  median $(med $TW_TURNS)"
print "    when $C wins:  n=${#CW_TURNS[@]}  median $(med $CW_TURNS)"
print "H2H_RESULT: $B $W/$N $VERDICT"
