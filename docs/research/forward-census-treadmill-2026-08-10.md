# Forward-turret live census vs the cap — the treadmill hypothesis, tested

Research arm, 2026-08-10T01:06:59Z, git 38acfc2.
**Fixture: LADDER ONLY** (`.meta.json triggeredBy == "ladder"`). No arena battery
files. Subject: **our side** (team `379a5d80-…`), gunner + sentinel, forward =
`d2_enemy < d2_own` at the build tile.

---

## VERDICT: **REFUTED**

The prediction was: *Eir's live forward census sits AT or NEAR cap through the
late game; v102's sits systematically BELOW it.*

Both eras sit **far below cap, essentially always, and by the same amount.**

| era | band | rounds | mean live fwd census | median | **share of rounds ≥ cap (3)** | **share strictly < 3** | share at **0** |
|---|---|---:|---:|---:|---:|---:|---:|
| **v102** | r400+ | 11,397 | **0.243** | 0 | **0.3 %** | **99.7 %** | 78.2 % |
| **Eir** | r400+ | 170,354 | **0.248** | 0 | **3.3 %** | **96.7 %** | **87.2 %** |

**0.243 against 0.248.** The two censuses are indistinguishable, and Eir spends
*more* of its late game at **zero** forward turrets than v102 does. Eir's forward
arm did not stop because a live census was pinned at 3. In 96.7 % of Eir's
late-game rounds the gate — read as a live census — would have been wide open,
and Eir built 0.129 forward turrets per game-reaching-r400 anyway.

The rising v102 forward-build rate **needs a different explanation**, and this
number has now changed owners a third time. Two candidates are below, one of them
already measured.

---

## 1. The premise the test was built on is wrong at the source

**Neither bot tree caps forward emplacements on a live census.**

`bots/_v102thor/main.py` (identical in `_v94fb`, `_v92sp`, `_v91os`, `_v90ft`):

```
1407:        self.forward_guns = 0        # __init__, per Player instance
2610:        if self.forward_guns >= cap: return False      # _plan_siege gate
2748:            self.forward_guns += 1                     # _try_siege_build
```

`self.forward_guns` is written in exactly two places: `= 0` in `__init__` and
`+= 1` on a successful plant. **It is never decremented and never reset.**
`docs/game-model.md:27` — "The engine creates **one `Player` instance per unit**"
— makes it a **per-builder-bot monotone build budget**, not a census of anything
alive. Deaths already cannot refund it.

So the CONFIRMED branch's prescription — *"make the cap count builds rather than
live units (a cumulative budget deaths cannot refund)"* — **is already the
shipped design, in both eras, and has been since the Eir tree.**

The Loki tree ran the *opposite* way, deliberately. `doctrine.py:1205-1225` of
`_v126loki9` (and `_v118loki2b`) is explicit:

> `SLOT_FWD_GUN` is written ONLY as `read + 1` (raid.py) and is never
> decremented … it counts every forward sentinel we have EVER built, alive or
> dead. Three destroyed turrets close the forward-sentinel arm PERMANENTLY …
> **THE FIX IS A LIVE CENSUS, NOT A BIGGER NUMBER.**

LOKI-2b added `_live_fwd_guns()` / `LOKI2B_LIVE_CAP_ON` to convert the monotone
counter *into* a live census, because the monotone version locked the arm out.
The brief's "structurally identical, both live" reading has the two trees
backwards and inverted relative to each other.

## 2. The cap does not bind in v102 — measured, not argued

Forward-turret builds attributed to the placing builder bot (via
`Update.builderBuild{id, target}` matched to the turret's `placeEntity` in the
same round), over builders that placed ≥ 1 forward turret:

| era | builders | 1 | 2 | 3 | 4+ | share > 3 | max by one builder |
|---|---:|---:|---:|---:|---:|---:|---:|
| Eir | 669 | 306 | 237 | 119 | 7 | **1.0 %** | 15 |
| v102 | 288 | 196 | 45 | 19 | 28 | **9.7 %** | **68** |

Eir shows a **cliff at exactly 3** — 99.4 % of its builders stop at or below the
role-0 cap. That is the per-unit budget working. **v102 has no cliff**: its tail
runs 14, 19, 34, 36, 48, 48, 68 forward turrets from *single* builder bots
against a cap of 3.

Traced instance — `4ff97967-bce2-4227-ba8f-3dfe672d288c_game_2` (drumlin,
Powerpuff Girls, our seat A, cores at (5,5) and (18,18)):

- builder id **2569**, alive r675 → r876, placed **19** forward sentinels;
  builder **1153**, alive r264 → end, placed **48**.
- **18 sentinels were placed on the single tile (17,16)**, `d2_enemy = 5`, and
  **every one of them lived exactly 2 rounds** — r839/841/843/845/847/849/851/853
  /855/857/859/861/863/865, r873.

That is a genuine rebuild treadmill at the enemy core. It is not gated by a live
census, and it is not gated by the per-unit budget either — **in v102 neither
brake is touching it.** No uncapped turret-build path exists in the v102 source:
`build_gunner`/`build_sentinel` appear at only two sites, `_try_siege_build`
(capped by `forward_guns`) and `_try_counterbattery` (uncapped, but gated on a
threat within `HUNT_BAND_DSQ = 41` of `self.core`, which resolves to our *own*
core at main.py:2031-2034 — geometrically incompatible with a plant at
`d2_own = 265`). **Source and replay disagree.** See §6.

## 3. What actually separates the two eras: survival, not the cap

Turret lifetime, our side, ladder (censored = still alive at game end):

| era | where | n | died | mean life \| died | life ≥ 50 r | life ≥ 10 r | life ≤ 3 r |
|---|---|---:|---:|---:|---:|---:|---:|
| v102 | forward | 736 | 556 | **8.9 r** | **12.6 %** | 39.8 % | **37.1 %** |
| Eir | forward | 1,188 | 768 | **30.8 r** | **35.8 %** | 68.8 % | 8.2 % |
| v102 | home | 415 | 149 | 40.9 r | 62.2 % | 82.2 % | 2.9 % |
| Eir | home | 1,917 | 690 | 111.2 r | 76.5 % | 89.5 % | 2.9 % |

The brief's **survival** premise is right (12.6 % vs the quoted ~11.6 %). Eir's
forward turrets last **3.5x longer** and only 8.2 % die inside 3 rounds against
v102's 37.1 %. But a 2.8x survival difference cannot move a census that is at 0
in 78-87 % of rounds in *both* arms.

## 4. Full by-band tables

### Live forward-turret census (gunner + sentinel), our side, ladder

| era | band | games in band | rounds | mean | median | ≥ 3 | **< 3** | = 0 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| v102 | r0-149 | 185 | 25,246 | 0.287 | 0 | 0.1 % | **99.9 %** | 74.0 % |
| v102 | r150-249 | 124 | 8,731 | 0.529 | 0 | 0.1 % | **99.9 %** | 56.3 % |
| v102 | r250-399 | 59 | 5,883 | 0.438 | 0 | 1.0 % | **99.0 %** | 64.2 % |
| v102 | r400+ | 27 | 11,397 | 0.243 | 0 | 0.3 % | **99.7 %** | 78.2 % |
| Eir | r0-149 | 700 | 97,752 | 0.365 | 0 | 1.2 % | **98.8 %** | 71.6 % |
| Eir | r150-249 | 545 | 49,049 | 0.397 | 0 | 4.1 % | **95.9 %** | 75.9 % |
| Eir | r250-399 | 441 | 57,768 | 0.325 | 0 | 4.0 % | **96.0 %** | 81.3 % |
| Eir | r400+ | 341 | 170,354 | 0.248 | 0 | 3.3 % | **96.7 %** | 87.2 % |

Full distribution, share of rounds at each census value:

| era | band | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---:|---:|---:|---:|---:|---:|
| v102 | r400+ | 78.2 % | 19.7 % | 1.8 % | 0.3 % | — | — |
| Eir | r400+ | 87.2 % | 6.1 % | 3.4 % | 2.0 % | 0.8 % | 0.5 % |

Note Eir reaching **4 and 5** live forward turrets. A team-wide live cap of 3
could not produce that; a per-builder budget of 3 (or 2) trivially can, with two
builders each spending their own. Independent corroboration that the gate is
per-unit and cumulative, not a shared live census.

### Rebuild rate — both denominators (rule 7)

| era | band | fwd builds | **/ game in era** | / game reaching band | / 1k rounds in band |
|---|---|---:|---:|---:|---:|
| v102 | r0-149 | 242 | 1.308 | 1.308 | 9.586 |
| v102 | r150-249 | 136 | 0.735 | 1.097 | 15.577 |
| v102 | r250-399 | 139 | 0.751 | 2.356 | 23.627 |
| v102 | r400+ | 219 | 1.184 | **8.111** | 19.216 |
| Eir | r0-149 | 951 | 1.359 | 1.359 | 9.729 |
| Eir | r150-249 | 128 | 0.183 | 0.235 | 2.610 |
| Eir | r250-399 | 65 | 0.093 | 0.147 | 1.125 |
| Eir | r400+ | 44 | **0.063** | 0.129 | 0.258 |

The `/ game in era` column reproduces the brief's context table (Eir
1.36 / 0.18 / 0.09 / 0.063 vs the brief's 1.36 / 0.18 / 0.09 / 0.06 — exact),
which is the check that my decoder and the one that produced that table agree.
v102 reads ~10 % low against the brief purely because my denominator is 185
games, not join.tsv's 160 — see §5.

**The choice of denominator is doing real work here.** `/ game in era` shows a
19x v102:Eir gap at r400+; `/ 1k rounds actually played in the band` shows **74x**,
because only 27 of 185 v102 games reach r400 against 341 of 700 Eir games. The
v102 late game is *rare*, and the games that get there are exactly the ones
spraying turrets.

### Both terms of the share (rule 7): the home arm and the labour pool

| era | band | home census (mean live) | home builds / game-in-band | live builders (mean) | builder deaths / 1k rounds |
|---|---|---:|---:|---:|---:|
| v102 | r0-149 | 0.657 | 1.443 | 5.02 | 9.47 |
| v102 | r400+ | 1.586 | 1.704 | 4.49 | 5.44 |
| Eir | r0-149 | 0.788 | 1.590 | 4.76 | 12.24 |
| Eir | r400+ | **2.670** | 0.815 | **8.23** | 16.31 |

Eir's late game is not turret-poor — it holds **2.67 home turrets** against
v102's 1.59, on **8.2** live builders against v102's **4.5**. Eir moved its
emplacements home; v102 did not, and fields half the labour to do it with.

### Per-opponent spread (rule 6), r400+, share of rounds with census < 3

| era | opponent | games | rounds | mean census | < 3 | fwd builds / game |
|---|---|---:|---:|---:|---:|---:|
| v102 | Powerpuff Girls | 11 | 5,253 | 0.193 | 99.4 % | **13.09** |
| v102 | OopsGotYourElo | 3 | 1,580 | 0.269 | 100 % | 0.00 |
| v102 | CtrlAltDefeat | 3 | 684 | 0.282 | 100 % | 4.00 |
| v102 | Askar City | 2 | 831 | 0.116 | 100 % | 3.50 |
| Eir | Powerpuff Girls | 64 | 34,195 | 0.007 | 99.9 % | 0.03 |
| Eir | OopsGotYourElo | 42 | 23,413 | 0.362 | 94.8 % | 0.10 |
| Eir | Ouroboros | 34 | 16,486 | 0.001 | 100 % | 0.03 |
| Eir | Lunds Stallions | 29 | 12,236 | 0.248 | 97.4 % | 0.31 |

The below-cap share is **≥ 94.8 % against every opponent in both eras** — the
verdict does not turn on opponent mix. But the v102 r400+ *build rate* very much
does: **all 219 builds come from 15 distinct games** (of 27 reaching r400+), the
top 3 games carry 65 % of them, and 11 of the 27 games are one opponent. Treat
"v102 builds 8 forward turrets per late game" as a **tail statistic from ~15
games**, not a rate.

Geometry check — these are real siege plants, not a midline artefact of the
`d2_enemy < d2_own` label. v102 r400+ forward builds: median `d2_enemy` **5**
(≈ 2 tiles off the enemy core), median `d2_own` **196**, 93.2 % within
`d2 ≤ 32`. Eir's are the same shape (median `d2_enemy` 13). The forward label is
sound in both arms.

## 5. Population and denominator

- **Fixture: ladder only.** Seat and version read from each match's
  `replay_archive/*.meta.json` (`teamAId`/`teamBId` vs our team id) — the
  platform's own record. **Not** `join.tsv:our_team`, which is derived from
  `winnerSide + won` (`tools/corpus/build_corpus.py:145-147`) and whose
  "reconciliation" against the replay's own `winner` is tautological (TRAP 7).
- **v102 = 185 games; Eir era (v80/90/91/92/94) = 700 games**; 885 total, **0
  decode errors** (a partial run would have had no number).
- `join.tsv` carries **160** v102 and **700** Eir rows for the same versions.
  **860 of my 885 files are in `join.tsv`; 25 are not** — files whose match is
  absent from `ladder_games.tsv` or that `join.tsv` dropped. All 25 missing are
  v102 (185 − 160). My denominator is therefore a **superset**: every ladder game
  the archive holds for these versions, including ones the corpus join could not
  place. The Eir arm is identical under both definitions.
- Where both exist, **meta-derived seat and `join.our_team` agree on 860/860**.
  This is *reported*, not treated as validation — TRAP 7 says the two are not
  independent.

## 6. Instrument — shown to fail, and shown to decrement

Rule 1. `scratchpad/test_instrument.py` builds a synthetic `.replay26` by hand
(known answer) and runs four arms. All pass:

| arm | what it proves |
|---|---|
| normal | census rises on build, **falls to 0 on `removeEntity`** (1 decrement recorded), builder attribution correct |
| **rotation re-emit** | a second `placeEntity` for an existing gunner id is counted **0 times** as a build (TRAP 2) |
| **corruption: `removeEntity` dropped** | census **never falls** (0 decrements) and the sum diverges 6 vs 4 — the failure mode is detectable, so the alarm exists |
| seat swapped | every our-side counter goes to 0 — the seat variable is not inert |

On the real corpus the census **is observed to decrement**: 78 of 145 v102 games
with any forward turret (458 decrement events) and 340 of 507 Eir games (752
events). **2,375 v102 and 26,400 Eir gunner rotation re-emits were suppressed** —
had they been counted as builds, the census would have grown monotonically and
spuriously CONFIRMED the hypothesis. That is exactly the trap the brief flagged.

Cross-check against an independently written decoder: my forward gunner+sentinel
build totals vs `corpus/builds.tsv` (`side == FORWARD`, same seat) on the 631
shared files — **0 mismatches**.

Rule 4 (the statistic must come out different where it must): the same instrument
separates the eras by **74x on build rate** and **2.8x on turret survival**. It is
not blind to the difference between v102 and Eir; the census simply is not where
the difference lives.

## 7. What I could not measure

- **Which code path emitted each turret build.** The replay carries
  `builderBuild{id, target}`, so a build can be attributed to a *builder*, but
  there is no branch label — I cannot tell `_try_siege_build` from
  `_try_counterbattery` from the tape.
- **Whether `Player` instance state actually persists per unit on the platform
  runtime.** `docs/game-model.md:27` says one instance per unit; the v102 source
  caps at 3 per instance; the v102 replays show 68 from one builder id. **At
  least one of those three is wrong**, and this is the single highest-value
  unresolved item here. It is settleable in one local game — a stderr print of
  `id(self)` and `self.forward_guns` per unit per round — which I did not run
  (arena and bot edits are outside this brief's scope). **Do not act on any
  `forward_guns` reasoning until that runs.**
- **The Loki tree's census.** No Loki version has ladder games in this
  population, so `LOKI_FWD_GUN_CAP` was read from source only, never measured.
- **Cause of death** for forward turrets — lifetime is measured, the killer is
  not.
- **Eir-era role split.** The cap is 3 for `role_n == 0` and 2 otherwise; the
  replay does not carry role, so the per-builder distribution is reported against
  the looser bound of 3.

## 8. What this changes

1. **Do not build "make the cap cumulative".** It already is, in both eras. That
   change is a no-op at best.
2. **The Loki tree's LOKI-2b live-census conversion is the change that is
   already in flight, and this data does not support it either** — a live census
   would sit below 3 in 96-100 % of rounds regardless of era, so converting the
   Loki cap from monotone to live effectively *removes* the cap rather than
   retuning it. That may be intended; it should be stated as such.
3. **The real v102 anomaly is that its declared cap is being exceeded 22x**, and
   the real era difference is **forward-turret survival (12.6 % vs 35.8 % at 50
   rounds)** plus **half the live builder pool late**. Those are the two threads
   worth pulling.
4. **Re-quote the r400+ forward-build number with its concentration attached**:
   15 games, top 3 = 65 %, one opponent = 11 of 27 games.

---

Scripts (scratchpad, not committed): `fwd_census.py` (census pass),
`test_instrument.py` (four-arm instrument check), `lifetimes.py`, `analyse.py`.
