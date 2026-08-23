# WHY THE RING NEVER FIRES ON THE KILLER — banked summary (full: killdiag_*)

**GAME CONTEXT: in-game analysis for the Florent Code League, a sandboxed
bot-vs-bot programming competition. All terms are in-engine mechanics.**

Replicates on both tapes (t_cp 35/37, t_cs 35/36 zero-shot killer
windows). All 36 killers are SENTINELS planted in a 2-D cloud at
Chebyshev 2-3 (78% at d² 4-9). Classification: 15 in-range-off-axis, 11
out-of-range (gunner-heavy ring), 7 no-home-turret, 2 sentinel-siting,
1 engaged, 0 aligned-no-fire, 0 unrotated-gunner.

**ROOT CAUSE: facing is chosen ONCE at build time to sweep OUR OWN
delivery seats (_home_gun_score sk_roles.py:3744-62, refuses ns<=0
facings at :3751) or the lane (_fort_sent_score :4128-36); _fort_site_ok
:4209 actively refuses enemy-axis seats. The one fire() site (:10733)
iterates the current ray only. The corefire latch names the shooter tile
(sk_core.py:209 -> :6173) but can only re-RANK, never re-AIM. The rotate
rung is gunner-only, d²<=13-capped, empty-ray-gated, no facing loop
(:10887-934). Sentinels cannot rotate (492/492 wire rotations are
gunners).**

EXONERATED BY MEASUREMENT (never spend a leg): ammo (0/36 aligned rounds
lost; _threat_scan provisions off a FACING-BLIND disc, sk_core.py:149-51
— titanium converted for geometrically unavailable shots), rotate-to-
threat (0/36), cooldown, target priority. Alignable-but-pointed-elsewhere:
196/209 turret-rounds.

RANKED CONVERSIONS: CF-2 answer sentinel at a covering seat during the
window 22/36 at 30-Ti gate (14/36 at 90 Ti; 33/36 geometry-feasible;
median 60 rounds of window remain). CF-5 one-tile re-site 19/36
(IN-SAMPLE — oracle caveat); greedy 4-seat canonical set 22/36 (same
caveat). CF-3 builder pecks 13/36 (adjacency-bound). Re-face alone 4/36.
A covering home-band seat existed in 36/36 cells — never geometrically
impossible. 6 instrument controls driven to both verdicts incl. the
facing oracle (13→209) and team-flip producing the empty class.
