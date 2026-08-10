---
tactic: EVIDENCE HYGIENE — the famous "AlphaStar learned to feint" claim traces to a Vox article, not to a measurement. Do not cite it.
source: https://arxiv.org/pdf/2308.14752
origin: Park, Goldstein et al., "AI Deception: A Survey of Examples, Risks, and Potential Solutions" (2023); citation traced to Piper, Vox, 2019
evidence: documented
transfers: no
---
WHAT IT IS — **A landmine planted directly in the path of this sweep, defused.** Anyone asked to
research deception in strategy AI will meet the claim that DeepMind's AlphaStar learned to feint,
usually in this form:

> *"AlphaStar's game data demonstrate that it has learned to effectively feint: to dispatch forces
> to an area as a distraction, even when it has no intention of launching an attack there (Piper
> 2019). Such advanced deceptive capabilities helped AlphaStar defeat 99.8% of active human
> players (Vinyals et al. 2019)."*

It reads like a measured result in a peer-reviewed survey. **It is a citation to a news article.**
The survey's own bibliography:

> *"Piper, Kelsey (2019). StarCraft is a deep, complicated war strategy game. Google's AlphaStar
> AI crushed it. URL: https://www.vox.com/future- perfect/2019/1/24/18196177/aiartificial-
> intelligence-google-deepmind-starcraft-"*

**Note what the sentence does.** Two claims are joined by a colon-free "Such advanced deceptive
capabilities helped…", and they carry *different citations*: the **feint** is sourced to Piper 2019
(Vox); the **99.8%** is sourced to Vinyals et al. 2019 (the Nature paper). The 99.8% figure is real
and measured; **the feinting claim it is attached to is not, and the grammar invites you to read
the Nature citation as covering both.** No ablation, no counterfactual, and no operational
definition of "intention" for a policy network is offered anywhere in the chain.

WHY IT DOES NOT TRANSFER — **there is no tactic here to transfer; there is only a claim not to
repeat.** Filed because this library has been burned three times by paraphrase-into-unmarked-text,
and this is the adjacent failure: **a correctly-quoted sentence from a credible-looking source that
is load-bearing on nothing.** The quote above verifies verbatim. It is still not evidence that
feinting works, and a file that cited it as such would be wrong while passing every verbatim check.
That is precisely the failure mode rule 3 of this library's evidence rules exists to catch.

**The corroborating negative sits one step away.** Čertický, Churchill et al.'s IEEE ToG 2018
survey of a decade of StarCraft AI competitions — the organisers' own retrospective, 8,783 words —
contains **zero** occurrences of `decept`, `bluff`, `feint`, `fake`, `deceiv` or `mislead`
(`grep -c -i -E`, file sanity-checked non-empty and confirmed to discuss *"opponent modeling"*).
**The one venue that ran bot-vs-bot StarCraft for ten years and wrote the survey never once
described a bot deceiving another bot.**

WHAT WOULD CHANGE IT — a primary source: DeepMind game data, an ablation, or any measurement in
which AlphaStar's feinting behaviour is isolated and its contribution quantified. Until such a
thing exists, **the correct citation for "AlphaStar feints" is "a journalist wrote that in 2019".**

BUILDER HOOK — none. This file exists so the next session that meets this claim spends zero minutes
on it.
