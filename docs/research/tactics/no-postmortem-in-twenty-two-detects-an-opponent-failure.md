---
tactic: (A/B) NEGATIVE RESULT — 22 Battlecode postmortems, 2019-2026, contain zero opponent-failure detectors. Every mention of running out of compute is a team describing its OWN bot, and the fix is always a self-guard
source: https://battlecode.org/past
origin: MIT Battlecode official team postmortems 2019-2026 (all 22 PDFs linked from battlecode.org/past), searched in full
evidence: documented
transfers: yes — as a prior on how rare this idea is in our direct ancestor
---

WHAT IT IS — a census, not an anecdote. All 22 postmortem PDFs linked from
`battlecode.org/past` were downloaded, converted with `pdftotext`, whitespace-flattened
(including `\f`/`\r`, per the library's method note) and searched.

**Positive control first, because a zero is not a result without one:** 21 of 22 files
match `enemy`, 15 of 22 match `opponent`. The corpus is loaded and the search works.

**Result — every one of these returns 0 hits across all 22 files:**
`opponent stopped`, `enemy stopped`, `opponent crashed`, `enemy crashed`,
`opponent timed out`, `enemy timed out`, `opponent is dead`, `opponent had crashed`,
`stopped moving`, `stopped responding`, `no longer acting`, `inactive opponent`,
`not doing anything`.

**What IS there is the mirror image — teams instrumenting their own failure and guarding
against it.** Every compute-exhaustion passage in the corpus is first-person:

> Just Woke Up (2025), describing the guard they added: *"bytecode limit, causing them to effectively do nothing that turn."*
> The surrounding sentences establish the referent — the guard is *"if our bots ran out of bytecode while computing the best location to splash, they would stop scanning nearby mapInfos and proceed with their turn"*, so that *"they would still take some actions instead of exceeding their bytecode limit"*.

> SPAARK (2025), naming a cost driver: *"out of bytecode after getting spammed with 20 messages from a tower."* — the towers are their own; this is a self-inflicted read cost, not an attack.

> Wololo (2021), stating the engine consequence of the era: *"halt its code for the round and take no action, and proceed the next round where its code left off, losing one round’s worth of action."*

**The one place a team's compute problem meets an opponent, it is the opponent's own good
play doing it incidentally, and the closest thing to deliberate degradation in the whole
corpus is an accident** — see
[`both-recorded-crash-inductions-came-through-the-message-channel`](both-recorded-crash-inductions-came-through-the-message-channel.md).

WHY IT MIGHT TRANSFER — against OUR ruleset specifically:

- **This is the direct ancestor of our engine and the closest population to our field.**
  Twenty-two finalist teams over eight years, several of them tournament winners, and not
  one wrote "the enemy stopped acting, so we did X". **Combined with
  [`every-other-league-resolves-the-failure-and-ours-does-not`](every-other-league-resolves-the-failure-and-ours-does-not.md)
  the explanation is structural rather than an oversight**: in Battlecode the failure is
  either fatal to a single robot (invisible from outside, exactly as here) or a lost turn
  that resumes (invisible from outside). There was nothing to see.
- **So a detector here would be genuinely novel, and the library should price it as
  novel.** That cuts both ways and the caution is the same one the library applies
  elsewhere: an idea absent from twenty-two strong postmortems is more often absent because
  it does not pay than because nobody thought of it. **Compare
  [`nobody-in-twenty-two-postmortems-built-a-decoy`](nobody-in-twenty-two-postmortems-built-a-decoy.md)
  — same corpus, same shape of finding.**
- **The transferable positive is the self-guard, and it is unanimous.** Every team that met
  the compute wall responded by making their own code degrade gracefully — bail out of the
  scan, keep the turn's action. **Our engine's penalty for the exception branch is worse
  than theirs and our measured TLE rate is 0.00% at ~12% of budget**, which means we have
  headroom the ancestor did not, and no excuse for an unguarded enumeration.

WHAT WOULD KILL IT —

- **Absence of the phrase is not absence of the behaviour.** A team could have shipped an
  idle-enemy heuristic and simply not written about it; postmortems are highlight reels.
  The claim this file supports is **no team chose to write about it**, which is weaker than
  **no team did it** — and it should be cited in the weaker form.
- **Search terms were English collocations chosen by one author.** A team could have
  described the same idea as, say, "unresponsive", "frozen", or in a code listing. Some
  paraphrase risk remains despite thirteen probes.
- **Eight years of Battlecode had eight different games.** In several of them (2020's
  flooding map, 2021's influence bidding) a passive opponent loses on its own, so the value
  of noticing was lower than it would be for us at round 1000.

BUILDER HOOK — none directly. **The usable output is a budgeting prior:** treat
opponent-failure detection as an unprecedented plank in this engine family, hold it to the
same bar the library holds other unprecedented planks to, and do the corpus cut named in
[`every-other-league-resolves-the-failure-and-ours-does-not`](every-other-league-resolves-the-failure-and-ours-does-not.md)
before any bot code is written.

**Method note for the library:** the 22-PDF corpus is reproducible in three commands —
scrape `postmortem-*.pdf` hrefs from `battlecode.org/past`, `curl` each from
`battlecode.org/assets/files/`, then `pdftotext` + `tr -s ' \n\t\f\r' ' '`. The positive
control (`enemy` → 21/22) should be re-run every time, because a broken extraction and a
true zero look identical.
