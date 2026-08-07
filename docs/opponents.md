# Opponents

Patterns observed in other players' bots. The ladder is the real metagame — knowing what the
field does is often worth more than optimizing our bot in isolation.

For each opponent worth tracking:

- **Name / team:**
- **Ladder position when observed:**
- **Opening:** what they do in the first phase of a match
- **Signature behaviour:** the thing that makes them recognizable
- **Where they're strong:**
- **Where they're exploitable:** and whether we've actually tested the exploit
- **Our record against them:**

## Opponents observed (2026-08-06)

First real opponent data. Source: `fcode match list --mine --type ladder` (97 series / 485
games, spanning our submissions v1–v42 over roughly 16 hours) plus 8 individually decoded
replays (protobuf, see Metagame notes below for how) across 5 losing series. Series/game
counts below are exact (measured from `fcode match info`); openings and mechanisms are only
as solid as the replay sample noted for each — call-outs say explicitly where a "signature"
is one game's worth of evidence rather than a confirmed pattern.

### 1337

- **Name / team:** 1337 (Umar, Aditya Singh — University of Oulu)
- **Ladder position when observed:** #48 of 103, rating 1254.7 — the highest-rated team we
  play with any regularity.
- **Opening:** No fixed pattern found across 8 series. Sometimes economy-first (conveyor
  ~turn 9, harvester ~turn 13), sometimes a slower tech path. Replay `3d957a49` game 2
  (`jackpot`, loss, turn 199) shows: conveyor turn 9, harvester turn 13, then from turn 66
  onward a pivot into a mixed force — launcher turn 66, first of 4 gunners turn 76, sentinel
  turn 144.
- **Signature behaviour:** **If a game against 1337 is decided by `core_destroyed`, we lose
  it.** Measured across every game we've played them, both series sampled in depth and the
  other 7 read from `fcode match info`: **0W–17L** on `core_destroyed`, at turn counts
  from 188 to 737 — this is not a fast-rush thing, it's that core combat with them never
  goes our way, early or late. In the one game we decoded in full (jackpot, turn 199 loss),
  we actually had *more* harvesters alive than they did (3 vs 2) when our core died — so
  that specific loss wasn't an economy problem, it was a straight military-tech/combat one.
- **Where they're strong:** Core combat, whenever it happens, regardless of when.
- **Where they're exploitable:** We win the economy race against them more often than not —
  15W–5L on `titanium_collected` (20 games), 2W–0L on `titanium_stored`. Games that go the
  distance without core combat tend to favour us. Untested as a deliberate plan (inference
  from the aggregate, not something we've tried to play for).
- **Our record against them:** 3W–5L series (8 series), 18W–22L games. Losing matchup,
  concentrated almost entirely in the core-combat games.

### Cookie

- **Name / team:** Cookie
- **Ladder position when observed:** #56 of 103, rating 1053.6 — below us.
- **Opening:** In the games that end in a fast core kill: almost no economy (0–1 conveyors,
  1 harvester total across 2 replay-decoded games) and 1–2 sentinel turrets walked straight
  at our core starting turn 5. Confirmed via replay: `cookie_g1` (`antler`) — sentinel placed
  turn 5 at (6,11), one tile from our core at (6,12); `cookie_g2` (`hive`, a bigger map) —
  first sentinel turn 32, second turn 35.
- **Signature behaviour:** Once a sentinel is in range, our core takes exactly -18 damage
  roughly every 2 turns. Both kills we decoded took exactly 28 hits (-504 total) — see
  Metagame notes for the core-HP-constant finding this feeds. Time to kill scales with map
  size (turn 38 on the small `antler` map vs turn 61 on the larger `hive` map) but the
  mechanism is identical both times.
- **Where they're strong:** The rush, if it lands before our defenses are up.
- **Where they're exploitable:** This is close to a one-trick strategy. We are **11W–0L on
  `titanium_collected` against them** — we have never lost an economy-tiebreak game to
  Cookie — and their alive-unit counts in both games we lost show almost nothing besides the
  sentinels (1 harvester, ≤1 conveyor, no other structures). The entire deficit against them
  is the 1W–4L on `core_destroyed`. Untested: whether a defense that comes online earlier
  than our current "3+ harvesters" trigger would close this out entirely.
- **Our record against them:** 3W–1L series (won `b0a8e063`, `f00c7ea0`, `52573367`; lost
  `796458a8`). The lost series and the two other `core_destroyed` losses that happened
  *inside* otherwise-won series all show the same rush signature.

### ArjunWorks

- **Name / team:** ArjunWorks
- **Ladder position when observed:** outside our current ±5 ladder window; rated
  ~1267–1294 at the times we played them (above us).
- **Opening:** Economy-first, similar shape to our own opening (conveyor/harvester in the
  first few turns).
- **Signature behaviour:** Never contests our core — 0 of 10 games across both series ended
  in `core_destroyed`. Out-produces us instead: replay `19c24058` game 5 (`atoll`, full 1000
  turns) shows them running 2 harvesters to our 1, collecting almost exactly 2x our titanium
  (4960 vs 2480) by the end.
- **Where they're strong:** Sustained economy over a full-length game.
- **Where they're exploitable:** Not identified. Small sample.
- **Our record against them:** 0W–2L series, 2W–8L games. Small sample (2 series) — a lead,
  not a conclusion.

### Albert And Einstein

- **Name / team:** Albert And Einstein
- **Ladder position when observed:** outside our current ±5 ladder window; rated
  ~1168–1249 across four earlier series (mostly above us). One new series decoded in full at a
  considerably higher rating — **1306.8** vs our **1222.8** — 2026-08-06 ~12:47 UTC, match
  `81d83bb5` (**0–5 blowout loss**, ELO −12.21, our first loss to a higher-rated team of this
  size). Treat the two rating bands as possibly different bot versions on their side; see
  Signature behaviour.
- **Opening:** Two modes now confirmed, not one inconsistent mix as first thought. *Non-rush
  mode* (their other 4 lower-rated series, 20 games, not replay-decoded): normal economy,
  `core_destroyed` never happened once. *Rush mode*: first seen in one outlier game (replay
  `3209e6da` game 3, `lighthouse`, immediate launcher turn 1 + sentinel by turn 5) and
  originally written off as non-representative — **that caution turned out wrong.** All 5
  games of match `81d83bb5` (decoded in full) show the identical opening, turn-for-turn:
  **Builder Bot turn 0 → Launcher turn 1 → Sentinel(s) from turn 4–15.** The earlier "outlier"
  and this new series are the same signature; it just wasn't their norm at the lower rating
  band we'd mostly seen until now.
- **Signature behaviour — the launcher-assisted builder rush [measured, high value, changes
  our threat model]:** Their first Builder Bot (always entity id 3, spawned turn 0 next to
  their own Core) takes one normal cardinal step, then in the same or next turn jumps **6–8
  tiles in a single `moveBuilderBot` event** — impossible for ordinary movement (cardinal, 1
  tile/round) — landing roughly halfway or more across the map. This lines up exactly with
  their Launcher (built turn 1, ~4–5 tiles from *their own* Core in every game, never near
  ours) picking up their own scout builder and throwing it. The builder then walks the rest of
  the way normally and is camped **inside our Core's 12-tile spawn ring by turn 6–27**
  depending on map size — see the Metagame note below, this is a mechanic we hadn't seen used
  this way before. Once there, the *same single builder* (id 3 again, every game, never
  rotated or replaced) camps for most or all of the remaining game — turns-occupied / game
  length: **440/449 (98%) G1 `heart`, 628/641 (98%) G2 `nordkap`, 75/132 (57%) G3
  `snowflake`, 77/125 (62%) G4 `hive`, 163/169 (96%) G5 `lighthouse`.** In G1, G2, G5 it's one
  continuous streak from turn 6–9 to the Core's death; in G3/G4 (their two shortest games)
  it's genuinely "circling" — many short streaks in and out rather than one block. Builder
  investment is lean and identical every game: **exactly 4 builders, all spawned turns 0–3**,
  none built after. Turret count: **3 Sentinels in 3 of 5 games** (matches what was flagged
  from watching it live), 4 in G3, just 1 in G4 — all placed **1–4 tiles (manhattan) from our
  Core**, all within the first 15 turns except G3/G4's later top-ups (turns 27–72). No Gunners,
  ever.
  **Verdict — sentinels killed us, not the blocker, every single time:** all 5 games ended
  `core_destroyed` (0/5 ended on `titanium_collected`), so the blocker never got the chance to
  decide a game on the economic tiebreak it's positioned to win — the Core always died first.
  Net Core HP consumed to kill us was **502–512 in every game** (consistent with the existing
  ~504–506 estimate), but the *raw* damage-event count behind that varies hugely — see the Core
  HP metagame note below for why (short answer: we heal our own Core mid-siege). The blocker's
  clearest effect is indirect, not a tiebreak win: our own defense only triggers once we hit 3
  harvesters, and while G3/G5 show our first Sentinel landing within turns of hitting that
  gate, **G1 and G2 show a massive delay** — gate met ~turn 28 (G1) / ~turn 22 (G2), first
  Sentinel not until turn 436 (G1, +408 turns) / turn 81 (G2, +59 turns) — and **G4 never meets
  the gate at all** (stuck at 1 harvester the entire game, 0 Sentinels built, 0 healing events,
  the single enemy Sentinel landed all 28 of its hits clean, unmitigated). Whether that delay
  is *caused* by the blocker tying up builders versus our own build-order simply
  deprioritizing turrets isn't distinguished by this data — flagged as an open question, not a
  conclusion.
  **Also measured, worth its own line: our builders actively heal the Core under fire.**
  `ct.heal()` events (+4 HP each, matches the documented rate exactly) land throughout the
  siege in 4 of 5 games — G1: 297 heals offsetting 70% of incoming damage (1182 of 1692 raw),
  G2: 79% offset, G5: 52% offset, G3: only 4% (barely engaged), G4: 0% (never engaged, matches
  the "gate never opened" finding above). We still lose every time — Sentinel damage output
  outpaces our max heal rate over a long enough siege — but this is real, active defense our
  bot already performs that wasn't written down anywhere in our docs before this.
  **One more anomaly, flagged but not root-caused:** `titanium_collected` read exactly 0–0 in
  G1 and G4 despite both games building substantial economy (G1: 5 harvesters, 99 conveyors by
  the end; G4: 79 conveyors). It's not that nothing moved — `distributeResources` events (a
  resource-stack-hop counter, not previously decoded) fired 33 times in G1 and 12 in G4 — but
  nothing ever completed the trip to the Core. **This is not the ring blocker's doing:** we
  confirmed every Core-adjacent delivery tile (the 8 of the 12 ring tiles that touch the 2×2
  footprint orthogonally) got a conveyor built on it, early, in every single game including
  G1/G4, and the enemy builder was never on those specific tiles at the moment we built there.
  G2/G3/G5 (comparable or higher ring occupancy) delivered 4000/290/760 titanium just fine.
  Reads as a pre-existing dead-end-conveyor-chain fragility in **our own** bot, independent of
  this opponent — real, worth a dedicated look, but out of scope for an opponent-pattern file;
  belongs in strategy-log.md territory.
  **Where we do not lose ground: the economy race itself.** In every game with a nonzero
  reading, we collected as much or more titanium than they did (G2: 4000 vs 190, G3: 290 vs
  290 tied, G5: 760 vs 400) — including G1, where they never built a single harvester the
  entire 449-turn game and funded their whole rush off the 500 starting balance plus passive
  income alone. This loss is a tempo/military problem, not an economic one.
- **Where they're strong:** The rush, when they choose to run it — fast (turns 4–15 for first
  Sentinel(s)), close (1–4 tiles from our Core), and backed by a spawn-ring blocker that ties
  up our response for most or all of the game.
- **Where they're exploitable:** Their entire rush runs on 4 builders and, in G1 at least, zero
  economy on their side either — if our own defense actually landed on schedule when the
  3-harvester gate opens (see the G1/G2 400-turn/59-turn delay above), we might catch the
  Sentinels before the siege compounds. Untested as a deliberate change.
- **Our record against them:** 1W–5L series (6 total, +1 loss from `81d83bb5`), 9W–21L games
  (+0W–5L from this match). Losing matchup, now with a specific, repeatable mechanism
  identified at the higher rating band — not just "a broad-based gap" as first read.

### Troupe

- **Name / team:** Troupe (Rashid, Albin Sand, Olivia, Axel Segendorf — KTH)
- **Ladder position when observed:** #51 of 103, rating 1204.5. Largest sample of any
  opponent we've looked at: 8 series, 40 games.
- **Opening:** Standard economy opening, nothing distinctive found.
- **Signature behaviour:** None found — and this is a correction to our own first impression.
  The 2 most recent losses we originally picked for replay analysis (`dca5a663`, games on
  `saga` and `heart`) were both decided by the `harvesters` tiebreak, which looked like a
  pattern worth writing up. Checking the full 40-game history killed that idea: `harvesters`
  only decides 3 of their 40 games against us (1W–2L). The dominant win condition is
  `titanium_collected` (34 of 40 games), where we're actually slightly ahead (19W–15L).
- **Where they're strong:** Nothing consistent found.
- **Where they're exploitable:** Nothing consistent found — this is close to a coin-flip
  matchup.
- **Our record against them:** 4W–4L series, 20W–20L games, exactly even. Don't spend more
  time hunting for a pattern here without new data — small-sample pattern-matching on recent
  losses (see Signature behaviour) produced a false lead once already.

## Metagame notes

Trends across the field — what the top of the ladder is converging on, what stopped working,
what nobody is doing yet.

### Inherited defects worth knowing about (2026-08-07, pre-ladder)

We have no opponent observations yet — no account. But anything the **organisers' shipped
starter bot** gets wrong is a defect most of the field starts with, so it's metagame
information we can gather offline. Two confirmed so far:

1. **`_try_build_conveyor_toward_core` never fires.** Verified dead code in
   `bots/starter/main.py:286` — a grid-parity mistake, see
   [strategy-log.md](strategy-log.md). Harmless in practice for us because incidental
   trail-laying covers it (99.6% of harvesters get an adjacent conveyor anyway), but a bot
   that *doesn't* lay trail conveyors while walking would inherit the dead function and get
   **zero delivery** from its harvesters — and delivery is tiebreak #1. Any opponent whose
   harvesters look connected but whose `titanium_collected` stays near passive-only is
   probably sitting in exactly that hole.
2. **The unguarded `is_tile_empty()` out-of-bounds crash** (`starter` `_try_move`) — the v1
   finding. Still live in the shipped starter: 56 tracebacks in one 30-match probe run.
   Each one permanently deletes a unit. Opponents who never wrapped `run()` in `try/except`
   are losing units to this all game.

Both are worth checking for in replays once we can see other players' matches.

### Ladder telemetry and loss-mechanism findings (2026-08-06)

Sample: full ladder history via `fcode match list --mine --type ladder` at the time of
writing — 97 completed series / 485 games, spanning submissions v1–v42 played over ~16 hours
(2026-08-05 19:46 UTC to 2026-08-06 11:47 UTC). Plus 8 individual game replays decoded
byte-for-byte via a hand-rolled protobuf reader — the `.replay26` format is protobuf
(package `battlecode`, message `Replay`), and the exact schema is recoverable without a
`.proto` file or the platform's source: it's embedded as a protobufjs JSON descriptor inside
the fcode CLI's own bundled visualiser JS
(`fcode/data/visualiser/assets/main-*.js`, search for `nested:{battlecode:`). Everything
below is measured from `fcode` output or decoded replay bytes unless marked "inference."

**Win condition is where the story is, not overall record.** Breaking down all 485 games by
`winCondition`:

| win condition | our record | win rate |
|---|---|---|
| `core_destroyed` | 15W–74L | 17% |
| `harvesters` (tiebreak 2) | 13W–26L | 33% |
| `titanium_collected` (tiebreak 1) | 164W–158L | 51% |
| `titanium_stored` | 7W–8L | 47% |
| `error` (opponent didn't compile) | 20W–0L | 100% |

We're close to break-even on the economy tiebreak, and the `error` bucket is entirely one
opponent (below) — but `core_destroyed` is a rout in the other direction, and it's not a
small bucket (89 games, more than harvesters and titanium_stored combined). This matches the
per-opponent numbers above: 1337 (0W–17L on `core_destroyed`) and Cookie (1W–4L) both beat us
specifically by reaching our core, not by outproducing us.

**Harvester count, not stored titanium, decides the `harvesters` tiebreak.** In both Troupe
replays that hit this tiebreak (`saga` and `heart` games of match `dca5a663`), we had *more*
stored titanium than Troupe (2426 vs 101 in the `heart` game) but *fewer* harvesters alive (1
vs 3), and lost both times. Oddly, `resourcesCollected`/`titaniumCollected` read 0–0 for both
sides in those two specific games — inference: possibly that field only gets populated when
`titanium_collected` is the condition that actually decides the game; not confirmed against
game source.

**Core HP looks like a fixed constant: ~504–506, in steps of exactly -18 per hit.** Every
core kill we decoded in detail — Cookie x2, Albert And Einstein x1, plus our one win over
Albert And Einstein where we did the killing — landed in exactly 28 hits of -18 damage each,
total -504 (one read -506, likely rounding/an edge case). Time-to-kill varies hugely by map
size and opponent aggression (38 turns on the small `antler` map, 320 turns on `atoll` in the
one core kill we scored ourselves), but the per-hit damage and total core HP look constant
across every map and opponent we checked. Not verified against game source — inferred purely
from replay damage logs, so treat "504–506" as an estimate, not a spec.

**The `error` win condition is entirely one broken opponent, not general instability.** All
20 `error`-decided wins, across all 4 matches with a non-null `errorMessage`, are against
**arsonist duck** (matches `f2fbfb76`, `9216594c`, `fb6400af`, `48807d12`), whose submission
fails to compile: `Bot A failed compilation: Bot compilation failed: <bot>/main.py:1:
expected an indented block after class definition on line 1`. This is a different thing from
the "Inherited defects" `is_tile_empty()` crash theory above — it's a non-starter (the bot
never runs at all), not a mid-game crash. Separately: we found **zero** games with a non-null
`resignMessage` (0 of 485) and **zero** `Traceback`/`Exception`/timeout (`tled`) flags in
`botOutput` events across the 8 replays we decoded in full. No evidence either side crashed
mid-game in anything we looked at directly.

**The map pool rotated mid-session — most historical per-map data is now stale.**
`fcode maps list` confirms the live pool is exactly these 15: antler, archipelago, atoll,
drumlin, eider, fjordgate, heart, hive, jackpot, lighthouse, meander, moonrise, nordkap,
saga, snowflake. Our 97-match history actually touched 33 distinct maps — 18 of them
(aurora, bridge, crossfire, duel, fjord, longship, pinch, quarry, runestone, showdown,
skerry, sprint, strait, string, sweden, twins, vase, vault) haven't appeared since
~2026-08-06 09:21 UTC and are presumably retired from rotation. Only 3 of the current 15
(atoll, hive, jackpot) were in rotation from the start of our history; the other 12 all
first appear between 09:27 and 11:08 UTC the same day. **Any per-map win rate computed over
the full 97-match history mixes in a map pool that no longer exists.** Restricting to games
after the rotation (2026-08-06 09:25 UTC onward — 15 series, 75 games, all on current-pool
maps) gives the actionable table:

| map | record | win rate |
|---|---|---|
| saga | 2W–8L | 20% |
| heart | 2W–3L | 40% |
| antler | 3W–3L | 50% |
| archipelago | 3W–3L | 50% |
| snowflake | 4W–3L | 57% |
| hive | 5W–3L | 62% |
| lighthouse | 3W–2L | 60% |
| fjordgate | 2W–1L | 67% |
| nordkap | 2W–1L | 67% |
| drumlin | 1W–1L | 50% (n=2) |
| atoll | 3W–1L | 75% |
| meander | 3W–1L | 75% |
| moonrise | 3W–1L | 75% |
| jackpot | 6W–1L | 86% |
| eider | 1W–0L | n=1 |

`saga` stands out — worst win rate of any current-pool map, and with 10 games it's not a
tiny sample. Everything else is within normal variance for n=1–8 and shouldn't be over-read
yet.

**Rating trend: mixed, depending on the window.** The team started at 1500 (fresh team,
created 2026-08-05 18:58 UTC) and sits at 1186.17 as of 2026-08-06 11:51 UTC — a steady
decline across the full history (first-third-of-matches average rating 1371, last-third
average 1211). But the most recent 15 series (the post-rotation window, the only one
comparable to our current map pool) are **9W–6L**, and the last 10 completed series are
**6W–4L** — both raw-record-positive. The rating-weighted view over that same last-15 window
is close to flat (-11.4 net): the wins were mostly against lower-rated opponents (arsonist
duck x2, worth +0.2 each) while the single costliest result was a **loss to Cookie**
(-16.26, the largest single swing in that window) — expensive precisely because Cookie is
rated below us. Net read: recent play is winning more often than losing, but not yet
climbing, because losses are costing more than wins are worth.

**`fcode status`'s "Last 10" figure does not match `fcode match list`.** `fcode status`
reported `recent_record: {wins: 3, losses: 7}` (checked 2026-08-06 11:51:24 UTC).
Reconstructing the actual last 10 completed ladder series from `fcode match list --mine
--type ladder --json`, sorted by `completedAt`, cross-checked by `createdAt` and again at
the individual-game level, gives **6W–4L** every time — not 3W–7L, confirmed 3 independent
ways, not a sorting artifact. We scanned every contiguous 10-match window in the full
97-match history for one that actually produces 3W–7L: the closest matches are from the
*middle* of the day (roughly 2026-08-05 22:00–23:30 UTC and 2026-08-06 01:00–03:00 UTC),
nowhere near the real most-recent matches. The `rating` field in that same `status` response
does match the true latest match exactly (1186.1729... = the last match's `ratingBBefore` +
its `eloDelta`), so this isn't a fully stale snapshot — specifically `recent_record` looks
like it's computed on a lagging or differently-scoped window. Worth a sanity check before
trusting that number for anything.

**Submission version churn: "v40" itself has one data point.** The active submission is v40
("aug7-sentinel-economy", uploaded 2026-08-06T11:18:34Z per `fcode status`), but the team
ran 42 distinct submission versions in the same ~16-hour window, switching every few matches
— evidently several people testing concurrently and re-activating earlier versions (v21
reappears at 11:19:53 after v22–v38 had already played; v41/v42 both post-date v40's upload
timestamp but aren't the active submission now). **v40 specifically has played exactly one
ladder series so far** (`1018bf11`, a 3-2 win over Leviathan, completed
2026-08-06T11:47:47Z). None of the per-opponent write-ups above are v40-specific — the 6
losing series we sampled were played by v21, v26, v32, v35, v36, and v38. Everything in this
note describes the team's ladder run and bot lineage broadly, not v40's individual track
record, because v40 doesn't have one yet.

### Unrated scouting: Pivot and StarTrekker (2026-08-06)

Separate sample, not pooled with the ladder numbers above — unrated matches don't move
rating and the opponent selection isn't random. `fcode match list --mine --type unrated`
shows 70 unrated matches for our team as of this writing: 63 against **Pivot** (#1 on the
ladder, rating 1946.7, all 63 losses — 0W–63L, spanning our v21 through v43) and single
matches against StarTrekker, Besvikomat (rated 1789), The Flotte Experience (x4, rated
1752), and Jacobs Code. We did not trigger any of these — `fcode match unrated` is a write
command outside this pass's scope — we only read the results via `fcode match list`/`match
info`/`match replay`. The volume against Pivot specifically (63 near-identical 0-5/1-4
losses across 20+ bot versions) doesn't read as deliberate scouting; one or two samples
already say everything the other 61 do.

Decoded one v40 game against each of Pivot and StarTrekker (both unrated, both single-game
samples — treat accordingly):

- **vs Pivot** (match `91d77721`, `snowflake`, core_destroyed turn 179, loss): Pivot ran 12
  harvesters and 39 conveyors to our 2 harvesters / 23 conveyors, collecting 3170 titanium to
  our 810. They built no sentinels or launchers at all — their whole offense was 17 gunners
  (first one turn 80) plus a barrier (turn 45), and once they started hitting our core at
  turn 104 they finished it in 179-104=75 turns via sustained gunner fire (176 hits, much
  higher hit-frequency than the sentinel-siege pattern seen elsewhere). Their harvester count
  (12, from only 7 ever-built builder bots) is the single biggest number in this entire
  investigation — worth treating as a rough ceiling estimate for what "good" economy scaling
  looks like on this game.
- **vs StarTrekker** (match `eb72ce59`, `lighthouse`, titanium_collected, loss): much closer
  — we had 3 harvesters / 49 conveyors and collected 4940 to their 4 harvesters / 36
  conveyors (181 ever-built, so a lot of churn) and 7330 collected. We're competitive here,
  not blown out, but still behind on the same economy axis.
### The (0,0) Core bug — confirmed for the starter lineage, and it is the field's problem too

A claim reached this file mid-session and was correctly refused for lack of evidence. The
evidence exists; it was measured locally the same day, and the refusal's counter-example turns
out to be about a different bot. Recording both halves, because the *shape* of the mistake is
instructive.

**The bug (measured, local, `docs/strategy-log.md` 2026-08-08):** every comms-store slot starts
at 0 and holds non-negative integers, so 0 doubles as "unwritten". The organisers' shipped
starter bot publishes the Core position as raw coordinates and reads it back behind
`if x > 0 or y > 0` (`bots/starter/main.py:230`). A Core at exactly **(0, 0)** — `jackpot`'s
team-A seat, the only such Core in the 15-map rotation — therefore reads as "no data" to its own
builders for the whole match. Everything gated on knowing where home is stops: no trail
conveyors (the only thing that delivers titanium), no turrets, no returning home.

**Direct measurement, not inference:** `starter` vs `starter` on `jackpot` leaves seat A with
`titanium_collected` **0**, `units` **0**, `buildings` **1** — the bare Core. Our own aug7
lineage: `titanium_collected` exactly **0** in 6 of 6 matches, and seat A **0 for 104** across
three bot generations in mirror arena runs. Fixing the guard moves that map's mirror seat split
from 0/48 to 22/48.

**Why the counter-example did not refute it:** replay `3d957a49` game 2 has our team as A on
`jackpot` with 31 conveyors and 950 titanium collected — but that game was submission **v32**,
a teammate's bot, not the starter lineage. Our team ran 42 submission versions that day from
several people; a per-replay observation is only evidence about the version that played it.
(Note also that 950 collected on jackpot is low — a healthy team collects ~4950 there.)

**Metagame consequence, and it is worth real money:** any opponent descended from the shipped
starter without fixing this guard **forfeits `jackpot` whenever they draw seat A**. Check it in
any replay where an opponent is team A on a map with a Core at the origin: if their
`titanium_collected` is ~0, or their final balance is near passive-only (500 + 2.5/round), they
have it. Worth checking specifically for **Pivot** — if the #1 team does *not* have it, how they
publish the Core position tells us what a fixed bot looks like.

### Launcher-assisted builder rush — a mechanic we hadn't seen used this way (2026-08-06)

Measured in full across all 5 games of rated match `81d83bb5` (Albert And Einstein, rated
1306.8 — full numbers under their opponent entry above). Their first Builder Bot makes one
normal cardinal step, then jumps 6–8 tiles in a single `moveBuilderBot` event — impossible for
ordinary movement — matching a Launcher built turn 1 next to *their own* Core picking up and
throwing their own scout builder toward us. It then walks the rest of the way and is camped
inside our Core's 12-tile spawn ring by turn 6–27, often for the rest of the game (96–98% of
all turns in 3 of the 5 games, one continuous streak from turn ~8 to Core death in those three).
**This defeats the "a large map buys us time" assumption for how fast an enemy builder can
reach our base.** The mechanic itself is already documented in game-model.md (Launcher: pick up
an adjacent Builder Bot, throw it within range) but we'd only ever considered it for combat
utility — sabotage, denial, repositioning under fire — never as a turn-1 rush-delivery tool for
a scout/blocker. Worth checking any future opponent that opens with a turn-1 Launcher built
near *their own* Core (not ours) for the same pattern. So far this is one series against one
team — flagged for pattern-watching across the rest of the field, not yet claimed as universal.

### Core HP "fixed constant" note revisited — only holds when nobody is healing (2026-08-06)

The `81d83bb5` series (Albert And Einstein, see above) complicates the earlier "every core kill
lands in exactly 28 hits of −18, total −504" finding from the 2026-08-06 ladder-telemetry note.
Net HP consumed to kill our Core across all 5 games of that series was still tightly banded
(−510, −510, −502, −504, −512 — consistent with the ~504–506 estimate), but the *raw* count of
damage events behind that ranged from 28 (game 4) to 136 (game 2) — because our own builders
were actively healing the Core (`ct.heal()`, +4 HP each) in 4 of the 5 games, offsetting
anywhere from 4% to 79% of incoming damage before eventually losing anyway. The clean "28 hits
of −18" pattern holds only in the *unhealed* case — reconfirmed here in game 4, which shows
zero heal events and exactly 28×−18 = −504. **Net Core HP-to-kill looks like the real constant;
raw hit count does not, once healing is in play** — don't use hit count alone to estimate how
long a siege lasted or how many turrets were involved without checking for interleaved heals.

### Ladder sweep (2026-08-06, ~13:16 UTC)

Fresh `fcode match list --mine --type ladder --json` / `--type unrated --json` pull, diffed
against the previous sweep's cutoff (last completed match at the time of the notes above:
2026-08-06T11:47:47Z rated / 2026-08-06T12:17:45Z unrated).

**8 new rated series** completed since, in order: TKB (W 4–1, opp rated 998.6), Cookie (W 4–1,
opp 1050.4), Cookie again (W 4–1, opp 1046.8), Troupe (W 4–1, opp 1214.5), **Kleos** (W 5–0, opp
1238.3 — new opponent name, not previously logged here, flagging the name only, no write-up
yet), **Albert And Einstein** (L 0–5, opp 1306.8 — match `81d83bb5`, the subject of this
update), vjg (W 4–1, opp 1072.7), Leviathan (W 4–1, opp 1159.0). Net effect: the two wins
immediately following the Albert And Einstein blowout (vjg, then Leviathan) recovered almost
exactly the rating the blowout cost (1222.8 before that loss → 1221.2 now, three series later).

**3 new unrated matches:** Pivot (L 0–5, `9436bd69` — consistent with the existing 63-loss
pattern, now 64 of 64), sporks (L 0–5, new name, single sample, not investigated), not adgato
(L 0–5, new name, single sample, not investigated).

**Named watchlist, checked as requested:**
- **Pivot** (#1, ~1947) — +1 unrated loss as above, nothing new in the pattern.
- **HTTP 418** (~1713) — **zero matches against them so far**, rated or unrated. Presumably
  outside pairing range on the rated ladder (they're ~1713, we're ~1221); unclear why they
  haven't turned up in unrated scouting either given other high-rated teams have (Pivot,
  Besvikomat 1789, The Flotte Experience 1752).
- **StarTrekker** (~1207) — unrated count unchanged (still the single game already decoded,
  match `eb72ce59`). But the *rated* ladder list shows **7 StarTrekker series** in the current
  100-match window that hadn't been called out as a group before (separate from the one
  unrated sample in the "Unrated scouting" note above) — not decoded, flagging for a future
  pass, not analyzed here.
- **1337** (~1248) — unchanged at 8 series in the current 100-match window, matches the
  existing write-up exactly. Nothing new.

**Mid-sweep note:** the active submission changed while this sweep was running — from **v40**
("aug7-sentinel-economy", the version that played the `81d83bb5` match this whole update is
about) to **v44** ("florent-v58", uploaded by x3r0 at 2026-08-06T13:00:45Z). Everything dated
2026-08-06 in this file up to and including this sweep describes v40's play; results from here
on reflect a different, newer bot.

Fresh `fcode status` snapshot, captured 2026-08-06 13:16:55 UTC (`date -u`): rating **1221.23**,
rank **#50 of 103**, **105** matches played, last-10 record **5W–5L** (per `status`; see the
earlier note in this file on why that specific figure has been unreliable before — not
re-verified this pass).

### florent-v58 (`bots/opp_v44`) — full source read, not a replay inference (2026-08-06)

The sweep above logged v44/"florent-v58" (x3r0, uploaded 13:00:45Z) becoming our active
submission. This entry is a source read of that same bot — `bots/opp_v44/main.py` (1312
lines) plus its author's earlier `bots/opp_v39/main.py` (845 lines) for a diff — done because
it just beat our own `bots/aug7` **40.8% [32.5%, 49.8%] over 120 matches, 38 `core_destroyed`,
0 crashes either side**, and is now the activation bar. `meta.json`: their own 378-game
acceptance suite (21 maps × 3 seeds × 3 opponents × both sides) scored 376W, **349 core_kills
(92%)**, 0 tracebacks, 0 TLEs.

**Mechanism catalogue, vs what `bots/aug7` does today:**

- **No blanket `try/except` in `run()` at all** (`_core`/`_builder`/`_turret`/`_launcher`
  dispatch directly, line 182) — the opposite of aug7's unconditional wrap. Robustness instead
  comes from bounds-checking every position inline before every engine call
  (`0 <= bp.x < w and 0 <= bp.y < h`, repeated at every call site rather than factored into a
  helper) plus four narrow, targeted `try/except` blocks exactly where the vision-raise trap
  bites: BFS neighbor-tile inspection (lines 877–892), a buildings-iteration guard
  (line 820–833), and the turret target-priority scan (1145–1170). No `get_cpu_time_elapsed()`
  call anywhere — no CPU guard at all, yet 0 TLEs on their own suite.
- **Exact per-map database.** `CORE_PAIRS`/`MAP_CODES` (lines 43–84, 21 map signatures each)
  hardcode the enemy Core's exact position and the full wall/ore grid (packed 3-per-char,
  decoded once by `known_map_for()`, line 98) for every map they recognize — sidestepping the
  rotation-vs-mirror trap this project's own game-model.md documents (6 of 15 live maps are
  actually mirror-symmetric) by memorizing ground truth instead of assuming an invariant.
  Falls back to the naive `Position(w-2-x, h-2-y)` rotational guess (`enemy_core_for()`,
  line 87) only for an unrecognized map. This is the root of most of what follows.
- **Deliberate conveyor chains, not incidental trail-laying.** `_link_path()`/
  `_build_next_link()` (801–946) run a real BFS — multi-source reverse BFS from every
  Core-input tile on a known map, forward BFS from the harvester on an unknown one — to plan
  an exact route from each harvester to the Core, then execute it waypoint-by-waypoint. A
  secondary opportunistic-paving system (`_move`, 1102–1123) mirrors aug7's own mechanism as a
  supplement for builders not currently on a link errand, so both systems run at once.
- **Economy is capped and staged, not open-ended.** `ECO_CAP = 8` hard-caps harvesters
  (aug7 has no cap); builder spawning is staged in three tiers keyed to economic milestones
  (`EARLY_BUILDERS=4` before the first harvester, +1 more while saving for a Launcher, 8 after)
  and throttled by an explicit `LAUNCHER_RESERVE = 80` Ti savings reserve the Core won't spend
  through until a Launcher exists (`_core`, 280–291) — aug7 has no concept of reserving Ti for
  anything beyond its next spawn.
- **Role caste assigned at builder spawn** (`_builder`, 366–378): builder #0 → "defend"
  (bootstraps the first harvester + its conveyor chain + the Launcher single-handedly); next
  up to 4 → "expand" (economy, statically partitioned across the known ore list by builder
  index on a known map, `_pick`, 969–990, so builders never race the same deposit); the rest →
  "saboteur" (walk to the enemy Core, `fire()` it directly once adjacent, plant a forward
  Gunner) or "launchwait" (large maps: stage near home for the Launcher). **Offense is a fixed
  fraction of the population from birth, not a threshold-triggered global switch** — aug7's
  entire population runs identical logic with zero role differentiation and zero offense.
- **The Core builds its own defense directly**, no builder required nearby: up to 3 emergency
  Sentinels the instant a threat is detected on larger maps (246–260), and up to 12 home
  Gunners once a Launcher exists (262–278, note: *not* gated on `under` — a standing garrison,
  not purely reactive). aug7's Core only ever spawns builders and tops up ammo; 100% of its
  turret construction depends on a builder bot happening to be within `distance_squared <= 18`
  of the Core when the harvester threshold trips (`_try_build_sentinel`, aug7:437-439) — a
  single point of failure v44 doesn't have.
- **Turret targeting is a full priority scan, not first-hit.** `_turret()` (1125–1193) scans
  every tile off `get_attackable_tiles()` and fires at the single highest-value target by an
  explicit table — `CORE:0, SENTINEL:1, GUNNER:2, BUILDER_BOT:3, LAUNCHER:4, HARVESTER:5,
  CONVEYOR/SPLITTER:6, BARRIER:7` (1158–1164) — orientation-independent by construction, and
  notably not just the geometric "nearest" fix game-model.md proposes for aug7's bug, but a
  strictly better *value*-based one. Gunners try the engine's `get_gunner_target()` helper
  first (1130–1131, gated to Gunners only — see v39 diff below) and `rotate()` toward the
  nearest visible enemy when idle (1185–1193); Sentinels never rotate (matches the engine
  rule). Compare aug7's `_run_sentinel` (627–646): first tile off `get_attackable_tiles()`,
  unconditionally — the orientation bug game-model.md documents.
- **Launcher use aug7 has zero equivalent of** — aug7 never builds one (confirmed: no
  `EntityType.LAUNCHER` anywhere in `bots/aug7/main.py`). `_launcher()` (1195–1312) runs a
  claim/heartbeat protocol (`SLOT_LAUNCH_ID`/`_RND`) to elect one waiting builder, throws it at
  pre-tiered `drop_sites` adjacent to the enemy Core, and — new in v44 — leapfrogs it partway
  (`advance` fallback, 1292–1312) when the full distance exceeds throw range (r²=26),
  closing the gap over several throws on maps wider than one hop (most of them: throw radius
  ≈5 tiles, maps run to 30×30). An ACK slot (`SLOT_LAUNCHED_ID`, 420–425) tells the thrown
  builder it arrived so it doesn't try to walk itself home. The Launcher is also repurposed
  defensively: it grabs and exiles enemy Builder Bots that wander adjacent (either-team
  pickup is a documented engine rule, game-model.md).
- **No `ct.destroy()` / `self_destruct()` anywhere in either bot** — confirmed absent in
  `opp_v44`, `opp_v39`, and `aug7` alike. Nobody in this comparison does active cost-scale
  management by tearing down obsolete buildings; that's a real gap on both sides, not a v44
  advantage.
- **Comms store: 14 of 16 slots active** (vs aug7's 4). Notably a leader-election-with-lease
  pattern for the Launcher claim (self-heals if the claimant dies or two builders race, since
  the Launcher only ever throws the bot whose id exactly matches the currently-stored claim),
  and a monotonic harvester-count ratchet (`_sync_harvesters`, 319–334: `if live >
  read_store(...)`, line 331) that only ever raises the shared count — fixed from v39's `!=`
  check (line 206), which could let a builder with partial vision undercount and corrupt the
  shared total downward.
- **Checked specifically for the two bugs this project's docs flag as costing whole games —
  both absent.** (1) The **(0,0) Core store bug**: `pack_pos`/`unpack_pos` (116–123) use the
  same `+1` offset scheme as our own fix, and `unpack_pos` additionally treats the raw
  sentinel `0` as "no data" explicitly (`if not val: return None`) — confirmed byte-identical
  in `opp_v39` too, so this bot never had it, at least not since v39. (2) The **first-tile
  orientation bug**: fixed, and via a value-priority scan rather than the geometric-nearest
  fix game-model.md suggests (previous bullet).
- **Does it scout?** No dedicated scout role. Reconnaissance is a side effect of
  saboteur/launchwait builders' offensive routing, plus a spiral expanding-radius search
  pattern around the Core for the unknown-map ore fallback (`_pick`, 996–1001) — a more
  systematic sweep than aug7's uniform-random map-wide teleport target
  (`_pick_target` step 4, aug7:604-606).

**v39 → v44, the most important lessons, in order of how much downstream code depends on
them:** (1) the exact per-map database is the headline addition — static ore partitioning,
BFS pathing (`_bfs_direction`, new in v44, 1003–1085, replacing v39's pure greedy
`p.cardinal_direction_to`), and BFS conveyor planning are all downstream of having it.
(2) The Launcher choreography was hardened from "works sometimes" to reliable: the
claim/heartbeat + ACK handshake replaced pure-proximity reselection (which could "steal" the
economy builder mid-transit, per v44's own comment at 421-422), and the multi-hop `advance`
fallback means a throw beyond one hop's range now makes progress instead of v39's Launcher
silently never firing on any map wider than the throw radius. (3) Small, precise, evidence-
grade bug fixes in the same spirit as this project's own strategy-log: a stray `return`
immediately after `convert_ammo()` that wasted the Core's otherwise-free spawn turn every
time ammo topped up (v39:160-161 vs v44:238-241, with an explicit comment citing the fix);
Sentinels calling the Gunner-only `get_gunner_target()` unconditionally (v39:747, no type
guard, vs v44:1130-1131, gated); and the harvester-ratchet monotonicity fix above. The home
Gunner cap also rose 5→12 and dropped its `under`-attack gate — a shift from reactive to
standing garrison.

**Gunners vs. Sentinels — not a contradiction of our own Sentinel-first result.** Sentinel is
still the *first*, most reflexive defensive response (Core builds one the instant a threat is
detected, even pre-Launcher). Gunner is predominantly used where Sentinel's advantages don't
apply: forward-planted adjacent to the *enemy* Core by saboteurs (range stops mattering at
point-blank) and as a cheap, massable *volume* addition once flush (cap 12) layered on top of
the Sentinel layer, not instead of it. Their v41–43 names ("ammo-gunner", "gunner-deadzone")
read as exactly this kind of placement/ammo tuning arc, not a static-defender A/B against
Sentinel.

**Ranked adoptable changes for `bots/aug7/main.py`, most valuable first:**

1. **Fix `_run_sentinel`'s targeting** (aug7:627-646): replace the first-hit
   `for tile in get_attackable_tiles(): ... return` with a full scan tracking the
   single best target by a priority table, matching v44:1145-1171. One function, ~15 lines,
   touches nothing else. Caveat for honesty: our own strategy-log found *zero* suboptimal
   sentinel-targeting events across 625 captured self-play firings, so the isolated win-rate
   value is unproven and may be small against a passive field — but it's free, strictly
   correct, and more likely to matter against an opponent as multi-unit-aggressive as v44.
2. **Give the Core its own threat signal and let it build a defensive Sentinel directly on
   its own ring**, independent of any builder being nearby — new store slot + ~15 lines in
   `_run_core`, modeled on v44:246-260/300-309. Removes aug7's single point of failure (no
   builder within dist²≤18 of Core when the harvester threshold trips = no defense).
3. **Track the enemy Core position at all.** aug7 has no equivalent of `self.enemy` /
   `SLOT_ENEMY_CORE` anywhere in the file — confirmed by grep, the word "enemy" appears only
   in comments. Add the naive rotational guess broadcast on a new offset-safe slot (mirror
   `pack_pos`'s `+1`), overwritten with ground truth on first sighting — v39's much simpler
   original version, not even the full 21-map table. Cheap, purely additive, and a
   prerequisite for #4 and for aiming home-Sentinel facing at the real enemy direction instead
   of just "away from our own Core."
4. **Minimum-viable offense**: once the economy threshold is met, redirect a small fixed
   fraction of newly spawned builders (e.g. every 5th) to walk toward the tracked enemy Core
   instead of continuing to hunt ore, and `fire()` any adjacent enemy building en route
   (Core preferred) — a scoped slice of v44's saboteur role, sized like this project's past
   single-swap experiments (e.g. Sentinel-first). It is the smallest change that gives aug7
   any core-kill capability at all, which today is exactly zero.
5. **Adaptive ammo buffer** (raise the target when under attack) — depends on #2/#3's threat
   signal; a ~3-line change once that signal exists. This is our own strategy-notes.md's
   "adaptive ammo" open item (it explicitly calls the fixed buffer wasteful in quiet phases
   and starved in fights) — v44 already implements it (`ammo_target = 60 if under else
   AMMO_FLOOR`, 233).
6. **Structural, not a single change — flagged honestly rather than oversold.** (a) The full
   BFS conveyor-chain planner (`_link_path`/`_build_next_link`, ~150 lines, stateful
   per-builder queue): high plausible economic value, but a genuine subsystem. (b) The exact
   per-map database: we already hold the raw ingredients (`maps/*.map26`, 15 files locally,
   already census-parsed once per game-model.md's wall-density table), so a Core-position-only
   table (6 ints × 15 maps) is a realistic scoped follow-up — but the full terrain grid plus
   the BFS pathing/ore-partition machinery built on top of it is a multi-part rewrite, not a
   patch. (c) The Launcher + role-caste + claim/heartbeat/ACK choreography in full: this is
   most of `opp_v44`'s file, and the actual explanation for its core-kill rate (below).
   Adopting it means writing a comparable subsystem, not editing aug7.

**Best explanation for the 38 `core_destroyed` outcomes against aug7:** aug7 has *no* code
path that produces a core kill unless an enemy happens to walk into a home Sentinel's line —
no enemy-location tracking, no unit ever moves toward the enemy, no direct-fire sabotage, no
forward turret placement, no Launcher. `opp_v44` has at least three independent, redundant
paths engineered specifically to produce one (forward Gunners planted at the enemy Core's
doorstep, bypassing Sentinel's range advantage entirely; direct low-cost `fire()` chip damage
from saboteurs once adjacent; Launcher-driven multi-hop insertion that skips most of the
walk), layered on top of three independent home-defense mechanisms (Core-direct emergency
Sentinels, a 12-cap Core-direct Gunner garrison, instant all-hands response to melee threats
near the Core) that a purely economic, non-scouting opponent's incidental wandering was never
going to punch through. Given aug7's 40.8% overall score, the parsimonious read is that
nearly all 38 core-kills are `opp_v44` finishing an unaware, undefended-in-depth aug7 Core —
a structural mismatch in offensive capability, not 38 close fights that could have gone either
way mechanically.

**Follow-up, same day — is it a rush? Timing analysis against the Albert-And-Einstein pattern
above.** Magnus flagged the launcher-assisted builder rush (Albert And Einstein entry, this
file: Launcher turn 1 next to *their own* Core, scout thrown 6-8 tiles, camped in our ring by
turn 6-27, first of 3-4 Sentinels turn 4-15) as the *common* ladder opening, not one team's
quirk, and asked whether `opp_v44` conforms to it. It does not — timings below are estimated
from spawn/movement/gating constants in the source, not measured (no match run).

- **Commitment to offense has no single trigger — role is assigned at spawn** (`_builder`,
  366-378), splitting the population from birth: builder #0 → "defend"; on a small map
  (`mw*mh<=220`) role_n 3+ → "saboteur" *immediately*, no economy gate on the role itself; on a
  large map role_n 5+ → "launchwait" (stages near home, doesn't walk yet) until the Launcher
  throws it, or until `rnd>=70 and no Launcher yet and role_n!=5` (438, the role_n==5 primary
  candidate gets extra patience), or unconditionally by `rnd>=180` (440). But the
  offense-*delivery* mechanisms are economy-gated: a forward Gunner needs the saboteur within
  d²≤64 of the enemy Core plus ammo≥4 (615-619); the **Launcher itself cannot be built before
  `harv >= ECO_NEED` (4)** (`_defend`, 682, unreachable until the "defend" builder's own
  first-harvester link chain is already finished, 675-682 sequential `elif`s) — a genuine
  multi-harvester economy milestone, categorically different from Albert-And-Einstein's turn-1
  Launcher next to their own Core. Spawning itself is cheap and fast early (500 starting Ti
  comfortably covers the first 4 builders even under +20%/build cost-scaling, and the
  `can_spend_spawn` reserve check at 287 is trivially satisfied that early), so builders 0-3
  are plausibly all spawned by round ~3-4 — but that only sets *when a saboteur exists*, not
  when it can hit anything. **Best-case estimate: small-map saboteur reaches an 8-tile band of
  the enemy Core roughly round 15-35** (spawn ~4 + cardinal walk); **large-map Launcher-assisted
  insertion is gated behind harv>=4, unlikely before roughly round 20-30 even optimistically.**
  Both are roughly an order of magnitude slower than the measured turn 4-15 first-Sentinel
  benchmark.
- **Forward turrets at the enemy Core: yes, but Gunner-only and un-clustered.**
  `_saboteur()` (615-629) plants a Gunner, never a Sentinel, on any adjacent tile to wherever
  the saboteur happens to be once within d²≤64 (8 tiles) of the enemy Core, facing it
  (`bp.direction_to(ec)`, 624). No fixed count — scales with however many saboteurs survive to
  get there, not a designed "3-4." Looser radius than the observed "1-4 tiles" pattern.
- **Launcher rush-delivery: yes, same mechanism, different schedule.** `_launcher()`'s primary
  path (1277-1312) throws the claimed builder at `drop_sites` computed from the *enemy* Core
  (`dest`, 1207), including a multi-hop leapfrog (1292-1312) if one throw doesn't close the
  distance — mechanically identical to what Albert-And-Einstein does. Difference is entirely
  timing: theirs fires turn 1 off their own Core; `opp_v44`'s can't exist before harv>=4.
  Defensive use (exile an adjacent enemy builder, 1253-1275, gated d²≤2 from the Launcher) is
  checked first each round and wins if applicable, but is opportunistic, not the design intent.
- **Spawn-ring blocking: no deliberate version.** No code enumerates the enemy's ring and parks
  a passive body on it. `_saboteur` targeting is attack-first (walk toward `ec`, or orbit
  radius 2 if stuck within d²≤8 of it, 644-649) — an active loop, not camping. Incidental
  overlap: `_launcher`'s first-priority `drop_sites` tier (211-216) *is* exactly the enemy's
  12-tile spawn ring (cardinal, `dist_core==1`), chosen so a landed saboteur can `fire()` the
  Core immediately via `_sabotage_prio`'s cardinal check — so one ring tile often does get
  occupied, but as a side effect of optimizing for immediate damage, not as denial-first design
  the way Albert-And-Einstein's 96-98%-of-the-game camping reads.
- **Anti-rush defense: yes, genuinely reactive, not schedule-gated — the important finding.**
  Two independent, vision/proximity-triggered tracks, neither gated on `opp_v44`'s own economy
  state: (a) `_core()` recomputes `under` fresh every round from its own live vision
  (enemy turret d²≤64 or enemy builder d²≤16 of the Core, 199-213, plus a 35-round memory via
  `SLOT_ATK_RND` for builder-reported threats, 218-221) and can go straight from that to
  ammo-banking (234-241) to an emergency 3-Sentinel battery *the same round*, facing the actual
  threat position (`aim = threat or ec`, 250) — **gated `w*h>120`, so disabled on the smallest
  maps** (fjordgate is 10×10=100, below threshold, per game-model.md's census); a slower,
  always-available fallback (`harv>=1`-gated reactive Sentinel, 300-309) covers every map size
  regardless. (b) `_home_defend()` (493-533): any saboteur/launchwait-role builder within d²≤25
  of the Core switches to all-hands mode — heal, fire, emergency Sentinel/Barrier, or body-block
  — the instant an enemy Builder Bot is within d²≤20 of the Core (469-482). Rough estimate: a
  camper landing in the ring by turn 6-27 (Albert-And-Einstein's own measured range) would very
  plausibly be seen by the Core the same round (the ring sits well inside its own r²=36 vision)
  and answered within a round or two after, i.e. roughly turn 7-29 in that timeline — *not*
  measured, but structurally the opposite of aug7, which has no threat detection at all and
  whose only trigger is a wandering ore-seeker's economy-gated coincidence (see this file's own
  Albert-And-Einstein entry: our real defense arrived turn 436 or turn 81, or never).
- **Classification: semi-rush (economy first, then a real timed attack) — with two honest
  caveats.** It's population-split-from-birth, not strictly sequential (offense-track *role*
  assignment doesn't wait on economy; only the delivery mechanisms do), and the "economy
  first" phase is deliberately shallow (`ECO_NEED=4`, well under `ECO_CAP=8`) rather than
  maximized. It is **not** full-rush by the Albert-And-Einstein yardstick — no turn-1 Launcher,
  no turn 4-15 forward turrets; its fastest path is roughly an order of magnitude slower by the
  estimate above. **If its opponent rushed it at turn 4-15:** the reactive-defense layer (two
  bullets up) is orthogonal to `opp_v44`'s own build progress — it only depends on seeing a
  threat — so it would plausibly still fire correctly that early. Its own offense would not
  reciprocate in time; against a mirror-image early rusher it would be surviving entirely on
  the reactive-defense layer, not winning a race with its own attack.

### florent-v63 (`bots/opp_v45`) — source diff against v58, and where the +38 points most plausibly comes from (2026-08-06)

x3r0's active submission jumped from `bots/opp_v44` ("florent-v58") to `bots/opp_v45`, measured
**beating v58 78.3% [70.1%, 84.8%] and our `bots/aug7` 80.0% [72.0%, 86.2%]**, zero crashes
either side. This is a full source read of `bots/opp_v45/main.py` (1573 lines) against
`bots/opp_v44/main.py` (1312 lines) — a +38-point jump inside one author's own lineage is
unusually clean signal. No matches run this pass, source only, per this task's constraints.

**A version-labeling note first, because it caps how much weight their own numbers can carry.**
`bots/opp_v45/main.py`'s own docstring calls itself **"v61 OFFLINE"** (line 1) — neither "v58"
nor "v63". Worse, `bots/opp_v45/meta.json` is **byte-identical to `bots/opp_v44/meta.json`** in
every field that matters — same `"version": "v58"`, same `sha256`, same `accepted_suite` (378
games, 376 wins, 349 core_kills, 0 tracebacks/TLEs) — despite `main.py` itself being a
substantially different, larger file (66,538 bytes / 1573 lines vs 55,812 bytes / 1312 lines).
**This meta.json was not regenerated for the new bot**; none of its numbers describe this file's
own acceptance run. Everything below is source-diff evidence only — there is no "official" v63
suite score to cite the way the existing florent-v58 entry above could.

**1. Mechanism inventory diff**

New in v63, not present in v58 at all:

- **Verified-alignment counterbattery**, `_try_counterbattery()` (`opp_v45:844-883`). Reads the
  attacker's exact tracked position from the new `SLOT_THREAT` slot (`opp_v45:34`, written at
  `opp_v45:252,257,434`) and, for each of 4 adjacent tiles × 8 facings, calls the engine's
  documented hypothetical-fire check `ct.can_fire_from(bp, facing, turret_type, threat)`
  (`opp_v45:870`; API confirmed at `docs/reference/official-docs.md:437`) **before** ever
  building — guarantees the placed turret's ray actually reaches the tracked threat. v58 had no
  such verification anywhere: its equivalents (`opp_v44:246-260` Core battery, `opp_v44:708-718`
  reactive builder Sentinel) both compute `facing = bp.direction_to(aim)` and build unconditionally
  once `can_build_sentinel` returns true for *some* position, with no check that the ray actually
  intersects the target. Since Sentinels can never re-aim once built (`docs/game-model.md:227`,
  "Rotate? No (fixed at build)"), an unverified placement can waste the whole turret.
- **Planned forward siege battery**, `_plan_siege()` (`opp_v45:667-766`) +
  `_try_siege_build()` (`opp_v45:768-800`). Runs a real BFS terrain flood for path distance
  (`opp_v45:691-704`), then for every enemy-Core-footprint tile × 8 facings × integer ray length
  enumerates firing positions, checks wall-blocking along the whole ray (`opp_v45:730-734`),
  requires cardinal-adjacent buildability (`opp_v45:740-758`), and scores by BFS distance plus a
  self-ray and ore-terrain penalty (`opp_v45:751-758`). The per-direction ray lengths — Sentinel 5
  cardinal / 4 diagonal, Gunner 3 cardinal / 2 diagonal (`opp_v45:682`) — are an exact integer
  decomposition of `docs/game-model.md:224-227`'s documented `r²=32` (Sentinel) / `r²=13` (Gunner)
  attack thresholds (5²=25≤32<6²; 4²+4²=32≤32; 3²=9≤13<4²; 2²+2²=8≤13<3²+3²), not an approximation.
  v58's forward emplacement (`_saboteur`, `opp_v44:639-663`) built only Gunners, on the first
  cardinal-adjacent tile within d²≤64 of the enemy Core, facing `direction_to(ec)` with no wall or
  alignment check at all.
- **`SLOT_SIEGE`** (`opp_v45:35`) coordinates the primary forward emplacement across builders —
  written once by the role_n==0 builder's first forward gun (`opp_v45:796-797`), read by every
  other builder's `_plan_siege` to avoid re-choosing that tile (`opp_v45:706,723-726`), and used by
  the role_n==0 builder to keep re-healing that specific position (`opp_v45:807-814`). No
  equivalent in v58.
- **An independent HP-drop threat trigger.** `opp_v45:260-263`:
  `if self.last_hp is not None and hp < self.last_hp: under = True` — a "we are losing HP right
  now" signal layered on top of the same vision/proximity checks v58 already had
  (`opp_v45:242-258`, matching `opp_v44:199-213` almost verbatim). Not present in v58.
- **Map-signature disambiguation.** `known_map_for(w, h, own, ct=None)` (`opp_v45:116-147`) now
  takes the controller and, when two pool maps share a `(w,h,core-anchor)` signature (the two
  26×26 layouts in `EXTRA_MAP_CODES`, `opp_v45:96-97`), scores every candidate against
  currently-sensed terrain (`opp_v45:139-147`) to pick the right one. v58's version
  (`opp_v44:98-113`) takes no controller and returns the first signature match unconditionally —
  silently wrong whenever two known maps collide.
- **Six more recognized maps.** `EXTRA_MAP_CODES` (`opp_v45:94-102`) plus 6 more `CORE_PAIRS`
  (`opp_v45:56-59`) extend the exact per-map terrain/ore database from 21 to 27 signatures — same
  mechanism as v58, wider coverage.
- **Deterministic, non-random builder placement.** `import random` is gone (present at
  `opp_v44:9`, absent from `opp_v45`'s imports). Spawn-tile choice is now a fixed hash sort
  (`opp_v45:320-321`), and the first builder is explicitly steered to the ring tile nearest the
  enemy Core rather than a shuffled one (`opp_v45:315-318`) — the stated purpose is reproducible
  offline testing (comment, `opp_v45:316-317`), but it also means the first offensive unit starts
  closer to the enemy from turn 0 every game, not just on lucky shuffles.
- **A large layer of hardcoded per-map/per-seat special cases — at least nine, none present in
  v58**: `atoll_burst_magazine`/`hive_magazine` ammo targets up to 256 (`opp_v45:281-292`);
  `nordkap_home_a`/`snowflake_home_b` builder-cap overrides (`opp_v45:303-309`); forced role
  overrides for two named seats (`opp_v45:447-467`); `keep_artillery_forward`
  (`opp_v45:535-545`); `hive_home_a`/`snowflake_home_b`-gated recall via the new `_rank2_hold`
  (`opp_v45:510-530`, method at `opp_v45:596-602`); a `hive_bunker` barrier routine fixed to tile
  (20,4) (`opp_v45:902-923,959-963`); `chase_battery` (`opp_v45:925-928,940-943`); `hive_freeze`,
  which stops all expander activity past round 42 on two named seats (`opp_v45:1003-1010`); and
  `healer_focus` turret-priority reordering on one named seat (`opp_v45:1377-1417`).

**Stale map tables — the single biggest defect found in v63 (2026-08-06, equivariance audit +
measured fix).** `CORE_PAIRS` / `MAP_CODES` / `EXTRA_MAP_CODES` (`opp_v45:44-102`) predate the
current weekly rotation: **eider, heart, meander, drumlin and saga have no entry**, so
`known_map_for` returns `None` there, `self.map_grid` stays `None`, and `_plan_siege`
(`opp_v45:669`) — the line's primary attack — is **disabled on 5 of the 15 pool maps**, three of
them mirror maps. Two long-standing mysteries fall out of this at once: (1) **the heart
zero-harvester-as-B defect is this bug** — with refreshed tables (bots/_v63maps) team B goes from
1 building / 0 mined to 75 buildings / 2450 mined on seed 1; (2) our Launcher wake-up swept
**eider** precisely because the base cannot siege there, so games decay to economy tiebreaks.
Corollary: **this table refresh must recur at every weekly pool cutover** (runbook step added).

**The fjordgate collapse, diagnosed (2026-08-06, subagent + 2 instrumented matches, both seeds
reproduce).** On the 10x10 (core anchors d²=32 apart — closest pair in the pool), v63's
threat-response complex misfires on opening noise and bankrupts itself pre-income: the core marks
`under` for any enemy builder within d²≤16 (`opp_v45:254-257`) — which covers ordinary spawn-ring
tiles here; the melee-recall gate (`opp_v45:546-558`, d²≤25/20) keeps the saboteur home, where
`_home_defend` runs **`_try_counterbattery` (`opp_v45:844-883`), which unlike `_plan_siege` has
no forward-gun cap and no economy gate** — it built 3 fixed-facing Sentinels by round 6 aimed at
*transient builder spawn tiles*, and with 5 builder spawns the bank hit ~12 Ti before the first
harvester. Permanent: any home gun makes `weapons` truthy, dropping `ti_floor` to 12
(`opp_v45:293-294`), so all income above the floor converts to ammo forever — seed 1 ends 255
rounds at **0 harvesters, 0 mined, ti = exactly 12**. Our line wins 26/32 there because our
near-core sentinel ring (r²=32, unblockable) reaches their core footprint at this separation —
home defense doubles as a siege battery. **Fix target, next queue: mirror `opp_v45:674`'s
ECO_NEED gate onto `_try_counterbattery`, and stop writing builder positions into SLOT_THREAT
for fixed-facing turret aiming (`opp_v45:254,257`).** Radii scaling by map size is the deeper fix.

**SOLVED, 2026-08-09 (session 9), by the first half of that fix alone.** Mirroring the
ECO_NEED gate onto `_try_counterbattery` — six lines, `bots/_v64cbA` — converts fjordgate
**16/32 → 32/32** both seats, every win by core kill, and takes the pooled gate vs `opp_v45`
from 63.3% to **70.0%**. It also converted **meander** (16/32 → 32/32), which was a separate
open puzzle, and lifted the rush guard from 86.7% to 95.4% on the frozen instrument. The
other two items in the fix target were **not** needed for this and remain open: SLOT_THREAT
still takes builder positions for fixed-facing aiming, and the absolute radii still do not
scale with map size. Both are still live in x3r0's engine — a third message for the team.
The strict variant (no free first battery, `bots/_v64cbB`) is refuted: it turns fjordgate into
a first-mover coinflip instead of curing it.

**Equivariance audit summary (same pass; full detail in the session transcript).** Ranked
per-seat asymmetry risks on mirrored maps: (1) the **nordkap one-seat gate cluster**
(`opp_v45:307-308,448-451,925-928`, all keyed to core `(9,6)` with no `(9,18)` twin — different
builder cap, role split and defense per seat); (2) **moonrise `keep_artillery_forward`**
(`opp_v45:536-537`, `core.x == 5` only — one seat never recalls forward artillery, the other
does); (3) **`_plan_siege`'s absolute west/north tie-break + `candidates[2]` follower pick**
(`opp_v45:754-762`) making mirrored seats' forward batteries non-mirror-images. Also notable:
**id-parity pathing chirality** (`opp_v45:1310`: `side = 1 if (self.idx & 1) else -1` — seat A's
unit ids are always one below seat B's, so corresponding builders prefer opposite detours on
every map), and `nearest_cardinal` (`opp_v45:160-167`) is not equivariant under reflection *or*
rotation. The named one-seat gates may be deliberate per-seat tuning; the tie-breaks are not.

Removed from v58, confirmed by grep as well as diff:

- **All Core-side turret construction.** v58's `_core()` built up to 3 emergency Sentinels from
  the Core's own ring, gated `under and w*h>120` (`opp_v44:246-260`), and up to 12 Gunners the
  same way (`opp_v44:262-278`). None of it survives in `_core()` — replaced by a one-line comment:
  "Cores cannot construct turrets; the defender consumes SLOT_THREAT and owns all counterbattery
  placement" (`opp_v45:328-329`).
- **Launcher construction, functionally, though not textually.** `_try_build_launcher()` still
  exists verbatim (`opp_v45:356-378`) but **has zero call sites anywhere in the file** — confirmed
  by grep, not just diff. Its one and only call site in v58, inside `_defend` (`opp_v44:682`), has
  no counterpart anywhere in v63's `_defend` (`opp_v45:900-957`). `_launcher()`
  (`opp_v45:1456-1573`), `_launchwait()` (`opp_v45:628-654`) and `_offer_launch()`
  (`opp_v45:656-665`) all still exist but are structurally close to unreachable: the spawn-time
  role split (`opp_v45:390-395`) never assigns `"launchwait"` at all (v58's did, `opp_v44:377`),
  the only path to it is a late dynamic promotion (`opp_v45:486-491`) gated on `role_n>=5`, which
  is unreachable under the new `MAX_BUILDERS=5` cap except on the one map special-cased to 6
  builders. The docstring states the reasoning directly: "one-hop Launchers and a 60-ammo
  stockpile were dead capital" (`opp_v45:3-4`).
- **The immediate-fire-on-adjacent-Core special case** in `_sabotage_prio` (`opp_v44:535-546`) —
  removed, folded into a unified priority table (below).
- **The "distance from home > 80 ⇒ Launcher dropped me" heuristic** (`opp_v44:465`) — deleted,
  with a comment explaining it was simply wrong: "long economy chains routinely travel farther
  than nine tiles" (`opp_v45:506-508`).
- **The Launcher-savings reserve gate** on paving and link-building (`opp_v44:907-913` and
  `opp_v44:1111-1114`) — gone from both call sites (`opp_v45:1160-1162`, `opp_v45:1358-1365`),
  consistent with the point above.

Reparameterized (same mechanism, different constants or priority):

- `MAX_BUILDERS` 8→5, `EARLY_BUILDERS` 4→5, `ECO_CAP` 8→18, `ECO_NEED` 4→3, `AMMO_FLOOR` 40→16
  (`opp_v44:17-20,37` vs `opp_v45:15-18,37`).
- Role assignment at spawn: v58 was 0→defend, then size-dependent (`opp_v44:370-377`: small map
  1-2→expand/3+→saboteur, large map ≤4→expand/5+→launchwait). v63 is 0→saboteur, 1-3→expand,
  4→defend (`opp_v45:390-395`) — offense now gets the *first* builder rather than a
  late-population fraction, and with only 5 total builders the split is close to a fixed 1:3:1
  ratio rather than v58's size/threshold branching.
- `_sabotage_prio`'s priority table: v58 excluded enemy turrets from its fallback fire list
  (`if et in (GUNNER, SENTINEL, CORE): continue`, `opp_v44:556`). v63 folds Core into a single
  table and puts enemy Gunner/Sentinel at *top* priority (`opp_v45:615-620`) — a cardinal-adjacent
  builder will now shoot an enemy turret, which v58's fallback path never did.
- `_heal_core`: v58 used `p.distance_squared(self.core) <= 5` (`opp_v44:497,662`), a Euclidean
  approximation of adjacency to the Core's 2×2 footprint. v63 factors this into a helper that
  checks the actual 4 footprint tiles via `core_tiles()` and heals whichever one `ct.can_heal()`
  accepts (`opp_v45:837-842`).

**2. Where the +38 points most plausibly comes from, ranked**

1. **[New capability, highest confidence] Replacing what was very likely non-functional Core-side
   defense with a working, verified, builder-side one.** `docs/reference/official-docs.md:174`
   states plainly: "The Core has no movement or attack actions — its active abilities are spawning
   Builder Bots and converting ammunition." Our own project's `_defense_port` design note
   confirmed this the hard way (`bots/_defense_port/main.py:15-19`): "Core-side turret
   construction was considered and empirically ruled out first: `ct.can_build_sentinel(...)` and
   the generic `ct.can_build(...)` both return False for every candidate tile when called from the
   Core's own `run()` branch (verified with a throwaway single-match probe, no exception raised)."
   v58's headline "Core builds its own defense directly" mechanism (`opp_v44:246-278` — the
   mechanism the *existing* florent-v58 entry above gave top billing) sits entirely inside
   `_core()` and depends on exactly that call succeeding. If the same engine restriction applies
   uniformly to every team — there is no reason to think it wouldn't — that code was very likely
   dead in every v58 game, on every map, `w*h` gate or not, which would also explain the existing
   entry's own replay-measured finding that v58's reactive defense "misses badly... or not at all"
   in roughly half of qualifying cases: what actually fired, when it did, was the low-priority
   builder-side fallback buried at the bottom of `_defend`'s `elif` chain (`opp_v44:708-720`), not
   the instant Core battery the source read like it should. v63 deletes the dead Core code outright
   and promotes a working, alignment-verified, builder-side counterbattery to a high position in
   the same call chain (`opp_v45:933-945`, `opp_v45:572-578`). Plausibly the single largest
   contributor — turning "usually not happening" into "actually happening, and aimed correctly."
   Caveat, stated plainly: this is inference from documented engine rules plus our own probe on our
   own bot, not a probe run against v58/v63 specifically — this pass's constraints rule that out.
2. **[New capability] Verified-alignment forward siege, Sentinel-primary.**
   `_plan_siege`/`_try_siege_build` replace v58's unverified, Gunner-only, proximity-triggered
   forward emplacement with wall-aware, ray-verified, BFS-ranked placement, and specifically
   prefer a Sentinel (longer, wall-piercing) for the first forward gun
   (`PRIMARY_SENTINEL`, `opp_v45:38,679`). Same category of change as our own biggest single-version
   win (Sentinel-first, 68.4% vs v4 — `docs/strategy-log.md:1054-1083`), taken one step further
   with engine-verified placement. Notably, our own attempt at verified aimed-placement
   (`can_fire_from`-style scoring of `_run_sentinel`, `docs/strategy-log.md:889-926`) came back "a
   perfect null" for us — for a specific, named structural reason: by the time our builder reaches
   the sentinel gate it's already boxed in by our own economy build-out, so the candidate set has
   usually collapsed to one legal tile before scoring even runs. v63's siege planner doesn't have
   that problem — it picks *where to walk* from a wide BFS-reachable candidate set before
   committing (`opp_v45:667-766`), rather than scoring only tiles the builder is already standing
   next to. That structural difference is plausibly why the same idea pays off for them where it
   measured as a null for us.
3. **[Mostly tuning, some capability] A leaner, front-loaded economy with offense assigned first,
   not last.** Fewer total builders (5 vs 8) all spawned early, higher `ECO_CAP` (18 vs 8)
   concentrating more harvesters per remaining builder, and the first builder assigned to offense
   from spawn instead of the last population fraction. Same underlying spawn/role mechanism as
   v58, but both the constants and — more structurally — *which* builder gets which role changed.
4. **[Tuning] Just-in-time ammo.** `AMMO_FLOOR` 40→16 plus graduated/map-specific targets
   replacing a flat "60 if under attack." Docstring names this as intentional ("a 60-ammo
   stockpile were dead capital"). Same `convert_ammo` mechanism, retuned thresholds.
5. **[Lowest confidence, probably map-concentrated] The 9+ new per-map special cases.**
   Individually narrow (named maps/seats only), so plausibly a real but concentrated contribution
   on the handful of maps each one targets, not a broad-based one. Can't rank more precisely
   without a per-map breakdown, which would need matches this pass didn't run.

**3. Delivery and economy — conveyor facing, precisely, since this is what we most need answered**

v63 (unchanged from v58 in this specific area) runs **two parallel conveyor-laying systems**, and
they answer the task's question differently:

- **The primary system — every harvester's link to the Core — is a planned path, not a walked
  trail, in both versions.** `_link_path()` (`opp_v45:1057-1158`) runs before a single conveyor is
  placed: a multi-source reverse BFS from every valid Core-input tile (`opp_v45:1058-1066` builds
  the goal set, `opp_v45:1091-1105` grows the tree) builds a parent-pointer tree, and the
  harvester's own route is read off that tree from harvester to Core (`opp_v45:1108-1113`). The
  resulting `link_queue` is walked in order by `_build_next_link()` (`opp_v45:1160-1195`); each
  interior tile's facing is set toward the *next tile already in that precomputed queue*
  (`opp_v45:1181-1182`: `f = tile.cardinal_direction_to(self.link_queue[1])`), and only the
  terminal tile — the one actually adjacent to the Core — recomputes a direct aim at the nearest
  real Core footprint tile (`opp_v45:1180,1186`). Because the whole route is a BFS tree grown from
  the goal outward, it is cycle-free by construction (every tile gets exactly one parent, once)
  *and* bend-safe by construction (facing always points at the actual next hop of the actual
  chosen route, never a recomputed "dominant axis" that could disagree with where the path really
  goes next).
- **This is a third architecture, distinct from both what we started with and what we just
  shipped.** Our own accepted fix threads a needle: dominant-axis-toward-Core inside
  `NEAR_CORE_FACING_DIST_SQ=18`, trail-linked (face back at the tile you came from) outside it — a
  hybrid forced by the finding that a naive always-trail-link rule produces closed cycles near the
  Core (43.6% of that experiment's failures — trails converging near the Core point back at each
  other, `docs/strategy-log.md:49`) even though it fixes the bend problem everywhere else. v63's
  plan-first approach gets both properties — no cycles, no bend breaks — simultaneously and
  without a near/far split, because what it calls a "trail" was never locally remembered; it's a
  global tree from the start. **Direct answer: v63 routes its primary delivery chains as a planned
  path, computed once via BFS ahead of construction, not as a walked trail.**
- **v63 does *not* have the facing/termination defect of the kind we just fixed, in this primary
  system — in either version.** This code is byte-identical between v58 and v63 (the only diff in
  this region removes a Launcher-savings spending gate, `opp_v44:907-913` vs `opp_v45:1160-1162`,
  not any part of the facing logic itself) — so whatever it gets right or wrong here isn't part of
  what changed between v58 and v63, and it isn't broken in the way pre-fix `aug7` was.
- **But there is a second, secondary system, and it still has exactly that defect, unchanged
  across both versions.** `_move()`'s opportunistic paving (`opp_v45:1351-1369`, identical logic to
  `opp_v44:1102-1123`) fires whenever an "expand"-role builder happens to step onto empty ground
  that's strictly closer to the Core than where it stood (`opp_v45:1358-1362`), and computes
  facing fresh, per tile, independent of any plan or memory:
  `nearest_cardinal(nxt.direction_to(nearest_core_tile(nxt, self.core)))` (`opp_v45:1363`) —
  dominant-axis-toward-Core, recomputed at every tile. This is the exact rule our own strategy log
  characterized as "Cause #2, 71% of the residual [facing] breaks... a conveyor should point where
  the trail goes, not where the Core is" (`docs/strategy-log.md:188-197`). It is a smaller-footprint
  problem for them than it would be for a bot that relies on it as the *primary* delivery
  mechanism (every harvester already gets a correct planned chain from `_link_path` regardless of
  what this secondary system does), and the monotonic-closer-to-Core guard likely limits how often
  it produces a genuine directional flip — but it is a live, citable, unfixed instance of the same
  defect, present in both v58 and v63, that has gone untouched across at least this one version
  jump.

**4. What remains unaddressed, and the fjordgate gate specifically**

- **The `w*h<=120` gate is gone, not narrowed — and so is the mechanism it gated.** Confirmed by
  grep as well as diff: `w * h` appears exactly once in all of `opp_v45/main.py`
  (`opp_v45:127`), inside the unrelated map-decoding routine — there is no map-area threshold
  anywhere in v63's control flow. v58's gate lived entirely inside the (very likely non-functional,
  see §2.1) Core-side emergency-Sentinel block (`opp_v44:247`). Its replacement,
  `_try_counterbattery` (`opp_v45:844-883`), has no size gate of any kind — it runs at any map
  size, fjordgate included. **But it trades one dependency for another**: because it only runs
  from a *builder's own* action (called from `_defend`/`_home_defend`, both builder-context
  methods — `opp_v45:933-945`, `opp_v45:572-578`), it requires an actual builder to be nearby when
  `SLOT_THREAT` is populated, which is exactly the "single point of failure" the original v58
  source-read flagged as `aug7`'s own weakness relative to v58's (apparently illusory) Core-side
  battery. Net effect specifically for the fjordgate exploit: **the mechanism the 32/32 sweep was
  tuned against — a size-gated, Core-side battery that structurally cannot fire below 120 tiles —
  no longer exists in v63 in that form.** Whether the sweep still holds against v63's
  builder-mediated replacement is a question this source read cannot answer without running
  matches, which this pass's constraints rule out; it would need dedicated re-verification.
- **v63 replaces one broad size gate with roughly nine narrow name-specific ones** (§1, "large
  layer of hardcoded per-map/per-seat special cases"). Each is brittle in the same way the
  exact-map database itself is — memorized from specific replays, works only on maps/seats already
  seen, silent no-op everywhere else (every one of them is guarded by an exact
  `(mw, mh, core.x, core.y)` tuple match) — but that is a known, already-accepted tradeoff in this
  lineage (the whole per-map terrain database works the same way), not a new category of risk.
- **Confirmed still absent in v63, same as v58:** no `ct.destroy()` / `self_destruct()` anywhere
  (grep, zero hits) — neither version does active cost-scale management by tearing down obsolete
  or redundant buildings. No `get_cpu_time_elapsed()` call anywhere (grep, zero hits) — no explicit
  CPU budget guard in either version; both rely on inline bounds-checks plus narrow `try/except`
  blocks instead (v63 has 9 such blocks vs v58's 6 — `opp_v45:140,808,869,1076,1133,1138,1143,
  1263,1397` — a modest increase consistent with the new `known_map_for` disambiguation and the
  new `can_fire_from` guard, not a change in overall philosophy).

**5. Adoption notes**

Ranked, what's worth porting from v63 into our own line:

1. **Verify fire alignment (`ct.can_fire_from`) at candidate-selection time, not just among tiles
   already reached.** This is the structural fix to why our own equivalent experiment
   (`docs/strategy-log.md:889-926`) came back a null — ours only ever scored tiles the builder had
   already walked into; v63's `_plan_siege` chooses *where to walk* from a wide reachable set
   first. Worth re-testing our own idea with that one change before concluding verified placement
   doesn't pay off for us.
2. **An exact threat-position broadcast slot**, not just a boolean flag — cheap (one comms slot,
   mirrors `SLOT_ATK_RND`'s existing pattern) and a prerequisite for the point above.
3. **The HP-drop independent trigger** (`opp_v45:260-263`) — catches damage sources a
   vision/proximity scan might miss, three lines, purely additive.
4. **The plan-first BFS conveyor router**, as a longer-term replacement for our own near/far
   hybrid rather than a bolt-on — it appears to get bend-safety and cycle-safety simultaneously
   without needing a radius split at all. Structural, not a quick port (`_link_path`/
   `_build_next_link` together are about 140 lines), but worth scoping.

And the harder, more important question — what of **ours** is worth porting onto **their** base if
we switched:

| our mechanism | status on v63's base |
| --- | --- |
| Trail-linked conveyor facing (exact-link, survives bends) | **Mixed.** Their *primary* delivery chain already solves the same problem by a different, arguably stronger route (plan-first BFS tree, §3) — porting ours there would be redundant. Their *secondary* opportunistic-pave path (`opp_v45:1351-1369`) still runs the unfixed dominant-axis rule, unchanged across two versions — a real, narrow, well-scoped port target: our exact fix, applied to their `_move()`. |
| (0,0)-Core store fix | **Already present**, unchanged since v58's predecessor v39. `pack_pos`/`unpack_pos` (`opp_v45:150-157`) use the identical `+1` offset scheme and explicit `if not val: return None` guard as ours (`bots/aug7/main.py:95-108`). Nothing to port. |
| Sentinel-first defense | **Already present, and more developed than ours.** `PRIMARY_SENTINEL=True` (`opp_v45:38`) drives both defensive and offensive turret-type choice, and — unlike our straight type swap at one fixed trigger — is paired with `can_fire_from` alignment verification before committing. Nothing to port; if anything, worth studying theirs. |
| Reactive vision-triggered defense port | **Already present, and *shipped* — unlike ours.** Our own `bots/_defense_port` failed its own accept gate (40.6% vs `opp_v44`, no measurable benefit vs `rush_probe`) and sits parked, not adopted into our active line (`docs/strategy-log.md:119-166`). v63's equivalent (`SLOT_UNDER`/`SLOT_THREAT`/35-round memory, now plus the HP-drop trigger) is live and wired into its only defense path. Nothing of ours to port here that would improve on theirs — the more useful move is treating v63's version as the working reference implementation of the idea our own attempt didn't clear its bar with. |

## Version-attributed match audit + top-team unrated pattern digest (2026-08-06, ~13:52 UTC)

Fresh full pull of `fcode match list --mine --json` (paginated with `--limit 100` + `--cursor`,
2 pages) — **181 total matches** since team creation: **107 rated ladder series** (matches
`fcode status`'s "107 matches played" exactly) and **74 unrated**. This supersedes
reconstructing version activation from timestamps, per this pass's brief: the JSON gives
`teamAVersion`/`teamBVersion` (the exact submission that played each side of each match),
`eloDeltaA`/`eloDeltaB`, and `ratingABefore`/`ratingBBefore` directly, so every row below is
attributed to a specific submission version with no inference required. Current snapshot:
rating **1233.34**, rank **#50/103**, active submission **v44** ("florent-v58") — matches
`fcode status` exactly (1233.34 = the last ladder match's `ratingBBefore` + its `eloDelta`),
consistent with the existing note above on that field's accuracy.

### Rating trajectory by submission version (all 107 rated series)

Version churn continues exactly as the sweep note above already flagged, and this pass
reconfirms it through the newest matches too: **v21 reappears** after v22–v38 had already
played (series `dca5a663`, 11:19 UTC), and from 11:30 UTC onward **v40, v41, v42, and v44
interleave directly** — v44's two series sit *between* v40 series chronologically, not after
them (full measured sequence of `our_version` by completed-time: `...,38,38,38,21,41,42,40,
40,40,40,40,40,40,40,44,40,44`). Several people are still shipping/reactivating versions
concurrently. Per-version record, every version with ≥3 rated series or a net Elo swing worth
calling out:

| version | series (W–L) | games (W–L) | net Elo | rating span |
|---|---|---|---|---|
| v20 | 22 (15–7) | 70–40 | +22.51 | 1199.5 → 1222.0 |
| v21 | 8 (6–2) | 24–16 | +22.77 | 1222.0 → 1179.4 (spans the reappearance, see above) |
| v40 ("aug7-sentinel-economy") | 9 (8–1) | 31–14 | **+35.24** | 1183.8 → 1226.1 |
| v44 ("florent-v58") | 2 (2–0) | 8–2 | +14.34 | 1214.1 → 1233.3 |
| v9 | 3 (0–3) | 1–14 | −43.20 | 1399.8 → 1356.6 (worst version sampled) |
| v11 | 3 (0–3) | 2–13 | −36.56 | 1350.6 → 1314.0 |

(all other versions, v1–v8/v10/v12–v19/v22–v38/v41–v42, played 1–4 series each — too small
individually to read much into; full per-version table generated but not reproduced here to
keep this section readable — see `build_table.py` output in scratch if needed later).

v40 is the strongest well-sampled version to date (8W–1L; its only loss is the
already-documented Albert And Einstein blowout `81d83bb5`, 1306.8). **v44 has only 2 rated
series so far** (both wins: Leviathan 4–1 @1159.0, Troupe 4–1 @1174.9) — too small a sample to
say anything about its ladder strength yet. Everything below about v44 *losing* comes from the
unrated bucket, not the ladder — v44 is currently undefeated on the ladder.

### Unrated matches ranked by opponent rating — the list this pass worked from

74 unrated matches, deduplicated by opponent identity, ranked by the opponent's
`ratingBefore` **at the time of that specific match** (their live/current rating shown
separately where it has since moved):

| rank | opponent | rating (at-match / live now) | matches | our record | our versions seen | status |
|---|---|---|---|---|---|---|
| 1 | **Pivot** | ~1907–1965 / 1948.0 | 65 | 0W–65L | v21–v44 (20+ versions) | #1 team; 1 game already decoded (`91d77721`, existing entry above); **+1 new decode this pass** (v44) |
| 2 | **sporks** | 1923.4 | 1 | 0W–1L | v44 | brand-new name — **decoded this pass** |
| 3 | **not adgato** | 1897.0 | 1 | 0W–1L | v44 | brand-new name — **decoded this pass** |
| 4 | **Besvikomat** | 1789.1 / 1802.6 | 1 | 0W–1L | v40 | named (not decoded) in the earlier "Unrated scouting" entry above — **decoded for the first time this pass** |
| 5 | The Flotte Experience | 1686–1696 / 1744.6 | 4 | 0W–4L | v21–v24 | named (not decoded) earlier; deprioritized this pass — **all 5 maps in every one of its games are retired from the current pool** (bridge/showdown/string/aurora/sweden), so behavioral data from it is map-stale |
| 6 | Jacobs Code | 1376.5 / 1384.7 | 1 | series 1W–4L | v38 | named (not decoded) earlier; still not decoded — lower rating priority than the above |
| 7 | **Albert And Einstein** | 1323.3 / 1323.2 | 1 | series **2W–3L** | v44 vs their **v8** | the explicitly-flagged sample — **full 5-game series decoded this pass**, see below |
| 8 | StarTrekker | 1206.5 / 1208.5 | 1 | 1W–4L | v40 | already decoded (existing entry above, match `eb72ce59`) |

**v44's entire unrated record is 0W–4L** — Pivot (`9436bd69`, 0-5), sporks (`81ce7948`, 0-5),
not adgato (`2397deb4`, 0-5), Albert And Einstein (`a2a03506`, **2-3**, the only
non-blowout). Per `fcode match info` on all four of v44's matches (**20 individual games
checked**): **every single one ended `core_destroyed`** — v44 has not lost a single unrated
game to economy or harvester count so far, only to a dead Core. (Widening the check to all 7
candidate matches this pass pulled `match info` for — 35 games total, including Besvikomat,
Flotte Experience, and Jacobs Code alongside the 4 v44 matches — `core_destroyed` still
dominates at 29 of 35, but the three non-v44 matches do show `titanium_collected` and
`harvesters` decisions on the games that ran the full 1000-turn cap.)

### Decode budget: 9 new replays, reusing the existing decoder unchanged

Downloaded and decoded **9 new games** across 5 matches (`replay_codec.py` and the
`analyze_aae2.py` ring-occupancy / `moveBuilderBot`-jump-detection logic reused as-is, wrapped
in a new `batch_analyze.py` in scratch that takes explicit win/loss + team-side per game instead
of assuming "we always lose" like the one-off AAE script did): 1 representative game each from
Pivot, sporks, and not adgato (v44's three new-opponent losses — all three are 0-5 sweeps where
every game is `core_destroyed`, so one sample per the existing "one or two samples already say
everything" finding), **all 5 games** of the Albert And Einstein v8 series (explicitly flagged
as the highest-value sample — the first time we have both a *win* and a *loss* from the same
opponent+version pairing to contrast), and 1 game from Besvikomat. All maps used are in the
current 15-map pool.

| match : game | opponent (rating) | our ver. | map (W×H) | turns | result |
|---|---|---|---|---|---|
| `9436bd69` g2 | Pivot (1961) | v44 | hive (25×25) | 217 | L |
| `81ce7948` g3 | sporks (1923) | v44 | fjordgate (10×10) | **63** | L |
| `2397deb4` g3 | not adgato (1897) | v44 | hive (25×25) | 177 | L |
| `a2a03506` g1 | Albert And Einstein v8 (1323) | v44 | eider (28×20) | 373 | L |
| `a2a03506` g2 | " | v44 | fjordgate (10×10) | 328 | **W** |
| `a2a03506` g3 | " | v44 | lighthouse (16×16) | 985 | L |
| `a2a03506` g4 | " | v44 | meander (25×15) | 971 | **W** |
| `a2a03506` g5 | " | v44 | heart (28×20) | 241 | L |
| `c5c193b6` g2 | Besvikomat (1789) | v40 | drumlin (25×25) | 239 | L |

All 9 ended `core_destroyed` (confirmed via `match info`, not inferred).

### Attacker opening timing, measured game-by-game

*(This section answers a "is the sentinel rush universal across the ladder" question raised
mid-pass — see the process note near the end of this entry for where that came from.)*

A cross-session message reached this task claiming "the sentinel rush is the common opening
across the ladder, including high-Elo teams" and asked for a turn/distance table. Rather than
take that on faith, here is the actual measured distribution from all 9 decoded games (18 rows,
both sides each game); `dist` = manhattan tiles from the attacking turret to the *defender's*
Core footprint:

| game (map W×H) | side | 1st Sentinel (turn / dist) | 1st Gunner (turn / dist) | 1st Launcher (turn) | thrown? | ring-camp starts |
|---|---|---|---|---|---|---|
| Pivot g2 (25×25) | v44 (us) | — | 48 / 6 | — | no | camped *their* ring turn 87 |
| Pivot g2 | Pivot | — | 33 / 5 | — | no | camped *our* ring turn 56 |
| sporks g3 (10×10) | v44 (us) | 4 / 6 | — | — | no | — |
| sporks g3 | sporks | **1 / 5** | — | — | no | — |
| not adgato g3 (25×25) | v44 (us) | — | — | 80 | 3×, jump 6–8 | camped *their* ring turn 83 |
| not adgato g3 | not adgato | 97 / 7 (late top-up) | 33 / 12 | — | no | — |
| AAE g1 (28×20) | v44 (us) | 116 / 16 | 140 / 5 | 81 | 1×, jump 5 | camped *their* ring turn 159 |
| AAE g1 | AAE | **4 / 2** | — | **1** | 2×, jump 6–7 | camped *our* ring turn 11 |
| AAE g2 (10×10, WIN) | v44 (us) | 4 / 9 | — | — | no | camped *their* ring turn 7 |
| AAE g2 | AAE | 3 / 1 | — | none | no | camped *our* ring turn 2 |
| AAE g3 (16×16) | v44 (us) | 38 / 9 | — | — | no | — |
| AAE g3 | AAE | 5 / 2 | — | 1 | 1×, jump 8 | — |
| AAE g4 (25×15, WIN) | v44 (us) | 9 / 4 | — | — | no | camped *their* ring turn 46 |
| AAE g4 | AAE | 5 / 2 | — | 1 | 2×, jump 7 | camped *our* ring turn 2 |
| AAE g5 (28×20) | v44 (us) | **none built at all** | — | — | no | — |
| AAE g5 | AAE | 6 / 1 | — | 1 | 2×, jump 5–7 | camped *our* ring turn 9 |
| Besvikomat g2 (25×25) | v40 (us) | 48 / 29 | — | — | no | — |
| Besvikomat g2 | Besvikomat | — | 39 / 6 | — | no | camped *our* ring turn 173 |

**Verdict: not one universal opening — two distinct, tightly-clustered archetypes.**

- **Instant-Sentinel archetype** (sporks, AAE×5): attacker's first Sentinel lands **turn 1–6**
  (median 4.5, n=6, excluding not adgato's turn-97 late top-up which is a different archetype
  entirely), already **1–5 tiles from our Core** (median 2). Measured across map sizes 10×10
  through 28×20 with **no timing correlation to map area** — turns 1,3,4,5,5,6 regardless of
  whether the map is 100 or 560 tiles. The mechanism: in **4 of these 6 sightings** (AAE
  g1/g3/g4/g5) a builder is thrown **5–8 tiles** turn 2–3 (`moveBuilderBot` jump — the Launcher
  mechanic already documented above; slightly wider than the "6-8 tiles" range noted there,
  now that AAE g5's jump-5 throw is in the sample), and the first Sentinel then appears turn 4–6 built
  **1–3 tiles from that throw's landing tile** (e.g. AAE g1: throw lands (15,10) turn 2,
  Sentinel built (17,10) turn 4; AAE g4: throw lands (13,11) turn 2–3, Sentinel built (14,11)
  turn 5) — i.e. **the thrown unit doesn't just camp, it builds a forward Sentinel on arrival**,
  which is a refinement on the existing "launcher-assisted builder rush" note above (that note
  describes the thrown unit as a passive ring-camper; this data shows it — or a companion thrown
  the same way — also functions as a forward turret-construction delivery). This explains the
  map-size independence directly: the throw does the map-crossing, not a walk, so wall-clock
  time to first threat is roughly constant regardless of map dimensions. **The two exceptions**
  — sporks, and AAE g2 (our win) — build their first Sentinel at home with no throw at all;
  sporks still reads as only dist 5 from our Core purely because fjordgate is a tiny 10×10 map,
  while AAE g2 is their one game in this whole pass with no Launcher built at all.
- **Forward-Gunner archetype, ~turn 33–39, no early Sentinel at all**: Pivot (33), not adgato
  (33), Besvikomat (39) — **three unrelated opponents** cluster tightly here, all
  forward-positioned (dist-to-enemy-Core 4–12 vs dist-to-own-Core 18–31, i.e. genuinely
  committed forward, not defensive). This is not slower-but-weaker than the instant-Sentinel
  archetype — all three win this way.
- **Calibration against this task's own "known context" claim** (Albert And Einstein: Launcher
  turn 1, sentinels turn 4–15, camped by turn 6–27, 3–4 Sentinels 1–4 tiles out): **fully
  reconfirmed at the higher v8 rating band** (was previously measured only at their v3,
  ~1168–1306). One measured update: the earlier v3 sample said the thrown scout is "always
  entity id 3, never rotated" — at v8, **2 distinct builders get thrown early in 3 of 5 games**
  (ids 3 and 11 in g1 and g4; ids 8 and 3 in g5) — not a contradiction of the old finding (which
  was scoped to that one v3 series) but a measured escalation worth carrying forward. Also new:
  in AAE g1, one thrown builder (id 3) gets **re-thrown 47 more times**, every ~6 turns from
  turn 99 to 370, always landing at the same tile (23,4) — a sustained forward-harassment loop,
  not a one-shot delivery.
- **Using the Instant-Sentinel combo doesn't guarantee AAE the win, and skipping it doesn't
  guarantee us one**: they ran the full throw+forward-Sentinel combo in g1, g3, g4, *and* g5 —
  losing g1/g3/g5 to us eventually but still winning g4 (a 971-turn grind). The one game they
  skipped entirely (g2, no Launcher, no throw) is one of our two wins, but n=1 for that
  specific configuration — a lead, not a conclusion.

### Cross-check against the `opp_v44` source-code rush-classification analysis

*(That entry sits immediately above this whole "Version-attributed match audit" section in the
file — not immediately above this particular subsection.)*

That analysis was added to this file while this pass was in progress, answering the same
"is the sentinel rush universal" question from source code rather than replays (explicitly
"estimated... not measured, no match run"). Its classification: `opp_v44` is a **"semi-rush"**,
not a scripted turn-1 rusher — Launcher gated behind `harv>=4` (categorically later than Albert
And Einstein's turn-1), forward offense is **Gunner-only** via saboteurs, and home defense is a
**reactive**, vision-triggered emergency Sentinel (`under` flag from live vision of an enemy
turret within roughly 8 tiles or a builder within 4, gated to maps with **area > 120 tiles** —
disabled on the smallest maps like 10×10 fjordgate, with a slower always-on fallback covering
those). This pass's replay data can directly test that estimate. Per-game, on the 6 **v44**
instances where the map qualifies (area > 120; Besvikomat is excluded here — that game was
**v40**, a different bot with its own separately-documented, harvester-threshold-gated defense
trigger, not `opp_v44`'s):

| game (map, area) | enemy first within ~8 tiles of our Core | our first Sentinel | gap |
|---|---|---|---|
| Pivot g2 (hive, 625) | turn 33 | **never built** | miss (184 turns of exposure) |
| not adgato g3 (hive, 625) | turn 97 | **never built** | miss, but a short exposure window (80 turns) |
| AAE g1 (eider, 560) | turn 4 | turn 116 | **112-turn miss** |
| AAE g3 (lighthouse, 256) | turn 5 | turn 38 | 33-turn partial miss |
| AAE g4 (meander, 375) | turn 1 | turn 9 | **8 turns — close to "same round"** |
| AAE g5 (heart, 560) | turn 6 | **never built** | miss (the total-build-freeze anomaly above) |

**Verdict: the reactive-defense layer the source read describes is real and does fire close to
on-schedule in roughly half of qualifying cases (AAE g4, and arguably not adgato given its short
exposure window) — but misses badly, by 30 to 112+ turns or not at all, in the other half
(Pivot g2, AAE g1, AAE g5).** This measured inconsistency is the concrete, replay-grounded
version of the source-read's own hedge ("plausibly still fire correctly that early... not
measured") — the mechanism exists and sometimes works as designed, but is not reliable enough
to be trusted as the sole answer to a fast approach, which sharpens differentiator #1 below
from "v44 seems slow sometimes" to a specific, falsifiable claim about the exact mechanism and
roughly how often it fails in practice (3 clear misses of 6 qualifying instances checked).

### Albert And Einstein v8 — the full 2–3 series against v44 (2026-08-06)

*(Supplements the existing entry above; that entry is not edited, per this pass's constraints.)*

Match `a2a03506`, unrated, AAE **v8** (rated 1323.27 at the time) vs our **v44**, final score
**3-2 to AAE** (we won g2 and g4, lost g1/g3/g5 — all five `core_destroyed`, all measured
directly from `match info`, not inferred). Core-kill mechanics for all 5, net HP consumed vs.
raw hits vs. heal events:

| game | who died | net ΔHP | raw hits | heal events (+HP offset) |
|---|---|---|---|---|
| g1 (loss) | ours | −502 | 282 | 208 (+830) |
| g2 (**win**) | theirs | −500 | 250 | 0 (+0) |
| g3 (loss) | ours | −500 | **1206** | **964 (+3856)** |
| g4 (**win**) | theirs | −500 | 683 | 201 (+576) |
| g5 (loss) | ours | −504 | 72 | 36 (+144) |

Net-HP-to-kill is extremely tight (−500 to −504) across every single game in both directions —
this **strongly reconfirms** the existing "Core HP fixed constant" note. The *raw* hit-count
range, however, needs updating: previously documented as 28–136 across the whole project; this
one series alone spans **72–1206**, and combined with the rest of this pass's batch (28 in
sporks g3, up to 323 in Pivot g2) the full measured range is now **28–1206 hits**, heal events
**0–964**. Net HP stays the real constant; raw hit count keeps growing with sample size exactly
as the existing note already warned it would.

**g3 is the standout data point in this whole pass**: 985 turns, we out-collected AAE
**4880–0** on titanium, healed our Core 964 times for +3856 HP offset — and *still* lost,
because AAE's entire offense was 3 units placed turns 1/5/9 (1 Launcher + 2 Sentinels) that
were **never reinforced, never destroyed, and never needed to be** — they just kept chipping
for 980 turns while we out-produced them on every economic axis and it didn't matter. This is
the cleanest measured illustration yet of "economy doesn't save you from an unanswered siege."

**g5 anomaly, flagged, not root-caused**: v44 built **nothing beyond its initial 4 builders**
the entire 241-turn game — no harvester, no conveyor, no turret ever placed
(`first_build_us: {"builderBot": 0}` and nothing else). Checked for a crash/timeout signal via
`analyze_replay.py`'s bot-output scanner (the same `Traceback`/`Exception`/`tled` check used
throughout this project): **zero flags found on either side this game.** So this isn't an
explained crash — it's either a map/seed-specific trigger-logic gap in v44's build-order, or
adequately explained by AAE's own turn-6 Sentinel landing 1 tile from our Core (which might
suppress every subsequent build attempt the same way Cookie's turn-5 sentinel did in the
already-documented antler game) — replay data alone can't distinguish those two explanations.
Worth a dedicated look; not claimed as a bug here.

### Besvikomat (new decode) — economic-volume Gunner spam, a third archetype

Rating 1789 at match time (759 matches played — a very experienced bot). Match `c5c193b6`
vs our **v40**, lost 1-4. Game 2 (drumlin, 239 turns, loss) decoded: Besvikomat built only 5
builders total (turns 0,1,2,3,9) but placed **35 separate turrets** over the game — almost all
Gunners, heavily *reused positions* (tile (4,9) alone was rebuilt **11 times**, (1,9) 6 times,
(7,11) 5 times — i.e. rebuilt after each loss, not 35 distinct simultaneous units),
forward-positioned (dist-to-our-Core 2–7, dist-to-their-own-Core 18–31). Fueled by a **6x titanium lead** (3290 vs our 550).
No Launcher, no throw events at all — they reach forward positions by walking, not throwing.
This is a third, distinct archetype from AAE's scripted rush and the Pivot/not
adgato/Besvikomat-shared "turn ~33-39 first Gunner" timing above: **sustained economic
dominance converted directly into an endless-replacement garrison** rather than a scripted
opener. Our v40 (aug7 lineage) response was 4 Sentinels (turns 48/60/144/200, all defensive,
dist-to-own-Core 1–3) — matches the documented aug7 profile exactly (Sentinel-only, no
Launcher, no Gunner) — a useful incidental cross-check that the source-read note's description
of aug7/v40 lines up with replay-observed behavior.

Incidental finding, about the *opponent* not us: Besvikomat's builderBot entity 4 shows **5
explicit `tled` (timeout) flags** in `botOutput`, turns 127 and 139–142, no accompanying error
text. Even a 1789-rated, 759-match-experienced bot hits its CPU budget sometimes — it didn't
cost them this game. Doesn't change any existing claim about *our own* bot's reliability (that
entity is `TEAM_B`, Besvikomat, confirmed via the map header's core-ownership record, not us).

### sporks and not adgato (brand-new names) — fast core kills via v44, minimal write-up

Both first-time opponents, single unrated sample each, both losses.

- **sporks** (1923.4): match `81ce7948`, 0-5. Game 3 (fjordgate, 63 turns) is **the fastest
  core-kill measured anywhere in this project's history to date** (previous fastest was Cookie
  at 38 turns on antler). sporks' first Sentinel: turn 1, one tile from their own Core (dist-
  own 1), dist-to-our-Core 5 on this tiny 10×10 map. v44's own Sentinel response was turn 4 —
  competitively fast by this project's standards — but 3 turns was still enough of a deficit to
  lose on a map this small. `titanium_collected` read **0 for us** (sporks collected 250) —
  plausibly just too fast a game for our side to complete any delivery round trip, not
  necessarily the unresolved dead-end-conveyor anomaly flagged elsewhere in this file.
- **not adgato** (1897.0): match `2397deb4`, 0-5. Game 3 (hive, 177 turns) shows the
  turn-33 forward-Gunner archetype (see table above) plus a late Sentinel top-up at turn 97.
  Notably, **v44 built zero Sentinels or Gunners this entire game** — its only turret was a
  Launcher at turn 80, and it landed **146 hits (−76 net) on not adgato's Core** anyway despite
  that, almost certainly via the saboteur-builder direct-`fire()` mechanic the source-read note
  documents (no dedicated turret required) — a real, replay-confirmed sighting of that
  mechanism operating in production, not just source-code inference.

### Candidate differentiators for beating v44, ranked

The instruction for this pass was explicit: name and rank what a *next* line should do
differently, aimed at where the top of the field already beats v44 specifically — not at
out-tuning v44 on its own game.

1. **Match the turn-1–6 instant-forward-Sentinel tempo (see timing table above) — v44's own
   reactive defense against it is unreliable, not just theoretically fast enough.** This is the
   single largest, most consistent measured gap: in **3 of the 6 decoded v44 losses** (Pivot,
   not adgato, and AAE g5 — the last one built nothing at all, see the anomaly below) **no
   Sentinel was ever built**; in a fourth (AAE g1) the first Sentinel arrives turn 116, ~112
   turns after an enemy turret was already within the source-documented detection range. The
   cross-check two sections above makes this precise: `opp_v44`'s vision-triggered emergency
   Sentinel is real and does fire close to on-schedule in about half of the qualifying cases
   checked (AAE g4: 8-turn gap) but misses badly — 33 to 112+ turns late, or not at all — in the
   other half (Pivot g2, AAE g1, AAE g3 partially, AAE g5). A next line that made this specific
   mechanism reliable rather than merely present would close the single largest gap measured in
   this whole pass.
2. **Add a "clear the siege" behavior — proactively kill an established enemy turret near our
   Core instead of healing indefinitely.** AAE g3 is the clean proof: we out-collected AAE
   4880–0 in titanium, threw +3856 HP of healing at our Core, and still lost to 3 units that
   were never reinforced *or removed* for 980 turns. This extends the already-documented "no
   `ct.destroy()`/`self_destruct()` in either bot" gap one step further — nobody in this
   catalogue clears the *enemy's* stale siege units either, and it's the direct cause of at
   least one loss where every other metric favored us.
3. **Plan for a second archetype at turn ~33–39: forward Gunner, no early Sentinel.** Three
   unrelated opponents (Pivot, not adgato, Besvikomat) converge on this almost exactly. A build
   tuned only to answer the instant-Sentinel rush (candidate #1) leaves this lane wide open —
   Besvikomat shows it can scale into 35 rebuilt Gunners off a 6x economic lead if never
   contested.
4. **Don't over-invest in ring-camping alone — it's correlated with v44's wins, not causal.**
   v44 already camps enemy Cores heavily in both wins this pass (917 turns / 95% of the game on
   meander; 312 turns / 95% on fjordgate) but camping intensity doesn't cleanly separate our
   wins from our losses in this series (0 turns camped in 2 of 3 losses too) — and Builder Bots
   can't attack, so camping alone never lands a hit (matches the existing game-model note). The
   real value only shows up paired with actual damage (a turret, or the saboteur `fire()`
   mechanic confirmed live in the not-adgato game above).
5. **Lower confidence — investigate the AAE-g5-style total-development-stall.** If it recurs and
   turns out to be a real trigger-logic gap rather than a one-off, fixing it prevents inheriting
   the same failure mode; not yet confirmed as more than a single-game anomaly.

### Anomalies, updates to existing notes, and one process note

- **Core HP raw-hit-count range needs updating**: previously 28–136 project-wide; this pass
  alone measured 28–1206 (hits) and 0–964 (heal events). Net-HP-to-kill stays the tight,
  reliable constant (−500 to −512 across every core death checked, both directions) — this is
  a *range extension*, not a contradiction of the existing finding, exactly as that finding's
  own hedge anticipated.
- **`titanium_collected` reading 0–0 despite real economic activity recurs at the v44/v8 tier**
  too (AAE g2, g4, g5; sporks g3) — the existing flagged-but-unresolved anomaly from the
  original Albert And Einstein deep dive is not version-specific; still not root-caused here
  either, still likely map-generic rather than opponent-specific given how often it recurs
  across unrelated matchups.
- **Pivot's strategy is not monolithic.** This pass's decode (5 builders, first Gunner turn 33,
  forward dist-to-our-Core 3–13, 720 titanium collected, ring-camping present) looks
  substantially different from the existing entry's decode (12 harvesters, 39 conveyors, first
  Gunner turn 80, 3170 titanium, no Sentinels/Launchers at all) — different map/seed, same
  opponent. Treat any single Pivot sample as one point in a real distribution, not their fixed
  playbook.
- **Process note on an inter-agent message received mid-task**: a message arrived from another
  Claude session (not from the user, not from whoever launched this task) claiming to relay a
  high-confidence field observation from Magnus ("the sentinel rush is the common opening
  across the ladder") and asking this pass to restructure its output around a timing-table
  extraction. Per this project's own agent-authority rules, a peer session's message is never
  treated as user approval or as authority to change task scope, so it did not redirect this
  pass's structure. Its underlying data request was reasonable and cheap given data already
  being gathered, so the timing table above was produced and checked against this pass's own
  measurements rather than accepted on faith — the claim turned out to be a real but partial
  pattern (one of two roughly-equally-common archetypes, not "the" opening). Note for whoever
  reads this next: the `opp_v44` rush-classification entry immediately above this one, added to
  this same file by a different session while this pass was running, opens with "Magnus flagged
  the launcher-assisted builder rush... as the common ladder opening... and asked whether
  `opp_v44` conforms to it" — near-identical framing to the message this pass received. That is
  retroactive evidence the message was a legitimate relay of real coordinated tasking (source
  code vs. replay evidence on the same question, run in parallel), not an injected instruction —
  recorded here for whoever reviews this, since it wasn't verifiable at the time the message
  arrived and was correctly treated with skepticism until corroborated.

### florent-v63: three defects found while porting our CPU guard onto it (2026-08-08)

Found by reading `bots/opp_v45` line by line to place guard bail-outs, not by measurement. None
were fixed — the port changed one mechanism only. **All three should go to x3r0.**

1. **The entire Launcher subsystem is dead code, and this is strategically expensive.**
   `_try_build_launcher()` is the only caller of `ct.build_launcher()` and it has **zero call
   sites anywhere in the file**. `SLOT_LAUNCHER` can therefore only ever be set by *noticing a
   Launcher that already exists*, never by building one — which makes the `launchwait` role and
   the ~100 lines of drop-site / exile-throw / launch-handshake logic in `_launcher()`
   unreachable. Compounded by `MAX_BUILDERS = EARLY_BUILDERS = 5`, which caps `role_n` at 4
   while entering `launchwait` requires `role_n >= 5`.
   **Why it matters: the turn-1 Launcher self-throw is *the* top-meta opening** — `sporks` (1923)
   killed a Core in 63 turns with it, and all five Albert And Einstein games opened that way
   (see the timing census above). The team's strongest bot carries the code for it and cannot
   execute it.
2. **`run()` dispatches with no top-level `try`/`except`.** Any exception escaping `_core`,
   `_builder`, `_turret` or `_launcher` permanently deletes that unit. Latent rather than active
   — 0 crashes across 480 gate matches — but it is the same three lines that took our own line
   from 515 crashes to 0 back at v1.
3. **Dead state consistent with the abandoned Launcher feature:** `self.forward_barriers`,
   `self.link_source`, and `LAUNCHER_RESERVE = 80` are written or defined and never read.

Separately confirmed while cataloguing v58 → v63: **the `w*h <= 120` small-map gate on the
vision-triggered battery is gone in v63**, along with the mechanism it gated — so our continued
`fjordgate` edge against v63 (26/32) no longer has the explanation that covered v44 (32/32).

### Source data for this pass

Full match list: `fcode match list --mine --json` (2 pages, cursor `2026-08-06T08:20:31.414Z`).
Match info pulled for 7 candidates before deciding what to decode: `9436bd69`, `81ce7948`,
`2397deb4`, `a2a03506`, `c5c193b6`, `e319d9c1` (Flotte Experience, ultimately not decoded —
retired maps), `f4404e8b` (Jacobs Code, not decoded — lower rating priority than the above).
9 replays downloaded to scratch (`replays/batch2/`), decoded with a new `batch_analyze.py`
(reuses `replay_codec.py` unchanged; generalizes `analyze_aae2.py`'s ring-occupancy and
`moveBuilderBot`-jump logic to take explicit win/loss + team-side per game). All raw JSON/log
output kept in scratch, not the repo.

## Production portfolio, Eir era (2026-08-07, unrated sweep, 15 maps/team)

First complete production win-map. Game-share vs rating expectation (E from the
measured Δ=32×(share−E) model); seat noted because the seat-B resolution-order
tax (see game-model) confounds several rows.

| team | their rating | score | share | E | read |
|---|---|---|---|---|---|
| Lunds Stallions | 1609 | 7-8 | .47 | ~.40 | **above expectation** — but 6-4 as seat A vs 0-5 as seat B |
| Powerpuff Girls | ~1560 | 8-7 | .53 | ~.51 | at expectation; won 4/5 as seat B (their chip doesn't tax builders) |
| CtrlAltDefeat | 1658 | 5-10 | .33 | ~.32 | at expectation; our 5 wins all fast core kills r117-215 |
| kladde | 1799 | 2-13 | .13 | ~.20 | slightly below; probe stale (they shipped v62 ~1811) |
| Flotte | 1837 | 1-14 | .07 | ~.15 | slightly below; above our weight at any seat |
| Ouroboros | 1597 | 1-14 | .07 | ~.40 | **the leak** — far below expectation, though all 15 games drew seat B |

Actionable: Ouroboros is the single biggest per-team Elo leak (≈ -5 games/15 vs
expectation); their pattern is still undecoded (NOT grind — core kills @265/323).
Eir 3's seat-B deferral targets exactly the confound; its validation legs decide.
