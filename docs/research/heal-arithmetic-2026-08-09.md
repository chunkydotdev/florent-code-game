# The defender wins attrition 2.2:1 — and we are the only ones playing defence with our titanium

**Research arm, 2026-08-09 (session 22).** From a Battlecode-postmortem sweep
(23 official PDFs, 2019-2026) that produced an arithmetic claim about **our**
ruleset, plus the corpus test of it.

**Version tag:** live **v90 "Heimdall 1 (launcher relight)"** = `bots/_v104latch`,
tree `2c6dbc17`, at-ship baseline **1556.83 @ 491, rank #31**. Corpus:
`corpus/econ.tsv` over all 3,831 archived replays, joined via `corpus/join.tsv`
(reconciled 1,155/1,155), 1,165 of our games. **Zero replay downloads.**

---

## 1. THE ARITHMETIC — every titanium-to-HP channel in the game

Straight from the ruleset, no measurement needed:

| channel | cost → effect | **HP per titanium** |
|---|---|---|
| **builder heal** | 1 Ti → **+4 HP**, to *all* friendly entities on the tile | **4.00** |
| builder attack | 2 Ti → 2 dmg | 1.00 |
| gunner shot | 4 ammo = 4 Ti → 7 dmg | 1.75 |
| sentinel shot | 10 ammo = 10 Ti → 18 dmg | 1.80 |

**Healing is 2.22x more titanium-efficient than the best damage source in the
game.** Two consequences, and the second is the one that bites:

1. **In a titanium-symmetric attrition race the defender wins**, always. Two
   equal economies, one spending on damage and one on repair, and the repairer
   comes out ahead by better than 2:1. **Neither side can kill the other by
   out-economising them** — you have to break the symmetry.
2. **Only turrets and launchers can remove a healer.** A builder attack damages
   *buildings only* — builder bots cannot attack enemy builder bots. So a screen
   of healing builders standing on a core is untouchable by anything except
   turret fire. **A bot that builds 0.2 turrets per game after r200 has no
   mechanism to clear a healing screen, which makes a healed core mathematically
   unkillable by attrition.**

The heal is even better than 4.00 in practice: it heals **all** friendly entities
on the target tile, so a stacked tile multiplies it.

> **AMENDMENT 2026-08-09 09:1x CEST (research arm, s23) — the stacking set is now
> pinned to engine source, not left qualitative.** The line above was written
> without saying *which* tiles can actually be stacked, which made it unusable.
> From `fcode/_types.py`:
>
> - `heal` (:578): *"Heal all friendly entities on an orthogonally adjacent tile
>   … by 4 HP. **If both a friendly builder bot and a friendly building are on the
>   target tile, both are healed.**"* Cost is 1 Ti for the tile, not per entity.
> - `is_tile_passable` (:345): a builder bot may stand on a tile only if it *"has
>   no building on it or has a **conveyor, splitter, or the allied core**"*.
>
> **So the stack is exactly one builder bot + one of {conveyor, splitter, allied
> core}, and the ceiling is 2 entities = 8.00 HP/Ti — not unbounded.** The
> defender's edge over the best damage source (1.80 HP/Ti) is therefore **4.4:1
> on a stacked tile**, against 2.2:1 on a bare one.
>
> **The load-bearing case is the core.** A friendly builder standing on a core
> footprint tile, healed by an adjacent builder, repairs the **core and the bot
> together for 1 Ti**. The core is 2×2, so up to four such tiles exist. This is a
> **home-defence** lever, which is the band the builder's 09:05 note measures as
> our one large advantage (+11.4 / +16.6 / +22.3pp over the field).
>
> Not yet measured: whether we ever actually do this, and whether the field does.
> `flow.tsv`/`econ.tsv` carry heal counts but not the target tile's occupancy, so
> this needs a decoder change and is **not** claimed as an observed behaviour —
> only as a verified rule. Found via tactics sweep 2 (topic 11), which flagged the
> 4.00 figure as possibly understated; it was, but only on this restricted set.

## 2. THE TEST — who actually spends their titanium on what

Per game, 1,165 of our archived ladder games:

```
                 heals   HP repaired    builder atks   ammo converted   dmg capacity
US               426.9      1,708           205.9          826.6 Ti        1,900
THEM             243.7        975           138.1        1,357.6 Ti        2,720

           damage capacity / HP repaired      US 1.11 : 1        THEM 2.79 : 1
```

**We heal 1.75x more than the field and buy 0.61x as much ammunition.** They
out-damage their own repair by nearly 3:1. **We barely break even.**

By band, the divergence widens exactly where our hazard dies:

| band | heals US/THEM | ammo Ti US/THEM |
|---|---|---|
| r0-150 | 86.7 / 68.2 | 291 / 388 |
| r150-200 | 26.6 / 19.9 | 57 / 99 |
| r200-300 | 49.5 / 32.2 | 83 / 176 |
| **r300+** | **264.1 / 123.5** | **394 / 694** |

At r300+ we heal **2.1x** the field and buy **0.57x** the ammunition.

## 3. WHY THIS EXPLAINS EVERYTHING WE MEASURED TODAY

This is the first hypothesis that accounts for **both halves** of our record
rather than just the failure:

- **Why we survive well.** Healing is the most efficient titanium in the game and
  we spend more of ours on it than anyone. Our r1000 share, our grind-pocket
  win rate, our low core-death rate late — all downstream of a genuinely optimal
  defensive conversion.
- **Why we cannot convert.** The same choice. We are winning the attrition race
  in the direction that does not end games, against opponents who spend theirs on
  the side that does.
- **Why the r150 cliff exists in five instruments at once.** Before r150 cores
  are unhealed and unscreened, so 1.00-1.80 HP/Ti damage is enough. After r150
  the screen is up and the arithmetic inverts. Raider survival 43 → 6 rounds,
  conversion ratio to 0.61, turret production to 0.2/game, ammo to a twelfth —
  these are not five problems. **They are one threshold being crossed.**
- **And our own lineage is named for it.** The bot family is *Eir* — the healing
  line. We optimised the defensive side of an asymmetry that already favoured
  defence.

## 4. THE FIELD LITERATURE SAYS THIS IS A KNOWN DESIGN TRAP

Not our discovery — Battlecode has hit it repeatedly:

- **XSquare (Java Best Waifu, 2020 champion):** *"Very often having the ability
  to 'heal' units make the games end in a deadlock (for instance in 2018 before
  the flying mages)."*
  [pdf](https://battlecode.org/assets/files/postmortem-2020-java-best-waifu.pdf)
- **5 Musketeers, 2022** hit the mirror image and named the fix: *"I saw replays
  where this would go on for a while, with soldiers just sitting at home waiting
  to be healed for over 1000 rounds… Even though the soldier needed healing, it
  was more advantageous for them to just go into the fight and do their best,
  even if it meant death. **To resolve these issues, I added a heal cap and
  timeout.**"*
  [pdf](https://battlecode.org/assets/files/postmortem-2022-5-musketeers.pdf)
- **Baby Ducks, 2021 champion** solved our exact symptom with an idle timer:
  units that see no enemy for 10 turns charge the enemy base. *"This greatly
  helped our ability to **turn an influence advantage into a unit advantage**,
  and push through defenses."*
  [link](http://web.mit.edu/agrebe/www/battlecode/21/index.html)
  > **⚠ UNVERIFIED ATTRIBUTION (2026-08-09, s23 quote audit).** This URL now returns
  > **HTTP 500** on both http and https, and `archive.org` was rate-limited (429), so
  > **I could not verify this quote or its attribution.** Worse, the third lane
  > established that the **sibling 2020 URL on the same site is a DIFFERENT team's
  > postmortem** (Battlegaode, zero Kryptonite hits) — so this URL family has a
  > demonstrated mis-attribution defect and cannot be trusted on authorship.
  > **Treat the quote and the "Baby Ducks / 2021 champion" attribution as
  > unconfirmed.** The claim is illustrative only; **§1's 4.00 HP/Ti arithmetic is
  > derived from our own ruleset and is unaffected.**
- **Four 2025 finalists independently** built a hard sink converting a hoarded
  resource into the binding one; confused measured **"70%+ win rate against my
  submission for qualifiers"** from it alone.

## 5. WHAT I AM **NOT** CLAIMING

**This does not say "heal less".** Healing is the most efficient titanium in the
game and our survival is real Elo — the grind pocket is 26-49% of our games. The
claim is narrower and it is a **ratio**, not a level:

> We are at 1.11 damage-capacity per HP-repaired; the field is at 2.79. Nothing
> here says which number is optimal. It says ours is an outlier in the direction
> that cannot close games, and that the outlier is a *spending choice*, not a
> resource shortage — **we deliver the same titanium as the field (452.9 vs 444.0
> stacks/game) and end r200-300 holding more of it.**

**The honest risk in acting on this:** we win 67% against the weak band, largely
by out-surviving it. A shift toward damage spends the thing that produces that.
The measurable question is not "does damage beat repair" but **"is our current
ratio past the point where more repair still buys wins?"** — and that is an
ablation, not an argument.

**Confounds I cannot remove.** Heal counts come from `builderHeal` events, which
do not carry how many entities were on the target tile, so "1,708 HP repaired" is
a floor, and it is a floor that flatters my own argument — a stacked heal repairs
more. Both sides are undercounted equally. Ammo *converted* is not ammo *spent*;
`ammo_end` shows both sides holding small balances (28-43), so conversion tracks
expenditure closely, but they are not identical. Attribution is our-games-only.

## 6. THE CHEAPEST DISCRIMINATOR — builder's lane

The literature hands us the exact instrument: **a heal cap and timeout**
(5 Musketeers) or an **idle-timer flip** (Baby Ducks), either one behind a flag,
measured on the **damage-capacity-to-repair ratio** as the mechanism metric —
not on net Elo, which cannot attribute.

Pre-registration that only the change can move: **does the r200-300 ratio rise
from 1.11 toward the field's 2.79, and does the r200-300 conversion ratio follow?**
If the ratio moves and conversion does not, this document is wrong and the
deficit is elsewhere. That is the same shape as the LOKI-3 pre-registration and
it can share its fixture.
