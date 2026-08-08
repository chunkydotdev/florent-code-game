# Lunds Stallions: 0 wins in 17, and what the losing cells share

Research arm, 2026-08-08 s19. Corpus: 17 archived OpenSverige-vs-Lunds ladder
matches / 85 games, our v64–v81 vs their v37–v45. **Zero downloads** (archive
only). Live version at write time: v83 (`bots/_v97e11`, md5 56b9d178).

## Headline

**We have never beaten Lunds Stallions. 0 match wins in 17; game share 21-64 =
24.7%.** Match outcomes are bimodal — 9× "2-3" against 8× swept (0-5 or 1-4),
almost nothing between.

## What the framing got wrong (twice, both corrected here)

1. **`docs/opponents.md:1504`'s "6-4 as seat A vs 0-5 as seat B" does not
   reproduce.** That row is a 15-game unrated sweep from 08-07 and its seat
   split is a 5-game slice. Archive ladder data: **seat A 27.5% (11-29), seat B
   22.2% (10-35)** — a 5-point gap at n=85, i.e. noise, with whitewashes on both
   seats. The table is now marked stale in-repo.
2. **My own census over-claimed "seven (map, seat) zero-cells".** I fingerprinted
   maps by dimensions + core positions, which is **not unique**:

   | | dims | cores | ore | wall |
   |---|---|---|---|---|
   | heart | 28×20 | (7,9)/(19,9) | 28 | 122 |
   | eider | 28×20 | (7,9)/(19,9) | 32 | 22 |
   | snowflake | 26×26 | (5,5)/(19,19) | 32 | 70 |
   | archipelago | 26×26 | (5,5)/(19,19) | 38 | 208 |

   "heart seat B 0/4" was heart-B 0/2 **+ eider-B 0/2** — below the n≥3 bar, so
   **one of the seven cells does not exist**. And for four of the remaining six
   the *other* seat is also winless (atoll 0/7 map-wide, lighthouse 0/4, drumlin
   0/5, hive seat-A only). **Only moonrise has a real seat contrast** (A 2/4 vs
   B 0/6). These are mostly maps we lose on both seats, not seat cells.
   **Standing rule: map identity requires TILE CONTENT, not dimensions + cores.**

## H-A vs H-B: it is H-B — at least three mechanisms

Delivered titanium separates the six surviving zero-cells three ways:

| cell | n | our Ti | their Ti | games we out-deliver |
|---|---|---|---|---|
| hive A | 3 | **363** | 2,813 | 0/3 |
| moonrise B | 6 | 1,785 | 4,688 | 0/6 |
| drumlin B | 4 | 3,735 | 8,500 | 0/4 |
| lighthouse B | 3 | 3,437 | 4,710 | 0/3 |
| antler A | 3 | 2,530 | 3,060 | 1/3 |
| **atoll A** | 5 | **3,850** | **2,858** | **4/5** |

atoll A is the inverse of hive A: we win the economy 4/5 and lose the core 5/5.
No single mechanism spans both.

## H-C vs H-D: both, per cell

### THEIRS — moonrise (the clean natural experiment)

Their launcher throws a builder at round 3 in **6/6** of our seat-B games and in
**0/4** when we hold seat A, across 688–1000-round games. The obvious
explanation was **tested and refuted**: the mirror-equivalent landing tiles were
free at rounds 2/3/4 in every seat-A game, with two of their builders adjacent
to the launcher throughout. Their opening is otherwise perfectly mirror-symmetric
(launcher (8,4) ↔ (12,4) about x→20−x). **The trigger is absolutely oriented in
their code.** Same pattern on meander; inverted on fjordgate.
Downstream: enemy body in our spawn ring from r3 in 6/6 seat-B games vs r9–13 in
4/4 seat-A; first core damage r4–18 vs r13–34; our core dies 5/6 vs 1/4.

### OURS — hive, and it is the actionable item

`bots/_v97e11/main.py:2401-2405`, byte-identical from `_v64cbA` to the live head:

```python
hive_magazine = weapons and w == 25 and h == 25 and (p.x, p.y) in ((2, 20), (21, 3))
ammo_target   = 256 if hive_magazine else (32 if atoll_burst_magazine else (24 if under else AMMO_FLOOR))
```

In **3/3** hive games it converts **286–341 Ti into ammunition and fires 3–16
shots all game**, delivering 170 / 320 / 600 Ti against their 3,130 / 3,590 /
1,720. Harvesters: ours 2–3, theirs 8–11, from mirror-image geometry. Bank trace
(70ce8cb2 g5): r0 470 Ti → **r50: 4 Ti / 73 ammo** → r150+ pinned at 1–46 Ti with
the magazine held at 256. **We spend more titanium filling an unfired magazine
than we mine all game.**

Two aggravating facts (builder's, verified here at source):
- **Its arming is `weapons = ct.read_store(SLOT_HOME_GUN)` (:2361)** — the
  monotone counter the file itself documents as "a monotone count of turrets this
  team has ever built", never decremented, counting rubble and the saboteur's
  forward gun at the ENEMY core. So the gate is not conditioned on home defence
  existing at all.
- **The block contradicts its own comment three lines above** (:2394-2396):
  *"Keep only a small working magazine. Conversion is action-free, so a 60-round
  stockpile merely starves harvesters and counter-gunners."* The next statement
  sets **256** — over 4× the stockpile that sentence warns about, and it starves
  exactly what the sentence predicts.

Note hive also carries `hive_freeze` (see `hive-arm-positional`): **two of our
own gates stack on the same map.**

## Refuted H-C candidates (worth as much as the positives)

- **"Our heal line fails to arm in the losing cells."** REFUTED — first core-heal
  lands within 0–2 rounds of first core damage in **23/24** zero-cell games. The
  heal line runs; it loses the exchange.
- **"We never counterattack the siege turret."** REFUTED — we kill **41/105**
  enemy turrets that sit within d²≤13 of our core in zero cells (vs 34/65 in win
  cells).
- **"We never build a forward turret there."** NOT A DISCRIMINATOR — zero forward
  turrets in antler A and moonrise B, but also zero in **fjordgate A, which is
  3/3 wins**.

## Geometry: nothing shared

Zero-cell core-to-core d² spans 64–617; ore 8–30; wall density 0.6%–25%. Win
cells span the same ranges. **All 15 pool maps are symmetric**, so per-seat
geometry is identical by construction — measured. **No geometry feature can
explain a seat split**; it has to be turn order, our orientation, or theirs.

Residual, reported honestly: on the three vertical-mirror maps (eider/heart/
moonrise) we are 5/10 seat A vs 0/10 seat B, Fisher two-sided p=0.033 — but it
survives only under the map de-merge, spans 3 maps, and moonrise's proximate
cause is demonstrably their launcher. **Re-test on more data; not a finding.**

## Decoder traps found (both now standing)

1. **`UpdateHp.delta` is int32** — negatives arrive as 10-byte two's-complement
   varints and read naively come back as ~1.8e19, so **all damage silently
   vanishes**. The decode's first pass had zero core-damage events.
2. **Map identity needs tile content** (see above).

## Uncertainty

n is 3–6 per cell. Our versions (v64–v81) and theirs (v37–v45) both trend with
time. The moonrise seat contrast spans our v64–v81 on seat B and v67–v75 on seat
A, so it is **not** a version artefact; their launcher opening is invariant across
all their versions. The hive sample is v75/v76/v80 only (n=3) though the gate text
is version-stable. **Undetermined:** why their launcher declines to throw in one
orientation; whether the ammo drain is the sole cause of the hive collapse (needs
an ablation, arena is out of research scope); any mechanism for antler A or
drumlin B.
