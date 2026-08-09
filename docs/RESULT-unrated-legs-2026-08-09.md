# RESULT — four unrated legs. One plank reads well; one probe of mine is INVALID.

Fired under Magnus's standing grant (*"You're always go for unrated legs"*).
All four on one fixed short-map fixture: nordkap, eider, heart, moonrise,
meander. **20 games, all complete.**

## 1. THE CAD DISCRIMINATOR IS INVALID. MY DESIGN ERROR, NOT A NULL RESULT.

LOKI-QUIET was built to separate *"CAD idles because we DAMAGED them"* from
*"CAD idles because a BODY IS IN THEIR BASE"* — the corpus cannot, because the
two are the same event there.

**Treatment held exactly as specified, verified by decode of the live replays:
0 builder attacks in all five games.** Pre-fire local decode said the same
(0 across 3 maps against a control's 985).

**And it is irrelevant, because the arm still fired 43–315 TURRET SHOTS per game
and destroyed CAD's core in 3 of 5.** `LOKI_QUIET_ON` silences builder melee —
peck, siphon, counterbattery. **The forward SENTINEL was never gated, and a
sentinel firing on their core is the most hostile thing this bot does.**

> **I verified the treatment I CODED, not the treatment the EXPERIMENT REQUIRED.**
> The pre-fire check counted `builderAttack` events and returned a clean 0/985.
> The quantity that mattered was *damage to CAD's core*, which stayed enormous.
> A correct check would have been "enemy core HP never decreases".

**⇒ Nothing in this leg speaks to damage-vs-presence. The question is still
open, and a valid probe must gate the forward sentinel too** (and then almost
certainly cannot win, which is fine — it was never supposed to).

**WHAT THE LEG DOES ESTABLISH, and it is not nothing:** a bot that lands **ZERO
builder attacks** went **3-2 against CtrlAltDefeat with three core kills**
(r157, r82, r235). **Builder melee — pecking, the siphon, counterbattery — is
not load-bearing for us against CAD.** That is worth knowing on its own and I
did not expect it.

**NOT READABLE: the 3-2 vs the attacking arm's 2-3.** The legs drew **opposite
seats** (quiet seat a, attacking seat b). My own PREREG required a shared
fixture and I got maps but not seats. Seat-confounded; not read.

## 2. LOKI-4 ON REAL OPPONENTS — 8-7, and 53.3% CORE-KILL SHARE

| leg | opponent | result | core-kill wins |
| --- | --- | --- | --- |
| `442cd494` | Ouroboros | **3-2** | heart r233, moonrise r181, meander r388 |
| `e4528eeb` | Orizon | **3-2** | eider r115, heart r301, meander r166 |
| `a3459155` | CtrlAltDefeat | 2-3 | eider r118, moonrise r226 |

**PRIMARY CURRENCY: 8 core-kill wins in 15 games = 53.3% `core_kill_share`**,
all seat b, all short maps. **18 of 20 games across all four legs were decided
by `core_destroyed`** rather than tiebreak.

**The Ouroboros cell is the eye-catching one and I am deliberately damping it.**
Our recorded baselines against Ouroboros are **v92 1-4** and **LOKI-2b 1-4**;
this reads **3-2**. Same seat (b) as v92's baseline. **But the map sets differ**
— the baseline ran saga/atoll/lighthouse/eider/nordkap and this ran
nordkap/eider/heart/moonrise/meander, **two maps in common of five**. So it is
**not** a clean before/after, n=5, and the honest word is *suggestive*, not
*improved*. Ladder record against them is 9 core-kill wins in 155 games (5.8%);
three in five would be extraordinary and extraordinary claims at n=5 are how the
C1b "tax" happened.

## 3. WHAT I WOULD DO NEXT, IN ORDER

1. **Re-fire the LOKI-4 legs on the BASELINE map set** (saga, atoll, lighthouse,
   eider, nordkap) so the Ouroboros comparison is a real before/after instead of
   two different experiments. Cheap now that legs are unlimited.
2. **Rebuild the discriminator properly** — gate the forward sentinel as well,
   accept that the arm will lose, and read CAD's build rate in r14-40 off the
   replay rather than our win/loss.
3. **Both arms of any future pair on the same seat**, by firing each twice if
   the platform assigns seats randomly.
