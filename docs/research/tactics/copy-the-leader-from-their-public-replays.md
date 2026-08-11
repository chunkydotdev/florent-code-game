---
tactic: reconstruct the current leader's strategy from their public replays — and deploy the rival-specific counter LATE, not resident
source: https://battlecode.org/assets/files/postmortem-2020-the-high-ground.pdf · https://blog.stoneztao.com/posts/bc21/ · https://battlecode.org/assets/files/postmortem-2021-wololo.pdf
origin: Battlecode 2020, team "The High Ground" (4th); Battlecode 2021, Stone Tao and Isaac Liao
evidence: documented narrative with named rivals and named outcomes; no game counts attached, so effect sizes are anecdotal
transfers: partial
---
WHAT IT IS — A complete two-sided scouting cycle in one document. The High Ground read the
scrimmage ladder to decide *whose* strategy to steal, rebuilt it from that team's public
replays, and climbed on the clone (`lad_bc_pm2020.flat`; note curly apostrophes in the
source):

> "We thought that although smite got 1st place in the seeding tournament, Java's
> terraform/attack variant was the future. This was due to Java's first place rank on the
> scrimmage ladder, and the potential room for improvement in the terraform/attack as
> opposed to rush/turtle. So, we decided to shamelessly copy Java's strategy."

> "We pulled up some replays of Java's games and worked on a new bot for several days until
> we imitated it"

**Referent:** "Java" is a rival team name — it went on to win the 2020 final tournament;
"replays of Java's games" are that team's public scrimmage-ladder matches.

**AND THE TARGET ANSWERED, WITHOUT SHOWING IT FIRST** — same document:
> "Java ended up winning, defeating both Battlegaode and smite. It turned out that Java also
> imple- mented a last minute fix to counter us, and through scrimmages we found out that
> they had a good win-rate against us."

*(`imple- mented` is a PDF line-break artifact, preserved verbatim.)*

Corroborated independently (`lad_bc21_stone.flat`, Stone Tao, Battlecode 2021): "After
copying other team's queues, I instantly shot back up" and "careful analysis of match
replays is crucial to doing well."

WHY IT MIGHT TRANSFER — **the READ is available to us at a scale these competitors never
had.** 98.0% of our league match table is matches between other teams, the platform serves
third-party replays, and our corpus already holds ~35k matches with per-match versions. We
can identify the current leader, pull their replays, and reconstruct what they do. Nothing
here needs bot state or a rated match.

**THE SECOND HALF IS THE WARNING, AND IT IS THE ONE THAT CHANGES BEHAVIOUR.** Java's counter
was withheld until it could not be scouted back. If we build a rival-specific counter off
public replays and then leave it resident on the ladder for hours, we hand them the same
read with more games — at ~6 games/hour of published behaviour. **A rival-specific counter
is the class of plank most damaged by holding the slot**, and the Battlecode precedent says
the correct deployment is short and late, not resident. That is the one place where this
literature and our exposure asymmetry genuinely coincide.

WHAT WOULD KILL IT — **the non-stationarity that opened this sweep is also the natural
defence against scouting.** A counter built from replays presumes the target's behaviour is
stable enough to counter. Against a team shipping four versions in 4.5 hours, at a measured
median version lifetime of **1.17 hours**, the read is stale by construction. **Scout the
teams whose version timeline is quiet; do not spend a leg countering a team that reships
hourly.** `tools/corpus/version_drift.py` ranks exactly that.

Three further limits:
* Every effect claim in this file is a **first-person narrative with no denominators.** The
  intent and design are documented; that the copying *caused* the result is not.
* One competitor rejected opponent-specific testing on principle and still placed well —
  _Royale: *"don't use the IDE or CG Spunk because I think it is too slow and not relevant
  with too few games"* (`lad_cg_spunkhiding.flat`). **No competitor in this corpus measured
  scouting against not-scouting**, so the positive case rests entirely on narrative.
* **A risk we have not priced:** where opponent-chosen unrated testing exists, strong teams
  opt out of being a fixture — *"many top teams turned the option off to avoid being flooded
  with scrimmages"* (`lad_bc_pm2021.flat`; "the option" = auto-accept for competitor-requested
  scrimmages). Our panel method assumes universal availability. If our league ever adds an
  opt-out, the panel degrades to whoever tolerates us, and those are systematically not the
  teams in the reachable band.

BUILDER HOOK — read-only and cheap: pick the highest-rated team whose current version has
been stable longest (`version_drift.py` gives both), pull their third-party replays from the
corpus, and write up what their opening actually does. That is a scouting *deliverable*, not
a plank, and it costs no matches. Only after that is it worth asking whether a counter is
worth a submission — and if it is, fire it inside a window and roll back, per the shipping
procedure already in `CLAUDE.md`.
