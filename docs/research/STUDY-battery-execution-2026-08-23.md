# BATTERY EXECUTION-QUALITY STUDY — banked summary (full: battex_* scratch)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition.**

**HEADLINE: THE ROLLING BATTERY IS NOT PLAYED. `SK_ROTATE = False`
(sk_maps.py:4286) — every doctrine mechanism (WANT=4, PRESTAGE=278,
CLUSTER_GAP=2) is dead code behind it.** What runs: the v619/v620 two-tube
nest pair, one body, continuous siege from median r32 — no phase flip.
59/90 cells never reach r300 alive; the eco-to-r300 premise does not
describe the shipped bot.

- Live binding gate: **sk_roles.py:7208 `if live >= want: return`,
  want = SK_NEST_PAIR_N = 2.** 62/90 cells hit exactly this ceiling.
- WIN cells: achievable peak 4.0 (own purse, own surcharge bar), achieved
  2.0 — **the largest measured gap; money was left on the table.**
- LOSS cells: achievable only 2.5-3.0 — titanium binds (the ROUTE plank's
  territory). Post-flip spend split: wins 52% sentinels / 28% bodies;
  losses 30% / 62% (replacing bodies instead of buying barrels).
- Duty (length-immune headline): wins 0.400 vs losses 0.199 per turret
  (ceiling 0.5). Ammo starvation costs ~half the gap (duty 0.334
  low-starvation vs 0.183 high; 1 in 5 battery-up rounds cannot afford one
  shot; the drip "NEVER BANK" note at sk_core.py:306). AP returns here.
- Spacing: successive plants d²21 (wins) vs 61 (losses); live min gap
  SK_NEST_PAIR_MIN_GAP=8; placement spread as a concurrency killer is
  structurally impossible (band max 32 == sentinel r²) — road closed.
- Wins-vs-losses contrasts DEFF-corrected (MAP cluster live, DEFF 2.16):
  only peak>=2 survives (+32pp, CI excludes 0); duty carries the largest
  raw gap and is length-immune.
- Doctrine-level finding FOR MAGNUS: the shipped bot sieges from r30 and
  its wins do too; the two-phase boundary describes neither. Reported,
  not silently changed.

Recommendations in headroom order: (1) raise the LIVE ceiling at :7208,
(2) burst rule (withhold #1 until two funded at the :8608 surcharge bar),
(3) bank ammo ahead of the battery (SK_AMMO_PUSH as the funding arm),
(4) tighten live spacing. Instrument: 6 controls both-verdict-driven; one
achievable() defect found and fixed pre-banking.
