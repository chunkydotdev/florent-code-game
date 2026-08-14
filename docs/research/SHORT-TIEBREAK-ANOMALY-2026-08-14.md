# The short `titanium_collected` rows: MUTUAL CORE DESTRUCTION, and the tiebreak cascade runs on it

**Research arm, 2026-08-14. Wall clock at start of the read: `2026-08-14T19:21:54Z`
(`date -u`). Live version at time of writing: v140 "Loki v10" = `bots/_v223sealrepair`
(`corpus/version_trees.tsv`, activated `2026-08-14T11:37:38Z`). Repo HEAD
`0ebee59a705328d8fa00b6c666226b19249c1e06`.**

**Corpus freshness:** `corpus/ladder_games.tsv` — 4,920 rows, newest `created`
`2026-08-14T18:52:59.715Z`, file mtime `2026-08-14T21:08:04` local. ~29 minutes
behind wall clock at read time; well inside one 20-minute pairing cadence plus
ingest, so not stale for this question.

---

## RULING

**(a) — there is a win path we did not have written down, and it is not a labelling
artefact and not a decode error.** A `titanium_collected` verdict at turn 140 means
exactly what it says: **both cores were destroyed in the SAME round, so
`core_destroyed` could not name a winner, and the engine fell through to the ordinary
tiebreak cascade (`titanium_collected` → harvesters → `titanium_stored` → coinflip) at
whatever round that happened.** The tiebreak ladder is therefore **NOT gated on
reaching the turn limit** — it is the general "no core-kill winner" resolver, and a
double kill triggers it mid-game.

The evidence is a perfect two-way discrimination over **42,035 archived replays**
(every `.replay26` on this box, rated + unrated + other teams' games), reading core HP
directly off `updateHp` deltas:

| replay-side core state | n | `winCondition` emitted |
|---|---|---|
| exactly ONE core reaches hp ≤ 0 | **33,830** | `core_destroyed`, **33,830 / 33,830** |
| NEITHER core reaches hp ≤ 0 | **8,183** | never `core_destroyed`; all at 1,000 rounds |
| **BOTH cores reach hp ≤ 0** | **22** | **never `core_destroyed`** — 16 `titanium_collected`, 5 `titanium_stored`, 1 `harvesters` |

and the set identity that closes it:

```
{ archived replays with cond != core_destroyed AND rounds < 1000 }  ==  { archived replays with BOTH cores dead }
   22 == 22, symmetric difference EMPTY
```

**All 22 have `zA == zB` (same round) and `rounds == z + 1`.** No double kill in the
archive was ever labelled `core_destroyed`; no single kill was ever labelled anything
else. **The instrument produces the other verdict 33,830 times, so it has been seen to
check** (D1 / the corpus-howto complement-group rule).

Branch **(b) truncation is dead**: platform `turnsPlayed` equals the replay's own
`len(turns)` in **3,615 / 3,615** rated rows with an archived replay, and the two short
games contain a complete, coherent end-state (final `updatePlayers`, both cores
removed via `removeEntity` in the last round). Branch **(c) bad decode is dead**: the
corpus does not decode `cond`/`turns` at all — `tools/corpus/ladder_meta.py:83-84`
copies `winCondition` / `turnsPlayed` straight off `fcode match info --json` — and a
live re-fetch today reproduces `cond=titanium_collected, turns=146` for the 2026-08-14
game, while the replay binary's OWN undeclared field 6 (`Replay.winCondition`) agrees
with the platform on **3,615 / 3,615** rated rows.

**The 25 `cond=error` rows are a different animal entirely and are almost certainly
THEIR bot failing to load, not a crash we induced** — see §4. `error` is not even in
the engine's win-condition string table.

---

## 1. Re-derivation of the relayed counts — the relay is EXACT

**Population: `corpus/ladder_games.tsv`, one row per GAME of our RATED ladder matches,
4,920 rows, `created` spanning 2026-08-05T19:42:43Z → 2026-08-14T18:52:59Z.** This is
the authority for rated denominators; `meta_join` is not (it pools unrated).

```bash
.venv/bin/python - <<'EOF'
import csv, collections
rows=list(csv.DictReader(open('corpus/ladder_games.tsv'),delimiter='\t'))
print("total rows:",len(rows))
print("cond dist:",collections.Counter(r['cond'] for r in rows).most_common())
tc=[r for r in rows if r['cond']=='titanium_collected']
print("cond=titanium_collected:",len(tc))
print("  turns dist:",collections.Counter(r['turns'] for r in tc).most_common(10))
err=[r for r in rows if r['cond']=='error']
print("cond=error:",len(err),"; turns<1000:",sum(1 for r in err if int(r['turns'])<1000))
EOF
```

```
total rows: 4920
cond dist: [('core_destroyed', 3773), ('titanium_collected', 1060), ('harvesters', 44),
            ('error', 25), ('titanium_stored', 18)]
cond=titanium_collected: 1060
  turns dist: [('1000', 1058), ('140', 1), ('146', 1)]
cond=error: 25 ; turns<1000: 25
```

**The relay is reproduced digit-for-digit: 1,060 `titanium_collected`, 1,058 at exactly
1,000, exactly two short (140 and 146), 25 `cond=error` all with turns < 1000.** No
discrepancy to report.

Context for the denominators, same population (n = 4,920 rated game-rows): our game
share **2,528 / 4,920 = 51.38%**; **1,120 / 4,920 = 22.8%** of rated games reach turn
1,000; median turns 233.

*(Note the tiebreak-key mix here differs from the 1,055-game figure in `CLAUDE.md`
because that figure conditioned on r1000 games only. Over ALL 4,920 rated rows the mix
is core_destroyed 76.7%, titanium_collected 21.5%, harvesters 0.9%, error 0.5%,
titanium_stored 0.4%.)*

## 2. The two short rows, in full

Both are **wins for us**, both on `archipelago`, both 26×26 with cores at (5,5) and
(19,19).

| field | game A | game B |
|---|---|---|
| `match` | `f72a02b0-5361-4370-a98e-07b6d1f3e0fd` | `006f3c12-9aec-46e7-916c-2e2bd252bf87` |
| `created` | `2026-08-12T10:12:59.502Z` | `2026-08-14T09:12:59.675Z` |
| `opp` | Powered by SmartFridge | diverge |
| `oppver` | 59 | 20 |
| `ourver` | **115** (a TEAMMATE's ship — x3r0's ammo pre-buy; no local tree, `version_trees.tsv`) | **139** = `bots/_v218mapfix` ("Loki v9") |
| `ourbef` / `oppbef` | 1661.85 / 1644.13 | 1759.10 / 1751.73 |
| `map` | archipelago | archipelago |
| `winner_seat` | b | a |
| `won` | 1 | 1 |
| `cond` | titanium_collected | titanium_collected |
| `turns` | **140** | **146** |
| `s3` | `..._game_3.replay26` | `..._game_5.replay26` |

⚠ `winner_seat` is the WINNING seat, not ours (TRAP 7). Since we won both, it happens
to equal our seat here: we were **B** in game A and **A** in game B.

Both replays are in `replay_archive/`.

## 3. The replays — both cores died, in the same round, and the tiebreak decided it

`tools/corpus/replay_autopsy.py` on both files, plus a purpose-built HP trace over
`Update.updateHp` (field 5) and `Update.removeEntity` (field 3) restricted to the two
core entity ids from `Map.cores`:

```
f72a02b0..._game_3.replay26  rounds=140 winner=B cond=titanium_collected
   core A id=1 final_hp=-8  first_hp<=0 at round 139  removeEntity at 139
   core B id=2 final_hp=-2  first_hp<=0 at round 139  removeEntity at 139

006f3c12..._game_5.replay26  rounds=146 winner=A cond=titanium_collected
   core A id=1 final_hp= 0  first_hp<=0 at round 145  removeEntity at 145
   core B id=2 final_hp=-6  first_hp<=0 at round 145  removeEntity at 145
```

**Both cores cross zero in the same round and both receive a `removeEntity` in that
round.** The game did not "simply stop": it ended because there was no core left on
either side. `replay_autopsy`'s independent damage ledger reconciles in all four cases
(`attributed total == summed UpdateHp deltas`, MATCH), so the HP arithmetic is not the
weak link.

**And the tiebreak key visibly decided the winner.** Last `updatePlayers` in each game:

| game | A `titaniumCollected` | B `titaniumCollected` | winner |
|---|---|---|---|
| f72a02b0 g3 | 910 | **1,310** | **B** (us) |
| 006f3c12 g5 | **1,260** | 1,010 | **A** (us) |

The winner is the team with the higher key-1 value in both, margins 400 and 250 Ti.
That is the documented cascade running, not a coin flip and not a mislabel.

Mechanically both were **mutual sieges**: in f72a02b0 g3 their sentinel ground our core
down 18/round from r41 while our gunners ground theirs down from r26 (both cores were
being healed the whole time — 98 and 207 `builderHeal` events); in 006f3c12 g5 both
cores died to sentinel fire. Neither is a launcher/kidnap effect.

### The class-level control — this is what makes it a ruling and not a story

Swept **every** archived replay (42,035 files, 0 decode failures, ~108 s wall on 10
processes) for the same signature:

```bash
# tools used: tools/replay_census.py primitives (fields/read_pos), reading
# Replay.map.cores -> core ids, then Update.updateHp deltas (64-bit two's complement)
# and Update.removeEntity, per round, for those ids only.
```

```
archived .replay26 files: 42035   decoded ok: 42035   errors: 0
cond dist (ALL archived replays): core_destroyed 33830 · titanium_collected 7695
                                  harvesters 401 · titanium_stored 107 · coinflip 2

BOTH cores hp<=0 : 22 of 42035          (0.052%)
  all 22 have zA == zB                  TRUE
  all 22 have rounds == z+1             TRUE
  cond of the 22: titanium_collected 16 · titanium_stored 5 · harvesters 1
core_destroyed n=33830 : with both cores dead = 0 ; with neither core dead = 0
{cond != core_destroyed AND rounds < 1000} == {both cores dead} : SET EQUAL (22 == 22)
```

**The full tiebreak ladder is observable inside the double-kill class alone**: 16 games
settled on key 1, 1 on key 2 (harvesters), 5 on key 3 (`titanium_stored`) — exactly the
documented cascade, and the same cascade `CLAUDE.md` describes for the r1000 case.
*(Side observation, first sighting in this corpus: **2 games carry `cond=coinflip`**, key
4, both at exactly 1,000 rounds.)*

### The 22, attributed (join on `corpus/meta_join.tsv` by replay filename)

| rounds | cond | fixture | teams (version at match) | ours? |
|---|---|---|---|---|
| 53 | titanium_collected | unrated | Banminary v59 vs gsxWins v22 | — |
| 63 | titanium_collected | unrated | The Bisons v4 vs SmartFridge v35 | — |
| 63 | titanium_collected | unrated | The Bisons v4 vs SmartFridge v33 | — |
| 70 | titanium_collected | unrated | gsxWins v22 vs **OpenSverige v104** | **WIN** |
| 79 | titanium_collected | unrated | The Bisons v4 vs **OpenSverige v102** | loss |
| 89 ×3 | titanium_stored | unrated | SmartFridge v30/v33/v35 vs diverge v12 | — |
| 98 | titanium_stored | unrated | **OpenSverige v65** vs Team 48 v16 | **WIN** |
| 101 | titanium_collected | unrated | SmartFridge v38 vs diverge v12 | — |
| 105 | titanium_collected | unrated | The Bisons v5 vs Jython v113 | — |
| **140** | **titanium_collected** | **RATED** | SmartFridge v59 vs **OpenSverige v115** | **WIN** |
| **146** | **titanium_collected** | **RATED** | **OpenSverige v139** vs diverge v20 | **WIN** |
| 153 | titanium_collected | unrated | SmartFridge v35 vs Big O v7 | — |
| 173 ×3 | titanium_collected | unrated | Leviathan v55 vs SmartFridge v30/v33/v34 | — |
| 175 | titanium_collected | unrated | Torsko v39 vs CtrlAltDefeat v132 | — |
| 354 | titanium_collected | unrated | Askar City v87 vs **OpenSverige v104** | **WIN** |
| 405 | harvesters | unrated | I Stone v22 vs **OpenSverige v103** | loss |
| 407 | titanium_stored | unrated | SmartFridge v67 vs **OpenSverige v121** | **WIN** |
| 642 | titanium_collected | unrated | SmartFridge v30 vs **OpenSverige v114** | loss |

**8 of the 22 involve us; we won 5 of those 8.** Us-only, n = 8 — a number to notice,
not to bank.

**Two independent corroborations that this is a general engine behaviour and not
something about our bot:**
1. **14 of the 22 are games we were not in at all** (other teams' unrated matches in our
   archive) — the phenomenon reproduces across SmartFridge, diverge, The Bisons,
   Leviathan, Torsko, CtrlAltDefeat, Banminary, gsxWins.
2. The engine's own condition string table, read off the shipped `.so`
   (`.venv/lib/python3.13/site-packages/fcode/fcode_engine.cpython-313-darwin.so`,
   engine pinned 2.3.6), is one contiguous literal:
   `resigned coinflip core_destroyed timeout titanium_stored harvesters titanium_collected`
   — i.e. the tiebreak conditions are peers of `core_destroyed` in a single enum, not a
   turn-limit-only branch. *(Inference from a string blob, not from disassembled control
   flow: this build's symbol table carries only std/backtrace symbols, so the resolver
   function could not be located by name here. The 42,035-replay behavioural result is
   the load-bearing evidence; this is corroboration.)*

**Field control:** `corpus/league_games.tsv` (3,705 games between OTHER teams,
2026-08-03 → 2026-08-09) contains **426 `titanium_collected` games and 0 with
turns ≠ 1000** — consistent with a ~0.05% base rate over a 3.7k sample.

## 4. The 25 `cond=error` rows — a load failure of the OPPONENT's submission, not a crash we caused

```bash
# same file, filter cond=='error'
```

Every one of the 25 is homogeneous:

* **`turns` = 0 in 25 of 25.** The game never ran a single round.
* **`s3` (replay key) is empty in 25 of 25.** No replay was produced, so none is in the
  archive — which is why §3's sweep cannot see them.
* **`won` = 1 in 25 of 25.** Every single one was awarded to us.
* **5 matches, 2 opponents:** `arsonist duck` × 4 matches (20 games), `Kleos` × 1 match
  (5 games).
* **`oppver` = 1 for all 20 arsonist duck games** (their debut submission) and `12` for
  the 5 Kleos games.
* **All 25 fall on a single day, 2026-08-06**, between `03:52:43Z` and `12:32:43Z`.
  Our version rotated across them (v20 ×10, v34 ×5, v38 ×5, v40 ×5) while the
  OPPONENT's version did not — the constant is theirs, not ours.
* Maps are scattered across 18 different maps — no map clustering.

**Ruling on this class: THEIR bot failed to start, and the platform forfeited the match
to us.** The discriminating facts are (i) **turns = 0** — our units never executed, so
nothing we could do had happened yet, which rules out any crash we induced (all our
approved crash-induction mechanisms require a launcher to exist and a throw to land,
i.e. round ≥ 8 at the very earliest); (ii) **25/25 in our favour** — a generic
engine/platform fault would not be systematically one-sided; (iii) the invariant is
**the opponent's version**, not ours, not the map, not the seat.

**`error` is not one of the engine's win conditions.** It does not appear in the engine
string table quoted above, and it appears **0 times in the 3,705 other-team games** in
`corpus/league_games.tsv` and **0 times in 42,035 archived replays**. Best reading: it
is a *platform-level* record for a match whose game never reached the engine — a
submission that failed to import (`main.py` missing, no top-level `class Player`, a
syntax/import error), or a container that failed to start. **Inference**, on the
evidence above.

**What would settle it if this is ever load-bearing:** `fcode match info <id> --json`
carries a match-level `errorMessage` field (it is `null` on healthy matches — verified
today on `006f3c12`). Pulling it for the five error matches
(`48807d12`, `fb6400af`, `9216594c`, `f2fbfb76`, `74d30f5c`) would name the failure
directly. Not done here because the class is 25 games from 8 days ago against two
opponents, all wins, with no live decision hanging on it.

⚠ `corpus/league_games.tsv` covers 2026-08-03 → 2026-08-09 and contains **zero** games
involving arsonist duck or Kleos, so it is NOT a control for whether those two teams
also errored against other opponents. That control does not exist in the corpus today.

## 5. Is `archipelago` special? No — the 2-of-2 clustering is a coincidence at n = 2

Population: all 4,920 rated game-rows.

| map | n | our win% | % at turns=1000 | median turns |
|---|---|---|---|---|
| **archipelago** | **311** | **52.7** | **19.0** | **160** |
| antler | 315 | 59.7 | 18.7 | 223 |
| atoll | 304 | 53.0 | 27.0 | 285 |
| … (15 maps ≥ 240 rows) | | | | |
| ALL rated | 4,920 | 51.4 | 22.8 | 233 |

archipelago's cond mix (n = 311): `core_destroyed` 249, `titanium_collected` 61,
`error` 1. Nothing anomalous — its `titanium_collected` share (19.6%) is normal, its
win rate (52.7%) is within a point and a half of our overall 51.4%.

The one thing that *is* mildly distinctive is that **archipelago is a fast map**: median
160 turns, second-lowest of the fifteen high-volume maps. A fast map is a map where both
cores are under fire early, which is weakly consistent with a mutual kill — but it is
not where the near-misses concentrate. Measuring "how close did we come to a double
kill" as *the surviving core's final HP* over the 3,068 rated `core_destroyed` games
with an archived replay:

```
median surviving-core HP = 500      (i.e. the usual game is not close at all)
surviving core HP <=  10 :    4  (0.13%)
surviving core HP <=  20 :   18  (0.59%)
surviving core HP <=  50 :   57  (1.86%)
surviving core HP <= 100 :  122  (3.98%)
```

Per map, archipelago's `HP ≤ 20` near-miss rate is **1 / 214 = 0.5%** — rank 11 of the
15 high-volume maps, below atoll (1.9%), saga (1.2%), lighthouse (1.1%). **archipelago
is not the tight-race map.**

**Coincidence arithmetic:** P(two independently drawn rated game-rows share a map)
= Σ p_m² = **0.0499** over 43 maps; archipelago's own share is 311/4,920 = 6.32%. Two
events landing on the same map is a ~5% coincidence and on *archipelago specifically* a
~0.4% one — neither is evidence at n = 2, and the wider 22-game class spreads over at
least **nine distinct map geometries** (dimensions × core positions), so the map is not
the mechanism. *(Caveat on that count: the 26×26 / cores-(5,5)-(19,19) fingerprint that
9 of the 22 share is **not** unique to archipelago — a 1,500-row random sample of rated
archived games shows both `archipelago` (107) and `snowflake` (87) carrying it. So "9 on
archipelago" would be wrong; it is 9 on {archipelago ∪ snowflake}.)*

---

## WHAT THIS CHANGES

**Honestly: for the ladder, close to nothing. For our model of the engine, one real
correction, and it is the kind that quietly poisons cuts.**

1. **CORRECTION TO THE ENGINE MODEL (durable).** The tiebreak cascade is *not* the
   turn-limit resolver. It is the **no-core-kill-winner** resolver, and a simultaneous
   double kill invokes it at whatever round it happens. This should be stated wherever
   we describe win conditions. It also means **`titanium_collected` can be the deciding
   key in a game that ended at round 53** — the shortest instance in the archive.

2. **A CUT HAZARD, and it is the practical one.** Any analysis that uses
   `cond != 'core_destroyed'` as a proxy for *"this game went the distance"*, or
   `cond == 'titanium_collected'` as a proxy for *"r1000 tiebreak defeat"*, mislabels
   the double-kill class. Rated impact today is **2 of 1,060** (0.19%) — negligible in
   any bar we currently quote. **But the correct filter is `turns == 1000`, not the cond
   string, and it costs nothing to use it.** Same shape as the corpus's known
   name-vs-content traps: a field whose name implies a semantic (`titanium_collected` ⇒
   "went to time") that its content does not carry.

3. **KILL-ROUND ACCOUNTING GETS SLIGHTLY BETTER, NOT WORSE.** Under `R1000_IS_DEFEAT`
   these two rows are **not** r1000 tiebreak games — they are **kills at r140 and r146**,
   both inside the <r250 target band, and we won both. Anything that binned them as
   tiebreak wins (i.e. as defeats-in-disguise) was wrong in our favour by two games.

4. **A PLANK IDEA, offered as a hypothesis and explicitly NOT a finding.** On a mutual
   kill the game is decided by `titanium_collected` — so in the exact scenario where a
   pure-rush build trades cores, **economy is the tiebreak that pays**. We won 5 of the
   8 double kills we were in, and both rated ones, with key-1 margins of 400 and 250 Ti.
   **n = 8, us-only, and the class is 0.05% of games** — this is nowhere near a reason to
   buy economy, and it must not be cited as one. It is at most a footnote against
   stripping harvesters to literally zero in a rush variant. Per point 6 of the
   programme, nothing here retires or opens a road: it has no live-game backing as a
   *plank*.

5. **NOTHING TO DO ABOUT `cond=error`.** 25 games, all wins, all on 2026-08-06, all
   caused by two opponents' submissions failing to start. It is not a crash we induced
   and not a channel we can steer — we cannot make an opponent's *submission* fail to
   import. The only residue is a data note: those 25 rows have `turns=0` and no replay,
   so they are dead weight in any turn-distribution or kill-round cut and should be
   filtered out of both. They are currently 25 of 4,920 rated rows (0.51%) and they all
   count as wins in our 51.38% game share — **which is correct, they were awarded to
   us**, but a reader should know 25 of our 2,528 wins were walkovers.

6. **ONE THING THIS DOES *NOT* CHANGE, stated so nobody re-derives it:** it is not an
   exploit and not a lever. A double kill is a coincidence of two independent sieges
   landing in the same round; there is no call we can make to force one, and forcing one
   would be strictly worse than landing the kill a round earlier.

---

### Reproduction

All numbers above come from `corpus/ladder_games.tsv` (rated denominators),
`corpus/league_games.tsv` (field control), `corpus/meta_join.tsv` (attribution of
non-rated archived replays — used for *identity*, never for a rated denominator), and a
direct sweep of `replay_archive/*.replay26` built on `tools/replay_census.py`'s
`fields` / `read_pos` primitives. The two per-game deep reads used
`tools/corpus/replay_autopsy.py` unmodified. Live spot-check:
`.venv/bin/fcode match info 006f3c12-9aec-46e7-916c-2e2bd252bf87 --json`
(`errorMessage: None`, game 5 archipelago `cond=titanium_collected turns=146
winnerSide=a`) — note this call returns `teamBVersion: None`, the documented `match
info` defect; opponent versions above come from `ladder_games.oppver` /
`meta_join.teamXVersion`.

Sweep scripts were scratch (`.../scratchpad/coretrace.py`, `allsweep.py`) and are not
committed; the method is ~40 lines and is described in full in §3 so it can be rebuilt
in minutes. **If this class is ever queried again, the right fix is to add a
`both_cores_dead` / `core_death_round` pair of columns to the corpus rather than
re-sweeping 42k replays.**
