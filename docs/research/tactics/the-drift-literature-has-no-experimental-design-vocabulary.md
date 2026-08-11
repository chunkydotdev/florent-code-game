---
tactic: importing a blocked/paired experimental design for opponent drift from the coevolution & MARL literature
source: term census over 11 flattened primaries (~800 KB) — Balduzzi 2018/2019, Czarnecki 2020, Lanctot 2017, Hernandez-Leal 2017, Vinyals 2019, Glickman, Rosin & Belew 1997, Pollack & Blair 1998, Cartlidge & Bullock 2004
origin: sweep 22, arm ACADEMIC (research arm, 2026-08-11)
evidence: documented (measured term census)
transfers: no
---
WHAT IT IS — Sweep 22's arm (B) asked: *did anyone run paired/blocked/interleaved designs
to absorb opponent drift, and what did they block on?* Against the academic corpus the
answer is a clean measured negative: **that is not a literature.** Term census across all
11 usable flattened primaries:

| term | total hits |
|---|---|
| `blocking` | **0** |
| `stratif*` | **0** |
| `power analysis` | **0** |
| `common random numbers` | **0** |
| `matched pairs` | **0** |
| `variance reduction` | **0** |
| `counterbalanc*` | **0** |
| `pre-regist*` | **0** |
| `p-value` | **0** |
| `statistical significance` | **0** |
| `randomized controlled` | **0** |
| `control group` | 1 (AlphaStar) |
| `confidence interval` | 7 (Glicko doc only) |

The coevolution and multi-agent-RL communities solved opponent drift by building
**archives and populations** — hall of fame, league, CIAO matrices, PSRO — and **never** by
importing design of experiments. Pollack & Blair's foil setup is the only recognisably
blocked design in the corpus, **and they never call it that.**

A second, adjacent negative from the same corpus: **nobody studies a population of
independently-authored, silently-versioned opponents.** `concept drift` appears 10 times,
all in one file (the Hernandez-Leal survey), and every instance is a *single* opponent
switching among its own stationary strategies **mid-interaction** — an online,
within-episode detection problem. `patch` appears 5 times, none about game balance. The
framing closest to ours — *N human teams each shipping unannounced revisions to a public
ladder* — is **absent**. And the survey's own taxonomy of responses is, verbatim, "five
categories: ignore, forget, respond to target opponents, learn opponent models and theory
of mind" — **all five presuppose an agent adapting online, and we are stateless across
games.** All five are unavailable to our bot and relocatable only to our analysis pipeline.

WHY IT MIGHT TRANSFER — it does not transfer; it **redirects effort**, which is why it is
filed rather than discarded. Two consequences:

1. **Stop looking for the citation.** No one wrote "block on opponent version". A future
   session that goes hunting for it will burn a sweep and find the same zeros. The design
   fix for our problem had to be derived here, and it was — see
   `block-on-opponent-version-not-opponent-id.md`, measured at **−8.00pp game share,
   t = −15.81**, with the classical *shape* borrowed from Pollack & Blair rather than any
   drift-specific source.
2. **We are ahead of this field on one axis and behind it on another.** The discipline this
   repo already runs — preregistration, placebo arms, negative controls, stop-losses,
   powered nulls — is **not** borrowed from the coevolution literature and cannot be
   validated against it. What that literature has and we do not is **archive machinery**;
   what we have and it does not is **inferential hygiene.** Trade accordingly: mine it for
   archives and matchmaking rules (PFSP, held-out validation sets, CIAO matrices), never
   for statistics.

WHAT WOULD KILL IT — the census covers the coevolution / MARL / rating-systems corpus
selected for this sweep. It says nothing about the **general** experimental-design
literature, where blocking and matched pairs obviously do live; the claim is narrowly that
**the literature on drifting opponent populations does not use them.** It is also 11
documents, not a systematic review — a targeted search of, say, the tournament-design or
sports-analytics literature could well come back positive and would be a different sweep.

BUILDER HOOK — none. This is a road-closing result: it stops the next session
re-researching arm (B) in the same place.
