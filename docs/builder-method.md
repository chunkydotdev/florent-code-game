# The builder method

How the builder arm works, written 2026-08-09 (s22) so a successor can run the
same loop without rediscovering it. This is **method**, not state — state lives
in `HANDOVER.md` and the running log lives in `docs/coordination.md`.

The session that produced this opened five roads, **refuted four of them**, and
shipped one maintenance fix. That ratio is the point: the method is optimised for
**killing ideas cheaply and being unable to fool yourself**, not for shipping.

---

## 1. The order of operations for any claim

> **rule → probe → code → corpus → local arena → field**

Cheapest and most certain first. Most claims die before they cost a build.

1. **Rule/spec arithmetic.** Free, cannot be confounded. The best finding of s22
   was a four-line table (heal 4.00 HP/Ti vs sentinel 1.80) derived purely from
   the spec. It explained more than any measurement that day.
2. **Engine probe.** A ~40-line throwaway bot in `bots/_probe_*/` and one
   `fcode run` settles most mechanics in minutes. s22 probed cost-scale
   (global, live-tracking), ore denial (works), imprisonment (probe-refuted
   on our own fixture only — a road closes on LIVE games per CLAUDE.md rule 6;
   status lives in `docs/research/SIX-ROADS-STATUS-2026-08-13.md`, never
   here), and the
   spawn ring (12 tiles, contradicting `CLAUDE.md`). **Always include a control**
   — the ore probe destroyed its own barrier to prove the barrier caused the
   denial.
3. **Read the code.** Our own source, with line numbers, before theorising.
4. **The replay corpus** (`corpus/`, `tools/corpus/`) — query it, do not rebuild it.
5. **Local arena** — see §4; it is a *safety* instrument, not a doctrine one.
6. **The field** — the only thing that decides a ship.

**Never skip upward.** s22's worst error was inferring in-game behaviour from
source (`_plan_siege` places forward guns, therefore forward siege is exploited)
and closing a road on it. The census said the opposite.

## 2. Pre-register, in a commit, before the run

Write the threshold into `docs/coordination.md` and **push it** before firing
anything. A threshold that could still be edited is not a threshold.

- Pre-register **the metric only the change can move**, not a whole-bot metric.
  A near-identical variant cannot be attributed by win rate.
- **State what would refute you**, and state the confounds *before* the numbers
  exist. Written afterwards they are excuses. s22 pre-registered "v89 was
  climbing, so a regression-to-mean drop is not evidence against Heimdall" —
  and then had to honour the symmetric version when the result was positive.
- **A stop-loss is not proof of benefit.** Heimdall passed "≤0 net Elo after 3
  matches" at +18.34 — which is **1.36 sd, not significant**. It was retained on
  its census evidence, not on that number. Say so explicitly or a successor will
  quote it as a win.

## 3. Label every claim: mechanism, or hypothesis

Three distinct things, never conflated:

| label | example from s22 |
|---|---|
| **code fact** | the raid pipeline is off after r180 (`LAUNCH_GIVEUP_RND`) |
| **measurement** | raider survival collapses 43 → 6 rounds at r150 |
| **hypothesis** | therefore unblocking r180 raises late conversion |

That third line was **false**, and the first two were both true. The whole s22
Loki programme turned on noticing they are different sentences.

Also label **post-hoc explanations as post-hoc.** If you formed it after seeing
the result, say so in the same sentence.

## 4. What the local arena can and cannot do

**It is a safety and mechanism instrument. It is not a doctrine instrument.**
s22 ran ~1,080 matches across a 2×2 and got four nulls; every doctrine answer
that day came from the replay corpus.

- **CAN** answer: does it crash? does the bot now *do* the thing (turrets built,
  shots fired, titanium spent)?
- **CANNOT** answer: is the doctrine right? The pool is dominated (we beat local
  opponents 72–90%), so it answers "is aggression free?" by construction.
- **Check the pool can generate the effect before firing.** s22 pre-registered a
  careful threshold for the launcher-latch fix and still pointed it at a pool
  where the opponent was a copy of ourselves and never inserted raiders — the
  arena could see the fix's cost and none of its benefit.

**Before any of this: identify the pool and enforce the limit — §10.** s23
learned both the expensive way, after this section was written.

**Two confounds that invalidate arena numbers outright:**

- **CPU contention.** Under `--tle 10` an overrun turn is *interrupted* with **no
  crash and no traceback**, so contention degrades play invisibly to the crash
  counter. **Run one battery at a time**; lowering `--jobs` does not fix it.
  Check `uptime` and `pgrep -f "[a]rena.py"` first. Tell subagents "do not
  measure", not "use fewer jobs".
- **Opponent crash rates.** `arena.py` prints both bots' crash counts and we read
  only ours for the whole project. s22's LOKI-1 showed +3.6pp pooled, **+6.1pp
  on legs where the opponent crashed more against it and +1.1pp on crash-free
  legs.** Its entire edge was the opponent self-destructing. **Always stratify.**

## 5. Composite first, then ablate downward

**"Refuted alone" is not "refuted."** If a plank sits at the end of a dependency
chain, its solo null measures the *absence of its prerequisite*.

LOKI-3, measured: `LATE_AMMO` alone 0.38 · `HEALER_FOCUS` alone **0.17, an exact
null** · `LATE_TURRET` alone 0.32 · **all five together 2.82** (16× the parent).
Tested one at a time and discarded on merit, the winning configuration would have
been thrown away piece by piece. The chain was turret → ammo → targeting, and
targeting is last.

So: **test everything-on against the parent first**, and only if it wins spend
legs isolating what is load-bearing. Bottom-up is also unaffordable — 2^N configs
at ~90 matches each.

## 6. Delegation

Delegate **builds and read-only measurement**; never delegate a **verdict**.

A good brief contains: the measured evidence with denominators; the cautionary
tape (what already failed and why); the hard constraints (CPU guard, blanket
`try/except` — an uncaught exception *permanently destroys that unit*; `can_*()`
before every mutating call; no platform `fcode` commands; no commits; scope to
one directory); **a pre-stated kill criterion**; and an explicit statement that
**a well-evidenced negative is as valuable as a win.**

That last line works. s22 agents killed their own doctrines, deleted machinery
they had built after measuring it misbehaving, flagged their own controls as
unusable, and led with the bad number. **Reward the self-correction, not the
clean record.**

Verify what comes back. Subagent findings are *claims*: s22 re-derived a
tree-hash tool's exclusion set against `fcode`'s real packaging source, and
re-read every load-bearing line number quoted at it.

## 7. Working with the research arm

Findings arrive as claims, not facts — and **deferring to the check-arm by
default inverts the protocol exactly as badly as ignoring it.**

- **Verify numbers against primaries before a verdict consumes them.**
- **When two analysts disagree, confirm METRIC IDENTITY before theorising about
  why.** s22 burned an exchange on a "10× conflict" that was one analyst's *mean
  of metric A* paired against another's *median of metric B*. Both were right.
  Compare like against like, then compare medians before means.
- Announce ships **and rollbacks** in `coordination.md` before they fire; a ship
  with no match behind it is invisible to a match-driven monitor.
- CPU is a shared resource: announce full-archive passes, hold them while a
  battery is live.

## 8. Hygiene that keeps the tape honest

- **Stamp note headers from `git log`, not by hand.** A stamp written at the top
  of a long note is already stale when it commits. s22 drifted three headers by
  up to 11 minutes *one hour after flagging the same bug in someone else's work*.
- **Append the process delta with the verdict**, never at wrap. It is part of
  writing the verdict, not a chore afterwards.
- **Version identity is `tools/treehash.py`**, not `md5 main.py` — the latter
  stops identifying a multi-file bot.
- **Never inherit a blocker without testing it.** "`activate` is classifier-
  blocked so I cannot ship" shelved a working fix for a night; `fcode submit` was
  never blocked and auto-activates.
- **Re-verify "known" exploit lists.** Two of three entries on the inherited
  "measured exploits to weaponise" list failed verification in one session —
  both had been corrected in our own docs years of sessions earlier and the list
  was never updated.

## 9. The standing question

Before shipping anything, ask: **is the gap this closes the gap that decides the
games?** A fix sized to the wrong gap does exactly what it claims and still
loses. The matched fixture answers that *before* the ship for the same cost as
after — and cheap evidence run in the wrong order is still the wrong order.

## 10. The instrument is a claim too (s23 — the finding that re-priced everything before it)

Every methodological rule above is aimed at the analysis. s23 learned that
none of them ask what the instrument is, and paid for it three ways in one
session:

- **The pool.** `bots/opp_v*` is OUR OWN PRIOR VERSIONS — every arena battery
  in project history was self-play, discoverable by a 4-minute grep of the
  opponents' docstrings. Published literature puts ~2× inflation on self-play
  amputation results, with reported sign flips. The foreign pool
  (`bots/*_probe`, imitations of 7 real teams) was on disk unused the whole
  time; pointed at it once, a "locally unmeasurable" plank refuted at −7.8pp.
  **State what the pool IS, from its source, before measuring.**
- **The limit.** 1,860 games ran at `--tle 0` while the real engine enforces
  10ms and our worst measured unit-turn is 12,967µs. `fcode match test` (remote
  engine, real TLE, free) exists. A plank that has never run under the enforced
  limit has an untested failure mode the local arena cannot see.
- **The enforcement.** Both of the above, plus determinism and control
  equivalence, are now mechanical: **`tools/gate.py` is the sole entry to a
  battery** (see `.claude/commands/builder.md`). `tests/test_instruments.py`
  and `tools/corpus_sanity.py` run at boot. The reason these are tools and not
  paragraphs: on this repo's record, rules written in prose get broken by their
  own author inside one session (NOISE_ON, IN-FLIGHT-before-start, the
  working-range check); rules that exit 1 do not.

Instrument selection itself follows
`docs/research/test-process-proposal-2026-08-09.md` (S0–S8): every build walks
rule → probe → parity → local mechanism → **unrated fidelity (S5)** → ship →
field window → production read, and skips are stated, never silent. **No ship
decision, positive or negative, on local numbers alone.** Local magnitudes are
labelled "local — direction only"; unrated refutes but never confirms
(47% power at n=10 — record `NOT-REFUTED (n=10)`, never `pass`); only the
ladder confirms.

## 11. Scope rules (the s23 failure family — six instances in one day)

The arithmetic was right every time it was checked; what failed was what the
arithmetic was taken to MEAN. Four rules, each bought with a battery or worse:

1. **Ask what a thing PRODUCES before subtracting it for what it costs.**
   Survival/persistence metrics never carry verdict weight — output, denial,
   delivered-objective, and win-condition currencies do. (PLANK SITE: −6.7pp
   on a true, confound-controlled survival statistic; the doctrine file itself
   pre-stated "survival is not damage".)
2. **Compute a constant's working range before building a battery on it.**
   Four lines of arithmetic would have redirected a 300-game battery whose
   dead zone covered most of its population.
3. **When a finding is stated as a category, first test whether the members
   behave alike.** Five-of-seven-row tables invert conclusions; "defect class"
   claims die at the version cut.
4. **Name the population.** "The field" meant our opponents in one doc and
   the league in another; a share of deaths is not a hazard rate until it is
   normalised by exposure.

---

## AMENDMENT — THE LIVE PINNED LEG IS GATED ON THE DOSE, NOT THE SCREEN
## (Magnus, 2026-08-13 s37: "in most cases we can run it as soon as it shows
## potential")

The ladder above reads as serial; two of its stages are not. The corefill
SCREEN (self-play vs incumbent) and the LIVE PINNED LEG (real opponents,
matched cells) answer INDEPENDENT questions — the screen prices harm in the
general case, the leg prices value against the mechanism's target class,
and self-play frequently CANNOT present that class at all (the incumbent
does not creep, camp, or ladder). Serializing them buys nothing and costs
calendar.

**The rule: a plank earns its live leg the moment its DOSE bar is met** —
the mechanism demonstrably fires — regardless of screen state. The screen
runs in parallel and both reads join at the ship decision. What the dose
gate keeps (unchanged, load-bearing): an undosed arm's live leg is a
non-experiment (dose.sh's own header); each leg still carries its own
prereg, window discipline, rate-budget yield, and counts-only claims at
small n.

Worked instances the same day this was written: rc8.3 (leg fired mid-screen,
correctly), rc8.4 (prereg initially serialized screen→leg on an illusory
dependency, amended away — the instance that prompted this rule).

---

## AMENDMENT — OPPONENT-COUPLED SCREEN DISCOUNT (research's divergence
## decomposition, 2026-08-14; basis in the coordination tail ~05:3xZ)

Self-play screens FLATTER opponent-coupled planks (eco-under-pressure,
launcher usage — anything whose payoff depends on the OPPONENT's behaviour)
by ~5-14pp against the live field, uniformly across opponent classes.
Map-mix and class-interaction were tested and excluded; MAPCODE (screened
73%, validated live) bounds the effect — map/self-knowledge planks do NOT
carry it. **The rule: an opponent-coupled plank's screen verdict carries a
−5pp haircut, and no ship recommendation cites it without a live pooled
n ≥ 50.** Corollary from the same decomposition: per-cell live reads
against an n=5 control manufacture interaction stories — control arms need
≥10/cell before class claims. (Both rules earned the hard way: the ECORAID
packet that did not assemble, 2026-08-14.)
