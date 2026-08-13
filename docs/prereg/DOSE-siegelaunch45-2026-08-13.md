# DOSE PREREG — LOKI-SIEGE-LAUNCH (#45, iteration 2): does the eviction road OPEN?

**Committed before any dose game (two-clock: this commit's git author time vs
the runs' wall clocks in the readout).** Builder s37, 2026-08-13. Follows
`DOSE-feeder45-2026-08-13.md` (iteration 1: dose NOT met — sentinel-only
exposure). Research's prioritisation and design requirement (coordination /
message 17:2xZ) are adopted verbatim and shape this arm:

## The plank

`bots/_v200siegelaunch` = incumbent `_v197mapcode` + `LOKI_SIEGE_LAUNCHER`:
when the unit deciding a launcher build can see an enemy gunner/sentinel
within `LOKI_SIEGE_DSQ=32` of our core, BOTH launcher gates are waived — the
round deferral (`LAUNCHER_MIN_RND=160`, vs measured siege onset r89-112) AND
the eco reserve (`LAUNCHER_RESERVE=80` → 0 under siege; research: the
Leviathan autopsy shows the bank pinned at ~12 Ti in exactly the sieged
games, so a round-gate-only waiver can null with the mechanism sound). The
launcher's existing EXILE path then evicts adjacent enemy builders — the
feeders — at 0 ammo against their 1-2-round rebuild economy. Single diff vs
incumbent (52 insertions, no feeder-first turret change — single planks
first).

## Tags (all local-only; platform strips stdout)

* `SIEGE45` — the waiver opened (round-gate branch).
* `GATE45 gate=<harvester|eco> …` — a LATER gate refused under siege, with
  its own arithmetic (bank/cost/reserve), so a no-fire attributes to a NAMED
  gate rather than to the plank.
* `EVICT45` — the exile path threw an enemy builder.
* `CREEP45` — fixture plant (unchanged fixture, frozen as of its first banked
  use per the side lane's boundary; any further fixture edit ships as
  `_probe_creeper2`).

## Arms and bars

Fixture: `bots/_probe_creeper` (unchanged; lie direction as recorded — it
overstates rebuild persistence and never retreats, which makes eviction
HARDER to show as feed-interruption, not easier: the evictee walks straight
back). 8 games × {midgard, frostgate}, kept replays, per-tag `strings`
counts, seeds 992001-8.

1. **FIXTURE VALIDITY:** CREEP45 in ≥6 of 8 games per map (treatment surface;
   the iteration-1 control at 8/8+8/8 stands as the no-treatment surface).
2. **DOSE BAR:** `EVICT45 ≥1` in ≥half of the games that show CREEP45 plants.
   **FALSIFIER: 0 EVICT45 across all valid games ⇒ the road did not open as
   built** — and the GATE45/SIEGE45 tags then name which gate held it shut:
   0 SIEGE45 ⇒ detection never fired (check LOKI_SIEGE_DSQ vs where plants
   land); SIEGE45>0 with GATE45(eco) ⇒ the bank is the binding gate (queue
   #28's territory, not this plank's); SIEGE45>0, no GATE45, no launcher ⇒
   the build-site loop is the suspect.
3. **OFF-BRANCH (2 games, frostgate, flag-off scratch copy,
   `LOKI_SIEGE_LAUNCHER=False`):** 0 SIEGE45/EVICT45/GATE45 tags WITH CREEP45
   plants reported as the exposure denominator.

## Mechanism metric for the NEXT stage (not this dose's bar)

Feed-interruption, per research: feeder-absence rounds near their siege
turret / rebuild latency stretched beyond the 1-2-round baseline — NOT enemy
builder deaths (eviction displaces; the EXILE +0.265pp signal measures
vanish-undamaged, a different quantity, and is not cited as mechanism here).

## What this dose does not license

No currency claim; no live window on `_v200siegelaunch` unless the dose bar
is met. If met: corefill screen `SIEGELAUNCH` vs `_v197mapcode`
(non-regression; also catches the scale-surcharge cost of early launchers in
UNSIEGED games — the reason LAUNCHER_MIN_RND exists — though the waiver
should make treatment≈control there), then the pinned live leg vs the ladder
teams with its own prereg.

---

## READOUT (clock = this commit's git author time; runs 17:30:13-17:30:35Z,
## off-branch after; replays scratchpad/feeder45_dose/siege_*, siegeoff_*)

**BAR 1 — VALIDITY: PASS.** CREEP45 in 16/16 games (midgard 1-2/game,
frostgate 2-6/game).

**BAR 2 — DOSE: FALSIFIER FIRED, WITH CLEAN ATTRIBUTION.** EVICT45 = **0 in
all 16 games**. Per the pre-registered decision tree: SIEGE45 > 0 in 15/16
(detection works, up to 102 waivers in one game) and **every logged refusal
is `gate=eco` — 0 `gate=harvester` across all replays — with `reserve=0`
already applied: bank 1-44 Ti against launcher cost 52-61 throughout the
siege window.** ⇒ **The bank is the binding gate (the prereg routes this to
queue #28's territory). Research's Leviathan bank-pin observation is
reproduced on the local fixture: waiving BOTH declared gates does not open
the road because the sieged economy never reaches the launcher price.**

**BAR 3 — OFF-BRANCH: PASS.** Flag-off copy, 2 frostgate games: 0
SIEGE45/GATE45/EVICT45 with CREEP45 plants 2/2 as exposure.

**RESIDUAL, disclosed:** SIEGE45 exceeds GATE45 in several games (e.g. 102 vs
26) — the two latch gates (`SLOT_LAUNCHER` claim / `seen_launcher`) return
False unlogged, so part of the refusal mass is unattributed between them.
Immaterial to the verdict (no launcher was ever affordable pre-160; a latched
slot presupposes a build attempt), but a successor extending GATE45 should
cover those two sites.

**VERDICT (mechanism): the eviction road is shut by the SIEGED ECONOMY, not
by the launcher's gates.** Iteration 3 candidates, in order: (i) **pre-build**
— the launcher exists BEFORE the siege; note `LAUNCH0` already screened
**52.77% ±1.33 at n=5408** (above `LATE160`'s 51.42) and the shipped 160 was
chosen for the scale surcharge, so a screen-backed revisit is cheap and #28
(`LAUNCHER_RESERVE` starves the launcher) points the same way; (ii) a
siege-priority spend freeze (stop heal/eco spending until the launcher is
affordable) — deeper, touches the under-latch. No live window on
`_v200siegelaunch`; the plank as built provably cannot fire.
