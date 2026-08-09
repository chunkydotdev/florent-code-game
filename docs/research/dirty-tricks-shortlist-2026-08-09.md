# The dirty-tricks shortlist: what to actually try, ranked by whether it beats the five teams that beat us

**Side lane, 2026-08-09 15:10 CEST. Synthesis of today's aggression work
(early-kill-arsenal, mechanic-bans, cad-core-kill, revert-brackets) into one
ranked answer to Magnus's question — "what dirty tricks do we need to try?" —
under the EV lens the builder sharpened and this lane verified: a trick is
worth (its effect) × (the games it applies to), and the games are concentrated.**

## The denominator that ranks everything (verified vs `corpus/ladder_games.tsv`)

Our whole rating deficit sits in five teams. We are **51.1% overall (1341/2625
games)** but **25.9% against the five teams that beat us (181/700 games)**:

| our worst | games | win rate |
| --- | ---: | ---: |
| **Ouroboros** | 150 | **15.3%** |
| Lunds Stallions | 180 | 25.6% |
| Kings College Munich | 115 | 27.0% |
| CtrlAltDefeat | 100 | 31.0% |
| Powerpuff Girls | 155 | 32.3% |

**A trick that does not move one of these five is rounding.** Teams we already
beat (vjg 72.5%, Cookie 65.7%, I Stone 58.8%) are not where the Elo is, no
matter how exploitable they look.

## TRY — ranked

### 1. The sentinel rush (Loki-2) — building now, highest EV
**What:** plant 3 sentinels against the enemy core by ~r17 at d²≈18 and kill
it by ~r52. **Why it's #1:** it targets the CORE, so it works regardless of
opponent meta-game; it is a parameter change to the thing we are already the
league's #1 at (309 early kills, but thin/slow — 1 turret at d²=32, killing
at r91); it has a rule-arithmetic floor (3 sentinels = 18 DPS ≈ 28 rounds
through 500 HP); and it is on the **surviving-strong-line side of every
organizer nerf** ("defence is hard, attack is easy"; turret aggression was
never nerfed — mechanic-bans doc). **Hits the five:** Ouroboros and Lunds
beat us by out-*siegeing* us (cad-core-kill: the sentinel is exactly the
weapon we can't defend); winning the *race* is the direct counter to teams
that win the siege. **Field-proven recipe** (Banminary r52, Big O r63).

### 2. The spawn-denial ring (Loki-3) — bundle with the rush
**What:** park builder bodies on the enemy core's spawn-ring tiles to suppress
their heal detail while the sentinels fire through the collar (sentinel shots
ignore obstacles). **Evidence, three independent lines:** the builder's own
probe (body on a ring tile → `can_spawn` false 1:1, dumb park-bot won 9/12);
a BC2024 precedent (offensive spawn-blocking used as a legal, never-banned
tactic); and it *composes* with #1 rather than competing for tiles. **Caveat:**
barrier-form is refuted, only the **body** form works, and a real lock needs
all ring tiles (the core needs one free tile) — so measure it as "heal-tiles
denied/round," not "spawn locked." Don't ship alone; it needs the rush as its
damage source.

### 3. Pointed crash-induction at Ouroboros ONLY — low confidence, probe first
**What:** throw an enemy builder to a destination its pathing doesn't expect,
inducing an uncaught `GameError` → **permanent unit loss** (documented in our
OWN chassis, PIECE N `main.py:4664`: a launcher throw broke our positional
invariant; we survived only via a blanket `try/except`). **Why it survives the
EV cut at all:** Ouroboros is our worst matchup (15.3%) AND carries a 29.1%
no-damage-removal rate (74/254, 4× the field baseline). **But this lane's join
just deflated the field-prevalence argument:** across the whole corpus,
no-damage removals are NOT throw-correlated — they are *less* likely to follow
a throw than damage deaths are (0.1–0.5% vs 0.5–2.2%; enrichment 0.1–0.3×).
So Ouroboros's 29.1% is **not** evidence a throw will crash them — it is
Ouroboros crashing on its own, unrelated to being thrown. **The mechanism is
real (it happened to us) but is not visibly weaponised by anyone in the
field.** Verdict: worth ONE pointed probe — throw `ouroboros_probe` into
surprising cells, watch its stderr under `fcode run` for a traceback (the
discriminator the stdout-stripped archive can't give) — but the honest prior
is low, and the probe tests *our imitation*, not the real team.

## DO NOT TRY — measured dead (protects arena time)

- **Suicide-builder rush** — `self_destruct` deals 0 damage (organizer nerf,
  "removing builder self-destruct damage nerfs rushes").
- **Cheap-builder swarm** — 30 Ti + 20% scaling + 50-cap all anti-spam.
- **Infinite self-heal blob** — heal nerfed to 1 Ti/4 HP.
- **Ammo-drain baiting** — died pre-build (drain-discriminator doc).
- **Late forward insertion as doctrine** — refuted on four instruments; only
  the EARLY window (r<150) is open, and #1 already occupies it.
- **More-defence / ESCALATE** — −7.8pp; SITE forward siting −6.7pp.
- **Kidnap-for-damage** — 61k corpus throws, 0 core attacks; it's displacement
  only (throw-into-arc is the untested exception, folded into #3's probe).

## NOT A BUILD — already deployed, just don't break it

- **Tiebreak-turtle** is **Eir's** job, and Eir holds the slot: we are 16-4
  against CAD at r1000 (cad-core-kill), and CAD is one of the five. The
  discipline is to NOT let an aggressive Loki overwrite the matchups where
  survive-to-r1000 already wins. That is the whole argument for shipping the
  rush as a *separate* bot, not a posture bolted onto Eir.

## Two decay classes for the process ledger (both surfaced today)

- **"Correct mechanism, irrelevant target"** (builder): crash-induction priced
  high on effect, ignoring that its visible targets are teams we already beat.
  Same family as the morning's 15× builder-death artifact — a real number on
  the wrong population. The fix is the denominator, applied *first*.
- **"Field prevalence ≠ inducibility"** (this lane): a mechanism being common
  in the field (Ouroboros's 29.1% no-damage) is not evidence *we* can induce
  it — the throw-correlation join says the two are unrelated. Measure the
  causal link, don't infer it from co-occurrence.

## Provenance

Win rates: `corpus/ladder_games.tsv`, game-level, verified this lane (five-team
25.9%/700 reproduced exactly). No-damage-by-team: `dc_deaths` cls column
(vjg 97.7%, us 0/8564 — reconciles with the death-attribution doc). Throw↔death
join: `throws.tsv` bot-id × `dc_deaths` bid, death within K∈{1,2,3,5} rounds of
a throw. PIECE N quote verified verbatim at `main.py:4664`. Changelog quotes
re-verified in mechanic-bans doc.
