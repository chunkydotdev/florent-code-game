#!/bin/zsh
set -u
BOT=bots/_v171launch0ammo
log(){ print -r -- "[$(date -u '+%H:%M:%S')] $*" }
HOLDER=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:' | sed 's/.*Active bot: *//' | awk '{print $1}')
VER=$(print -r -- "$HOLDER" | tr -cd '0-9')
[[ -z "$VER" ]] && { log "!! CANNOT READ HOLDER -- ABORT"; exit 1; }
log "HOLDER READ LIVE: $HOLDER (restore v$VER)"
log "SUBMIT -- ACTIVATES NOW"
.venv/bin/python tools/submit_clean.py "$BOT" --activate 2>&1 | tail -2
LIVE=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:')
log "LIVE: $LIVE"
[[ "$LIVE" != *"Active bot"* ]] && { log "!! ABORT, RESTORING"; .venv/bin/fcode submission activate "$VER"; exit 1; }
# same opponents AND same maps as the v116 burst -> paired contrast
fire(){ log "$1"; .venv/bin/fcode match unrated "$2" ${@:3} 2>&1 | tail -1 }
fire Leviathan     26286680-d861-4f9e-9073-a6201bd48d3b --map moonrise --map meander --map fjordgate --map nordkap --map jackpot
fire Coreflood     ea0d33c8-ca2b-497a-9be0-1837379eab1e --map heart --map lighthouse --map saga --map hive --map moonrise
fire 0033          74ae65ff-96ae-4da5-a43e-692eb6fee38f --map snowflake --map atoll --map nordkap --map fjordgate --map drumlin
fire BeanCounters  47803c19-e264-4492-bd62-fbdd58cfd7e6 --map meander --map hive --map moonrise --map drumlin --map fjordgate
fire SmartFridge   7fd91e77-812c-44da-bce7-457be94d2548 --map atoll --map drumlin --map snowflake --map eider --map saga
log "ROLLBACK to v$VER"
.venv/bin/fcode submission activate "$VER" 2>&1 | tail -1
BACK=$(.venv/bin/fcode status 2>/dev/null | grep 'Active bot:')
log "HOLDER NOW: $BACK"
[[ "$BACK" == *"v$VER"* ]] && log "ROLLBACK VERIFIED" || log "!! ROLLBACK NOT VERIFIED -- activate $VER BY HAND"
