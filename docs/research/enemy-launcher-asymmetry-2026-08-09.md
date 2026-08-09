# Are enemy launchers eating our raiders? — answered in one pass, and the answer is NO for the opponent that motivated the question

**Research arm, session 25, 2026-08-09 ~17:3x CEST.** The builder proposed a cut:
*"whether opponents' launchers are eating OUR raiders at a rate that explains our 5.8%
arrival against Ouroboros. THAT is worth a cut and it aims straight at incidence."*
**It did not need a cut — the corpus answers it directly.** Written up because a
negative that closes a proposed deliverable is worth as much as the deliverable.

**Version tag.** Live slot **v94** = `bots/_v115dodge`, treehash `6ae6871c`. Corpus git
sha `7418e13`. Frozen copies of `throws.tsv` (100,047 lines), `builds.tsv` (92,802),
`join.tsv` (1,446 → **1,445 attributed games**) taken before analysing. Zero downloads.

---

## THE ANSWER: **Ouroboros has never built a launcher and has never thrown anything**

| opponent | attributed games | **their** launcher builds | our launcher builds | **throws of OUR bots by THEM** | throws of their bots by us |
| --- | ---: | ---: | ---: | ---: | ---: |
| **Ouroboros** | **105** | **0** | 72 | **0** | 2,018 |
| CtrlAltDefeat | 85 | 80 | 70 | **0** | 473 |
| Kings College Munich | 115 | 79 | 93 | **0** | 2,143 |
| **Lunds Stallions** | 130 | 130 | 86 | **1,834** | 1,759 |
| Powerpuff Girls | 105 | 0 | 81 | 0 | 57 |
| Team 48 | 110 | 22 | 45 | 0 | 878 |
| Leviathan | 95 | 0 | 71 | 0 | 206 |
| OopsGotYourElo | 95 | 44 | 78 | 866 | 1,391 |
| **Memtrace** | 85 | 244 | 42 | **11,652** | 100 |

**So the proposed mechanism is dead for the motivating case.** Our 5.8% core-kill arrival
rate against Ouroboros cannot be explained by their launcher: **they have never built
one in 105 attributed games, and not one throw in those games came from their side.**
Whatever stops us arriving against Ouroboros, it is not interception. (Consistent with
the campaign plan's own pre-autopsy line — *0 launchers, 0 enemy throws* — which this
verifies independently rather than repeats.)

## VALIDATION — because three exact zeros in one column is a bug signature first

Corpus trap 3 says throws with launchers of **both** teams in range are marked
`UNATTRIB`, so an apparent zero could be an attribution failure rather than a behaviour.
Checked directly on the `amb` column:

| opponent | `amb == one` | `both_teams` | `same_team` |
| --- | ---: | ---: | ---: |
| Ouroboros | 2,080 | 0 | 0 |
| CtrlAltDefeat | 719 | 0 | 0 |
| Kings College Munich | 2,378 | 0 | 0 |
| Lunds Stallions | 3,965 | 2 | 1 |
| Memtrace | 12,357 | 511 | 472 |

**Attribution is essentially complete for every zero-cell in the table**, so the zeros are
behaviour, not decoder failure.

## THE FIELD SPLITS THREE WAYS ON THE LAUNCHER, AND THE MIDDLE GROUP IS THE SURPRISE

1. **No launcher at all** — Ouroboros (0/105), Powerpuff Girls (0/105), Leviathan (0/95).
2. **Builds launchers, uses them ONLY on its own bots** — **CtrlAltDefeat: 197 throws, all
   197 of its own bots, zero of ours**, across 80 launcher builds in 85 games. **Kings
   College Munich: 174 throws, all 174 of its own.** These teams pay for the piece and
   have never once used it on us.
3. **Uses it on us, heavily** — Lunds Stallions **1,834** throws of our bots (14.1/game),
   OopsGotYourElo 866, **Memtrace 11,652 across 85 games = 137/game**.

**Group 2 is worth flagging to whoever next reads sweep 12.** That sweep found the field
converged on grabbing the *enemy's* unit defensively and *away from* ferrying its own
forward. CAD and KCM are doing the thing sweep 12 says the field abandoned — and are
doing it exclusively. **Not overclaimed:** `throws.tsv` records thrower and victim team,
so "their own bot" is certain, but whether those throws are *forward ferries* or
*defensive repositioning* needs the `d2_before`/`d2_after` columns and is not read here.

## WHAT THIS DOES AND DOES NOT LICENCE

- **Closes** the proposed enemy-launcher cut **for Ouroboros**, which is the opponent the
  Loki programme is aimed at.
- **Opens** a genuine one for **Lunds Stallions** — a hard-five team throwing our bots
  14× per game — and for Memtrace at 137/game. If our raiders are being intercepted
  anywhere, it is there. Filed as an idea, not a detour: the incidence cut stays the top
  item.
- **Says nothing** about whether interception *matters* where it happens. A throw of one
  of our bots is not automatically a lost raid; `throws.tsv` carries `life`, `core_atk`,
  `any_atk` and `reached` for exactly that question, and none of them are read here.

## LIMITS

- **"In N attributed games"** always, never "never": `join.tsv` covers **1,445 of ~6,233**
  archived replays (23.2%); per-opponent coverage is 85-130 games here.
- **Trap 3 undercount stands:** a throw landing exactly one tile away is indistinguishable
  from an ordinary step and is not counted. This biases every throw count **down**,
  including the zeros — but a systematic undercount cannot manufacture 0 from 1,834.
- Version columns are dead in this corpus; nothing here is stratified by opponent version,
  so a team that only recently added a launcher would appear diluted, not absent.
