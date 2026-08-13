# DOSE PREREG — #47 (iteration 4): approach-triggered launcher

**Committed before any dose game (two-clock: this commit's git author time vs
run wall clocks in the readout).** Builder s37, 2026-08-13. Built from queue
row #47 as stocked by research (same day); mechanism carry-over per the row:
eviction-when-launcher-exists needs no re-proof (205 r<160 evictions,
`DOSE-launch0evict45`). This dose tests only the CONDITIONAL claim.

## The plank

`bots/_v207apprlaunch` = incumbent `_v197mapcode` + `LOKI_APPR_LAUNCHER`:
an enemy builder bot within `LOKI_APPR_DSQ=50` of our core (seen by the unit
deciding the launcher build) waives `LAUNCHER_MIN_RND` and zeroes
`LAUNCHER_RESERVE` for that decision. Cap stays 1 (the existing latch).
Outside the triggered state the behaviour is the incumbent's. Per-round
`GATE45` arithmetic log carried from iteration 2 on research's request, so
trigger-timing attribution (approach round vs bank vs build round) is
readable. Tags: `APPR45` (trigger, with bank), `GATE45`, `EVICT45`.

## Bars (fixture `_probe_creeper`, frozen; 8 games × {midgard, frostgate},
## seeds 994001-8, kept replays)

1. **VALIDITY — PRE-treatment denominator (iter-3's collider fix):** enemy
   builders APPROACH (APPR45 ≥1) in ≥6 of 8 games per map. Plants are NOT
   the denominator — the treatment suppresses them.
2. **DOSE BAR (a) — the conditional's triggered half:** among games with
   APPR45, a launcher is BUILT at r<160 in ≥half (readable as EVICT45 r<160
   or the launcher's build via GATE45 cessation; the definitive read is the
   replay's entity events if tags are ambiguous). **FALSIFIER: 0 r<160
   launcher builds across all approached games ⇒ approach detection triggers
   too late to beat the bank drain — the row's named fallback (spend-freeze
   fork) becomes the design, and the GATE45 log shows the bank level at
   trigger to prove it.**
3. **DOSE BAR (b) — the conditional's quiet half is screened, not dosed:**
   the creeper fixture approaches in every game, so (b) — launcher count 0
   in unsieged games — cannot be read here. It is the corefill screen's job
   (`APPRLAUNCH` vs `_v197mapcode`, self-play: the incumbent's raiders DO
   enter our half, so self-play prices the trigger's false-positive premium
   — the −6.34pp hazard — exactly where it lives). Named here so nobody
   reads the dose as having covered it.
4. **TAG-ATTRIBUTION CONTROL (2 games, frostgate):** scratch copy with
   `LOKI_APPR_LAUNCHER=False`, tags present: 0 APPR45/GATE45, 0 r<160
   EVICT45; r≥160 legacy throws disclosed.

## Sequence if bars pass

Corefill screen `APPRLAUNCH` (the unsieged premium is the named hazard; an
inside-band screen + a met dose is the plank's case) → pinned live leg vs
CAL-3 C1/C4 (LingLing40, team lazy) with its own prereg and research's
fire-order coordination. Feed-interruption is the live mechanism metric.

---

## READOUT (clock = this commit's git author time; runs 17:39:32-17:39:55Z,
## bar-4 control after; replays scratchpad/feeder45_dose/appr_*, approff_*)

**BAR 1 — VALIDITY (pre-treatment denominator): PASS.** APPR45 ≥1 in 16/16
games (midgard 2-21/game, frostgate 25-126/game).

**BAR 2 (a) — LAUNCHER BUILT r<160 IN APPROACHED GAMES: MET POOLED, 10/16.**
* Frostgate: 6/8 by r<160 evictions alone (41-152 evictions/game).
* Midgard: tags ambiguous (evictions only in 994007), so the prereg's
  definitive read was taken — replay entity events via `replay_autopsy`:
  **launchers built at r48, r52, r52, r55 (+ a second at r81) in 4 of 8
  games — exactly ≥half — all inside the healthy-bank window** (GATE45
  eco-refusals occur but cease; APPR45 bank readings at trigger are healthy).
* **The siting stratum reconfirms with sharper data: on midgard, 4 games
  build the launcher and only 1 converts to evictions** (994007: 24
  evictions and the ladder NEVER FORMED, CREEP45=0 — the second such game
  across iterations). The launcher gets BUILT at home; on 900-area maps the
  feeder ring is outside pickup reach d²≤2 unless siting follows the creep.
  #47's frostgate/midgard strata carry this number: **build 4/8, convert
  1/4.**

**BAR 3 (b):** not read here, by prereg — routed to the corefill screen
(`APPRLAUNCH` queued, seed base 228000).

**BAR 4 — TAG-ATTRIBUTION CONTROL: PASS, strongly.** Flag-off copy, 2
frostgate games to r1000: 0 APPR45, 0 GATE45 at ANY round, 0 EVICT45, plants
3/6. The side lane's legacy-GATE45 flag does not bite this arm: both GATE45
sites are conditioned on `approached`, which is unreachable flag-off (guard
written at build time in response to the iter-2 flag class).

**VERDICT: the conditional design's triggered half WORKS — approach
detection fires early enough to buy the launcher at a healthy bank (builds
r48-55 vs iteration 2's bank-dead siege window), and on small maps it
converts to heavy feeder eviction (41-152/game) with two games where the
ladder never formed at all.** The quiet half (unsieged premium, the −6.34pp
hazard) is the screen's question and the screen is queued. Next after the
screen: launcher SITING on big maps (build 4/8, convert 1/4 is the number to
beat), then the pinned live leg vs CAL-3 C1/C4 with its own prereg.

**D26 REPLICATION RULE for the APPRLAUNCH screen, declared at queueing:**
replicated iff final |share − 50| ≥ 2.0pp; second shard seed base 229000,
scored alone, pools only if both finals sit the same side of 50.

---

## AMENDMENT (ADD-only; clock = this commit's git author time) — LIVE LEG
## REORDERED AHEAD OF THE SCREEN FINAL (Magnus's prompt: "did we try
## APPRLAUNCH as an rc?")

The registered sequence (screen → live leg) implied a dependency that does
not exist: the screen prices the UNSIEGED PREMIUM (harm side — self-play
cannot present the creeper shape), the live leg prices the VALUE side vs the
real ladder teams. Independent surfaces; order not load-bearing. The screen
CONTINUES to its final unchanged (currently 53.54 at n=2854, past GATE-2700).

**rc8.4 leg, declared before firing:** `bots/_v207apprlaunch` as
"Loki rc8.4" via submit_clean --leg; 5 pinned matches:
* C1-shape team lazy (648d1d5b…) --match ddf48911… (the tri-arm pin)
* C4-shape LingLing40 (86d0b484…) --match 446bb6a3… (pin holds them at v40,
  the profiled build the plank was designed against)
* + the same three remaining tri-arm cells (Leviathan/Juusto/Coreflood pins)
  so all 25 games stay matched-pair comparable with arms A-D.
Maps: the tri-arm five. Window: first clean post-pairing slot with CAL-3
yielded. TARGET BAND: unrated pays 0; cells kept for pairing integrity
(same disclosure as rc8.3).
**Bars (wire, by construction):** (a) launcher built at r<160 in ≥half of
games with enemy-builder approach — v125 CANNOT build pre-160, so every
early launcher is treatment-caused; (b) EVICT45-equivalent throws read from
throw events (platform strips stdout — the WIRE events are the instrument,
not tags); (c) feed-interruption vs arm A's same cells (rebuild latency of
their siege turrets stretched off the 1-2 baseline). Counts only at n=25.
