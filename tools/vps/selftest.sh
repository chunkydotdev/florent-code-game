#!/usr/bin/env bash
# VPS CHAIN ACCEPTANCE TEST — the whole system, WITHOUT A SERVER.
#
# ⛔ DRAFT — UNTESTED. Authored by the s36 VPS agent, which was killed AT the
# acceptance-test step (s36 wrap note, 2026-08-13T16:41Z): this script has
# NEVER completed a run. Do not trust it until it has run green and the run is
# recorded; until then it is exactly the artefact class the drift-watch lesson
# names (a test whose passing has never been observed).
#
#   bash tools/vps/selftest.sh [scratch_dir]
#
# ⭐ WHY THIS EXISTS AND WHY IT IS NOT OPTIONAL. The point of building the VPS
# machinery before the server arrives is that provisioning becomes ~15 minutes
# of runbook rather than an afternoon of debugging over ssh. That is only true
# if the chain has ALREADY RUN. So this drives the real thing:
#
#     gen → push → [4 REFUSAL GATES, each driven to the OTHER verdict] →
#     NULLHOST-first run at WORKERS=2 → STOP → resume → pull → reader
#     certification BOTH WAYS (real null CERTIFIED, doctored null EXCLUDED)
#
# ⛔ WHAT IS **NOT** COVERED, STATED UP FRONT RATHER THAN DISCOVERED LATER:
#    the network transport. `ssh` is not available to this session, so the run
#    uses `--local-sim`, which swaps `ssh host cmd` for `bash -c cmd` and
#    `rsync -e ssh host:path` for local `rsync` — SAME rsync flags, SAME remote
#    command strings, SAME snapshot contents, SAME gates. What is untested is
#    exactly: key auth, ssh-config alias resolution, and rsync-over-ssh. Those
#    are the three things `orchestrate.sh setup` and the runbook's first two
#    commands exercise on the real host, and they fail LOUDLY (the push has a
#    post-push presence check that gates on the LOAD-BEARING FILE, not on `$?`).
#
# Each gate below must be shown REFUSING and, after the cause is removed, must
# be shown PASSING. A gate that has never produced the other verdict has not
# been seen to gate.
set -u
REPO=$(cd "$(dirname "$0")/../.." && pwd)
cd "$REPO"
SCRATCH=${1:-${TMPDIR:-/tmp}/vps_selftest.$$}
SIM=$SCRATCH/server/fcode-worker
WORKLIST=$SCRATCH/src_worklist.txt
LOCALDIR=$SCRATCH/local_overnight
PULLDIR=$SCRATCH/pulled
ORCH="tools/vps/orchestrate.sh"
PY=.venv/bin/python
fails=0
step() { printf '\n\033[1m═══ %s\033[0m\n' "$*"; }
ok()   { printf '  [ok]   %s\n' "$*"; }
bad()  { printf '  [FAIL] %s\n' "$*"; fails=$(( fails + 1 )); }
want_rc() { # want_rc <expected> <actual> <label>
  if [ "$2" -eq "$1" ]; then ok "$3 (rc=$2)"; else bad "$3 — expected rc=$1, got rc=$2"; fi
}

mkdir -p "$SCRATCH" "$LOCALDIR" "$PULLDIR"
export PULL_ROOT=$PULLDIR
export LOCAL_ROOT=$SCRATCH/gen

# A two-row source worklist: a byte-identical pair (so `gen` can find a NULL
# structurally) and one real contrast. Real trees, real maps, real engine.
cat > "$WORKLIST" <<'EOF'
# test source worklist
NULL125 bots/_v198null125 bots/_v197mapcode 5400 215000
MINI    bots/_v205combo   bots/_v197mapcode 5400 225000
EOF

step "1. GEN — seed partition + structural NULL discovery"
bash "$ORCH" gen localhost MINI --from "$WORKLIST" --null-target 40 --target 40 --local-sim "$SIM"
rc=$?; want_rc 0 "$rc" "gen"
echo "--- generated worklist ---"; cat "$SCRATCH/gen/localhost/worklist.txt"
echo "--- sidecar ---"; cat "$SCRATCH/gen/localhost/SEED_OFFSET.sidecar"

step "2. GEN REFUSES a source with no byte-identical pair (the OTHER verdict)"
printf 'MINI bots/_v205combo bots/_v197mapcode 40 1\n' > "$SCRATCH/nonull.txt"
bash "$ORCH" gen localhost --from "$SCRATCH/nonull.txt" --local-sim "$SIM" >/dev/null 2>&1
want_rc 2 $? "gen refuses when no NULL cell can be constructed"
# restore the good worklist (the refusal above must not have clobbered it)
bash "$ORCH" gen localhost MINI --from "$WORKLIST" --null-target 40 --target 40 --local-sim "$SIM" >/dev/null

step "3. PUSH — minimal snapshot"
bash "$ORCH" push localhost --local-sim "$SIM"
want_rc 0 $? "push"
echo "--- what landed on the 'server' ---"
( cd "$SIM" && find . -maxdepth 2 -not -path '*/bots/*/*' | sort | head -40 )
echo "--- snapshot size vs repo ---"
printf '  snapshot: %s   repo(bots+maps+docs+corpus): %s\n' \
  "$(du -sh "$SIM" | awk '{print $1}')" "$(du -sh bots maps docs corpus 2>/dev/null | awk '{s=$1} END{print "(see below)"}')"
du -sh "$SIM" bots maps docs corpus replay_archive 2>/dev/null | sed 's/^/  /'
for forbidden in docs corpus replay_archive scratchpad .git elo_history.tsv fcode.toml; do
  if [ -e "$SIM/$forbidden" ]; then bad "LEAK: $forbidden is on the worker"; else ok "not shipped: $forbidden"; fi
done

step "4. GATE G1 — no venv ⇒ REFUSE with the exact setup commands"
( cd "$SIM" && bash tools/vps/worker.sh ) ; want_rc 3 $? "worker refuses with no engine"

step "   G1 satisfied — the sim shares this box's venv (same engine, same pin)"
ln -sfn "$REPO/.venv" "$SIM/.venv"
ok "symlinked $SIM/.venv -> $REPO/.venv"

step "5. GATE G2 — ENGINE PIN mismatch ⇒ REFUSE"
cp "$SIM/tools/ENGINE_PIN" "$SCRATCH/PIN.bak"
printf '9.9.9\n' > "$SIM/tools/ENGINE_PIN"
( cd "$SIM" && bash tools/vps/worker.sh ) 2>&1 | sed 's/^/  | /' | head -6
rc=${PIPESTATUS[0]}
( cd "$SIM" && bash tools/vps/worker.sh ) >/dev/null 2>&1; want_rc 4 $? "worker refuses on engine pin mismatch"
cp "$SCRATCH/PIN.bak" "$SIM/tools/ENGINE_PIN"; ok "pin restored"

step "6. GATE G3 — maps/ disagreeing with the shipped pool ⇒ REFUSE"
FIRSTMAP=$(head -1 "$SIM/work/MAPS.list")
mv "$SIM/maps/$FIRSTMAP.map26" "$SCRATCH/$FIRSTMAP.map26"
( cd "$SIM" && bash tools/vps/worker.sh ) 2>&1 | sed 's/^/  | /' | head -6
( cd "$SIM" && bash tools/vps/worker.sh ) >/dev/null 2>&1; want_rc 5 $? "worker refuses on a missing pool map"
mv "$SCRATCH/$FIRSTMAP.map26" "$SIM/maps/$FIRSTMAP.map26"
# ...and the other direction: an EXTRA map is equally a mismatch.
cp maps/atoll.map26 "$SIM/maps/atoll.map26" 2>/dev/null
( cd "$SIM" && bash tools/vps/worker.sh ) >/dev/null 2>&1; want_rc 5 $? "worker refuses on a RETIRED map present in maps/"
rm -f "$SIM/maps/atoll.map26"; ok "pool restored"

step "7. GATE G4 — basename collision ⇒ REFUSE (unscorable)"
cp "$SIM/work/worklist.txt" "$SCRATCH/wl.bak"
printf 'COLLIDE bots/_v197mapcode bots/_v197mapcode2 40 1\n' >> "$SIM/work/worklist.txt"
mkdir -p "$SIM/bots/_v197mapcode2"; cp "$SIM/bots/_v197mapcode/main.py" "$SIM/bots/_v197mapcode2/main.py"
( cd "$SIM" && bash tools/vps/worker.sh ) 2>&1 | grep -i 'collide\|REFUSE' | sed 's/^/  | /' | head -3
( cd "$SIM" && bash tools/vps/worker.sh ) >/dev/null 2>&1; want_rc 2 $? "worker refuses a substring basename collision"
cp "$SCRATCH/wl.bak" "$SIM/work/worklist.txt"; rm -rf "$SIM/bots/_v197mapcode2"; ok "worklist restored"

step "8. GATE — a worklist with NO NULLHOST row ⇒ REFUSE"
grep -v '^NULLHOST' "$SCRATCH/wl.bak" > "$SIM/work/worklist.txt"
( cd "$SIM" && bash tools/vps/worker.sh ) >/dev/null 2>&1; want_rc 6 $? "worker refuses a worklist with no NULLHOST cell"
cp "$SCRATCH/wl.bak" "$SIM/work/worklist.txt"; ok "worklist restored"

step "9. STOP FILE — set before launch ⇒ halts immediately, keeps rows"
touch "$SIM/STOP"
( cd "$SIM" && WORKERS=2 LOAD_CEIL=999 bash tools/vps/worker.sh ) 2>&1 | tail -3 | sed 's/^/  | /'
if [ -f "$SIM/results/NULLHOST.COMPLETE" ]; then bad "STOP did not prevent completion"; else ok "STOP honoured — no COMPLETE marker written"; fi
rm -f "$SIM/STOP"

step "10. REAL RUN — NULLHOST first, then MINI, WORKERS=2"
( cd "$SIM" && WORKERS=2 LOAD_CEIL=999 bash tools/vps/worker.sh ) 2>&1 | sed 's/^/  | /'
want_rc 0 $? "worker run"
echo "--- results ---"
for f in "$SIM"/results/*.tsv; do printf '  %-12s rows=%s\n' "$(basename "$f" .tsv)" "$(( $(wc -l < "$f") - 1 ))"; done
echo "--- heartbeats ---"; cat "$SIM"/results/*.heartbeat | sed 's/^/  | /'
echo "--- NULLHOST head ---"; head -4 "$SIM/results/NULLHOST.tsv" | sed 's/^/  | /'
echo "--- seat/map balance + seed range (NULLHOST) ---"
awk -F'\t' 'NR>1{s[$6]++; m[$4]++; if(!lo||$5<lo)lo=$5; if($5>hi)hi=$5} END{
  printf "  seats: "; for(k in s) printf "%s=%d ", k, s[k];
  printf "\n  distinct maps: %d   seed range: %s-%s\n", length(m), lo, hi}' "$SIM/results/NULLHOST.tsv"

step "11. RESUME — a completed shard is SKIPPED, not replayed"
( cd "$SIM" && WORKERS=2 LOAD_CEIL=999 bash tools/vps/worker.sh ) 2>&1 | grep -i 'SKIP\|COMPLETE' | sed 's/^/  | /'
n1=$(( $(wc -l < "$SIM/results/NULLHOST.tsv") - 1 ))
[ "$n1" -eq 40 ] && ok "NULLHOST still 40 rows after a second invocation" || bad "row count changed to $n1"

step "12. STATUS over the transport"
bash "$ORCH" status localhost --local-sim "$SIM" | sed 's/^/  | /'

step "13. PULL"
bash "$ORCH" pull localhost --local-sim "$SIM"
want_rc 0 $? "pull"
ls -1 "$PULLDIR/localhost" | sed 's/^/  | /'

step "14. READER — production floor (400): n=40 is NOT certified"
$PY tools/overnight_read.py --dir "$LOCALDIR" --include-remote --remote-dir "$PULLDIR" 2>&1 \
  | sed -n '/REMOTE BATTERY HOSTS/,$p' | head -30 | sed 's/^/  | /'

step "15. READER — smoke floor (40): the REAL null CERTIFIES"
$PY tools/overnight_read.py --dir "$LOCALDIR" --include-remote --remote-dir "$PULLDIR" --null-floor 40 2>&1 \
  | sed -n '/REMOTE BATTERY HOSTS/,$p' | head -30 | sed 's/^/  | /'

step "16. READER — DOCTORED null at 30% ⇒ host EXCLUDED (the other verdict)"
cp "$PULLDIR/localhost/NULLHOST.tsv" "$SCRATCH/NULLHOST.real.tsv"
awk -F'\t' -v OFS='\t' 'NR==1{print; next}{ $7 = (n<12 ? "T" : "C"); n++; print }' \
  "$SCRATCH/NULLHOST.real.tsv" > "$PULLDIR/localhost/NULLHOST.tsv"
awk -F'\t' 'NR>1{c[$7]++} END{printf "  doctored null: T=%d C=%d (%.0f%%)\n", c["T"], c["C"], 100*c["T"]/(c["T"]+c["C"])}' \
  "$PULLDIR/localhost/NULLHOST.tsv"
$PY tools/overnight_read.py --dir "$LOCALDIR" --include-remote --remote-dir "$PULLDIR" --null-floor 40 2>&1 \
  | sed -n '/REMOTE BATTERY HOSTS/,$p' | head -30 | sed 's/^/  | /'
cp "$SCRATCH/NULLHOST.real.tsv" "$PULLDIR/localhost/NULLHOST.tsv"; ok "real null restored"

step "17. SETUP — print-only by default"
bash "$ORCH" setup localhost --local-sim "$SIM" | sed 's/^/  | /'
bash "$ORCH" setup localhost --local-sim "$SIM" --execute >/dev/null 2>&1
want_rc 2 $? "setup --execute REFUSES under --local-sim (it would apt-get this box)"

printf '\n═══ RESULT: %s\n' "$([ "$fails" -eq 0 ] && echo 'ALL CELLS PASS' || echo "$fails FAILING CELL(S)")"
printf 'scratch kept at: %s\n' "$SCRATCH"
exit "$fails"
