# BOOT-LOAD AUDIT — where the ~100k session-init tokens go

**Side lane, 2026-08-10 08:0x CEST**, on Magnus's question: *"are we duplicating
information or carrying stale/irrelevant information"* in the boot docs.
Read-only analysis; **the cuts themselves are builder/command-file/HANDOVER edits
and are NOT this lane's to execute** — this doc is the analysis + a ranked cut
list for whoever owns each file. Two load-bearing claims verified against the
primaries (below); the rest is the sub-agent's audit, anchors spot-checkable.

## THE HEADLINE: THE 100k IS NOT `CLAUDE.md`. IT IS THREE WHOLE-FILE READS.

`CLAUDE.md` (9.4k) is real but small. The boot cost is dominated by three reads
the command files issue **without a line budget**, against files that grew
unbounded:

| read | ~tokens | lane | the problem |
|---|---|---|---|
| **HANDOVER.md** (whole) | **34,500** | builder | 93% is superseded session log |
| **tactics/INDEX.md** (whole) | **25,800** | research | it's a registry; boot needs the tail |
| **coordination.md "tail"** | **5k–30k+** | all | "tail" undefined against a 434k-token file |

**Auto-loaded every session (unavoidable): ~10,300** — project CLAUDE.md 9,400 +
global 379 + MEMORY index ~500. Everything else is an *instructed Read*, and the
Read tool loads the WHOLE file unless `offset/limit` is passed. That is the
mechanism: the bloat is not what the docs contain, it is that boot reads them
entire.

## VERIFIED CLAIMS (checked against the primary, not taken from the agent)

- **HANDOVER split point CONFIRMED at ~line 152/153.** Line 1 = `# LIVE: v102 …
  Session 26 wrap` (current); line 152 = `## ===== PRIOR STATE (s24 boot block)
  — superseded, kept for reasoning =====`. A booting session needs **lines
  1–152 (~2,500 tok); lines 153–2106 (~32,000 tok) are self-labelled superseded.**
- **AGENTS.md CONTRADICTS the corrected rules — verified by direct read, not
  grep** (my first grep for the *corrected* phrase came back empty, which is
  exactly what a file holding the *un*corrected phrase produces — so I read the
  lines):
  - line 11: *"titanium **delivered to core**"* — CLAUDE.md line 11 explicitly
    corrects this: *"'collected', not 'delivered to core' … the ENGINE settles
    it: `titanium_collected`."*
  - line 23: cost *"rises as you build more of **that category**"* — CLAUDE.md
    line 23: *"ONE GLOBAL ADDITIVE team factor (NOT per-category) … Per-category
    is dead."*
  **AGENTS.md is a stale fork of CLAUDE.md 1–201 carrying two engine-refuted
  rules.** It is NOT auto-loaded by Claude Code (grep for any import/`@`-ref: 0
  hits, control matched), so it costs 0 boot tokens here — but any Codex/Cursor
  session in this repo boots on the wrong rules. **Correctness hazard above
  token cost.**

## RANKED CUT LIST (owner in brackets — none are the side lane's)

1. **[builder] Split HANDOVER.md at line 153** → archive 153–2106 to
   `HANDOVER-archive.md`; keep 1–152. **~32,000 tok/builder boot. Risk: low** —
   the split point is a clean self-labelled boundary. Belt-and-braces: make
   `builder.md` step 1 read HANDOVER with `limit≈160`, so the saving holds even
   before the file is split. **This is the single highest-value change.**
2. **[research] Stop reading `tactics/INDEX.md` whole at boot** → read its
   wheel/summary tail, not 1,306 lines. **~20,000 tok/research boot. Risk: low**
   — it's a lookup registry, not linear prose.
3. **[all lanes] Bound the `coordination.md` "tail"** → "since the last `## …
   wrap` marker" or "last 300 lines". **Up to ~25,000 tok. Risk: low if
   generous** — too tight and a session misses an open ASK.
4. **[builder] Fix AGENTS.md** → reduce to a pointer to CLAUDE.md, or regenerate
   it FROM CLAUDE.md 1–201 so it can't drift. **Fixes the two wrong rules; 0
   boot tok for Claude, ~6k for any second harness.**
5. **[builder] Move CLAUDE.md 296–358** (launcher offsets, six-roads status
   table, carve-outs) → HANDOVER or the research doc it already cites
   (`AUDIT-the-six-refuted-roads`). **~1,335 tok/every session. Risk: low** —
   it's volatile *status* in an auto-loaded file; `gate.py` greps PROGRAMME, not
   CLAUDE, so no tool depends on these strings.
6. **[builder] Dedup the Loki directive** — it is byte-identical in PROGRAMME.md
   54–61 and CLAUDE.md 259–266, with the "consequences" near-verbatim in both.
   Keep it in **PROGRAMME.md** (the parsed authority, read before HANDOVER at
   boot anyway); replace CLAUDE.md 259–295 with a 2-line pointer. **~650 tok.
   Risk: low.**
7. **[builder] Trim the outage-forensics** from CLAUDE.md's two new
   instrument bullets (225–239) — keep each rule as one line, drop the
   byte-level `Error: True` / `rating=1599` retelling. **~400 tok.**

**Realistically recoverable from the boot path: ~50–65k tokens**, dominated by
cuts 1–3. Cuts 4–7 are smaller but 4 fixes a live correctness bug and 5–6 stop
auto-loaded files carrying volatile status that drifts.

## THE ONE STRUCTURAL LESSON

**Every one of the big three is "Read a file that grows unbounded, with no line
budget."** The durable fix is not a one-time trim — it is that **boot Reads of
append-log files (HANDOVER, coordination, INDEX) must carry a `limit` or a
"since marker X" bound**, so they cannot re-inflate as the files grow. A trim
without that bound is back at 100k in a week. This is the same shape as the
register/match-id work: the content was fine, the apparatus around loading it
was unbounded.
