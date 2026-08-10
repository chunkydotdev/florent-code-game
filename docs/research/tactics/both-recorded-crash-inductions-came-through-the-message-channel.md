---
tactic: (C) CLOSURE — both recorded Battlecode crash-inductions arrived through the SHARED MESSAGE CHANNEL, and one of them was an accident its own authors reported. Our comms store is team-private, so that channel does not exist here
source: https://battlecode.org/assets/files/postmortem-2020-confused.pdf
origin: MIT Battlecode 2020, team "confused" (official postmortem); corroborated by the Battlecode 2009 "message warfare" account already in this library
evidence: documented
transfers: no — the vector requires a channel our engine does not provide. Filed with what would reopen it.
---

WHAT IT IS — the library already carries one crash-induction precedent: Battlecode 2009,
team "little", who reverse-engineered the broadcast hash and sent corrupted messages that
made opponents allocate a huge array and die
([`cpu-timeout-induction`](cpu-timeout-induction.md)). **Sweep 21 found the second one, in
the official 2020 postmortem corpus, and it is the same channel and the opposite intent** —
team "confused" reporting it against themselves, as a "Funny note":

> *"which caused an ArrayOutOfBoundException and crashed some other bots. We fixed this after the tournament by padding the message with zeros later on."*

*(Context establishing the referent of "which": the preceding clause in the same sentence
reads "Before the sprint tournament there was a conflict between the documentation and the
specs, so we sometimes sent 2 integers in the blockchain". "The blockchain" is Battlecode
2020's PUBLIC message channel — every team could read every message posted to it. So the
malformed payload was broadcast to the whole game, and other teams' parsers threw on it.)*

**Two independent Battlecode instances, eleven years apart, same vector: a shared,
adversary-readable message channel whose payload the receiver parses.** One deliberate and
award-winning, one accidental and self-reported. **In neither case was the attack surface
the opponent's units, the map, or the board state. It was the parser.**

**And the corpus contains the cost side of the same channel, from a different team:**
SPAARK (2025) blames message *volume* for compute exhaustion — *"out of bytecode after
getting spammed with 20 messages from a tower."* — though there the towers are their own,
so it is a read-cost problem rather than an attack.

WHY IT MIGHT TRANSFER — **it does not, and the reason is a hard engine fact worth stating
once so nobody re-opens it by mistake:**

- **Our 16-slot store is private per team.** `read_store` / `write_store` operate on this
  team's slots only. There is no cross-team channel, no broadcast, no payload we can put in
  front of an opponent's parser. **The entire vector that produced both recorded
  inductions in this engine's ancestor is structurally absent here.**
- **The library's other finding points the same way.** The only cross-team spoof anyone
  found anywhere was a replayed message
  ([`the-only-cross-team-spoof-was-a-replayed-message`](the-only-cross-team-spoof-was-a-replayed-message.md)),
  which also needs a shared channel.
- **What DOES remain is not a channel but a geometry**, and it is a different tactic with a
  different evidence base: our field measurement of undamaged builder vanishings on map
  border tiles. **That is the opponent's own enumeration failing on the map, not on
  anything we send.** It belongs to
  [`a-crash-is-recorded-as-a-win-so-learners-converge-on-it`](a-crash-is-recorded-as-a-win-so-learners-converge-on-it.md)
  and is HELD on the same organiser question as everything else in this area.

WHAT WOULD KILL THE `no` — i.e. what observation would reopen this road:

- **Any engine surface where WE choose a value that the OPPONENT's code reads and parses.**
  Sweep 21 did not find one — the store is team-private, entity getters return engine
  values, and `print()` goes to the replay. **If a probe found any such surface (a shared
  slot, a readable tag, an id we control the shape of), this file flips.** Worth one
  deliberate look at the shipped engine binary rather than an assumption, since that is how
  the loader's `ast` rules were recovered.
- **Note the transferable defensive point either way, which costs nothing:** both incidents
  killed the RECEIVER because the receiver parsed without guarding. Our engine destroys a
  unit permanently on an uncaught exception. **Every value our own units read from the
  engine and index on — an id, a position, a store slot another of our units wrote — should
  be treated as capable of being out of range**, because the 2020 team's opponents were
  killed by a documentation mismatch, not by an attacker.

BUILDER HOOK — none offensive. **Defensive and free:** audit our own store reads for
unvalidated indexing (a slot value used directly as a list index or a coordinate), since a
stale or clamped value there reproduces the 2020 failure with no opponent involved at all.

Related: [`cpu-timeout-induction`](cpu-timeout-induction.md) ·
[`the-sixteen-ints-really-are-the-only-channel`](the-sixteen-ints-really-are-the-only-channel.md) ·
[`comms-jamming-and-spoofing`](comms-jamming-and-spoofing.md) ·
[`catch-everything-at-the-top-of-run`](catch-everything-at-the-top-of-run.md)
