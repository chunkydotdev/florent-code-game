# LOKI-3 (v119) — THE KIDNAP PLANK. Pre-registered before the first battery.

version: dev only. NOT a ship, NOT a slot swap. v94/`_v115dodge` stays live.
dev_dir: bots/_v119loki3
line: loki (PROGRAMME.md). **COMPARE_AGAINST: `_det_v118loki2b`** — the previous
  line iteration, never Eir, never v92.
control: `LOKI_KIDNAP_ON = False` reproduces LOKI-2b exactly. Every other
  difference is zero by construction, so the flags-off leg is a true ablation
  and is the only leg that can attribute anything.

produces: **DENIAL OF THE ENEMY HEAL LINE, priced as a dead enemy Core inside
  r250.** The plank plants forward launchers (we currently build 0.64
  launchers/game and none forward) and throws enemy builders off the 8 collar
  seats. Primary currency `core_kill_share`, secondary `time_to_core_kill`,
  both vs `_det_v118loki2b`. Mechanism metrics (attribution ONLY, never the
  bar): enemy-core HP-recovery rate r0–250, collar-seat occupancy denial.

falsifier: **`core_kill_share` not above `_det_v118loki2b` AND
  `time_to_core_kill` not shorter**, on the paired battery. If the mechanism
  metrics move and the currency does not, **the plank is NULL and I will record
  it null** — a denial metric is attribution, never a substitute bar. Also
  refuting: any leg with a crash, or treatment occurrence at zero (below).

treatment_occurrence: **UNMEASURED AT WRITE TIME — measured before the battery,
  not after.** The triggering state is (a) a forward launcher actually built
  (`_try_forward_launcher` returning True inside d²≤50 of an enemy core tile),
  and (b) an enemy builder actually thrown by one. **LOKI-2 is the cautionary
  case: it delivered ONE turret when its recipe called for three, and nobody
  checked before the battery.** Bar: **≥1 forward launcher in ≥50% of games and
  ≥1 enemy-builder throw from a forward launcher in ≥30%.** Below that the
  battery measures nothing and I re-aim the placement gates instead of reading
  a null.

S5_unrated: **the unrated leg is the conversion probe, per Magnus's standing
  directive 2026-08-09 — "test theories using unrated games between ladder
  games."** Research labelled the kidnap conversion NEEDS PROBE precisely
  because no corpus geometry can answer it. **Opponent choice is HELD OPEN**
  pending a per-opponent collar-heal staffing number (side lane commissioned
  it): healer-exile is untestable against an opponent that staffs ~zero collar
  healers, and an outcome null there would not separate "denial fails" from
  "nothing to deny". If Ouroboros staffs ~0, the discriminating opponent is CAD
  and an Ouroboros leg tests only the ray bonus + rush carry-over.

## THE HONEST PRICE OF THIS PLANK, STATED BEFORE ANY NUMBERS EXIST

**The brief was "throw an enemy builder onto our own gunner's ray." Two free
checks reshaped it before a line was written, and both are on the record:**

- **CODE FACT** — our turrets already fire at enemy builder bots (`main.py:660`
  gunner; sentinel priority map `main.py:687`, `BUILDER_BOT` prio 3). The
  our-side half of the conversion needed no new code and carries no behavioural
  bet on either team. That half of the brief survives intact.
- **SPEC ARITHMETIC** — free, unconfoundable. Gunner 7 dmg / 4 ammo / reload 1 →
  **6 shots, ~11 rounds** for a 40 HP builder. Sentinel 18 dmg / 10 ammo /
  reload 2 → **3 shots, ~7 rounds**. A thrown builder whose move cooldown is
  clear steps off the ray in **ONE round**. **So kidnap-into-our-ray is worth
  ~7–18 HP per throw unless the target is pinned — harassment arithmetic, not a
  kill.** s22 refuted imprisonment, so pinning is not re-opened.

**⇒ The ray bonus is a bonus. The plank rests on DISPLACEMENT of the heal line**
— research's own §7 ranked PLACEMENT first, and LOKI-1's collar doctrine says
the heal line is why cores survive (raw hits-to-kill 28 → 1206 for a stable
500–512 net, across 14 decoded games).

**THE ONE NUMBER THAT COULD STILL OVERTURN THIS SHAPE** is out with research:
how many rounds a thrown builder remains on its landing tile. If the modal
answer is "leaves next round", the ray bonus is confirmed decorative and the
plank is pure displacement. If it dwells 3+ rounds, the ray bonus is a kill
term and `LOKI_KIDNAP_RAY_BONUS` is underweighted at 36. **I am not waiting on
it to build, and I am not claiming either way until it lands.**

## CONFOUNDS, NAMED NOW SO THEY CANNOT BECOME EXCUSES LATER

- **Cost scale.** A launcher is +10% on every launcher after it and 20 Ti at
  base. Two forward launchers is real money taken from sentinels, which are the
  measured damage source (99.3% of 1,269 early core kills are turret fire).
  **A null could therefore be the plank crowding out the thing that works** —
  the flags-off control is what separates these, which is why it exists.
- **Opportunity ≠ conversion.** The 20.65% placement figure ignores action
  cooldown, the 20 Ti, and cost scale; research called it an upper bound. I am
  not entitled to expect 20.65% of anything.
- **The ray prefilter over-reports.** `get_attackable_tiles_from` ignores
  occupancy by contract, so for a gunner it reports through our own barriers —
  and the collar is made of barriers. `can_fire_from` is the confirming
  instrument, bounded to 6 calls/turn for the 10 ms budget.
- **CPU.** The launcher turn now does a set intersection plus up to 6
  `can_fire_from` calls. A TLE is silent degradation, not a crash. Watched.
- **Never measure under load.** LOKI-1's DESIGN records a retracted result from
  batteries run while another session used the same machine (48.3% → 62.2% on a
  clean box, same pairing). Battery runs alone.
