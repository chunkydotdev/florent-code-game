---
tactic: Score every throw destination, and pick up before you know where to throw
source: https://battlecode.org/assets/files/postmortem-2026-lorem-ipsum.pdf
origin: Battlecode 2026 Lorem Ipsum (seeded 15/16 in the final tournament); corroborated by Battlecode 2026 Generalized Strokes Theorem
evidence: documented
transfers: partial
---

WHAT IT IS — **Battlecode 2026 is the closest published analogue to our launcher
that has ever existed, and it is one season old.** Baby rats

> *"can also have rudimentary attack capability as well as a particular ability to
> pick up other baby rats and throw them"*

and picking up an *enemy* rat is a named verb in that league — Lorem Ipsum's
attack module *"can attack, as well as ratnap enemy rats"*. Both 2026 postmortems
converged on the same two design rules.

**Rule 1 — score the destination, do not take the first acceptable one.** Lorem
Ipsum's upgrade path is stated as a before/after:

> *"Switched our system from “throw at first good thing” to a weighted system,
> where we have weights for throwing at rat kings, cats, and other baby rats, as
> well as negative weights for throwing at our rat kings and ally rats. • Added
> ability to throw at walls"*

Generalized Strokes Theorem did the same thing exhaustively:

> *"considering every (reasonable, typically valid, and generally beneficial)
> combination of move + turn + throw, by scoring each path depending on whether it
> ended by hitting a cat, an enemy, a wall, an ally, or just left vision without
> any of these occurring"*

**Rule 2 — decouple the grab from the throw.** Lorem Ipsum's last combat change:

> *"Instead of only picking up if we know we have a good throw, we just pick up
> regardless. This is since we can just carry the rat for a while up until we get
> a good throw direction. If the 10-round timeout occurs for carries, then we just
> throw at the best direction we have."*

And Generalized Strokes Theorem adds the tempo reason for holding: *"we would
hold enemies for multiple turns before starting to consider throwing"*, because a
better target may arrive.

WHY IT MIGHT TRANSFER — **rule 1 transfers cleanly and rule 2 does not, and the
split is worth stating precisely because our current hook is the naive version.**

[[launcher-defensive-interception]]'s builder hook is literally *"throw it to the
farthest passable tile from our core"* — that is **"throw at first good thing"**,
the exact policy a 2026 team measured itself out of. The scored version costs no
extra engine call: `is_tile_passable` is already needed per candidate, and the
destination set is bounded by r²=26 around the launcher.

Terms our ruleset actually supports, in rough order of value:

| term | why | sign |
|---|---|---|
| tile lies in a visible **enemy gunner**'s facing line | blanks their gun / burns their ammo ([[blind-their-gun-with-their-own-body]]) | **+** |
| distance from **their** core | maximises the walk-back, and turns are the resource they cannot buy ([[displace-dont-kill]]) | **+** |
| tile is inside a prebuilt cell | imprisonment ([[throw-into-prebuilt-cell]]) | **++** |
| tile is adjacent to one of **our** buildings | hands them a free attack seat | **−−** |
| tile is orthogonally adjacent to **our core** | hands a raider the only tiles that matter | **−−−** |
| tile lies in **our own** gunner's lane | blanks our own gun (see [[the-blockade-blanks-your-own-guns]]) | **−** |

**Rule 2 is `transfers: no` and should be recorded as such**: our
`launch(bot_pos, target)` is a single atomic action — pick up *and* place. There
is no carry state, no 10-round hold, no waiting for a better target while holding.
The engine gives us the grab and the throw in one call, so the only decision is
the destination. **Do not build a carry queue; the API forbids it.**

**One more thing the source hands us for free: they shipped it broken and said
so.** Lorem Ipsum's own confession — *"Note that as of now we do not have any
toll at throwing at our own rat kings or rats, or any checks for throwing at
walls (added later)"* — is the strongest available argument for writing the
negative terms in the table above **in the first version**, not the second.

WHAT WOULD KILL IT — 

1. **CPU.** We have **10 ms per unit per turn** and the candidate set inside
   r²=26 is up to ~81 tiles; scoring each against every visible enemy gunner's
   attack pattern is the kind of nested loop that has cost us turns before.
   Lorem Ipsum flags the identical cost in their own league: *"this was pretty
   bytecode heavy. This forced me to remove the one-step BFS"*. **Cap the
   candidate set before scoring, not after.**
2. **Volume.** At ~1-3 grabs per game at home, the difference between a good
   destination and a mediocre one is a small number multiplied by a small number.
   This is a cheap refinement to a launcher we build for other reasons, **not a
   reason to build a launcher.**
3. **Provenance caution, stated plainly.** Lorem Ipsum seeded **15/16** in the
   final tournament and describe the module as vibecoded with known defects
   (*"it only considers throwing at places it can actually see"*). Their *rules*
   are worth taking; their *results* are not evidence of strength. Generalized
   Strokes Theorem independently reaching the same design is what makes this
   `documented` rather than anecdotal.

BUILDER HOOK — replace the destination rule in the launcher plank with a scored
`argmax` over passable tiles in range, starting with only the three
highest-confidence terms (**+** enemy-gunner lane, **+** distance to their core,
**−−−** adjacent to our core). Everything else can wait for a measurement.

Related: [[launcher-defensive-interception]] · [[blind-their-gun-with-their-own-body]] ·
[[displace-dont-kill]] · [[throw-into-prebuilt-cell]] · [[ratnapping-ignores-hp]]
