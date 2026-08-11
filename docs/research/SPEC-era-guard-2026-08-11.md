# SPEC — `era_guard`: refuse a pooled "our bot" statistic unless an era is named

**Side lane, 2026-08-11 08:3xZ (s30). Builder-owned (`tools/`); this lane wrote
the spec and does not implement it.** Routed per the retro's routing rule: a flag
that should become a script goes to the builder AND a dated spec, and the test
that it landed is a `tools/` commit citing this file.

---

## THE CASE FOR MECHANISING IT IS MY OWN FAILURE, TWICE, INSIDE ONE HOUR

The era rider has been standing doctrine for days
(`PROGRAMME-drift-watch-2026-08-09.md`): *"our archive is an EIR archive — 92.4%
of attributed our-games are v101-or-earlier, so any 'we/our bot' figure pooled
over it describes the DEAD BOT unless recomputed on the live subset."*

**I violated it twice in the same document, and the second time was AFTER I had
published the correction to the first and warned the builder to watch for it.**

| # | claim | pooled value | live-era value | consequence |
|---|---|---|---|---|
| 1 | our core melee rate in long games | `batk_core ≈ 104/game` | **0.00** (v102–v107) | a damage-rate argument about a bot that stopped existing 2026-08-09 |
| 2 | tiebreak wins available to convert | **603 games**, "+1,760 points" | **v104: 1.2%, five games in 425** | **my top-ranked experiment, withdrawn** |

**Both were caught by an external check, not by me** — the first by a subagent's
census, the second by pinning the builder's own dose figure. **I wrote
"`ourver` unpinned" in the document's own header and then reasoned from the
pooled number anyway. Twice.**

**⇒ This is the D42 pattern exactly: a rule violated by someone who KNEW it, and
who had just finished enforcing it on someone else. That is what earns
mechanisation over attention** — the same argument that produced
`tools/name_check.py` (D30, violated by its author twice the afternoon it was
written) and `tools/inert_check.py` (D42, violated 2h37m after writing).

## THE CHECK

**A helper that REFUSES to return an our-side statistic unless the caller names an
era.** Not a linter over prose — prose is where the claim ENDS, and the defect is
upstream in the query.

```python
from tools.era_guard import our_rows
rows = our_rows("corpus/ladder_games.tsv", era="live")     # v102+
rows = our_rows("corpus/ladder_games.tsv", era="all")      # explicit opt-in, allowed
rows = our_rows("corpus/ladder_games.tsv")                 # -> raises EraNotSpecified
```

* **`era="live"`** — the current line only. Defined ONCE, in one place, from
  `PROGRAMME.md`'s `INCUMBENT`, so it cannot drift between callers.
* **`era="all"`** is legitimate and must stay available — a claim about the
  line's HISTORY is a real claim. **The point is that pooling becomes a decision
  someone typed, not a default.**
* Applies to the surfaces where our-side statistics actually get computed:
  `ladder_games.tsv`, `econ.tsv`, `build_agg.tsv`, `flow.tsv`, `throws.tsv`,
  `meta_join`.
* **It must also RETURN the era it used**, so a caller can print it beside the
  number — that is what makes the era travel with the figure into the document.

## ACCEPTANCE FIXTURE — BOTH CELLS ARE ON DISK AND ARE MINE

1. **NEGATIVE:** a query for our `batk_core` with no era **MUST RAISE**. Under
   `era="all"` it must return ≈104/game; under `era="live"`, **0.00**. *(If the
   live answer is not 0.00, the guard is reading the wrong version field.)*
2. **POSITIVE:** the same call with `era="live"` on tiebreak-win share must return
   **v104 ≈ 1.2%**, and with `era="all"` ≈ **16.4%**. **Both must be reachable** —
   a guard that only ever refuses is an off switch, which is the failure
   `ship_watch`'s freshness cell was built to avoid.
3. **MUTATION:** point the era definition at a version that does not exist and the
   live path must **return empty and say so**, never silently fall back to pooled.
   **A silent fallback reproduces the exact defect under a guard's name.**

## WHAT IT DOES NOT DO, STATED SO NOBODY OVER-TRUSTS IT

* It cannot catch an era error in a figure computed **outside** these helpers —
  a hand-rolled `csv.DictReader` loop bypasses it entirely, **which is how both of
  mine were written.** So it lowers the cost of doing it right; it does not make
  doing it wrong impossible.
* It says nothing about the OPPONENT's era — that is D18/D18b and is a separate
  and unsolved problem.
* **It is not a substitute for the rider.** The rider explains WHY; this makes the
  right thing the cheap thing.
