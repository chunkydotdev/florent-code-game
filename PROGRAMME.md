# ACTIVE PROGRAMME — machine-readable. `tools/gate.py` reads this and refuses off-programme batteries.

Edit this file ONLY on an explicit directive from Magnus. Both arms and every
successor session inherit it. The fields below are parsed; the prose is not.

    LINE: loki
    LINE_DIRS: bots/_v105loki1 bots/_v10?loki* bots/_v1??loki*
    INCUMBENT: bots/_v115dodge
    INCUMBENT_FROZEN: yes
    PRIMARY_CURRENCY: kill_speed_score
    SECONDARY_CURRENCY: core_kill_share
    WIN_RATE_IS_VERDICT: no
    COMPARE_AGAINST: previous_line_iteration
    KILL_WINDOW_RND: 250
    R1000_IS_DEFEAT: yes
    PLAY_DEFENCE: never
    FIXTURE_OF_RECORD: live_unrated

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

**PLAY_DEFENCE: never.** A plank whose mechanism is survival, screening, home
turrets or heal-uptime is off-programme regardless of what it measures. This
kills queue items that were alive at the s26 wrap.

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
consistent with `PLAY_DEFENCE: never`:** at 0 a pure survival plank converting
20 losses into 20 tiebreak wins would have scored +200 and looked like a
triumph; at -10 it scores exactly zero improvement. Balance property verified
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
