# Open questions

Things we don't know, with how we'd find out. Move an answer into
[game-model.md](game-model.md) once verified, and delete it from here.

Most of the original blocking questions were answered by the official docs on 2026-08-06.
What's left is mostly gaps in the published numbers and one real contradiction.

## Settled

- [x] ~~Do turrets fire by themselves, or must we call `ct.fire()`?~~ **You must call it.**
      Measured 2026-08-06 — see [game-model.md](game-model.md#turrets). The tutorial's
      "attack automatically" line is wrong.
- [x] ~~Starting titanium balance~~ — **500 Ti**, measured. Undocumented anywhere.
- [x] ~~Can we run matches locally without an account?~~ **Yes** — see
      [tooling.md](tooling.md); `.map26` maps are generatable offline.
- [x] ~~Why does the second mover always win on some maps?~~ **Two mechanisms, settled
      2026-08-06** with a direction-neutralised bot (`bots/probe_neutral`). (1) The seat
      wipeouts on mid20/small12 were **our own bot's absolute orientation** — above all the
      spawn scan reaching only the N/W sides of the Core's ring, so one seat spawned toward
      the map corner and the other toward the centre; the neutral bot plays those maps fair
      (mid20 0/32 → 17/32). Fixed for real in v3 (full-ring spawn). (2) A genuine
      **engine first-mover advantage remains on the 8×8 map** — seat A 78% [61%, 89%] even
      with the neutral bot. Unfixable bot-side; folded into game-model.md. Raises the
      priority of the "how does the ladder assign seats in a best-of-five" platform question.
- [x] ~~Why did seat A lose every single game on `jackpot`?~~ **Because a Core at (0,0)
      publishes its position into the comms store as two zeros, and every slot starts at 0,
      so its own builders read "no data" and never learn where home is — for the whole
      match.** Settled 2026-08-08: that team lays no trail conveyors, builds no sentinels, and
      delivers **exactly zero** titanium (measured 0 in 6 of 6 matches). Fixing it by
      publishing x+1/y+1 moves the map's mirror seat split from 0/48 to 22/48. Inherited from
      the organisers' shipped starter bot, so most of the field has it too — see
      [opponents.md](opponents.md). Full write-up in [strategy-log.md](strategy-log.md).
      A prior hypothesis — that `get_position()`'s NW-corner reference is not
      rotation-equivariant — was measured and **refuted**; it is a real asymmetry that turned
      out not to bind.
- [x] ~~Core spawn range: r²=2 or r²=8?~~ **Neither is a radius — spawnable tiles are
      exactly the 12-tile ring around the 2×2 footprint**, measured tile-by-tile
      (`bots/probe_spawn`). The two published numbers describe that same ring from different
      reference points. Now in game-model.md, including the trap that the tutorials' own
      spawn scan reaches only half the ring.

## Undocumented numbers

Everything previously listed here was answered by `docs/game-rules-builder-bot`,
`game-rules-conveyors`, `game-rules-other-buildings`, `game-rules-resources`, and
`game-rules-reference` — pages missed on the first scrape. All folded into
[game-model.md](game-model.md). What's left:

- [ ] Harvester ore depletion — do ore tiles ever run out, or is income indefinite?
      Nothing in the docs mentions depletion, which suggests indefinite, but it's untested.
- [ ] Does a stack pushed onto an **enemy** conveyor actually credit their balance? The docs
      say resources "can still be pushed onto an opposing team's conveyor network or core" —
      if that credits them, a misaimed chain is worse than no chain.
- [x] ~~What exactly does tiebreak #1 count — and when is produced titanium credited?~~
      **Delivered to the Core, and credited only then.** Measured 2026-08-06 with dead-end
      and no-conveyor probes (`bots/probe_credit`, `probe_credit_nc`): both give a balance
      slope of exactly passive-only 2.5/round and `titanium_collected` 0 over 990 rounds.
      The starter bot's numbers reconcile because its walking-trail conveyors evidently do
      deliver. Now in game-model.md. *Residual sub-question:* is a stack sitting in a
      dead-end chain recoverable via `destroy()`, or lost once pushed off the chain's end?
      **ANSWERED 2026-08-08 (s19): LOST. There is no in-transit refund** — destroying a
      loaded conveyor incinerates the stack (0 Ti in 191/191, positive control
      40,427/40,427). The sub-question was built on a false premise this doc inherited from
      game-model.md, now struck there too.

## Strategy questions we can answer ourselves offline

- [x] ~~Is Sentinel-first actually better than Gunner-first?~~ **Yes, decisively.** Measured
      2026-08-07: 68.4% [62.4%, 73.7%] vs v4 (Gunner-first), 256 matches, 24 `core_destroyed`
      appearing where the Gunner baseline had essentially none. See strategy-log.md (aug7).
- [ ] What's the real payback period on a harvester once conveyor cost and builder-rounds are
      counted? At what chain length does a harvester stop being worth building?
- [x] ~~Does the "scout first, build later" scale-tax dodge beat building immediately?~~
      **No, decisively.** Measured 2026-08-07: a 20-round build delay scored 8.3%
      [3.3%, 19.6%] vs building immediately, 48 matches. Harvester ROI (~8-12 round payback)
      dominates the scale-tax argument by a wide margin. See strategy-log.md.
- [ ] How much does map size change the right opening? Where's the crossover? **Partial
      negative result 2026-08-07:** lowering the small-map (<=150 tile) harvester-to-defense
      trigger from 3 to 1 was refuted, 35.4% [23.4%, 49.6%] vs the sentinel-first incumbent
      (strategy-log.md). Consistent with the scout-first discard just below -- economy-first
      looks robust across map size, at least via this lever. Untested: branching on something
      other than the harvester trigger (sentinel placement, spawn rate, MAX_BUILDERS).
- [ ] Does `ct.destroy()` on obsolete buildings measurably cut later build costs?
      **Mechanics half MEASURED 2026-08-07 (session-12 probe, replicated across builders):
      `destroy()` consumes NEITHER the action NOR the move and is unlimited per turn** —
      two destroys in one turn left acd=0/mcd=0 with build and move both still available;
      the follow-up build then took the action normally. The organisers' "free, no
      cooldown, unlimited" claim is confirmed against the engine. The Elo half (does a
      destroy doctrine pay?) is what remains — thread-10 spec + pave-facing bug hand-off
      in the research session's findings.
- [ ] **Why is seat A systematically favoured or punished on `archipelago`, `atoll`, `heart`
      and `lighthouse`?** This is now the biggest open question in the project, and it is worth
      several times what the jackpot bug was. Measured 2026-08-08 in mirror runs (identical
      bots, so a strength difference is excluded by construction) and reproduced in a
      480-match head-to-head: **archipelago seat A ~77-78%** (n=64+), **atoll ~28-31%**,
      **heart ~31%**, **lighthouse ~28%**. All four are far outside the interval, all four are
      terrain-symmetric maps, and **none of them is the (0,0) Core bug** — that one is
      jackpot-only and is now diagnosed. `fjordgate` (10×10, seat A ~69-75%) is probably the
      documented engine first-mover edge showing up at small size and is a separate story.
      Method that worked on jackpot and should be used here: stop looking at win rates, read
      the **per-team process metrics** in the end-of-match JSON (`titanium_collected`,
      `units`, `buildings`) across a dozen single matches, and look for a quantity that is
      *structurally* different rather than merely lower for one seat. Then instrument the
      one function that quantity flows through.
- [x] ~~What order do `get_nearby_tiles()` and `get_attackable_tiles()` return tiles in?~~
      **Row-major in absolute map coordinates, y then x, independent of the querying entity.**
      Measured 2026-08-08, now in [game-model.md](game-model.md). Consequence: our
      `_run_sentinel` takes the first occupied tile off its ray, so turrets facing N/NE/NW/W
      engage the **farthest** enemy on the line and E/SE/S/SW the **nearest** — an absolute
      orientation bias that breaks under rotation as well as reflection, on all 15 maps.
- [ ] **How many legal (position, facing) pairs does a builder actually have at the
      sentinel-build gate?** Raised by the 2026-08-07 aimed-sentinel discard, which was a
      perfect null (`core_destroyed` 17.2% vs a no-op control's 16.7% — no mechanism-level
      effect at all). The suspicion is that by the time a builder reaches dist²≤8 of the Core
      the surrounding tiles are already occupied by our own build-out, collapsing the choice
      to a single legal position — in which case *every* arc-scoring experiment is measuring
      nothing, and the real lever is where sentinels get built at all. Cheap to instrument
      (count candidates at the gate, print to stderr, aggregate over a few matches); do this
      **before** any further turret-placement work.
- [x] ~~**Do the conveyor chains our builders lay actually complete a path to the Core?**~~
      **Answered** (2026-08-08, `tools/replay_census.py`): often not. Roughly half of
      graph-connected harvesters are also facing-correct — conditional rate ~53% for the `ladder1`
      candidate and for `aug7`, against a field average of 68.4% — and `chain_dir == 0` implies
      zero titanium collected in every economically-decided game measured. Chains are worth
      completing; ours frequently do not complete.
- [ ] **Does the facing metric measure the right thing?** Two accepted facing changes in a row
      won on the harness while leaving the end-of-game conditional rate statistically unchanged
      (52.9% vs 53.1%), with the gain showing up as volume instead — +19% harvesters, +29%
      titanium. End-state `chain_dir` is a snapshot and cannot see **time-to-first-delivery**.
      Measure the round at which each team's first `distributeResources` into the Core fires,
      per replay; that is the number the wins are probably tracking.
- [ ] **Why does the `ladder1` candidate still show a 3× dangling-head spike at Chebyshev distance
      1-2 from the Core**, when its code inside that radius is byte-identical to `aug7`'s? The
      far-zone topology must be feeding the near zone differently. Unexplained, and it is the
      most likely place another 10 points of delivery is hiding.
- [ ] **What does a conveyor cost us per unit of delivered titanium?** On `hive` against
      `opp_v44` we finish with **125 buildings to their 16** while collecting **400 to their
      1,190**. Every walked tile lays a conveyor, at +1% category scale each, whether or not the
      trail will ever carry anything. A budget, a cap, or laying only on tiles that already
      connect to a harvester are all untested and all cheap.
- [ ] Does a trail conveyor ever face its *output* into an adjacent harvester (which would
      refuse that harvester's stack on that side)? The 99.6%-adjacency probe measured presence,
      not accept-side correctness.

## Platform / competition

- [x] ~~What are the **prize categories**?~~ **Raw Elo** (confirmed by Magnus 2026-08-06,
      post-approval). Nothing to redirect: ladder rating is the single optimisation target.
      Fractional-series scoring (a 5-0 moves rating ~2.5× a 3-2) means consistency across
      the whole 15-map rotation beats peak performance on a subset — which is exactly what
      the accept gate already selects for.
- [ ] **Team size limits** — solo entry or do we need teammates? (`fcode team` and a
      `/team/join` route both exist, so teams are a first-class concept.)
- [ ] Qualification cutoff and dates for the Stockholm finals (top 16 qualify).
- [ ] **How does the ladder assign seats within a best-of-five?** Priority raised 2026-08-06:
      first mover has a measured ~78% edge on the 8×8 map even with a direction-neutral bot,
      so a series without seat alternation is partly a coin flip on tight maps.
- [ ] Is there a public ladder API worth polling for opponent tracking, or is `fcode ladder`
      the only interface?
- [x] ~~The competition **map pool** — how many maps, what size distribution?~~ **Current
      rotation obtained 2026-08-06 (`maps/new-maps/`), and the rotation is reportedly
      WEEKLY.** Census (tile-exact parse): **14 maps, areas 100–676, median ~470** — only one
      truly small map (fjordgate 10×10, cores 4 apart) plus a 21×8 corridor (moonrise), so
      the small-map case is a minor slice this week. **All three symmetries appear** (8
      rotational, 3 horizontal-mirror, 3 vertical-mirror) — our invented pool was
      all-rotational, so mirror-map behaviour is newly load-bearing. **Wall density runs
      0.6%–30.8%** (five maps ≥14%, far wallier than our inventions — pathfinding and the
      Sentinel's wall-ignoring line matter more). `jackpot` has a literal corner Core at
      (0,0), where the full-ring spawn scan earns its keep. Weekly rotation means re-census +
      re-baseline weekly ([runbook.md](runbook.md) §2), and per-map tuning has a one-week
      shelf life.

## Blocked on account access

- [ ] Registration approval (`/application-pending` and `/application-denied` routes exist,
      so approval isn't automatic). Application submitted; awaiting the invitation as of
      2026-08-06. The moment it lands, run [runbook.md](runbook.md) §1 top to bottom.
