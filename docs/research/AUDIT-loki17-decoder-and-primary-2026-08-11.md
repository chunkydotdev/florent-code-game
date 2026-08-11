# AUDIT — LOKI-17: the decoder, and the primary it is meant to feed

**Side lane, 2026-08-11 04:0xZ** (`date`, this shell). **HEAD at audit start:
`f375672`**; the builder's `ae39a67` landed mid-audit and is reconciled below.
**Commissioned by the builder** before pre-committing a matched-cell baseline
into LOKI-17 Amendment 2: *"Audit that decoder before I run it in anger."*

**Read-only.** No bot edits, no batteries, no matches. Every claim below names
the file and line it was read off.

---

## BOTTOM LINE

**The decoder is mostly fine. The PRIMARY is not, and no amendment repairs it.**

The pre-registered primary — *shootable-on-build*, 50.4% → >85% — sits
**downstream of a guard that LOKI-17 does not change**, so it reads identically
in the treatment and control arms. A leg fired on it spends a rate-limited
window and cannot learn anything, under either reading of the plank.

---

## FINDING 1 — ⛔ THE PRIMARY IS CAUSALLY BLIND TO THE INTERVENTION, IN BOTH ARMS

`bots/_v134loki17/raid.py:453`, immediately before `build_sentinel` at `:472`:

```python
if not ct.can_fire_from(bp, facing, EntityType.SENTINEL, target):
    continue
```

The plank's own comment, `raid.py:423`, states the decisive fact unprompted:

> *"The guard below (range + can_fire_from + buildable) **was already here and is
> unchanged**."*

**Therefore every sentinel `raid.py` builds is shootable-on-build in the CONTROL
arm too.** The measured value on that population is **100.0% (n=287)** — the
builder's own positive control, `docs/legs/LEG-loki17-battery-2026-08-10.md`.

**This is stronger than obligation 7's "the predicted-change set is already in
the target state at lock."** Obligation 7 describes a bar that cannot fail
honestly. This is a metric that **cannot respond to the treatment at all**: it
would read 100% if the LOKI-17 edit were reverted, deleted, or replaced with
`pass`, because both arms pass through the same unchanged gate.

### What LOKI-17 actually changes

Not *whether* a sentinel can fire — **which of the already-qualifying tiles is
chosen.** `raid.py:441-471` scores every legal `(tile, facing)` pair and takes
the closest, tie-broken by how many core footprint tiles are on-ray. Its real
channels, per the plank's own comment:

| channel | comment's claim | status |
|---|---|---|
| **distance** | median nearest d² = 32, *exactly* the sentinel range limit | plausible, **not** re-derived under the corrected decode |
| **coverage** | footprint tiles on-ray, tie-breaker | unmeasured |
| **lifetime** | median 27 rounds vs 74 | unmeasured, and see the caveat below |

**None of these is the pre-registered primary. All three are plausibly real.**

### The fork, stated with both branches and its discriminator

* **(a) the plank is dead** — the builder's own `c91c078`: *"LOKI-17 (first-fit →
  best-fit) has no defect to fix on this evidence. Its supersession is withdrawn
  **and so is the plank**."*
* **(b) the plank is alive and the PRIMARY is the wrong instrument** —
  shootable-on-build was never its channel; distance/coverage is.

**The discriminator is already in hand and it does not resolve (a) vs (b) — it
resolves the METRIC question, which is the one blocking the leg.** Because the
guard is unchanged, shootable-on-build cannot move; so its readings are
uninformative about the plank under **both** branches. **A leg on the current
primary is unspendable either way.** Re-registering on distance/coverage is a
**NEW pre-registration**, not an ADD-only amendment, because it retargets the
bar (s28 rule: an amendment may only ADD a constraint).

**⚠ CAVEAT ON THE LIFETIME NUMBER, flagged not resolved:** "median lifetime 27 vs
74 rounds" compares sentinels at the range boundary against closer ones. Closer
to the enemy core is not obviously safer, and the comparison is observational —
siting distance is chosen by the same conditions that determine survival.
**Cited here as the plank's claim, not as a finding.**

### Nothing revives the plank after `c91c078`

Checked every commit since **08-10 22:03** touching
`docs/prereg/PREREG-loki17*`, `docs/legs/LEG-loki17*`, `bots/_v134loki17*`.
`c91c078` is the last word and it is the builder's own retirement.

---

## FINDING 2 — ⛔ "DOES IT REPRODUCE AMENDMENT 1b?" INVERTS: A MATCH WOULD BE THE DEFECT

The commissioning question asked whether `tools/loki17_mech.py` reproduces
Amendment 1b's table (ours-vs-Ouroboros n=522 → 55.9 / 52.1 / **50.4**).

**It should not, and if it did that would be the alarm.**

| | Amendment 1b | `loki17_mech.py` |
|---|---|---|
| predicate | `loki9_facing.py`, **`ALIGNED_DEG = 45.0`** — a full compass step of tolerance | **exact-ray** collinearity (cross-product zero), `:83-85` |
| population | Ouroboros/Askar games, home + forward pooled | our own sentinels |

The builder's leg doc says it in terms, unprompted, the night before:

> *"The 50.4% / 67.6% figures are a 45° tolerance on a DIFFERENT population…
> **They are not comparable to these and no claim should mix them.**"*

**⇒ 50.4% is not a baseline for this decoder and must not be pre-committed as
one.** Answering the commissioning question "yes" would have certified exactly
the units error this line has caught repeatedly.

**AND THE HALF THAT SURVIVES `ae39a67`:** the builder's new comment keeps the
headline on ALL sentinels *"because that is the population Amendment 1b's 50.4%
baseline was computed on."* **Matching the POPULATION while the PREDICATE still
differs is the more dangerous version of the same error, because it looks
reconciled.** Both axes have to match, or neither number is a comparator.

---

## FINDING 3 — THE TOOL COULD NOT RUN. **FOUND INDEPENDENTLY BY THE BUILDER THE SAME MINUTE; THEIR FIX LANDS FIRST**

```
tools/loki17_mech.py:90    rows.append((ent.team, d2, ok, d2own))   # 4-tuple
tools/loki17_mech.py:107   for team, d2, ok in decode(out):         # unpacked 3
```

`ValueError: too many values to unpack` on the first decoded sentinel.
Introduced at **`b4420d0` (08-10 21:54)**, which added `d2own` and never touched
the consumer; `c91c078` fixed the DELTA table and did not touch this. One
`rows.append`, one `decode(...)` call — no other path. **Its only two possible
outcomes were a raise or *"no sentinels decoded"*.**

**FIXED by the builder at `ae39a67` (08-11 04:04Z), found by RUNNING it while
this audit found it by READING it.** Recorded because the convergence is the
evidence, not the credit: two lanes, two methods, one defect, minutes apart —
the duplication-over-division property, firing again.

**The consequence outlives the fix: the 100.0% did NOT come from this tool.** It
came from **`scratchpad/shootable.py`** — a separate 181-line instrument, same
DELTA and same nearest-footprint basis, **untracked**. The number that killed
LOKI-17 and voided LOKI-18 rests on a file one `rm -rf scratchpad/` from gone.
Same durable-record class as the audit doc committed this morning.

---

## FINDING 4 — 🆕 "FORWARD" NOW CARRIES **THREE** DEFINITIONS IN ONE EVIDENCE CHAIN

| where | definition | n |
|---|---|---|
| leg doc population table | `d²_own > 41` | 327 |
| **the 100.0% positive control** | beyond `main.py`'s reach, `d²_own > 145` | **287** |
| `ae39a67`, new forward subset | `d2_enemy < d2_own` (midpoint rule) | — |

**Three partitions, one word.** The **100.0%** attaches only to the middle row;
the new subset is neither of the other two. This is the same shape as yesterday's
*two definitions of `undamaged` differing 3.8% under one name*, and it is the
mechanism behind the LOKI-16 sign flip.

**And the midpoint rule has a specific cost:** `d2_enemy < d2_own` admits
sentinels sited by `main.py`'s home/threat path, which read **13.9%** because
they correctly aim at *threats* rather than the core. **Pooling those into a
subset labelled "the population the plank can move" reintroduces the pooling
artefact under a new name.** LOKI-17 edits `_try_forward_sentinel` in `raid.py`
only, so the population it can move is the `raid.py` one — the honest filter is
the reach argument (`d²_own > 145`), not the midpoint.

---

## THE TWO COMMISSIONED CHECKS THAT CAME BACK CLEAN

**Q3 — BASIS: nearest-FOOTPRINT, verified in the code, not the docstring.**
`:74` builds the four footprint tiles; `:76` takes `min` over them for range;
`:81-86` iterates the same list for the ray test; `:87-89` does the same for the
own-core distance. **No anchor-basis leak in this file** (the defect Amendment 1f
caught elsewhere). `scratchpad/shootable.py:6-12` documents the same basis.

**Q4 — PURE PYTHON GEOMETRY, no authoritative call:** `d² ≤ 32` + cross-product
zero + dot-product > 0, `:83-85`. Validated against the engine by
`bots/_probe_firefrom`, **with one gap worth closing:**

> `bots/_probe_firefrom/main.py:28` — `for d in (Direction.NORTH,
> Direction.NORTHEAST, Direction.EAST)`

**Three of eight facings, all in the same quadrant (+x / −y).** The defect this
probe was built to settle was **a one-compass-step rotation** — so facing
coverage is precisely the axis on which such an error hides, and the probe
samples one eighth of the compass to certify all of it. The generalisation is
probably right by symmetry; **it is an assumption wearing a measurement's
clothes, and it costs one line to make it a measurement.**

**Second, on Amendment 1g limit 1 (still open):** the probe fires across empty
tiles, so it cannot see a first-entity stop. CLAUDE.md says the sentinel's line
shot **ignores obstacles** (unlike the gunner) — which if true retires 1g — but
that is the organisers' doc, which is known-wrong in places. **One blocker placed
on the ray in the same probe settles it on the engine.** Until then TRUE remains
an upper bound, exactly as 1g states.

---

## BOOKKEEPING

The builder cited `03d2314` for *"Body + Amendment 1"*. `03d2314` (17:27) is the
body; **Amendment 1 is `e842d03` (17:38)**. Both two-clock clean and the leg has
not fired, so nothing is harmed — flagged because a lock cert naming one hash for
two documents is the re-dating hazard recorded yesterday, and it costs a
keystroke now versus an argument later.

---

## RECOMMENDATION — a recommendation, not a verdict; the builder owns the call

**Do not fire LOKI-17 on this primary.** Findings 2, 3 and 4 are repairable in
minutes. **Finding 1 is not repairable by an amendment**, because the repair is a
different bar on a different quantity — which is a new pre-registration.

## WHAT THIS AUDIT DID NOT CHECK

Stated so a successor does not read silence as clearance:
* I did **not** re-derive the median d² = 32 or the 27-vs-74 lifetime claim.
* I did **not** verify `scratchpad/shootable.py`'s arithmetic — only its
  documented basis and DELTA, which match.
* I did **not** run any instrument (lane limit: no batteries, no matches). Every
  finding is a code read or a git read, and **finding 3 is the one the builder
  settled by execution** — the check I could not run is the one that confirmed it.
