# PREREG — **SPAWNPOCKET (`QUEUE #64`)**: never put a builder in a cell it cannot leave (research s40, 2026-08-14)

**STATUS: committed BEFORE the arm tree exists** (two-clock standard; side lane
certifies against the first shard row). Research designs; **the BUILDER builds
and executes**; the verdict sentence is theirs.
**Control: `bots/_v223sealrepair` (v140)**, live holder.
**Source: `docs/research/HOME-LOCK-MECHANISM-2026-08-14.md` §5.1** — five
candidate mechanisms refuted with controls, this is the residue.

---

## THE TREATMENT — two halves, and they act on DIFFERENT MAPS
**(a) TERRAIN HALF** — `main.py`, the `cands.sort(key=…)` before the `can_spawn`
loop: add a precomputed free-region size as the **leading** key so a pocket tile
is demoted to last resort rather than banned (never lose a legal spawn).
`POCKET_MIN = 8`; one cardinal flood per ring tile, cached — MAPCODE-class,
map-keyed, deterministic, zero recurring CPU. **Fixes 37/37 terrain pockets, ALL
ON VALKYRIE, at 50% of valkyrie games.**
**(b) PAVE HALF** — `eco.py:934-954`, the `readable` pave branch of `_move`:
refuse the pave when laying that conveyor would leave an orthogonally adjacent
friendly builder with ≤1 free exit. **Addresses 62 pave-sealed bots — midgard 30,
fjordgate 10.**

## ⛔ WHERE THIS PREREG DEPARTS FROM ITS SOURCE, AND WHY
The report's registration line proposes **one primary segment: pocket maps
{valkyrie, midgard, fjordgate}**. **I am not registering it that way**, and the
reason is the constraint I put in the worst-maps brief this afternoon: *do not
assume one cause.*

**The two halves act on DISJOINT map sets and on maps with OPPOSITE standing.**
(a) is **valkyrie-only**, and **valkyrie is one of our BEST cells (80.0%)**. (b)
is **midgard + fjordgate**, which are **two of our five WORST cells (38.2%,
38.5%)**. ⇒ **A pooled read over {valkyrie, midgard, fjordgate} would let a
valkyrie move — on a map we already win four games in five — carry a segment
whose value proposition is the worst-map deficit.** A positive result would be
unattributable, and the row would ship on evidence from the wrong half.

**⇒ OBLIGATION 15a/15b AS REGISTERED HERE:**
* **PRIMARY SEGMENT (single, per 15b): {midgard, fjordgate}.**
  **PRIMARY MECHANISM: the PAVE half (b).** **EXPECTED DIRECTION: POSITIVE.**
* **`valkyrie` is DESCRIPTIVE ONLY.** The terrain half (a) is built — it is
  cached, free at runtime and provably correct — **but a valkyrie move CANNOT be
  read as evidence for the primary, and the pooled three-map number is not this
  arm's effect.**
* **`ragnarok` is EXCLUDED** (2 pocket bots / 84 games); the report is right that
  including it dilutes, and **my own "lock-heavy" vocabulary would have made
  exactly that mistake** — the segment term must come from the mechanism, not
  from a geometry label.

## ⛔⛔ AMENDMENT A1 — 2026-08-14 ~16:4xZ, PRE-SCREEN, ON THE BUILDER'S DOSE PROBES: **HALF (a) IS INERT BY MEASUREMENT AND ITS SOURCE PREMISE IS REFUTED**

**The per-half dose clause below fired exactly as written, on its first use, and
it killed half of this prereg before a screen row existed.**

**(a) TERRAIN HALF — REPORTED AND STOPPED.** The builder dumped spawn-candidate
region sizes on **both valkyrie seats: every non-wall candidate reads ≥40
(open).** ⇒ **THE TERRAIN POCKETS ARE NOT SPAWN CANDIDATES. BOTS WALK INTO THEM
AFTER SPAWNING.** ⇒ **the source report's §5.1(a) claim — *"fixes 37/37 terrain
pockets"* — is FALSE: the spawn chooser was never the entry mechanism.** The
half stays in the tree (behaviour-equivalent off-pocket, cached, free) and **is
reported-and-stopped per this prereg's own dose rule. Valkyrie is removed even
from the descriptive read: there is nothing to describe.**
⇒ **THE VALKYRIE FIX, IF IT IS EVER BUILT, IS A NAV-SIDE ENTRY-POINT GUARD AND
BELONGS IN `#63`'s DESIGN SPACE** — which is the row I have deliberately held
pending a navigation-or-destination decision. **This is the second independent
argument that `#63`'s answer is a nav change: pockets are ENTERED, not
spawned-into.**

**(b) PAVE HALF — SITE CORRECTED, MECHANISM UNCHANGED, AND IT IS RICH.** The
report's named site (`eco.py:934-954`, the pave-behind branch of `_move`) is **too
rare to carry a dose — a mutation probe with `floor=999` (refuse everything)
fired ZERO there.** **The volume site is the CHAIN builder (`_build_next_link`).**
The guard is now a shared method on **both** sites, and the natural dose on the
primary segment is **5-11 seal-refusals per game.** ⇒ **the primary screen is
unaffected in design and better founded in fact.**

**⇒ NET EFFECT ON THIS PREREG: the PRIMARY is unchanged and now carries the whole
arm** — primary segment {midgard, fjordgate}, primary mechanism the pave half,
bars and falsifier as registered. **What is lost is a descriptive half whose
premise did not survive measurement, and what is gained is that we know why.**

## METRICS — per half, because that is the whole point
1. **DOSE, PER HALF, BEFORE ANY EFFECT IS READ.** (a): pocket-tile spawns on
   valkyrie → ~0. (b): pave-refusals > 0 on midgard/fjordgate AND pave-sealed
   bots → ~0. ⛔ **If a half's dose does not move, that half is inert and its
   map's outcome is uninterpretable — report the dose and stop for that half.**
2. **PRIMARY: game share on {midgard, fjordgate}.**
3. **MECHANISM: class-P bot count** (sealed-region bots with zero lifetime
   actions) **per map, and locked builder-rounds** — `#54`'s census is the
   baseline (11.58% of our builder-rounds; midgard 35.6%).
4. **RIDER: kill-round non-regression**, stated as an EXCLUSION per `CLAUDE.md` —
   the CI must exclude a kill-round rise, not merely fail to show one.

## OBLIGATION 12 — RESOLUTION
Local screens are balanced-by-construction at **DEFF = 0.98**, so **naive bars
apply and the platform constants must NOT be used.** At **n = 2,700
primary-segment rows**, the 95% half-width near 50% is **±1.9pp**.
⇒ **BAR: ≥52.0 @ 2,700 continues · <50.0 drops · 50.0–52.0 UNRESOLVED-carries.**
⚠ **`GATE-1000` is `< 51` (Magnus, `c62f90c`, 14:45:59Z), NOT the superseded 48.
Operating characteristics at n=1000: a true-52 arm reads below the gate 26.4% of
the time, a true-50 73.6%.** ⇒ **a drop at 1,000 is a THROUGHPUT decision with a
known 26.4% false-drop rate at the success case; it does NOT close this row.**
Only the 2,700 falsifier does.

## FALSIFIER
**If the pave dose moves and the {midgard, fjordgate} share does NOT rise above
50.0, the "pave-sealing costs us on long-approach maps" story is refuted and
`#64`'s primary closes** — the sealing is measured and certain; that it costs
us is the hypothesis, and it can lose. **A valkyrie improvement would NOT rescue
it**; that would be a separate, smaller finding on a map we already win.

## COMPOSITION WITH `RETIRE60` — free, and stated so it is not double-counted
The same region precomputation gives `RETIRE60` a **provable** retirement
predicate for class P: **a bot in a ≤8-tile sealed region with zero lifetime
actions can never become employable**, so retiring it reclaims its +20% scale
with no judgement call (**51.5% of class-P bots never act**). ⚠ **If both arms
run, their scale-curve effects OVERLAP on the same bots — neither may claim the
full reclaim.**

## TARGET-VALUE LINE
Local screen: zero rated exposure, zero submits, zero unrated budget. Band
re-read before any live leg. ⚠ **The primary segment is ~14% of pairings, so a
live confirmation is slow by construction — say so before one is expected.**

## SCRIPT NAMING (banking rule clause v)
Mechanism, controls and counts are the home-lock report's; the per-map standings
quoted here (valkyrie 80.0%, midgard 38.2%, fjordgate 38.5%) are from this
session's per-map cut over `corpus/ladder_games.tsv` at `ourver` ≥ 125, 415
games, reproducible in ~10 lines.
