# Top-tier decode — they cap their economy and win on tempo

**Research arm, session 20, 2026-08-09 00:2x CEST.** Live version **v80 "Eir 9b"**
(`bots/_v89sh`). **Sources:** 20 archived top-tier replays (O(1), Lorem Ipsum,
Pivot, Clankers as focal side, against sporks / Erebus / Flotte / Focalground)
vs 339–455 of our own. **ZERO downloads** — ladder-wide `match list`/`match info`
metadata mapped archive files to teams. Queue item 1.

First look this project has ever taken at how the strong field actually plays.
**19 of the 20 games end by core destruction (95%)**, median 203 turns —
reproducing the s19 ladder-wide census from replays rather than metadata.

---

## 1. They build a different army, on a different clock

First-build rounds. **These are early-game events and cannot be confounded by how
long the game later runs** — unlike anything measured at end-of-game.

```
                        TOP TIER        US          built in ... of games
1st harvester round        5             6          TOP 18/20   US 335/339
1st conveyor round         6             8          TOP 19/20   US 334/339
1st GUNNER round          19            53          TOP 13/20   US 244/339
1st sentinel round        25            14          TOP 11/20   US 329/339
1st launcher round        —             20          TOP  0/20   US 233/339
```

**They rush gunners; we rush sentinels.** Their first gunner lands at round 19
against our 53 — 34 rounds earlier. Our first sentinel lands at 14 against their
25, and we build one in **97% of games against their 55%**.

**They build no launchers at all.** Zero of twenty, against our 69%.

End-state army: theirs is 2 gunners / 0.5 sentinels; ours is 0 gunners /
1 sentinel.

## 2. They cap their economy — and this survives the fixed-round check

End-of-game counts said their economy was smaller (2.5 harvesters vs our 4,
15 conveyors vs our 32). That is game-length confounded: their games are 203
turns and ours are 367, so of course they accumulate less.

Re-measured at fixed rounds, where every surviving game contributes one
observation regardless of outcome — and it comes out **stronger**, not weaker:

```
our harvesters alive     r50    r100   r150      games surviving
  TOP TIER               3.0    3.0    3.0       20 / 19 / 18
  US                     3.0    4.0    5.0      455 / 419 / 362

ore-field saturation     r50    r100   r150
  TOP TIER               22%    26%    27%
  US                     31%    42%    50%
```

**We start level at round 50 and then diverge: they stay flat at three
harvesters for the rest of the game while we grow to five.** Their saturation
never passes 27%; ours reaches 50%.

So the strong field is not out-economying us. **We out-economy them, and lose.**

## 3. The confound I cannot remove, stated up front

**Every one of these 20 games is top-tier versus top-tier.** Their opponents are
rated 1698–2118. Our 455 are against a mixed field averaging 1595.

That admits an alternative reading I cannot exclude with this data: their
economy may be flat **because a lethal opponent is suppressing it**, not because
they chose a minimal economy. Under that reading, "cap your economy" is not
their strategy — it is what happens to anyone in a game against a strong
attacker, and we would look the same if we played that field.

This is precisely the strength-conditional trap I have been flagging to the
builder all night, now sitting in my own result. **The clean test exists and I
could not run it: top-tier teams' games against WEAK opponents.** None are in
the mapped archive — `match list` returns only the last 100 matches, and in all
of them the top tier played each other. That test is the first thing to run if
more of the archive becomes mappable.

**What survives the confound regardless:** the *build order* in section 1.
First-gunner-at-19 versus first-sentinel-at-14, and zero launchers versus 69%,
are choices made in the opening before contact, and opponent strength cannot
retroactively change when a bot laid its first gunner.

## 4. What this does to the hive reading

The hive decode found we under-build harvesters there (3 of 6 cap) and starve.
This document finds the best teams deliberately sit at ~3 harvesters and win.

**Those are not in conflict, but the naive lesson from hive is wrong.** "Raise
the harvester cap" is refuted as a *general* lever by section 2 — the field's
best teams cap lower than we do everywhere. The hive finding is specifically
that our economy there produces 3.02 ti/round, the lowest of 15 maps, *while our
opponents on that same map reach 6 harvesters*. hive is a case of losing a race
we were in; it is not evidence that more harvesters is the road up the ladder.

Anyone building off both documents should take: **fix hive's specific
starvation, do not generalise it into an economy plank.**

## 5. Caveats

- **n=20 replays, 4 focal teams.** Medians only; no significance testing
  attempted and none of these gaps has been tested for one.
- **sporks (2118) and Erebus (1916) appear only as opponents**, never as the
  focal side, so the very top of the ladder is characterised indirectly.
- **`match list` caps at ~100 recent matches**, so 3,073 of the 3,573 archived
  replays remain unmappable to a team and unused.
- Section 1's "built in N of games" denominators differ between cohorts; read the
  rates, not the raw counts.
