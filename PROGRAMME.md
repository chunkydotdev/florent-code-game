# ACTIVE PROGRAMME — machine-readable. `tools/gate.py` reads this and refuses off-programme batteries.

Edit this file ONLY on an explicit directive from Magnus. Both arms and every
successor session inherit it. The fields below are parsed; the prose is not.

    LINE: loki
    LINE_DIRS: bots/_v105loki1 bots/_v10?loki* bots/_v1??loki*
    INCUMBENT: bots/_v115dodge
    INCUMBENT_FROZEN: yes
    PRIMARY_CURRENCY: game_share
    SECONDARY_CURRENCY: kill_speed_score
    KILL_SPEED_SHIP_GATE: -1.76
    KILL_SPEED_MIN_N: 200
    KILL_SPEED_IS_LEG_VERDICT: no
    WIN_RATE_IS_VERDICT: yes
    COMPARE_AGAINST: previous_line_iteration
    KILL_WINDOW_RND: 250
    R1000_IS_DEFEAT: yes
    PLAY_DEFENCE: not_at_the_kill_s_expense
    DEFENCE_ADMISSION_BAR: kill_round_non_regression
    FIXTURE_OF_RECORD: live_unrated
    ALWAYS_BE_RUNNING: yes

## ⭐⭐⭐ CORE VALUE, MAGNUS, 2026-08-11 (s31) — **ALWAYS BE RUNNING.**

**Written into this file on his direct instruction — *"put this in your
programme, it's a core value for you"* — after he had to ask THREE TIMES in ten
minutes whether anything was running locally.** The exchange, verbatim:

> *"anything running locally?"*
> *"do we not monitor the local runs? if nothing is running we're losing time we
> could use to figure out the next Loki version"*
> *"If we are not running locally we should grab items from the queue and run
> them, the researcher has a monitor that makes them put more items in the queue
> if it is running out."*

**THE RULE: IDLE CORES ARE A DEFECT. If nothing is running locally, the builder
takes the top unblocked item from `QUEUE.md` and runs it — without being asked,
without waiting for analysis, and without a window.**

**WHY IT IS A VALUE AND NOT A PREFERENCE, in this project's own numbers:**
* Local games are **free, unlimited and instant**. The rate limit (5 unrated per
  20 min) governs the PLATFORM only. **Nothing rations local cores but attention.**
* **~420 rated matches remain in the whole game** (~84/day). **A ship converges
  in the BACKGROUND while we work**, so an unshipped plank is a certain zero and
  an idle hour is unrecoverable.
* Measured on this machine 2026-08-11 13:53Z: **load average drained 14.67 -> 1.57
  with ZERO `fcode run` processes and a fully stocked queue sitting unread.**
  Ten cores idle while three planks waited.

**⛔ AND THE STRUCTURAL REASON NOBODY NOTICED — this is s30's D66 recurring:**
that session ran screens on **1 core of 10** for ninety minutes. The lesson was
recorded as *"subagents are for judgment, cores are for games"* and it **did not
prevent the same failure one session later**, because it was written as a lesson
rather than built as an instrument.

⇒ **`tools/monitors/cores_idle.py` (s31) IS THE INSTRUMENT.** It polls every
300 s, and on two consecutive polls with zero local games it prints
`*** CORES IDLE — NEXT QUEUE ITEM: <plank> ***` and writes
`corpus/CORES_IDLE_ALERT`. **The alarm carries its own remedy: it names the plank
to start.** It gates on the process count (never `$?`), reports the queue file's
AGE, and returns **BLIND rather than "idle"** if `ps` fails — because an alarm
that cannot tell it is blind is this repo's most-repeated defect.

**THE DIVISION OF LABOUR MAGNUS SET, and both halves are now instrumented:**
**RESEARCH keeps `QUEUE.md` stocked** (their monitor fires when it runs low);
**BUILDER keeps the CORES BUSY** (this monitor fires when they go quiet).
**An empty queue is a research failure; idle cores are a builder failure.**

## ⭐⭐ DIRECTIVE, MAGNUS, 2026-08-11 — **"WIN RATE DECIDES."** GIVEN DIRECTLY TO THE BUILDER, NOT RELAYED.

Preceded in the same session by *"The goal for any of this is to climb ELO"* and
*"Any improvement no matter how small should be considered as the replacement of
v104."* **`WIN_RATE_IS_VERDICT` flips `no` -> `yes` and `PRIMARY_CURRENCY`
becomes `game_share`.**

**AND IT IS NOT A COMPROMISE WITH RIGOUR — IT IS THE OBJECTIVE FUNCTION.** The
ladder pays `delta = 32 x (S - E)` where **S = games won / 5**. Game share IS
what the ladder pays, verified to a max residual of 0.000000 across 100 matches.
`kill_speed_score` was always a PROXY, adopted because `R1000_IS_DEFEAT` made a
tiebreak win worthless *to us*; **the ladder never agreed and pays for it
anyway.** Optimising the proxy while the goal is Elo is the mistake, not the fix.

**⛔ ONE CONSEQUENCE THE BUILDER FLAGGED BACK RATHER THAN APPLYING SILENTLY, AND
IT IS THE ONLY PLACE THIS DIRECTIVE COLLIDES WITH ANOTHER:** under
`PRIMARY_CURRENCY: game_share` **a round-1000 tiebreak win is a WIN**, because the
ladder pays it. `R1000_IS_DEFEAT: yes` (below) says it is a defeat, and the
`-10` in `tools/score.py` exists precisely to make tiebreak-turtling score zero.
**Those two cannot both drive a ship decision.** Until Magnus rules:
* **`game_share` decides the SHIP** (this directive, and it is what Elo pays);
* **`R1000_IS_DEFEAT` still governs what we BUILD** — no plank may be *designed*
  to farm tiebreaks, because that is the doctrine and it was set on 2026-08-10;
* **`tools/score.py` and every baseline in it are UNCHANGED**, so v20 -10.00
  through v104 -1.76 stay mutually comparable. Changing the scale in place
  orphaned every earlier figure once already, within the hour.

## What this means, in the words of the directive (Magnus, 2026-08-09)

> *"Loki should be our main focus now, leave Eir behind to hold the lines while
> we build something that has a shot at actually ranking high."*
> *"Eir is what, iteration 50+, Loki v1 was never supposed to be shippable...
> we need a lot of iterations to make Loki stand a chance."*
> *"Although Loki is supposed to be an entirely separate bot from Eir."*
> *"We need to find good tricks we can use, poisonings, exploits, manipulations,
> anything that seems to have a shot at killing teams in the first 250 rounds,
> and lean into that hard once we find it."*

**INCUMBENT_FROZEN** — `bots/_v115dodge` (v92) holds the ladder slot and receives
no further planks. It defends the rating; it is not the work.

**LINE: loki** — Loki is a SEPARATE BOT, not a flag on the Eir chassis. Iterations
edit Loki's own tree. Porting Loki features onto Eir is the line-mixing this
directive forbids; `bots/_v116thor` is the last instance and is retired.

**COMPARE_AGAINST: previous_line_iteration** — LOKI-N is measured against
LOKI-(N-1), never against Eir. "Does it beat the incumbent" is the wrong
instrument for a line under development and is what buried LOKI-1 in s22: a v1
was judged against a v46+ line, on a self-play pool, and the road was closed on
the result.

**WIN_RATE_IS_VERDICT: no** — the probe pool is dominated (both arms win 87-90%),
so a win-rate ceiling that high cannot show an edge. Read
**core-kill share** and **time-to-core-kill**. Measured 2026-08-09: LOKI-1 vs v92
was a win-rate NULL (+3.1pp, p=0.22) and a core-kill landslide (91% vs 61% share,
paired sign test p=5.2e-09).

**KILL_WINDOW_RND: 250** — the target is a dead enemy core inside 250 rounds.
Our own tape: before r200 we go 277-148 (65.2%); after r200, 164-363 (31.1%).

## DIRECTIVE, Magnus, 2026-08-10 06:0x CEST — read this as the definition of the line

> *"Loki is the ultimate trickster, playing into other teams by using cheap
> tricks, manipulation, poisoning and every exploit we can find. Loki plays
> dirty and is the ultimate weapon at that. We want to destroy the enemy core,
> never play defence. A r1000 round is a defeat even if we by chance win it.
> You need to constantly figure out and test new tricks that we can use by
> building prototypes and putting them against live teams in unrated games —
> that beats our own calculations every time, and sometimes you find things
> that surprise you. Those are of fantastic importance for our growth."*

Three fields above are new and each one closes a road that was open yesterday.

**R1000_IS_DEFEAT: yes.** A tiebreak win is a LOSS in this programme's ledger.
This retires the whole tiebreak-turtle family and demotes every economic plank
whose only channel is `titanium_collected` — that currency is only ever paid out
in games we have already lost by this definition. Economy is now purely
INSTRUMENTAL: it buys the kill, it never scores.

**PLAY_DEFENCE: not_at_the_kill_s_expense.** ⭐ **AMENDED 2026-08-11 (s31) ON
MAGNUS'S DIRECT INSTRUCTION TO THE BUILDER — "update the programme".** The
directive, relayed to the side lane and confirmed to me directly:

> *"This does sound like we should allow SOME defence strategies, but our FOCUS
> should be to kill at <r250."*

**THE FIELD WAS `never`. IT IS NOW A BAR, NOT A BAN — and the bar exists because
"SOME defence" is a GRADIENT and a gradient is unenforceable unless the test is
written down.** `never` was a bright line, enforceable at zero judgement cost;
replacing it with a preference would have made every survival plank arguable.
So it is replaced with a MEASURABLE ADMISSION TEST, declared in the parsed block
at the top of this file as `DEFENCE_ADMISSION_BAR: kill_round_non_regression`.
**(Written inline as prose, NOT indented four spaces: an indented copy is read by
`gate.py` as a SECOND field declaration and, because it builds a dict, the LAST
occurrence WINS — so a prose illustration would silently override the canonical
block with no error and no diff. That is exactly what this section did for its
first eleven minutes; caught by the side lane.)**

⇒ **A defensive plank is ADMISSIBLE if and only if it does not slow the kill.**
Any survival-mechanism plank carries a **kill-round non-regression bar beside its
survival bar. If median kill round RISES, the plank is off-programme, whatever it
does to win rate.** (Operational form proposed by the side lane; adopted here
because it converts the directive into something `gate.py` can eventually read.)

**⛔ THE SCOPE, AND IT IS WHAT KEEPS `R1000_IS_DEFEAT` UNCHANGED.** "SOME defence"
means **surviving the r150-250 window so OUR OWN KILL LANDS.** It does NOT mean
surviving to r1000. Measured, 1800-1900 band cut (side lane, `9209e3e`):
**our median kill round is 174 and our median death is 187 — a thirteen-round
race**, and **our core dies in 46.3% of all v104 games** with 98.3% of our losses
by core destruction against the band's 89.7%. Defence aimed at that thirteen-round
gap is the good road. **Defence aimed at reaching a tiebreak is still the retired
one** — the tiebreak tail is a coin flip (1800-1900 wins 49.4% of tiebreaks vs
45.2% overall), so there is no salvage there, and `R1000_IS_DEFEAT: yes` stands
untouched.

**⭐ AND THE CHEAP CLASS IS ALREADY IDENTIFIED, MEASURED RATHER THAN ASSUMED:
SEPARATE DEFENCE THAT SPENDS THE KILL BUDGET FROM DEFENCE THAT SPENDS IDLE
RESOURCES.** When our core dies, **~5 of our builders are ALIVE** (median 5.0,
mean 4.43 vs 5.20 in wins) with **0.38 builder deaths across the whole 40 rounds
before the core falls** — they are not even in combat. Home turrets and barriers
COMPETE with the assault and must clear the bar the hard way; **re-tasking
builders who are already alive and already idle costs the kill nothing and cannot
violate the non-regression bar by construction.** That is where the first
defensive plank belongs.

**WHAT THIS DOES NOT REVIVE.** `never` killed queue items at the s26 wrap; this
amendment does not restore them wholesale. Each must now clear the
non-regression bar on its own, and heal-idle staffing / home turrets / screening
re-enter as CANDIDATES, not as confirmed planks. Note that s30 measured
`home-turrets-off` at 433/1024 and `barrier-seal-off` at 399/1024 — both REAL
NEGATIVES, i.e. **removing that defensive behaviour cost us**, which is evidence
the amended field was already the truer description of the bot we ship.

**FIXTURE_OF_RECORD: live_unrated.** `bots/*_probe` is a fixture WE WROTE, and
s26 D21 proved it lies in a specific direction: five of our probes share a
`best_core or best_any` short-circuit, so every verdict we ever resolved faced an
opponent that prefers our core over anything else — which is why zero of our
forward turrets died in 480 arena games while **46.9% die on the ladder**.
Magnus's *"beats our own calculations every time"* is therefore not a preference,
it is the already-measured fact. **`fcode match unrated <team_id>` is the
instrument** — 5 games against a real team's real bot, no rating at stake.

**THE CONSTRAINT THAT COMES WITH IT, and it is real:** `fcode match unrated`
plays **our ACTIVE submission**. There is no flag to point it at a local tree.
So testing a prototype against live teams means ACTIVATING the prototype, and
the ladder keeps pairing us (~6 rated matches/hour) for as long as it is up.
**A trick leg therefore costs rated exposure, roughly 2-3 ladder matches per
20-30 minute window, bounded and recoverable by re-activating the incumbent.**
That is the price of the only honest fixture we have. Pay it deliberately:
prototype activated -> burst of unrated challenges -> incumbent re-activated,
with the window and the rated matches inside it recorded.

## KILL-SPEED SCORE — the currency, commissioned by Magnus 2026-08-10

**Magnus commissioned it and confirmed the `PROGRAMME.md` edit directly** (asked
in-session, answered *"Yes i did"*). Spec:
`docs/research/SPEC-kill-speed-score-2026-08-10.md`; implementation
`tools/score.py`, wired into `leg_read.py`.

    core kill <100 -> 10 · <130 -> 8 · <170 -> 6 · <250 -> 4 · <400 -> 2
    slower kill -> 1 · tiebreak/titanium win -> -10 · LOSS (any cause) -> -10
    reported as MEAN POINTS PER GAME

**It SUBSUMES the two fields it replaces.** `core_kill_share` is retained as
SECONDARY because it is the cheaper diagnostic, but the score already contains
it: a kill scores 1-10 and a tiebreak win scores -10, so kill share and
time-to-kill are both inside one number. **`R1000_IS_DEFEAT` is now arithmetic
rather than doctrine** — a tiebreak win scores **-10, identical to a loss**
(Magnus, 2026-08-10: *"we should never optimize for tiebreak wins, all of our
effort should be on killing the cores"*). **This is what keeps the currency
consistent with the defence field:** at 0 a pure survival plank converting
20 losses into 20 tiebreak wins would have scored +200 and looked like a
triumph; at -10 it scores exactly zero improvement. **⭐ THIS SENTENCE SURVIVES
THE 2026-08-11 AMENDMENT AND IS NOW LOAD-BEARING RATHER THAN DECORATIVE.** It
said `PLAY_DEFENCE: never` when written; the field is now
`not_at_the_kill_s_expense`, and **the -10 is what still makes turtling score
zero once the blanket ban is gone.** The ban used to do that work by fiat; the
scoring does it arithmetically, which is why loosening the field did not reopen
the tiebreak-turtle road. Balance property verified
UNCHANGED by the switch (speed +0.75, conversion +0.63, ratio 1.20 either way).

**⛔ IT IS NOT A LEG VERDICT STATISTIC. `KILL_SPEED_IS_LEG_VERDICT: no`.**
Per-game sd is **7.74**, so a realistic change needs **~2,100 games per arm**,
and it carries only **1.1x the power of plain win rate**. **A leg reporting it as
its primary repeats the 2026-08-10 failure exactly — an 18pp bar fired at a
fixture whose own MDE floor was 19.5pp — with a better-looking number.**
Legitimate uses: **version scorecards** (free, spends no games) and the **ship
gate**. `leg_read.py` prints the prohibition on the line itself, because a label
that lives only in a spec is a label nobody re-reads.

**SHIP GATE: beat -1.76 at n >= 200** — RECOMPUTED on the -10 tiebreak scale;
the old **-1.77** was computed under the 0-tiebreak rule and is STALE. Baselines:
v20 **-10.00** · v53 **-2.60** · v72 **-4.20** · v80 **-5.54** · v94 **-5.08** ·
v102 **-2.47** · **v104 -1.76** (best shipped, n=255).
**The rescale changed the HISTORY:** v20 scores exactly **-10.00 over 110 games**
— it never destroyed a core once, every "win" was a tiebreak — and **v53, which
read -1.77 on the old scale and appeared to TIE v104, drops to -2.60.** The old
scale credited tiebreak wins and flattered our early versions into looking like
today's bot.

**THE BALANCE PROPERTY IS A MAINTENANCE OBLIGATION, NOT TRIVIA.** These exact
numbers exist so that speed and conversion are weighted comparably: killing 40
rounds faster across the board pays **+0.79/game**, converting 10 of 109 losses
pays **+0.67/game** — within 20%. **If any bucket edge or the loss penalty
moves, RE-RUN that check**, or speed silently becomes decorative and the score
degenerates into a win-rate proxy with extra steps. `score.py`'s selftest
asserts the ratio and fails loudly if it drifts.

## Exit conditions — the only things that end this programme

1. Magnus says so.
2. The Loki curve crosses Eir on the primary currency AND survives a ladder read.

A Loki iteration that measures null does NOT end the programme. That is what an
iteration is.
