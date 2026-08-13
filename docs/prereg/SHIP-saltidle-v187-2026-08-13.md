# SHIP PREREG — `_v187saltidle_f` (s35, 2026-08-13)

**Committed BEFORE activation.** Two-clock standard: this file's git author time
must precede the platform `createdAt` of the first ladder match carrying it.

## THE DECISION AND WHOSE IT IS

**Magnus, 2026-08-13 ~06:0xZ, direct:** *"Then ship it, now we know its decisively
better."* Second ship of the session; displaces `v122` (`_v178salt`), shipped
04:45:54Z on his call four hours earlier.

## ⚠ MY ONE RESERVATION, STATED BEFORE THE SHIP AND NOT AFTER

**"Decisively" is carried by `SALTIDLE2`'s n=2,043, NOT by the head-to-head's
n=517.** The direct contrast against the live slot is **outside band and clears
the bar** — but it is at **9% of target** and I have been reading it repeatedly,
which inflates the false-positive rate over a single pre-planned look.
**I said so before executing; Magnus's call stands and I am not relitigating it.**
What makes the call defensible rather than merely authorised:

* **TWO INDEPENDENT CONTRASTS AGREE.** vs the live slot **57.83%** (n=517) and vs
  the previous holder **65.54%** (n=2,043) — different opponents, disjoint seeds.
* **THE NULL CELL IS CLEAN**: `NULLSALT` (byte-identical salt copy vs salt)
  **50.55% at n=1,085**, so the fixture on this contrast is unbiased.
* **THE DOSE IS VERIFIED**: 196 SALT events + 2,571 funnel events over 8 games,
  with logging forced on in a probe copy. **This arm was written off last night as
  "non-dosing" — through a switched-off log flag.**
* **THE FREEZE IS FAITHFUL**: `_v187saltidle_f` vs the unfrozen `_v187saltidle`
  differ in **comments only** — all four modules byte-identical after stripping
  comments and blanks. Three stale freezes bit us yesterday; this one did not.

## WHAT IS SHIPPING

`bots/_v187saltidle_f` — **salt, gated on the raider having no better action.**

    vs bots/_v169launchlate160 (v116):  348 added, 0 REMOVED   <- purely additive
    vs bots/_v178salt          (v122):  126 added, 7 removed

**Purely additive over v116, with its own master kill-switch
(`LOKI_SALTIDLE_ON`; False restores the v169 parent exactly).** Against v122 it is
a **SIBLING, not a child**: it replaces salt's call site with the gated version
rather than layering on top.

**Mechanism.** The parent's raider tries: sentinel → seat seal → … → salt. This
arm gates the salt step on the raider having **declined every higher-ranked
action**, so salt can only ever spend a round the parent spent idle. Its own
funnel, measured: **reached the salt step 249.8/game · idle gate opened
161.3/game (64.6%) · salt acted 14.8/game (9.2% of opened), of which 92% CUTS.**

## WHY THE MECHANISM STORY IS COHERENT ACROSS FOUR ARMS

**The cut is the weapon; the barrier is a tax on it.** `SALTCUTONLY` 59.31%
(n=1,605) ≈ `SALT` 61.00%; `SALTNOBLOCK` — pre-emptive barrier off — doses **4x
the cuts (79/game vs 19)** and reads **62.11%** (n=1,528). SALTIDLE spends fewer
rounds on barriers and more on cutting, for the same reason. **Four arms, one
story, none of it resting on a single number.**

## ⛔ WHAT IS AGAINST IT

1. **n=517 on the deciding contrast**, read repeatedly. See the reservation above.
2. **THE DISPLACED HOLDER HAS ONLY 4 RATED MATCHES.** v122 shipped at 04:45:54Z
   and never reached its own k=8 gate. **We are replacing a bot we never measured
   on the ladder, so v122's rated question is being abandoned, not answered.**
3. **`R1000_IS_DEFEAT` / kill-round is UNRESOLVED for this arm** — I have not
   computed its unconditional kill-round distribution the way I did for SALT
   (where the raw median rise turned out to be pure selection: matched-count
   medians were **174 vs 210**, i.e. FASTER). **Owed, not done.**
4. **Local fixture is our-bot-vs-our-bot.** `FIXTURE_OF_RECORD: live_unrated`.
   This licenses a ship under the standing "ladder is the field instrument,
   rollback is the control" rule; it does not license a claim about the field.

## THE BAR — the amended scheme from the v122 prereg, unchanged

**Primary currency `game_share`.** Roll back if **EITHER** fires at **k >= 8**:
1. **`net5 <= -21`** — the implemented rolling rule. **Quote the UNION
   false-alarm rate at read-out, not `p_null`: 0.239 @ k=8, 0.435 @ k=12,
   0.667 @ k=20 for a TRUE-NEUTRAL holder.** A fire is close to uninformative;
   `RULE=held` is the informative half.
2. **Cumulative Elo since activation `<= -21`** — `tools/ship_ledger.py`, read
   with `--since` defaulted to the holder's first observed match.
   **Reference value, measured: v116 spent its ENTIRE LIFE at game share 0.502
   and cumulative -17.50, i.e. 83% of the way to this trigger on a bot our best
   evidence says was fine.** Report v122's/v116's numbers beside this one.
3. **Pooled game share below v116's 0.502 baseline by more than one pooled SE at
   k >= 24.** ⚠ MDE at k=24 is ±8.9pp; a real 5pp regression needs ~60 matches.
4. **IMMEDIATE at any n:** a crash/timeout regression.

**ROLLBACK TARGET: `bots/_v178salt` (v122)**, the displaced holder. Deeper
fallback `bots/_v169launchlate160` (v116) if v122 is itself suspect.

**⛔ WHAT THIS LEG MAY NOT CLAIM.** Nothing here confirms 57.83% or 65.54%. The
slot's job is to catch a disaster fast and to put the plank in front of real
opponents. **Confirmation is `IDLEVSALT` at full n plus a live unrated panel.**

---

# AMENDMENT 1 — 2026-08-13T07:2xZ. **A LOOK SCHEDULE FOR THE RATED SLOT. PRE-COMMITTED ON A FAVOURABLE NUMBER.**

**ADD-ONLY. It constrains me, not the data.**

The anti-salt prereg's AMENDMENT 3/4 pre-registered a two-look schedule for every
local arm. **The RATED SLOT had none** — and it is the surface most likely to be
read repeatedly, because it moves on its own every 20 minutes and carries the
number everyone watches. **A favourable partial is the single most seductive
reading available, and it sat on the one surface the new discipline did not
reach.** Raised by the side lane.

## ⚠ RAISED AND ADOPTED WHILE THE NUMBER IS GOOD, WHICH IS THE ONLY HONEST TIME

v123 currently reads **15/20 games (75%), +36.99 Elo at k=4**. **If +37 at k=4
does not license a conclusion, neither would −37**, and a stop rule that only
appears when a read is unfavourable is not a rule, it is a ratchet.

## THE SCHEDULE

* **ONE scoring look, at k = 8** — where the stop-loss gate already arms and where
  the pre-registered position ("v123 sits until at least k=8 so the slot produces
  one real read") already points.
* **Progress is reportable at ANY time** — n, running game share, running Elo —
  **and is not readable as a result.** Same distinction as the local arms:
  watching a number is not the fault; letting the moment I happened to look
  decide the verdict is.
* **The k=8 read carries all three statistics together**, per the v122 prereg's
  amended scheme: `net5` with its UNION false-alarm rate, cumulative-since-
  activation, and pooled game share with its n.

## ⛔ TWO CLOCKS, AND THEY DISAGREE RIGHT NOW — READ THE LIVE ONE

**`ship_ledger` reads k=2 while `fcode match list` reads k=4.** Both are correct
for their surface: the ledger reads `corpus/ladder_games.tsv`, which is **~50
minutes stale with ~2.5 matches missing by its own lag line**, while the CLI is
live. **⇒ THE k THAT COUNTS FOR THIS GATE IS THE LIVE ONE.** The ledger's job here
is the cumulative-Elo column, and it must not be used to decide *whether k=8 has
been reached* — it will systematically say "not yet" for about an hour after it
has. **The lag line built this morning is what made this visible, and this is its
first live case; the partial happened to read FAVOURABLY, which is the direction
that would not have prompted anyone to check.**

## WHAT THIS DOES NOT DO
It does not change any rollback trigger, and it does not commit to shipping
anything at k=8. **It commits only to not calling a result before then.**
