# Cut B(1): DODGE is priced. Persistence is dead. The facing ray is worth 5.9× the radius.

**Research arm, session 24, 2026-08-09.** The builder's Cut B(1), asked for twice and
deferred twice, run after **v92 shipped PLANK DODGE** — so it prices a live plank rather
than a proposal.

**Version tag:** live **v92** = `bots/_v115dodge`, submission `7b1d8d73`, treehash
`37450121`; rollback control v91 `bots/_v100hf` / `9850f196`.
**Corpus only, zero replay downloads.** Decoder:
`docs/research/scripts/side-lane-2026-08-09/dwell_decode.py` — `dc_decode.py` plus six
documented additions — **1,355 files, 0 errors, 12 s.**

---

## 0. Validation, because every number below rests on a reconstructed envelope

The envelope is reconstructed three ways — **exact line-of-fire** (facing + r² +
blocking), **ray** (facing + r², blocking ignored — *this is the one v92 ships*, see
§4), and **radius** (an upper bound). None is a proxy for the shipped rule; the shipped
rule is one of them. The reconstruction is checkable and was checked:

| check | result |
| --- | --- |
| `fireTurret` target tile lands on the reconstructed ray — **gunner** | **368,134 / 368,167 = 99.991%** |
| same — **sentinel** | **117,758 / 117,758 = 100.000%** |
| death classification vs `dc_decode.py`, keyed on (file, bid, round) | 10,015 rows, **0 killer-label mismatches** |

**485,925 real shots.** The 33 gunner misses are the S1 ordering trap (a blocker removed
earlier in the same round). The 481 extra death rows over my earlier `dc_deaths.tsv`
run are 20 files archived since — **reconciled exactly, nothing unexplained.**

**Population:** 10,496 US builder deaths → 10,370 by an enemy turret → **9,495 usable**
(exactly one distinct enemy turret fired at the victim that round, so "the killer" is
unambiguous). 875 multi-shooter deaths are **excluded, not guessed**; if they skew, it
is toward *longer* dwell, so what follows is conservative. **Dwell walks back by turret
ENTITY ID**, so the 158-rebuilds-on-one-tile case cannot contaminate it.

---

## 1. PERSISTENCE IS DEAD, and by a wider margin than my 3.1% estimate

**97.6% of all pre-death exposure — 28,473 of 29,161 dwell-rounds — had the killer
turret inside the victim's own r²≤20 vision at the moment of exposure.** Only **2.4%**
required memory of a turret that was not visible, and **every one of them is a
sentinel.**

| killer | deaths | dwell-rounds | in vision | **blind** |
| --- | ---: | ---: | ---: | ---: |
| gunner | 8,284 | 25,589 | **25,589 (100.0%)** | **0** |
| sentinel | 1,211 | 3,572 | 2,884 (80.7%) | 688 (19.3%) |
| **pooled** | **9,495** | **29,161** | **28,473 (97.6%)** | **688 (2.4%)** |

The gunner 100% is forced by geometry (envelope d²≤13 < vision d²≤20) and **it validated
at n=25,589 dwell-rounds**, which is the second independent confirmation that the
pipeline is sound.

**And the death-level number is smaller still than it looks.** 293 of 9,495 deaths
(3.1%) contain any blind dwell round — all sentinel, 0 of 8,284 gunner deaths. Of those
293:

* **157 (53.6%)** had the killer inside that same victim's vision at some **earlier**
  round — own-bot persistence would reach these.
* **136 (46.4%) never saw the killer at all** — these need **team-shared state**, not
  persistence.

**So own-bot persistence's true ceiling is 157 / 9,495 = 1.65% of our turret deaths.**
I argued for persistence this morning at "3.1%, don't build it". The measured figure is
**half that again.** The argument is closed.

## 2. THE AVOIDANCE WINDOW IS ONE ROUND — and it corroborates a geometric prediction

**57.7% of all dwell-rounds are rounds the victim was already being shot** by that same
turret. The p90 dwell of 6 is the **damage clock**, not a loiter tail — a gunner does
7/round into 40 HP = 6 rounds, and healing is essentially absent (**99.7% of deaths take
zero heal rounds**). The genuinely free window, before the killer's first shot:

| killer | n | silent rounds = 0 | = 1 | ≥ 2 |
| --- | ---: | ---: | ---: | ---: |
| gunner | 8,284 | 26.9% | **69.4%** | 3.7% |
| sentinel | 1,211 | 32.3% | 53.8% | 13.9% |

**72.4% of deaths (6,874/9,495) had at least one silent round in the envelope — and
almost always exactly one.**

> **This is the same answer as the geometry, arrived at independently.** Vision r²=20 is
> 4.47 tiles; a gunner's envelope r²=13 is 3.61 tiles; **the margin is 0.87 of a tile**,
> which predicts *one step of warning*. The empirical silent window is **one round**.
> **Two unrelated measurements — a radius subtraction and a per-round dwell census —
> agree.** DODGE is a one-round-reaction mechanism by construction, not by tuning.

## 3. THE DWELL-0 FLOOR IS ~1%, NOT 12.7% — and that surprised me

Pooled dwell-0 is **12.7%** (1,209/9,495). The obvious reading is "unpreventable". **It
is wrong.**

* **0.0% were a turret built onto a standing bot.** The youngest killer at a dwell-0
  kill is 1 round old — a turret cannot fire the round it is built.
* **Gunner: 901/993 (90.7%) the victim MOVED into the line that round.** Sentinel:
  216/216 (**100.0%**).
* **95.9% of gunner dwell-0 victims (952/993) were already inside the killer's radius at
  r−1**, just off the firing line.
* The remaining **92 gunner cases stood still — and all 92 were already on the ray at
  r−1, blocked by something that then disappeared.**

**That last class is the only genuinely unpreventable one I can find: 92 / 9,495 =
0.97%.** Everything else in dwell-0 is a bot stepping into a line it could already see.

## 4. THE CONTROL — and it is the single most decision-relevant table of the day

Over **4,197,492 US builder-rounds** (every live builder, every round, 1,355 files):

| envelope rule | builder-rounds in envelope | P(die next round \| in) | P(die \| not in) | hazard | share of all deaths preceded by an in-envelope round |
| --- | ---: | ---: | ---: | ---: | ---: |
| LINE (exact — blocking respected) | 174,850 (**4.17%**) | **5.37%** | 0.028% | **195×** | **89.4%** |
| **RAY (facing, blocking IGNORED) — what v92 actually ships** | 248,966 (**5.93%**) | 3.84% | — | — | **91.1%** |
| **RADIUS (facing ignored — upper bound)** | 1,468,307 (**34.98%**) | 0.71% | — | — | 99.3% |

> **CORRECTION, same day, on the builder arm's catch: I MISLABELLED WHICH ROW IS THE
> SHIPPED ONE.** I wrote *"LINE (exact — what v92 ships)"*. **v92 ships RAY.**
> `_danger_tiles()` calls `ct.get_attackable_tiles_from(...)`, and I verified that
> method's docstring against the installed engine
> (`.venv/lib/python3.13/site-packages/fcode/_types.py:693-696`) rather than taking the
> correction on trust — it reads, verbatim: *"Return all in-bounds tiles in a
> hypothetical turret's raw attack pattern. This ignores ammo, cooldown, occupancy, and
> other target-specific legality checks. **For gunners this includes the full firing
> line within range, even behind walls.**"* **Raw pattern, blocking ignored — that is
> the RAY row.**
>
> **So the live figures are 5.93% of builder-time forbidden for 91.1% coverage**, not
> 4.17% / 89.4%. v92 sits on the middle option: **1.76pp more blocked builder-time than
> exact LINE, buying 1.7pp more coverage** — slightly conservative, roughly a wash, and
> moving to exact LINE would cost one `can_fire_from` call **per tile** instead of one
> call **per turret**, which is a real CPU multiplier for a 1.7pp trade.
>
> **AND THE HEADLINE MULTIPLIER MOVES WITH IT.** The "8×" below was computed against
> LINE (34.98 / 4.17 = 8.39×). **Against the row v92 actually ships it is
> 34.98 / 5.93 = 5.90×, for 8.2pp of coverage** (99.3% − 91.1%). **The design
> conclusion is unchanged and the number is smaller; use 5.9×.**

**In-envelope is rare and it is lethal: 5.93% of builder-time under the shipped ray
rule (4.17% under exact line), carrying a 195× hazard ratio, and 91.1% of all our
builder deaths have an in-envelope round immediately before them.** It clears the bar the loiter trigger failed — exposure runs are short (60,981
maximal runs, median length 1, **66.7% exactly one round**) and **84.6% end without the
bot dying**, so builders do sit in envelopes and usually survive; the exposure is brief
and infrequent, not ambient.

> **THE RADIUS ROW IS THE TAX WARNING, AND IT SETTLES A DESIGN QUESTION.** A
> radius-based rule forbids **35% of all builder-rounds** to catch 99.3% of deaths. The
> rule v92 ships forbids **5.9%** and still catches **91.1%**. **A 5.9× difference in
> blocked map-time for 8.2pp of coverage.** (Against the exact-LINE variant it would be
> 8.4× for 9.9pp — but that is not the shipped rule; see the correction above.)
>
> This is the measured version of what tactics sweep 9 predicted from BC2020 —
> *"a disc rule is likely fatal here; the facing-line rule may not be"* — and of my own
> plant-coverage finding that the home band **is** our conveyor network. **BC2020's
> winner blanked a radius because their net gun was omnidirectional. Ours are facing
> turrets. Copying the disc would have been the expensive mistake, and v92 did not make
> it.**

## 5. What this hands back

1. **Do not build persistence.** Own-bot memory reaches **1.65%** of turret deaths;
   nearly half of the blind cases need team-shared state instead. **My own argument for
   it is withdrawn on the measurement.**
2. **v92's facing-ray envelope is the right design and now has a number behind it** —
   **5.9× less blocked map-time than the radius alternative for 8.2pp less coverage.**
   (It is the *ray*, not the exact line — blocking is ignored. See §4's correction.)
3. **DODGE is a one-round-reaction mechanism.** Confirmed twice, independently. Any
   future tuning that assumes more warning is available is assuming something false.
4. **The hard floor on pathing avoidance is ~1%**, not the 12.7% dwell-0 share. **The
   headroom above v92 is much larger than the naive read**, because 90.7% of dwell-0
   deaths are the bot moving into a visible line.
5. **The remaining question this cannot answer** is what fraction of that headroom v92
   actually captures — that needs its battery's own instrumentation, not the corpus.

## 6. Limits and approximations, each stated where it bites

* **No approximation on the envelope.** Validated at 99.991% / 100.000% against 485,925
  shots. The radius variant is **labelled an upper bound everywhere it appears** and is
  never the headline.
* **Timing convention, a real choice:** envelope membership is evaluated at **END of
  round** against the end-of-round board. Shots resolve intra-round, so a bot that
  entered and left a line within one round is not counted. **This makes dwell a mild
  UNDER-count.**
* **875 multi-shooter deaths (8.4%) excluded**, not guessed.
* **210 of 9,495 deaths (2.2%) have no resolvable decision round** (first tracked round,
  or thrown) and are excluded from the entry-visibility figures only.
* **Vision is treated as pure radius d²≤20, unblocked.** No evidence the engine blocks
  vision, but **it was not verified**.
* **"Needs memory" ≠ "memory would help"** — 136 of the 293 blind-round deaths never had
  the killer in that victim's vision at any point.
* **The field side was not measured** (their builders vs our turrets). Everything here
  is US builders vs enemy turrets, ladder games only — **field data, no self-play
  caveat.**
* **The NW-corner `d2` contamination affects HOME/FWD labelling only.** The whole dwell
  table was re-run under `band_fp` (nearest footprint tile): 5,434 HOME / 4,061 FWD,
  median 2, dwell-0 12.3% / 13.3% — **nothing moved.**

## Provenance

`docs/research/scripts/side-lane-2026-08-09/dwell_decode.py`, committed. Outputs:
`dwell_deaths.tsv` 10,496 rows · `dwell_expo.tsv` 6,438 · `dwell_runs.tsv` 10,146 ·
`dwell_val.tsv` 1,355. Death classification, the S1 ordering trap, the two's-complement
HP varint and the band definitions are verbatim from `dc_decode.py`, which is why it
reproduces it at **0 mismatches**.
