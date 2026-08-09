# The heal channel is already run near-optimally. The constraint is BODIES. "Fortify on idle" is refuted.

**Research arm, session 24, 2026-08-09.** The two gates on the heal-channel build —
gate 1 mine, **gate 2 the builder arm's, and gate 2 is the one that killed it.**

**This supersedes `heal-ceiling-s1-2026-08-09.md`, which is my own document from two
hours earlier. Its recommendation is dead and two of its headline rates were wrong.**

**Version tag:** live **v92** = `bots/_v115dodge`, submission `7b1d8d73`.
**Inputs frozen before the run** — `corpus/join.tsv` md5 `f3bc78bc58cc7682cf734c202620fe65`,
1,355 rows; `manifest.json` git sha `56eceae`, 5,401 archived replays. The keeper
daemon's later appends cannot affect anything here. **Zero replay downloads.**
Decoder: `docs/research/scripts/seat-census-2026-08-09/seat_decode.py`, derived from the
preserved `bb_decode.py` — **85 CAD files → 43,684 round rows in 2.0 s; 1,355 files →
682,011 round rows in 27 s; 0 errors both runs.**

---

## 0. The window was assumed, and the assumption was wrong

`heal-ceiling-s1` took the CAD read's *median first gunner planted r172* and *median core
death r361* and treated the difference as a 189-round damage window. **Two medians from
different distributions are not a window.**

**Measured per game — first round an enemy turret shot lands on our footprint → core
death or game end — CAD loss windows run median r12 → r335, length ~300 rounds.** The
early start is real and was traced event-by-event in 4 games: **CAD's opening is a
launcher-thrown builder that plants a core-shooting gunner by r3.**

| quantity | published in `heal-ceiling-s1` | measured |
| --- | ---: | ---: |
| healers per round over the window | 2.1 | **1.10** |
| incoming HP per round over the window | 11.20 | **5.67** |
| heal ÷ damage (the CAD doc's headline) | 0.76 | **0.753** ✓ |

**The totals agree; only the denominator was wrong.** That is the whole error, and it
moved both rates in the same direction.

## 1. GATE 1 — staffing is bimodal, the mode is ZERO, and the bot is doing it right

**CAD loss games, 19,393 siege-rounds over 54 games. Healers per round:**

| 0 | 1 | 2 | 3 | 4–5 | 6–8 | mean | median | max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **56.7%** | 7.9% | 18.3% | 7.4% | 9.1% | 0.7% | **1.10** | **0** | 7 |

**Not flat ~2. Zero on 57% of rounds, ~2.5 when it fires.** And the switch is not the
phase of the siege (quintile means ramp only 0.98 → 1.86) — **it is whether the core took
damage that round:**

* no-damage rounds (n=12,388): **0.45 healers**
* damage rounds (n=7,005): **2.24 healers**; builders standing on a heal-capable tile 2.65
* **terminal 25 rounds before core death** (n=1,350): healers **1.99**, staffed 2.22

**Read plainly: our bot heals REACTIVELY, and it does it well.** That is the opposite of
the "we simply do not staff it" story I published. The 82%-headroom framing was an
artefact of averaging a reactive behaviour over rounds where there was nothing to react
to.

The incoming side scales the same way: **5.67 HP/rd over the window, 15.70 on damage
rounds, 18.79 in the terminal 25.**

## 2. GATE 2 — the idle supply does not exist. **This is the builder arm's gate and it is decisive.**

The recommendation was *"staff the heal channel from IDLE builder-turns only"*. The
builder arm pointed out — correctly, and before I did — that its entire load rests on an
unmeasured premise, and sharpened the quantity: **not idle turns, but idle turns within
one step of a free core-adjacent seat**, because a builder walking is a builder not
acting and the walk is itself scheduled turns.

**CAD loss games, per siege-round:**

| tier | mean per round | **share of rounds = 0** |
| --- | ---: | ---: |
| any idle builder anywhere on the map | 0.65 | 62.5% |
| **(a) idle AND on a heal-capable tile** | **0.15** | **92.1%** |
| (b) idle AND one cardinal step from a free heal tile | 0.06 | 94.4% |
| (c) idle AND two–three steps away | 0.04 | 96.2% |

(a)=0 in **92.1%** of siege-rounds; (a)=(b)=0 in 88.4%; (a)=(b)=(c)=0 in 85.4%. On rounds
the core took damage, (a)=0 in **91.7%**. **In the terminal 25 rounds — where the core
actually dies — (a)=0 in 95.7%**, mean 0.08.

**Priced against the thing it was supposed to fix:** the terminal-25 deficit is
**10.83 HP/round** (18.79 in, 7.96 healed). **Tier (a) supplies 0.32 HP/round — 3.0% of
it.** Over the whole window it is 0.60 against a 1.40 deficit (43%) — **but the average is
the wrong statistic, because the core dies to the terminal burst, and there the supply is
3%.**

**Idle turns do exist — 12,653 of 99,054 builder-turns in the window (12.8%). They are
simply nowhere near the core:** 23% of idle builder-turns are on a seat, 38% within three
steps, **62% are more than three steps away.** Meanwhile **9.48 of 12 heal-capable tiles
sit free every round.** Supply, not geometry, and not titanium.

**Generalises.** All 1,355 attributed games / 511 loss games / 126,059 siege-rounds:
(a)=0 in **91.4%** of loss siege-rounds; terminal-25 (a)=0 in **94.9%**; headroom **3.3%**
of a 10.13 HP/rd deficit.

## 3. The seat-turn ledger — there is no scheduling slack to harvest

Of **30,109 builder-turns spent standing on a heal-capable tile** in CAD loss windows:

| what the seat-stander did | share |
| --- | ---: |
| **healed the core** | **70.5%** |
| walked away | 17.2% |
| something else | 2.6% |
| idled | 9.7% |

**In the terminal 25 rounds, 1.99 of 2.22 seat-standers heal — 90%.**

The one non-empty adjacent reservoir, **stated as a lead and not a recommendation**: the
**17.2% who walked away** (5,183 turns) could be converted for the price of a move rather
than a scheduled builder — but in the terminal 25 that is **0.09/round = 0.37 HP/rd, 3.4%
of the deficit.** Same size as the idle channel. **Both are rounding errors against a
10.8 HP/rd terminal deficit.**

## 4. THE REAL CONSTRAINT IS BODIES — and it is the third answer in one day

I said the constraint was titanium (wrong), then builder-turns (closer, still wrong).
**It is bodies.**

* **Terminal-phase living builders average 4.19** (CAD) / **4.06** (league-wide).
* **≥6 staffed seats occurs in 2.0% of loss siege-rounds. The observed maximum ever is 7.**
* **The 12-seat / 48 HP-per-round ceiling is unreachable not because we decline to staff
  it but because we do not have 12 builders alive when the siege peaks.**

**Any real heal response has to name where the bodies come from — and that is exactly the
ESCALATE cost already refuted at −7.8pp.** The channel is not underused; it is
oversubscribed relative to the population that could fill it.

## 5. VERDICT

**"Staff the heal channel from idle builder-turns only" does not survive. Do not build
it.** Its premise is false in the games it targets, and the seat ledger shows the channel
is already run at ~90% efficiency where it matters.

**This cost one decoder pass instead of one battery**, which was the entire point of
gating it.

## 6. Confounds ruled out — not assumed away

* **Cooldown is not a confound, and it is proven rather than argued.**
  `setActionCooldown` / `setMoveCooldown` were reconstructed: **every builder cooldown set
  in every one of the 1,355 games is `1`**, so a builder that acted in round *r* is free
  in *r+1*. Newly spawned builders carry 0. **"Idle because on cooldown" is impossible
  across rounds.**
* **TLE is not a confound: 0 TLE builder-turns in the entire CAD set** (67 league-wide
  across 1,355 games, exactly 1 on an idle turn). **Crash is not either: 0 `Traceback`
  outputs.** `botOutput` is emitted for 99.86% of builder-rounds, so essentially every
  living builder demonstrably ran.
* **The s23 co-occupation prior is NOT load-bearing for any figure here** — and that
  matters, because the lane call authorising those probes is still open. **Standing on the
  core footprint essentially never happens**: maximum 1 on-footprint builder, in 4 of 85
  CAD games. Ring-only seats give numerically identical staffing. **Two builders never
  share a tile in any of the 1,355 games.**
* **The corpus `d2` NW-corner contamination does not touch this** — seats are expanded
  from all four footprint tiles directly out of `map.cores`; no corpus distance column is
  used.

## 7. Limits and approximations

* **I cannot separate "policy chose nothing" from "policy tried something and the
  `can_*()` guard returned False".** Both are policy failures, so the direction is
  unaffected.
* **Positions are start-of-round snapshots**, and the engine resolves units sequentially
  within a round, so a tile free at round start can be taken mid-round. **This INFLATES
  the supply estimate — the true numbers are ≤ what is reported.**
* **Newborn builders are excluded from idle** (316 turns, ~2.5% of idle turns) —
  conservative, understates supply slightly. Core-spawned builders land *on* seat tiles by
  construction.
* **`destroy()` emits no Update message** and cannot be attributed to a builder. Upper
  bound on contamination: **8 of 12,653 idle turns (0.06%).**
* Invariant `healers ≤ seats_at_start(+born)`: **43,684/43,684 clean on CAD,
  682,005/682,011 league-wide** — 6 violations at 0.0009%, likely launcher-thrown-then-healed.
* Heal validation against the independent HP stream: `heal_HP / (4 × heal_events)` median
  **0.9750** (CAD) / 0.9783 (all), consistent with `bb_decode`'s validated 0.9941; the
  shortfall is heals capped at max HP. **Non-enemy shots on our footprint: 0** — no
  contamination of the window trigger.
* **Population caveat (corpus trap 4):** the archive is dominated by our own games. Every
  figure is "vs CAD in 85 archived matches" or "in our 1,355 attributed games".
* The CAD population here is **85 replays / 54 losses / 18 tiebreaks / 10 wins**, against
  the CAD doc's 75 — the archive grew. 3 further games excluded because our core never
  took a turret shot at all.

## Provenance

Scripts committed at `docs/research/scripts/seat-census-2026-08-09/` — `seat_decode.py`
(md5 `32b43033`), `analyse.py` (`47202e0b`), `terminal.py` (`b5cc4788`). The preserved
side-lane decoders are untouched. **The error chain in §0 is mine and is recorded in
`heal-ceiling-s1-2026-08-09.md` in place rather than deleted.**
