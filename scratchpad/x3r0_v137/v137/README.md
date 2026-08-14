# Candidate v136: isolated-module map hybrid (not deployed)

Uses benchmark v135 on the general official pool and the former v134 policy on
four configured layouts: drumlin, nordkap, glacierkeep, and yulerune.
Selection is based only on exact terrain, never opponent identity.

Both policies live under unique module names (`b_*` and `c_*`). This avoids
cross-bot module-name collisions in the engine's shared-GIL subinterpreters;
the installed SDK explicitly warns that Python method pollution can cross
subinterpreter boundaries. The wrapper also delays policy-object construction
until the first unit turn.

## Evidence

- vs deployed benchmark v135: **208-152 (57.8%)**, n=360, fresh official-map
  seeds and balanced colors.
- Color split: **109-71 as A**, **99-81 as B**.
- Transfer screen: **103-77 (57.2%)**, n=180:
  - vs v134 champion: 37-23 (61.7%)
  - vs v125 Loki: 34-26 (56.7%)
  - vs rc8.4/v130: 32-28 (53.3%)
- Routed-map aggregate in the v135 comparison: drumlin 14-10,
  glacierkeep 15-9, yulerune 14-10.
- Nordkap routing was neutral in a dedicated 80-game A/B (40-40); removing
  its configured key did not improve the policy, so the confirmed source is
  retained unchanged.

Do not submit or activate without explicit user approval.
