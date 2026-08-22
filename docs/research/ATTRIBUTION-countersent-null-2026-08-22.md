# ATTRIBUTION — which conjunct binds the `SK_COUNTER_SENT` (PLANK 3) null

**Written 2026-08-22T19:05:39Z (`date -u`, same shell). Repo HEAD at write time
`0ceb490e21f76d80f024f3ea1459f34b8481aa72`.**

## ⭐ GAME CONTEXT — READ FIRST

**Everything below describes moves inside the Florent Code League, a sandboxed
bot-vs-bot programming competition played on a simulated grid under
organiser-approved rules.** "Core", "damage", "shooter", "counter-battery",
"purchase", "alarm" refer *exclusively* to in-engine mechanics between competing
game bots — an in-game sentinel reducing an in-game core's HP inside the game
engine. Nothing here concerns real systems, networks, infrastructure or people.
Read-only replay analysis: **zero platform matches fired, no file under `bots/`
edited, nothing committed by the author of this document.**

## PROVENANCE — the named inputs

1. `docs/research/PRECHECK-counterbattery-gate-2026-08-22.md` — the prior §3.3 precheck this addendum extends; its LIMITS #4 and #5 are the questions answered here.
2. `docs/research/DESIGN-v629-homeanswer-2026-08-22.md` §3.3 — the commissioning frame.
3. **The gate itself:** `bots/_v628compose/sk_roles.py:1136-1175` (`_counter_sent_action`), `:1279` (`_keeper_counter`, its only caller), `:614-641` (`_counter_target`), `:525-567` (`corefire_fresh` / `_corefire_tick`), `:330-356` (`_claim_role` — the keeper-seat re-claim), `bots/_v628compose/sk_core.py:139-260` (`_corefire_report` / `_corefire_shooter` incl. the latch), `bots/_v628compose/sk_maps.py:986-1008, 1255-1290, 2385-2399, 2562-2563`.
4. `scratchpad/s56_cmp/t_full_f{1,2}/` — **P2**, 60 deterministic local screen games of the v628 line.
5. `scratchpad/s56_cmp/arm_c_full/` — the tree that produced the P2 tape.
6. **`scratchpad/s54_v608/tape_p3only/`** (30 games) and its matched control **`scratchpad/s54_v608/tape_v607ctl/`** (30 games) — **the flag-ON tape**, located during this work; arm flags read from `scratchpad/s54_v608/ablate1.log:19` and `arm_p3only/sk_maps.py:1053,1061,1065,1072`. Also read: `tape_ship/` (the shipped v608 arm, `bots/_v608skalman`), `tape_cnt10/`, `tape_ttl8/`.
7. `tools/skalman_fidelity.py` (`scan_replay`, `_roles`, `_signed`) and `tools/replay_census.py` (`fields`, `parse_entity`, `read_pos`, `scalars`, `WIRE_LEN`, **`DIRECTION_DELTA`**) — parsing helpers imported, not re-implemented.
8. `scratchpad/s56_drip_lib.py` / `scratchpad/s54_klad_lib.py` — read for the ledger approach; the bank is ultimately read from the replay's own `updatePlayers` titanium field and cross-checked against a full reconstructed ledger (V6).

Analysis scripts (not committed, left for review):
`<session-scratchpad>/attribution_countersent.py`, which imports
`<session-scratchpad>/precheck_counterbattery.py`.

---

## ⛔ 0. THE FIRST THING TO KNOW: THE P2 TAPE CANNOT ANSWER "WHY DIDN'T IT FIRE"

**`SK_COUNTER_SENT = False` in the tree that produced the P2 tape.**
`scratchpad/s56_cmp/arm_c_full/` is **byte-identical to `bots/_v628compose`** —
all five modules match, `sk_maps.py` md5 `d9608a9de8a6cc590d5cec990e76519b` on
both — and its line 1255 reads `SK_COUNTER_SENT = False`.

⇒ On the P2 tape **the verb was never live**. No purchase could have happened,
so no absence of purchases is evidence about any conjunct. What the P2 tape CAN
answer is everything the *gate reconstruction* needs — C1 (the keeper's streak),
C2 (the bank) and C3 (the shooter read) are all computable whether or not the
verb runs. Those are reported below as **opportunity**, never as **refusal**.

**AND THE TAPE THAT CAN ANSWER IT IS IN THE REPO.** The flag comment's recorded
null (`sk_maps.py:1255-1266`) was measured on the v608 ablation battery, whose
arms and tapes are still on disk. Named from `ablate1.log` / `ablate2.log`'s own
`effective:` lines rather than guessed:

| tape | flags as logged | what it is |
|---|---|---|
| **`scratchpad/s54_v608/tape_p3only`** | `COREFIRE=True TTL=24 · MEDIC=False · PECK=False · SENT=True RNDS=20 CAP=1 RES=20` | **the PLANK-3-ALONE arm — the flag's own "ALONE it reproduces the v607 outcome … and moves two sentinels"** |
| `scratchpad/s54_v608/tape_v607ctl` | the v607 control | its matched pair, same 15 maps x 2 seats, same seeds |
| `scratchpad/s54_v608/tape_ship` | `MEDIC=False · PECK=True · SENT=False` (`bots/_v608skalman`) | **the SHIPPED tree — the subject of "the shipped streak median is 11"** |
| `scratchpad/s54_v608/tape_cnt10` | `MEDIC=True · PECK=True · SENT=True RNDS=10` | **the gate re-price §3.3 proposes HAS ALREADY BEEN FIRED, at RNDS=10** |
| `scratchpad/s54_v608/tape_ttl8` | `TTL=8 · SENT=False` | the TTL arm |

⚠ **`tape_cnt10` has no matched comparator on disk.** Its flag set is
`MEDIC=True PECK=True SENT=True RNDS=20 CAP=1 DSQ=100 rayonly=False` with only
`RNDS` changed — and no tape in the battery carries that flag set at `RNDS=20`
(the shipped arm has `MEDIC=False, SENT=False`). So the re-price arm as banked
cannot be read against its own control without firing one. Stated as a finding,
not fixed here.

---

## VALIDATION

**V6 the titanium ledger (the bank instrument), with three mutation handles.** The reconstructed OUR-side balance is compared against the replay's own `updatePlayers` titanium field, every round of every game. A residual row is a round where they disagree by any amount.

| ledger variant | residual rows / round-rows (P2, 60 games) | reads |
|---|---|---|
| SHIPPED: global additive scale, rotate=10 Ti, passive +10 at rnd%4==3 | **0 / 16118** | CLOSES |
| MUTATION A: cost scale forced to 1.0 (no scale factor) | **16058 / 16118** | FAILS (as it must) |
| MUTATION B: gunner rotate() not charged | **9938 / 16118** | FAILS (as it must) |
| MUTATION C: passive income removed | **15938 / 16118** | FAILS (as it must) |
| MUTATION D: passive phase shifted to rnd%4==0 | **12107 / 16118** | FAILS (as it must) |

⇒ the scale model that produces `get_sentinel_cost()` below is not asserted, it is **pinned by a ledger that closes to the unit and that three separate corruptions break.**

**V7 keeper identification.** `skalman_fidelity._roles` recognises the HOME KEEPER by a forward-action share of exactly 0.000 with >= 5 actions. Per game, identification either succeeds or it does not — **there is no fallback to max-over-bodies anywhere below.**

* identified in **59/60** P2 games (`roles['home_keeper']` non-null).
* keeper LINEAGE size (bodies meeting the same criterion, ordered by birth): median **1**, range 0-3, total **87** keeper-lineage bodies across the 60 games.
* **DISCRIMINATING CHECK (independent of the recogniser's own criterion):** median d² from OUR core anchor across each body's whole life. The identified keeper is the CLOSEST body to home in **39/59** games; median keeper d² **10** vs median non-keeper d² **252** (ratio **25.2x**). The recogniser keys on ACTIONS; this check keys on POSITION.
  ⚠ **NOT UNANIMOUS: in 20/59 games the recognised keeper is NOT the closest body to home.** `_roles` takes the FIRST body meeting the criterion, not the best, so a short-lived early body can win the label. **Every C1/C2/C3 figure below is therefore reported over the whole keeper LINEAGE** (all bodies meeting the criterion) — a superset of any single pick, so the attribution does not turn on resolving this.
* **MUTATION (every body marked forward-acting):** lineage identified in **0/60** games — the identifier is driven to its other verdict.
* **MUTATION (every body's action count zeroed):** lineage identified in **0/60** games — the identifier is driven to its other verdict.

---

## C1 — THE KEEPER BODY'S COREFIRE STREAK

| statistic | subject | n | median | share reaching 20 |
|---|---|---|---|---|
| max streak of the RECOGNISED keeper body | one body per game | 59 | **46** | **41/59 (69.5%)** |
| max streak per KEEPER-LINEAGE body | every body meeting the criterion | 87 | **54** | 69/87 (79.3%) |
| best keeper-lineage body per game | one figure per game | 59 | **50** | 42/59 (71.2%) |
| max over ALL our builder bodies (the precheck's figure) | one per game | 60 | 52 | 43/60 (71.7%) |

### Does reset-on-retirement reproduce the tree comment's *"streak median is 11"*?

| candidate statistic | n | median | == 11? |
|---|---|---|---|
| max streak of the recognised keeper body, per game | 59 | **46** | no |
| max streak per keeper-lineage body (reset on handover) | 87 | **54** | no |
| best keeper-lineage body per game | 59 | **50** | no |
| running streak value, all keeper body-rounds | 22940 | **0** | no |
| running streak value, keeper body-rounds with the alarm FRESH | 4942 | **26** | no |

**AND THE SAME QUESTION ON THE RIGHT SUBJECT.** The phrase *"the shipped streak
median is 11"* is about the SHIPPED v608 tree, not about v628 — so it is measured
here on `tape_ship` (`bots/_v608skalman`, `MEDIC=False PECK=True SENT=False`) and
on its neighbours, all 30 games each, same fixture:

| v608 tape | recognised-keeper max | per-lineage-body max (resets on handover) | best per game | running value, fresh keeper rounds | C1 open (streak reaches 20) |
|---|---|---|---|---|---|
| **`tape_ship` — the subject of the "11"** | **54** | **54** | **54** | 28 | **23/30** |
| `tape_p3only` (flag ON, RNDS=20) | 54 | 54 | 54 | 43 | 22/30 |
| `tape_v607ctl` (the matched control) | 54 | 54 | 54 | 43 | 22/30 |
| `tape_cnt10` (RNDS=10) | 54 | 54 | 54 | 28 | 23/30 |

**Nothing reads 11 on any tape under any of the five statistics.** And the
reset-on-retirement mechanism specifically is ruled out: the per-lineage-body
column — which *does* restart at 0 at every keeper handover — is identical to the
per-game column. **The hypothesis in the prior precheck's LIMITS #5 is refuted,
not confirmed.**

---

## C2 — THE BANK CONJUNCT

* **ROUND-INSTANCES:** across the 60 P2 games there are **1864** keeper-body round-instances in which C1 is satisfied (that body's `corefire_streak` >= 20). In **484** of them (26.0%) the bank entering the round was also >= `sentinel_cost + 20`. ⇒ **C2 is satisfied in 26.0% of C1-open round-instances.**
* **GAMES:** C1 opens for a keeper-lineage body in **42/60** games; C1 AND C2 are jointly satisfied on at least one round in **19/60** games (**31.7%**).
* **BANK-THRESHOLD CONTROL (shipped reserve = 20):** sufficient in **484/1864** C1-open round-instances.
* **BANK-THRESHOLD CONTROL (MUTATION: reserve = 100000):** sufficient in **0/1864** C1-open round-instances.

| game | cell | first round C1 opens | C1-open rounds | of those, C2 also OK | first round C1+C2 both hold |
|---|---|---|---|---|---|
| f1:auroraveil_seatB | t_full_f1 | 143 | 39 | 1 | 217 |
| f1:bifrost_seatA | t_full_f1 | 123 | 35 | 35 | 123 |
| f1:glacierkeep_seatB | t_full_f1 | 103 | 63 | 0 | — never |
| f1:helheim_seatA | t_full_f1 | 353 | 19 | 19 | 353 |
| f1:helheim_seatB | t_full_f1 | 85 | 59 | 14 | 104 |
| f1:holmgang_seatA | t_full_f1 | 85 | 92 | 10 | 169 |
| f1:icefloe_seatA | t_full_f1 | 58 | 39 | 0 | — never |
| f1:icefloe_seatB | t_full_f1 | 79 | 83 | 0 | — never |
| f1:jotunheim_seatA | t_full_f1 | 126 | 43 | 0 | — never |
| f1:jotunheim_seatB | t_full_f1 | 61 | 108 | 16 | 61 |
| f1:longhouse_seatA | t_full_f1 | 60 | 42 | 38 | 60 |
| f1:longhouse_seatB | t_full_f1 | 81 | 58 | 0 | — never |
| f1:midgard_seatA | t_full_f1 | 61 | 35 | 0 | — never |
| f1:midgard_seatB | t_full_f1 | 61 | 46 | 34 | 61 |
| f1:paths_seatA | t_full_f1 | 165 | 40 | 40 | 165 |
| f1:paths_seatB | t_full_f1 | 81 | 53 | 0 | — never |
| f1:skald_seatA | t_full_f1 | 83 | 53 | 20 | 83 |
| f1:stavkirke_seatA | t_full_f1 | 78 | 26 | 0 | — never |
| f1:valkyrie_seatA | t_full_f1 | 73 | 35 | 0 | — never |
| f1:valkyrie_seatB | t_full_f1 | 81 | 59 | 8 | 132 |
| f1:yggdrasil_seatA | t_full_f1 | 72 | 44 | 0 | — never |
| f2:auroraveil_seatA | t_full_f2 | 171 | 78 | 24 | 220 |
| f2:bifrost_seatA | t_full_f2 | 135 | 35 | 0 | — never |
| f2:bifrost_seatB | t_full_f2 | 105 | 20 | 0 | — never |
| f2:glacierkeep_seatA | t_full_f2 | 618 | 17 | 0 | — never |
| f2:glacierkeep_seatB | t_full_f2 | 225 | 8 | 0 | — never |
| f2:helheim_seatA | t_full_f2 | 65 | 42 | 0 | — never |
| f2:helheim_seatB | t_full_f2 | 106 | 17 | 0 | — never |
| f2:holmgang_seatA | t_full_f2 | 503 | 35 | 35 | 503 |
| f2:icefloe_seatA | t_full_f2 | 176 | 11 | 0 | — never |
| f2:icefloe_seatB | t_full_f2 | 383 | 40 | 0 | — never |
| f2:longhouse_seatB | t_full_f2 | 443 | 15 | 15 | 443 |
| f2:midgard_seatA | t_full_f2 | 63 | 26 | 0 | — never |
| f2:midgard_seatB | t_full_f2 | 35 | 27 | 27 | 35 |
| f2:paths_seatA | t_full_f2 | 77 | 84 | 84 | 77 |
| f2:paths_seatB | t_full_f2 | 138 | 39 | 39 | 138 |
| f2:skald_seatA | t_full_f2 | 28 | 44 | 10 | 28 |
| f2:skald_seatB | t_full_f2 | 29 | 55 | 0 | — never |
| f2:stavkirke_seatA | t_full_f2 | 28 | 53 | 15 | 28 |
| f2:stavkirke_seatB | t_full_f2 | 42 | 81 | 0 | — never |
| f2:valkyrie_seatA | t_full_f2 | 115 | 35 | 0 | — never |
| f2:valkyrie_seatB | t_full_f2 | 110 | 31 | 0 | — never |

---

## C3 — THE SHOOTER-READ CONJUNCT

**V8 direction-decode control (the C3 instrument).** The wire carries a turret's facing as an integer; C3's rank-0/1 test walks that facing as a ray. If the decode were wrong the ray would point somewhere arbitrary. Discriminating test: over the rounds in which OUR CORE actually lost HP, how often does SOME enemy turret's facing ray reach our core footprint?

| direction decode | ANY enemy turret on the map (pure geometry) | only turrets inside the core's own r²=36 |
|---|---|---|
| CORRECT (`replay_census.DIRECTION_DELTA`, 1-indexed) | **1189/1189 (100.0%)** | **1095/1189 (92.1%)** |
| MUTATION: rotated +1 | **43/1189 (3.6%)** | **43/1189 (3.6%)** |
| MUTATION: rotated +2 | **0/1189 (0.0%)** | **0/1189 (0.0%)** |
| MUTATION: rotated +4 | **0/1189 (0.0%)** | **0/1189 (0.0%)** |

⇒ **the corrected decode reads 100.0% and the three rotations read 3.6% / 0% / 0%.** Under the correct table EVERY round in which our core lost HP has an enemy turret whose facing ray lands on our core footprint — i.e. on this tape core damage is turret ray fire and nothing else. (Independently: an enemy `builderAttack` targeted our core footprint on only **8/1189** of those rounds.)

⚠ **THIS CONTROL CAUGHT A REAL DEFECT IN THIS SCRIPT.** The first cut hand-rolled a zero-indexed direction table from `fcode.Direction`'s iteration order and read **43/1189 (3.6%)** — a number low enough to look like a fact about the fixture rather than a bug. The wire is ONE-indexed with 0 = CENTRE/unset; `replay_census.DIRECTION_DELTA` already had it right and is now reused instead of re-derived. The 3.6% row above is that defective decode, kept as the +1 rotation.

The two columns differ by **1189 - 1095 = 94 rounds (7.9%)**: in those, the turret whose ray reaches our core sits OUTSIDE the core's own r²=36 vision — the hazard `sk_core.py:142-148` names, present but smaller than that note implies on this tape.

**THE CONJUNCT LADDER, over keeper-lineage round-instances (P2, 60 games).** Each row adds one conjunct of `_counter_sent_action`; the drop between rows is what that conjunct costs.

| conjunct set | round-instances | share of C1-open | games with >= 1 qualifying round |
|---|---|---|---|
| C1 (keeper streak >= 20) | **1864** | 100.0% | **42/60** |
| C1 + C2 (bank >= sentinel_cost + 20) | **484** | 26.0% | **19/60** |
| C1 + C3 (a shooter tile is published & in fence) | **1190** | 63.8% | — |
| C1 + C2 + C3 (all three) | **351** | 18.8% | **16/60** |

⚠ **C3 here is the CORE-PUBLISHED half only** — `_counter_target` also falls back to the body's own `_core_ray_shooter()` memo, which is not reconstructable from the wire. **So the C3 rows are LOWER bounds: the true C1+C2+C3 share is at least this and possibly higher.** That direction is safe for saying C3 does not bind and unsafe for saying it does.

---

## THE FLAG-ON TAPE — `scratchpad/s54_v608/tape_p3only` (`SK_COUNTER_SENT = True`, RNDS=20, CAP=1, RES=20; PLANK 1 and PLANK 2 OFF)

30 games, same fixture family as P2's F1 cell (`opp_v542wave_noiseoff`, 15 maps x 2 seats, NOISE_OFF). **This is the tape on which the flag's recorded null was measured, and unlike the P2 tape the verb is LIVE on it.**

**Counter-sentinel PURCHASES, by two independent instruments:**

* **STRUCTURAL** (our sentinel built on a tile orthogonally adjacent to a keeper-lineage body — the site domain `_counter_sent_action` searches, `sk_roles.py:1157 for d in CARDINALS: q = p.add(d)`): **3 purchases across 30 games** — holmgang_seatB r651, midgard_seatB r62, valkyrie_seatB r83.
* **PAIRED DELTA** vs the matched v607 control tape (`tape_v607ctl`, same maps/seats/seeds): our sentinel count **+2 across 30 games**.
* The flag's own comment records *"moves two sentinels"*. The two instruments measure DIFFERENT things and are consistent: **3 purchases** (structural, gross) against a **+2 NET sentinel count** (paired, so a purchase that displaces an engineer sentinel elsewhere nets to zero). The recorded figure is the net one. Either way the null is concrete: **3 purchases in 30 games, 3 games touched.**

**THE CONJUNCT LADDER ON THE LIVE TAPE (30 games):**

| conjunct set | keeper round-instances | share of C1-open | games with >= 1 qualifying round |
|---|---|---|---|
| C1 keeper streak >= 20 | **1654** | 100.0% | **22/30** |
| C1 + C2 bank >= sentinel_cost + 20 | **853** | 51.6% | **12/30** |
| C1 + C3 shooter tile published & in fence | **1399** | 84.6% | — |
| C1 + C2 + C3 | **794** | 48.0% | **11/30** |
| **ACTUAL PURCHASES** | **3** | 0.18% | **3/30** |

⇒ **11 of 30 games offered at least one round on which C1, C2 and C3 were ALL satisfied, and 3 purchases were made.** The three conjuncts the flag comment and the design doc name do not account for the gap; a FOURTH conjunct does — the SITE loop that runs after them (`sk_roles.py:1157-1175`: a cardinal neighbour of the keeper that is `may_build`, NOT on the enemy axis, NOT on an armed axis, leaves `free_neighbours >= 2`, and passes `path_arbiter_ok`), plus the `SK_COUNTER_SENT_CAP = 1` ceiling once one is bought.

---

## LIMITS

1. **The P2 tape's `SK_COUNTER_SENT` is OFF (§0).** Every P2 number in this document is an *opportunity* count — how often the gate's conjuncts were satisfiable — never a count of refusals. Only the `tape_p3only` section measures a live verb.
2. **C3 is reconstructed from the CORE-PUBLISHED half only.** `_counter_target` (`sk_roles.py:620-622`) falls back to the body's own `_core_ray_shooter()` memo, which depends on that body's private `armed_memo`/`armed_facing` vision history and is not on the wire. **The C3 rows are LOWER bounds** — safe for concluding C3 does *not* bind, unsafe for concluding it does. Since C3 already reads 84.6% on the live tape, that asymmetry does not threaten the conclusion drawn.
3. **A FOURTH CONJUNCT IS NOT MODELLED AT ALL.** After C1/C2/C3, `_counter_sent_action` runs a site loop (`sk_roles.py:1157-1175`): a cardinal neighbour `q` of the keeper that passes `may_build(q, OWNER_DOOR)`, is not `_on_enemy_axis(q)` nor `_on_armed_axis(q)`, leaves `free_neighbours(exclude=q) >= 2`, and passes `path_arbiter_ok`; then a facing search over all 8 directions. Plus `SK_COUNTER_SENT_CAP = 1` ends the game's purchases after one. **None of that is reconstructed here**, and the residual gap between C1∧C2∧C3 and actual purchases is exactly where it lives. This document narrows the null to that residual; it does not open it.
4. **Keeper identification is not unanimous.** `_roles` takes the FIRST body with a forward-action share of 0.000 and >= 5 actions, not the best; on the independent position check it is the closest-to-home body in only 39/59 P2 games. **All C1/C2/C3 figures are therefore computed over the whole keeper LINEAGE** (every body meeting the criterion) — a superset of any single pick — so the attribution does not turn on resolving it. The lineage is the right object anyway: `_claim_role` (`sk_roles.py:330-356`) has a replacement take the lowest STALE role, and `SK_HOME_KEEPER = 0` is the lowest, so a dead keeper's seat is re-claimed by the next body.
5. **The bank is read entering the round.** The keeper acts *during* round r, so the balance it reads lies between end-of-(r−1) and end-of-r. The entering balance is used; a unit acting earlier in round r could have spent some of it. This biases C2 satisfaction *upward*, i.e. against attributing the null to C2.
6. **Deterministic local fixtures throughout.** Both `s56_cmp` and `s54_v608` tapes are NOISE_OFF, one seed per (map, seat), against authored local opponents. MATCH cluster dead, OPPONENT and MAP clusters live, CONTENT-DUPLICATE unverified. **No interval is quoted anywhere in this document** and none should be read in — these are counts, not estimates.
7. **Round indices are 0-based** and taken directly from the replay turn index.
8. **`tape_p3only` runs PLANK 1 and PLANK 2 OFF.** Its C2 figures are therefore *more* favourable than the shipped tree's (no peck-Ti, no heal-Ti competing for the same pool) — visible as C2 = 51.6% there against 26.0% on P2, where `SK_COUNTER_PECK` is on. The conjunct that binds may be spend-order dependent, and this document does not separate that.

---

## WHAT THE EVIDENCE ATTRIBUTES THE NULL TO

Stated plainly, per the commission, with no build/no-build call — that is the
builder's:

* **C1 (the keeper's `corefire_streak >= 20`) DOES NOT BIND.** On the live `tape_p3only` it is open in **22/30 games** and on the shipped `tape_ship` in **23/30**; on P2 in **42/60**. Median keeper max-streak is **54** on every one of the four v608 tapes measured. The flag comment's *"THE GATE IS ALMOST NEVER OPEN IN TIME"* is not what the tapes show.
* **The "shipped streak median is 11" hypothesis is REFUTED on its own subject tape.** Measured on `tape_ship` — the exact arm the phrase describes — the recognised-keeper median max streak is **54**, the per-lineage-body median is **54**, the best-per-game median is **54**, and the running-streak median over fresh keeper body-rounds is **28**. **No candidate statistic reads 11**, and reset-on-retirement does not produce it: the per-lineage-body figure (which *does* reset at each handover) is identical to the per-game figure.
* **C2 (the bank) BINDS, but not enough to account for the null.** It removes **48.4%** of C1-open round-instances on the live tape (853/1654 survive) and **74.0%** on P2 (484/1864 survive). It is the largest single reducer among the three, and it is nowhere near sufficient.
* **C3 (the shooter read) BARELY BINDS** — **84.6%** of C1-open instances on the live tape already carry a published, in-fence shooter tile, and that figure is a lower bound (LIMITS #2).
* **⇒ THE NULL IS NOT ATTRIBUTABLE TO C1, C2 OR C3, SEPARATELY OR TOGETHER.** On the live tape all three held simultaneously on **794 of 1654 keeper round-instances (48.0%), spread over 11 of 30 games** — and **3 purchases** were made. **The unexplained residual is ~99.6% of the qualifying round-instances and 8 of the 11 qualifying games.**
* **The remaining candidates, both unmodelled here (LIMITS #3):** the **SITE loop** after the three gates (`sk_roles.py:1157-1175` — `may_build`, off-enemy-axis, off-armed-axis, `free_neighbours >= 2`, `path_arbiter_ok`, then a facing that scores), and **`SK_COUNTER_SENT_CAP = 1`** truncating each game after one purchase. The cap cannot explain games with zero purchases, which leaves the site loop as the only named candidate standing.
* **One consequence worth stating because §3.3 proposes it:** the gate re-price §3.3 asks for was **already fired at `RNDS = 10`** (`scratchpad/s54_v608/tape_cnt10`) and **has no matched `RNDS = 20` comparator on disk**. And since C1 is open in 22-23 of 30 games at `RNDS = 20` on these tapes, a re-price from 20 to a smaller N is moving a constraint that the reconstruction does not find binding.
