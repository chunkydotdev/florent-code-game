# `_v87ad` det flip corpus — margin decode

**Research-arm decode, 2026-08-08.** Answers: *why does the fix candidate lose
r1000 tiebreak margins that its parent wins?* Measurement and attribution only —
no games run, no bot files touched, no downloads.

> ## VERDICT
>
> **One toggle half owns all five flips: Fix A (HS3 conscription). Fix D (spur
> repair) is not the owner anywhere — it is inert or below the noise floor in
> every primary.** All five divergences are the conscription broadcast firing,
> at exactly `HS3_BLEED_ROUNDS + 1` rounds after the Core first reads a
> below-max HP (exact on 3/5, +2 and +9 on the other two).
>
> - **lighthouse a — H1 (conscription opportunity cost), dominant.** The two
>   builders that in the base perform the counterbattery are recalled at r100
>   and dead by r149; the enemy's two core-side turrets survive to r1000;
>   incoming goes **2.42 → 14.00 HP/round** and five of nine builders sit on
>   seats *healing* it forever (seat-heal share of builder-rounds **6.8% →
>   41.9%**). Expansion stops dead: **zero builds r300-r899**.
> - **meander a — H1 dominant, H3 a close second.** The conscription claims
>   builder `#10`'s move at r20 and the harvester-(7,6) link is never finished;
>   3 of 5 builders end up permanently seated (**0.8% → 44.7%**); the bank sits
>   at **0 Ti for 800 rounds**, so no ammo, no turrets, no contest — and a
>   displaced enemy builder then cuts the one surviving artery at (13,5) (r84-93,
>   never repaired), taking our delivery to **0 stacks/100 r for 800 rounds**.
> - **snowflake b — H1 dominant, by tempo rather than by lock.** ~3.4 builders
>   pinned on seats through **r100-r399** — the exponential-growth window —
>   during which our harvester count is frozen at **3.00** while the base climbs
>   **3.5 → 15.7**. The lock *does* release at r400; by then the game is gone.
> - **hive b (secondary).** The r602 core kill does not vanish because the
>   killers were recalled — it vanishes because the conscription cost a
>   **delivery terminus** at r39, our delivery rate halved (**48.5 → 24.7
>   stacks/100 r**), and the second and third siege gunners that did the killing
>   were never affordable.
> - **archipelago a (control).** Confirms the known counterbattery story, and
>   supplies the discriminator: it is the **only** leg where incoming *falls*
>   (**8.53 → 3.45 HP/round**) and the only leg where the conscription share
>   *falls* (**32.7% → 13.3%**).
>
> **The one-line rule the corpus supports:** conscription pays for itself only
> when the recalled body **removes** incoming. When it merely **matches**
> incoming — heal ÷ incoming ≈ 1.00 in all four losing legs — it buys a stable
> siege that runs to r1000 while the reserve stops mining, stops linking and
> stops raiding. Same channel in all three primaries; the *proximate* damage
> differs by map (lost counterbattery / lost link / lost growth window), the
> channel does not.

| | |
|---|---|
| Candidate | `bots/_v87ad/main.py` md5 `90e678bacc91e1dbbc4e6cf3a11df72d` — **KEEP-dev, gate NOT passed**, tape row `_v87ad-acceptance` |
| Base / parent | `bots/_v85hsd/main.py` md5 `4a2aeb50ef8ff63ea55ddc25baca2628` = **live ladder v75 "Eir 8"** |
| Opponent | `det_v74` (deterministic copy of `bots/opp_v74/main.py` md5 `cb5452e66c69a21d8aa1af340cdc37dd`) |
| Corpus | `replay_archive/diag_ad_flips_2026-08-08/` — **LOCAL det, NOISE_OFF, `--tle 0`, paired base-vs-candidate on identical map/seed/seat. NOT wild-ladder data.** |
| Toggles under test | Fix A `HS3_ON` (bit-20 bleed broadcast on `SLOT_HEAL_BUDGET`, `HS3_BLEED_ROUNDS=12`, `HS3_MAX_CONSCRIPTS=2`, roles {2,3}); Fix D `SPUR_ON` (`SPUR_MAX_REBUILDS=3`, `SPUR_MAX_QUEUE=4`, `SPUR_GIVEUP_RNDS=12`) |
| Tooling | `scratchpad/ad_flips/{decode,ledger,compare,flow,trace,summary}.py`, adapted from the archb decode; `tools/replay_schema.md` is ground truth. `decode.py` extended to parse `ResourceMove.resourceId` (field 3) so every stack is followed from its harvester to the core that banks it. |
| Channel discipline | every number is from `.replay26` wire events. The `fcode` JSON sidecars were read once, for headline outcomes and as the delivery self-check. `.err` files read for the displacement meter only. |
| Method rule | all homeostatic claims in **ratio form** — heal ÷ incoming, per-100-round rates, shares of builder-rounds. Absolute totals appear only inside a single fixed-length pair. |

---

## 1. Divergence table — every flip is Fix A

Both legs of each pair are byte-identical in event content up to the round
below. The Core acts first in the round (its `coreConvertAmmo` is the first
update emitted), so it reads the **previous round's end-of-round HP**; the flag
therefore arms on the 12th consecutive such reading and is visible one round
later (buffered store).

| game | seat | first below-max read by Core | armed | visible | **first divergent round** | lag | what the candidate did differently |
|---|---|---|---|---|---|---|---|
| lighthouse a | A | r88 | r99 | r100 | **r100** | 0 | `#9` abandons its attack on (7,12) and steps north toward the core; `#7` reverses direction. Both dead by r127 / r149. |
| meander a | A | r6 | r17 | r18 | **r20** | +2 | `#10` declines to build its planned link tile (10,6) and steps onto it instead. The harvester-(7,6) spur is never finished. |
| snowflake b | B | r36 | r47 | r48 | **r57** | +9 | `#10` turns south toward the core instead of continuing west. |
| hive b | B | r27 | r38 | r39 | **r39** | 0 | `#10` walks north off its link line. The (20,3) delivery terminus is never built. |
| archipelago a *(control)* | A | r39 | r50 | r51 | **r51** | 0 | `#7` and `#9` redirected toward core seats. |

The +2 / +9 lags are the `_hs3_busy_building` gate: a conscript standing beside
its next planned tile with the bank to pay for it finishes that tile first.

**Fix D is excluded at every divergence point**, by construction rather than by
assertion:

- hive and archipelago: **zero** own buildings of ours had been destroyed
  anywhere on the map before the divergence round, so `spur_built` had no gaps
  to re-queue.
- meander: builder `#10`'s only remembered tiles at r20 are (8,6) and (9,6);
  (8,6) dies at r56 and (9,6) at r996. Both alive at r20 → no gap → no queue.
- lighthouse and snowflake: whole-game counts of *"we built on a tile where our
  own building had previously died"* are **3 (cand) vs 61 (base)** and **11 vs
  27** — the candidate does strictly **fewer** such rebuilds than the base. Fix D
  cannot own a loss by building less than the thing it is compared against.

Direct Ti cost of Fix D across the three primaries, upper-bounded by that same
over-inclusive proxy: **≤ 19 conveyor rebuilds ≈ ≤ 60 Ti**, against per-game
delivered titanium of 12,170 / 290 / 10,020. **H2 ≤ 0.5% of income in every
primary.**

---

## 2. The ratio table

Whole-game, per-round / per-100-round forms. `seat-heal%`, `raid%`, `build%`,
`idle%` are shares of *classified builder-rounds* (a builder's round is labelled
by what it did: healed a core-footprint tile from an adjacent tile = seated
heal; attacked something on the enemy's half = raid; built = build; no action
and no move = idle).

| game | ver | R | dlv us /100r | dlv them /100r | harv-rounds/r us | harv-rounds/r them | seat-heal% | raid% | build% | idle% | **incoming HP/r** | **heal HP/r** | **heal ÷ incoming** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| lighthouse a | hsd | 1000 | 124.7 | 118.5 | 7.64 | 3.00 | 6.8 | 10.9 | 1.7 | 11.9 | **2.42** | 2.47 | 1.02 |
| lighthouse a | **ad** | 1000 | 121.7 | **138.2** | **4.91** | **6.01** | **41.9** | 11.0 | **0.5** | 11.5 | **14.00** | 14.06 | **1.00** |
| meander a | hsd | 1000 | 25.4 | 0.0 | 2.03 | 1.02 | 0.8 | 0.8 | 0.5 | 20.7 | **0.16** | 0.16 | 1.01 |
| meander a | **ad** | 1000 | **2.9** | **24.3** | 2.00 | 1.05 | **44.7** | 0.4 | 0.7 | 2.7 | **8.08** | 8.93 | 1.11 |
| snowflake b | hsd | 1000 | 192.8 | 190.6 | 15.43 | 8.71 | 8.7 | 17.2 | 3.6 | 14.0 | 2.52 | 2.75 | 1.09 |
| snowflake b | **ad** | 1000 | **100.2** | **318.0** | **5.84** | **15.96** | **15.6** | **2.2** | 2.7 | 19.4 | 3.98 | 4.29 | 1.08 |
| hive b | hsd | 602 | 48.5 | 17.6 | 2.94 | 1.70 | 18.5 | 7.9 | 1.0 | 25.3 | 3.53 | 3.69 | 1.05 |
| hive b | **ad** | 1000 | **24.7** | 24.8 | 2.97 | 1.98 | **31.6** | **0.7** | 0.5 | **43.8** | 6.17 | 6.31 | 1.02 |
| archipelago a | hsd | 190 | 46.8 | 67.4 | 2.97 | 2.79 | 32.7 | 8.5 | 3.1 | 10.9 | **8.53** | 5.83 | **0.68** |
| archipelago a | **ad** | 1000 | **120.0** | 84.1 | **11.66** | **8.51** | **13.3** | 1.9 | 2.5 | 2.5 | **3.45** | 3.72 | 1.08 |

Two readings carry the whole document:

1. **`heal ÷ incoming` is ~1.00 in every candidate leg, winning and losing
   alike.** The homeostat always closes. It is therefore *not* a discriminator,
   and any prediction stated on heal throughput is uninformative (the A.3-item-1
   correction from the archb addendum, re-confirmed on five more games).
2. **The discriminator is the level at which it closes.** In the one leg the
   candidate wins, incoming *falls* (8.53 → 3.45). In all four it loses,
   incoming *rises or stays* and the conscription share *rises*. Removing the
   shooter is the win condition; paying the shooter is the loss condition, and
   the price of paying is the reserve's entire output.

**Casualty note (contradicts a carried archb finding).** On archb the conscripted
reserve raided and took casualties. Here it does not: lighthouse builder deaths
after r100 are **23 (base) vs 10 (candidate)**. The candidate loses *fewer*
builders because it never sends them anywhere — except for the two that die
walking home through the fire lane at r127/r149.

---

## 3. Per-game ledger diffs, with closing arithmetic

Every stack is followed from the harvester that emitted it to the core that
banked it, so the margin identity is exact rather than fitted:

```
delivered_X  =  mined_X  −  lost_in_transit_X  −  leaked_X→Y  +  leaked_Y→X
margin  M    =  delivered_us − delivered_them
```

All figures in **stacks** (× 10 = titanium). Residual = 0 by integer identity in
all three primaries.

### 3.1 lighthouse a — the counterbattery that never happens

| | base (hsd) | cand (ad) | Δ |
|---|---|---|---|
| we mined | 1,734 | 1,228 | **−506** |
| we delivered to our core | 1,247 | 1,217 | −30 |
| **we leaked to the enemy core** | **460** | **0** | **−460** |
| our stacks lost in transit | 27 | 11 | −16 |
| they mined | 733 | 1,399 | **+666** |
| they delivered | 1,185 | 1,382 | +197 |
| their stacks lost | 8 | 17 | +9 |
| **margin M** | **+62** | **−165** | **−227** |

**Closing arithmetic** (`ΔM = Δmine_us − 2·Δleak_us − Δlost_us − Δmine_them + Δlost_them`):

| component | stacks on the margin | share |
|---|---|---|
| enemy mining no longer suppressed | **−666** | 293% |
| our mining collapse (harvester expansion halted) | **−506** | 223% |
| our belt stops feeding the enemy core (base pathology the candidate accidentally cures) | **+920** | −405% |
| in-transit losses, both sides | **+25** | −11% |
| **sum** | **−227** | **100.0%** |
| **observed ΔM** | **−227** | **residual 0.0%** |

**Mechanism, in events.** The enemy's two core-side turrets sit at **(3,7)** and
**(4,9)** — a gunner (7 dmg, 1/round) and a sentinel (18 dmg, 1/2 rounds), 700 +
900 = **1,600 HP per 100 rounds** on our core at (3,3)-(4,4).

- **Base:** our builders spend **72 attacks on our own side in r200-r299** and
  kill both. Core damage after r300: **0 per 100 rounds, for 700 rounds.** The
  freed reserve then grinds the enemy: 4 enemy harvesters killed (r211, r384,
  r401, r416), three of those ore tiles retaken by us (r274, r417, r418). Enemy
  harvester-rounds fall to **2.00/round** and their mining to **50 stacks/100 r**.
  Our own harvesters climb to **9-10** — though four are orphaned, which is
  where the 460-stack leak into the enemy core comes from.
- **Candidate:** on-side attacks are **4, then 2, then 0**. The two builders that
  did the base's counterbattery are recalled at r100 and dead by r149. From
  **r300 to r999 the game is an exact limit cycle**: our core takes 1,600 and
  heals 1,600 per 100 rounds, sitting at the 500 cap; **five builders** (`#362`,
  `#518`, `#576`, `#171`, `#637`) hold seats and heal **every single round**
  (`#362` moves 3 times in 870 rounds); one builder grinds an enemy harvester
  100 times per 100 rounds that the enemy heals back; and **we build nothing at
  all from r300 to r899**.

The proximate cause is that a builder's turn is one action: a body on a seat
next to a damaged core **heals** rather than **attacks**. Conscription converts
a potential attacker into a permanent healer, and the guns live.

**Lock persistence.** The lock never released: 400 core-heal actions per 100
rounds, unbroken, r300-r999. Half of those rounds end at exactly 500 HP, so if
the Core read its HP after the round's heals the flag would clear every other
round and the falling edge would hand the conscripts back to their role
machines — visible immediately as movement. `#362` moved three times in 870
rounds. The Core therefore reads below-max on **every** turn, and
`hs3_flag`'s "full HP is the ONLY release" is unreachable inside any
heal-matched siege. **This is a near-absorbing state, not a transient.**

### 3.2 meander a — the link that is never laid, then the artery that is never repaired

| | base (hsd) | cand (ad) | Δ |
|---|---|---|---|
| we mined | 262 | 40 | **−222** |
| we delivered | 254 | 29 | −225 |
| they mined | 3 | 244 | **+241** |
| they delivered | **0** | 243 | +243 |
| in-transit losses (us / them) | 8 / 3 | 11 / 1 | +3 / −2 |
| **margin M** | **+254** | **−214** | **−468** |

**Closing arithmetic:**

| component | stacks on the margin | share |
|---|---|---|
| enemy economy unlocked (0 → 243 delivered) | **−241** | 51.5% |
| our mining collapse | **−222** | 47.4% |
| in-transit adjustments | **−5** | 1.1% |
| **sum** | **−468** | **100.0%** |
| **observed ΔM** | **−468** | **residual 0.0%** |

**Mechanism, in events.**

1. **r20 — conscription claims builder `#10`'s move.** It steps onto (10,6)
   instead of laying the conveyor there. The harvester-(7,6) → core link is
   never completed. `#10` reaches seat (10,4) at r24 as soon as `#3` vacates it,
   and ends the match with **857 heals from seat (13,3)**. `#7` (872 heals from
   (11,2)) and `#12` (468 heals from (12,5)) join it: **3 of 5 builders
   permanently seated**, against 15 / 5 / 16 lifetime heals in the base.
2. **r84-r93 — the enemy's builder `#13` walks to (13,6) and kills our conveyor
   at (13,5)**, ten attacks. **(13,5) is the last link of the only working
   chain** — the (16,6) harvester's route. In the base, `#13` never goes there
   and (13,5) survives the whole match. This is the corpus's clearest **H3**
   event: a genuinely different opponent trajectory on a different board.
3. **(13,5) is never rebuilt.** Fix D does not save it — its owner is on a heal
   seat. What Fix D *does* rebuild is **(10,6)** (r80 → dead r90, r93 → dead
   r103) and **(8,6)** (r74 → dead r104), both on the abandoned link, both under
   a live enemy grinder at (9,6): the **treadmill, confirmed again**, three
   rebuilds and the `SPUR_MAX_REBUILDS` cap exhausted, ~15 Ti, and zero delivery
   recovered.
4. **r100-r899 — bankruptcy.** Delivery **0 stacks/100 r**. Income is the 250
   Ti/100 r passive alone, and it is exactly consumed by 250 heals/100 r. Bank
   **0 Ti for 800 consecutive rounds**; ammo conversion **0** (the base converts
   500 Ti/100 r and its sentinel contests the middle); enemy attacks on us fall
   to 0 because nothing of ours is left to contest with.

The enemy's 0 → 243 is downstream of that bankruptcy — with no ammo and no
contesting builders, `det_v74` finishes the delivery chain it never managed in
the base (it adds (13,12), (12,12), (17,12) and a third harvester). It is a real
H3 term in the arithmetic; it is not an autonomous adaptation.

### 3.3 snowflake b — 300 frozen rounds in the growth window

| | base (hsd) | cand (ad) | Δ |
|---|---|---|---|
| we mined | 2,059 | 1,041 | **−1,018** |
| we delivered | 1,928 | 1,002 | −926 |
| they mined | 1,953 | 3,311 | **+1,358** |
| they delivered | 1,906 | 3,180 | +1,274 |
| we leaked to them / they leaked to us | 0 / 0 | 124 / 136 | +124 / +136 |
| in-transit losses (us / them) | 131 / 47 | 51 / 119 | −80 / +72 |
| **margin M** | **+22** | **−2,178** | **−2,200** |

**Closing arithmetic** (`ΔM = Δ(mine−lost)_us − 2·Δleak_us − Δ(mine−lost)_them + 2·Δleak_them`):

| component | stacks on the margin | share |
|---|---|---|
| enemy mining expansion (8.71 → 15.96 harvester-rounds/round) | **−1,286** | 58.5% |
| our mining collapse (15.43 → 5.84 harvester-rounds/round) | **−938** | 42.6% |
| net cross-belt leakage (both directions, new in the candidate) | **+24** | −1.1% |
| **sum** | **−2,200** | **100.0%** |
| **observed ΔM** | **−2,200** | **residual 0.0%** |

**Mechanism.** The decisive window is **r100-r399**, not the endgame:

| /100 r | base builds | base harv-rounds/r | base seated heals | cand builds | cand harv-rounds/r | cand seated heals | cand incoming |
|---|---|---|---|---|---|---|---|
| r100-199 | 17 | 3.49 | 100 | **0** | **3.00** | **315** | 1,154 |
| r200-299 | 55 | 10.72 | **0** | **1** | **3.00** | **249** | 900 |
| r300-399 | 61 | 15.65 | 186 | **6** | **3.00** | **326** | 1,160 |

Three-plus builders are seated for 300 rounds. Our harvester count does not move
off 3.00 while the base compounds to 15.65. The lock **does** release at r400
(seated heals fall to 9/100 r, core damage to 0) — but a compounding economy
that loses 300 rounds at the base of the curve does not recover: by r900 we are
at 9 harvesters against the base's 21, and the enemy — unraided (raid share
**17.2% → 2.2%**) — has gone from 8.71 to 21.00 harvester-rounds/round and 59 to
169 conveyors.

Snowflake is therefore the same channel with a different shape: **tempo loss in
the growth window** rather than a terminal lock.

---

## 4. Hypothesis ranking

| game | 1st | 2nd | 3rd | dominant channel |
|---|---|---|---|---|
| lighthouse a | **H1** — reserve seated instead of doing counterbattery; owns both the −666 and the −506 term | H3 — enemy keeps 5 harvesters it loses in the base, but only because we stop killing them | H2 — 3 rebuilds all game, ≤ 10 Ti | **H1** |
| meander a | **H1** — link abandoned at r20, 3/5 builders seated, bank 0 for 800 r | **H3** — enemy `#13` cuts (13,5) at r84-93 (never happens in the base); enemy completes its own chain | H2 — 5 rebuilds ≈ 15 Ti, treadmill confirmed, no delivery recovered | **H1**, with a real H3 term (~52% of ΔM by arithmetic, but downstream of H1) |
| snowflake b | **H1** — 300 rounds of frozen expansion, r100-r399 | H3 — enemy doubles unraided | H2 — 11 rebuilds, fewer than the base's 27 | **H1** |
| hive b | **H1** — delivery terminus lost at r39 | H3 — enemy survives because we cannot fund the siege | H2 — 0 rebuilds all game | **H1** |

**Same channel or map-dependent?** **Same channel — H1 — in all three primaries
and in hive.** What is map-dependent is only *which* output of the reserve is
the load-bearing one:

- lighthouse: the reserve's **counterbattery** (guns adjacent to our own core);
- meander: the reserve's **link laying** (a single-artery economy);
- snowflake: the reserve's **expansion rate** (during exponential growth);
- hive: the reserve's **second delivery terminus** (which funds the siege).

The H3 term is real but consistently **second-order and consequential**: on
lighthouse and snowflake the enemy does not build *more*, it merely *loses less*
to a raid that stops happening. Only meander shows a genuinely new opponent
trajectory (`#13` at (13,6)). The free displacement meter agrees and puts a
small bound on it: `det_v74`'s own caught `Position out of vision range`
tracebacks in its `_expand` appear in **exactly one** of the ten legs —
`snowflake_s1_b_ad`, **5 tracebacks**, against 0 in its base pair and 0 in all
eight other legs. Displacement of the opponent's builders is not what is
happening here; if anything the candidate displaces `det_v74` *less* than the
base does, because it never leaves home.

**H2 (spur repair) is not the owner of any loss.** Its measured signature across
the corpus is: fewer rebuilds than the base on two primaries, ≤ 5 on the third,
0 on hive — and 43 on **archipelago, the game the candidate wins**. The
treadmill is confirmed again on meander (three rebuilds of (10,6) inside 23
rounds, all re-cut) but it is ~15 Ti and it recovers no delivery. Fix D's
verdict from the archb addendum ("downgraded — a treadmill against a live
saboteur") stands, unchanged and unaggravated.

---

## 5. Secondary — hive b: where the r602 core kill went

Base kills `det_v74`'s core at **r602**. Candidate reaches r1000 and loses the
tiebreak by **one stack** (2,470 vs 2,480).

**It is not a recall of the killers, and not a lost tempo at the front — it is a
lost delivery terminus at home.**

| | base | cand |
|---|---|---|
| our delivery termini | **two**: (23,4) 148 stacks + (20,3) 144 stacks | **one**: (23,4) 247 stacks |
| our delivery rate | **48.5 stacks/100 r** | **24.7 stacks/100 r** |
| our forward turrets firing | **three**: (7,16) 250 shots, (3,17) 149, (5,18) 13 | **one**: (7,16), 321 shots over 1000 r |
| damage on the enemy core | 900 → 970 → **1,256** → **1,175** per 100 r | flat **~630** per 100 r for 900 rounds |
| enemy core HP | 482 → 188 (r400s) → 13 (r500s) → **dead r602** | never below 494 — 630 in, 630 healed |
| our builder-rounds idle | 25.3% | **43.8%** |
| our raid share | 7.9% | **0.7%** |
| our seat-heal share | 18.5% | **31.6%** |

**Chain.** At **r39** — one round after the flag becomes visible, exactly on
schedule — builder `#10` walks off its link line and the **(20,3) terminus is
never built**. That terminus carried **23.9 stacks/100 r** in the base; our rate
falls by **23.8 stacks/100 r**. *The single lost link accounts for 100.4% of the
delivery-rate loss.* With half the income the bank never leaves 16-19 Ti, the
second and third gunners at (3,17)/(5,18) are never bought, our siege output
stays at ~630 HP/100 r, and `det_v74` heals exactly that much. From r200 the
game is a 100-round-periodic frozen cycle: identical delivery, identical heals,
identical damage, zero builds, zero raids, for 800 rounds.

So the answer to "did conscription pull the killer builders home?" is **no** —
the killers were turrets, and the conscription killed their *funding*, not their
crew.

---

## 6. Control — archipelago a (one paragraph)

Confirmed: the gain mechanism is the known counterbattery story and nothing new.
The candidate converts a **r190 core loss into a r1000 win, 12,000 vs 8,410 Ti**.
Conscription arms at r50 and is visible at r51 — the divergence round, exact —
and the recalled bodies **remove** the incoming instead of paying it: enemy
gunners destroyed at r~200, r~400 and twice around r600, our builders' attack
targets in every window from r200 to r699 being almost exclusively
`(enemy, gunner)` (12 / 9 / 13 / 13 attacks per window), enemy fire on our core
ceasing entirely after r699. Incoming falls **8.53 → 3.45 HP/round**, the
conscription share falls **32.7% → 13.3%** (it stands itself down, exactly as
the archb addendum described), our delivery rate rises **46.8 → 120.0
stacks/100 r** and our harvester-rounds **2.97 → 11.66** per round. Fix D runs
its treadmill here too (43 rebuild events, the most in the corpus) and it does
not matter either way. This leg is the discriminator, not a counter-example: it
is the only leg where incoming *falls*.

---

## 7. Kladde inference — **INFERENCE ONLY, no kladde data in this corpus**

> **Flagged:** the corpus contains zero kladde-guard games. What follows is a
> mechanism-to-symptom inference from the five det games above plus the two
> toggles' source, offered to aim an ablation. It is not a measurement.

Builder-side report: against **kladde guard**, median game length **halved
(335 → 160)** with win rate roughly flat.

**Suspect: the conscription half (HS3), not SPUR.** This is *not* the obvious
reading, because on this corpus conscription is measurably a game *lengthener* —
candidate length ≥ base length in 5/5 pairs, strictly longer in 2 (602 → 1000,
190 → 1000). The reason to suspect it anyway is the funding mechanism the corpus
exposes:

**Healing is titanium-funded, and conscription defunds it.** Every conscript
spends 1 Ti per 4 HP, every round, forever, while simultaneously not mining, not
linking and not expanding. Measured on meander: bank **0 Ti for 800 consecutive
rounds**, with heals paid entirely out of the 250 Ti/100 r passive drip — i.e.
the heal rate is pinned at exactly 2.5/round because that is all the passive
income can buy. Meander survives only because incoming there is 8.08 HP/round.
**On any map where incoming exceeds what the passive drip can heal, the same
state is a fast death: the reserve has stopped the economy, the bank empties,
the heals stop, and the core falls.** A guard opponent that applies steady
early pressure is exactly the shape that produces that. And the win rate stays
flat because the games moving into the early-death mode are games that were
being lost slowly anyway.

The corollary prediction — the one that makes this falsifiable — is that the
shortening should be **bimodal, not a uniform shift**: games where the flag
never arms should be unchanged in length, and games where it arms early should
collapse. A halved *median* with a flat *mean-ish* win rate is what a bimodal
split looks like.

**SPUR is the weaker suspect** but has one plausible route worth excluding: a
spur-planted `link_queue` is non-empty, and the source notes that the `role_n == 3`
saboteur conversion reads `not self.link_queue`. Frequent spur queues would
suppress the saboteur conversion — which lengthens rather than shortens games.

**What the ablation should look for.** Two arms against kladde guard,
`HS3_ON=False / SPUR_ON=True` and `HS3_ON=True / SPUR_ON=False`, det, NOISE_OFF,
paired on seeds, and report:

1. the **length distribution**, not the median — specifically P10/P50/P90 and
   the bimodality;
2. the **`win_condition` mix** (`core_destroyed` against us vs
   `titanium_collected`) — the conscription story predicts a rise in
   `core_destroyed`-against-us among the short games, the SPUR story does not;
3. the **arming round** of the HS3 flag per game (derivable from the replay as
   in §1: first below-max Core read + 12), correlated with game length — the
   prediction is a strong negative correlation in the HS3-on arm and none in the
   HS3-off arm;
4. **bank-at-0 round-count** and **harvester-rounds/round** in the first 200
   rounds — the defunding signature;
5. spur rebuild counts and builder deaths on rebuilt tiles, to close out H2.

---

## 8. Self-checks

### 8.1 Parser validation

- **`core_delivery_stacks × 10 == titaniumCollected`: 20 / 20 team-sides exact**,
  across all ten replays, against the `fcode` JSON sidecars. (lighthouse
  1247/1185 → 12470/11850 and 1217/1382 → 12170/13820; meander 254/0 and 29/243;
  snowflake 1928/1906 and 1002/3180; hive 292/106 and 247/248; archipelago 89/128
  and 1200/841.)
- **Stack-flow conservation**: for every replay,
  `mined_us + mined_them == stacks_originated`, with **unknown-origin = 0 in
  10/10** — every stack's emitting harvester was identified, so no delivery is
  attributed by guesswork.
- **Conveyors treated as bot-passable** throughout (the documented decoder trap);
  seat occupancy is computed from builder-bot positions only, never from tile
  emptiness.
- Round indexing per `tools/replay_schema.md`: `turns[i]` **is** round `i`,
  0-based. Cores seeded from `map.cores` at 500/500 before turn 0.

### 8.2 Ledger closure

| game | ΔM observed (stacks) | ΔM from named components | residual |
|---|---|---|---|
| lighthouse a | −227 | −227 | **0.0%** |
| meander a | −468 | −468 | **0.0%** |
| snowflake b | −2,200 | −2,200 | **0.0%** |
| hive b (rate form) | −23.8 stacks/100 r on our side | −23.9 (the lost (20,3) terminus) | **0.4%** |

Closure is exact on the primaries because the decomposition is an integer
identity over followed stacks, not a regression.

### 8.3 Bounded unexplained residue

- **In-transit / undelivered stacks** (destroyed with their conveyor, or still on
  the belt at r1000): 11-178 per replay, **0.3%-4.4%** of stacks originated.
  These are carried **explicitly** as the `lost` term in every closing sum, so
  they are accounted, not residue.
- **Divergence lag**: 2 of 5 divergences land later than the arming round + 1
  (meander +2, snowflake +9). Attributed to the `_hs3_busy_building` deferral
  gate; not separately verified round-by-round. Bound: it does not affect any
  arithmetic in §3, which is computed from whole-game flows.
- **The `attack_own_side` / `raid` split** is a geometric proxy (nearer whose
  core), not a read of intent. It is used only for shares in §2 and never inside
  a closing sum.
- **Fix D's cost** is upper-bounded by an over-inclusive proxy ("we built where
  our own building had died"), which also counts ordinary re-planning. The bound
  (≤ 60 Ti across the three primaries) is therefore conservative in the safe
  direction.
- **Stack ids** are assumed not to be recycled within a match. If they were, the
  flow ledger would under-count originations — it does not, since
  `originated == delivered + in-flight` holds in all ten replays and matches
  `titaniumCollected` exactly.

---

## 9. What this hands back

1. **`_v87ad` should not ship as-is**, and the loss is not a tuning problem: the
   conscription's release condition ("Core at full HP") is unreachable inside the
   equilibrium the conscription itself creates. Measured dwell: the rest of the
   match in 3 of 5 games.
2. **The archb read's §6 rank-1/rank-2 merge should be narrowed.** Staffing is
   the delivery mechanism for counterbattery **only when the enemy's gun is
   orthogonally adjacent to a heal seat** (archb, archipelago). When it is not
   (lighthouse: guns at (3,7)/(4,9); hive; snowflake), conscription buys a
   permanent garrison that pays the damage instead of removing it, and a seated
   builder's single action goes to `heal`, never to `attack`.
3. **A cheap discriminator exists for any future HS-family candidate**: does
   incoming HP/round *fall* between base and candidate? It falls only in the leg
   that wins (8.53 → 3.45) and rises in all four that lose. `heal ÷ incoming` is
   ≈ 1.00 everywhere and carries no information.
4. **Two adjacent findings worth issues** (not acted on here — research arm):
   (a) the base leaks **460 of 1,734 mined stacks (27%)** into the *enemy* core
   on lighthouse, all game, through its own sprawling belt — a live v75 defect
   the candidate masks rather than fixes; (b) lighthouse candidate builder `#5`
   is **idle for 874 consecutive rounds** — the archb idle-reserve pathology,
   still present, because `HS3_ROLES` covers only roles 2 and 3.

---

## Post-landing scope correction (2026-08-08 15:0x — builder toggle ablation, research-adopted)

The builder's direct counterfactual ablation (6 flip games × hs3-only /
spur-only, det) CONFIRMS the HS3-lock attribution on all three primaries
(archipelago / hive / snowflake: hs3-only reproduces full-ad, spur-only
reproduces base) and REFINES two claims in this document:

1. **"Fix D (SPUR) inert everywhere" is scope-corrected.** On lighthouse
   the flip reproduces under EITHER toggle alone — SPUR is not inert there
   in the counterfactual sense. This document's divergence-point analysis
   is correct FOR THE FULL-AD WORLD (at full-ad's divergence, Fix D had
   not fired); the single-toggle worlds have different divergence points,
   which the method here cannot see. Both results are true in their own
   worlds; the universal phrasing was too strong.
2. **meander (and moonrise in the kladde corpus) reproduce under NEITHER
   single toggle** — combination-dependent, margins ≤100 Ti.

Standing rule adopted from this exchange (builder, board 15:0x): r1000
margin-flip det games are **butterfly-class** — banned as attribution or
acceptance criteria; only regime-change games (core-death → survival)
carry det weight. The three primaries in this document remain valid as
mechanism DESCRIPTION of the full-ad world; their use as toggle
attribution is superseded by the direct ablation.

---

# Addendum: kladde shape corpus (noisy, seed-1)

**Research-arm, 2026-08-08.** Second corpus, commissioned to test whether the
acceptance leg's kladde-guard length collapse (median 335 → 160) is the same
HS3 mechanism this document decodes. Answers Q1-Q4 as put.

> ## CAVEAT HEADER — BINDING
>
> 1. **Seed 1 only.** Per-map rows are **single games**. The target is the
>    shape/length distribution. **No win-rate claims from this corpus** (the
>    24/30 vs 25/30 headline is reported as context, never as evidence).
> 2. **NOISE ON — and this voids the pairing.** `NOISE_ON = True` in *both*
>    bots (Piece G) draws `spawn_salt = random.Random().randrange(97)` once per
>    process, from OS entropy. The source comment says it outright: *"at the
>    cost of exact paired-seed reproducibility."* **Measured: 29 of 30 pairs
>    diverge at round 0-3** (25 at r0, 27 by r1), i.e. at the first spawn — before HS3
>    can arm (needs 12 bleeding rounds) and before SPUR can fire (needs a
>    destroyed own building). One pair, `atoll-b`, is byte-identical with
>    ΔT = 0 — the salts collided (expected ≈ 0.3 collisions in 30 draws over 97
>    salts; observed 1), which confirms the harness and the seed are sound and
>    that the divergence is the salt, not a parser artefact. **Consequence: a
>    per-map ΔT in this corpus is not an intervention effect. It is one draw
>    from a noisy distribution, and the 17 "big movers" are a mixture of toggle
>    effect and spawn-salt luck that no per-game analysis can separate.**
> 3. **Zero TLEs** in all 60 replays, both teams (`--tle 10`). The candidate's
>    extra per-turn work is not costing turns; that channel is excluded.
> 4. **This corpus therefore supports distribution- and marker-level statements
>    only.** Every claim below is either (a) a *description* of what shape the
>    games took, or (b) a *conditional* comparison using an arming predicate
>    that is computable in **both** arms and is **inert in the base** — never a
>    per-game toggle attribution. Toggle attribution belongs to the builder's
>    direct ablation (see the scope correction above), not here.
> 5. Consistent with the standing rule: r1000 margin-flip games are
>    **butterfly-class**, description only.

## A.1 Method — an arming predicate that works without a paired prefix

The divergence method of §1 needs identical prefixes and cannot be used here.
Instead the HS3 arming predicate is **reconstructed from our Core's own HP
trace**, which is measurable in any replay: the Core acts first in the round, so
it reads the *previous* round's end-of-round HP; simulate `hs3_bleed` /
`hs3_drop_rnd` / `hs3_flag` over that series with `HS3_BLEED_ROUNDS = 12` and one
round of store buffering. This yields, per game, `arm_round` (first round a
conscript could see the flag) and `armed_frac` (share of rounds it is visible).

The predicate is computed **identically in both arms**, and in `hsd` it is
**inert** — `_v85hsd` has no HS3 code to respond to it. The base arm is therefore
a proper control for "what a bleeding core does *without* conscription", and the
comparison is a difference-in-differences on behaviour inside vs outside the
armed window.

**The behavioural response is present and large:** median ratio of our
seat-occupancy inside the armed window to outside it —

| arm | n (armed_frac ≥ 0.10) | median seat-occupancy ratio (armed ÷ unarmed) |
|---|---|---|
| hsd (predicate inert) | 7 | **1.52** |
| **ad** | 8 | **2.91** |

The candidate roughly **doubles** the staffing response to the same trigger.
Conscription is really firing, and the marker detects it.

## A.2 Q1 — Is the shortening HS3-driven? **No.**

Length distribution, split by the same predicate (`arm_round ≤ 200` = the flag
could plausibly influence the game's course):

| arm | subpopulation | n | median R | mean R | lengths |
|---|---|---|---|---|---|
| hsd | arms ≤ r200 | 12 | 364 | 451 | 83, 148, 182, 227, 275, 358, 370, 451, 580, 739, 1000, 1000 |
| **ad** | **arms ≤ r200** | 11 | 357 | **514** | **61, 71, 83, 103, 130,** 357, **853, 998, 1000, 1000, 1000** |
| hsd | never arms | 16 | 306 | 462 | 69 … 1000 |
| **ad** | **never arms** | 17 | **235** | **386** | 66 … 1000 |

Two readings, both against the naive story:

1. **The median shortening lives in the HS3-inert subpopulation.** Games where
   the flag never arms go 306 → 235 median (462 → 386 mean). Those games contain
   **no conscription at all** — the mechanism cannot be responsible for their
   length.
2. **Where HS3 *does* engage, the candidate gets *longer* on average
   (451 → 514 mean) and, more tellingly, becomes bimodal.** The base's
   early-arming lengths are a smooth spread (7 of 12 in the 200-850 middle,
   σ = 303). The candidate's are hollowed out: **5 games ≤ 130, 5 games ≥ 853,
   exactly 1 in the middle** (σ = 425). This is the bimodality the §7
   pre-registered inference predicted — but with the *opposite* sign on which
   half HS3 owns: HS3 owns the **long** peak, not the short one.

Correlation of shortening with conscription firing, stated plainly: **6 of the 9
shortened big movers never arm the flag at all** (`armed_frac = 0.00`), and the
other 3 arm only 4-75 rounds before their game ends. **4 of the 8 lengthened big
movers carry sustained conscription** (`armed_frac` 0.55-0.93), and all four run
to 853-1000 rounds.

This is fully consistent with §1-§5: conscription's measured signature is a
homeostatic lock that pushes games to the cap (there: 602 → 1000, 190 → 1000).

## A.3 Q2 — Direction split: all 17 big movers classified

`armF` / `arm@` are the candidate leg's `armed_frac` / `arm_round`; `rb` = the
candidate's rebuild-event count (over-inclusive SPUR proxy). **Classification is
shape description, not toggle attribution** (caveat 4).

### Shorter (9) — **9 of 9 are "our kill arrives earlier". Zero are "our death faster". Zero are kladde's siege resolving earlier.**

| game | hsd → ad | ΔT | outcome transition | armF | arm@ | rb | shape class |
|---|---|---|---|---|---|---|---|
| nordkap b | 1000 → 130 | **−870** | W tiebreak → **W core kill** | 0.13 | 55 | 1 | eco stalemate converted to an early kill |
| lighthouse a | 1000 → 269 | −731 | W tiebreak → **W core kill** | **0.00** | — | 10 | eco stalemate converted to a kill; **HS3 never arms** |
| nordkap a | 1000 → 300 | −700 | **L** tiebreak → **W core kill** | **0.00** | — | 4 | seat flip; **HS3 never arms** |
| lighthouse b | 563 → 83 | −480 | **L** core death → **W core kill** | 0.29 | 53 | 1 | seat flip; flag arms 30 r before the end |
| jackpot b | 1000 → 556 | −444 | W tiebreak → **W core kill** | **0.00** | — | 29 | eco stalemate converted to a kill; **HS3 never arms**, SPUR busiest in corpus |
| heart a | 451 → 61 | −390 | W core kill → W core kill | 0.07 | 57 | 0 | kill accelerated; flag arms 4 r before the end |
| atoll a | 402 → 94 | −308 | W core kill → W core kill | **0.00** | — | **0** | kill accelerated; **both toggles provably inert** |
| meander b | 358 → 177 | −181 | **L** core death → **W core kill** | **0.00** | — | 2 | seat flip; **HS3 never arms** |
| saga a | 287 → 127 | −160 | W core kill → W core kill | **0.00** | — | **0** | kill accelerated; **both toggles provably inert** |

Every shortened mover is our offence landing sooner — in three of them
(nordkap-a, lighthouse-b, meander-b) converting a base loss into a win, and in
four converting a 1000-round economic stalemate into a core kill. **Not one
shortened game is us dying faster.** The §7 inference's proposed mechanism
("conscription defunds the heal, the core falls early") is **refuted on this
corpus**: it predicts a rise in `core_destroyed`-against-us among the short
games, and there are none.

### Longer (8)

| game | hsd → ad | ΔT | outcome transition | armF | arm@ | rb | shape class |
|---|---|---|---|---|---|---|---|
| moonrise b | 113 → 1000 | **+887** | W core kill → **L tiebreak** | **0.77** | 151 | 0 | **kill → r1000 lock.** Flag arms *after* the base's r113 decision, so it cannot have caused the game to pass r113 — but it then holds the stalemate for 850 rounds. **Combination-dependent class per the ablation.** |
| antler b | 83 → 1000 | +917 | W core kill → **L tiebreak** | 0.01 | 778 | 28 | kill → r1000 stalemate **formed without conscription** (flag arms at r778, long after) |
| snowflake b | 325 → 1000 | +675 | W core kill → **L tiebreak** | **0.65** | 225 | 4 | **kill → r1000 lock**, flag armed before the base's decision round |
| archipelago b | 153 → 756 | +603 | W core kill → W core kill | **0.00** | — | **0** | kill delayed 600 r with **both toggles provably inert** |
| fjordgate a | 370 → 853 | +483 | W core kill → W core kill | **0.55** | 143 | 5 | sustained lock; the kill still lands, 483 r later |
| meander a | 580 → 998 | +418 | L core death → L core death | 0.12 | 100 | 7 | our death delayed 418 r |
| fjordgate b | 739 → 1000 | +261 | **L core death → L tiebreak** | **0.93** | 47 | 0 | **the lock does its job**: heal ÷ incoming **0.89 → 1.21**, our core survives to the cap instead of dying at r739 — and still loses the tiebreak |
| eider a | 227 → 357 | +130 | W core kill → W core kill | 0.01 | 51 | 12 | kill delayed |

**Stalemate taxonomy for the longer half:** 3 are the §5 hive-b pattern exactly
(**core kill → r1000 titanium tiebreak loss**: moonrise-b, snowflake-b,
antler-b); 1 is a **core-death → tiebreak-loss save** (fjordgate-b); 4 are simply
a delayed decision. Of the four with sustained conscription
(`armF` ≥ 0.55) — fjordgate-a/b, moonrise-b, snowflake-b — **all four run
853-1000 rounds**.

### The win-condition swap — the crispest sort in the corpus

Aggregate mix is **identical**: `core_destroyed` 22 / `titanium_collected` 8 in
*both* arms. But **8 games swapped sides**, and the swap sorts almost perfectly
on conscription:

| direction | games | HS3 markers |
|---|---|---|
| `core_destroyed` → `titanium_collected` (4) | antler-b, **fjordgate-b**, **moonrise-b**, **snowflake-b** | **3 of 4 have sustained conscription** (armF 0.93 / 0.77 / 0.65); antler-b arms only at r778 |
| `titanium_collected` → `core_destroyed` (4) | jackpot-b, lighthouse-a, nordkap-a, nordkap-b | **3 of 4 never arm at all**; nordkap-b arms at r55 with armF 0.13 |

Conscription does not change *how often* games end by core kill — it changes
*which* games do, pushing the games it engages toward the tiebreak cap and
leaving the rest to resolve faster.

## A.4 Q3 — Does `heal ÷ incoming ≈ 1` reproduce in the noisy regime vs a picket-class opponent?

**Yes, conditional on a sustained armed window — and the LEVEL still
discriminates.** Measured *inside the armed window only* (the regime where the
homeostat is actually engaged):

| game | arm | R | armed frac | incoming HP/r | heal HP/r | **h ÷ i** | delivery /100 r inside armed | outside armed | outcome |
|---|---|---|---|---|---|---|---|---|---|
| fjordgate b | hsd | 739 | 0.95 | 2.90 | 2.58 | **0.89** | 0.00 | 0.00 | core destroyed (we die r739) |
| **fjordgate b** | **ad** | **1000** | 0.93 | 3.00 | 3.63 | **1.21** | 0.00 | 0.00 | tiebreak (**core survives**) |
| moonrise b | ad | 1000 | 0.77 | 3.85 | 3.98 | **1.03** | **0.00** | 10.21 | tiebreak loss |
| snowflake b | ad | 1000 | 0.65 | 3.98 | 3.99 | **1.00** | **0.31** | 48.31 | tiebreak loss |
| fjordgate a | ad | 853 | 0.55 | 2.04 | 3.65 | 1.79 | **0.00** | 8.64 | core kill (W) |
| fjordgate a | hsd | 370 | 0.52 | 0.46 | 1.11 | 2.40 | 24.74 | 23.86 | core kill (W) |

Three points:

1. **The `h ÷ i ≈ 1.00` pin reproduces** in every candidate leg that reaches a
   sustained lock: **1.21, 1.03, 1.00**. It does *not* reproduce in short or
   intermittently-armed games — there the ratio scatters 0.36-3.75 in both arms,
   because a 4-round armed window has no time to settle. **Scope correction to
   §2: the `≈ 1` pin is a property of sustained sieges, not of the machinery in
   general.** In the det corpus every game was a 1000-round siege, so the
   distinction did not surface.
2. **The level still discriminates outcome, and here it discriminates in the
   *saving* direction.** fjordgate-b is the same predicate, the same map, the
   same opponent: base sits at **0.89 and the core dies at r739**; candidate sits
   at **1.21 and the core survives to the cap**. Conscription did exactly what
   it was built to do — and converted a core-death loss into a tiebreak loss.
3. **The economic price reproduces intact.** Delivery *inside* the armed window
   versus outside it, in the candidate's sustained locks: **0.00 vs 10.21**
   (moonrise-b), **0.31 vs 48.31** (snowflake-b — 0.6% of the unarmed rate),
   **0.00 vs 8.64** (fjordgate-a). The base, under the *same* predicate, shows no
   such collapse: fjordgate-a **24.74 vs 23.86** (ratio 1.04), meander-a
   **15.81 vs 13.70** (1.15). Median delivery ratio armed÷unarmed across the arm:
   **hsd 1.02, ad 0.98** overall — but the divergence is concentrated exactly in
   the sustained locks, which is where §3's mechanism says it should be.

So the picket-class opponent does not change the homeostat's behaviour; it
changes how often a sustained siege forms at all.

## A.5 Q4 — Corroborate or complicate? **Both, cleanly split.**

**CORROBORATES — the lengthening tail tracks HS3 behavioural markers.** Every
independent marker moves the way §1-§5 says it should, measured against the same
predicate held inert in the base:

- seat-occupancy response to the armed window: **1.52 (base) → 2.91 (candidate)**;
- seat-heal share of builder-rounds in the sustained locks: **+8.2 to +19.7 pp**
  (fjordgate-a 3.9 → 12.1, fjordgate-b 10.2 → 23.3, moonrise-b 0.0 → 19.7,
  snowflake-b 0.0 → 12.1);
- delivery collapse inside the armed window, absent in the base under the same
  predicate;
- `h ÷ i` pinned at 1.00-1.21 in every sustained lock;
- all four sustained-conscription games run to **853-1000 rounds**, and three of
  them are the §5 hive-b pattern (core kill → r1000 tiebreak loss) reproduced
  against a different opponent in a different regime.

**COMPLICATES — the *shortening* half, which was the corpus's headline, does not
track HS3 markers at all.** 6 of 9 shortened big movers never arm the flag; two
of those (atoll-a −308, saga-a −160) additionally show **zero** rebuild events,
so both toggles are provably inert in them and the candidate is behaviourally
the base. The acceptance leg's "median 335 → 160" is therefore **not** an HS3
effect on this evidence — and, per caveat 2, a large part of it may not be an
effect of `_v87ad` at all, because the pairing is void and the same bot re-run
draws a different spawn salt.

**Phrasing discipline, per the adopted scope correction.** I am **not** claiming
SPUR-exclusion from marker absence. The opposite reading is live and, given the
ablation, more likely: **a full-ad game in which HS3 never arms *is* a spur-only
world**, and that is precisely the subpopulation the shortening lives in. Three
of the six carry real SPUR activity (jackpot-b **29** rebuilds, lighthouse-a 10,
nordkap-a 4) — and the builder's ablation independently found that **lighthouse
flips under spur-only**. `lighthouse-a` sitting in this corpus's shortening set
with HS3 never arming and 10 rebuilds is a convergence between the two corpora,
not a coincidence to explain away. It is also not proof: seed-1 single games
under independent spawn salts cannot attribute, and two of the six have no SPUR
activity either.

**Net for the ablation stake.** The kladde corpus **supports** ablating HS3 as
the owner of the *shape* change in the direction this document decoded
(lock-forming, cap-seeking, economy-stopping), and **redirects** the
length-shortening question away from HS3 toward the spur-only slice and the
noise regime. Recommended, in order:

1. **Re-run the kladde shape corpus with `NOISE_ON = False`** (or ≥ 20 seeds per
   cell). As it stands the pairing carries no information and the headline
   median is unbounded by noise. This is the single highest-value fix and it is
   free.
2. In the HS3 arm, report **`arm_round` and `armed_frac` per game** alongside
   length — the predicate is reconstructable from the replay (A.1) and turns
   length into a conditional statement instead of a marginal one.
3. Score the **win-condition swap**, not the win rate: the 22/8 aggregate is
   identical while 8 games changed sides. Aggregate mix is blind to the effect;
   the swap is not.

## A.6 Self-checks (kladde corpus)

- **`core_delivery_stacks × 10 == titaniumCollected`: 120 / 120 team-sides
  exact**, across all 60 replays, against the `fcode` JSON sidecars.
- **Pairing integrity**: 30/30 pairs matched on map/seat/seed; `atoll-b`
  byte-identical (ΔT = 0, no divergent round found) confirms the harness is
  deterministic when the salts collide.
- **Divergence census** (histogram over 30 pairs): **r0 = 25, r1 = 2, r2 = 1,
  r3 = 1, identical = 1** (`atoll-b`). **No pair diverges later than r3**, so no
  pair has an interpretable shared prefix.
- **TLE census**: `botOutput.tled` set on **0 records** in all 60 replays, both
  teams. The CPU channel is excluded, not assumed away.
- **Arming predicate**: validated against the det corpus of §1, where the ground
  truth is known — it reproduces the measured divergence rounds exactly on
  lighthouse (r100), hive (r39) and archipelago (r51), and within +2 on meander.
  It is a *predicate*, not a detection of the flag itself; on snowflake it fires
  9 rounds before the observed behavioural change (the `_hs3_busy_building`
  deferral), so `arm_round` should be read as an **upper bound on how early**
  conscription could have acted.
- **Bounded unexplained**: the `rebuilds` column is the same over-inclusive proxy
  as §8.3 (it counts ordinary re-planning too), so it bounds SPUR activity from
  above and can never be used to assert SPUR *absence* — consistent with the
  scope correction. `armed_frac` is endogenous to game length (a longer siege
  has more armed rounds), which is why `arm_round` — an early, length-independent
  marker — carries the causal argument in A.3 and `armed_frac` only describes
  intensity.

---

# Addendum: lighthouse misroute rates, hsd vs v76 (noisy 32-game corpus, pooled)

**Research-arm, 2026-08-08.** Fresh corpus, commissioned to (a) re-confirm
`_v85hsd`'s misroute rate outside the single det game that produced the
460/1,734 = 27% headline in §9 item 4(a), and (b) test whether `opp_v76`'s
`_chain_dead` watchdog — which targets orphaned harvesters, the misroute
precondition — measurably lowers that rate against the same base.

> ## CAVEAT HEADER — BINDING
>
> - **NOISE ON.** Per-game pairing is void (spawn-salt rule, same mechanism as
>   the kladde addendum above). **Pooled rates only, both seats combined per
>   bot.** No per-seed or per-game comparison is load-bearing.
> - **Scope: misroute channel only.** Neither `_v85hsd` nor `opp_v76` plants
>   siphon-belt infrastructure, so this pairing cannot measure the ~81%-of-
>   wild-volume adjacency-siphon channel documented against opponent-planted
>   siphon belts elsewhere; that channel is out of scope here by construction
>   of the corpus (see `replay_archive/diag_leak_lighthouse_2026-08-08/README.md`).
> - **Tooling**: `scratchpad/ad_flips/{decode,flow}.py`, extended with dynamic
>   belt-tile ownership tracking (conveyor/splitter/harvester place/remove
>   events) so every hop of a stack's `ResourceMove` path can be attributed to
>   an owning team, not just its origin and delivery endpoints.
> - Corpus: `replay_archive/diag_leak_lighthouse_2026-08-08/`, `_v85hsd`
>   (md5 `4a2aeb50ef8ff63ea55ddc25baca2628`, = live ladder v75 "Eir 8") vs
>   `opp_v76/main.py` (md5 `580dfe40926c4feed521d96630eace6c`), lighthouse map
>   only, seeds 1-16, both seat orderings (`hsdA`/`hsdB`), `--tle 10`.

## B.1 Validation

`core_deliv × 10 == titaniumCollected`, checked per team-side against the
`fcode` JSON sidecars (`*_titanium_collected`): **64/64 team-sides exact**
(32 games × 2 sides). No game excluded — every replay parsed cleanly, zero
unknown-origin stacks (`origin` team always resolved via live harvester/
conveyor/splitter ownership at the moment of first move).

## B.2 Pooled misroute rates

Stacks leaked into the enemy core ÷ stacks mined, pooled across both seats,
32 games:

| bot | mined | leaked → enemy core | delivered to own core | lost in transit | **misroute rate** | lost-in-transit rate |
|---|---|---|---|---|---|---|
| **hsd** (`_v85hsd`) | 19,923 | 460 | 19,026 | 437 | **2.31%** | 2.19% |
| **v76** (`opp_v76`) | 24,738 | 555 | 23,636 | 547 | **2.24%** | 2.21% |

**vs. the prior det figure (460/1,734 = 27%, one game, NOISE_OFF):** the
pooled 32-game rate is **2.31%, roughly 12× lower — not the same order of
magnitude.** The absolute leaked-stack count (460) is coincidentally
identical to the det game's, but the denominator here is ~11.5× larger
(19,923 mined vs 1,734), because most of the 32 games run to or near r1000
while the det game's misroute accumulated across a shorter effective window.
The det figure was never claimed as a corpus-representative rate (§9 item
4(a) calls it a defect measured *on lighthouse, all game*, in one leg of a
paired det comparison) — this addendum shows it does not generalize as a
per-game-typical rate once seed/seat variety and the noisy regime are
admitted. **The channel is real and reproduces, but at roughly 2%, not 27%,
pooled.**

**Watchdog question: is v76's rate materially lower than hsd's?** **No.**
2.24% (v76) vs 2.31% (hsd) — statistically indistinguishable given the pooled
counts, and if anything v76 leaked marginally *more* stacks in both absolute
(555 vs 460) and relative terms across a larger mined base. `_chain_dead`
does not show a measurable protective effect against misroute in this
corpus, despite targeting orphaned harvesters (see B.3 for why: the leaks are
not diffuse "sprawling belt" cases the watchdog would generically catch, but
a handful of contested border-ore tiles specific to each game).

## B.3 Mechanism spot-check — **unexpected result, flagged prominently**

The pre-registered expectation (task framing, README) was that this corpus
would be **misroute-dominated**: leaked stacks traveling on the **miner's
own** conveyor/splitter network the whole way, only crossing into the enemy
core on the final hop (the mechanism named in §9 item 4(a) and in §3.1's
"four orphaned harvesters"). Walking the full hop-by-hop tile-ownership
sequence for every leaked stack (not just origin/destination) shows this is
**not quite what's happening**:

| | hsd leaked (n=460) | v76 leaked (n=555) |
|---|---|---|
| hop-count distribution | 4:7, 5:169, 6:145, 8:77, 10:62 | 4:5, 5:2, 10:85, 11:171, 12:121, 15:171 |
| all-own-belt (every hop's src tile owned by the miner) | **0 / 460 (0.0%)** | **0 / 555 (0.0%)** |
| single-hop (harvester → enemy core direct) | 0 / 460 | 0 / 555 |
| ≥2-hop leaks where every hop *after the first* is on the **receiver's** own network | 723 / 1,015 combined (71%) | (same pooled figure) |

**Every leaked stack takes exactly one hop on the miner's own tile (the
harvester's output move) and then rides multiple hops (4-14) entirely on the
**receiver's** belt network** before landing in the receiver's core — the
opposite of "traveling on the owner's own belt." This is the "zero
own-belt hops [after origination]" pattern the task asked to flag if
substantial, and it is substantial: **0% of leaked stacks are pure
own-belt misroute by the strict definition.**

This is **not**, however, deliberately-planted siphon infrastructure (no
belts built specifically to intercept an opponent's output — consistent with
the corpus design). Drilling into origin tiles resolves the mechanism: leaks
are extremely concentrated —

- **hsd**: 6 distinct (game, origin-tile) pairs across 6/32 games, e.g.
  `(8,4)` in s5, `(6,13)` in s3, `(8,3)` in s15/s8, `(7,12)` in s11 —
  contested ore tiles near the map's centerline.
- **v76**: 14 distinct (game, origin-tile) pairs across 7/32 games, same
  centerline ore cluster (`(15,7)`, `(9,2)`, `(0,8)`, `(7,11)`, `(8,3)`,
  `(8,4)`, `(6,13)`, `(7,12)`).

This matches the mechanism already named in §3.1: a harvester rebuilt on a
contested/reclaimed border-ore tile, standing next to a still-intact segment
of the *other* team's conveyor grid (which accepts input from 3 sides — see
project rules). The new harvester's output direction lands on that surviving
enemy tile, and the stack then rides the enemy's own belt into the enemy's
own core. It is **border-capture, not sprawl-misroute and not siphon** — a
third category distinct from both the naive hypothesis and the excluded
wild-ladder channel. **Flagged prominently per the task's instruction**,
since it changes the mechanism story for future misroute work: fixing this
requires detecting "my harvester's output tile is enemy-owned," not
"my belt eventually reaches the enemy core."

## B.4 Secondary numbers (context)

- **Lost-in-transit rates**: hsd 2.19% (437/19,923), v76 2.21% (547/24,738) —
  also statistically indistinguishable between bots.
- **Win split, hsd vs v76, 32 games (noisy pairing, context only):** hsd 5,
  v76 27. Not a per-seed comparison and not load-bearing for any misroute
  claim; reported because it was cheap to compute alongside the ledger pass.

## B.5 What this hands back

1. **hsd's misroute channel reproduces** at a much lower pooled rate (~2.3%)
   than the single det game (27%) that flagged it — same mechanism, not the
   same magnitude. The det figure should not be quoted as a per-game-typical
   rate going forward.
2. **v76's `_chain_dead` watchdog shows no measurable misroute reduction**
   against hsd on this corpus (2.24% vs 2.31%, pooled). If the watchdog has a
   real effect, it is below this corpus's noise floor, or it targets a
   different failure mode (harvesters that stop delivering entirely) than
   the one measured here (harvesters that misdeliver to the enemy).
3. **Mechanism correction, worth an issue**: leaked stacks are not "our own
   sprawling belt reaches the enemy core" — they are single-hop handoffs onto
   the *enemy's* still-intact network from harvesters rebuilt on a handful of
   contested border-ore tiles. Any future fix should target output-direction
   sanity at harvester build time (is the output tile enemy-owned?), not
   belt-routing audits of the owner's own network.

---

# Addendum: _v89sh case-metric accounting (kladde-probe corpus, seed-1 noisy, pooled)

> ## CAVEAT HEADER — BINDING
>
> - **NOISE ON, seed 1 only.** Per-game/per-seed pairing is void; this is a
>   pooled-reads-only pass, per the corpus README's own instruction.
> - **Not a paired A/B.** `_v85hsd` and `_v89sh` each played their own 30
>   games against `bots/kladde_probe` (15 maps × both seats) — there is no
>   shared-seed counterfactual between the two tags, only two independent
>   pools vs the same opponent. Differences below are pooled-rate
>   differences, not matched-pair effects.
> - **Fix under test:** `_v89sh` = `_v85hsd` (base) + siphon hygiene
>   (pending-wire queue at harvester build time + deny-adjacent-enemy-
>   conveyor builder behavior). Tape row `_v89sh-acceptance`, **KEEP**.
> - **Tooling**: `scratchpad/ad_flips/{decode,flow}.py` method, extended in
>   `scratchpad/sh_accounting/analyze.py` with (1) per-round harvester wiring
>   state (harvester alive × ≥1 friendly orthogonal conveyor/splitter), (2)
>   per-round adjacency-situation detection (enemy conveyor/splitter, or
>   enemy core footprint, orthogonally adjacent to one of our harvesters),
>   (3) full-hop-path ownership tracking for mechanism classification
>   (adjacency-siphon / handoff / direct-misroute / single-hop-direct, per
>   eir8-doc §8.2's method), (4) deny-arm action detection (our builder
>   `attack` on an enemy belt tile orthogonally adjacent to one of our
>   harvesters).
> - Corpus: `replay_archive/diag_sh_accounting_2026-08-08/` — `_v85hsd` and
>   `_v89sh`, each vs `bots/kladde_probe` (border-contest proxy), all 15
>   maps, seed 1, both seats, `--tle 10`, NOISE ON. 60 games total.
> - Wild ladder baseline for context: **4.33% mined stacks banked by the
>   enemy core** (79.7% of that volume adjacency-siphon), per
>   `eir8-production-read-2026-08-08.md` §8.1–8.2.

## C.1 Validation

`core_deliv × 10 == titaniumCollected`, checked per team-side against the
`fcode` JSON sidecars: **120/120 team-sides exact** (60 games × 2 sides,
30 hsd + 30 sh). No game excluded.

## C.2 Situation census — the adequacy gate

Per the corpus README's pre-stated gate: if zero siphon/border-capture
geometries arose, the case metric is CORPUS-INADEQUATE and routes to a wild
window. **That is not what happened — situations arose on both tags,
census is nonzero, the gate passes, and the case metric below is
reportable.**

| | **hsd** (base) | **sh** (fix) |
|---|---:|---:|
| harvester-rounds (our harvesters, alive, pooled 30 games) | 69,684 | 51,126 |
| (a) harvester-rounds w/ enemy acceptor orthogonally adjacent | **2,014 (2.890%)** | **29 (0.057%)** |
| — of which enemy conveyor/splitter (deny-arm's literal target) | 2,014 (2.890%) | 29 (0.057%) |
| — of which enemy core footprint (not deny-armable) | 0 | 0 |
| (b) distinct harvester-tiles ever in that state | 6 | 3 |
| (c) stacks whose first hop landed directly on an enemy acceptor | 109 | 3 |

**hsd's belt-adjacency situations are concentrated on 6 harvester-tiles
across 30 games; sh's on 3.** Every situation in both pools is
belt-adjacency (conveyor/splitter), zero are core-footprint-adjacency, so
the deny-arm's target class (enemy conveyor next to our harvester) covers
100% of the census in both pools.

A drill-down on the 109 hsd stacks that touched an enemy tile on their
first hop: **93 were nonetheless eventually delivered to our own core, 16
were lost in transit, and zero ended up banked by kladde_probe.**
kladde_probe's own splitter round-robin (team-blind, per the engine rule)
apparently cycles the stack back out rather than routing it home — this
census component measures geometric exposure, not eventual loss, and the
two diverge sharply here.

## C.3 Case metric — enemy-banked stack rate (gate passed, reportable)

| | **hsd** | **sh** |
|---|---:|---:|
| our mined stacks | 11,568 | 9,110 |
| **leaked (banked by kladde_probe)** | **461 (3.99%)** | **3 (0.03%)** |
| kladde_probe mined | 8,269 | 5,650 |
| kladde_probe leaked to us | 331 (4.00%) | 223 (3.95%) |
| lost-in-transit (ours) | 527 (4.56%) | 447 (4.91%) |

hsd's pooled 3.99% sits close to the wild rated baseline (4.33%) — a
useful cross-corpus consistency check. sh's 0.03% is a ~130× reduction.
**Read this pairing carefully before taking it as a clean effect size —
see the concentration flag next.**

**Mechanism classification of the leaked stacks** (own-belt vs enemy-belt
ownership of every hop after the originating harvester emission, per the
eir8-doc §8.2 method):

| mechanism | hsd | sh |
|---|---:|---:|
| ADJACENCY_SIPHON (zero hops on our belt after emission) | 0 (0.0%) | **3 (100.0%)** |
| HANDOFF (our belt partway, then enemy belt) | **461 (100.0%)** | 0 |
| DIRECT_MISROUTE (entirely our own belt into their core) | 0 | 0 |
| SINGLE_HOP_DIRECT (harvester itself adjacent to enemy core) | 0 | 0 |

**Concentration flag, prominent per the corpus's own method precedent
(§8, §B.3 above): hsd's 461 leaked stacks are 95.4% (440) a single game**
(`moonrise_s1_a_hsd`, our harvester at (19,4), 1,000-round tiebreak game).
Excluding that one game, hsd's leak rate over the remaining 29 games is
**21 / 10,308 = 0.20%** — much closer to sh's 0.03% than the pooled 3.99%
headline suggests. sh has no comparable outlier game (max single-game leak
= 3 stacks, in `snowflake_s1_a_sh`, which is also sh's only nonzero
mechanism entry).

**What this means for attributing the fix:** sh's 3 leaked stacks are
100% ADJACENCY_SIPHON — exactly the mechanism the deny-arm targets — and
the census shows the geometry arose 69× less often for sh (29 vs 2,014
belt-adjacent harvester-rounds) than for hsd. That part is a clean,
consistent story. hsd's 461-stack headline, however, is 100% HANDOFF
(mixed own-belt-then-enemy-belt), driven almost entirely by one outlier
game, and is **not** the mechanism sh's specific arms (pending-wire queue,
deny-adjacent-conveyor) were built to fix. The honest pooled case-metric
comparison (3.99% vs 0.03%) is directionally consistent with a real
improvement, but the ex-outlier hsd rate (0.20%) is the fairer baseline for
judging the deny-arm's marginal contribution — against which sh's 0.03%
is still an improvement, just a smaller one (~7×, not ~130×) than the raw
headline implies. **Do not quote 130× or 3.99%→0.03% without this caveat.**

## C.4 Mechanism metric — unwired-harvester-rounds (wire-queue's direct effect)

Always measurable, independent of whether any siphon situation arose.

| | **hsd** | **sh** |
|---|---:|---:|
| harvester-rounds | 69,684 | 51,126 |
| **unwired-harvester-rounds** | **2,236 (3.21%)** | **2,396 (4.69%)** |
| time-to-first-wire: n / mean / median / p90 / max (rounds) | 228 / 2.98 / 2 / 4 / 125 | 200 / 2.85 / 2 / 4 / 113 |
| never-wired harvesters (destroyed or game-ended before any friendly acceptor) | 6 / 234 built (2.6%) | 12 / 212 built (5.7%) |

**The wire-queue arm shows no measurable reduction in unwired time on this
corpus — if anything, sh runs a higher unwired-rounds share and a higher
never-wired-harvester share than hsd.** Median and p90 time-to-first-wire
are statistically indistinguishable (2 / 4 rounds, both tags). This is the
opposite of the arm's stated hypothesis ("pending-wire queue should cut
unwired-rounds") and should be reported as such rather than folded into
the case-metric win. Two readings, neither confirmed here: (1) the queue
targets *which* tile gets wired first rather than *how fast* wiring
happens on average, so this corpus's aggregate rate is the wrong lens; or
(2) the queue's effect is below this corpus's noise floor and the
case-metric improvement above is carried entirely by the deny-arm, not the
wire-queue arm. **Not disambiguated by this corpus — flagged for the
builder, not resolved.**

## C.5 Context (cheap, not load-bearing)

- **Win split** (noisy pairing vs kladde_probe, context only): hsd 25/30,
  sh 25/30. Different loss sets per tag (hsd lost on eider, hive×2,
  jackpot, meander; sh lost on fjordgate, hive, meander×2, moonrise) — the
  identical 25-5 split is coincidental, not a script artifact.
- **Delivery/100r pooled:** hsd us=75.99 vs kladde_probe=56.34; sh
  us=76.22 vs kladde_probe=44.30. Our own delivery rate is flat between
  tags; kladde_probe's delivery rate is lower in the sh pool, plausibly
  just game-length/board-state variance (not paired) rather than an sh
  effect on the opponent's economy.
- **Deny-arm actions observed** (our builder `attack` on an enemy belt
  tile orthogonally adjacent to one of our harvesters): **18 for hsd, 18
  for sh** (identical by coincidence — different games, different maps).
  hsd's 18 are a baseline builder-vs-adjacent-enemy-building behavior
  already present pre-fix; they are not evidence the specific
  deny-adjacent-enemy-conveyor arm is absent from hsd, only that generic
  attack behavior on nearby enemy structures predates it. Consistent with
  the low situation-count on both tags: there simply wasn't much to deny
  either way in this corpus.

## C.6 What this hands back

1. **Gate result: ADEQUATE, not CORPUS-INADEQUATE.** kladde_probe did
   create real (if sparse) adjacency-siphon geometry — 2,014 belt-adjacent
   harvester-rounds for hsd, 29 for sh, all belt-class, zero core-class.
   The case metric is reportable.
2. **Case metric, with the honest caveat carried forward**: pooled headline
   3.99% (hsd) → 0.03% (sh) is real but hsd's number is 95% one outlier
   game's HANDOFF-mechanism leak, not the ADJACENCY_SIPHON pattern sh's
   arms target. Ex-outlier, the fairer comparison is 0.20% → 0.03%
   (~7×), and sh's 3 leaked stacks are 100% the targeted mechanism.
3. **Mechanism metric answer for the wire-queue arm: not confirmed.**
   Unwired-harvester-rounds and never-wired-harvester share are both
   *higher*, not lower, for sh on this corpus. If the queue has a real
   effect, this corpus does not show it — recommend a dedicated
   ablation (sh with wire-queue on vs off, deny-arm held constant) before
   crediting the wire-queue specifically for any of the case-metric gain.
4. **Routing:** the case-metric win here is best attributed to the
   deny-arm (situation count collapsed 69×) rather than the wire-queue arm
   (no measurable change, wrong-signed if anything). Worth a follow-up
   ablation before the `_v89sh` tape credits both arms equally.
