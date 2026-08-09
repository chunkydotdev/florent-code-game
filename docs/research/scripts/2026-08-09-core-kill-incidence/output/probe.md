## A. MAP stratification (5th confounder, not in the pre-registered family)

15 distinct maps; meander=110, snowflake=106, antler=105, archipelago=103, heart=103, saga=101, drumlin=99, atoll=99, nordkap=97, moonrise=95, lighthouse=95, hive=87

| feature | AUC (strata=map) | z | p |
| --- | ---: | ---: | ---: |
| `THEM_ti_collected_end_w50` [THEM] titanium collected by r50 | 0.314 | -11.52 | 0.00e+00 |
| `THEM_b_harvester_w50` [THEM] harvesters built r0-50 | 0.308 | -12.03 | 0.00e+00 |
| `THEM_b_conveyor_w50` [THEM] conveyors built r0-50 | 0.356 | -8.84 | 0.00e+00 |
| `THEM_ti_end_w50` [THEM] titanium banked at r50 | 0.391 | -6.63 | 3.35e-11 |
| `US_shot_w50` [US] turret shots fired r0-50 | 0.662 | +9.89 | 0.00e+00 |
| `US_ammo_converted_w50` [US] titanium converted to ammo r0-50 | 0.666 | +10.13 | 0.00e+00 |

## B. REDUNDANCY -- one latent or two?

Spearman-style rank correlation between the two constructs, whole population:

| a | b | rank corr |
| --- | --- | ---: |
| `THEM_ti_collected_end_w50` | `THEM_ti_end_w50` | +0.497 |
| `THEM_ti_collected_end_w50` | `US_shot_w50` | +0.029 |
| `THEM_ti_collected_end_w50` | `US_ammo_converted_w50` | -0.017 |
| `THEM_b_harvester_w50` | `THEM_ti_collected_end_w50` | +0.809 |
| `THEM_b_harvester_w50` | `THEM_ti_end_w50` | +0.477 |
| `THEM_b_harvester_w50` | `US_shot_w50` | -0.086 |
| `THEM_b_harvester_w50` | `US_ammo_converted_w50` | -0.110 |
| `THEM_b_conveyor_w50` | `THEM_ti_collected_end_w50` | +0.645 |
| `THEM_b_conveyor_w50` | `THEM_b_harvester_w50` | +0.740 |
| `THEM_b_conveyor_w50` | `THEM_ti_end_w50` | +0.416 |
| `THEM_b_conveyor_w50` | `US_shot_w50` | -0.125 |
| `THEM_b_conveyor_w50` | `US_ammo_converted_w50` | -0.117 |
| `THEM_ti_end_w50` | `US_shot_w50` | -0.128 |
| `THEM_ti_end_w50` | `US_ammo_converted_w50` | -0.121 |
| `US_ammo_converted_w50` | `US_shot_w50` | +0.870 |

CONDITIONAL: does each survive inside tertiles of the other construct?
(strata = opponent x tertile of the conditioning variable)

| tested feature | conditioned on | AUC | z | p |
| --- | --- | ---: | ---: | ---: |
| `US_shot_w50` | `THEM_ti_collected_end_w50` tertile x opp | 0.638 | +6.53 | 6.73e-11 |
| `THEM_ti_collected_end_w50` | `US_shot_w50` tertile x opp | 0.314 | -8.99 | 0.00e+00 |
| `US_ammo_converted_w50` | `US_shot_w50` tertile x opp | 0.568 | +3.26 | 1.11e-03 |
| `US_shot_w50` | `US_ammo_converted_w50` tertile x opp | 0.549 | +2.35 | 1.88e-02 |
| `THEM_b_harvester_w50` | `US_shot_w50` tertile x opp | 0.365 | -6.78 | 1.23e-11 |
| `US_shot_w50` | `THEM_b_harvester_w50` tertile x opp | 0.623 | +5.80 | 6.46e-09 |

## C. THE ACTIONABLE 2x2 -- core-kill incidence by quadrant

Split at the population medians: US shots by r50 = 10, THEIR titanium collected by r50 = 170.

| our shots r0-50 | their Ti collected by r50 | n | core-kill wins | incidence |
| --- | --- | ---: | ---: | ---: |
| <=10 | <=170 | 447 | 138 | **30.9%** |
| <=10 | >170 | 338 | 47 | **13.9%** |
| >10 | <=170 | 326 | 186 | **57.1%** |
| >10 | >170 | 333 | 108 | **32.4%** |

And as a single ordered signal -- rank(US shots) - rank(their Ti collected):

| composite quintile | n | core-kill wins | incidence | median kill round |
| --- | ---: | ---: | ---: | ---: |
| Q1 (least violent) | 288 | 33 | **11.5%** | 284 |
| Q2  | 289 | 60 | **20.8%** | 185 |
| Q3  | 289 | 84 | **29.1%** | 182 |
| Q4  | 289 | 123 | **42.6%** | 147 |
| Q5 (most violent) | 289 | 179 | **61.9%** | 117 |

## D. WHEN DOES THE SIGNAL EXIST? (same features at earlier windows)

| feature | AUC w25 | AUC w50 | AUC w75 | AUC w100 |
| --- | ---: | ---: | ---: | ---: |
| `THEM_ti_collected_end` [THEM] titanium collected by r50 | 0.353 | 0.331 | 0.316 | 0.292 |
| `THEM_b_harvester` [THEM] harvesters built r0-50 | 0.375 | 0.362 | 0.341 | 0.340 |
| `THEM_b_conveyor` [THEM] conveyors built r0-50 | 0.409 | 0.393 | 0.372 | 0.376 |
| `THEM_ti_end` [THEM] titanium banked at r50 | 0.486 | 0.395 | 0.357 | 0.337 |
| `US_shot` [US] turret shots fired r0-50 | 0.574 | 0.636 | 0.666 | 0.685 |
| `US_ammo_converted` [US] titanium converted to ammo r0-50 | 0.569 | 0.628 | 0.655 | 0.672 |

(w75 and w100 are CENSORED -- games that ended before the window closes are dropped, which preferentially removes fast kills. Read the trend, not the level.)

## E. RUNTIME READABILITY of the enemy-economy signal

Where do their r0-50 harvesters and conveyors actually sit, relative to THEIR OWN core? A scout builder bot has vision r^2=20; our core has r^2=36 but cannot move. So the question is how deep a scout must go.

| their building (r0-50) | n | median d2 to their core | share within d2<=20 | within d2<=36 | within d2<=64 |
| --- | ---: | ---: | ---: | ---: | ---: |
| harvester | 4275 | 25 | 43.6% | 73.8% | 88.2% |
| conveyor | 16227 | 13 | 70.1% | 83.7% | 94.3% |

## F. OUROBOROS CELL -- UNDERPOWERED, reported not concluded from

n=105 archived joined games alive at r50, 5 core-kill wins (4.8%).

| feature | mean in kill games | mean in non-kill | median kill | median non-kill | unstratified Mann-Whitney p |
| --- | ---: | ---: | ---: | ---: | ---: |
| `THEM_ti_collected_end_w50` [THEM] titanium collected by r50 | 170.0 | 274.7 | 90.0 | 240.0 | 0.178 |
| `THEM_b_harvester_w50` [THEM] harvesters built r0-50 | 2.4 | 4.7 | 2.0 | 5.0 | 0.041 |
| `THEM_b_conveyor_w50` [THEM] conveyors built r0-50 | 10.0 | 17.1 | 12.0 | 17.5 | 0.031 |
| `THEM_ti_end_w50` [THEM] titanium banked at r50 | 29.4 | 78.2 | 5.0 | 57.5 | 0.057 |
| `US_shot_w50` [US] turret shots fired r0-50 | 13.2 | 9.5 | 15.0 | 8.0 | 0.074 |
| `US_ammo_converted_w50` [US] titanium converted to ammo r0-50 | 136.6 | 101.8 | 135.0 | 96.0 | 0.071 |

## G. OPPONENT HOLDOUT -- is the discriminator opponent-fitted?

Half A = 17 opponents, half B = 16, split by alternating corpus size so both halves span the rating range.

| feature | AUC half A | n A | AUC half B | n B |
| --- | ---: | ---: | ---: | ---: |
| `THEM_ti_collected_end_w50` [THEM] titanium collected by r50 | 0.355 | 744 | 0.309 | 655 |
| `THEM_b_harvester_w50` [THEM] harvesters built r0-50 | 0.392 | 744 | 0.334 | 655 |
| `THEM_b_conveyor_w50` [THEM] conveyors built r0-50 | 0.382 | 744 | 0.403 | 655 |
| `THEM_ti_end_w50` [THEM] titanium banked at r50 | 0.424 | 744 | 0.367 | 655 |
| `US_shot_w50` [US] turret shots fired r0-50 | 0.649 | 744 | 0.624 | 655 |
| `US_ammo_converted_w50` [US] titanium converted to ammo r0-50 | 0.634 | 744 | 0.622 | 655 |

## H. DOES THE SIGNAL PREDICT SPEED TOO, OR ONLY INCIDENCE?

Among core-kill wins ONLY, is the kill faster when the signal is stronger?

| feature | rank corr with kill round (kills only, n=479) |
| --- | ---: |
| `THEM_ti_collected_end_w50` [THEM] titanium collected by r50 | -0.092 |
| `THEM_b_harvester_w50` [THEM] harvesters built r0-50 | -0.035 |
| `THEM_b_conveyor_w50` [THEM] conveyors built r0-50 | -0.011 |
| `THEM_ti_end_w50` [THEM] titanium banked at r50 | +0.078 |
| `US_shot_w50` [US] turret shots fired r0-50 | -0.457 |
| `US_ammo_converted_w50` [US] titanium converted to ammo r0-50 | -0.449 |
