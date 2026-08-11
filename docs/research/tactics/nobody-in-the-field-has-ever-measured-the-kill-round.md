---
tactic: MEASURED NEGATIVE — A/B testing of individual features is routine in this field and EVERY reported outcome is a win rate. Across 41 primary documents / 166,155 words, 27 duration and time-to-win phrasings return ZERO hits. Nobody has ever run our admission bar.
source: https://battlecode.org/assets/files/postmortem-2025-just-woke-up.pdf
origin: census over Battlecode 2019-2026 (24 documents), Halite II/III, Screeps, Terminal, StarCraft AI ladder writing
evidence: documented
transfers: yes
---

## WHAT IT IS — the census, and it is the sharpest arm of sweep 24

`DEFENCE_ADMISSION_BAR: kill_round_non_regression` requires a defensive plank to carry a
kill-round bar beside its survival bar. **Sweep 24 went looking for anyone who had ever
done that. The answer is nobody, and the corpus is not thin.**

**Corpus:** 41 flattened primary documents, 166,155 words — all 22 official Battlecode
postmortems 2019-2026 plus the XSquare guide and alext's 2026 postmortem (24 Battlecode
documents in total), Halite II/III writeups (rooklift, teccles, TheDuck314, mlomb),
Screeps documentation and forum threads, Terminal (C1 Games) starter algo and the
3rd-place APAC team's algorithm README, and Jay Scott's StarCraft AI ladder articles.

**Part 1 — the instrument EXISTS and is well developed.** A/B testing against a held-out
bot is standard practice and is named as such:

| source | quoted |
|---|---|
| Just Woke Up (BC2025, winners) | *"slight adjustments to the spawning micro that we honed in by doing AB tests against our various versions of old bots"* |
| Just Woke Up (BC2025), same document, first-person section | *"that enabled me to AB test two bots on every single map I had at my disposal"* — a borrowed script from team camel_case, replacing what the author calls *"going off of vibes"* |
| alext (BC2026) | *"if you use an older version of your bot as a baseline, and accept any change that increases your win rate"* |
| SPAARK (BC2025) | *"Make a runmatches.py script and look at your scrims"* |

*(⚠ Attribution note, recorded because the check caught it: the second row was drafted
against **confused (BC2025)** on the strength of its first-person voice — the Just Woke
Up postmortem is co-authored by Tim Gubskiy and Andy Nguyen and its Automations section
is written in the first person singular. The literal grep put it in
`postmortem-2025-just-woke-up.pdf` and nowhere else. **Verbatim caught a wrong-file
attribution that verbatim-plus-plausibility would have waved through.**)*

**Part 2 — every outcome anyone reports from it is a WIN RATE or a RATING.** Gone Fishin'
*"increase our win rate by 5%"*; cout for clout *"improved our rating a whopping 130
points (from 1720 to 1850)"*; confused *"a 70%+ win rate against my submission for
qualifiers"*; om nom *"a substantial win rate against our old bot"*.

**Part 3 — THE COUNT. 27 distinct duration / time-to-win phrasings over the full 41-file
corpus:**

```
game length 0 · game duration 0 · average game 0 · length of the game 0
average number of rounds 0 · median round 0 · shorter game 0 · longer game 0
time-to-win 0 · time to win 0 · won faster 0 · win faster 0 · kill faster 0
end sooner 0 · ends sooner 0 · ended earlier 0 · turns to win 0 · rounds to win 0
number of rounds it 0 · how many rounds it 0 · average turn count 0 · win in fewer 0
fewer rounds 0 · fewer turns 0 · slowed our 1 · slowed down our attack 0
delayed our attack 0
```

**Total: 1 hit across 27 terms, and it is not about defence** — BC2020 The High Ground,
*"in the other it slowed our progress considerably"*, whose subject is **cows**, an
environmental obstacle near their HQ that blocked their wall, not a defensive investment
of theirs.

**⇒ In 166,155 words of competitive writeups from six leagues, nobody reports how long
their games took, before or after any change.** The metric on which our programme now
adjudicates defence is not merely unmeasured in the field; **the vocabulary for it does
not appear.**

## THE TWO NEAR-MISSES, because they are more instructive than the zero

**(1) cout for clout (BC2024) measured the COST side of a defensive commitment and only
the cost side.** They tried the "sitting duck" pattern — three units held on their own
spawn — and priced it by deleting the units from the fight entirely:

> *"Turns out, using 3 ducks to sit on your spawn makes you lose just about every micro
> battle. By doing a simple test of 47 vs 50 ducks, we found that the version with 47
> lost 90% of the games, and it wasn’t even close."*

> *"Instead we decided to be even less defensive and go full aggro"* … *"This improved
> our rating a whopping 130 points (from 1720 to 1850)."*

**This is a clean experiment on the opportunity cost of a defensive assignment and it
removed the defensive BENEFIT from the test entirely** — the 47-duck arm does not station
anyone on the spawn, it simply has three fewer units. It answers "what does the
commitment cost" and cannot answer "was it worth it". *(Already filed from the
population angle in* [`self-play-ab-has-the-wrong-population`](self-play-ab-has-the-wrong-population.md)*.)*

**(2) The BC2025 CHAMPION A/B-tested its defensive addition, THE TEST SAID NO, they
shipped it anyway on an explicit population argument, and it won them the tournament.**

> *"When we performed AB testing against our past bots, and using defense towers did not
> seem to be very good… Against our past bots it usually went even in wins, or even
> slightly lost. But our bot wasn’t super aggressive, and we believed that this, in
> theory, SHOULD be better against the teams that we have the worst matchups against."*

The referent of *"this"* is their gated defense-tower rule (≤2 towers, choke geometry,
near map centre — filed as [`cap-the-expensive-emplacement-and-gate-it-on-a-choke`](cap-the-expensive-emplacement-and-gate-it-on-a-choke.md)).
They then report *"the results were unbelievable"* and credit it with beating their two
biggest threats. **The A/B was a win-rate A/B run against a population that did not
contain the threat the plank existed to answer.**

## WHY IT TRANSFERS — and what it does to our own bar

**Three consequences, in descending order of how much they should change behaviour.**

1. **THERE IS NO PRECEDENT TO PORT. `kill_round_non_regression` is ours to define, and
   nobody's constants, thresholds or estimators are available to borrow.** Any sweep or
   prereg that writes "the field does X for the tempo bar" is inventing it.
2. **A kill-round bar run on our own arena inherits exactly the defect that nearly cost
   Just Woke Up the title.** Their A/B was against *"our past bots"*, and their own
   diagnosis of why it misled them is a POPULATION statement: *"our bot wasn’t super
   aggressive"*. Our arena opponents are `bots/*_probe`, which we wrote, and which the
   library already records as lying in a known direction. **A defensive plank whose whole
   point is to survive an aggressive opponent CANNOT be adjudicated against a fixture that
   is not aggressive**, on either the survival bar or the kill-round bar.
   ⇒ The bar must be read on **`fcode match unrated <team_id>` legs against live teams**,
   which `PROGRAMME.md` point 3 already requires for a different reason.
3. **A win-rate bar and a kill-round bar can disagree, and the field only ever collected
   the one that our own ladder does not pay.** Our ladder scores `delta = 32 x (S − E)`
   with S = games won / 5 — game share, not match wins. So we would be running a bar the
   field has never run, on a currency the field does not use, against opponents the field
   never had. **Every part of it has to be built and validated here.**

## HOW IT MEETS THE ADMISSION BAR

It does not need to — it is not a plank, it is the finding that the bar has no
precedent. **What it obliges is that every OTHER file in this sweep names, concretely,
what observation would show the kill slowed.** All of them do.

## WHAT WOULD KILL IT

* **Publication bias, stated plainly.** These are postmortems: narrative documents
  written after the fact for a general audience. A team could have tracked game length
  in a spreadsheet and never written the word. **The claim is "nobody REPORTS it", not
  "nobody computed it"** — and the useful consequence is the same either way, because an
  unreported method is not one we can port.
* **Some of these leagues have no kill to time.** Halite I-III, Lux and Terminal score at
  a fixed horizon, so "time to win" is not a quantity that exists in them. **The negative
  is therefore strongest where it matters most — Battlecode, whose game ends on a killed
  HQ and whose 24 documents contain zero of all 27 terms.**
* A single counterexample in an unswept league would narrow it. It would not restore a
  portable constant.

## BUILDER HOOK

**None needed for the finding.** The consequence for tooling is one line: **the overnight
reader and the leg scorer should print MEDIAN KILL ROUND beside win rate and game share
on every arm, unconditionally, whether or not the arm is defensive.** A bar that is only
computed when someone remembers to ask for it will be met and missed by choosing an
estimator afterwards — the repo's own standing lesson. If the number is always on the
page, no future prereg can quietly omit it.
