# PREREG — LOKI-25: STAND OFF THE ENEMY GUNNER'S AXIS. **PROBE TIER.**

**Written 2026-08-11 by the s30 BUILDER. Committed BEFORE submission and before
any LOKI-25 game exists.** Tree `bots/_v146gunaxis`. Diff vs v104
(`bots/_v130loki13`): **one enumeration + one penalty term**, in `raid.py` and
one constant in `doctrine.py`. `main.py` and `eco.py` byte-identical.

**FIRED ON MAGNUS'S CALL** — *"It sounds significant enough to test on unrated
games and see if it gives something."*

## 1. WHY THIS ONE AND NOT THE OTHER SEVEN

It is the only arm today that beat a **properly powered** null.

| arm | vs v104 | n |
|---|---:|---:|
| **LOKI-25 gunner-axis** | **34/64 = 53%** | 64 |
| null — byte-identical renamed v104 copy | **32/64 = 50.0%** | 64 |
| best-fit siting | 12/24 = 50% | 24 |
| `FWD_GUN_CAP` 3→6 | 32/64 = 50% | 64 |
| heal budget · home turrets | 43% · 42% | 64 |
| rush | 16/64 = 25% | 64 |

**And it is the only arm all day with a positive kill differential at full
power: 33 core kills FOR against 27 AGAINST.**

**⛔ IT IS NOT SIGNIFICANT AND THIS DOCUMENT SAYS SO BEFORE THE LEG, NOT AFTER.
34/64 against a 50% null is p ≈ 0.35.** Two arms today read positive at n=24 and
collapsed to exactly 50% at n=64 (`FWD_GUN_CAP` 58%→50%), and the null itself
read 44% at n=36. **This is a PRIORITISATION, not a result.** The live leg is
being spent because it is the best candidate we have, not because the screen
settled anything.

## 2. THE MECHANISM

**`get_attackable_tiles_from` has ZERO call sites anywhere in the tree.** We never
compute a hypothetical turret's firing pattern, so we neither site into good rays
nor route out of bad ones. The diff enumerates visible enemy **gunners**, takes
their attackable set, and penalises any raid station inside it — reusing the
`threats`/`LOKI_EXILE_PENALTY` machinery that already exists for launchers.

**The engine asymmetry it exploits:** a gunner's shot is a straight line **blocked
by obstacles**, r²=13; a sentinel's **ignores obstacles**, r²=32. **Gunner damage
is avoidable by geometry. Sentinel damage is not.** And rotating costs a gunner
**10 Ti plus a full action cooldown**, so forcing a rotate is a tempo trade in our
favour even when they answer it.

## 3. PRECONDITION — measured, with a correction the research arm made against its own headline

**Exposure-normalised forward builder deaths per 1,000 builder-rounds:**
**US 2.915 · FIELD_pure 0.847 — 3.4×.** That is the attrition claim with exposure
controlled and it does not depend on any killer split.

**⛔ AND THE HEADLINE FIGURE WAS CORRECTED DOWNWARD BEFORE THIS DOCUMENT WAS
WRITTEN.** The first relay said our forward deaths are 91.94% gunner against a
field 42.77%. **That field number pooled games where WE did the killing** — we
are sentinel-heavy, which dragged the field's gunner share down. **The honest
comparison is 91.94% vs FIELD_pure 64.39% = +27.5pp, not +49pp.** The proposal
is unaffected — the diff targets 92% of *our* forward deaths whatever the field's
share is — but the two-fold framing was wrong and is not used here.

## 4. BARS

* **5a DOSE (live) — GATE.** Forward builder deaths per game, ours, and forward
  builds per game. **Treatment must DIFFER from control.** If the raid stations
  do not move, VOID — implementation failure, no claim about geometry.
* **5b MECHANISM.** Forward builder deaths per 1,000 forward builder-rounds.
  *What moves it: the penalty term, and nothing else in the diff.*
* **5c CURRENCY — NOT RESOLVABLE AT THIS n AND NOT CLAIMED.**
* **5d COST.** Forward presence must not fall. If raiders avoid gunner axes by
  simply not going forward, the plank has bought survival by abandoning the
  assault — **that is the falsifier and it is the most likely way this dies.**

## 5. n AND WHAT RESOLVES — gates sized as well as bars

**PROBE: 25 games, one window.** Control: the banked v104 games.

| item | kind | resolves at 25? |
|---|---|---|
| 5a dose | GATE | **YES** — a station shift shows in build/death positions |
| 5b mechanism | BAR | **PARTIALLY** — a large change in death rate, not a small one |
| 5c currency | BAR | **NO. Not claimed under any result.** |
| 5d falsifier | BAR | **YES for a collapse** in forward presence, no for a small fall |

## 6. OBLIGATION 13

```
MECHANISM METRIC READS: bots/_v146gunaxis/raid.py:499
TREATMENT DIFF TOUCHES: raid.py, doctrine.py
INTERSECTION: raid.py
```

## 7. WHAT THIS PROBE MAY NOT DO

No currency claim. No verdict. **It may not be described as confirming the
head-to-head** — 53% at p≈0.35 is not a finding, and one unrated window does not
make it one. It may not borrow any other plank's bars.
