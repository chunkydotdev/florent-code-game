---
tactic: Destroy-and-rebuild as a resource/scale converter
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: Battlecode 2025 — Gone Whalin' (originators), Just Woke Up, confused, Om Nom all describe it
evidence: documented
transfers: partial
---
WHAT IT IS — "tower flickering"/"nuking": destroy your own building and rebuild
it to convert one resource into another, because buildings spawn with a resource
endowment. Om Nom: "each tower spawns with 500 paint, allowing you to trade 1000
money for 500 paint." Three of the four 2025 postmortems independently found it.
It was nerfed mid-season once towers gained a build cost.

WHY IT MIGHT TRANSFER — **not the resource conversion (we have no building
endowment), but the SCALE side.** Our builder measured today that cost scale is a
**single global multiplier tracking LIVE entities** — a destroyed entity stops
contributing. `destroy()` is free, costs no action cooldown, and is unlimited per
turn. So **destroying dead-weight conveyors late lowers the price of everything
bought afterwards**, which is exactly the constraint that will bite a late
gunline (each gunner is +20 points of global scale).

WHAT WOULD KILL IT — if the pruned conveyors were still carrying titanium, the
delivery loss exceeds the price saving; and delivered titanium is tiebreak key
#1. This needs the arithmetic done, not assumed.

BUILDER HOOK — this is already a live plank idea (LOKI-2 "destroy/prune
doctrine"). The corpus can price it: `corpus/build_agg.tsv` has per-band conveyor
build counts, and we build 9.4 conveyors/game in r200-300 against their 5.3
while delivering less.
