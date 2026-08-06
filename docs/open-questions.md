# Open questions

Things we don't know, with how we'd find out. Move an answer into
[game-model.md](game-model.md) once verified, and delete it from here.

Most of the original blocking questions were answered by the official docs on 2026-08-06.
What's left is mostly gaps in the published numbers and one real contradiction.

## Contradictions in the official material

- [ ] **Do turrets fire by themselves, or must we call `ct.fire()`?**
  The turrets tutorial says they "attack automatically once built — no CPU time spent aiming
  or deciding when to fire." The rules doc says "like every other unit, each turret runs its
  own instance of your bot code once per round," and every tutorial code sample writes an
  explicit `_run_gunner` that calls `get_gunner_target()` / `can_fire()` / `fire()`.
  These can't both be right. Evidence favours "you must call `fire()`" — a Gunner with no
  code branch would make the ammo tutorial pointless.
  *How to settle it:* run a match with a Gunner that has no `GUNNER` branch at all and watch
  whether ammo drops. **Do this before designing anything around turret behaviour.**

## Undocumented numbers

The docs publish full stats for Core, Harvester, and all three turrets, but not these:

- [ ] Builder Bot **HP**, **vision radius²**, and **base spawn cost**
- [ ] **Base costs** for Conveyor, Splitter, Barrier (the `get_*_cost()` methods exist;
      the base values aren't published)
- [ ] Barrier **HP**
- [ ] **Cost-scale contribution** of everything except Harvester (+5%) and Gunner/Sentinel
      (+20%). What does spawning a Builder Bot add? A Conveyor? A Launcher? A Barrier?
      *How to find out:* read `get_scale_percent()` before and after one build of each type
      in a local match. Cheap and fully answerable offline.
- [ ] Conveyor and Splitter **HP** (matters for how many builder-fire hits cut a supply line)
- [ ] Harvester ore depletion — do ore tiles ever run out, or is income indefinite?

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
