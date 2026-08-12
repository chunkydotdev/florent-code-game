# LOKI-14 (v131) — launcher kidnap as crash-induction

**Prototype, PREPARED not shipped.** Tree copied from `bots/_v124loki8` (v102,
the live bot); `main.py` and `eco.py` are byte-identical to it. The only
behavioural change is the DESTINATION of a throw the incumbent already makes:
when our launcher picks up an adjacent ENEMY builder, LOKI-14 alternates
between a MAP-BORDER site (the crash bid) and an INTERIOR site (the within-leg
placebo, which must read ~0). One flag, `LOKI14_KIDNAP_ON`, in `doctrine.py` —
set it False and the destination ordering is v102's verbatim.

The mechanism, the evidence and the split rule are written out in full in the
`LOKI-14` comment block at the end of `bots/_v131loki14/doctrine.py`; the
primary is `docs/research/engine-source-crash-and-launcher-2026-08-10.md`.
Code lives in `raid.py`: `_kidnap_plan` / `_kidnap_done`.

**`PREREG.md` in this directory is INHERITED FROM `_v124loki8` and pre-registers
LOKI-8, not LOKI-14.** LOKI-14 has no pre-registration in this tree; that
belongs to whoever creates the leg.

---

# LOKI-2 (v117) — the committed opening

**LOKI-2 is LOKI-1 plus one flag, `LOKI2_RUSH_ON`.** Everything below this
section is LOKI-1's DESIGN.md unchanged, and it is still the doctrine.

Corpus, 1,269 real early Core kills (≤ r300): **99.3% are turret fire**, and
the sub-r80 recipe over 190 games is **3 turrets planted by r22** (p25 r11).
Specialists by median kill round: Banminary r52 (plants r17 at d²=18), Big O
r63 (plants r14), Team 48 r74, Cookie r88. We are the league's **#1 early
killer by volume** (309 early kills, 48 sub-r80) and slow and thin about it:
**1 turret per game against their 2–3, at d²=32 against Banminary's 18, median
kill r91 against r52**. Three Sentinels at 18 dmg / 2-round reload put ~28
rounds of fire through a 500 HP Core, through our own collar (the Sentinel
line ignores obstacles) and from outside Gunner range.

So LOKI-2 commits to the opening LOKI-1 already half-runs. Inside
`LOKI2_RUSH_RND = 60` and only there:

| gate | LOKI-1 | inside the window |
| --- | --- | --- |
| harvester prerequisite for a forward Sentinel | `LOKI_FWD_MIN_HARV = 2` | `LOKI2_RUSH_MIN_HARV = 0` |
| bank left after paying for one | `LOKI_FWD_TI_FLOOR = 40` | `LOKI2_RUSH_TI_FLOOR = 8` |
| seats that leave at once | seat 0 | `LOKI2_RUSH_SEATS = (0, 1)` |

`LOKI_FWD_GUN_CAP = 3` is untouched — 3 was already the specialists' number,
so the cap was never the delay. Past r60 the bot is LOKI-1 exactly. The
roster lift is an override at the point of use in `main.py`; `LOKI_ECO_SEATS`
is not mutated. Full reasoning is in the LOKI-2 block at the end of
`doctrine.py`.

Pre-registered metric: **time to Core kill**, not win rate.

---

# LOKI-1 (v105) — the collar

**Doctrine in one line: don't break the door, jam the lock.**

## What raises the kill rate

A builder heals +4 HP for 1 Ti from any of the **8 tiles orthogonally adjacent
to the enemy 2×2 footprint** — 0.25 Ti/HP against ~0.56 for any attacker. Net HP
to kill a Core is a stable 500–512 but the raw hits landed range 28 → 1206
(14 decoded games): the 43× spread *is* the defender's heal line. Those same 8
tiles are also the only tiles a conveyor can deliver into a Core from, and 8 of
its 12 spawn tiles. One chokepoint for healing, income and reinforcement.

A **barrier is 3 Ti / 30 HP** and bot-impassable. Breaking one costs 15 pecks at
2 Ti = **30 Ti, a 10:1 exchange**, and every round spent pecking is a round not
spent healing. A raider on one of the **4 diagonal ring tiles** is orthogonally
adjacent to exactly the two seats flanking it, so four corner raiders seal all
eight. Sealed, every point of damage we land is permanent.

Damage then comes from a **forward Sentinel** — forced, not preferred: barriers
block LOS so a Gunner ray would die on our own collar, while the Sentinel line
ignores obstacles and shoots *through* it. 18 dmg / 2-round reload = 6 HP/round
against a defender who can no longer repair.

## Re-aim after the mid-build evidence

Built first against "remove the r180 cutoff, target r200-300". That premise was
refuted mid-build (ablation 49.4%, n=180; 11,895 throws show median raider life
collapsing 43 → 6 rounds at r150; only 2.34% of r200+ throws ever land one
attack). What survived: of 528 raiders that *did* attack, 25 produced half of
all 40,114 attacks and **319 were on the winning team**. The scarce resource is
**survival at the destination**.

So the two are now separated (`raid.py`, `_raid_open`):

- **Cold insertion** — a fresh body walking at intact defences — is open only
  until `LOKI_COLD_INSERT_RND = 150`.
- **Foothold reinforcement** — any round a raider is still acting at the ring,
  published as a heartbeat in `SLOT_RAID_LIVE` — has **no cutoff**. That is
  exactly the state the winning 319 were in.

## Survival package (the answer to defender-exile)

Defensive disposal is ~70% of all launcher activity in the field, so a lone
raider beside a defended Core is food. Six answers, all in `raid.py`:

1. **Value outlives the body** — the first action after landing is a barrier;
   an exile does not un-build it.
2. **The collar is also cover** — barriers block LOS, so Gunner rays cannot
   reach a raider standing behind its own wall.
3. **Numbers** — 12 stations, deterministically preassigned by raid slot, so
   raiders arrive spread instead of one-at-a-time (the incumbent staged one).
4. **Site choice** — a station within d²≤2 of a visible enemy Launcher is
   scored down by `LOKI_EXILE_PENALTY`; a raider that detects a teleport bans
   that station and re-enters elsewhere instead of walking back into the pickup.
5. **Buddy heal** — +4 HP/1 Ti onto an adjacent wounded raider cancels a
   Gunner's 3.5 HP/round.
6. **A building, not a body** — the forward Sentinel keeps firing after every
   raider is dead.

The raider **never waits** for a launcher (the incumbent's `launchwait` role is
gone): it walks, and the ferry throws it forward only if the walk happens to
cross the pickup ring.

## Kept vs rebuilt

**Ported verbatim from `_v103split` (`eco.py`)** — harvester bootstrap, trunk
chain planner, pave trail, BFS nav, heal-seat reservation, siphon hygiene, chain
medic, multi-healer convergence; `doctrine.py` copied whole. **Rebuilt** — roles,
Core spawn/ammo policy, home defence, the whole raid layer. **Dropped** — every
per-map special case (hive/snowflake/nordkap/atoll), the siege planner, the
`launchwait` role and its four gates.

`raid.py` is ablatable: delete its four call sites in `main.py` and what remains
is a plain economy bot.

## Measured (local arena, `--tle 10`, both seat orderings)

**Matched vs-field pair, clean machine, 15 maps × 3 seeds, n=90 each:**

| leg | result | crashes |
| --- | --- | --- |
| `_v105loki1` vs `opp_v78` | **62.2%** [51.9, 71.5] — clears 50% | 0 / 28 |
| `_v103split` vs `opp_v78` | 56.7% [46.4, 66.4] — no verdict | 0 / 15 |

LOKI-1 is **+5.5 pts** on the incumbent against this proxy. Intervals overlap
heavily and the legs are unpaired, so this is "not worse, plausibly better" —
**not** a demonstrated improvement. One opponent only; the wider battery
(`opp_v72`, `opp_v63`, `opp_v50`) is the instrument that decides.

**Retracted:** an earlier revision of this file reported 48.3% vs `opp_v78` and
concluded LOKI-1 was ~12 pts *behind* the incumbent. Those legs (and the
61.7%/n=120 self-leg) were run while a second session was running its own
batteries on the same machine. Under `--tle 10` a unit's turn is truncated when
it overruns 10 ms, so arena results are **load-sensitive and CPU contention
silently degrades play without producing a crash**. Same pairing, same bot, clean
machine: 62.2%. Never measure while another battery is running.

Zero uncaught exceptions for LOKI-1 across every leg (~360 matches), and zero
CPU-guard trips observed in a full instrumented game.

## Known weak points

- The full 4-corner collar is a *model*, never observed holding. Measured games
  end with 1–3 barriers alive, not 8.
- Cold-insert seats are few before r150 (seat 0, then seat 3 after the harvester
  shell); "arriving in numbers" depends on a surplus bank that may come late.
- `LOKI_SURPLUS_TI`/`LOKI_RICH_TI` population lifts are unmeasured guesses.
- Barriers are +1% team cost scale each; 8 of them is +8% on everything after.
