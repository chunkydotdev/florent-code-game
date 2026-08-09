# LOKI-6 (v122) — THE ARRIVAL DEFECTS. Three fixes, one currency.

version: unrated benchmark only; the slot returns to v94 immediately after.
dev_dir: bots/_v122loki6
line: loki (PROGRAMME.md). Forked from `_v120loki4` (LOKI-4, rush off).
  **COMPARE_AGAINST `_v120loki4` on the identical fixture.**

produces: **CORE-KILL SHARE, by removing three ways the bot stops being ALLOWED
  to reach the enemy ring.** The ladder says incidence is the scarce quantity —
  74.4% of our core-kill wins are already inside r250 and that holds at 1600+,
  while against Ouroboros we arrive in 9 of 155 games (5.8%). Three defects,
  each traced to a line, none of which changes what the bot TRIES to do:
  (1) the stall detector counts productive action as being stuck, because
  acting and moving are mutually exclusive, so a raider that works for 8 rounds
  trips a 120-round station ban on its first real nav failure;
  (2) the pause returns BEFORE the foothold heartbeat is written, so a paused
  raider *sitting at the ring* silences the signal that keeps the cold-insert
  window open for the whole team — permanently past r150;
  (3) `SLOT_LAUNCHER` is never cleared on death, so one launcher loss removes
  the ferry and our cheapest home defence for the rest of the match.

falsifier: **`core_kill_share` at or below `_v120loki4`'s on the same fixture.**
  Also refuting: any crash, or any sign the released launcher latch causes
  repeated rebuild churn (watch launcher count per game).

treatment_occurrence: **NOT YET VERIFIED, and I am saying so rather than
  assuming.** These are *removals of blocks*, so the treatment only occurs in
  games where the block would have fired. **The honest bar is on the OUTCOME
  side: does the team stand down less often?** If the legs come back null I
  will decode `SLOT_RAID_LIVE` continuity and launcher rebuild counts before
  reading it as "the fixes do not help" — a null with no measured treatment is
  the LOKI-2 mistake and I have already made a version of it today
  (LOKI-QUIET: treatment verified as coded, wrong quantity entirely).

S5_unrated: **THIS IS the unrated read**, under Magnus's standing grant
  (*"You're always go for unrated legs"*). Same 5-map short fixture and the
  same three opponents as LOKI-4's benchmark, so the comparison is a real
  same-fixture one rather than two experiments.

## LIMITS, BEFORE THE LEGS

- **n=5 per opponent, 15 total.** Directional only. Both prior legs at this n
  were seat-locked (LOKI-4 seat b ×3, v94 seat a ×3) and **I cannot control
  seat assignment** — if this draws a single seat again the comparison carries
  that confound. Research measured seat effects NULL league-wide at n=2,715
  (core-kill share 30.2% a vs 30.7% b), which bounds it but does not remove it.
- **Three fixes in one iteration means a positive result is not attributable to
  any one of them.** Accepted deliberately: they share a single mechanism
  (the bot being disallowed from raiding) and splitting them into three legs of
  n=5 would be weaker than one leg of n=15 on a shared question.
- **Fix 3 could plausibly HURT** by paying 20 Ti + 10% scale to rebuild a
  launcher that then dies again. That is the main way this iteration loses.
