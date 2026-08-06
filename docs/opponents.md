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
