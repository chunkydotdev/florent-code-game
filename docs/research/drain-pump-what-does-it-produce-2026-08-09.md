# The drain pump: what it costs them is measured; what it produces for us is not

**Research arm, session 23, 2026-08-09.** Corpus only. Zero downloads, zero arena.
**Version tag:** live **v91 "Eir 9c hivethaw (rollback from v90)"** = `bots/_v100hf`,
1530 @ 508, rank #35. Corpus join 1,255 rows, 100.0000% reconciled.

Written **before** the drain pump becomes a build, because it is structurally the
same kind of claim as the siting finding that cost a −6.7pp plank four hours ago.

---

## 0. The claim, and why it needs a check

The third lane's reaction atlas measured that the drain is **already happening
inadvertently**: 97.9-99.4% of opponent shots on our heavily-absorbing buildings
overlap heals, and **one Ouroboros gunner put 677 shots ≈ 2,708 Ti into a single
healed 3 Ti conveyor.**

**Independent corroboration from building churn** (1,255 games, my decode):

| | US built | US died | US loss% | THEM built | THEM died | THEM loss% |
|---|---|---|---|---|---|---|
| conveyor | 59.2 | **14.3** | **24.2%** | 33.8 | 5.7 | 16.9% |
| harvester | 7.5 | 1.8 | 23.8% | 6.6 | 0.8 | 12.6% |
| gunner | 2.1 | 1.2 | 55.9% | 8.9 | **4.5** | 50.0% |

Titanium value lost per game at base cost: **US 360 Ti** (223 of it *builder bots*,
43 conveyors) against **THEM 293 Ti** (137 builders, **89 gunners**). **We absorb
into cheap things; they lose expensive ones.** The drain is real as a description.

**But "2,708 Ti of their shots went into a 3 Ti object" is an EXCHANGE-RATE
statistic. It says what they spend. It does not say what we get.** That is exactly
the shape of *"our forward turrets survive at 19%"* — true, clean, and silent on
purpose. **The lesson from that episode is now standing: before recommending
something, measure what it PRODUCES, not what it costs the other side.**

## 1. The obvious test is confounded, and I am not offering it as evidence

Enemy shots per round against our win rate, length-controlled, 1,255 games:

| their shots/round | median | **our win%** |
|---|---|---|
| Q1 | 0.06 | **80.9%** |
| Q2 | 0.28 | 62.2% |
| Q3 | 0.49 | 48.6% |
| Q4 | 0.77 | 31.1% |
| Q5 | 1.24 | **25.1%** |

Monotone and steep against us. If enemy ammo were scarce and draining it were
profit, the slope should point the other way.

**It does not refute the drain pump.** Enemy shot count is an **opponent-strength
proxy** — a winning opponent shoots more because it has more turrets and more
targets. **The causation almost certainly runs backwards.** This is the
opponent-thermometer error already catalogued twice today
(`middle-game-hazard-and-economy-2026-08-09.md` §3), and calling this table a
refutation would be committing it a third time.

**What it does establish is narrower and still useful: the naive prediction fails,
so the obvious test cannot discriminate, and the drain pump must not be built on
the exchange-rate number alone.**

## 2. The two cuts that would discriminate

**Neither is runnable from our corpus — shot *targets* are not decoded here; they are
in the third lane's `rx` decode.** Both have been requested.

1. **Hold total enemy shots roughly constant; vary the SHARE absorbed by cheap
   healed buildings.** If, at a fixed level of enemy shooting, a higher
   absorbed-share predicts a better outcome for us, the drain is real and worth
   siting for. If the share does not move the outcome, those shots were going to be
   wasted anyway and baiting them buys nothing.

2. **Cheaper, and a cleaner causal chain: does the opponent's TITANIUM DELIVERED
   fall when their absorbed-share is high?** Ammo is bought 1:1 from titanium, so a
   genuine drain should show up as *less economy for them*, measured independently
   of the fight. **This routes around the dominance confound entirely**, because
   delivery is not a function of who is winning the exchange in the way shot count
   is.

## 3. Standing note

**This document is a gate, not a finding.** The drain pump may well be real — the
atlas evidence is strong and the churn asymmetry is consistent with it. **The point
is that nothing measured so far tells us what absorbing those shots produces**, and
the last time this project acted on an exchange-rate statistic without that check it
cost 6.7pp with dose-response.

*Related: `turret-mix-and-map-width-2026-08-09.md` (the refuted recommendation and
the lesson), `heal-cancellation-by-core-separation-2026-08-09.md` (the escalation
finding, held pending its own discriminator).*
