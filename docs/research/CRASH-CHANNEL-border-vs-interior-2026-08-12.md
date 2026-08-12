# THE CRASH CHANNEL IS NOT WHERE THE KIDNAP EFFECT LIVES — border vs interior, s33

**Research arm, 2026-08-12. Zero games run, zero rated exposure.** Instrument:
`tools/kidnap_fate.py` (landing recorded at throw time), classifier
`tools/corpus/replay_throws.is_border` (11 cells incl. the map-size trap).
Rows: `scratchpad/kf_border.tsv`, 44,639 victims, 9,697 thrown, **9,697 classified**.

## THE QUESTION

The kidnap effect has two channels and only one is the approved exploit:
* **CRASH** — victim thrown to a map-border tile, its own code queries an off-map
  neighbour, raises, and the engine destroys it permanently.
* **DISPLACEMENT** — victim simply thrown far from where it was useful.

Which one carries the measured effect decides which prototype dose it, and
therefore what a live leg's pre-registration is allowed to predict.

## THE RESULT — the crash channel shows NOTHING

```
                        BORDER landing    INTERIOR landing   not thrown
Powered by SmartFridge    1/29  = 3.45%    37/796 = 4.65%     3/318  = 0.94%
Ouroboros                 3/43  = 6.98%     4/69  = 5.80%    42/732  = 5.74%
OpenSverige (self-play)   8/1022= 0.78%    54/3795= 1.42%   151/18635= 0.81%
POOLED (opponents only)   4/670 = 0.60%    41/2683= 1.53%    81/10079= 0.80%

BORDER − INTERIOR    = −0.93pp   z = −2.45      (border LOWER)
BORDER − NOT THROWN  = −0.21pp   z = −0.67      (no elevation at all)
```

**A border landing carries no elevation over not being thrown.** SmartFridge's
+3.7pp asymmetry is carried entirely by **interior** landings — 4.65% against
0.94% — i.e. **displacement, not crash-induction.**

⇒ **A border-share prototype (`_v157gunborder`) doses the channel with no archive
signal.** The correct tree is one that raises **throw frequency**. This was the
builder's objection, raised before the measurement, and it is upheld.

## WHAT THIS DOES **NOT** SAY — the boundary is load-bearing

* **It does not retire crash-induction as a mechanism.** The mechanism is
  engine-confirmed and was watched landing in a local both-ways probe (13/13
  unguarded, 0/16 guarded). What this measures is its **prevalence in the field's
  outcomes**, which is a different quantity.
* **SmartFridge's border cell is n=29 with 1 event** and refutes nothing alone.
  The **pooled** contrast (n=670, 4 events) carries the weight.
* **The +3.71pp SmartFridge asymmetry stands** and is now better measured. Only
  the mechanism claim died.
* `no_damage_removal` **conflates an uncaught exception with `self_destruct()`** —
  unchanged since s32.
* **Unexplained and worth knowing:** SmartFridge's border share is **3.5% against
  an archive-wide 17.45%**. We throw them to interior tiles far more than average.

## HOW A NULL-SHAPED HARNESS FAILURE WAS EXCLUDED BEFORE THE NUMBER WAS READ

The previous attempt at this split **joined** victim fate to `throws.tsv` on
`(file, eid, thrown_rnd)`. **That join was invalid** — the two passes share no
entity-id space, 4,300 of 9,372 rows "matched" by coincidence, SmartFridge
collapsed 779 → 9 — **and it produced +0.52pp in the predicted direction.**
Withdrawn, not published.

The rewrite removes the join by recording the landing at throw time. The side
lane then flagged that **nothing asserted the capture path populates**: a silent
empty classifies every victim as INTERIOR and **degrades to a clean-looking null
in exactly the direction this document reports.** So the path was mutation-tested
first:

```
MUTANT A  landing never captured   -> "192 thrown victims carry NO landing"
MUTANT B  classifier pinned to 0   -> "ZERO border landings across 120 replays"
restored                            -> 192 thrown, 192 classified, 31 border, PASS
```

**Mutant B fabricates output indistinguishable from a genuine negative.** The cell
names the ground truth that refutes it (`crash_cells` seed 7102, antler, unit 14
at (13,1), BORDER on 14×18). **Without that control this result and a broken
harness would look the same, and they would look the same in this direction.**

---

# ⭐ AMENDED — THE PER-OPPONENT CUT. The pooled cell was the wrong aggregation, and the right one CLOSES THE ROAD HARDER.

**Objection raised by the side lane, and it is correct: the pool bounds the FIELD
MEAN and cannot see a concentrated effect.** The crash requires an **unguarded**
victim, and our own local probe measured that between-victim variance as a
**switch — 0/16 guarded, 13/13 and 16/16 unguarded** — not a covariate. Averaging
over a switch hides a minority. **And we never attack the average opponent:
`fcode match unrated <team_id>` is per-team and `target_value.py` picks the team.**

So the cut was re-run per opponent. **33 teams with ≥1 border landing · 1,805
border landings · 15 events total · only FOUR teams have ANY event.**

## THE ROAD CLOSES ON THE POPULATION WE ARE ACTUALLY ALLOWED TO FIRE AT

```
ADMISSIBLE TARGETS (rating >= 1650 AND inside the reachable band)
  Powered by SmartFridge  1/29     The Bisons 0/27     Leviathan 0/14
  Besvikomat 0/11   Focalground 0/8   arsonist duck 0/7   Coreflood 0/5
  LingLing40 0/4    Big O 0/3         0033 0/2           Bean counters 0/0
  team lazy 0/0
  ------------------------------------------------------------------
  TOTAL 1 event on 110 border landings = 0.91%
  the SAME teams' not-thrown baseline  = 0.74%      -> no elevation
```

**95% upper bound on the true rate given 1/110: 4.2%.** The unguarded probe rate
is **100%**; a 20% rate would have produced **22 events and we observed 1**.
⇒ **No admissible target is unguarded in the probe's sense.** That is a far
stronger closure than the pooled null, and it is the one the side lane said would
be worth publishing — **it rules out the concentrated case on exactly the
population a target-selecting programme can use.**

## ⛔ AND THE ONE CONCENTRATED SIGNAL IS THE s28 TRAP, EXACTLY

**Team `S`: 3/3 border landings removed — 100% — against 6/15 = 40% not-thrown.**
The only opponent in the archive whose border cell looks like the unguarded probe.
```
target_value.py S  ->  gap -714,  a 5-0 pays 0.52 rating points,  NOT admissible
```
**S is 714 points below us. A perfect result pays half a rating point.**
**The single team where the weapon demonstrably works is the team it is worthless
to beat** — which is s28's lesson arriving from the opposite direction, and the
reason `target_value.py` is a gate in front of pre-registration rather than a
clause inside one. *(n=3. It refutes nothing and establishes nothing; it is
recorded because it is the only concentrated signal in the archive and a
successor will otherwise re-find it and think it is new.)*

## WHAT THIS AMENDMENT CHANGES ABOUT THE TITLE

Nothing operational — `_v157gunborder` remains the wrong tree and the displacement
channel remains where the effect lives. **What changes is the STRENGTH and the
SCOPE of the negative:** it now rests on the admissible population rather than on
a field average, and **D12 is satisfied without straining** — this is archive
evidence, it sends the road to the bottom of the queue, and it does not take it
off. **A live unrated leg against an admissible team could still overturn it; what
it may not do is claim surprise, because the prior is now measured at ≤4.2%.**
