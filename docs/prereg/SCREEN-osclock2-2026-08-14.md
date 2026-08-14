# SCREEN PREREG — #54 arm 1b: `_v224osclock2` (K=4 + loop bans, v139 chassis)

**Committed BEFORE the shard's first heartbeat.** Builder s38, 2026-08-14.
Successor to arm 1 (OSCLOCK, cancelled by allocation at 48.67/n=1804 — its
sub-50 drift plus Magnus's requirement, verbatim: "I would want this fix to
actually make our bot perform better").

## What changed vs arm 1, and why each piece
* **K 8→4** (Magnus: "8 rounds is a lot of oscillation") — false fire costs
  ~1 round, missed lock costs 8+/cycle repeatedly; K=4 showed no false-fire
  blowup in the paired dose.
* **THE BANS — the piece arm 1 dropped from research's own variant (a):**
  on detection, the loop's TARGET is banned 80 rounds (raid_ban pattern)
  and the bounce pair 40 rounds; `_pick` skips banned targets and
  `_bfs_direction` treats banned tiles as blocked — the repick genuinely
  DIVERTS instead of routing back into the same corridor. Arm 1's residual
  re-locking is the hypothesized cause of its flat-to-negative screen
  (repick churn without diversion).
* **v139 chassis vs `_v218mapfix` control** (class rule; map strings
  grafted, verified: eco.py 34 changed lines = detector+bans only,
  main/raid untouched).

## Dose (paired midgard batch, seeds 260001-6, both seats, census instrument)
Treated **1.38%** locked builder-rounds (1/12 games) vs **9.44%** control
side (5/12) — 85% within-batch reduction, the strongest of any variant
(arm 1: 71%). Between-batch control swings (5.4/0.0/0.7/9.4 on the same
seeds) re-confirm lock formation is interaction-dependent — ratios within
a batch are the honest read, levels across batches are not.

## Read rules — THIS ARM CARRIES A PERFORMANCE PREDICTION, not only a harm gate
1. Primary: pooled share vs OB-F band at n=5400 (post-patch pool via
   pool26 runner).
2. **REGISTERED DIRECTIONAL PREDICTION: the GRAND-class (900-area) split
   exceeds the CQ/STD splits** — the lock tax concentrates on big maps
   (census: midgard 35.6%, 900s 11-14% vs 3-8% small), so if freed+diverted
   builders convert to performance anywhere locally, it is there. A flat
   GRAND split with a clean mechanism dose kills the "performance is
   recoverable locally" theory and routes the value question entirely to
   the live census re-run (research's path).
3. Futility gates apply. D26: replicate iff |final−50| ≥ 2.0pp (seed 273000).
   Kill-round paired-seed rides.
4. Coupling unchanged (opponent-induced exposure): live value read is the
   post-ship ladder census; the screen decides local performance and harm.

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.
