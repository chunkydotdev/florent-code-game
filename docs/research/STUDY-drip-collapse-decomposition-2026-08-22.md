# STUDY — the drip-collapse causal decomposition (H1/H2/H3), banked verbatim

**PROVENANCE: builder-commissioned fresh opus agent, s56 2026-08-22 ~17:3x-17:49Z
(registered on the tail; Magnus's hypothesis named H1). Banked verbatim by the
builder from the agent transcript. Scratch instruments scratchpad/s56_drip_*.**

---

**GAME CONTEXT: everything below is in-game analysis for the Florent Code League, a sandboxed bot-vs-bot programming competition on a simulated grid under organiser-approved rules. "kill", "attack", "death", "shot" refer exclusively to in-engine unit removal and the engine's own API verbs between competing game bots. No real systems are involved.**

Written 2026-08-22T17:49:43Z, HEAD `bdff0f425`. Read-only: no `bots/` edits, no `bots/` opened, zero platform calls — every replay was already on disk.

---

## VERDICT: H1 is refuted. H2 is confirmed on its ordering but its stated *mechanism* is also refuted. The true mechanism is a third thing neither hypothesis named.

**The convert total is not an economy metric. It is a shot counter.**

Team ammo has exactly one source (`convert_ammo`, 1:1 from titanium) and exactly one sink (gunner 4 / sentinel 10 per shot; launchers 0). So the wire supports a closed ledger, and it closes:

```
Ti converted  ==  ammo spent on shots  +  ammo left at end
    FIXTURE  30/30 games EXACT      CONTACT  65/65 games EXACT
    MUTATION CONTROL (shot price +1):  0/20   <- the ledger is 1-point sensitive
```

So "converts/game 533 → 162" **is** "shots/game 52.5 → 15". And the shortfall is one factor, not two:

| SUBJECT: us, v180 | gun-rounds (Σ live gunners+sentinels) | ammo spent | **converted Ti per gun-round** |
|---|---|---|---|
| FIXTURE (`t_ctrl_f1`, n=30) | **482** | 519 | **0.966** |
| CONTACT (65 games, 3 opponents) | **138** | 148 | **1.056** |

Per gun-round we convert **the same or slightly more** in contact. The entire 3.3x drip collapse is 3.5x fewer gun-rounds. Pearson r(gun-rounds, converted Ti) = **0.835 across all 95 games**.

---

## H1 (defence-of-economy) — refuted, on four independent counts

Magnus's mechanism requires titanium scarcity to gate the drip. It is not scarce.

1. **We are RICHER in contact, not poorer.** Median titanium balance, rounds 0-50: **contact 305 vs fixture 238**. Whole-game median balance: contact 76.5 vs fixture 64.0. Share of rounds broke (balance < 10, cannot convert): **contact 5.3% vs fixture 7.0%** — the wrong direction for H1.
2. **Passive income alone covers the entire fixture demand.** Passive is 10 Ti / 4 rounds = **2.5 Ti/round**, and it is untouchable by anything the opponent does. The fixture's *whole* convert rate is **2.42 Ti/round**. Contact runs at **1.16 Ti/round**. Even with the belt at literally zero, funding is not binding.
3. **At the convert stall, 72.6% of games are neither broke nor gunless** (n=62 games with a detected stall): broke-only 19.4%, gunless-only 6.5%, both 1.6%. Only 17.7% had a belt collapse already.
4. **Magnus's own stated conditional fails.** *"In the minority of contact games where the belt survives, converts hold near fixture levels."* Terciles on **belt income Ti/round** (length-controlled, per round — the stage-1 totals were survivorship-confounded and I discarded them):

| tercile | income Ti/round | **convert Ti/round** | rounds |
|---|---|---|---|
| BOT n=21 | 0.270 | 0.769 | 169 |
| MID n=21 | 0.783 | 1.410 | 150 |
| **TOP n=23** | **2.391** (≈ fixture's 1.95) | **1.000** | 112 |
| *FIXTURE ref* | *1.95* | ***2.420*** | *184.5* |

Contact games whose belt income **matches or beats the fixture** still convert at **41% of the fixture rate**. Belt survival terciles say the same: TOP (0.90 survival) converts 1.032 Ti/r vs BOT (0.20) at 0.786 — a mild positive, nowhere near 2.42.

**The one place H1's temporal prediction does hold, stated honestly:** an income cliff precedes the convert stall in **75% of games, median lead 18 rounds** (n=55). Ordering alone does not separate — both series fall in contact. It is the funding test (1-3) and the per-gun-round invariance that exclude the mechanism.

---

## H2 (offense churn) — ordering confirmed, *spend* mechanism refuted, restated as NEED-GATING

Onset ordering across contact games (definitions fixed before reading the table; see `s56_drip_analyse.py` docstring):

```
churn < stall               26        pairwise: churn<stall 37, stall<churn  1   (97%)
stall (neither preceded)    18                  belt<stall  11, stall<belt   7   (61%)
churn < stall < belt         5
belt < stall                 4
belt < churn < stall         3
churn < belt < stall         3
stall < belt                 2
belt < stall < churn         1
no stall detected            3
```
Lead times (stall minus onset, positive = leads): **churn +24r median, leads in 97%** (n=38); belt +8r median, leads in 61% (n=18); core damage +14r, 59% (n=61).

**Dose-response with a placebo, which is what makes this causal rather than definitional** — our ammo spend in the ±20 rounds around each of our own turret deaths (n=129 events with a full window):

```
ammo/round BEFORE  2.500 median      AFTER  0.200 median     delta -1.500,  65.9% falling
PLACEBO (random non-death rounds, n=195)   delta +0.000,      22.6% falling
```

**But H2's stated mechanism — "repurchases consume Ti before conversion" — is false.** The bank is full (see H1 point 1); nothing is being crowded out. What a turret death removes is the drip's *demand*: fewer live guns → fewer shots → less ammo consumed → less converted. The bot is behaving correctly; the metric is downstream.

**Corroborating latency read, and it is exact:** first convert follows first turret build in **95 of 95 games**, median lag **+1r (fixture) / +2r (contact)**. The published "first convert slips r15 → r34" is entirely the first *turret build* slipping **r14 → r31**. Not a money-latency at all.

---

## H3 (lost board) — partially true and not the whole story

Core damage co-times rather than leads (+14r median, only 59% leading), and contact games are shorter (140 vs 184.5 rounds). But the ordering is *not* structureless — churn leads in 97% with a clean placebo — so H3 alone is insufficient.

---

## Where the gun-rounds actually go — the number for v630

| SUBJECT: our gunners+sentinels | FIXTURE (n=30 games) | CONTACT (n=65) |
|---|---|---|
| first turret build | r14 | **r31** |
| turrets built/game | 4.0 | 4.0 |
| **share that die** | **0.00 median (12.9% pooled)** | **0.60 median (59.4% pooled)** |
| life (all turrets, censored at game end) | 130r | **23r** |
| life (of those that die) | 28r | **11r** |
| alive at end | 3.5 | 2.0 |
| shots per turret | 9.0 | **4.0** |
| damage delivered per turret | 126 | **54** |

**We buy the same battery and it lives a fifth as long.** Restore contact turret survival to fixture levels and gun-rounds go 138 → ~480, which closes the whole drip gap arithmetically (162 → ~500).

---

## Kill-cause census (§4 of the commission, answered for both layers)

**Our turrets** (142 deaths, contact; 15 on fixture):
- **96.5% turret-fire-only**, 0% builder-attack-only. Attributed shot events by killer type: **gunner 515, sentinel 126** — enemy **gunners** are 79% of it.
- Shooter distance to victim: **median d² = 4** (2 tiles), p10 = 1 (adjacent), p90 = 16. This is BC's point-blank plant, measured from our side.
- **Median 7 damage per damaged round == exactly one gunner shot** (gunner dmg 7). Median 5 rounds first-hit → death, 6 damaged rounds. (Fixture reads 18/round = sentinel — the authored fixture opponent kills with a different weapon than the field does.)
- **One of our builders was orthogonally adjacent in the round before death in 13 of 142 cases (9.2%).** There is no healer present.

**Our belt** (340 deaths in 65 contact games = 5.2/game; fixture 56 in 30 = 1.9/game):
- Killer events: **builder_attack 1120, gunner 698, sentinel 149** — enemy *builders* walking up and hitting conveyors (2 dmg/hit) is the plurality of events; shooter d² median 2.
- Median **4 rounds from first damage to death**, 7 damage per damaged round. Conveyor life 50.5r (n=244), harvester 41r (n=96). 3% are our own demolitions (zero damage events).

---

## Cheapest-defence dose arithmetic

Heal is +4 HP for 1 Ti, one orthogonally-adjacent tile per builder per turn. Against the measured 7 dmg/round:

| under 7/r (one gunner) | 0 healers | 1 healer | 2 healers |
|---|---|---|---|
| sentinel (40 HP) | 5.7r | **13.3r** | never dies |
| gunner (25 HP) | 3.6r | 8.3r | never dies |
| conveyor (20 HP) | 2.9r | 6.7r | never dies |
| harvester (30 HP) | 4.3r | 10.0r | never dies |

Against 14/r (two gunners) healing loses: sentinel 2.9r → 4.0r (1 healer) → 6.7r (2) → 20r (3).

**Queue #52's exchange does work against the modal case** — one builder babysitting one forward sentinel takes it 5.7 → 13.3 rounds (2.3x) for **1 Ti/round**, buying ~+7 gun-rounds ≈ +7 shots ≈ **+126 damage for ~13 Ti**. Two builders make it net-immortal against a single gunner. The binding cost is not the Ti; it is the builder's action (heal blocks build/move that turn) and the 90.8% of deaths where no builder is anywhere near.

**Design inference, flagged as inference not measurement — the barrier screen is cheaper per HP and I did not test it:** a barrier is 3 Ti for 30 HP = **10 HP/Ti**, vs healing at **4 HP/Ti** — 2.5x better — and per the rules a gunner's straight-line shot is blocked by obstacles while a sentinel's is not. Since **79% of our turret killers are gunners at median d²=4**, a 3-Ti barrier on the intervening tile addresses the modal killer without spending a builder-turn per round, and costs +1% scale against a builder bot's +20%. This needs a live leg; it is arithmetic, not evidence.

---

## Instrument validation (run before any reading; controls driven to the other verdict)

| check | result | control |
|---|---|---|
| delivery ledger `core_deliv × 10 == titaniumCollected` | **130/130 contact + 120/120 fixture team-sides EXACT** | `swap_core` (deliveries to the wrong core): **0/20 ok** |
| convert cadence vs published `DECODE-firstcontact` M3b/M3c | **MIRROR 11/130, PIVOT 18/173, KLADDE 15/162, FIX-A 49/504, FIX-B 51/536 — digit-for-digit** | `swap_ammo_team`: yields **51 / 430 Ti**, which is *exactly* BC v68's published M3b/M3c row — the wrong-team attribution lands on the opponent's own numbers |
| ammo ledger `converted == spent + left` | **95/95 EXACT** | shot price +1: **0/20** |
| turns per game vs `corpus/unrated_games.tsv` | 65/65 | (inherited from the prior decode's mis-pair control, 65→1) |
| belt-death counter | median 4/game, range 0-18 | wrong-side: median 1, range 0-36 |
| content-duplicate fingerprint | contact **58 distinct of 65** | reproduces the prior decode's §0.3 independently |

---

## Effective n, per the DEFF enumeration procedure

- **MATCH cluster: live** (65 contact games are 5-per-match across 13 matches).
- **OPPONENT cluster: live** (3 opponents).
- **CONTENT-DUPLICATE cluster: live and measured** — 7 of 65 contact games are byte-identical repeats (58 distinct). Fixture `t_ctrl_f1`: **30 files, 30 distinct, 0 duplicates**.
- **MAP cluster: unverifiable on the contact side** (map identities are not recorded on the platform side) — carried as possibly-live. Fixture is 15 maps × 2 seats.

⇒ Contact: nominal 65, distinct 58, and with the platform unrated pooled DEFF 1.833 the effective n is **~32**. Fixture is a local balanced-by-construction battery (DEFF ≈ 0.98), so n=30 stands naively.

**⛔ SURPRISE, and it is an instrument finding for the builder: `scratchpad/s55_siteless/t_pb_f1` and `scratchpad/s54_v620/t_ctrl_f1` are 28 of 30 byte-identical replays.** They produce the identical M3b/M3c row (49/504 seatA, 51/536 seatB). The commission named `t_pb_f1` as the comparator and the prior decode named `t_ctrl_f1`; **they are one population, not two.** I used `t_ctrl_f1` throughout. Any grid treating those as independent arms has an effective n of half what it thinks.

**Direction check (the correction cannot flatter the claims):** every load-bearing claim here is an exclusion — funding excluded as the gate, restated positively as "contact balance is *higher* and broke-share *lower* than fixture", not as a failure to find a difference. Widening intervals makes those harder, which is the correct direction.

---

## What the tape cannot answer

- **Why the first turret build slips r14 → r31.** I measured that it does, and that the convert latency is entirely downstream of it. Whether that is a siting search, a path block, or a builder diverted under pressure is a `bots/` question, not a wire question.
- **Whether a barrier screen actually blocks the observed gunners.** The rules say a gunner's shot is obstructed and a sentinel's is not; I did not test it in-engine. Needs a probe or an unrated leg.
- **Counterfactual gun-rounds.** "Fixture survival would give ~480 gun-rounds" is arithmetic on the observed ratio, not a measured intervention.
- **Whether the income cliff and the gun-round collapse share a common cause** (both our belt and our turrets sit forward). The 75%/18r income lead is real; I excluded it as *the drip's* gate but did not identify what drives it.
- **Map identity and seat.** KLADDE is 25/25 seat B; no seat contrast exists there.
- **Shooter attribution near a rebuilt tile.** 27 of 652 turret-kill shot events resolve to a `conveyor` at the shooter tile — a tile-reuse artifact (~4%). It does not move the gunner-vs-sentinel split.

---

## Files

All scratch, prefixed as instructed:
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_lib.py` — per-round trace extractor (adds only `DistributeResources` to `s54_klad_lib`)
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_validate.py` — stage 0, validation + controls
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_analyse.py` — onset ordering, funding-vs-need
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_rate.py` — length-controlled rates, state at the stall
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_shots.py` — the closed ammo ledger
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_final.py` — gun-rounds, dose-response, kill census
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_close.py` — proportionality, heal arithmetic, effective n
- `/Users/junghard/Projects/Work/florent-code-game/scratchpad/s56_drip_games.json` — per-game rows

**The one-line answer for Magnus:** no — our economy does not collapse, our *battery* does. We hold more titanium in contact than on the fixture and the belt keeps paying; what falls is turret uptime (59% of our turrets die, life 28r → 11r, killed 79% by enemy gunners at 2 tiles for 7 damage a round with no builder of ours within reach 91% of the time), and "Ti converted" is just a counter of the shots those turrets never got to fire.