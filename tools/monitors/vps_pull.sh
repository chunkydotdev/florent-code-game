#!/usr/bin/env bash
# vps_pull.sh — fleet constraint #4 made real: remote TSVs rsync back on a
# cadence so the ONE status authority (corefill_status → dashboard) stays
# local and current. Reads hosts from scratchpad/vps/hosts.txt (one per
# line, # comments ok). Each cycle logs per-host row counts + the pull's
# own success/failure — a silent pull failure would make remote shards look
# stalled, so failures print loudly and the log line carries the clock.
cd "$(dirname "$0")/../.." || exit 2
HOSTS=${HOSTS:-scratchpad/vps/hosts.txt}
INTERVAL=${INTERVAL:-300}
while :; do
  if [ -r "$HOSTS" ]; then
    grep -v '^#' "$HOSTS" | while read -r h; do
      [ -n "$h" ] || continue
      if bash tools/vps/orchestrate.sh pull "$h" > /dev/null 2>&1; then
        printf '%s pull ok %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$h"
      else
        printf '%s ⛔ PULL FAILED %s — remote shards will read stale until this recovers\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$h"
      fi
    done
  else
    printf '%s ⛔ BLIND: no hosts file at %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$HOSTS"
  fi
  sleep "$INTERVAL"
done
