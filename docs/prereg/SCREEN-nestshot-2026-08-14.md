# SCREEN PREREG — #3 arm 1: `_v226nestshot` (counterbattery answers the plant)

**Committed BEFORE the shard's first heartbeat.** Builder s38, 2026-08-14.
Queue #3, evidence chain: Bisons book (66% of their losses show nest
removal; we remove at 15-17%) → research's damage-fingerprint ledgers
(removal that works = SENTINEL fire, 74.7% of removal damage, 2-4 round
kills, zero gunner kills; the failure case = follow-up plants unengaged) →
**grep-the-incumbent findings that shrank the arm to one gate: detection
(enemy turret ≤64 d² of core → SLOT_THREAT) and target priority (SENTINEL
ranks above builders in `_turret`) are ALREADY SHIPPED. The gap: with a
live home gun, `_try_counterbattery` waits for `_core_shelled()` — actual
core damage — before answering a plant. Against a 2-4-round killer that
wait is the loss.**

## The arm (one gate change)
`bots/_v226nestshot` = v140 + `LOKI_NESTSHOT_ON`: when the reported threat
tile holds a STANDING enemy GUNNER/SENTINEL (defender-vision check,
exception-guarded, falls back to current behaviour out of vision), the
counterbattery skips the core-shelled wait. Flag-off = byte-identical
behaviour. main.py + doctrine only; eco/raid untouched.

## Dose evidence and the declared gap
Code-level: single-occurrence asserted edits, parse-verified, flag guards
structural. **GAP declared: no engine-level dose pre-launch** (the branch
needs an enemy plant inside the band with a live home gun — opponent-
dependent). A kept-replay spot check (counterbattery build round vs plant
round) is OWED at the read if the final is outside the band either way.
Coupling: the TRIGGER is opponent-induced (plants), the RESPONSE is
self-knowledge; self-play under-doses plant frequency (creeper-class
opponents plant most — the field's, not ours) ⇒ screen is harm-gate +
directional; the value read wants the live surface / the Bisons rematch.

## Design
`NESTSHOT` vs `_v223sealrepair` (v140), full 15-map POST-patch pool
(pool26 runner), n=5400, seed_lo 276000, futility gates per
RULE-futility-gates, OB-F band 48.67–51.33. D26: replicate iff |final−50|
≥ 2.0pp (seed 277000). Kill-round paired-seed rides (the response spends
Ti a kill might want — the non-regression bar is live here).

## Not licensed
No ship implication (v140 sitting, k=1). #41 (siting/facing coverage) and
the reactive-second-sentinel variant are SEPARATE arms, built only if this
gate change screens short of the ledger's implied effect.

## Target-value line
Local screen, zero live exposure ⇒ payout gate N/A.
