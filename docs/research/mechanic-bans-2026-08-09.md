# Mechanic bans in the ancestor league: what the organizers already killed, and the four things they never touched

**Side lane, 2026-08-09 15:06 CEST. Companion to the early-kill arsenal, on
Magnus's max-aggression directive via the builder. The builder's insight
drives it: a mechanic an organizer BANNED or PATCHED OUT is the strongest
possible evidence it was too strong — the one signal a winner's write-up
can't fake. Web-sourced (opus agent), changelog quotes independently
re-verified against the live page by this lane before use.**

## The load-bearing fact, verified and corrected

**Our engine is a re-tuned descendant of Cambridge Battlecode 2026**
(`docs.battlecode.cam/changelog`), whose changelog describes the exact entity
roster we play — builder/gunner/sentinel/launcher/harvester/conveyor/
splitter/barrier, 2x2 core, titanium economy, 50-unit cap. The *balance
history* is therefore ours to read: the classic rush/spam exploits were found
and patched before we inherited the ruleset.

**Correction to the agent's claim, caught on verification:** it reported "every
number matches exactly." It does not — the changelog's sentinel is **damage 10 /
ammo 5**, ours is **damage 18 / ammo 10** (CLAUDE.md). So we are NOT a
byte-identical copy; there was further tuning after that changelog or our fork
diverged. **What transfers is the design INTENT and the direction of each
nerf, verified by quote — not the exact spec.** Every "already dead" item
below was additionally cross-checked as still structurally true in our own
CLAUDE.md, so the do-not-rebuild list holds regardless of the version gap.

## DO NOT REBUILD — organizer-patched, and confirmed dead in our rules

Each verified two ways: the ancestor's changelog quote (why they killed it) +
our CLAUDE.md (that the nerf is present in what we actually play).

| dead strategy | organizer action (verbatim) | confirmed in our ruleset |
| --- | --- | --- |
| **suicide-builder rush** | *"Builder bots no longer deal damage when they self-destruct… Removing builder self-destruct damage nerfs rushes"* | `self_destruct()` = "no damage dealt" ✓ |
| **cheap-builder swarm** | builder base 10→50→30 Ti; *"more expensive builders and a global unit cap… reduce spam"* | builder 30 Ti, +20% scaling, MAX_TEAM_UNITS 50 ✓ |
| **infinite self-heal blob** | *"Healing is now 1 Ti for 4 HP (down from free 10 HP)… so normal attacking is actually viable"* | heal 1 Ti → +4 HP ✓ |
| **two-sentinel builder one-shot** | sentinel reload→2, dmg cut; *"stops two Sentinels from instantly one-shotting a builder bot"* | our 2×18 = 36 < 40 HP — **invariant preserved** at different numbers ✓ |
| **wide unit spam generally** | 50-cap + +20% scaling on builders/gunners/sentinels | present ✓ — go tall/efficient, the 40th unit is brutally scaled |

These were the historically DOMINANT strategies in the family and they are
gone by rule. Building toward any of them re-runs a fight the organizers
already settled against us.

## STILL OPEN — never nerfed in the ancestor, live in our rules (the gold)

These appear in **zero** balance changes across a complete dated changelog —
left alone, which means underexplored or deliberately permitted. Ranked by
expected value for an "unreasonable variant":

1. **Launcher throw / kidnap — ZERO balance changes ever** (only a bug fix:
   "launchers couldn't fire under certain conditions"). Our launcher picks up
   a builder *from either team* and throws it to any passable tile. The
   corpus shows it used only as displacement (early-kill-arsenal §4: 61k
   throws, 0 core attacks) — so the OFFENSIVE forms are both unpatched AND
   unexplored: yeet an enemy builder into our sentinel line (friendly-fire
   hits whatever's on the tile), into a walled pocket, or off its heal seat
   mid-siege. **Strongest Loki-class candidate.** Gated behind the builder's
   S2 probe (does a thrown enemy eat our turret fire same-round?).
2. **Enemy-core spawn-tile denial — never banned; BC2024 teams used offensive
   spawn-blocking as a legal tactic.** This *externally corroborates the
   builder's own spawn-lock probe today* (body-form verified: enemy body on a
   ring tile makes can_spawn false 1:1). Two independent lines — a live probe
   and a comparable-league precedent — say the same thing. This is Loki-3, and
   it composes with the rush (sentinel fires through the collar).
3. **Tiebreak-turtling — never patched** (Halite's "desertion meta" was
   community-discussed, never balanced away). Our win condition falls to
   tiebreakers at r1000 (Ti delivered → harvesters alive → Ti stored →
   coinflip). **This is exactly the CAD survive-to-r1000 finding, externally
   corroborated:** a bot that can't win the core fight but maximizes delivered
   Ti and keeps harvesters alive steals games without attacking. Since Elo is
   game-share, every steal pays. The rush and the turtle are opposite tools
   for opposite matchups — which is the tension the builder is currently
   resolving by matchup (rush ships as Loki, Eir keeps the survive matchups).
4. **Crash-induction — never patched, and our engine's hard failure mode.**
   TLE only interrupts a turn (soft); an *uncaught exception permanently
   destroys that unit for the whole match* (hard). You cannot steal enemy CPU
   (isolated 10ms budgets, unlike the Screeps CPU-theft ban), but driving an
   enemy bot into a state its `run()` doesn't handle — e.g. a launcher
   throwing its builder somewhere its code assumes impossible — induces the
   permanent-kill. **Speculative transfer, labelled as such; needs a probe
   before any weight.** Highest ceiling, lowest confidence.

## The strategic backbone, externally confirmed

- **"Defence is hard, attack is easy" is the family equilibrium** (BC2021
  postmortem), and our pre-nerfed ruleset softened the *builder* rush but left
  **turret aggression** as the surviving strong line. **This is direct
  external backing for Loki-2 (the sentinel rush)** — the organizers nerfed
  every cheap-swarm and self-heal line but never the turret push toward the
  core.
- **Cautionary tale (BC2020, DIRECT):** organizers nerfed economy buildings to
  slow rushers; it *backfired* — the defensive tech-up lost its payback window
  and **rush prevailed harder.** Read-across: a slow economic answer to
  aggression entrenches aggression. It weakly supports the builder's decline
  of a hedged dual-posture Loki — half-measures against rush lose to rush.

## What this hands the builder

1. **A verified do-not-rebuild list** (the table above) — protects arena time
   with organizer patch notes, not just our tape.
2. **Loki-2 sentinel rush is on the surviving-strong-line side of every nerf**
   — the family's whole balance history points at turret aggression.
3. **Three more unpatched offensive avenues in EV order:** launcher-throw
   kidnap (S2 probe first), spawn-tile denial / Loki-3 (probed today, plus
   BC2024 precedent), tiebreak-turtle (the Eir/CAD survive line, now with an
   external name). Crash-induction is the moonshot behind a probe.
4. **Version caveat:** treat the changelog as *why levers were pulled*, not
   *our exact spec* — our sentinel hits harder (18 vs 10) than the version
   quoted, so re-derive any magnitude from CLAUDE.md/probes, never from the
   ancestor's numbers.

## Provenance

Web agent (opus, read-only): Cambridge Battlecode changelog + Lux 2021
changelog + BC2020/2021 postmortems + Screeps ban forum + Halite/Terminal/
CodinGame (nulls recorded). Changelog quotes in the DO-NOT-REBUILD table
**re-verified verbatim against the live page by this lane** (WebFetch,
2026-08-09 15:0x) — all six confirmed; the "exact numbers match" overclaim
was corrected here. Nulls: Terminal, CodinGame, Halite carry no organizer
bans reachable. Internal doc-mine (offensive tactics with our own refutation
status) is the third piece and lands separately.
Key URLs: docs.battlecode.cam/changelog ·
github.com/Lux-AI-Challenge/Lux-Design-2021/blob/master/ChangeLog.md ·
stonet2000.github.io/battlecode/2020 · blog.stoneztao.com/posts/bc21.
