# SCREEN PREREG — `BBAMMO`: the ammo-drip bank floor raised to the SHREDDER's price, on the Band-1 BELTBREAK carrier — **the minimal eco × offense pair**

Drafted by a fresh opus subagent with NO inherited session context beyond the
inputs listed under `PROVENANCE`. The builder lane ratifies the judgment lines
and types the lock commit; this agent wrote no code under `bots/`, appended no
worklist row, appended no `docs/prereg/BARS.tsv` row, fired no game, started no
shard, and touched neither `results.tsv` nor `HANDOVER.md` nor `PROGRAMME.md`
nor `QUEUE.md`. No tool was fixed.

**STATUS: drafted BEFORE the `BBAMMO` row is appended to
`scratchpad/corefill_work.txt`, BEFORE any `docs/prereg/BARS.tsv` row exists,
BEFORE any file named `scratchpad/overnight/BBAMMO*` exists, and BEFORE the
leg's first game.** Drafting session wall clock at write time
**`2026-08-17T13:01:56Z`** (`date -u`, same shell call); repo HEAD at draft
`e728c6f8` (author time `2026-08-17T14:52:24+02:00` = `12:52:24Z`). Verified at
draft: `grep -c BBAMMO scratchpad/corefill_work.txt` → **0**; same grep on
`docs/prereg/BARS.tsv` → **0**; same on `results.tsv` → **0**;
`ls scratchpad/overnight/ | grep -i bbammo` → **0 files**.

### LOCK, clock 2 (local shard)
Per the obligations doc's **2026-08-17T07:24:55Z addendum**, which replaced the
clock-2 boilerplate eleven preregs had copied and that was not executable as
written. **PRIMARY:** the shard tape's own `# FIXTURE … start=` stamp
(`tools/overnight.sh:99` sets `START=$(date -u …)`, `:103` writes it to the tape
before the first game). Quote it verbatim beside the lock commit's git author
time. **BACKSTOP, if the tape carries no `# FIXTURE` line** (every REMOTE tape;
107 of 238 local tapes carry it): the tape's **FIRST COMPLETED ROW `ts`** —
conservative by construction, since the true start is strictly earlier, so the
substitution can only OVERSTATE the prereg-to-start gap (measured cost 1–2 s).
**SECOND BACKSTOP, serial runners:** the preceding shard's `COMPLETE` time on
the same worker. ⛔ **NOT AVAILABLE: the heartbeat's `STARTING` line** —
`overnight.sh:100` writes it with `>` and every later state overwrites it.
**State which clock was used.** This shard is registered LOCAL and SAME-HOST, so
the primary is expected to be available.

### ⭐ COMMIT PROVENANCE OF THE TREATMENT TREE — IT IS **TRACKED**, unlike the carrier's
`bots/_v504bbammo/` is committed and clean: `git status --porcelain
bots/_v504bbammo` → **empty**; `git ls-files bots/_v504bbammo` → **four files**;
added in **`54129ed7`** (`2026-08-17T12:50:15Z`). ⇒ **the OB13 defect the
carrier's own page had to disclose (`OB13_UNTRACKED_ARM`) does NOT apply here,
and the one-clause claim below is verifiable BY GIT**, not only by a file diff.
`TREATMENT DIFF REFS` below names the exact ref pair, verified at draft to
return the four paths.

---

## ⛔ READ BEFORE RATIFYING — EIGHT THINGS THE LANE OWNS, AND THE FIRST THREE ARE DECISION-CHANGING

### 1. ⛔⛔ THE `COMBO-BAR-EXEMPT` PRECEDENT DOES **NOT** TRANSFER TO THIS ARM ON ITS OWN REASONING, AND THAT DECISION IS WORTH A FACTOR OF **32** ON WHETHER THIS LEG EVER RETURNS A VERDICT.

`tools/auto_gate.py:715 combo_of()` greps the `stack.py` compose marker off the
**TREATMENT** tree's `doctrine.py`. `bots/_v504bbammo/doctrine.py` carries it
(`grep -c "composed by tools/stack.py"` → **1**, inherited from
`bots/_v468kladturbo/doctrine.py:1879` as every arm on this chassis does), so
**the gate will score `BBAMMO` as a COMBO and `COMBO_BAR = 55.0` binds on the
n=2700 prefix** (`auto_gate.py:278`, `:952-960`; Magnus 2026-08-16).

**THE PRECEDENT ROWS EXIST AND I HAVE READ THEM VERBATIM.**
`docs/prereg/BARS.tsv:310` (`BELTBREAK-EARLY`) and `:312` (`BELTBREAK2`) both
carry `⭐ COMBO-BAR-EXEMPT`, and both were **GRANTED BY MAGNUS DIRECTLY**
(`BELTBREAK-EARLY` at `2026-08-17T08:30:36Z`, on the builder's escalation;
`BELTBREAK2` on the same ruling). `grep -c COMBO-BAR-EXEMPT docs/prereg/BARS.tsv`
→ **2**, and both were zero when the carrier's page was written.

⛔ **BUT READ WHAT THE GRANT WAS GRANTED ON. Both rows say, in the same words:
*"This arm is a SOLO plank (ONE mechanism added to the incumbent chassis), not a
combination."*** The exemption's whole ratio decidendi is that the COMBO
classification was a **defect** — an inherited marker, not a property of the
arm. **THAT IS NOT TRUE HERE, AND THIS PAGE WILL NOT PRETEND IT IS.** The
builder's own brief names this arm **"THE MINIMAL ECO × OFFENSE PAIR"**;
relative to `bots/_v468kladturbo` it carries **TWO** mechanisms — the BELTBREAK
shredder plank (at `RND = 10`) **and** the ammo-drip bank floor. **It is exactly
the class Magnus pinned `COMBO_BAR = 55.0` for** (`auto_gate.py:263-278`,
verbatim: *"we want better combinations"*). ⇒ **carrying the token here is a
NEW GRANT, not an application of the old one, and it needs Magnus's word on
THIS arm.** A builder who types it citing `:310`/`:312` is citing a ruling about
a different question. *(The token's other registered purpose —
`auto_gate.py:906-919`, a MECHANISM test scored against its own additive
prediction — is arguably closer to true here than it was for the carrier, since
this leg's interest IS additivity; but it is still a judgement for the bar's
owner, not for a drafting agent or a builder.)*

**THE ARITHMETIC, DONE BEFORE THE FIRE.** 40,000-path simulation per cell of the
pinned gate chain in order (`CATASTROPHE@400` CI-hi<45 `:244-247` → `TREND-FLOOR
52.0 @1000` `:261` → `COMBO-BAR 55.0 @2700` `:278` → the `FUTILITY-BAR` CI rule
with its `0.5 × half-half-width` margin `:971-991`), naive intervals at DEFF
0.98:

```
true share      P(cat@400)  P(floor@1000)  P(combo@2700)  P(REACH n=5400)
                                                        NO EXEMPT / EXEMPT
  48.09  (stack's measured cost applied)  0.001   0.993   0.007   0.000 / 0.007
  51.09  (clause costs ~2pp)              0.000   0.709   0.291   0.000 / 0.296
  53.09  (clause EXACTLY NEUTRAL)         0.000   0.236   0.740   0.024 / 0.761
  54.59  (clause adds +1.5pp)             0.000   0.046   0.616   0.337 / 0.953
  56.00  (clause adds +2.9pp)             0.000   0.005   0.137   0.857 / 0.995
```

⇒ **WITHOUT the exemption, the single most likely true state of the world — the
clause is neutral and the arm simply reproduces the carrier's measured 53.09 —
reaches its own registered n with probability 0.024.** With the exemption,
0.761. **That is a 32× swing produced entirely by a registry token, and it is
the largest single number on this page.** **REGISTERED READING, pre-committed so
it cannot be re-read afterwards: a `COMBO-BAR@2700` cancellation with a prefix in
[52.0, 55.0) is an OPERATIONAL CANCELLATION and is NOT a refutation of the
pair.** It says *"this combination is not the 55-class combination we are
prospecting for"* — a statement about the CHASSIS TOTAL, not about the ammo
clause. Such a stop licenses **no** sentence of the form "reserving the
shredder's price did not pay", **no** comparison against the carrier's 53.09, and
**no** closure of the funding axis. ⛔ **AND THE 52.0 TREND-FLOOR IS NOT WAIVED
BY ANY EXEMPTION** (`auto_gate.py` waives only the 55.0 prefix): at the neutral
hypothesis it alone kills this arm 23.6% of the time.

**Whether to spend a core at 0.024, or to escalate for a 0.761, is a
BUILDER/MAGNUS decision and is deliberately not made on this page.**

### 2. ⛔⛔ THE RESERVE IS **~94 Ti AT LIVE SCALE, NOT DOSE 4's ~54.** IT IS THE SWEEP'S **DOSE 6**, SITTING BETWEEN DOSE 5 AND THE **DISQUALIFIED** DOSE 3 — AND TWO INDEPENDENT INSTRUMENTS AGREE ON THAT PLACEMENT.

The brief and the tree's own comment (`bots/_v504bbammo/main.py:396`) describe
this clause as *"dose-4 SHAPE … at the SHREDDER's price"*. **The SHAPE claim is
correct — BOTH branches, `max()` below E1 — and the PRICE claim is where a
certifier must not stop reading.** The sweep's own pricing table
(`bots/_v501ammofloor/doctrine.py:1917-1926`, reserve in Ti at the stated live
scale ~2.7):

```
  dose 4  get_gunner_cost()                        ~54 Ti   SHIPPED
  dose 5  get_sentinel_cost()                      ~81 Ti
  dose 3  get_sentinel_cost() + LOKI_FWD_TI_FLOOR ~121 Ti   DISQUALIFIED (-27.5pp timely-kill)
  ---------------------------------------------------------------------------
  BBAMMO  get_gunner_cost() + LOKI_BELTBREAK_TI_FLOOR(40)
                                                   ~94 Ti   <-- between 5 and 3
```

`floor(scale × 20) + 40`, computed at draft, not asserted: scale **1.0 → 60 ·
2.0 → 80 · 2.7 → 94 · 3.0 → 100 · 4.05 → 121, i.e. dose 3's own disqualified
level.** ⛔ **AND SCALE ONLY EVER RISES** (`CLAUDE.md`: ONE GLOBAL ADDITIVE team
factor, engine-confirmed via `bots/_probe_scale` s26), **while the magazine's
需要 does not scale — a gunner shot is 4 ammo at every scale.** ⇒ **the reserve
grows through the sweep's ladder over the course of every game, and the price of
what it is protecting the bank for grows with it, but the shots it displaces do
not get cheaper.** That is the mechanism by which this clause can end up at
dose 3's position late in a long game.

**THE SWEEP'S COST CURVE IS MONOTONE IN RESERVE SIZE — that is its own stated
finding** (*"THE COST CURVE IS MONOTONE IN THE RESERVE AND WELL IDENTIFIED"*),
so placing BBAMMO on it is a linear interpolation and **is labelled as a
RECONSTRUCTION, not a measurement**:

| quantity | d4 ~54 | d5 ~81 | **BBAMMO ~94 (interpolated)** | d3 ~121 | control |
|---|---|---|---|---|---|
| mean ammo held | 25.3 | 17.7 | **~15.3** | 10.2 | 30.9 |
| dry-turret rounds/game | 40.0 | 82.1 | **~114** | 181.4 | 26.2 |
| kill-by-r300 | 0.854 | 0.846 | **~0.769** | 0.608 | 0.883 |

⭐ **AND THE INTERPOLATION IS CORROBORATED BY A SECOND, WHOLLY DIFFERENT
INSTRUMENT ON THE RIGHT CHASSIS** — see #4: `_v502bbstack`'s LEG-3 battery
measured **dry-magazine rounds 6.3/game → ~95-101/game** on the BELTBREAK
chassis (`bots/_v502bbstack/doctrine.py:1800-1802`), against this table's
reconstructed ~114. **Same order, same sign, from a paired replay battery rather
than from an interpolation.** ⇒ **the "dose 4" framing understates this arm's
position on the only curve the sweep measured cleanly, and this page registers
the arm at dose 6.**

⚠ **CAVEATS ON THE TABLE, stated so it is not over-read:** the sweep's fixture is
eight old versions of our own lineage where the control wins 97.9% of 240 games
(its own doctrine says absolute shares there are meaningless); the chassis is
`_v468kladturbo`, not this one; and linear interpolation in Ti is an assumption
about the curve's shape, not a property of it. **The ORDERING is the robust part.**

### 3. ⛔⛔ EVERY BAR ON THIS PAGE IS **PRE-SATISFIED BY THE CARRIER**, SO THE ARM CAN PASS ALL OF THEM WHILE THE CLAUSE IS A MEASURED NET NEGATIVE. THIS IS OBLIGATION 7 IN ITS DUAL FORM AND IT IS THE DESIGN CRITIQUE OF THE WHOLE LEG.

OB7: *"a prereg must verify the predicted-change set is not already in the target
state at lock time. A prereg predicting change on cells already changed cannot
fail honestly."* The registered control is `bots/_v468kladturbo`. **The carrier
alone, with this clause absent, already measures — at the full registered n, on
the same control, same host, same seat/map balance:**

```
results.tsv:beltbreak2-final   share 53.09 [51.76, 54.42]  n=5400
   (recomputed at draft off scratchpad/overnight/BELTBREAK2.tsv: 2867/5400 = 53.0926%)
   ITT timely-kill-by-r300  T 30.80%  vs  C 24.35%   paired diff +6.44pp
   ITT RMST300              T 268.21  vs  C 275.52   paired diff -7.30 rounds (FASTER)
   kill-win median (T)      244        (gross backstop at 300)
```

**THE SLACK EACH BAR HANDS THE CLAUSE, computed:**

| bar as registered vs `_v468kladturbo` | carrier's own reading | **how much the clause may COST and still pass** |
|---|---|---|
| pooled share ≥ **51.33** | 53.09, CI-lo **51.76** | **≈1.76pp of share** |
| ITT timely-kill: CI-lo on (T−C) excludes a fall of **3.0pp** | **+6.44pp** | **≈9.4pp of timely-kill** |
| ITT RMST₃₀₀: CI-hi on (T−C) excludes **+5.0 rounds** | **−7.30 rounds** | **≈12.3 rounds** |
| kill-win median crosses **300** | **244** | **≈56 rounds** |

⇒ **Band 1 on this page would be delivered by shipping the carrier with
`LOKI_BBAMMO_ON = False`.** And the stack's measured cost for this exact clause
(#4) is **−5.5pp timely-kill and +44 rounds of median kill** — **both inside
every one of those slacks.** ⛔ **A leg whose every registered bar can be
cleared by the chassis it is testing an addition to cannot fail honestly about
the addition.**

**THE REMEDY, AND IT IS REGISTERED RATHER THAN LEFT TO READOUT.** The design is
Magnus's chosen pair and this agent does not change it. What it does is
**register the clause-attributing contrast as the THIRD FALSIFIER with its own
pre-committed reading** — treatment vs `scratchpad/overnight/BELTBREAK2.tsv`, an
n=5,400 tape on the identical control, fixture, host and balance. Pre-data
half-widths, DEFF 0.98 both sides, two-sample:

```
share difference           +-1.86pp     (p~0.53, 5400 + 5400)
ITT timely-kill difference +-1.68pp     (p~0.28)
ITT RMST300 difference     +-2.08 rounds (sd 55.66 per side, measured on the carrier's tape)
```

**All three RESOLVE the stack's measured effect sizes** (−5.0pp share, −5.5pp
timely, +44 rounds). ⇒ **the clause question is answerable on this leg; it is
just not what the registered PRIMARY answers.** ⛔ **AND THE CROSS-TAPE CONTRAST
IS ONLY VALID WITHIN-HOST** (OB16's 2026-08-15 cross-host rider: the local 0.98
exemption is a WITHIN-HOST measurement). `BELTBREAK2.tsv`'s header reads
`host=MacBook-Pro`. ⇒ **this shard is REGISTERED SAME-HOST, MacBook-Pro.**
Running it remote does not invalidate the pooled bar, but it **voids the third
falsifier**, which is the only bar on the page that can fail because of the
clause. Moving hosts is an amendment typed BEFORE the first row.

**RECOMMENDATION TO THE RATIFYING BUILDER, offered and not taken:** the cleanest
repair is a **second registered shard with `bots/_v488beltbreak2` as the
CONTROL** — that makes the clause the only difference between the arms and turns
the third falsifier into a within-shard primary. It costs a second core. This
page is written so that the single-shard version is still readable without it.

### 4. ⭐⭐ THIS ARM IS **ALREADY MEASURED AT n=200 NOISE_ON**, AND THE MEASUREMENT IS ON THE RIGHT CHASSIS, AT THE RIGHT DOSE. THE CURRENCY MOVED AGAINST IT ON EVERY COLUMN.

Relayed by the builder lane during drafting and then read at source
(`bots/_v502bbstack/doctrine.py:1689-1935`), which is why it is quoted with
file:line rather than as a message.

**WHY IT IS *THIS* ARM AND NOT A COUSIN — the identity chain, each link
measured:** `_v502bbstack` with `BBSTACK_ON = False` is `_v488beltbreak2`
**exactly** (16/16 byte-identical, with a flag-on positive control at 16/16
DIFFERING, `:1861-1864`). `LEG 0` is **behaviour-neutral, measured twice**
(S0 vs L0 identical in 50/50 AND L3 vs L0+L3 identical in 50/50, with the
normaliser itself driven against a case that MUST differ — S0 vs L1, 27 of 50
differ — because it silently no-opped on the first attempt, `:1866-1876`).
`LEG 3` is `get_gunner_cost() + LOKI_BELTBREAK_TI_FLOOR`, BOTH branches,
`max()` below E1 (`:1739`, `:1982-1986` dose 6). Legs 1 and 2 were OFF in that
cell. ⇒ **the `L0+L3` arm differs from `bots/_v504bbammo` only by a leg measured
neutral in 100 of 100 games.**

```
NOISE_ON=True, NOISE-ON opponent, 25 maps x 2 seats x 4 reps = 200 games/arm, unpaired
  arm                     plants/gm    win   kill   ITT300   medKill   r1000
  chassis (_v488beltbreak2)  1.365      112    103   28.0%      259       26
  L0+L3  (== this clause)    1.815      102     95   22.5%      303       14
```

* ⭐ **THE MECHANISM REPLICATES AND IT IS THE STRONGEST CLAIM IN THE FAMILY:**
  plants/game **+0.450, 95% CI [+0.134, +0.766], EXCLUDES ZERO**, in the regime
  that killed the sweep's own turret gain. The bank doubled at r95-105 (29 → 54
  Ti). **This arm's F1 dose read should land cleanly, and the wiring-null branch
  is close to closed before the fire.**
* ⛔ **AND EVERY CURRENCY COLUMN MOVES THE OTHER WAY:** wins 112→102, kills
  103→95, ITT timely-kill 28.0%→22.5% (**diff −5.5pp, 95% CI [−14.0, +3.0]pp**),
  **median kill 259 → 303 — THROUGH the r300 gross backstop.** Dry-magazine
  rounds 6.3 → ~95/game. **No column is resolvable at n=200** (win share alone
  carries ±9.8pp) — **but they all point one way while the mechanism column
  points the other, which is the shape of a plank that buys the intermediate and
  not the goal.** The one column that moves FOR it: r1000 games 26 → 14.
* ⇒ **`bots/_v502bbstack` therefore ships this leg `BBSTACK_L3_AMMOFLOOR =
  False`**, with the author's own reasoning recorded (`:1907-1912`): *"neither
  convicts — but the burden is on the plank to CLEAR a bar, not on the bar to
  convict the plank."*
* ⛔ **A THIRD CONFIRMATION OF THE SAME SHAPE, from the same tree and it is worse
  than the pair-wise reads: the FULL four-leg stack failed the sweep's own
  disqualifying test** — plants +21% while **shots/shredder fell 56% (14.0 →
  6.2)** and total fires fell 46%. And the deepest sentence in that block, which
  this page is obliged to quote because it is the version of the null that
  closes the road rather than narrowing it: **`L0+L3` bought +43% plants and
  `L0+L1+L3` bought +32% plants for 6.0 shots each — 33% more shredders
  delivered FEWER kills. Plants may never have been the kill constraint at
  all.** The stack's funnel says the dominant refusal is **STILL `TI`** after
  all four legs (62-75% of every post-fix funnel; bank moved, `TI` refusals
  stayed ~56/game).

⚠ **WHAT THAT n=200 READ IS AND IS NOT.** It is 200 games per arm against ONE
opponent on a LOCAL fixture we authored; per this repo's directive 6 it
**prioritises** a road and does not close one. It is also **not this leg's
control** (chassis, not `_v468kladturbo`), so its share figures are not
commensurable with the bar on this page. **It is the reason the second and third
falsifiers below are LIVE rather than ceremonial.**

### 5. ⛔ THE CLAUSE FIRES ON **EVERY MAP**, INCLUDING THE THREE WHERE THE PLANK CANNOT PLANT — SO THIS ARM'S SEGMENT COMPLEMENT IS PREDICTED **NEGATIVE**, NOT A/A. THIS IS THE SHARPEST DIFFERENCE FROM THE CARRIER'S PAGE.

Read at `bots/_v504bbammo/main.py:407`: the guard is `if LOKI_BBAMMO_ON:` and
**nothing else** — no `bb_live` heartbeat test, no BELTBREAK gate, no round gate,
no map test. It sits on the CORE's path inside `if not endgame_dumped:`
(`:344`), so it raises `ti_floor` in essentially every round the drip wants a
top-up, in every game, on every map. *(The clause always binds where it fires:
`gunner_cost + 40 ≥ 60` exceeds the ceiling the incumbent block can reach —
`12`/`52` at `:389` and E1's `min(harvester_cost, 23) + 23 = 46` at `:390-394`.)*

**MEASURED, on the carrier's own tape at n=360 per cell:** the three maps that
plant **zero** shredders in both arms read **antler 47.78% · fjordgate 51.67% ·
royale 50.28%**, every CI containing 50 (±5.11pp per cell) —
*A/A by construction for the carrier.* ⇒ **on those three maps BBAMMO delivers
PURE COST: the reserve is held, ammunition is displaced, dry-turret rounds rise,
and there is no shredder anywhere to fund.** **EXPECTED DIRECTION on the
complement: NEGATIVE.** That is a real, directional, falsifiable prediction and
it is the clause that can surprise the person running it — the carrier's
complement prediction was *no movement*, and this one predicts movement with a
sign.

### 6. ⚠ "THE SHREDDER'S OWN REFUSAL THRESHOLD" IS **NOT** WHAT THE PLANT PATH REFUSES BELOW. READ IT OFF THE SOURCE.

`bots/_v504bbammo/raid.py:902-907`, verbatim:

```python
        need = ct.get_gunner_cost()
        if live > 0:
            need += LOKI_BELTBREAK_TI_FLOOR + LOKI_BELTBREAK_AMMO
```

⇒ the plant path refuses below **`gunner_cost`** for the FIRST shredder (no
margin at all — the arm deliberately waives the forward reserve for it,
`:896-899`) and below **`gunner_cost + 40 + 24`** for the second. **The clause's
reserve — `gunner_cost + 40` — matches NEITHER.** It is the SECOND shredder's
threshold **minus the magazine**, which is a coherent choice with a stated
reason (`main.py:404-406`: the magazine bump downstream handles the magazine;
double-counting would starve the tap it opens — and the stack independently
reached the same correction at `:1741-1746`, calling the +`AMMO` variant "dose 7
… NOT a candidate" because it would reserve ~130 Ti). **But it over-reserves the
FIRST plant by 40 Ti relative to that plant's own threshold, and the sweep's
registered pricing discipline was *"each dose reserves EXACTLY the bank
threshold that the corresponding plant path refuses below, read off that path's
own source line"* (`_v501ammofloor/doctrine.py:1917`).** ⇒ **this arm departs
from that discipline. Stated, not hidden; it is not a bug and it is not the
described thing either.**

### 7. ⛔ OBLIGATION 17 — THE F1 METHOD THE BRIEF NAMES IS **NOT EXECUTABLE BY `tools/dose.py`**, AND THE CLAUSE THAT FOUND IT IS THE ONE THAT COULD SURPRISE ME.

1. **EXECUTING TOOL NAMED:** the brief registers *"F1 dose at the SHARD's
   fixture (`--tle 10` battery)"*.
2. ⭐ **THE PATH DOES NOT EXIST IN THAT TOOL — grepped, not assumed.**
   `grep -n tle tools/dose.py` returns **exactly one line, `:77`, and it is the
   substring inside the map name `antler`.** There is no `--tle` option in its
   argparse (`:134-172`) and `:226-228` builds
   `[FCODE, "run", bots[0], bots[1], map, "--seed", seed, "--replay", rp]` with
   **no `--tle` at all**, while `fcode`'s own `run.py:119` is
   `@click.option("--tle", default=0, …, help="Turn time limit in ms (0 to
   disable, server uses 10)")`. ⇒ **`tools/dose.py` measures at NO CPU LIMIT,
   which is a chassis that does not exist** (`tools/overnight.sh:131-137`: *"⛔
   `--tle 10` IS NOT OPTIONAL … a run without `--tle` measures a chassis that
   does not exist"*, with `_v145bestfit` 6/6 with the limit off and 1/6 with it
   on).
3. **CONSEQUENCE OF SILENT NON-EXECUTION — and this is measured, not
   hypothetical.** `results.tsv:beltbreak2-final`: *"F1 AS REGISTERED READ NO
   INFORMATION AT 0.98x OF ITS BAND (+0.367/game vs band 0.374, n=60 full, no
   shortfall — missed by 0.007/game) — AND THE FIRING AGENT FOUND WHY … ON THE
   SHARD'S OWN FIXTURE the same registered n=60 reads DOSE DELIVERED at
   1.26x/1.45x, and the doctrine's quoted median 49.5→40 reproduces (49.0→40) —
   which it does NOT at tle=0."* ⇒ **the tool does not fail; it quietly measures
   a different chassis and prints the same verdict vocabulary.** The carrier's
   verdict was materially changed by this.
4. **ROUTED AROUND, NOT FIXED** (standing instruction: no tool fixes). **F1 below
   is registered as a DIRECT `fcode run … --tle 10 --replay <file>` battery**
   with the map/seat/seed rotation reproduced from `dose.py:218-231` so the
   fixture stays comparable, decoded with the shipped
   `tools/corpus/replay_events.py`. **Defect named in one line for the wrap
   list:** *`tools/dose.py` passes no `--tle` and `fcode run` defaults to 0 (limit
   disabled); every registered dose read on a `--tle 10` fixture must bypass
   `dose.py` or the tool must gain the flag.* **Second known defect, unchanged
   from the carrier's page:** `tools/dose.py:77`'s default `MAPS` is the retired
   pre-2026-08-13 8-map pool (`atoll`, `heart`, `hive`, `meander` are not in the
   live pool), so `--maps` must always be passed explicitly.
5. **A DECODER FACT THAT WOULD HAVE INFLATED THE PLANT COUNT ~3×, checked
   clean:** `rotate()` re-emits `placeEntity`; `tools/corpus/replay_events.py:16,113`
   guards it (a build is the FIRST `placeEntity` carrying an id). **The guard is
   present.** Recorded as a check that came out clean, not as one that was absent.

### 8. THE SHARD TAPE CANNOT SEE THIS MECHANISM AT ALL, AND THE FIRINGS READ IS A HARD SEQUENCE.
`tools/overnight.sh:138-139` runs every game with `--replay /dev/null`; the
tape's columns are `ts shard game map seed seat winner cond turns` — **no
entity, build, titanium, ammunition or turret information exists on it, in either
arm.** The `FIRINGS-BEFORE-PRIMARY` rule (`docs/prereg/BARS.tsv` header,
research 2026-08-16T13:27:33Z) is registered here as a **HARD SEQUENCE**:
> **F1 and F2 are RUN, and their numbers written down, BEFORE any sentence
> containing this arm's primary share is typed.** A primary typed ahead of the
> firings read is a REGISTRATION BREACH regardless of what it says, and the
> repair is an amendment chain, not a re-write. *(Precedent on the tape:
> `results.tsv:kladladder-verdict-amendment-f1f2-pending`.)*

---

## RATIFY: Hypothesis

**HYPOTHESIS.** *Reserving the shredder's price from the core's ammunition drip
— ONE guarded assignment raising `ti_floor` by `max()` to `ct.get_gunner_cost() +
LOKI_BELTBREAK_TI_FLOOR`, on BOTH branches, below the E1 harvester-reserve block
so E1 is never lowered — added to the Band-1 BELTBREAK carrier
`bots/_v488beltbreak2` and to nothing else, converts a measured and
NOISE_ON-replicated **+0.450 shredder plants per game** into a LOCAL pooled game
share vs `bots/_v468kladturbo` of **51.33% or higher** at n = 5,400 games across
all 15 corefill maps and both seats, WITHOUT pushing our own kill past r300.*
Registered direction **POSITIVE**.

**Provenance of the pair, verbatim (the builder lane's brief, s49):** Magnus
narrowed the board to **ONE offensive plank (BELTBREAK) + ONE eco plank
(AMMOFLOOR)**; this arm is *"the minimal eco × offense pair"*.

**THE MECHANISM CLAIM, STATED SO IT CAN BE WRONG, WITH BOTH SIDES CARRIED — this
is the section the whole leg turns on.**

**(PRO.)** Ammunition conversion is the **#1 titanium claimant in this bot —
29.7% of r25-120 spend and 36.2% full-game**, on two independent fixtures
(`_v501ammofloor/doctrine.py:1884-1887`, plus a second-fixture reproduction at
737 Ti/game to ammo against 1,902 collected = 39%). The incumbent floor
collapses to **12** the moment any weapon slot has ever been written and E1 lifts
it only to **46**, while the BELTBREAK plant path refuses on `TI` **638×/game**
(instrumented, unrate-limited, 30 games) against `CAP` 6.6×/game — **the bank,
not the cap, is what stops a shredder**, which is the finding that killed the
rival `CAP 2→3` axis on measurement. ⇒ **the magazine outbids the turret, and
this clause reserves the turret's price.** The sweep's own causal split is the
strongest single argument: **for turrets 2..n the floor IS causal (+4.3 to +7.8
turrets when reserved); it is only the FIRST turret whose gate is SITING.** And
the pair is aimed at exactly that case: **turrets 2..n, at a ~54-Ti gunner
rather than a 121-Ti sentinel, firing at 4 ammo/shot — the cheapest shot in the
game, so the magazine cost per turret-of-value is the smallest available.**
**It is not an argument that survived nothing: the mechanism REPLICATED at n=200
under NOISE_ON, CI excluding zero** (#4).

**(CON, and it is heavier than the pro.)** The sweep's **gain curve did not
replicate** across noise regimes on the control chassis (dose-4 turret gain
+4.33 NOISE_OFF → +0.47 NOISE_ON) while the **cost curve replicated in both**
(ammo held −5.6 / −5.0, both excluding 0; dry-turret rounds monotone 26 → 181).
**Dose 3 — the same both-branches shape at sentinel price — was DISQUALIFIED at
−27.5pp timely-kill**, and this arm's reserve is **~94 Ti**, between dose 5 and
dose 3 rather than at dose 4's ~54 (#2). The control-chassis verdict was that
**the kill constraint is turret THROUGHPUT, not COUNT**: dose 3 bought +7.8
turrets, lost 13.8 shots, and gave back −27.5pp — *"the magazine was not
overbidding; it was correctly priced ON THAT CHASSIS."* And on **THIS** chassis
the same clause has already been measured once, at n=200, with every currency
column against it and the median kill through the backstop (#4).

⇒ **THE REGISTERED CROSSING, and it is the ONE read this arm lives or dies on:
PLANTS UP *with* SHOTS-PER-SHREDDER FLAT.** **Plants up and shots down is the
exact trade that disqualified dose 3 and collapsed the full stack (14.0 → 6.2),
and it is this arm's NAMED failure mode — not a mixed result, a
disqualification.**

---

## REGISTRATION BLOCK

**TARGET BAND: N/A — local corefill screen with ZERO rated ladder exposure: no submission, no activation, no unrated challenge, so `tools/target_value.py` has no input. Nothing on this page ends in a ship; the only branch that reaches the ladder is a later, separately-registered head-to-head against the holder.**
**PINNED: N/A — local self-play. The opponent version is fixed by construction: the control tree is `bots/_v468kladturbo` at the commit this shard runs from, pinned at `scratchpad/CONTROL_PIN`. There is no opponent churn to pin against and no calibration relevance to protect (CLAUDE.md's rule: pin treatment legs, never pin calibration panels — this is neither, it is self-play).**
**SURFACE: local**
**CLUSTER UNIT: none** — CLAUDE.md's enumeration PERFORMED, not asserted: (i) the **MATCH** cluster does not exist on this surface — `tools/overnight.sh` writes one TSV row per `fcode run`, so 1 row = 1 game and no row shares a match with another; (ii) the **OPPONENT** cluster is degenerate — every one of the 5,400 rows plays the identical control tree, so the pooled stratum holds exactly one opponent and there is no between-opponent variation for a design effect to describe; (iii) **HOST** is killed by REGISTRATION, not by measurement: this shard is registered SAME-HOST on **MacBook-Pro**, and OB16's 2026-08-15 cross-host rider (the 0.98 exemption is a WITHIN-HOST measurement) is why splitting it across hosts requires an amendment typed BEFORE the first row — **and here the host registration is load-bearing beyond the usual, because the THIRD FALSIFIER pools this tape against `scratchpad/overnight/BELTBREAK2.tsv`, whose header reads `host=MacBook-Pro`.** All surviving clusters die ⇒ DEFF = the measured local constant **0.98** (pair-weighted, ρ = −0.020, 124 shards, s39 audit), i.e. **NAIVE intervals are correct and marginally conservative. The platform constants (1.529 rated / 1.833 unrated) are NOT applicable and importing them would widen every interval on this page by 24-35% for correlation measured absent.**
**ESTIMATOR: the unweighted pooled treatment game share** = (rows with `winner == T`) / (completed rows), over all 5,400 rows, both seats pooled, all 15 maps pooled, no reweighting. Because the shard is exactly balanced on 15 maps × 2 seats × 180, the pooled share and the map-stratified equal-weight share coincide by construction; the stratified form is computed at readout as an **arithmetic consistency check only** and is not a second estimator (s28 ring-hold: four estimators inside 0.010 of one bar flipped MEET/MISS among themselves). Seat A and seat B shares are reported SEPARATELY as a fixture diagnostic and are never a bar — seat is worth ~7.6pp on byte-identical arms, which is why n is a multiple of 30. **Any estimate quoted at readout arrives from `tools/cluster_ci.py` (HEAD) so the interval and the point are produced by the same call; the pre-data half-widths on this page are closed-form Wald with DEFF 0.98 and their arithmetic is shown inline.**
**DOSE: shredder plants per game 1.815 (treatment shape: this exact clause as `_v502bbstack` LEG 3 / dose 6, `LOKI_BBAMMO_ON`-equivalent ON) vs 1.365 (flag-off control: the same tree with the clause disabled == `bots/_v488beltbreak2` byte-identical), n=200 games per arm, NOISE_ON=True with a NOISE-ON opponent, 25 maps × 2 seats × 4 reps, unpaired; paired difference +0.450, 95% CI [+0.134, +0.766], EXCLUDES ZERO.** Source `bots/_v502bbstack/doctrine.py:1880-1900`. **BOTH VERDICTS PRESENT, and the flag-off half is the one that matters:** the same tree with its master flag off is **16/16 games byte-identical** to `bots/_v488beltbreak2`, **WITH a flag-on positive control on the same fixture reading 16/16 games DIFFERING** (`:1861-1864`) — 16/16 identical alone is equally consistent with a harness that cannot see any difference; the positive control is what makes the zero mean something. **LEG 0's presence in that cell is neutralised by measurement, not by argument: behaviour-identical in 50/50 games alone AND 50/50 under composition, with the normaliser itself driven against a case that MUST differ (27 of 50), because it silently no-opped on the first attempt.** ⚠ **THE ARM'S OWN 16-GAME EQUIVALENCE BATTERY IS AMBIGUOUS IN THE RECORD AND THE BUILDER MUST RESOLVE IT AT LOCK:** commit `54129ed7`'s message reads *"Equivalence driven both ways on both: flag-off 0/16 non-identical, flag-on 8/16 and 16/16 differing"* for `_v503bbcap3` and `_v504bbammo` together. **The flag-off half is unambiguous and applies to both (0/16 non-identical = 16/16 identical); which arm scored 8/16 and which 16/16 on the positive control is NOT stated.** List order implies `_v504bbammo` = 16/16, and this agent refuses to bank an inference as a measurement. **Either figure is a valid non-zero positive control, so nothing on this page depends on the answer — but the lock commit should state which is which, since the builder ran it.** **0 tracebacks, 0 `GameError`, 0 probe exceptions in 700 games on the stack fixture; NOWINNER 0 of 850.**
**PLANNED n: 5400 games** (= 15 maps × 2 seats × 180, so map and seat balance is exact; `tools/overnight.sh:68` has run a 15-map pool since the 2026-08-13 rotation and its own comment requires multiples of 30). ⛔ **5400 IS SAID EXPLICITLY BECAUSE A SOLO SHARD OTHERWISE DEFAULTS TO A 2700 TARGET, and at 2700 the bar arithmetic below is unreachable** (margin 1.33pp against a half-width of ±1.87pp).
**BOUNDARY: 5400 games** — LOCAL surface, one tape row is one game; there is no accept/attempt distinction on this fixture and no accepts count is declared. ⛔ **A LINE COUNT IS NOT A ROW COUNT**: the tape carries an unprefixed header line under the `# FIXTURE` line, so a naive `wc -l` over-reports n by exactly one (measured on KLADLADDER, `results.tsv:kladladder-n-final-correction`; re-confirmed at draft — `wc -l scratchpad/overnight/BELTBREAK2.tsv` = 5,402 for 5,400 games). The registered denominator is **DictReader row count over non-`#` lines, cross-checked against the heartbeat's `n TARGET` and against `max(game id) + 1`.**
**CUT-SHORT: floor 2700 games.** Below 2,700 completed rows this arm publishes descriptive tallies (share, per-seat, per-map, per-class, kill-round, `cond` mix) and takes **NO bar verdict**; the one-sample half-width at 2,700 is ±1.87pp, already wider than the 1.33pp margin the bar is built on, so a sub-2,700 read cannot resolve its own branches. An `auto_gate` firing at CATASTROPHE@400, MARK-1000, TREND-FLOOR@1000, COMBO-BAR@2700 or the FUTILITY-BAR CI rule is an **OPERATIONAL CANCELLATION, not a verdict**, typed `cancellation`. ⭐ **ONE CARVE-OUT, PRE-COMMITTED:** a CATASTROPHE-clause cancellation (95% CI upper < 45.0 at n ≥ 400) is arithmetically INCOMPATIBLE with every band above Band 4, so a stop under that clause DOES license the Band-4 sentence at the partial n — **provided F1/F2 have been read first** and provided the partial share is disclosed as **selected-pessimistic** (a floor stop fires on a LOW PREFIX DRAW, so conditional on stopping the arm's true share is HIGHER than the number that stopped it; expect roughly +2pp of regression — side lane s47, n=2 cases, a DIRECTION with a rough size, not a calibrated correction). ⛔ **NO OTHER CLAUSE'S CANCELLATION LICENSES ANY BAND — see READ-BEFORE-RATIFYING #1 for the COMBO-BAR case specifically, which is the likely one at 0.740 unexempted / 0.000 exempted at the neutral hypothesis.**
**BAR: 51.33 ge. MDE: 0.00pp — THIS BAR IS A POINT RULE ONLY AND LICENSES NO EXCLUSION CLAIM ABOUT AN EFFECT SIZE** (OB16 corollary, 2026-08-15T03:52:45Z: the standard corefill band IS `50 ± half_width` at n = 5,400, so clearing 51.33 puts the CI's lower edge at exactly 50.00 — it excludes 50 and excludes no positive effect size whatsoever). n for the one exclusion it CAN make (bar ≠ 50.0): **5,400**, the planned n. ⛔ **AND ON THIS PAGE THE POINT-RULE STATUS IS NOT THE BAR'S WORST PROPERTY: per READ-BEFORE-RATIFYING #3 the bar is ALSO PRE-SATISFIED BY THE CARRIER (53.09, CI-lo 51.76), so clearing it licenses no sentence about the CLAUSE either. The bars that CAN fail because of the clause are the SECOND and THIRD falsifiers, and both are sized below.**
**BASE RATE: 50.00**
**BAR SOURCE:** the house-standard corefill futility band, `50 + 1.96*sqrt(0.98*0.25/5400) = 51.32pp`, rounded to the family's registered **51.33** — the identical bar carried by `docs/prereg/BARS.tsv` rows `SEALFLOOR6`, `SENTTHR`, `KLADTKILL`, `KLADTK2`, `KLADTURBOR`, `DRAINTURBO`, `KLADLADDER`, `SEALSENTAN`, `SEALSENTA`, `ROUTESCORE`, `BELTBREAK-EARLY`, `BELTBREAK-LATE` and `BELTBREAK2`, which is what keeps this arm numerically comparable to the turret-family reads it extends — **and specifically comparable to its own carrier, which is the point of a pair.** **Constructed, not observed.**
**BASE RATE SOURCE:** structural A/A expectation of a seat-balanced, map-balanced self-play fixture whose control tree is the treatment's own chassis base. Empirically calibrated by `IDNULL140` — **49.27% [47.94, 50.60] at n = 5,400**, 2026-08-16T18:02:04Z, same host and fixture (`results.tsv:idnull140-cert-5400`) — and by `NULL125` — **51.04% at n = 5,400** (`results.tsv:null125-final`). Two A/A cells, one either side of 50.0, both intervals containing it. ⇒ **a bare clearance in [51.33, 52.4] is a band an A/A cell has already produced**, which is why Band 2 is pre-registered as WEAK. ⚠ **The two cells are 1.77pp apart**; on a fixture where byte-identical arms can differ by that much, an arm whose registered comparator is 1.76pp below its own chassis's measured share is asking this fixture a question at its floor. **Disclosed before the data.**
**REFERENCE n: none** — the BAR's comparator is a CONSTRUCTED null of 50.00 generated inside this same shard from its own 5,400 seeds; there is no external reference SAMPLE for the BAR. ⛔ **THE CARRIER'S TAPE IS DELIBERATELY *NOT* DECLARED AS THIS BAR'S REFERENCE.** Naming it would make the checker size 51.33 as a two-fixture comparison at ±1.86pp and correctly FAIL it — a true statement about a bar nobody registered. **The carrier-vs-this-arm difference is a SEPARATELY REGISTERED ESTIMAND (the THIRD FALSIFIER), with its own explicit half-widths (±1.86pp share, ±1.68pp timely-kill, ±2.08 rounds RMST₃₀₀), its own same-host requirement, and its own pre-committed reading — it is not this bar's reference term and the two are never combined into one interval.**
**TREATMENT TREE: bots/_v504bbammo**
**TREATMENT DIFF REFS: 54129ed7^ 54129ed7 -- bots/_v504bbammo** — verified at draft: `git diff --name-only 54129ed7^ 54129ed7 -- bots/_v504bbammo` returns the four `.py` paths. ⚠ **The whole tree is ADDED in that commit, so a PATH-ONLY intersection would pass for a trivial reason, and that reading is REFUSED on this page** (the same refusal the carrier's page had to make for a different reason): `eco.py` and `raid.py` are **BYTE-IDENTICAL** to `bots/_v488beltbreak2`'s (`cmp` clean, verified at draft), so the only files that can make the metric read differently are the two the clause lives in. **The executable diff of record is against the CARRIER and is reproduced verbatim in THE CHANGE.**
**MECHANISM METRIC READS: bots/_v504bbammo/main.py:407-414 — the clause itself, `if LOKI_BBAMMO_ON: try: ti_floor = max(ti_floor, ct.get_gunner_cost() + LOKI_BELTBREAK_TI_FLOOR)`, the SINGLE site at which the reserve is imposed, inside the CORE's ammunition block and BELOW the E1 harvester-reserve block at `:390-394`. TREATMENT DIFF TOUCHES: bots/_v504bbammo/main.py, bots/_v504bbammo/doctrine.py. INTERSECTION: yes — DIRECT, not by import binding: the read site IS one of the added lines.** grepping `LOKI_BBAMMO_ON` across all four files of the arm tree returns **exactly two hits, `doctrine.py:1440` (the flag) and `main.py:407` (the read)**. **The metric therefore CANNOT read identically in the two arms, which is the LOKI-18 failure this obligation exists for** — and unlike the carrier's arm, this intersection is computable by git.
**METRIC WINDOW: r0-r1000. GATING CONSTANTS: LOKI_BBAMMO_ON=True, LOKI_BELTBREAK_TI_FLOOR=40, ENDGAME_RND=960, LAST_RND=1000, E1_AMMO_FLOOR_ON=True, E1_RESERVE_CAP=23, E1_HARV_RESERVE_MARGIN=23, AMMO_FLOOR=16, LOKI_BELTBREAK_AMMO=24, LOKI_BELTBREAK_RND=10, T4_AMMO_IDLE_RNDS=12, T4_AMMO_IDLE_MIN=16, T4_BURN_RNDS=10, T4_AMMO_PER_RND=4. MECHANISM CAN OCCUR IN WINDOW: yes** — **exactly ONE of these is a round gate**, `ENDGAME_RND = 960`, and it is a CLOSING gate, not an opening one: from r960 the endgame dump sets `endgame_dumped = True` and the whole drip block (and therefore this clause) is bypassed **in games where any weapon slot has ever been written**; where none has, the block runs to r1000. ⇒ **the mechanism's window is r0-r959 at worst and r0-r1000 at best, inside the declared r0-r1000, and there is NO opening gate at all — the clause is unconditional on round, on map, on `bb_live` and on whether a shredder exists (READ-BEFORE-RATIFYING #5).** The rest are titanium/ammunition thresholds, counts, and staleness budgets in rounds.
⚠ **DISCLOSED, because a green tool run with warnings under it is how a warning stops being read: `tools/prereg_check.py` will emit `OBLIGATION 17, PARTIAL WINDOW` warns against the line above and THEY ARE ARTEFACTS OF THE CHECKER.** Its `check_metric_window` arithmetic reads every declared integer as a ROUND, so a Ti reserve of 40, an ammo floor of 16 and a magazine of 24 render as "rounds r0-r15 cannot contain the mechanism". The constants are declared anyway — an undeclared constant is the failure OB17 exists for.
**PLANK CLASS: ECONOMIC — a funding-reservation clause on the CORE's titanium-to-ammunition drip, in service of an OFFENSIVE plank (a forward gunner planted in the enemy's belt). Not defensive, not a survival plank, not a home screen.** ⭐ **AND THE r300 ADMISSION READ IS REGISTERED ANYWAY, NOT CLAIMED AS INAPPLICABLE.** `PROGRAMME.md`'s `DEFENCE_ADMISSION_BAR` binds on defensive planks; it is carried here regardless because **this clause has an ALREADY-MEASURED kill-delay signature — ITT timely-kill 28.0% → 22.5% and median kill 259 → 303 at n=200 (READ-BEFORE-RATIFYING #4), plus a monotone dry-turret-rounds cost curve (READ-BEFORE-RATIFYING #2) — and a plank with a measured kill-delay signature carries a kill-delay bar whatever its class label.** Registering it is strictly stricter than the programme requires and cannot function as a second chance to pass: **the share bar, the r300 bar AND the clause falsifier must all hold.**
**KILL-ROUND NON-REGRESSION: ITT RMST₃₀₀ is the operational estimator (PROGRAMME.md's 2026-08-16T05:36:10Z arbitration, whose vintage rule makes it binding on preregs locked from that date — this one is) — mean kill time censored at the r300 horizon over ALL games, a non-kill scoring 300, computed per side on the same rows; the bar is scored as an EXCLUSION: the 95% CI UPPER bound on (treatment RMST₃₀₀ − control RMST₃₀₀) must EXCLUDE +5.0 rounds (MDE +5.0 rounds; paired sd on the carrier's own tape is 85.02 rounds ⇒ half-width ±2.24 at n=5,400, so the exclusion resolves). SECOND REGISTERED FORM, both required: the ITT timely-kill-by-r300 rate (share of ALL games ending `cond == core_destroyed` with `turns <= 300`, denominator every game played, per side) — its 95% CI LOWER bound on (treatment − control) must EXCLUDE a fall of 3.0pp (MDE 3.0pp; paired sd 73.99pp ⇒ half-width ±1.95pp at n=5,400). THIRD, THE GROSS BACKSTOP AND IT IS REGISTERED EXPLICITLY BECAUSE THE n=200 READ ALREADY CROSSED IT: the treatment's kill-win-conditioned MEDIAN kill round must not cross 300 (carrier anchor 244; the stack's L0+L3 cell read 303 on its own chassis). FOURTH, and it is a DIAGNOSTIC ONLY because it carries a collider: the kill-win-CONDITIONED share plus the conditioned median — reported beside the bars, never as one of them.**
**PRE-STATE: SPLIT VERDICT, and the split is the honest answer rather than a hedge.** ⭐ **The MECHANISM's predicted change is NOT already in the target state.** Verified at draft against both comparisons: `grep -c 'BBAMMO\|AMMOFLOOR\|ammofloor' bots/_v468kladturbo/{doctrine,eco,main,raid}.py` → **0/0/0/0** and the same greps on `bots/_v488beltbreak2/*` → **0/0/0/0** — neither the control nor the carrier has any ammo-floor reservation at all, so the whole clause is absent from both, and the reserve regime it imposes (`ti_floor ≥ gunner_cost + 40 ≥ 60`) is one the incumbent block cannot reach (its ceiling is `52`, and E1's is `46`). The stack's measurement confirms it fires: bank at r95-105 **29 → 54 Ti**, plants **+0.450 CI excluding 0**. ⛔ **BUT THE OUTCOME CLAIM *IS* PARTIALLY PRE-SATISFIED, AND THAT IS OB7'S DEFECT IN ITS DUAL FORM: the pooled bar (51.33), the ITT timely-kill bar (fall ≤ 3.0pp), the RMST₃₀₀ bar (rise ≤ 5.0 rounds) and the median backstop (300) are ALL cleared by the CARRIER ALONE at the full registered n** (53.09 CI-lo 51.76 · +6.44pp · −7.30 rounds · median 244). **A prereg whose bars are cleared by the chassis it is testing an addition to cannot fail honestly about the addition.** ⇒ **the THIRD FALSIFIER exists precisely to supply a bar that CAN fail on the clause, and this token records the defect rather than papering it.** *(Recorded per OB7's own template, which requires the pre-state check to be performed on the OUTCOME as well as the mechanism.)*
**MAP SEGMENT: plank-EXPRESSIBLE maps — the 12 of 15 excluding `antler`, `fjordgate` and `royale` — mechanism reason: those three plant ZERO (antler, fjordgate) or ~zero (royale) shredders in BOTH arms, because on maps of small area the d²20-100 annulus of the ENEMY core overlaps our own hunt band (`HUNT_BAND_DSQ = 41` of OUR core) and no tile satisfies both clauses of the siting predicate — measured on two independent instruments (the carrier's dose battery, and the carrier's own n=5,400 tape where those three are the flattest cells of fifteen: antler 47.78%, fjordgate 51.67%, royale 50.28%, every CI containing 50). EXPECTED DIRECTION POSITIVE on the segment, and ⭐ NEGATIVE — NOT A/A — on its complement, because this clause fires on EVERY map whether or not a shredder exists (`main.py:407`, guarded on the flag and nothing else), so on the three inexpressible maps it delivers reserve cost with no plant to fund.** This is ONE primary segment. The `CQ`/`STD`/`GRAND` split (`tools/overnight_read.py:76-94`) and the per-map table are **DESCRIPTIVE ONLY** and carry no pre-registered direction. ⚠ **The segment is defined by MEASURED EXPRESSIBILITY, not by area class: `royale` is `STD` by area (`map_area_class`, computed at draft) and is in the complement anyway because the mechanism reason is "no tile satisfies the siting predicate", which area only proxies.** A proxy dilutes (OB15's segment-vocabulary note), and the carrier's own verdict row reports both cuts, so this is the cut with the mechanism attached. **Disclosed: the segment was chosen using the carrier's data, so it is PRIOR-INFORMED, not blind; the prediction it makes about THIS arm's 5,400 rows is out-of-sample, which is what OB15c requires — the choice itself is not.** **Per OB15b/15c: the pooled bar is the bar; a pooled fail that clears on-segment RE-SCREENS as a NEW leg with its own n, never as a re-read of these rows.**
**EXPECTED DIRECTION: POSITIVE on the plank-expressible segment (12 maps, n=4,320, ±1.48pp), and NEGATIVE on its complement (antler, fjordgate, royale — n=1,080 pooled, ±2.95pp; ±5.11pp per cell at n=360).**
**SEGMENT VALUE CEILING: 80.00% x 1.91pp = 1.53pp.** The share is the segment's pairing weight, 12 of 15 maps = 80.00% of a balanced shard. **1.91pp is the on-segment effect the pooled 1.33pp margin REQUIRES once the complement's own predicted NEGATIVE drag is added back** rather than merely diluted: at −1.0pp on 20.00% of games the complement subtracts 0.20pp pooled, so `(1.33 + 0.20)/0.80 = 1.91` and `0.80 × 1.91 = 1.53`, of which 1.33 survives. ⇒ **the dilution is a HARD CAP AND THE COMPLEMENT IS A HARD DEBIT: no on-segment effect can pool above 0.8000× itself, and unlike the carrier's arm the two dead cells are not free — they are a cost centre.** *(The conservative variant, recorded so a later reader can price it without re-choosing anything: if `royale` were treated as expressible, `13/15 = 86.67%` and the required on-segment effect falls to 1.62pp — it is NOT moved, because the segment must be fixed on the mechanism reason and royale's measured dose is ~0.)*
**POOL ERA: post-2026-08-13-rotation** — the 15-map local pool of `tools/overnight.sh:68`. (`check_pool_era` treats this as n/a on a LOCAL surface per SPEC §6; declared anyway so the population is on the page.)
**CELL VERSION CHURN: N/A — not a panel, no `CELLS:` line, one fixed local control tree.**
**GATE RESOLUTION: four gates, sized separately.**
* **(a) THE SHARE BAR.** Margin 1.33pp against a one-sample half-width of ±1.32pp at n=5,400, DEFF 0.98 — resolvable, and only just. ⚠ **The slack is 0.01pp, which is `GUNAXABL`'s exact failure mode: that arm missed its keep edge by 0.0152pp — ONE GAME — on a bar with zero constructed slack.** Registered consequence: **a result within one game of the bar is reported as "the fixture cannot resolve the question", not as a verdict in whichever direction the rounding falls.** ⛔ **AND SEE #3: even when this gate RESOLVES, it resolves a question about the PAIR, never about the clause.**
* **(b) THE r300 ADMISSION BARS.** RMST₃₀₀: MDE +5.0 rounds against half-width ±2.24 → resolves. ITT timely-kill: MDE 3.0pp against ±1.95pp → resolves. Median backstop: a point comparison against 300, no interval, and it is registered as a BACKSTOP for exactly that reason. Branches separated by construction. ⛔ **But all three carry the carrier's slack (#3): they resolve whether the PAIR delays the kill relative to the CONTROL, not whether the CLAUSE does.**
* **(c) THE CLAUSE GATE (THIRD FALSIFIER).** Share difference vs the carrier's tape: ±1.86pp against the stack's measured −5.0pp → resolves. ITT timely-kill difference: ±1.68pp against −5.5pp → resolves. RMST₃₀₀ difference: ±2.08 rounds → resolves anything above ~4 rounds. **This is the only gate on the page that can fail because of the thing the leg is testing, and it resolves at the effect sizes already measured.** ⛔ **It is VOID if the shard runs off MacBook-Pro** (cross-host rider), and an UNRESOLVED clause gate **defaults to the RESTRICTION: no promotion, no combination claim, no ship conversation.**
* **(d) THE OPERATIONAL FLOORS.** `CATASTROPHE@400` (CI-hi < 45.0, `auto_gate.py:244,247`), `MARK-1000`/`TREND-FLOOR@1000` (prefix < 52.0, `:261`), `COMBO-BAR@2700` (prefix < 55.0, `:278`) and the `FUTILITY-BAR` CI rule with its `0.5 × half-half-width` margin at MARK-1000/2700 (`:971-991`) — all Magnus's confirmed constants. Their firings are **OPERATIONAL CANCELLATIONS** that free a core, typed `cancellation`, never `verdict`, licensing no exclusion claim beyond the CATASTROPHE carve-out in CUT-SHORT. **The floors bind REMOTE too (`a50f27ef`, s48, via `tools/remote_cancel.py`), so the binding registration is not "LOCAL" but "SAME HOST: MacBook-Pro".** ⛔ **AND (d) IS THE GATE MOST LIKELY TO DECIDE THIS ARM'S FATE — at the neutral hypothesis, 0.976 probability of cancellation without the COMBO exemption and 0.239 with it (READ-BEFORE-RATIFYING #1).**
**Everything else on this page (F1, F2, D3, D4, the seat / map / class splits) is DIAGNOSTIC and cannot rescue a failed bar. Any branch that does not resolve is UNRESOLVED, and an UNRESOLVED gate defaults to the RESTRICTION: no promotion, no ship conversation, no combination claim.**

---

## THE CHANGE — `file:line`, carrier → treatment

**TREATMENT TREE: `bots/_v504bbammo`** = `bots/_v488beltbreak2` plus **ONE
GUARDED ASSIGNMENT and ONE FLAG**. Verified at draft, and re-runnable in four
commands:

```
$ cmp bots/_v488beltbreak2/eco.py  bots/_v504bbammo/eco.py    # clean
$ cmp bots/_v488beltbreak2/raid.py bots/_v504bbammo/raid.py   # clean
$ diff bots/_v488beltbreak2/doctrine.py bots/_v504bbammo/doctrine.py \
      | grep -E '^[<>]' | grep -vE '^[<>] *(#| *$)'
> LOKI_BBAMMO_ON = True
$ diff bots/_v488beltbreak2/main.py bots/_v504bbammo/main.py \
      | grep -E '^[<>]' | grep -vE '^[<>] *(#| *$)'
>             if LOKI_BBAMMO_ON:
>                 try:
>                     ti_floor = max(
>                         ti_floor,
>                         ct.get_gunner_cost() + LOKI_BELTBREAK_TI_FLOOR,
>                     )
>                 except Exception:
>                     pass
```

⇒ **ONE non-comment line added to `doctrine.py` (`:1440`, the flag) and EIGHT
physical lines forming ONE guarded assignment added to `main.py` (`:407-414`).**
Nothing is removed anywhere: the full diffs are `doctrine.py` +5 / −0 (4 comment
lines + the flag) and `main.py` +20 / −0 (12 comment lines + the 8). **`eco.py`
and `raid.py` are BYTE-IDENTICAL to the carrier's, `cmp` clean.**

**⚠ PRECISION, because the brief and the tree's own comment both say "one
clause": it is ONE STATEMENT, not one executable LINE.** Calling it a one-line
diff would be wrong, and this page does not.

**THE PLACEMENT, and it is the load-bearing property of the clause** —
`bots/_v504bbammo/main.py:389-414`:

```python
            ti_floor = 12 if (under or weapons_top) else 52     # :389  the TWO BRANCHES
            if E1_AMMO_FLOOR_ON and not under:                  # :390  E1 raises it to <=46
                ti_floor = max(
                    ti_floor,
                    min(ct.get_harvester_cost(), E1_RESERVE_CAP) + E1_HARV_RESERVE_MARGIN,
                )
            if LOKI_BBAMMO_ON:                                  # :407  THE CLAUSE
                try:
                    ti_floor = max(
                        ti_floor,
                        ct.get_gunner_cost() + LOKI_BELTBREAK_TI_FLOOR,
                    )
                except Exception:
                    pass
```

* **BOTH BRANCHES.** `:389` is the two-branch construction (armed `12` / unarmed
  `52`); the clause sits AFTER it and applies to whichever was taken. That is
  dose-4's SHAPE, and it honours the sweep's finding that **unarmed-branch-only
  reserves are INERT** (dose 1 changed 0 of 120 cells on every metric; the
  unarmed branch is 0.8 of 107.8 wanted-rounds per game).
* **BELOW E1, COMPOSING BY `max()`.** ⇒ **E1's harvester-rebuild reserve is an
  INPUT here and can never be LOWERED by this clause** — verified by reading the
  composition, not asserted: `max()` is monotone. This is Magnus's s48 warning
  honoured in the direction a turret plank is likely to breach it.
* **`LOKI_BELTBREAK_AMMO` (24) IS DELIBERATELY NOT IN THE SUM**, with the
  rationale on the page at `:404-406` and independently reached by the stack at
  `:1741-1746` (the +`AMMO` variant is dose 7, ~130 Ti, *"NOT a candidate"*).
* ⚠ **THE `try/except Exception: pass` IS A CORRECTNESS GUARD AND ALSO A SILENT
  ONE.** `ct.get_gunner_cost()` should not raise, and an escaping exception from
  `run()` permanently destroys the unit — here the CORE — so catching is right.
  **But a bare `except: pass` means a clause that never fires and a clause that
  fires every round are INDISTINGUISHABLE from the outside**, which is why F1's
  reserve read (below) is registered as a MEASUREMENT rather than assumed. *(The
  carrier's `_v501ammofloor` sibling used the identical shape; the observation is
  about the family, not about this build.)*

**THE READ SITE, and it is exactly one:** `grep -n 'LOKI_BBAMMO_ON'
bots/_v504bbammo/*.py` → **two hits, `doctrine.py:1440` and `main.py:407`.**
The clause is **not** on any raider path, does not touch `SLOT_BELTBREAK`,
`SLOT_FWD_GUN` or `SLOT_HOME_GUN`, and does not change the plant path's own
funding gate at `raid.py:902-907` — **it changes only what the CORE is allowed to
spend on ammunition.**

---

## SEGMENT AND POPULATION — the split, its n, and the dilution arithmetic

**Registered per-class n at the planned 5,400** (classes from
`tools/overnight_read.py:76-94 map_area_class`, computed at draft from each map's
own `.map26` header, never a hardcoded size table):

| class | area | maps | **n** | half-width at DEFF 0.98 | status |
|---|---|---|---:|---|---|
| **CQ** | ≤ 260 | antler, fjordgate | **720** | **±3.62pp** | DIRECTION-ONLY |
| **STD** | 261-676 | archipelago, auroraveil, drumlin, frostgate, icefloe, nordkap, royale, yulerune | **2,880** | ±1.81pp | DIRECTION-ONLY |
| **GRAND** | > 676 | drakkarfjord, glacierkeep, midgard, ragnarok, valkyrie | **1,800** | ±2.29pp | DIRECTION-ONLY |
| **PRIMARY SEGMENT** (expressible, 12 maps) | — | all but antler, fjordgate, royale | **4,320** | **±1.48pp** | the one segment carrying a registered direction |
| **COMPLEMENT** (inexpressible, 3 maps) | — | antler, fjordgate, royale | **1,080** | **±2.95pp** (±5.11 per cell) | registered direction NEGATIVE |

**⇒ EVERY size class is pre-labelled DIRECTION-ONLY: none of the three can
resolve the 1.33pp margin the pooled bar is built on.** Only the pooled read
(±1.32) and the primary segment (±1.48, marginal) can, and the segment's own
margin would have to be 1.48pp or better against a required 1.91pp — **which is
why the segment cell is registered as CONFIRMATORY-IF-IT-CLEARS and never as a
rescue for a pooled fail.**

**THE ARITHMETIC, written out because it is a HARD CAP AND A DEBIT rather than a
caveat:**

```
pooled = 0.8000 x on_segment  +  0.2000 x on_complement
with the registered complement direction NEGATIVE (registered value -1.0pp):
   to clear the pooled bar (+1.33pp over 50):  on-segment >= 1.91pp
   CEILING: no on-segment effect can pool above 0.8000x itself
CONTRAST WITH THE CARRIER, whose complement was A/A (0.0pp) on 2 of 15 maps:
   its required on-segment effect was 1.54pp; this arm's is 1.91pp, i.e. 24% higher
   for the SAME pooled margin, because its dead cells cost rather than dilute.
```

⭐ **INDEPENDENT CORROBORATION OF THE DEAD CELLS, off a tape that is NOT this
arm's data and NOT the dose instrument** — `scratchpad/overnight/BELTBREAK2.tsv`,
the carrier's own shard, n=5,400, recomputed at draft: **antler 47.78%,
fjordgate 51.67%, royale 50.28%** (the three flattest of fifteen, every CI
containing 50) against **EXPRESSIBLE-12 at 53.89% [52.40, 55.38]**. **The dose
instrument and the outcome tape agree about which cells are dead, and they are
different instruments.**

---

## FALSIFIER

**PRIMARY FALSIFIER: at n = 5,400 the 95% CI UPPER bound on this arm's pooled
share vs `bots/_v468kladturbo` falls BELOW 51.33.** That excludes the arm's own
bar. ⚠ **And per READ-BEFORE-RATIFYING #3 this falsifier is about the PAIR: it
can fail only if the clause costs more than the carrier's entire 1.76pp of
headroom, and it can pass while the clause costs up to that much.**

**SECOND FALSIFIER (the r300 admission bars, and each can fail on its own while
the share passes):** the 95% CI UPPER bound on (treatment − control) ITT RMST₃₀₀
fails to EXCLUDE +5.0 rounds; **or** the CI LOWER bound on the ITT
timely-kill-by-r300 difference fails to EXCLUDE a fall of 3.0pp; **or** the
treatment's kill-win-conditioned median kill round crosses 300. **Any one is
disqualifying on its own, regardless of the share** — `PLAY_DEFENCE:
not_at_the_kill_s_expense`, and this clause's measured kill-delay signature is
why the bar is carried on an economic plank. **Anchors from the carrier's tape,
quoted as anchors and NOT as this arm's prediction:** RMST₃₀₀ **T 268.21 vs
C 275.52** (treatment 7.30 rounds FASTER, paired sd 85.02); ITT timely-kill
**30.80% vs 24.35%**, paired diff **+6.44pp**, paired sd 73.99pp; kill-win
median **244**; `cond` mix **core_destroyed 4,791 / tiebreak 609 of 5,400**.

**⭐ THIRD FALSIFIER — THE CLAUSE FALSIFIER, AND IT IS THE ONLY BAR ON THIS PAGE
THAT CAN FAIL BECAUSE OF THE THING BEING TESTED.** Treatment's tape against
`scratchpad/overnight/BELTBREAK2.tsv` (n=5,400, identical control, identical
15×2×180 balance, `host=MacBook-Pro`), two-sample, DEFF 0.98 both sides, all
three pre-sized:

| read | half-width | **the clause is REFUSED as a carrier modification if** |
|---|---|---|
| pooled share difference | ±1.86pp | the CI UPPER bound is below **−1.0pp** |
| ITT timely-kill difference | ±1.68pp | the CI UPPER bound is below **−3.0pp** |
| ITT RMST₃₀₀ difference | ±2.08 rounds | the CI LOWER bound is above **+5.0 rounds** |

**Each is written as an EXCLUSION, per the DEFF-direction rule** (a
fail-to-exclude must be restated as an exclusion before the correction is
applied, or DEFF launders a weak null into a confident one). ⇒ **a refusal here
means: whatever the pooled bar says about the PAIR, the clause is a net cost ON
THE CARRIER and `LOKI_BBAMMO_ON` does not go forward.** ⛔ **VOID if the shard
runs off MacBook-Pro; VOID if the carrier's tape is amended or re-stocked after
this lock. A void clause gate is UNRESOLVED and defaults to the restriction.**
⚠ **Explicitly NOT a paired estimator: `NOISE_ON` pins an unseeded RNG
(`main.py:445`) and `fcode run` is measured NON-reproducible for this chassis —
three runs of antler seed 1 returned 45/106/74 event rows
(`results.tsv:beltbreak2-final`). Seed-paired language is void for this chassis;
the shared seed base controls map/seat/opponent, never the spawn salt.**

**MECHANISM FALSIFIER (independent of all of the above, and it fires FIRST):**
* ⭐ **THE REGISTERED CROSSING. If F1 shows shredder plants per game UP but
  SHOTS-PER-SHREDDER DOWN outside its own band, the arm is DISQUALIFIED on the
  mechanism regardless of every share on the page.** *Plants up, shots down* is
  the exact trade that disqualified the sweep's dose 3 (−27.5pp timely-kill) and
  collapsed the full stack (14.0 → 6.2 shots/shredder, total fires −46%). **It
  is not a mixed result; it is the named failure mode.** Registered form: plants
  UP **with** shots/shredder inside ±15% of the flag-off control's.
* if **F1** shows the treatment's shredder plants per game are not above the
  flag-off control's outside the band, **the clause did not deliver its dose**
  and the share is **uninterpretable**: a flat share would mean "the mechanism
  never fired", not "the mechanism fired and did not pay". The primary is then
  reported as **NOT MEASURED**, not as a null. *(This branch is close to closed
  before the fire — the stack measured +0.450 CI [+0.134, +0.766] under NOISE_ON
  — which is why the crossing, not the dose, is the live mechanism question.)*
* if **F1(d)** shows the realised reserve is NOT above the flag-off control's
  `ti_floor` at matched rounds, **the clause is a wiring null** and the shard ran
  two identically-behaving bots. The `except Exception: pass` at `:413` is the
  named path by which this could happen silently.
* if **F1(e)** shows dry-turret rounds and mean ammunition held UNCHANGED, the
  registered magazine cost did not materialise — **which is a GOOD outcome and
  must be reported as such rather than dropped.**
Per FIRINGS-BEFORE-PRIMARY all of F1 and F2 are read BEFORE the primary is typed.

### ⭐ THE HONEST-NULL CLAUSE — pre-committed, THREE branches, because the third is what two fixtures already say

**The registered discriminator is F1's five reads, and they are read before the
share.**

| state | evidence | pre-committed reading |
|---|---|---|
| **1. THE DOSE DID NOT LAND** | F1(a) plants flat, and/or F1(d) shows no reserve regime change | **NOT MEASURED.** The leg says nothing about funding. The defect is wiring (the silent `except`) or a scale regime the reserve never reached, the road stays open, and the repair is a probe, not a verdict. |
| **2. THE RESERVE WAS EATEN BY SOMETHING OTHER THAN SHREDDERS** | F1(a) plants flat **while** F1(d) confirms the reserve regime DID change and F1(e) confirms ammunition fell | ⭐ **A REAL FINDING: the money was withheld and did not become shredders.** Bank rose, plants did not. Names the plant path's OTHER binding constraints as dominant — the stack's own funnel says the top refusal is **STILL `TI`** after four legs (62-75%), and that would be a second instrument saying the same thing. Prices the funding axis DOWNWARD; the next iteration is SITING, not funding. |
| **3. ⭐⭐ THE RESERVE DELIVERED PLANTS AND THE MAGAZINE COST ATE THE KILLS** | F1(a) plants UP **and** F1(e) shows ammunition held DOWN / dry-turret rounds UP **and** the crossing read shows shots-per-shredder DOWN, with the share and/or the r300 bars flat-to-negative | ⛔ **A REAL FINDING AND THE MODAL OUTCOME BY TWO FIXTURES' EVIDENCE: more shredders, each firing less, fewer kills.** The deepest form of it, and it must be written down before it is explained away: **PLANTS WERE NEVER THE KILL CONSTRAINT.** The stack measured **+33% shredders delivering FEWER kills** (plants 1.365→1.815 with wins 112→102, kills 103→95) and the control-chassis sweep reached the same conclusion independently (*"the kill constraint is turret THROUGHPUT, not COUNT"* — dose 3 bought +7.8 turrets, lost 13.8 shots, gave back −27.5pp). **This branch closes the FUNDING road for the shredder family and re-points the line at throughput: rotation, targeting, and shots per plant.** |

**⛔ THE DISCRIMINATOR BETWEEN 2 AND 3 IS EXACTLY F1(a) × F1(e) × the crossing,
which is why those three reads are LOAD-BEARING AND NOT DECORATIVE, and why the
firings sequence is HARD.** Branch 2 says *the money never became weapons*;
branch 3 says *the money became weapons that could not shoot*. **They point the
line at different next iterations and no share on the tape can tell them apart.**

⚠ **ATTRIBUTION BOUND ON EVERY BRANCH, per READ-BEFORE-RATIFYING #2: this leg
does NOT separate "reserving the shredder's price is wrong" from "reserving ~94
Ti is too much and ~54 would have been right".** Naming which requires a dose
ladder on this chassis (the sweep's dose 4 at bare `get_gunner_cost()` is the
obvious rung and is NOT this arm), which this leg is not. **No readout sentence
may pick one.**

---

## READING, PRE-COMMITTED

Registered now so no band is chosen after the fact. **Read TOP-DOWN; the first
row whose condition holds is the reading. Rows are disjoint by construction.**
**Every band below is CONDITIONAL on (i) F1 and F2 having been read first, (ii)
the mechanism crossing having HELD (plants up, shots/shredder flat), and (iii)
the r300 admission bars having HELD. A crossing failure or an r300 failure
overrides every row** — the reading is then `DISQUALIFIED — plants up, shots
down` or `OFF-PROGRAMME — kill delayed`, whatever the share.
⛔ **AND EVERY BAND CARRIES ITS THIRD-FALSIFIER RESULT INLINE: a band claimed
without the clause contrast beside it is a sentence about the pair being read as
a sentence about the clause, which is this page's central named defect.**

| # | band on this arm's pooled share vs `bots/_v468kladturbo` at n = 5,400 | pre-committed reading |
|---|---|---|
| **1** | **CI lower ≥ 51.33 AND the clause contrast does not refuse** | **THE PAIR HOLDS AND THE CLAUSE IS NOT A COST.** Promotes to a combination input and to a separately-registered head-to-head. ⚠ Report the size with its OB16 status: this bar's MDE is 0, so this branch may claim "we can exclude 50 vs `_v468kladturbo`" and may NOT claim any minimum effect size. ⚠ **And it may NOT claim the clause ADDS unless the clause contrast's CI LOWER bound excludes 0** — otherwise the honest sentence is "the clause is free on this carrier", which is Band 1's likely content. |
| **2** | **point ≥ 51.33 but CI lower < 51.33** (includes the whole [51.33, 52.4] window an A/A cell has already produced) | **REAL-BUT-SMALL, COMBINATION INPUT ONLY.** Pre-registered as WEAK: `NULL125`'s byte-identical A/A read 51.04, and the two A/A cells are 1.77pp apart. Rows are KEPT; no ship conversation; a replication on fresh seeds, same host, is the price of promoting it. **And note what this band means HERE: it is 1.7pp+ BELOW the carrier's own measured share, so on this page Band 2 is evidence the clause SUBTRACTED — read the clause contrast, not the band label.** |
| **3** | **point < 51.33 AND CI contains 50.0** | **THE PAIR LOST THE CARRIER'S EDGE.** Since the carrier alone measured 53.09 [51.76, 54.42] on the identical fixture, a pooled read at parity is a **~3pp fall attributable to the one clause** — and at ±1.86pp the clause contrast resolves it. **REGISTERED CONSEQUENCE: `LOKI_BBAMMO_ON` dies as a carrier modification and the funding axis is priced DOWNWARD**, joining the sweep's dose-3 disqualification and the stack's `BBSTACK_L3_AMMOFLOOR = False`. **Attribution is bounded per #2: this refutes the ~94-Ti reserve on this chassis, NOT the ~54-Ti rung, and NOT "funding never binds".** |
| **4** | **CI upper < 50.0** | **THE PAIR IS WORSE THAN THE BOT WE SHIP.** The clause did not merely fail to add, it destroyed a measured +3.09pp. `RND=10 + BBAMMO` dies as a ship candidate outright, and **the third instance of the same shape** (sweep dose 3, stack L0+L3, this) is enough to say the FUNDING road for the shredder family is closed on local evidence and to spend the next core on THROUGHPUT. **⛔ Per LOKI directive point 6 a local screen still cannot CLOSE a road; the honest form is "closed on local evidence, prioritised for no further local spend", and a live-team unrated leg remains the only instrument that could close it.** |

⚠ **Nothing here treats 50.0 as a floor.** A share below 50 is a live outcome
with named mechanisms (a ~94-Ti reserve withheld from a magazine whose shot price
does not scale; dry-turret rounds reconstructed at ~114/game; ammunition held
reconstructed at ~15 against a control's 30.9) and it is pre-named so a negative
is not explained away as noise.

⛔ **AND ONE CROSS-BAND NOTE, registered so it is not improvised: a
`COMBO-BAR@2700` or `TREND-FLOOR@1000` cancellation reaches NONE of these rows.**
Per READ-BEFORE-RATIFYING #1 those are operational stops on the CHASSIS TOTAL and
the reading is `CANCELLED — combination below the 55.0 prospecting bar (or below
the 52.0 trend floor); the funding question is UNRESOLVED and defaults to the
RESTRICTION`.

---

## FIRINGS-BEFORE-PRIMARY — the reads, with exact invocations

**Measurability is declared per read. `NOT MEASURABLE` is written where it is
true, rather than a metric being quietly renamed into something the tape happens
to carry.** ⛔ **NOTHING BELOW READS OUR OWN `print()` OR `stderr` OUTPUT AS ITS
PRIMARY INSTRUMENT.** Platform replays strip `stdout` (30,664 of 30,664 events,
`CLAUDE.md` s28) and `bots/_v504bbammo/doctrine.py:1459` has
`LOKI_BELTBREAK_LOG = True`, whose prints are therefore useless off any platform
surface. **On a LOCAL replay they ARE readable and are admitted as a SECONDARY
cross-check only, never as the read of record** — every quantity below has an
engine-side form. *(Note for a ship conversation, not for this screen:
`LOKI_BELTBREAK_LOG = True` is a ship-blocker to be turned off and re-screened.
It is identical in both arms here, so it cannot bias this contrast.)*

### F1 — THE DOSE, THE CROSSING AND THE COST. MEASURABLE, but NOT off the shard tape and NOT via `tools/dose.py`.
`tools/overnight.sh:138-139` passes `--replay /dev/null`, so the shard produces
**no** entity events. And per READ-BEFORE-RATIFYING #7, **`tools/dose.py` cannot
run this battery at the shard's fixture** — it emits no `--tle` and `fcode run`
defaults to `--tle 0` (limit disabled). **F1 therefore runs as a DIRECT battery**,
SERIAL (never parallel: D65, a 16-game parallel dose check once reported the
OPPOSITE of a serial one and both were wrong), reproducing `dose.py:218-231`'s
rotation so the fixture stays comparable:

```
# REGISTERED SIZE: 60 games per arm (15 maps x 2 seats x 2 seeds), SERIAL, --tle 10.
# TREATMENT: bots/_v504bbammo      CONTROL: the SAME TREE with LOKI_BBAMMO_ON = False
#   (== bots/_v488beltbreak2, cmp-verified; the flag-restore control is the ONLY
#    comparison that isolates the clause. NOT bots/_v468kladturbo.)
mkdir -p scratchpad/bbammo_replays
n=0; seed=0
for M in antler archipelago auroraveil drakkarfjord drumlin fjordgate frostgate \
         glacierkeep icefloe midgard nordkap ragnarok royale valkyrie yulerune; do
  for S in 1 2; do
    for ORD in A B; do
      .venv/bin/fcode run <BOT_A> <BOT_B> maps/$M.map26 --seed $S --tle 10 \
        --replay scratchpad/bbammo_replays/g$(printf %04d $n)_${M}_s${S}_${ORD}.replay26
      n=$((n+1))
    done
  done
done
.venv/bin/python tools/corpus/replay_events.py scratchpad/bbammo_events.tsv \
    scratchpad/bbammo_replays/*.replay26
```
**⛔ `--tle 10` IS THE WHOLE POINT OF THE SUBSTITUTION** and its consequence is
measured, not argued: on the carrier, `--tle 0` returned "no information at 0.98×
of the band" while the same registered n=60 on the shard's own fixture read
**DOSE DELIVERED at 1.26×/1.45×**, and the doctrine's median plant round
49.5→40 reproduced only at `--tle 10` (`results.tsv:beltbreak2-final`).

**The five reads, all engine-side off the decoded events
(`tools/corpus/replay_events.py:157` emits `file ev rnd team kind x y d2_own
d2_enemy mw mh`):**
* **(a) SHREDDERS PER GAME — THE DOSE.** Friendly `BUILD`/`kind == gunner` events
  whose FIRST `placeEntity` lands at **d²_enemy 20-100 AND d²_own > 41**
  (`HUNT_BAND_DSQ`), per game, per arm. **Pre-registered expectation: treatment
  strictly above the flag-off control's, paired difference outside a 2×SE band.**
  Anchor, NOT a prediction: the stack read **+0.450, CI [+0.134, +0.766]** for
  this clause at n=200 NOISE_ON.
* **(b) ⭐ SHOTS PER SHREDDER — THE CROSSING, AND THE DISQUALIFYING READ.**
  Friendly turret-fire events attributable to the shredder ids from (a), divided
  by the shredder count, per arm; **total fires reported alongside, because a
  per-unit ratio can hold while the total collapses** (the full stack's fires fell
  46% — the ratio and the total must BOTH be reported). **Pre-registered
  expectation: FLAT, within ±15% of the flag-off control's.** Anchors: carrier
  25.7 → 24.7 flat on 360 games; the stack's paired battery 14.0 (chassis) → 13.6
  (this clause) → 6.2 (full stack). ⚠ **The stack did NOT re-read this under
  NOISE_ON**, so the flat finding rests on the paired battery alone — which is
  exactly why it is registered here as the crossing rather than assumed.
* **(c) TI-REFUSAL COUNT ON THE PLANT PATH.** `_bb_refuse("TI", …)` occurrences
  per game (`raid.py:906-907`), treatment vs flag-off control. **Pre-registered
  expectation: DOWN for the treatment** — that is the clause's proximate claim
  (the bank is what refuses; the reserve raises the bank). Anchors: 638×/game on
  the carrier's instrumented probe, ~56/game on the stack's post-fix funnel, and
  the stack's *"AMMOFLOOR MOVED THE BANK WITHOUT DETHRONING IT"* (bank r95-105
  29→54 Ti, TI refusals unchanged). ⛔ **AND THE ANTI-INFERENCE IS REGISTERED
  BECAUSE THE STACK'S ABLATION EARNED IT: `a refusal counter names the rung that
  fired, NOT the constraint that binds` — its `CAP 10.4/game` read as "the cap
  now binds" and raising the cap bought nothing.** A fall in (c) is therefore
  NOT by itself evidence the clause worked; only (a) is. **This read is
  SECONDARY, off the local replay's captured `LOKI_BELTBREAK_LOG` output, and is
  labelled as such.**
* **(d) THE REALISED RESERVE — the read this page adds and the one that locates
  the arm on the sweep's ladder.** Reconstruct `get_gunner_cost() +
  LOKI_BELTBREAK_TI_FLOOR` at fixed rounds (**r25, r40, r60, r100, r200**) from
  the cumulative additive scale implied by all `BUILD` events up to that round
  (gunner/sentinel/builder +20, harvester +5, launcher +10,
  conveyor/splitter/barrier +1 — `CLAUDE.md`'s engine-confirmed table), per arm.
  **Pre-registered expectation, and it is a HAZARD read so the direction that
  worries us is the one predicted: the realised reserve is ABOVE ~81 Ti (dose 5)
  by r100 and approaches ~121 Ti (the DISQUALIFIED dose 3) in the long tail.**
  ⚠ **NOT MEASURABLE: the engine's own `get_scale_percent()` value.** The decoded
  stream carries BUILD events, not the scale counter, so (d) is a
  **RECONSTRUCTION** from the engine-confirmed table (`bots/_probe_scale`, s26:
  observed == `floor(scale × base)` for all 8 entity types in every round) —
  labelled as one, and it is the closest executable form of the hazard's metric.
  **It is also the wiring check: a reserve identical between arms means the
  clause never fired, which the silent `except Exception: pass` at `main.py:413`
  makes possible.**
* **(e) THE MAGAZINE COST — mean ammunition held and DRY-TURRET ROUNDS.** Dry
  round = a round in which a friendly turret was live and the team's ammunition
  held less than one shot for it. **Pre-registered expectation: ammunition held
  DOWN and dry rounds UP for the treatment** — this is the cost the sweep
  measured as replicating in BOTH noise regimes and is the half of the trade this
  arm must be shown to have paid. Anchors: sweep control 30.9 ammo / 26.2 dry;
  d5 17.7 / 82.1; d3 10.2 / 181.4; the stack on this chassis **6.3 → ~95/game
  dry**. ⚠ **`get_cpu_time_elapsed()` and `execTimeUs` are absent from 100% of
  LOCAL replays, so nothing in (e) may be reported as a CPU or TLE figure** —
  that is the s42 blind-zero and it is named here so an absence is not read as a
  clean zero.

⭐ **REGISTERED-SIZE SHORTFALL RULE, pre-committed:** if the battery runs short,
the readout states the shortfall factor, and **a `DOSE DELIVERED` verdict whose
|paired diff| clears its own band by less than 2× on a short battery is
UNRESOLVED** — which defaults to the restriction and means the primary is typed
with the mechanism unverified.

### F2 — THE WIRING AND PLACEMENT CHECK. MEASURABLE off F1's retained replays.
Off `scratchpad/bbammo_events.tsv`, per arm:
* **(a) THE PLANT-ROUND HISTOGRAM.** Gunner `BUILD` rounds, both arms. **The
  carrier's own signature must still be present in BOTH arms — earliest
  beltbreak-shaped plant at r10, r10-24 mass ~30% of plants** (carrier measured
  20/61 = 32.8% vs 0/41 for its own parent). ⛔ **THIS ARM DOES NOT TOUCH THE
  TIMING GATE, SO A DIFFERENCE IN THE r10-24 MASS BETWEEN THESE TWO ARMS IS AN
  INSTRUMENT ALARM, NOT A FINDING** — report it and do not read the cell. *(A
  legitimate SECOND-ORDER exception exists and is named so it is not mistaken for
  the alarm: the clause can change WHETHER a plant is funded at a given round,
  so the plant-round DISTRIBUTION may shift while the GATE's r10 edge does not.
  The alarm is the EDGE moving off r10, not the mass redistributing.)*
* **(b) THE ANNULUS HISTOGRAM.** `d2_enemy` mass for gunner builds, both arms.
  **Predominantly in the 20-100 band in BOTH; this arm changes siting NOT AT ALL,
  so a difference is an INSTRUMENT ALARM.** ⚠ **THE EXACT NUMERIC CUT IS
  DELIBERATELY NOT ASSERTED AT LOCK:** `replay_events.py:95-96,113` measures d²
  to a **single core anchor** while the bot's `dsq_core` measures to the
  **nearest tile of the 2×2 footprint**, so a plant the bot scored at d²=20 can
  decode a few units higher. **The band edges are read with an explicit tolerance
  CALIBRATED FROM THE CONTROL ARM'S OWN DISTRIBUTION at readout** — a
  control-derived quantity that cannot be tuned toward a verdict. **The DIRECTION
  is registered; only the cut point is deferred.**
* **(c) HARVESTERS AT r25 / r40 / r60 — the E1-not-lowered check, measured
  rather than argued from `max()`.** **Pre-registered expectation: NOT BELOW the
  flag-off control's.** ⛔ **A FALL is a named negative and is reported as one,
  not folded into the share** — `max()` proves E1's floor cannot be lowered, but
  it does not prove the harvester COUNT is unharmed, since a higher ammo floor
  changes what the bank holds and therefore what else gets bought. Anchor: the
  carrier's read had harvesters *slightly AHEAD* at r25/40/60, so the named eco
  negative did not occur there.

### D3, D4 — the outcome-shape reads. MEASURABLE, shard-native.
`cond` and `turns` are on the tape.
* **D3 — THE r300 ADMISSION BARS (see `KILL-ROUND NON-REGRESSION`).** ITT
  RMST₃₀₀ per side over all 5,400 rows; the ITT timely-kill-by-r300 rate per
  side; the kill-win-conditioned median (the GROSS BACKSTOP, registered
  explicitly because the n=200 read crossed it at 303); and the conditioned share
  as a DIAGNOSTIC. All bars scored as exclusions off `tools/cluster_ci.py --null`.
* **D4 — COND MIX**, the share of games ending `core_destroyed` / `tiebreak` /
  `NOWINNER`, per arm. Carrier anchors: 4,791 / 609 / 0 of 5,400.
  **`R1000_IS_DEFEAT` makes a tiebreak share a cost even when the tiebreak is
  won** — and note the one column that moved FOR this clause at n=200 was
  **r1000 games 26 → 14**, i.e. FEWER tiebreak defeats, which under
  `R1000_IS_DEFEAT` is a real credit and must be reported rather than dropped
  because it is inconvenient for the rest of the picture.

### NOT MEASURABLE on this leg — named, not silently dropped.
* **PLANTS, PLANT ROUND, RESERVE, AMMUNITION, DRY ROUNDS AND SHOTS ARE NOT
  DECODABLE OFF THE SHARD.** `tools/overnight.sh:138-139` runs `--replay
  /dev/null`: **local corefill keeps TAPES, not REPLAYS.** The tape can carry
  share, kill round, `cond` mix and D3's rates, **and nothing else.** ⇒ **every
  mechanism number in this leg comes from the SEPARATE F1/F2 batteries, and the
  shard's n = 5,400 lends them none of its power.** Anyone quoting a plant count
  or an ammunition figure "from the BBAMMO shard" is quoting something that does
  not exist.
* **THE ENGINE'S OWN `get_scale_percent()` AND THE ENGINE'S OWN `ti_floor`.**
  Both are reconstructions (F1(d)); neither is in the event stream.
* **PER-UNIT CPU / TLE.** Local replays carry no exec-time fields at all
  (`execTimeUs`/`tled` absent from 100% of local `BotOutput` events;
  `get_cpu_time_elapsed()` returned 0 on all 22,289 local unit-turns on the
  carrier's battery), so any local number is a **blind zero** and is labelled
  UNINFORMATIVE rather than clean. **The structural argument is what carries:
  this clause adds one integer comparison, one `max()` and one
  `get_gunner_cost()` call, on the CORE's path only, never a raider's — the stack
  measured `--tle 10` reproducing `--tle 0` EXACTLY on all three shipped-shape
  arms.** `--tle 10` caps a timeout engine-side.
* **SEED DETERMINISM AND ANY PAIRED ESTIMATOR.** `NOISE_ON` pins an unseeded
  `random.Random()` spawn salt (`main.py:445`) in both trees, and `fcode run` is
  measured NON-reproducible for this chassis (three runs of antler seed 1 →
  45/106/74 event rows). **No seed-matched or replay-diff equivalence claim is
  available on this fixture; the flag-restore equivalence claim rests on the CODE
  (`cmp` on eco/raid, an 8-line guarded assignment behind one flag) plus the
  16/16 flag-off battery with its non-zero flag-on positive control, never on a
  replay comparison of shard games.**
* **WHAT A PLANTED GUNNER WAS AIMED AT, AND WHETHER ITS ROTATION WAS USED.**
  Facing is not in the decoded event stream. **The throughput half of the
  question this leg's likely null points at is therefore UNOBSERVED here by
  construction** — it is the named NEXT axis, and its registered hazard is
  `GUNPIN`'s rotate-thrash negative (44.27 vs `_v468kladturbo`).

---

## SEEDS

**SEED BASE: 850000.** Registered worklist row (**to be appended by the builder,
not by this agent**):
```
BBAMMO bots/_v504bbammo bots/_v468kladturbo 5400 850000
```
**FREENESS, verified at draft on five surfaces, with a POSITIVE CONTROL RUN
FIRST so the check has been seen to produce the other verdict:**
* **POSITIVE CONTROL: `grep -c '826000' scratchpad/corefill_work.txt` → 1**, the
  `ODINVSSLEIP` row. **The grep HITS when it should hit.**
* `grep -c '850000' scratchpad/corefill_work.txt` → **0**;
  `scratchpad/fleet_queue.tsv` → **0**;
  `grep -l '850000' scratchpad/overnight/*.tsv` → **no file**;
  `grep -ln '850000' docs/prereg/*.md` → **no file**;
  `grep -rl '850000' scratchpad/overnight-remote/` → **no file**.
* **Same-day bases enumerated per file, not assumed:** 812000 `SEALSENTAN`,
  814000 `SEALSENTA`, 816000 `ECOMMIT`, 818000 `FREEROUND`, 820000 `ROUTESCORE`,
  822000 `BELTBREAK-EARLY`, 824000 `BELTBREAK-LATE`, 826000 `ODINVSSLEIP`,
  828000 `KLADLADDER2`, 830000 `KLADLADDER3`, 832000 `SEALPIERCE`, 834000
  `ECOMMIT2`, 836000 `OPENFAST`, 840000 `BELTBREAK2`.
* ⚠ **842000, 844000, 846000 and 848000 are ALSO free at draft (all four checked
  on all five surfaces, all 0), and 850000 was chosen by the brief rather than by
  first-fit.** ⛔ **CONSEQUENCE FOR A SUCCESSOR, recorded so a collision is not
  discovered at fire time: `bots/_v503bbcap3` and `bots/_v502bbstack` are the
  sibling arms from the same commit and NEITHER HAS A REGISTERED SEED BASE
  anywhere in the repo** (`grep -rn 'BBCAP3\|bbcap3' docs/prereg/
  scratchpad/corefill_work.txt` → **no match**). **Whoever registers them must
  re-verify, not assume the gap.**
* **NO OVERLAP, verified by reading the runner rather than assuming it.**
  `tools/overnight.sh:124` is `seed=$(( SEEDLO + n / 16 ))` — **sixteen games per
  seed** — so a 5,400-game shard consumes **338 distinct seeds, not 5,400**.
  BBAMMO at 850000 uses **850000-850337**, against BELTBREAK2's 840000-840337.
  **No overlap, 1,662 seeds of headroom, and the 2,000-wide stride is ~6× larger
  than it needs to be.**
* ⛔ **THE STACK'S AND SWEEP'S BATTERY SEEDS ARE DELIBERATELY EXCLUDED from the
  screen** (the stack's paired battery and its NOISE_ON replication, and
  `_v501ammofloor`'s 2,160-game sweep). They are the fixtures the clause's dose
  was measured on; reusing them would screen the arm on the seeds that selected
  it. **F1's own battery walks seeds 1-2, which the shard never touches.**
* ⚠ **A NAIVE GREP-FOR-COLLISIONS RETURNS FALSE POSITIVES on any prereg that
  verified its own seed freeness** (`PREREG-OPENFAST:314` records a
  freshness-check line quoting 840000 while its registered base is 836000).
  **Named here so no successor re-derives it as a conflict.**

---

## AMENDMENTS

**ADD-ONLY, and blind to the data.** Any amendment to this document is a NEW
dated section appended below this line, never an edit to anything above it; it
must be typed and committed BEFORE the number it could bear on exists, and it
must say what it is blind to. An amendment that removes, weakens or re-words a
registered bar, falsifier, band, segment, MDE or host registration is not an
amendment — it is a new pre-registration and needs a new leg.
*(`tools/prereg_check.py --amendment <locked.md> <amended.md>` is the checkable
form.)*
**Pooling extra rows into this shard after lock is an unregistered n increase —
optional stopping with extra steps — and is prohibited. A replication on fresh
seeds is reported SEPARATELY and NEVER pooled** (the GUNAXABL/SENTTHR precedent:
remote replications corroborated a null they were not allowed to rescue).
⛔ **AND SPECIFICALLY: moving this shard off MacBook-Pro, or amending
`scratchpad/overnight/BELTBREAK2.tsv`, VOIDS THE THIRD FALSIFIER** and must be
typed as an amendment BEFORE the first row, not discovered at readout.

---

## WHAT THIS LEG COSTS AND WHAT IT DOES NOT

**Cost: one LOCAL core to n = 5,400, plus 120 serial games (60 per arm) for F1
and the replay decode for F1/F2.** ZERO rated ladder exposure, zero submissions,
zero unrated challenges — nothing on this page touches the platform, which is
why `TARGET BAND` is N/A rather than a number.

**⚠ AND THE EXPECTED VALUE OF THAT CORE IS DOMINATED BY READ-BEFORE-RATIFYING
#1: without a Magnus grant of `COMBO-BAR-EXEMPT` on THIS arm, the clause-neutral
hypothesis reaches its own registered n with probability 0.024; with the grant,
0.761.** The 2,700-prefix cancellation is not a failure mode of this design — it
is the design working as Magnus specified it — but **it means the core most
likely buys a `cancellation` row and the F1/F2 mechanism reads, not a bar
verdict, unless the exemption question is settled first.** That trade is the
builder's to make and the number is here so it is made with eyes open.

**It does NOT decide a ship.** The strongest branch promotes the arm to (a) a
combination input and (b) a separately-registered head-to-head against the live
holder, which is the pipeline step Magnus's procedure names verbatim (*"we start
by testing it against the current slot, if it beats it we can switch"*). **A
local screen against our own shipped bot is gate 1; gate-1-to-gate-2 transitivity
is UNVALIDATED in this repo (QUEUE #65: 3 concordant, 1 not), so the head-to-head
is not skippable on the strength of this number.** And `SLOT_STOP_LOSS: off` plus
the parked SWITCH step of `X3R0_SLOT_RULE` (which now requires **≥60% game share
with a ≤2pp half-width**, a bar no arm on the board reaches — the ceiling at that
ruling was 55.24%) mean **the slot changes only on Magnus's explicit word,
whatever this leg returns.**

**⚠ ONE KNOWN PREFLIGHT FAIL, NAMED AND NOT FIXED:**
`.venv/bin/python tools/preflight.py bots/_v504bbammo` FAILs on *"no PREREG.md or
README.md in bots/_v504bbammo — write the S0 block before the build, not after
the battery"*. **The carrier `bots/_v488beltbreak2` and its parent
`bots/_v480beltbreak` have neither either** (verified at draft: each directory
holds only `doctrine.py`, `eco.py`, `main.py`, `raid.py` and `__pycache__`), **so
this is not a regression introduced by this arm** — it is a standing property of
every tree in this family. ⚠ **It is worth one line of the builder's attention
anyway, because the SIBLING `bots/_v501ammofloor` DOES carry a `PREREG.md` with
an `S5_unrated: REQUIRED, NOT DONE` line on it** — the S0 discipline exists in
this family and this branch of it skipped the file. Reported; not fixed by this
agent.

---

**PROVENANCE:** `docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md` (read IN FULL: OB7 — invoked directly and answered SPLIT in `PRE-STATE`; OB8, OB10, OB11, OB12 + its pre-committed restriction default; OB13; OB14; OB15a/b/c + the segment vocabulary and the units rider; OB16 + its `BAR = null + MDE + half_width` amendment, its zero-MDE corollary for the standard corefill band, and its 2026-08-15 CROSS-HOST rider, which is why this page registers SAME-HOST as a load-bearing token rather than a note; OB17 + its "run the clause that can surprise you" rider, which is what produced the `tools/dose.py --tle` finding in READ-BEFORE-RATIFYING #7; and the **2026-08-17T07:24:55Z addendum** that replaced the local-shard clock-2 boilerplate — quoted rather than restated) · `PROGRAMME.md` (parsed block `:6-30` — `INCUMBENT: bots/_v468kladturbo`, `PRIMARY_CURRENCY: game_share`, `WIN_RATE_IS_VERDICT: yes`, `KILL_WINDOW_RND: 250`, `R1000_IS_DEFEAT: yes`, `PLAY_DEFENCE: not_at_the_kill_s_expense`, `DEFENCE_ADMISSION_BAR: r300_crossing_non_regression`, `SLOT_STOP_LOSS: off`, `X3R0_SLOT_RULE`; the `:31-49` stop-loss retirement; the `:63-94` X3R0 re-pricing to 60±2 and its three-step pipeline; the `:488-564` r300 re-pricing chain in full — the 05:15:45Z re-pricing, the 05:19:38Z collider correction, the 05:3xZ arbitration freeze, and the **05:36:10Z ITT RMST₃₀₀ resolution with its vintage rule**, which is why this page registers RMST₃₀₀ as the operational estimator alongside the ITT timely-kill rate and the median backstop) · `docs/prereg/PREREG-BELTBREAK2-2026-08-17.md` (**the CARRIER's prereg, read IN FULL** — its match structure, token order, registered machinery and caveat set are inherited here where they still apply; its dose table, its CQ-complement segment and its `#1` cancellation-probability section are the templates this page's `#1`, `#2` and `SEGMENT` sections extend and, where the mechanism differs, contradict) · `results.tsv` row **`beltbreak2-final`** (read in full: the Band-1 verdict 53.09 [51.76,54.42] n=5400, timely-kill 30.80 vs 24.35, the three inexpressible-map cells, the F2 gate signature, and the **two instrument facts — `dose.py` passing no `--tle` against `fcode run`'s `--tle 0` default, and `fcode run` being non-seed-reproducible for this chassis at 45/106/74 event rows**) · `docs/coordination.md` (the **AMMOFLOOR SWEEP** entry at `~12:2xZ`, `:70766-70775`, read in full: the unarmed-branch inertness, the cost-curve-replicates/gain-curve-does-not split, dose 3's −27.5pp disqualification, the turrets-2..n-vs-first-turret causal split, the *"kill constraint is turret THROUGHPUT, not COUNT"* verdict, the re-brief of LEG 3 at the shredder's price with **the plants-up-shots-flat crossing named as mandatory**, and the sweep-hygiene log; plus `:70754-70756` the nesting hypothesis this arm's evidence now contradicts) · `bots/_v501ammofloor/PREREG.md` (the solo sweep arm's own S0 page, read in full — its `S5_unrated: REQUIRED, NOT DONE` line and its treatment-occurrence figures) · `bots/_v501ammofloor/doctrine.py:1880-2042` (the `LOKI-AMMOFLOOR` block and THE SWEEP block in full: the 29.7%/36.2% ammo-claimant finding, the `ti_floor = 12 … else 52` mechanism read, the dose ladder and its **pricing discipline**, the reserve/ammo/dry-round/median/kill-by-r300 table at ~54/~81/~121 Ti, the non-replicating gain, the dose-3 disqualification, the first-turret regime inversion, the `max()` composition rule, and the fixture's own stated lie) and `bots/_v501ammofloor/main.py:355-374` (the ported clause, dose 4 == bare `get_gunner_cost()` on both branches — which is what establishes that this arm is dose 6, not dose 4) · `bots/_v502bbstack/doctrine.py:1689-1940` (**the stack's LEG-3 block, read in full at source after the builder lane relayed it**: the dose-6 definition and the deliberate exclusion of `LOKI_BELTBREAK_AMMO_EFF`, the crossing rule verbatim, the 10-arm NOISE_OFF ablation table, the sub-additivity finding, the LEG1×LEG3 collapse and the 6.3→~95-101 dry-magazine figures, the funnel's still-`TI` verdict and its refusal-counter anti-inference, the verification log incl. the 16/16 flag-off with 16/16 positive control and LEG 0's 50/50-twice neutrality with its must-differ normaliser control, and **the NOISE_ON n=200 replication with plants +0.450 CI [+0.134,+0.766] against wins 112→102, ITT300 28.0→22.5, median kill 259→303**) and `bots/_v502bbstack/doctrine.py:1936-1940` (the `BBSTACK_L3_AMMOFLOOR = False` default and its reasoning) · `docs/prereg/BARS.tsv` (**header/format ONLY, incl. the FIRINGS-BEFORE-PRIMARY rule of 2026-08-16T13:27:33Z, the column spec and the `le`-direction never-stop carve-out; plus rows `:310` `BELTBREAK-EARLY` and `:312` `BELTBREAK2` read VERBATIM for the COMBO-BAR-EXEMPT precedent and its ratio decidendi — `grep -c COMBO-BAR-EXEMPT` → 2. NO ROW WAS ADDED BY THIS AGENT**) · `CLAUDE.md` (the ONE GLOBAL ADDITIVE cost-scale factor and its `bots/_probe_scale` s26 confirmation — load-bearing for F1(d) and for the reserve's growth; the DEFF scope procedure, its direction clause and the local 0.98 exemption; the `print()`-stripped-from-platform-replays ruling; `R1000_IS_DEFEAT`; the r300 bar's operational form; the ammunition/convert_ammo rules and the 4-vs-10 ammo-per-shot table the pro case rests on) · `bots/_v504bbammo/{doctrine,eco,main,raid}.py` (read at draft: `doctrine.py:1434-1460` the new comment block and the flag, `main.py:300-427` the whole core ammunition block incl. the T4 brake, the endgame dump, the two-branch `ti_floor`, E1 and the clause, `raid.py:896-915` the plant path's actual funding gate) · `bots/_v488beltbreak2/{doctrine,eco,main,raid}.py` (the CARRIER, `cmp`'d file-by-file: `eco.py` and `raid.py` byte-identical, `doctrine.py` +5/−0, `main.py` +20/−0) · `bots/_v468kladturbo/doctrine.py:1879` (the `stack.py` compose marker every arm on this chassis inherits — the whole basis of `#1`) · `scratchpad/overnight/BELTBREAK2.tsv` (**the carrier's tape, n=5,400 non-`#` rows, recomputed at draft rather than cited: pooled share 53.0926%, the per-map cells, ITT RMST₃₀₀ 268.21/275.52 with paired sd 85.02 and per-side sd 55.66, ITT timely-kill 30.80/24.35 with paired sd 73.99, the `cond` mix 4791/609/0, the kill-win median 244, the EXPRESSIBLE-12 cell 53.89 [52.40,55.38], and the `# FIXTURE … host=MacBook-Pro start=2026-08-17T09:13:33Z` header that the THIRD FALSIFIER's same-host requirement is derived from**) · `tools/prereg_check.py` (read for `KNOWN_KEYS`, `key_pattern`, `RULES` in full, `check_presence`, `check_arithmetic` incl. `BOUNDARY_UNITS`'s local exemption, `CUT_SHORT_FLOOR`, `BAR_RESOLVABLE`, `REFERENCE_FLOOR`, `SEGMENT_CEILING`, `DOSE_BOTH_VERDICTS` and the OB13 branch, `git_diff_paths`, `untracked_arm_paths`, `_DEFENSIVE`/`_defence_bar_ok`, and `DEFF`/`CLUSTER_SYNONYM`) · `tools/auto_gate.py` (`:236-247` the marks and `CATASTROPHE_CI_HI`, `:249-261` `TREND_FLOOR = 52.0` with its Magnus provenance, `:263-278` `COMBO_BAR = 55.0` with its pre-adoption pricing table, `:280-290` the confirmation-class exemption, `:715` `combo_of` and its read of the TREATMENT tree's `doctrine.py`, `:902-960` the COMBO-BAR clause and the exemption's citation guard, `:962-1000` the `FUTILITY-BAR` CI rule and its `0.5 × half-half-width` margin — all four clauses simulated at draft to produce `#1`'s probability table) · `tools/overnight.sh` (`:57-68` the live 15-map pool, `:99-103` the `START=`/`# FIXTURE` stamp, `:118-124` the resume arithmetic and the `SEEDLO + n/16` seed walk, `:131-139` the `--tle 10` mandate and `--replay /dev/null`) · `tools/overnight_read.py` (`:76-94` `map_area_class`, run at draft to classify all 15 live maps) · `tools/dose.py` (read in full for OB17: `:77` the retired default `MAPS`, `:134-172` the argparse with NO `--tle`, `:175-200` the CLASS B no-default gate, `:212-231` the seed/map/seat walk and the `subprocess.run` command line that omits `--tle`, `:250-262` the `--keep` retain-and-name path) · `.venv/lib/python3.13/site-packages/fcode/commands/run.py:119` (`--tle` default 0, *"0 to disable, server uses 10"* — the other half of the OB17 finding) · `tools/corpus/replay_events.py` (`:16,113` the rotation guard, `:95-96` the single-anchor core convention, `:157` the output columns) · `tools/cluster_ci.py` (`--help` read; `--null` is the exclusion-restatement path the r300 and clause bars use) · `tools/preflight.py` (run at draft against `bots/_v504bbammo`; the named FAIL) · `tools/control_pin.py` / `scratchpad/CONTROL_PIN` (the control's identity) · `scratchpad/corefill_work.txt` (the row format and the full 812000-840000 seed sequence, tail read at draft) · `scratchpad/fleet_queue.tsv` and `scratchpad/overnight-remote/` (seed freeness surfaces) · `results.tsv` rows `idnull140-cert-5400`, `null125-final`, `kladladder-n-final-correction`, `kladladder-verdict-amendment-f1f2-pending` · git `e728c6f8` (HEAD at draft), `54129ed7` (the commit that added the arm tree, with its message read in full for the equivalence figures), `git status --porcelain`, `git ls-files`, `git log --diff-filter=A` and `git diff --name-only 54129ed7^ 54129ed7 -- bots/_v504bbammo` output quoted above · the drafting brief supplied by the builder lane s49 and its mid-task course correction relaying the `_v502bbstack` LEG-3 evidence. **No file under `bots/`, `tools/`, `scratchpad/`, `docs/prereg/BARS.tsv`, `results.tsv`, `HANDOVER.md`, `PROGRAMME.md`, `QUEUE.md` or `docs/coordination.md` was created or modified by this agent, no tool was fixed, and no game was run. The only write was this document.**
