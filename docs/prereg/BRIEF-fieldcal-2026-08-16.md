# BUILDER COMMISSIONING BRIEF — live unrated leg, 2026-08-16 (s45)

AUTHORISATION: Magnus, in-session today: "You're free to use the unrated games"
(given in answer to the builder's go/no-go on the leg described below). Standing
platform rule: unrated is free, 5 test/unrated matches per 20 minutes.

## THE QUESTION THE LEG ANSWERS
Local screens (self-play vs `bots/_v223sealrepair` = v140) drive every decision,
including Magnus's slot bar (measure >=60.0% +-2pp vs v140, 60 mid-span). Nothing
links local units to the field. This leg calibrates that link on the KILL-TIME
axis and gives descriptive-only field win-share data.

## DESIGN CONSTANTS (settled, do not re-open; argue only what is marked open)
- Two arms, each holding the platform slot during its window (displaces teammate
  x3r0's v152; authorised above; submits inside observed pairing gaps, offset
  re-derived from recent `fcode match list` rows at fire time, never hardcoded;
  tools/submit_clean.py without --activate... NOTE: the leg arm must BE active,
  so submit_clean is used per its holder-restore contract).
- ARM A (field baseline): bots/_v223sealrepair (v140).
- ARM B (treatment): OPEN FOR THE DRAFTER TO ARGUE, two candidates only:
  bots/_v280mix4 (MIX280mix4, board leader 55.24% +-1.33 vs v140) or
  bots/_v267awrlnch (AWRLNCH, 53.95%, and on unbiased ITT RMST_300 the FASTER
  arm: -6.43 rounds [-8.88,-3.99] vs MIX280's -0.87 [-3.18,+1.43]).
- PRIMARY: ITT RMST at horizon 300 (mean; censor at 300; ALL games, a non-kill
  scores 300). The ITT MEDIAN pins at the horizon (only ~39% of games kill
  inside) so the mean is the estimator, stated explicitly.
- Sizing: +-20 rounds at 80% power: ~250 games/arm on rated-tape constants
  (sd 74.59, DEFF 1.145 measured), x1.199 unrated projection => "~300 games/arm
  (PLANNING value, unrated DEFF ASSUMED)" — the leg RE-MEASURES DEFF on its own
  games and the banked interval uses the re-measured value. ~4h/arm at the
  75/h cap.
- REPORT the estimator TRIPLE (ITT timely-kill rate, rate factor, speed factor)
  plus the kill-win-conditioned median — the factorisation identity
  RMST = H - P(kill<=H)*E[H-T|kill<=H] is exact; both decompositions reported.
- WIN SHARE IS DESCRIPTIVE ONLY and the prereg must label it unresolvable at
  this n (powering 3.7pp vs field needs ~5,258 games/arm; nobody is buying that).
- Opponent handling: matched pairs across arms — same opponent list both arms,
  PINNED per docs/research/SPEC-opponent-pinning-2026-08-13.md (treatment legs
  pin; `fcode match unrated <team> --match <past_match_id>` plays their pinned
  version). Opponent list comes from research's fire order (live `fcode team
  search` reads, never target_value's cached column).
- TARGET BAND line per the standing gate (tools/target_value.py output quoted;
  for an unrated calibration leg the payout is informational, the line is still
  mandatory).
- Rated exposure during windows: ~2.6-3.1 rated matches/hour played by the
  active arm; priced at roughly -8 Elo per adverse leaked match historically;
  windows split to keep each short.

## KNOWN HAZARDS THE PREREG MUST CARRY (each cost us once already)
- Platform replays STRIP stdout: arms are read from ENGINE-SIDE facts only.
- `fcode submit` AUTO-ACTIVATES: the submit IS the activation; fire only inside
  an observed pairing gap; submit_clean restores the holder and verifies on the
  `Active bot:` line, never the exit code.
- The archive lags: absence in ladder_games/meta_join is not evidence.
- 5-per-20-min window: the runner must wait out the window and retry the SAME
  cell, rotating starting cells (tools/panel2_cal.sh pattern, NOT fanout.sh).
- Unrated DEFF 1.833/1.434 (games not independent); use the two-fixture
  half-width form for any local-vs-field comparison.
- MIX horizon sensitivity (declared by research): mildly slower at H=250,
  faster at H=400 — H=300 is the registered horizon (bar re-priced to r300 by
  Magnus today), no post-hoc horizon shopping.

## NAMED INPUT FILES (the PROVENANCE line lists exactly these plus this brief)
- PROGRAMME.md (current: bar re-priced to r300, slot rule, precision reading)
- docs/research/PREREG-amendments-and-lock-obligations-2026-08-09.md (template + OBs)
- docs/research/SPEC-opponent-pinning-2026-08-13.md
- docs/research/KILL-HAZARD-REDERIVED-2026-08-16.md
- docs/builder-method.md (S0-S8)
- this brief (scratchpad copy; the numbers above attributed to research's
  in-channel RMST relay of 2026-08-16 ~05:5xZ, side-lane audit pending — the
  prereg must carry that pending-audit flag on any number it inherits from it)
