---
tactic: Remember the tile, re-take it as DEFENCE — per-tile memory instead of a shipped table
source: https://battlecode.org/assets/files/postmortem-2025-confused.pdf
origin: Battlecode 2025 / confused
evidence: documented
transfers: partial
---

WHAT IT IS — Battlecode 2025's towers are immobile structures built on fixed map
sites, and confused's bot kept a **per-site memory of what had stood there**, so
that a destroyed structure was rebuilt as a *defensive* one rather than whatever
it had been:

> "Upon completing a tower, a soldier would mark it as a defense tower,
> regardless of its actual type. Then if this tower was destroyed, a soldier
> would come to it and see the mark and build a defense tower, and this
> implementation was able to build defense towers in previously attacked areas."

and then the correction that makes it work, which is the important half:

> "Eventually I changed it so that this would only happen if there were still
> [enemy units around], as defense towers were being overbuilt."

*(bracketed text: the sentence is split by a figure caption in the PDF —
"…if there were still 8 Figure 10: Tower marks enemy units around, as defense
towers were being overbuilt." The reconstruction is mine and is marked as such.)*

The same year, SPAARK record what a defensive structure planted on contested
ground is worth: "We lost center control, and they were able to build a defense
tower in the center and completely destroy us."

WHY IT MIGHT TRANSFER — **it is the form of "defend the tiles that get attacked"
that survives our own refutation.** `gunner-plant-tiles-are-not-enumerable`
killed a table learned *across games* (−3.0pp at shippable sizes). confused's
mark is learned **within the game, from an event that already happened on that
exact tile**, and re-applied to that tile. It makes no cross-game claim at all.

And we have the matching measurement. Of the 1,156 enemy plants that landed on a
tile we had built on first, **100% had one of our buildings die on that tile
between our build and their plant.** A tile where one of our buildings just
disappeared is a tile that gets taken. confused's rule says: mark it, and when it
comes free, take it back — as defence.

The gate matters as much as the rule. confused's uncorrected version overbuilt;
the fix was to require **enemies still present**. That maps directly onto our
cost-scale problem — gunners and sentinels scale **+20% each** — so an
unconditional rebuild loop is not merely wasteful here, it inflates every
subsequent turret we buy.

WHAT WOULD KILL IT — three, and the first is a hard limit on the evidence:

1. **We cannot tell, from the corpus, why our building on that tile died.** The
   `DEATH` row cannot distinguish an enemy kill from our own free `destroy()` —
   both emit `removeEntity`, and the research doc that found the 100% explicitly
   declines to choose between "they cleared our building" and "we removed it
   ourselves and they took the vacancy". If it is mostly the latter, this file is
   describing our own build churn, not an attack pattern. **In the live bot the
   ambiguity does not exist** — we know whether we called `destroy()` — so the
   rule is implementable even though the corpus cannot validate it.
2. **The tempo is slow.** Median **202 rounds** between our building dying on a
   tile and their plant landing on it. This is a grind, not a clear-and-plant
   exchange, so a rebuild rule races nothing and mostly just re-occupies ground.
3. Per-tile memory has to live somewhere. The 16-slot store cannot hold it, and
   per-unit `Player` state (which does persist — confirmed in `bots/_v100hf`) dies
   with the builder. The natural owner is the **core**, which is a single
   long-lived unit with a persistent instance and full r²=36 vision of its own
   surroundings — but the core cannot build, only spawn, so it would have to
   publish an intent through the store to a builder.

BUILDER HOOK — **the cheapest version needs no memory structure at all**, because
the physical world already stores the mark: an empty tile inside our band that we
previously built on *is* the mark, and we can see it.

> If a builder is orthogonally adjacent to an empty tile inside our home band,
> **and an enemy builder bot or enemy turret is currently in vision**, build a
> barrier there (3 Ti) rather than leaving it open.

That is confused's rule with her own correction applied, priced at the cheapest
legal object rather than a turret, and it dodges the +20% scale problem entirely
because barriers scale at **+1%**. It is also the only version of "pave the dead
ground" that the enumerability refutation left standing — recall its own
conclusion that "the 64.6% of plants on ground we never touch is the affordable
part" of covering the band.

Related: [[gunner-line-blinding]] · [[runtime-density-siting]] ·
[[spawn-smothering]] ·
[gunner plants are not enumerable](../gunner-plant-tiles-are-not-enumerable-2026-08-09.md)
