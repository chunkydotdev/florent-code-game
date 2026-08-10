---
tactic: (D) THE FALSE POSITIVE THAT ACTUALLY HAPPENED — it was not a bot mis-reading a dead opponent, it was an ANALYST. A bot author's headline win-rate conclusion was overturned when he separated crash wins from played wins
source: http://satirist.org/ai/starcraft/blog/archives/679-CIG-2018-what-Steamhammer-learned.html
origin: Jay Scott (author of Steamhammer), "CIG 2018 - what Steamhammer learned", Brood War AI ladder (CIG 2018)
evidence: documented
transfers: yes — the contaminated-denominator failure applies directly to our own field battery
---

WHAT IT IS — sweep 21 went looking for the case where a bot wrongly concluded an opponent
was dead and committed on it. **The documented false positive found is one level up: the
author of a strong bot drew a conclusion about the FIELD from a win rate whose denominator
was polluted by crashes, published it, and then retracted it in the same post once he
separated the two populations.**

> *"This also means that my glib conclusion that Steamhammer won 66% of non-crash games, so it seems to have kept up with general progress is not sound. The non-crash games were mostly against weak opponents."*

The mechanism is stated immediately above it in the same post: crashes were **not
distributed at random across opponents** —

> *"The stronger opponents tend to be learning bots, so Steamhammer crashed more often on average against strong opponents."*

**So conditioning on "non-crash games" silently conditioned on "weak opponents", and the
66% measured the sample, not the bot.** The author caught it only because he wrote a script
to analyse the per-opponent opening tables; the aggregate number gave no hint.

**A second, cleaner control appears in the same tables and is worth keeping.** Against the
strongest opponent in the set, the crash channel simply did not open:

> *"PurpleWave shut out Steamhammer. It didn’t learn to make Steamhammer crash because every game was a win for it anyway."*

**That is the complement group.** Crash-contamination is not uniform across the field; it
concentrates in the matchups where the opponent needs it. Any per-opponent rate that is
computed pooled will smear that structure away.

WHY IT MIGHT TRANSFER — against OUR ruleset and, more to the point, our instruments:

- **We have exactly this denominator in the field battery.** Our ship verdicts weigh a
  class-weighted vs-field battery, and our own measurement says **four teams lose builders
  to an undamaged-vanish hazard at 224 per 10,000 border-tile builder-rounds while six
  teams have 722,545 border builder-rounds and zero events.** **The field is split into
  bots that self-destruct on geometry and bots that do not, and those two halves are not
  interchangeable opponents.** A pooled win rate over that field mixes "we outplayed them"
  with "they fell over", in unknown proportion, exactly as the 66% did.
- **And it bears directly on the primary currency.** `core_kill_share` and
  `time_to_core_kill` are both faster against a team that is quietly losing builders. **A
  fast kill against a crashing opponent is not evidence that the plank works**, and the
  Loki programme's whole verdict machinery runs on those two numbers.
- **The fix is the author's own and it is cheap:** stop reporting the pooled number, report
  it per opponent, and report the complement group alongside. The library already states
  the rule in the abstract — *numbers carry subjects, copy the denominator and the
  population* — **this is a worked example of the cost of not doing it, from someone who
  paid it in public.**

WHAT WOULD KILL IT —

- **This is an analyst error, not a bot error, and the brief asked for the bot error.**
  A bot that wrongly commits on "the enemy is dead" is still unevidenced in this sweep —
  see [`no-postmortem-in-twenty-two-detects-an-opponent-failure`](no-postmortem-in-twenty-two-detects-an-opponent-failure.md),
  where no team even built the detector that could be wrong. **Do not cite this file as
  evidence about in-game false positives; it is evidence about measurement.**
- **The contamination may be small for us.** 224 per 10,000 border builder-rounds is a
  rate on a subpopulation of rounds, not a rate of games decided. **Nobody has computed
  what fraction of our wins against those four teams coincide with a vanish event**, and
  until someone does, the analogy to Steamhammer's 66% is structural, not sized.
- **One post, one tournament, one bot.** Jay Scott's analysis is a single author's
  retrospective on his own data with no independent replication.

BUILDER HOOK — a corpus cut, no bot change, and it is the highest-leverage thing in this
file: **split every existing head-to-head result against the four vanish-prone teams into
games with and without an observed undamaged-builder vanish, and re-read our
`core_kill_share` and `time_to_core_kill` in each half.** If the two halves agree, the
battery is clean and we can stop worrying. If they diverge, several banked verdicts need
their denominators restated — which is exactly the discovery Jay Scott made, and it cost
him a headline claim.

Related: [`self-play-ab-has-the-wrong-population`](self-play-ab-has-the-wrong-population.md) ·
[`benchmark vs field, not self`](gains-land-in-the-hard-matchups.md) ·
[`a-crash-is-recorded-as-a-win-so-learners-converge-on-it`](a-crash-is-recorded-as-a-win-so-learners-converge-on-it.md)
