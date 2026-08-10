# RECORD — `ship_watch.py` SELFTEST, RUN AND BANKED (s28)

**Why this file exists: `tools/claim_check.py` flagged `ship_watch.py` on its
first live run** — it asserts *"Mutation testing caught it"* in a fixture comment
with **no record anywhere naming the file**. The claim is narrative about a past
mutation test rather than a live guarantee, and **a reader had no way to tell
those apart, which is precisely the gap the checker exists to close.**

**Rather than weakening the checker's predicate to excuse a historical sentence,
the selftest was RUN and is banked here.** `ship_watch` is the monitor that
guards ship decisions and it was worth confirming on its own merits.

```
$ .venv/bin/python tools/monitors/ship_watch.py --selftest
  [ok  ] armed holder at net5 -40 FREES THE SLOT  net5=-40.0
  [ok  ] ...and the alert text names the rule
  [ok  ] cleared-then-bleeds is CAUGHT (restart-on-OK)  sprt=BLEED cumulative_llr=+6.43
  [ok  ] ...and the fixture really does fool the no-restart design  +6.43 >= +1.73
  [ok  ] ...and cleared-then-bleeds raises an alarm
  [ok  ] unarmed holder never frees the slot  k=6 armed=False
  [ok  ] holder change resets the window  holder=v902 net5=+25.0
  [ok  ] a wrong SHIP_BASELINE cannot silence the rule
  [ok  ] slow bleed -4/match: the RULE is silent  net5=-20.0 over k=60, total -240 Elo
  [ok  ] ...the FAST bound reads OK (so the fixture is not redundant)  fast=OK
  [ok  ] ...the SLOW bound CATCHES it  slow=BLEED
  [ok  ] ...and an alarm is raised naming the slow bound
SELFTEST PASSED
```

**The strongest line is the discriminating fixture.** A `-4/match` bleed over 60
matches — **−240 Elo total** — leaves `net5` at −20.0, one point above the −21
threshold, so **the slot rule stays silent while we lose 240 points.** The fast
SPRT bound also reads OK. **Only the slow bound catches it**, and the fixture
asserts the fast bound is OK precisely so the slow bound cannot pass vacuously.
That is a guard against the failure mode the rule alone cannot see, and it is
directly relevant tonight: **v104's live reading is `sprt_fast=BLEED,
sprt_slow=OK`, i.e. the opposite pairing.**

**What this record does NOT claim:** that the historical mutation test described
in the comment happened as described. It cannot — that event is not recoverable.
**What it establishes is that the fixture discriminates TODAY**, which is the
part a decision can rest on.
