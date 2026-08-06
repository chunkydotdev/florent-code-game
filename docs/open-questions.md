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
      dead-end chain recoverable via `destroy()`'s in-transit refund, or lost once pushed
      off the chain's end?

## Strategy questions we can answer ourselves offline

- [ ] Is Sentinel-first actually better than Gunner-first? (see [strategy-notes.md](strategy-notes.md))
- [ ] What's the real payback period on a harvester once conveyor cost and builder-rounds are
      counted? At what chain length does a harvester stop being worth building?
- [ ] Does the "scout first, build later" scale-tax dodge beat building immediately?
- [ ] How much does map size change the right opening? Where's the crossover?
- [ ] Does `ct.destroy()` on obsolete buildings measurably cut later build costs?

## Platform / competition

- [ ] What are the **prize categories**? €20K is split among "category winners", so raw ladder
      rank may not be the only thing being rewarded — this could change what we optimise for.
- [ ] **Team size limits** — solo entry or do we need teammates? (`fcode team` and a
      `/team/join` route both exist, so teams are a first-class concept.)
- [ ] Qualification cutoff and dates for the Stockholm finals (top 16 qualify).
- [ ] **How does the ladder assign seats within a best-of-five?** Priority raised 2026-08-06:
      first mover has a measured ~78% edge on the 8×8 map even with a direction-neutral bot,
      so a series without seat alternation is partly a coin flip on tight maps.
- [ ] Is there a public ladder API worth polling for opponent tracking, or is `fcode ladder`
      the only interface?
- [ ] The competition **map pool** — how many maps, what size distribution? `fcode maps list`
      answers this once we're logged in, and it directly determines how much the small-map
      case matters. **Announced 2026-08-06: the pool has changed and stays hidden until the
      tournament, and other variables may be tweaked** — so census it at approval AND again
      at tournament start, and run the recalibration checklist in [runbook.md](runbook.md)
      both times.

## Blocked on account access

- [ ] Registration approval (`/application-pending` and `/application-denied` routes exist,
      so approval isn't automatic). Application submitted; awaiting the invitation as of
      2026-08-06. The moment it lands, run [runbook.md](runbook.md) §1 top to bottom.
