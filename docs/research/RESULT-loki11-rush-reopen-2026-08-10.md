# RESULT — LOKI-11, the committed opening re-tested on LIVE TEAMS

Prereg: `docs/prereg/PREREG-loki11-rush-reopen-2026-08-10.md`, git author time
**2026-08-10T06:24:02+02:00**, committed before submission, activation and leg
creation. Treatment = `bots/_v128loki11` = the live bot with **one constant**
flipped (`LOKI2_RUSH_ON: False -> True`); `main.py`, `raid.py`, `eco.py`
byte-identical to v102.

**Fixture: live-unrated, 5 real teams x 5 pinned maps, 25 games per arm.**
Control is the pinned-testbed leg fired one window earlier on the same panel and
the same maps with v102.

## THE CURRENCY — and this is NOT A PASS

| | control (v102) | LOKI-11 (v103) | delta |
|---|---|---|---|
| **`core_kill_share`** (ours / all games) | 9/25 = 36.0% | **13/25 = 52.0%** | **+16.0pp** |
| **`r1000_rate`** (= DEFEAT rate) | 4/25 = 16.0% | **1/25 = 4.0%** | -12.0pp |
| our kill turns, median | 167 | **147** | |
| our kills inside r250 | 6/9 | **10/13** | |
| their kills against us, median | 87 | 142 | |

    Wilson 95% CI  treatment 33.5-70.0%   control 20.2-55.5%   -- HEAVY OVERLAP
    Fisher exact two-sided                p = 0.393
    Paired McNemar on 25 matched (opponent, map) cells:
        both kill 8 | LEG-only 5 | CONTROL-only 1 | neither 11
        exact two-sided sign test         p = 0.219
    MDE at n=25/25, 80% power, base 36%:  39pp

**+16.0pp is well below the 39pp this leg can resolve. THE PRIMARY CURRENCY
RESULT IS A NULL AT THIS n**, and the prereg said so before the data existed:
*"this leg cannot detect a small effect and I am not going to claim one either
way."* Direction is favourable and consistent across both estimators. That is
all it is.

## WHAT THE LEG ACTUALLY ESTABLISHES — it is about the ARENA, not the plank

The road was closed by a **replicated** arena measurement: `core_kill_share`
**-15.6pp (p=0.020)** on orizon and **-18.9pp (p=0.003)** on cad, 360 paired
deterministic games. **Live teams gave +16.0pp — the OPPOSITE SIGN at comparable
magnitude.**

**The pre-registered branch was: "if live-unrated lands in the -15.6 to -18.9pp
band, the arena is corroborated and I will say so plainly." It did not.** But
the leg cannot exclude that band either, so the honest statement is the weaker
one: **the arena's large negative effect is not reproduced on live teams, and a
road should not have been closed on that measurement alone.** It is not proof
the arena lied.

## THREE THINGS WORTH MORE THAN THE HEADLINE

1. **Three round-1000 games became kills** — CtrlAltDefeat/jackpot 1000->236,
   gsxWins/saga 1000->165, I Stone/jackpot 1000->393. Under `R1000_IS_DEFEAT`
   those are three defeats converted to wins, which is the currency the old
   arena verdict was never scored against.
2. **The Bisons went 0-5 against us in BOTH arms**, kills at 53-126 turns
   either way. **Tempo does not answer their method** — whatever they do is not
   something an earlier bank floor reaches.
3. **fjordgate produced 0 kills for us in both arms, 10 games.** A 10x10 map on
   which we never kill, in either configuration, is its own unexplained fact.

## THE CAVEAT THAT WOULD BE EASY TO BURY

**5 of the 25 paired cells are seat-mismatched.** CtrlAltDefeat was seat B in
the control and seat A in the leg; the other four opponents matched.
**Excluding those five cells the discordance is 3-1, p=0.625.** Two of
LOKI-11's five discordant wins sit in seat-mismatched cells. The platform
assigns seats and we cannot pin them, so this is a permanent property of the
fixture and must be reported with every paired live-unrated leg.

## MECHANISM BARS — NOT YET READ

The prereg's bars (median first forward-sentinel plant **< r60**; **>= 1.8**
forward sentinels/game) are decoded from the leg's own replays and are still
outstanding. **If either bar is not met, the prereg pre-commits that THE LEG
ANSWERED NOTHING about the rush, regardless of the currency table above.** This
document is not a verdict until that line is filled in.

## COST PAID

v103 was live from **04:23:46Z** (upload auto-activates — `fcode submit` makes
the new version active immediately, learned by watching) to **~04:32:5xZ**, when
an automatic rollback fired the instant the fifth challenge was accepted.
**One rated ladder match was created in that window.** The rating moved
1590 -> 1582 on a match created at 04:22:43Z, which was **v102's**, not v103's.
Absolute floor 1550 was never approached.

**Procedural correction for every future trick leg:** unrated matches complete
in ~15 s and the ladder pairs us about once per 10 minutes, so the sequence must
be **activate -> fire -> roll back within the same minute**, with the
rate-limit wait served while the INCUMBENT is live. This leg spent ~9 minutes
activated, almost all of it waiting on a rate limit, which was pure unforced
exposure.

## ⚠ PER-OPPONENT CONCENTRATION — THE +16.0pp IS TWO CELLS, AND ONE IS THE SEAT-FLIPPED ONE

Prompted by the side lane noticing the same shape in game score. Computed on the
PRIMARY currency, which is the one that matters:

| opponent | control kills | LOKI-11 kills | Δ | seat |
|---|---|---|---|---|
| CtrlAltDefeat | 2/5 | 4/5 | **+2** | B→A **SEAT FLIPPED** |
| gsxWins | 1/5 | 3/5 | **+2** | A→A |
| I Stone | 2/5 | 2/5 | 0 | B→B |
| Leviathan | 4/5 | 4/5 | 0 | B→B |
| The Bisons | 0/5 | 0/5 | 0 | A→A |
| **total** | **9/25** | **13/25** | **+4** | |

**THREE OF FIVE OPPONENTS MOVED BY EXACTLY ZERO.** The whole aggregate is two
cells. **Drop the seat-flipped cell and what remains is gsxWins alone: 7/20 →
9/20, +10.0pp, two kills.**

**This materially weakens the read and it is the honest version.** "+16.0pp
across a five-team panel" and "+2 kills against gsxWins, +2 against an opponent
whose seat changed" invite completely different next legs, and only the second
is supported. **A /25 denominator is not five comparable cells and must not be
quoted as though it were** — the same shape as the denominator rule already
written into the prereg, now caught on my own headline.

**What survives all of it:** three r1000 games became kills, the Bisons remain
0-5 in both arms, and the arena's replicated -15.6/-18.9pp did not reproduce in
sign. **What does not survive: any claim that the rush helps generally.** At
best it helped against one or two specific opponents, which is a
`per-opponent gate` question, not a doctrine question.

## MECHANISM BARS — READ. BOTH NOMINALLY MET, AND BOTH PREMISES REFUTED.

Decoded from the leg's own 50 replays (25 treatment, 25 control, **0 decode
errors**). "Forward" defined as `min_d2(tile, enemy 2x2 footprint) <
min_d2(tile, own 2x2 footprint)`, using the FULL four-tile footprint on both
sides so the known NW-anchor bias cancels; ties counted as not-forward. Seats
resolved per match from `teamAId`, not assumed.

| bar | threshold | treatment | control | verdict |
|---|---|---|---|---|
| **A** median round of first forward sentinel | **< 60** | **32** | **43** | **MET** |
| **B** mean forward sentinels/game | **>= 1.8** | **2.08** | **3.44** | MET numerically |

**BOTH BARS PASS THEIR LITERAL THRESHOLD AND BOTH WERE BADLY CONSTRUCTED,
because I sized them off a SINGLE LOCAL MATCH against `_probe_victim` — our own
lying fixture — and the live control does not behave like it.**

* Bar A's premise was *"control r73-r93"*. **The live control's own median is
  43**, already inside the window. The treatment is still 11 rounds earlier
  (32 vs 43), which is a real and correctly-signed effect — but the bar was
  built to clear a hurdle the control was already clearing.
* Bar B's premise was *"control ~1.0/game"*. **The live control builds 3.44/game
  (2.00 excluding one 1000-round grind with 38 rebuilds at a single tile).**
  **So the treatment does not double the siege — it builds FEWER forward
  sentinels than the control, or about the same once the outlier is dropped.**

**THIS IS THE D16 FAULT AGAIN AND IT IS MINE: a number true of a local run
against a self-authored probe, used to size a bar for live teams.** The bars
"passed" while the story they encoded was false, which is the worst of both
outcomes and would have been invisible without the control arm's own numbers.

## WHAT THE MECHANISM ACTUALLY DID — measured, not assumed

| per game, our team | treatment | control |
|---|---|---|
| first forward sentinel, median round | **32** | 43 |
| forward sentinels built | 2.08 | 3.44 |
| **harvesters built** | **3.12** | **5.44** |
| **conveyors built** | **20.92** | **38.20** |
| builder bots spawned | 6.36 | 6.88 |
| **our own units lost** | **2.76** | **4.52** |

**The rush is not "more siege, sooner". It is a LEANER game: plant 11 rounds
earlier, build 43% fewer harvesters, 45% fewer conveyors, and lose 39% fewer of
our own units — with slightly FEWER forward sentinels.** That is a coherent
mechanism and it is not the one the prereg described.

## VERDICT

**The mechanism engaged (timing, and a large economy reduction). The primary
currency is a NULL at this n** (+16.0pp, Fisher p=0.393, paired p=0.219,
MDE 39pp) **and the +16.0pp is carried by two of five opponents, one of them
seat-flipped.** The plank is NOT banked and NOT discarded: it is the first live
evidence that a road closed on our own arena behaves differently against real
teams, and it earns more power rather than a verdict.

**COST, CORRECTED — IT WAS FREE.** v103 played **ZERO rated ladder matches**
(verified on the platform: all recent ladder matches carry `ourver=102`; the
-8.92 delta I earlier attributed to v103 was v102's game against CtrlAltDefeat,
created 04:22:43Z, before v103 existed). Ladder pairings land ~10 minutes apart
and the activation window was shorter than one interval. **A trick leg on this
procedure costs zero rated exposure, not the 2-3 matches every prereg so far has
priced.** That materially changes the cadence arithmetic in favour of buying
power.
