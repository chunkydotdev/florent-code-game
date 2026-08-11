---
tactic: hall of fame — require a new candidate to beat an ARCHIVE of past opponents, not just the current ones
source: https://cseweb.ucsd.edu/~crosin/newmethods.ps
origin: Rosin & Belew, "New Methods for Competitive Coevolution", Evolutionary Computation 5(1), 1997
evidence: documented
transfers: no
---
WHAT IT IS — The canonical fix for "my benchmark opponents changed under me": keep the
best opponent from every generation forever, and score each new candidate against both the
current population **and** a random sample of that archive. Verified verbatim
(`acad_rosin.flat`):

> "hall of fame, which extends elitism in time for purposes of testing. The best individual
> from every generation is retained for future testing. Hosts are tested against both
> current parasites, and a sample of the hall of fame."

> "Successful new innovations cannot overspecialize; they are required to be robustly
> successful against old parasites."

**Referent:** "innovations" = new host strategies in a competitive-coevolution GA; "old
parasites" = hall-of-fame members, i.e. the best opponents from prior generations. The
claim is about a **testing constraint**, not a learning rule.

**LIGATURE WARNING for anyone re-verifying:** this 1996 dvips PDF drops `fi`/`ff`/`fl`, so
the flat file contains `di erent`, `tness` (fitness), ` rst` (first), `bene t` (benefit).
Grep ligature-free substrings or you will get a false FAIL.

WHY IT MIGHT TRANSFER — the *principle* is exactly our problem stated correctly, and it is
the textbook answer to the sweep-22 incident: a candidate that wins only against what
happens to be in front of it right now should not pass.

WHAT WOULD KILL IT — **the archive is unplayable, and that is fatal rather than
inconvenient.** Rosin & Belew's hall of fame works because a stored genotype can be
re-executed on demand. Ours cannot: an opponent's retired version is **gone from the
platform** and there is no `fcode match unrated <team> --version 4`. We can never get
another game against the thing we most need as a fixed reference.

Two consequences, and the second is the one that closes the road:
* The only hall of fame we *can* instantiate is over **our own** past versions — and that
  is precisely the fixture `WHAT LOKI IS` point 3 warns lies in a known direction (our
  `bots/*_probe` set: zero forward-turret deaths in 480 arena games against **46.9%** on
  the ladder). Building it would buy a reference that is stable and wrong.
* **Any claim that we "tested against the hall of fame" would be a claim about REPLAYS,
  not games** — and under `WHAT LOKI IS` rule 6, *a refutation without live-game backing is
  a hypothesis, not a refutation*. Replaying an archived opponent version is not available
  to us at all; re-analysing archived replays of it is not a test.

**AND THE LITERATURE'S OWN NEGATIVE, which pre-empts the obvious refinement.** Rosin &
Belew tried weighting the hall-of-fame sample by fitness and **abandoned it** — verbatim,
in the ligature-loss form as extracted:
> "the computational e ort required to maintain performance information on members of the
> hall of fame is much greater than the bene t obtained over random sampling"

So even where the mechanism *is* available, clever weighting of the archive did not pay.
Do not spend effort designing one.

BUILDER HOOK — none for the mechanism. The salvageable residue is narrow and worth stating
so the next session does not re-derive it: use the hall-of-fame *idea* only to justify
holding a **fixed panel of live opponent team ids** as a standing control set across legs,
while accepting that each team's internals drift underneath the id at a measured median of
**1.17 hours per version**. That is a much weaker instrument than a hall of fame and must
not be described as one.
