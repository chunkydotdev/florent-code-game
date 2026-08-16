# REPLAY STUDY — OUROBOROS v8 (move-mining candidate)

**PROVENANCE.** Commissioned by the RESEARCH arm (s47, 2026-08-16) after
`tools/move_miner.py` fired Ouroboros v8 as its top candidate (155 unstudied of
155 on that version, all-time share 18.8%, n=160). Run by a fresh **opus**
subagent, read-only over `corpus/` + `replay_archive/` + the bot trees.
Governed by `docs/research/PLAYBOOK-move-mining-2026-08-16.md`.

**GROUND.** 110 rated replays vs Ouroboros in `corpus/join.tsv` (all `oppver=8`),
plus **1,281 archived Ouroboros games vs 31 teams** in `meta_join`. Our side
spans `ourver` **v65–v102 only**. Incumbent/control `bots/_v223sealrepair` =
platform **v140**; live holder v152/v153 at time of study.

⛔ **ERA DISCIPLINE.** Every *"what WE do"* claim is bound to `ourver` v65–v102 and
is **NOT** a claim about the incumbent. Every *"what THEY do"* claim is current:
**v8 has been their unchanged incumbent for 10 days.** Per the self-claim rule
established the same session (see `QUEUE.md` `#85`): a self-claim whose span
crosses more than one incumbent is presumed stale until split.

**RESEARCH-ARM VERIFICATION.** The code claims below were re-verified by hand in
the lane against `_v223sealrepair`, `ZZQXNOTATOKEN` control 0/0. **One flag in
the agent's report was wrong and is corrected in §6.**

---

## 0. ⛔ THE HEADLINE NUMBER IS STALE AND MUST NOT BE QUOTED AS CURRENT

**18.8% (30/160 rated) is real but is dominated by our v53–v86 era (130 of 160 games).**

| era | rated games | our game share | 95% CI (DEFF 1.529) |
|---|---|---|---|
| v53–v86 | 130 | **14.6%** | [8.6, 23.6] |
| v90–v102 | 25 | **36.0%** | [17.6, 59.8] |
| all | 160 | 18.8% | [12.4, 27.3] |

**The intervals overlap — no improvement is established, but neither is 18.8% a
current estimate.** Last match 2026-08-10 (v102): 4/5, all five core-kills; n=1.

⭐ **THE ROBUST FORM, which needs no era split: S−E = −0.294, 95% CI
[−0.364, −0.225] over 32 rated matches — excludes zero decisively**
(match-level, no DEFF needed). ≈ **−9.4 Elo per match** at prevailing ratings.

⚠ **RE-ENCOUNTER PRICE.** They are **live** (1,762 league matches, last seen
2026-08-16T15:32 — the same minute as every other active team) and pair every
20 minutes; they are **dormant against us, not gone**. At ~1761 vs their 1478,
E = 0.836 ⇒ **a pairing pays −20.7 Elo at the historical share, −15.2 even at
the v90–102 share.**

---

## 1. ⭐⭐⭐ MEASURED ZERO — OUROBOROS BUILDS ONLY GUNNERS

**29,543 gunners · 0 sentinels · 0 launchers · 0 barriers · 0 splitters, across
1,281 archived games vs 31 teams.** Every game, no exceptions.
**A MEASURED zero, not a not-measurable one: the same decoder reads nonzero
sentinels/launchers/barriers for their opponents in the same files.**
Per game: 23.1 gunners, 46.8 conveyors, 8.9 harvesters, 8.1 core spawns.

**Consequences, all structural:**
* A gunner's shot is **obstacle-blocked**; the sentinel's **pierces**. ⇒ **100% of
  their turret stock is pluggable** — they are the maximal-value target for
  `#84`, and the **only** team in the corpus where the sentinel escape hatch
  does not exist.
* **They can never plug us back — 0 barriers in 1,281 games** ⇒ `#83`'s defensive
  hazard is **inert** in this fixture and a leg reads the offensive half clean.
* **Kidnap/launcher counters are irrelevant** (0 launchers), and **`#79`'s
  plant-and-guard infiltrator does not work on them** (23 gunners/game).

**Their opening is a HOME GUNNER RING, then a creep.** Median gunner distance
from **their own** core by band: **4.1 → 6.1 → 9.5 → 11.2 → 8.1** (r0-50 /
50-100 / 100-200 / 200-300 / 300+). At r0-50, **77.3% of their gunners sit
within d²≤26 of their own core** vs the version-matched field's 49.0%; only
**27.5% are in our half** vs the field's 54.6%. Median first gunner r20.

**They REVERTED.** v8 first seen 2026-08-01; they ran v30–v33 on 08-04→08-06 and
**went back to v8**, now 1,392 matches unchanged. **Their own testing said v8 was
better.** A stable, deliberately chosen bot — not a moving target.

---

## 2. ⭐⭐⭐ HOW WE LOSE — AND IT IS A **CONVERSION** FAILURE, NOT A SPEED FAILURE

Version-matched field = 1,445 games, `ourver` 65–102, 31 opponents.

| | vs Ouroboros (n=110) | matched field (n=1,445) |
|---|---|---|
| we kill their core | **8.2%** | 37.4% |
| **timely kill (≤ r300)** — programme primary | **6.4%** | **31.1%** |
| our core dies | 47.3% | 39.0% |
| reaches r1000 | **44.5%** | 23.6% |
| **median round we kill** | **155** | **155** |
| median round we die | 370 | 235 |

⭐⭐ **WHEN WE KILL THEM WE KILL AT r155 — IDENTICAL TO THE FIELD MEDIAN. The kill
machine is not slowed by this opponent; it runs at full speed in 8.2% of games
and NEVER STARTS in the other 92%.** ⇒ every plank here re-aims from *"kill
faster"* to **"get the raid to arrive at all."**

**The shredder, per 100 rounds alive (removes the length confound — their games
run median 686 turns vs the field's 203):**

| r100–300 | vs Ouroboros | matched field |
|---|---|---|
| our conveyor deaths | **11.7 / 12.2** | 2.4 / 3.0 |
| our builder deaths | **5.0 / 4.7** | 1.2 / 1.5 |
| our core spawns (replacements) | **4.9 / 4.2** | 1.6 / 1.7 |

**≥98% of that destruction is TURRET FIRE, not melee: 648.6 enemy shots/game
against 10.5 enemy builder attacks/game.**

**Their shooting escalates while ours collapses** (shots per 100 rounds alive;
length control = field games ≥600 turns, n=431):

| band | US vs Ouro | US vs long field | THEM | THEM long field |
|---|---|---|---|---|
| r0-150 | 12.71 | 23.13 | 67.62 | 37.85 |
| r150-200 | 8.29 | 23.81 | **110.05** | 40.60 |
| r200-300 | 7.65 | 20.01 | **121.51** | 42.79 |
| r300+ | **1.81** | 14.38 | **101.79** | 45.96 |

⭐ **AND IT IS NOT POVERTY — IT IS SILENCE. At r300+ we hold a median 1,256 Ti and
24 ammo, converting 26.9 ammo/100r, against the long-field control's 2,845 Ti,
53 ammo and 158.7/100r.** We are rich, banked, and not shooting.

---

## 3. ⭐⭐ THE GENERALISING MECHANISM — GUNNER SHOTS EAT BELT, SENTINEL SHOTS DO NOT

This matters because **the `Controller` exposes no opponent identity** — a plank
saying *"do X against Ouroboros"* is unbuildable. **This one is unconditional.**

Our conveyor deaths per 100r rise monotonically with enemy shot rate across all
1,126 matched games ≥150 turns: **0.55 → 1.54 → 2.08 → 3.17 → 5.71** as enemy
shots/100r go 0-10 → 10-25 → 25-50 → 50-100 → 100-200.

Splitting enemy fire by turret type (games with ≥40 enemy shots, ≥90% one type):

| enemy fire | games | our conveyor deaths **per 1,000 enemy shots** |
|---|---|---|
| gunner-pure, excl. Ouroboros | 610 | **44.4** |
| **sentinel-pure** | 193 | **21.4** ← control, runs the other way |
| **Ouroboros** | 109 | **83.3** |

⭐ **A sentinel does 18 dmg to a conveyor's 20 HP (2 shots) and a gunner 7
(3 shots) — so PER SHOT the sentinel *should* be the better belt-killer, and it
measures at HALF. That is a TARGETING fact, not a damage fact:** the piercing
long-range turret is pointed at turrets and cores; the blocked short-range one
hits whatever is **first in its line**, and first in line is belt.

**Ouroboros sits at 83.3 belt-kills per 1,000 gunner shots = one conveyor per
4 shots against a 3-shot theoretical floor — ~75% of maximum possible
efficiency. Their gunners essentially never waste a shot.**

---

## 4. ⭐⭐ WHAT **WE** DO WRONG — WE RELAY THE SAME TILE INTO THE SAME GUN

Share of **our** conveyor builds landing on a tile where one of ours already died
in that game:

| population | r<200 | r<300 | whole game | median max-repeat | max |
|---|---|---|---|---|---|
| **vs Ouroboros** (110) | **7.5%** | **11.9%** | **26.3%** | 4 | **32** |
| long matched field ≥400t (539) | 3.5% | 5.3% | 12.8% | 2 | 49 |
| short matched field (889) | — | — | 1.1% (≥3×) | 1 | 10 |

✅ **CONTROLS RUN THE OTHER WAY, which is what makes this belt-specific rather
than "everything churns": at r<300 our HARVESTER rebuild rate is 5.0% vs the
long-field 6.4%, and our SENTINEL rebuild rate 9.9% vs 12.0% — both BELOW field.
Only the belt is above, and by 2×.** Their own conveyor rebuild rate against us
is 9.9%.

**23.7% of our conveyor builds against them go onto a tile we build ≥3 times in
the same game; 14.5% onto tiles built ≥5 times.** ⭐ **The titanium is trivial
(~3 Ti × scale). THE COST IS THE BUILDER TURN AND THE BUILDER BODY — the relay
requires standing orthogonally adjacent to the tile, i.e. INSIDE the gunner cone
that just cleared it, and we lose 4.7–5.0 builders per 100 rounds there.**

⛔ **AND THE INCUMBENT'S REPAIR PATH IS STATELESS *BY EXPLICIT DESIGN*, WITH A
NAMED REASON — verified in the lane.** `eco.py:626 _l4_repair`,
`LOKI_L4_REPAIR_ON = True` (`doctrine.py:1674`), `LOKI_L4_OWN_HALF_ONLY = True`
(`:1681`). Docstring **verbatim**:

> *"THE RULE, and it is stateless on purpose — no remembered map, no store slot,
> nothing to go stale **when a launcher throws this body across the map**."*

⇒ **the reason for statelessness is LAUNCHER DISPLACEMENT, and any memory added
here inherits exactly that exposure.** ⚠ **Bounded elsewhere in the same session:
our builders are thrown in ~0.2% of post-build actions, so the exposure is small
— but it is an ACCEPTED cost, not an unknown one.**
⚠ **And the one spatial guard does not bind on this matchup by construction:
every shredded tile is in our own half** (our conveyor deaths sit at median
d=5.8 from **our** core vs 10.8 from theirs; 77.2% closer to ours).

---

## 5. THE AMMO COUPLING — OUR AMMO TARGET IS KEYED TO OUR OWN TURRET COUNT

`main.py:234-236`, verified in the lane:
```
ammo_target = 24 if under else AMMO_FLOOR        # AMMO_FLOOR = 16
if weapons: ammo_target = max(ammo_target, min(48, 4 * weapons))
```
where `weapons = home_guns + fwd_guns` — **our own live turret count.** Once
`ammo >= ammo_target`, conversion stops entirely.

Measured `ammo_end` against Ouroboros is **exactly 24 in every band, every era**,
while the bank runs to 1,256 Ti and the `ti_floor` gate is 12–52. **The observed
value is the POLICY'S FLOOR, not a resource limit.**

⇒ **An opponent who suppresses our turret line therefore also throttles our
ammunition: few turrets → low ammo target → no shooting → belt dies → no
titanium converted → no turrets.** A closed loop with no exit.

⚠ **The CODE is v140; the EFFECT is measured on v65–102. The coincidence of
`ammo_end = 24` with an `AMMO_FLOOR`-class target is suggestive, not proof the
same rule was live then.**

---

## 6. ⚠ CORRECTION TO THE AGENT'S REPORT — MADE IN THE LANE

The report flags `ENDGAME_SWITCH_ON` / `SPORKS_AMMO_ON` as *"currently False,
`doctrine.py:1056`"* and suggests the ammo row may already be answered.
**Only `SPORKS_AMMO_ON` is False. `ENDGAME_SWITCH_ON = True` (`doctrine.py:854`).**

⭐ **BUT THE ROW SURVIVES, AND FOR A BETTER REASON THAN THE AGENT GAVE:
`ENDGAME_RND = 960`.** The switch fires only in the **last 40 rounds of a
1000-round game**, and its own comment describes it as a capped tiebreak-era
ammo **dump**. ⇒ **it cannot touch the r300 window the finding is about — 660
rounds earlier.**
⛔ **AND THE SHARPER READING: under `R1000_IS_DEFEAT`, an ammo mechanism that only
fires at r960 sits entirely on the RETIRED currency, while the r300 window —
where `DEFENCE_ADMISSION_BAR` actually binds — has NO round-conditioned ammo
response at all.** Our only such behaviour is in the era the programme gave up on.

---

## NOT FINDINGS — recorded so nobody re-derives them

1. **CPU-timeout induction is not supported here, and is norms-blocked anyway.**
   Ouroboros discards **2.83%** of unit-turns against us but **2.06%** pooled
   across all 1,281 archived games, and **higher against OopsGotYourElo (5.22%)
   and Torsko (3.41%) than against us**. **No us-specific effect.** Timeout
   induction remains HELD pending the organisers' answer; do not merge
   measurement with induction.
2. **"Teams that beat Ouroboros build gunners" — REFUTED as actionable.** The
   pooled table (rated+unrated, **not** a win-rate denominator) shows SmartFridge
   14-1 with 11.0 gunners and Kings College Munich 40-7 with 12.6, against
   Memtrace 13-94 with 2.2 — **but Atlas (1.7 gunners) sits at 22-25 and
   Banminary (2.6) at 15-14.** The trend is not clean and gunner count is
   confounded with winning (a winning team lives longer and builds more).
   **Do not build a gunner plank off this table.**
3. **Length inflation is real and was removed everywhere.** Raw per-game figures
   (54 conveyor deaths, 24 builder deaths, 94.9 conveyors built) are **not**
   admissible without per-100-round normalisation or a matched-length control.
4. **Their builder melee is not the mechanism** — 10.5 attacks/game against our
   137, refuted with the shot count as the alternative.

---

## COULD NOT DETERMINE — stated as not-measurable, never as zero

* **Whether the barrier plug works on them.** Turret **facing** is absent from
  `events.tsv`/`builds.tsv`; establishing which gunners are pluggable needs a
  fresh direction decode. **This is `#84`'s remaining gate.**
* **Whether the matchup is still bad.** Zero rated games since 2026-08-10; our
  bot went v102 → v152 and gained `_l4_repair` (which §4 argues cuts the wrong
  way here); their bot is unchanged. **The v90–102 CI [17.6, 59.8] contains both
  "fixed" and "unchanged". Only a leg answers it.**
* **Whether their gunner target selection is belt-first by design or emergent**
  from the obstacle-blocked ray. Inferred from the 4-shots-per-kill efficiency;
  their targeting was not read.
* **Why our sentinel placement flips backward against them** (30.6% forward vs
  43.0% field, n=242 — thin).

---

## ROWS ADMITTED FROM THIS STUDY

* **`#88`** — belt-repair attrition memory (new row).
* **`#69`** — **NARROWED**: second in-band instance supplied, but the spawn-ring
  half **refuted as necessary** — re-scoped to belt attrition with the ring as
  aggravator.
* **`#84`** — maximal-value target and built-in control; facing-decode
  precondition remains the gate.
* **Ammo coupling** — admitted after the `ENDGAME_RND = 960` read above.
