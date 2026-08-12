#!/bin/zsh
set -u
log(){ print -r -- "[$(date -u '+%H:%M:%S')] $*" }
HOLDER=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:' | sed 's/.*Active bot: *//' | awk '{print $1}')
VER=$(print -r -- "$HOLDER" | tr -cd '0-9')
[[ -z "$VER" ]] && { log "!! CANNOT READ HOLDER -- ABORT"; exit 1; }
log "HOLDER READ LIVE: $HOLDER (restore v$VER)"
log "ACTIVATE v118 (_v171late160ammo, already uploaded -- no new version burned)"
.venv/bin/fcode submission activate 118 2>&1 | tail -1
LIVE=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:')
log "LIVE: $LIVE"
[[ "$LIVE" != *"v118"* ]] && { log "!! NOT v118 -- RESTORING v$VER"; .venv/bin/fcode submission activate "$VER"; exit 1; }
ok=0
fire(){ log "$1"; out=$(.venv/bin/fcode match unrated "$2" ${@:3} 2>&1 | tail -1); print -r -- "   $out"
        [[ "$out" == *"Rate limit"* ]] && log "   ^ REJECTED (counts against the window)" || ok=$((ok+1)) }
fire Leviathan    26286680-d861-4f9e-9073-a6201bd48d3b --map moonrise --map meander --map fjordgate --map nordkap --map jackpot
fire Coreflood    ea0d33c8-ca2b-497a-9be0-1837379eab1e --map heart --map lighthouse --map saga --map hive --map moonrise
fire 0033         74ae65ff-96ae-4da5-a43e-692eb6fee38f --map snowflake --map atoll --map nordkap --map fjordgate --map drumlin
fire BeanCounters 47803c19-e264-4492-bd62-fbdd58cfd7e6 --map meander --map hive --map moonrise --map drumlin --map fjordgate
log "ACCEPTED $ok/4"
log "ROLLBACK to v$VER"
.venv/bin/fcode submission activate "$VER" 2>&1 | tail -1
BACK=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:')
log "HOLDER NOW: $BACK"
[[ "$BACK" == *"v$VER"* ]] && log "ROLLBACK VERIFIED" || log "!! NOT VERIFIED -- activate $VER BY HAND"
