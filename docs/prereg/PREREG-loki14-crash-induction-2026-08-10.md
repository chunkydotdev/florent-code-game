# PREREG — LOKI-14: CRASH-INDUCTION by launcher kidnap onto a map border

**Committed BEFORE submission, activation and leg creation.** Line `loki`.
Comparator **v104 "Loki v2" = `bots/_v130loki13`**, the live incumbent.
Pinned panel, pinned maps, **pooled to n=100/arm**.

**NORMS: APPROVED.** Magnus, 2026-08-10: *"That's the entire reason we are named
Loki — find these and use them. You are approved to build it."* The hold that
had been placed on this tree is released; `CLAUDE.md` point 0 now carries the
standing brief.

    bots/_v131loki14 = bots/_v130loki13 + LOKI14_KIDNAP_ON (+ LOKI14_KIDNAP_LOG)

`main.py` and `eco.py` **byte-identical**. `raid.py` replaces two lines of the
launcher's EXILE branch with a guarded plan call and adds `_kidnap_plan` /
`_kidnap_done`. **The plank is a DESTINATION CHANGE ONLY** — v104 already throws
adjacent enemy builders; this changes where they land.

## The mechanism, read off the engine binary

Every fact here is from disassembly, two toolchains intersected
(`docs/research/engine-source-crash-and-launcher-2026-08-10.md`), **not** from
the organisers' doc:

* `can_launch` / `launch` have **zero vision guards and NO team check**. Pickup
  ring **d² ≤ 2**; throw target **1 ≤ d² ≤ 26 measured from the launcher**;
  **0 ammo**; launcher cooldown +=1; **position-only mutation** of the victim.
* An uncaught exception escaping `run()` routes to `Game::destroy_entity`
  (`0x1ac5c`). **`SystemExit` and `KeyboardInterrupt` are the ONLY exemptions —
  an escaping `GameError` destroys the unit permanently. A CPU timeout does
  not.**
* `get_tile_*` / `is_tile_*` raise off-map; `can_*` predicates are total.

**So a builder standing on a map-border tile is one careless neighbour query
away from deleting itself, and we can put it there for free.**

## THE SPLIT-THROW DESIGN IS THE WHOLE POINT

**Half the throws go to a BORDER tile, half to an INTERIOR tile**, alternating
on a per-launcher counter that advances **only on a throw that landed on its
intended arm** (so a fallback cannot desynchronise it). Balanced to within 1 by
construction. **Deliberately not `random.` —** `rush_probe` is the only bot in
this repo that calls it and is excluded from paired runs for exactly that reason.

**THE INTERIOR ARM IS A WITHIN-LEG PLACEBO AND MUST READ ~0.** It holds "being
thrown" constant and varies only the border property, so **the leg never has to
assume that an INDUCED border-standing behaves like a naturally-occurring one**
— if thrown builders are in a different mode, both arms are. Census baseline for
the placebo: **0 events in 2,334,017 non-border builder-rounds.**

## Bars

**MECHANISM (did it fire): border-arm throws >= 20 across the leg**, decoded
from the leg's own replays via the `LOKI14 KIDNAP arm=…` stream. Local battery
produced border 20 / interior 19 over 16 matches. **Missed → the leg answered
nothing.**

**PRIMARY (the exploit itself): enemy units removed WITHOUT a damage event,
within 3 rounds of a border throw, versus the same within 3 rounds of an
interior throw.** Measured with `tools/crash_census.py`, which is validated
against a positive control (`bots/_probe_crash`: 20 detections / 0 on the
negative control) and whose false-positive class is stated — the wire format
cannot distinguish a crash from `self_destruct()`, a friendly `destroy()`, or
`resign()`.

**BAR: border arm >= 3 of 10 throws followed by an undamaged removal, against
the interior arm's ~0.** Base rate for an undamaged removal unconditional on
throws is 29.6%, so **the interior arm is the control that matters, not that
base rate.**

**SECONDARY: `core_kill_share` vs the v104 control at n=100.** Reported, and
**not** the thing this leg is for — a crash plank that deletes enemy builders
without moving the currency is still a finding.

## Falsifier

1. **Border ≈ interior → the border property does nothing**, and the 224-per-10k
   border census was confounded (those bodies walked there under their own
   navigation, plausibly while running the very routine that raises).
   **This is the outcome the placebo exists to make readable.**
2. **Border > interior, `core_kill_share` flat → the exploit works and does not
   pay.** Labelled, banked as mechanism, not as a currency gain.
3. **Border > interior AND currency up → the plank lands.**
4. **Mechanism bar missed → answered nothing.**

## Known limits, from the build, stated before the leg

* **THE BORDER ARM IS STRUCTURALLY UNREACHABLE ON BIG MAPS.** Throw range is
  d²≤26 *from the launcher*, and `_try_build_launcher` sites it near our core —
  so a border target exists only if the launcher is within ~5 tiles of an edge.
  Measured: on heart (28×20) the launcher sat at margin 6-8 and produced **36
  throws, all fallback, zero arm data.** **Usable n is kidnaps by launchers near
  an edge, not all kidnaps, and a large-map panel can return n=0.** Our pinned
  maps include fjordgate 10×10 and jackpot 16×16, which produced all the local
  arm data.
* **It is opponent-conditional.** Six teams show 722,545 border builder-rounds
  and **0** events — the border is not lethal in itself. Named carriers from the
  archive: `vjg` 96.1%, `S` 89.1%, `Ship Happens` 87.4%, `Troupe` 84.9%;
  `Cookie` excluded as adversary-locked (different mechanism, p=5.2e-08); four
  teams explicitly **unclassified rather than called immune**. **None of these
  are on our pinned panel**, so a null here is a null about OUR panel.
* **No natural experiment exists** — across 940 archived games there is not one
  hostile launcher throw of a vulnerable team's builder. **It can only be
  settled live**, which is what this fixture is for.
* 27 local matches, **0 tracebacks**, on a stderr instrument validated against
  `_probe_crash` (97 tracebacks captured). Local probes are our own
  reimplementations and **none of them crashed** — so nothing local supports the
  effect, only the mechanism firing.
