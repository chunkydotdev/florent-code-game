#!/bin/zsh
# LOKI-42 live leg. Every step verified on the LOAD-BEARING FIELD, never on $?
# (fcode exits 0 while printing `Error: True`).
set -u
BOT=bots/_v169launchlate160
OPP=f670dfed-dfee-421b-8c01-a67b8a278ce3     # The Bisons, 1682
log(){ print -r -- "[$(date -u '+%H:%M:%S')] $*" }

# ⛔ READ THE HOLDER LIVE. The previous draft hardcoded 114 and would have
# "restored" a version that had not held the slot since 08:57Z, silently
# demoting x3r0's v115. The holder is a FACT TO READ AT FIRE TIME, never a
# constant carried from a document.
HOLDER=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:' | sed 's/.*Active bot: *//' | awk '{print $1}')
VER=$(print -r -- "$HOLDER" | tr -cd '0-9')
if [[ -z "$VER" ]]; then log "!! CANNOT READ HOLDER -- ABORT"; exit 1; fi
log "HOLDER READ LIVE: $HOLDER (restore target v$VER)"

log "SUBMIT -- this ACTIVATES. Window starts NOW."
.venv/bin/python tools/submit_clean.py "$BOT" --activate 2>&1 | tail -3
LIVE=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:')
log "LIVE: $LIVE"
if [[ "$LIVE" != *"Active bot"* ]]; then
  log "!! NO Active bot LINE -- RESTORING v$VER AND ABORTING"
  .venv/bin/fcode submission activate "$VER"; exit 1
fi

for i in 1 2 3 4 5; do
  log "unrated $i/5"
  .venv/bin/fcode match unrated "$OPP" 2>&1 | tail -1
done

log "ROLLBACK to v$VER"
.venv/bin/fcode submission activate "$VER" 2>&1 | tail -1
BACK=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:')
log "HOLDER NOW: $BACK"
if [[ "$BACK" == *"v$VER"* ]]; then log "ROLLBACK VERIFIED on the Active bot line"
else log "!! ROLLBACK NOT VERIFIED -- BY HAND: fcode submission activate $VER"; fi
