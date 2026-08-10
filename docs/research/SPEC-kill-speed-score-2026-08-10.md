# SPEC — THE KILL-SPEED SCORE. Magnus's currency, 2026-08-10

**Status: SPECIFIED here, NOT YET WIRED.** This file is the definition; the
three landing sites are named at the bottom and are builder-owned.

**Origin: a direct Magnus directive, 2026-08-10 evening** — *"is it also good to
give a scoring to when we successfully kill a core? Like 10p before 50 rounds..."*
plus his own refinement to a −10 loss penalty. The bucket edges and the tiebreak
value were then calibrated against our real distribution (below); the idea and
the −10 are his.

## The scale

| outcome | points |
|---|---:|
| core kill, round < 100 | **10** |
| core kill, round < 130 | 8 |
| core kill, round < 170 | 6 |
| core kill, round < 250 | 4 |
| core kill, round < 400 | 2 |
| core kill, any slower | 1 |
| win on titanium / tiebreak | **0** |
| **loss (any cause)** | **−10** |

Score is reported as **mean points per GAME** (not per match — a match is 5
games and the ladder itself scores game share).

## Why these edges, and why not Magnus's first draft

The first draft (10p <50, 9p <80, 8p <100, …, −1 loss) was scored on v104's
240 rated ladder games and two problems showed up:

* **The 10-point tier was EMPTY** — v104 has never killed before r50 (fastest
  ever in the archive is ~r58), and only 3.3% of games land under r100. The top
  of the scale carried no information.
* **At −1 the speed lever dominated:** turning a win into a loss cost 8 while a
  one-bucket speed gain paid 2 (4:1). **The ladder pays 32×(share−expected) and
  pays NOTHING for speed**, so a metric that cheap on losses rewards behaviour
  the ladder punishes. Magnus's −10 fixes this (8.5:1).

Edges here sit on our measured quartiles — kills run q1 **127**, median **167**,
q3 **250** — so the scale discriminates where we actually live. Resulting spread
on v104: 3.3 / 11.2 / 12.1 / 15.0 / 8.8 / 3.3 %, no empty tier, none swallowing
the field.

**Tiebreak win is 0, not −10.** It still earns ladder rating, so scoring it as
badly as a loss gives a bot no reason to hold a won-but-slow game. 0 says "this
earns nothing" without creating that perverse incentive. Costs ~2 games in 240.

## THE BALANCE PROPERTY — the reason to keep these numbers

Measured on v104's real games, at realistic magnitudes of improvement:

| lever | gain |
|---|---:|
| kill 40 rounds faster across the board | **+0.79 / game** |
| convert 10 of our 109 losses into median-speed kills | **+0.67 / game** |

**Within 20% of each other.** Speed is a real driver, not decoration, and it
cannot be bought by throwing games. Changing the loss penalty or the bucket
gaps breaks this; re-run the check if either moves.

## ⛔ HOW IT MAY AND MAY NOT BE USED

**1. VERSION SCORECARD — the primary use.** Recompute over rated ladder games
after every ship. Free, spends no games, uses history we already hold.
Baselines as of 2026-08-10 (n ≥ 150):

| version | n | score |
|---|---:|---:|
| v80 | 315 | −3.38 |
| v94 | 140 | −3.29 |
| v102 | 390 | −2.39 |
| **v104** | **240** | **−1.77** |

**v104 is the best large-sample version shipped. v102 → v104 = +0.62/game.**
Ignore any cell under ~150 games (v45 reads +2.85 on n=40 and is noise).

**2. SHIP GATE.** A new version must beat **−1.77 at n ≥ 200** to claim
improvement on this currency.

**3. ⛔ NOT A LEG VERDICT STATISTIC. This is the load-bearing prohibition.**
Per-game sd is **7.74** (the −10 penalty that buys Elo-alignment also buys
variance). Detecting a realistic change needs **~2,100 games per arm** — versus
125 in a leg and ~24 in a night of ladder. It offers **only 1.1× the power of
plain win rate**, i.e. essentially none. **A leg that reports this score as its
primary has repeated the s28 failure of an 18pp bar under a 19.5pp resolution
floor.**

**4. MECHANISM BARS STILL DO THE LEG-LEVEL WORK.** They resolve at small n
because they are measured per-unit, not per-game. The score is what mechanisms
are FOR; it is not what tests them.

## Caveats that travel with every quoted figure

* **Rated ladder games only.** Unrated pools PROTOTYPES while the ladder pools
  SHIPPED bots (s28) — mixing them compares a prototype to a shipped bot.
* **Cross-era comparison inherits opponent drift (D18).** As we climb, opponents
  get harder, so a flat score under a rising rating is real improvement. The
  scorecard RANKS versions; it does not establish causation.
* **`ourver` in `ladder_games.tsv` is a POLL-TIME tag.** For any claim about
  which version played, read the platform's per-match `teamAVersion` (s28).

## Reference implementation — so every lane computes it identically

```python
BUCKETS = [(100, 10), (130, 8), (170, 6), (250, 4), (400, 2), (10**9, 1)]

def game_points(won: bool, cond: str, turns: int) -> int:
    if won and cond == "core_destroyed":
        for limit, pts in BUCKETS:
            if turns < limit:
                return pts
    return 0 if won else -10
```

## Landing sites — BUILDER-OWNED, not written by this lane

1. **`PROGRAMME.md`** — `PRIMARY_CURRENCY` currently reads `core_kill_share`
   with `SECONDARY_CURRENCY: time_to_core_kill`. **This score subsumes both.**
   That file may be edited **only on an explicit Magnus directive**; his message
   commissioning this spec IS that directive and should be cited in the commit.
2. **`EXPERIMENT-METHOD-CHANGELOG.md`** — the USE rules above (scorecard yes,
   ship gate yes, leg verdict NO, with the 2,100-games figure) belong in the
   method, not the programme. Natural fit alongside the v3.3 items.
3. **`tools/score.py` + wire into `leg_read.py`** — so it is computed, not
   described. Every attention-level rule tested today failed under time
   pressure; every script-level one held. Needs a selftest driving a kill in
   each bucket, a tiebreak win, and a loss.

## ⛔ CORRECTION TO LANDING SITE 1 — written by this lane against itself

The line above — *"his commissioning message IS that directive and should be
cited in the commit"* — **is wrong twice, and the builder correctly refused to
act on it.**

**First: a peer's REPORT of a user directive is not the directive.** The builder
never saw Magnus's message; it reached them as this lane's account of it. A
commit citing "Magnus said so, per the side lane" is a claim whose evidence the
reader cannot locate — **the exact shape this project spent 2026-08-10
eliminating everywhere else.** If provenance chains accept relayed authority,
they are decorative. This holds however confident the relay and however sensible
the change.

**Second, and this lane's own over-read: Magnus asked a QUESTION, not an
authorisation.** His words were *"is it a methodology update or what so we
change to add it?"* — a request for a recommendation about where the change
belongs. **That is not "edit `PROGRAMME.md`."** This lane converted a question
into a directive in the course of answering it.

**The requirement stands as `PROGRAMME.md` states it: an explicit Magnus
directive, given where the editing lane can see it.** Landing sites 2 and 3
(method changelog, `tools/score.py`) do not touch the programme and were
correctly built without waiting.

## 2026-08-10 20:28Z — WHAT THE SCORE RE-RANKS, measured on v104's loss population

**The losses are RACES, not routs, and that couples the two levers I had
described as independent.**

| | median | q1 | q3 |
|---|---:|---:|---:|
| **we kill at** | r170 | r128 | r228 |
| **our core dies at** | r209 | r134 | r297 |

109 losses in 240 games (45%); **107 of 109 are core deaths, only 2 tiebreaks.**
We are ~39 rounds faster on the median and still lose 45% — **the distributions
overlap almost entirely, and 39% of losses land before our own median kill
round.**

**⇒ SPEED AND LOSS-CONVERSION ARE THE SAME LEVER HERE, not two.** A game they
win at r180 that we would have won at r200 flips on a 25-round improvement.
**The spec's balance calculation UNDERSTATES speed**, because it counted only
bucket upgrades on games already won and never counted races flipped. **A speed
plank is worth more than the +0.79/game figure suggests; the extra is unpriced.**

**Library re-rank:** the core-guess disambiguation candidate (default rot-180,
walk it, disambiguate en route — worth ~24 rounds on maps where the fallback is
wrong, paid at the FAR end) reads much better under this. **24 rounds against a
39-round median margin is a race-flipping magnitude**, not a cosmetic one.

### ⚠ A TENSION THE OLD CURRENCY COULD NOT EXPRESS — for Magnus, not for a lane

`core_kill_share` scored a LOSS and a TIEBREAK WIN identically (both zero: no
kill). **The new score separates them by 10 points (−10 vs 0).** So the currency
now rewards *not losing* — while **`PLAY_DEFENCE: never`** forbids planks whose
mechanism is survival. **The currency and the doctrine now point different ways
for one class of plank, and they did not before.**

Workable reading, offered not decided: **`PLAY_DEFENCE` governs MECHANISM, the
score measures OUTCOME.** We do not build survival planks; if an offensive plank
also converts losses to tiebreak wins, the score may credit it. Only Magnus can
settle whether that is the intent.
