# SPEC — stamp our own initiative on every match we create

**Side lane, 2026-08-11 06:2xZ. Commissioned by Magnus in-session:** *"Do we
stamp anything that isn't our initiative? We have a script that runs games now,
that should do it automatically if it's not."*

**Builder-owned (`tools/`). This lane wrote the spec and does not implement it.**
Routed per the retro's routing rule: a flag that should become a script goes to
the builder AND a dated spec, and the test that it landed is a `tools/` commit
citing this file.

---

## THE ANSWER TO THE QUESTION, MEASURED — "partially, and by scraping"

Verified on the tree at `487466f`:

| surface | what it records | what it cannot answer |
|---|---|---|
| `scratchpad/.rate_ledger` | **25 lines of bare unix timestamps** (`1786425663`, …) | which match, which opponent, which arm, ours or theirs |
| `scratchpad/arm_*.txt` | the runner appends `"$id $R"` where `$R` is the raw CLI JSON **containing `matchId`** (`loki19_treat_w1.sh:23`) | untracked, per-leg, shape differs per runner, no schema |
| `tools/rate_budget.py:77` | **scrapes** `"matchId": "…"` back out of those arm files with a regex | nothing durable; it is reconstructing what was never written down |

**So the information exists and is thrown away into ad-hoc text.** `rate_budget.py`
already says so in its own docstring at `:25` — *"A local ledger would have been
the obvious build"* — and at `:60`: *"ATTRIBUTION IS REQUIRED AND THE PLATFORM
DOES NOT SUPPLY IT."*

**AND THE PLATFORM GENUINELY CANNOT SUPPLY IT.** `fcode match list --mine`
returns matches **opponents initiated against us** mixed with our own;
`triggeredBy` is the match TYPE (`unrated`/`test`/`ladder`), not the actor, and
`sourceMatchAId`/`sourceMatchBId` are null. **There is no field anywhere that
says who pressed the button.**

## WHY THIS IS NOT BOOKKEEPING — IT HAS ALREADY COST US TWICE

1. **The s28 budget meter read `7 of 5` spent.** Cause: two of the seven were
   Banminary challenging *us*. It was caught **only because 7-of-5 is
   arithmetically impossible**. *"Had ONE foreign challenge landed instead of
   two it would have read a plausible 5/5 and silently stalled every runner."*
   A ledger of our own creations makes the count exact instead of inferential.
2. **The scouting question Magnus raised the same session is unanswerable
   without it.** "Do opponents ship a version after we play them" requires
   knowing which matches were *our* initiative. Today that must be reconstructed
   from untracked scratchpad files, per leg, by regex.

## THE SPEC

**One tracked, append-only TSV: `corpus/our_matches.tsv`.** Written by every
script that creates a match, at the moment the CLI returns.

    created_at_utc  match_id  match_type  opponent_id  opponent_name  our_version  arm_tag  runner

* `created_at_utc` — from `date -u`, in the same shell call. Never interpolated.
* `match_id` — parsed from the CLI response. **If the response carries no
  `matchId`, write a row with `match_id=REJECTED`** — a rejected challenge still
  consumes rate-limit budget (measured: rejections appear to count), so a ledger
  that records only successes is wrong in the direction that matters.
* `arm_tag` — the leg/arm this fired for (`loki19_treat_w1`), so a read-out can
  select its own games without a scratchpad archaeology step.
* `runner` — which script wrote the row. Two runners served one leg on 2026-08-11
  and the read-out had to say so in prose.

**GATE ON THE LOAD-BEARING FIELD, NOT `$?`.** The row is written on the presence
or absence of `matchId` in the response body — never on the exit code, which on
this CLI is `0` while printing `Error: True`.

## THE SELFTEST THIS MUST CARRY, OR IT IS NOT AN INSTRUMENT

Per the standard the repo already enforces (`meta_attrib.py` is the template):
call the production writer, assert semantics, drive it to the uncomfortable
verdict.

1. **A rejected challenge MUST produce a row.** Feed a response body with no
   `matchId`; require `REJECTED`. (The failure mode is silent under-counting.)
2. **`--mine` MINUS the ledger MUST be non-empty on real data** — that difference
   IS the opponent-initiated set, and it is the whole point. If it comes out
   empty on a period where we know a foreign challenge landed, the ledger is
   over-claiming.
3. **The blind state must REFUSE, not permit** (the `rate_budget.py` standard):
   if the ledger file is missing or unwritable, the runner **aborts before
   firing** rather than firing unrecorded. An unrecorded match is exactly the
   defect being fixed.
4. **Mutation:** delete one row and require any consumer's count to change. A
   ledger nothing reads is a log.

## WHAT IT UNLOCKS ONCE IT EXISTS

* `rate_budget.py` drops the regex scrape for a read (`:77`), and the meter
  becomes **exact** rather than plausible.
* **Opponent-initiated matches become identifiable by subtraction** — we would
  learn, for the first time, how often other teams challenge *us*, which is
  itself a scouting signal and is currently unmeasured.
* Leg read-outs select their games by `arm_tag` instead of by reconstructing
  windows from timestamps.
* D18b's exposure count (how many times a cell has already seen a mechanism from
  us) becomes a query rather than a memory.

## LIMITS, STATED

* This records **our** initiative only. It cannot establish who initiated a
  match we did not create — it establishes that *we did not*, which is the
  half we can know and the half that was missing.
* It is retrospective to nothing: rows begin when the writer ships. The existing
  `scratchpad/arm_*.txt` files can be back-filled **only where they still exist
  and are unambiguous**; a back-fill must be tagged as such and never mixed with
  live rows without a source column.

---

**APPENDIX (append-only, 2026-08-13T17:09Z, builder s37):** implemented by
`tools/match_ledger.py`. Its selftest and both in-file mutation recipes were
re-run and recorded at
`docs/research/RECORD-mutation-tests-inert-ledger-diffcheck-2026-08-13.md`.
This line closes the citation chain: the tool declares IMPLEMENTS against this
spec, and the spec names its implementation.
