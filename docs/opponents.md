# Opponents

Patterns observed in other players' bots. The ladder is the real metagame — knowing what the
field does is often worth more than optimizing our bot in isolation.

For each opponent worth tracking:

- **Name / team:**
- **Ladder position when observed:**
- **Opening:** what they do in the first phase of a match
- **Signature behaviour:** the thing that makes them recognizable
- **Where they're strong:**
- **Where they're exploitable:** and whether we've actually tested the exploit
- **Our record against them:**

## Metagame notes

Trends across the field — what the top of the ladder is converging on, what stopped working,
what nobody is doing yet.

### Inherited defects worth knowing about (2026-08-07, pre-ladder)

We have no opponent observations yet — no account. But anything the **organisers' shipped
starter bot** gets wrong is a defect most of the field starts with, so it's metagame
information we can gather offline. Two confirmed so far:

1. **`_try_build_conveyor_toward_core` never fires.** Verified dead code in
   `bots/starter/main.py:286` — a grid-parity mistake, see
   [strategy-log.md](strategy-log.md). Harmless in practice for us because incidental
   trail-laying covers it (99.6% of harvesters get an adjacent conveyor anyway), but a bot
   that *doesn't* lay trail conveyors while walking would inherit the dead function and get
   **zero delivery** from its harvesters — and delivery is tiebreak #1. Any opponent whose
   harvesters look connected but whose `titanium_collected` stays near passive-only is
   probably sitting in exactly that hole.
2. **The unguarded `is_tile_empty()` out-of-bounds crash** (`starter` `_try_move`) — the v1
   finding. Still live in the shipped starter: 56 tracebacks in one 30-match probe run.
   Each one permanently deletes a unit. Opponents who never wrapped `run()` in `try/except`
   are losing units to this all game.

Both are worth checking for in replays once we can see other players' matches.
