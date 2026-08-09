# Play the players: three measurements, two of which kill the tactic they were meant to support

**Research arm, 2026-08-09 (session 22).** Magnus's trickster tasking, axis B
(measured opponent habits). **Version tag:** live **v90 "Heimdall 1"** =
`bots/_v104latch`, tree `2c6dbc17`, baseline 1556.83 @ 491. Corpus: all 3,831
archived replays via `corpus/events.tsv` (222,483 joined build/death events) and
`corpus/throws.tsv`. **Zero replay downloads.**

---

## 1. OPENING DETERMINISM IS GEOMETRIC, NOT BEHAVIOURAL

Ranking every ore tile by distance from its owner's core, then asking which rank
each team actually builds its first harvester on:

```
first harvester    rank-0 (nearest ore)    THEM 42.9%    US 49.9%
                   top-3 nearest           THEM 81.1%    US 85.5%
                   chance (20.9 ore/map)                 14.3%
n = 1,084 THEM sides / 1,144 US sides
```

**Everyone opens on the nearest ore, us included.** My earlier per-opponent cut
showed Lunds and Powerpuff both modal on hive **(23,7)** and looked like a shared
habit — it is simply the nearest ore to the seat-B core.

**This is better than a tile book, not worse.** There is nothing to go stale when
an opponent ships a new version, no version stamp, no expiry — the target set is
derivable from map geometry alone. It is exactly the generic siting LOKI-4 was
already told to use, now with a measured hit rate.

## 2. **BUT PRE-EMPTIVE ORE DENIAL DIES ON A PINCER** — killed before the battery

```
harvester build rounds       p10 = 6    median = 66
ore-rank by band     r0-30     top-3 = 63-70%
                     r30-150   top-3 = 15-20%
                     r150+     top-3 =  9-15%   (rank>=4 is 82-86%)
```

**The opening tile is predictable but unreachable** — first harvesters land r2-13
and a builder cannot cross a 25x25 map in six rounds. **The late tiles are
reachable but unpredictable** — by r150 expansion is spread across rank 4+.
There is no window where both halves hold.

This kills only the **pre-emptive tile-book** version — the one I proposed and was
most enthusiastic about. **It does not touch LOKI-4's reactive denial** (barrier
an ore tile you are already adjacent to), which is probe-verified and unaffected.

## 3. THE ONE THING THAT SURVIVED, and it points at raiding rather than denial

```
harvesters built NEARER THE ENEMY CORE than their own:
  r0-30   THEM 3.7%      r30-150  13.1%      r150+  33.9%
  (US     1.2%                    17.8%             35.4%)
```

**By r150 a third of new harvesters are on the opponent's side of the map** — 20
Ti each, +5% scale, far from their defences, reachable. That is a target, not a
denial site, and it is the first late-game job I have found for our builders that
is not healing.

## 4. DISPLACEMENT IS WORTH ~6 ROUNDS — the kidnapper doctrine, priced

The builder asked, before committing a battery, how long a thrown builder takes
to resume. Measured from repeated exiles of the *same* bot id:

```
bots exiled at least twice:  2,468 of 3,755  (66% come back)
rounds between consecutive exiles of the same bot:
   p10 4    p25 4    MEDIAN 6    p75 8    p90 17
   back within  5 rounds: 46.4%
   back within 10 rounds: 82.3%
```

**A displaced enemy builder is back in launcher range in a median of six rounds.**
The hand-waved estimate was ~10; the true figure is 6, and 82% are back inside 10.

So the kidnapper is **cheap but small**: at ~22 exile throws per game against
Ouroboros, inverting the throw direction buys on the order of 100-200 enemy
unit-rounds per game, and the ceiling is bounded by the launcher's r²=26 radius
(~5 tiles), so reversing the sort key roughly doubles a six-round walk-back — it
does not create a new one. **It costs no ammo and the launcher acts anyway, so it
is close to free; it is just not a game-winner.**

**And we are not even the bigger bouncer**: in joined games we exile 10,519 times
to their 11,945 (**ratio 0.88**).

## 5. WHAT WOULD REFUTE EACH

- **§1** — if ore-rank concentration were an artifact of maps where the nearest
  ore is also the only reachable ore. Not tested; the chance baseline (14.3%) is
  computed per map from that map's own ore count, which controls for ore density
  but not for reachability.
- **§2** — if builder move speed or map traversal is faster than I assume. The
  pincer rests on "cannot cross the map in six rounds"; a launcher-assisted
  opening insertion would break that assumption and reopen the tactic.
- **§3** — if those contested-space harvesters are defended by turrets I have not
  counted. I measured position, not protection.
- **§4** — if re-exiled bots are a biased sample (a bot that comes back is by
  definition one that survived and chose to return). **This is a real selection
  effect: bots thrown once and never seen again contribute no gap.** The median
  of 6 is therefore a lower bound on "time to resume" for the population, and an
  accurate figure for the ones that do resume. It flatters the doctrine's critics
  slightly less than it looks.

## 6. LIMITS

Our-games-only (1,155 joined games); per-(opponent,map) cells run 1-13 games with
median 3, which is why §1 is reported pooled by rank rather than per opponent —
**no (opponent, map) cell reached 80% modal at n>=8, and I did not relax that
bar.** Round bands are game rounds. Harvester rank uses each map's decoded ore
set from `maps/*.map26`.
