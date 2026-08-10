# SCRIPTABLE-OPS AUDIT — token-down / determinism-up (Magnus side-quest, 2026-08-10)

**The thesis:** any recurring DETERMINISTIC lane operation done by ad-hoc LLM
shell/python pays twice — tokens (re-derived per use) and determinism
(re-derived DIFFERENTLY per use). This session's own errors — the seat-flip
(7-18 that was 14-11), the map-pairing check that compared two empty strings, the
mismatched-scope greps — were ALL ad-hoc data-pulls a validated script would have
made identical every time. So token-down and determinism-up are the same fix.
Scripts land in `tools/` (builder-owned); this audit is side-lane. Token figures
are estimates (tokens/use × uses/session).

## CUT LIST — SCRIPTABLE + HYBRID, ranked by tokens × frequency × determinism-risk

| # | op | class | build | ~tok/session | determinism risk |
|---|---|---|---|---|---|
| 1 | **two-clock lock-cert** (prereg git time vs earliest leg `createdAt` → margin+verdict) | HYBRID | extend `leg_read.py --lockcert` | ~4–5k | done by hand 4+×, left "HALF DONE", direction-of-comparison from memory |
| 2 | **boot monitor-verify BY OUTPUT + freshness** (not `ps`) | SCRIPTABLE | new `boot_verify.py` | ~1.2k | **HAS erred**: "six monitors alive carried forward as if verification had a shelf life"; "alive in ps is not verified" |
| 3 | **treatment/control map-pairing + control-spread** | SCRIPTABLE | extend `leg_read.py --mapcheck` | ~1.2k | **HAS erred twice**: empty-string "MAPS MATCH"; non-discriminating control |
| 4 | **bar-null assertion at prereg time** (`bar == base_rate` → fail) | SCRIPTABLE | extend `preflight.py` | ~0.8k | ledger MECHANISABLE; "would have caught 3/10-vs-29.6% pre-commit" |
| 5 | **D14 cross-citation flag** (closure files vs newer contradicting deliverables) | HYBRID | new `xcite.py` | unbounded (not done) | its only catch to date was "luck, not process" |
| 6 | **source-age field in monitor rows** (two-freshness) | SCRIPTABLE | extend monitors | low | ledger MECHANISABLE; folds into #2's freshness helper |

## WORST WASTE — a script exists and lanes hand-roll it anyway

**`tools/leg_read.py` (built 06:29 today) already kills the seat-flip** — it
"joins on `winnerId == OUR_TEAM_ID`, never touches scoreA/scoreB". **Yet lane
work — this lane included — kept reading matches via ad-hoc inline python all
session** (every `fcode match list/info` one-liner I wrote). That is BOTH the
token cost AND how the seat-flip happened. **The top determinism win is not new
code — it is USING the tool that exists.** Recommendation: make `leg_read.py`
the SOLE sanctioned reader of leg/match results, and forbid raw `scoreA`/`scoreB`
reads in lane configs. (Precedent: the repo already shipped two slot-rule
implementations and "the durable one was the wrong one".)

## STAYS WITH THE MODEL — JUDGMENT, do NOT script

Verdict wording (D3/D4/D6–D10); saturation/resolution (D11/D13 — "requires
knowing what the fixture could have shown"); the D12 carve-out ("behavioural-
premise detection is a judgement about meaning"); method-faults narratives, loss
autopsies, transferability verdicts. **The LLM half of every HYBRID stays; only
the deterministic data-pull is scripted.**

## BUILD FIRST

**`boot_verify.py` (#2)** — cheapest (freshness helpers already exist in
`breakin_watch.py`/`sweep_watcher.py` to lift), highest frequency (every boot ×
3 lanes × every session), has a documented wrong-answer incident AND a standing
CLAUDE.md rule behind it, and produces the reusable freshness helper #6 needs.
**Close second: two-clock lock-cert as `leg_read.py --lockcert`** — highest
tokens/use, natural sibling to today's `leg_read.py`, consolidates the
leg-lifecycle deterministic ops in one certified reader.

**The standing rule applies to the fixes themselves** (drift-watch ledger): each
script runs against a case it MUST flag before its silence counts — a negative
control fixture per script. One script with a proven control beats three that
have never fired.

## PROVENANCE
Sub-agent survey of `.claude/commands/*.md` × `tools/` × the enforcement ledger,
determinism-risk anchored to incidents in `docs/coordination.md`. Builds on the
enforcement ledger's script-vs-attention labels rather than repeating them.
