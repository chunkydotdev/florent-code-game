---
tactic: (A) NEGATIVE WITH AN INVERSION — no competitive AI in this sweep rolls back a partly-built route. Abandoned track is simply left on the map. Our engine gives us the primitive they lacked, and our ruleset punishes the leftovers harder
source: https://raw.githubusercontent.com/Zutty/ottd-noai-pathzilla/master/pathfinding/PathWrapper.nut
origin: PathZilla (Zutty), AdmiralAI, NoNoCAB, CluelessPlus, ChooChoo, WrightAI — OpenTTD NoAI; the negative is leg 1's grep over all seven repositories
evidence: documented
transfers: partial
---

WHAT IT IS — leg 1 grepped all seven OpenTTD AI codebases (192 `.nut` files) for
`rollback`, `transaction`, `atomic`, `all-or-nothing`, `partially built` and
neighbours, and reports **no matches**. There is no transactional route
construction, no demolish-on-partial-failure and no all-or-nothing build anywhere in
that ecosystem. **Three strategies exist instead, and all three keep what was
already laid.**

PathZilla's is the clearest: `BuildPath` **returns the tile where it broke**, and
the caller re-pathfinds from there:

> *"* Build the path specified by path as a road of type roadType. If there any"*

> *"* construction errors the method will re-try to a limited extent. If this also"*

> *"* fails the method will return non-zero. If the returned value is greater than"*

> *"* zero it indicates the tile just before which construction failed."*

> *"// If we failed, try to find the path from the point it went wrong"*

bounded by `PathZilla.MAX_REPATH_TRIES`. The other two are the dry-run-then-commit
of [`test-build-the-whole-route-before-laying-one-tile`](test-build-the-whole-route-before-laying-one-tile.md)
and the build-then-verify-and-patch of
[`verify-connectivity-after-building-not-only-before`](verify-connectivity-after-building-not-only-before.md).

**And the cost of leaving the residue is acknowledged in one place**, NoNoCAB's own
readme, on unreconcilable orphans: *"Note that roads, rail tracks and depots are not
removed in that case. If you are playing with infrastructure costs enabled, this
will affect NoNoCAB negatively."*

WHY THE INVERSION MATTERS MORE THAN THE NEGATIVE — against OUR ruleset specifically:

- **Leftover road in OpenTTD is dead weight. Leftover conveyor here is a CORK.** A
  conveyor pointing at empty ground does not merely waste 3 Ti — it holds a stack
  and **blocks everything upstream of it for the rest of the game**. The
  binding-tile cut prices the asymmetry: ~10 corked tiles hold ~100 Ti visibly while
  withholding **7,767 Ti of emission**, a ratio of about **1:78**. **The field's
  tolerance for abandoned infrastructure is safe in their games and expensive in
  ours.**
- **And we have the primitive they did not.** Our `destroy()` targets an allied
  building on an orthogonally adjacent tile, **costs no titanium, does not use the
  action cooldown, and is unlimited per turn.** The organisers' reference adds that
  it *"returns any resources currently in transit on that tile to your team's
  balance"*, and destroying an entity **removes its contribution to the cost scale**.
  **So rolling back a stub is free three ways: the stack comes back, the scale comes
  back, and it costs no turn.** No AI in this sweep had anything like that.
- **The consequence is a rule the field cannot supply and our ruleset argues for
  directly: a route attempt that cannot be completed should be UNDONE, not
  abandoned.** That is a genuine inversion of documented practice, and it is the
  clearest place in sweep 19 where the field's answer is wrong for us.

WHAT WOULD KILL IT —

- **⚠ The scale refund is unprobed on the timing that matters.** Sweep 17B already
  flagged this exact gap — *"whether `destroy()` updates scale within the same
  round"* — and marked it a builder probe rather than a library claim. **The
  free-three-ways argument above degrades to free-two-ways if the answer is no**,
  which is still positive but changes the sizing.
- **`destroy()` on a conveyor holding a stack refunds it — per the organisers' doc,
  which the project's own notes say has known errors.** The string verifies; the
  behaviour is unprobed. **Probe before relying on it.**
- **⚠ And the obvious hazard is real: a bot that destroys eagerly on a wrong
  diagnosis dismantles a working network faster than the enemy can.** The FLE paper
  observed exactly that in agents — *"the agents broke existing working structures
  due to incorrectly identifying the root-cause of problems"*. **`destroy()` being
  free is what makes this idea good and what makes it dangerous, and both follow
  from the same rule.**
- **The negative itself is leg 1's grep, not mine.** I verified the PathZilla
  strings first-hand; I did not re-run the seven-repository absence grep.

BUILDER HOOK — two probes, both cheap, and neither is a strategy change. **(1)** In
a throwaway bot: build a conveyor, read `get_scale_percent()`, `destroy()` it, read
`get_scale_percent()` again **in the same round**. That settles the sweep-17B
question for everyone. **(2)** Build a conveyor, feed it a stack, `destroy()` it,
and check `get_global_resources()` for the +10. **Then** — and only with a terminus
predicate you trust — let a builder destroy an adjacent friendly conveyor whose
forward walk terminates on empty ground and which has held the same stack for N
rounds. **Both conditions, not either.**
