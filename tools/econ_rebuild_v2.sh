#!/bin/zsh
# econ_rebuild_v2.sh — one-shot rebuild of corpus/econ.tsv under the v2 schema
# (s39, 2026-08-14). WHY: the s36 COLS widening (17->19) was never followed by a
# rebuild, so 31,986 rows sat column-shifted under the stale header; and the
# decoder never counted CORE turns in any era (9-15% cpu/turns undercount).
# This script: stops the keeper (sync appends would race the swap), re-decodes
# every ledgered file in 12 chunks / 3-wide, concatenates under ONE header,
# GATES the swap on width+coverage sanity, swaps atomically, restarts the
# keeper. Old table kept as corpus/econ.tsv.pre-v2-<ts>. Rows are never mixed:
# a failed gate leaves the old table in place and says so loudly.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
TS=$(date -u +%Y%m%dT%H%M%SZ)
RB=corpus/_rebuild
say() { echo "[$(date -u +%H:%M:%SZ)] $*"; }

say "stopping keeper for the rebuild window"
.venv/bin/python tools/corpus/keeper.py --stop || true

rm -rf $RB && mkdir -p $RB
# portable chunking: macOS split has no -n l/N
total=$(wc -l < corpus/decoded.txt | tr -d ' ')
per=$(( (total + 11) / 12 ))
split -l $per corpus/decoded.txt $RB/chunk_
chunks=($RB/chunk_*)
say "${#chunks[@]} chunks over $(wc -l < corpus/decoded.txt | tr -d ' ') ledgered files, 3-wide"

i=0
for group in 1 2 3 4; do
  pids=()
  for k in 1 2 3; do
    i=$((i+1))
    (( i > ${#chunks[@]} )) && break
    c=${chunks[$i]}
    ( files=()
      while read -r f; do [[ -f "replay_archive/$f" ]] && files+=("replay_archive/$f"); done < "$c"
      .venv/bin/python tools/corpus/replay_econ.py $RB/part_$(printf '%02d' $i).tsv "${files[@]}" \
        2> $RB/part_$(printf '%02d' $i).err ) &
    pids+=($!)
  done
  for p in $pids; do wait $p; done
  say "group $group done"
done

say "concatenating"
head -1 $RB/part_01.tsv > corpus/econ.tsv.new
for p in $RB/part_*.tsv; do tail -n +2 "$p" >> corpus/econ.tsv.new; done

# ---- SWAP GATES: refuse a bad table rather than install it ----
widths=$(awk -F'\t' 'NR>1 {c[NF]++} END {n=0; for (k in c) n++; print n}' corpus/econ.tsv.new)
w19=$(awk -F'\t' 'NR>1 && NF==19' corpus/econ.tsv.new | head -1 | wc -l | tr -d ' ')
nfiles=$(awk -F'\t' 'NR>1 {f[$1]=1} END {print length(f)}' corpus/econ.tsv.new)
ledger=$(wc -l < corpus/decoded.txt | tr -d ' ')
errs=$(cat $RB/part_*.err 2>/dev/null | grep -c '^ERR ' || true)
say "gates: distinct widths=$widths (want 1, all 19: nonzero=$w19)  files=$nfiles/$ledger  decode errors=$errs"
if [[ "$widths" != "1" || "$w19" != "1" ]]; then
  say "*** GATE FAILED: mixed or wrong row widths — OLD TABLE KEPT, new left at econ.tsv.new ***"
  .venv/bin/python tools/corpus/keeper.py --start || true
  exit 1
fi
if (( nfiles < ledger - errs - 50 )); then
  say "*** GATE FAILED: coverage $nfiles << ledger $ledger minus $errs errors — OLD TABLE KEPT ***"
  .venv/bin/python tools/corpus/keeper.py --start || true
  exit 1
fi

mv corpus/econ.tsv corpus/econ.tsv.pre-v2-$TS
mv corpus/econ.tsv.new corpus/econ.tsv
say "swapped: old table at corpus/econ.tsv.pre-v2-$TS"

.venv/bin/python tools/corpus/keeper.py --start || true
say "keeper restarted"
say "DONE — $nfiles files, $errs decode errors, single 19-col schema"
