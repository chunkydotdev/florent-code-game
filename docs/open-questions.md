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

## Contradictions still unresolved

- [ ] **Core spawn range: r²=2 or r²=8?** `docs/game-rules-core` says spawn range r²=2
      ("adjacent ring, including diagonals") and every tutorial uses
      `get_nearby_tiles(dist_sq=2)`. `docs/agents-md` says the Core has "an action radius of
      sqrt(8)" used to decide where it may spawn. If it's really 8, the Core can spawn onto a
      wider ring than any tutorial uses — which matters for getting builders out past a
      blocked-in base. *Settle by:* iterating `get_nearby_tiles(dist_sq=8)` and logging which
      tiles return `can_spawn() == True`.

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
- [ ] What exactly does tiebreak #1 count? `game-rules-overview` says "titanium collected",
      `agents-md` says "titanium delivered to core". The match summary prints a "mined"
      figure. If it's *delivered*, an unrouted Harvester scores nothing at all.

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
- [ ] Is there a public ladder API worth polling for opponent tracking, or is `fcode ladder`
      the only interface?
- [ ] The competition **map pool** — how many maps, what size distribution? `fcode maps list`
      answers this once we're logged in, and it directly determines how much the small-map
      case matters.

## Blocked on account access

- [ ] Register / get approved on the platform (`/application-pending` and
      `/application-denied` routes exist, so approval isn't automatic).
- [ ] `pip install fcode` + `fcode login` + `fcode starter` — until this is done we can't run
      a single match, and every strategy question above stays theoretical.
