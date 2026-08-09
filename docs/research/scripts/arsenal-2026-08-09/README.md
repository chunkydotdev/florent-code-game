# Arsenal decoders (2026-08-09, session 24 research arm)

Preserved at wrap. Read-only over `replay_archive/` + `corpus/`.
Full results and method: `docs/research/loki-arsenal-pricing-2026-08-09.md`.

- `arsenal_decode.py` — the decoder. **Extends
  `../side-lane-2026-08-09/dwell_decode.py`** (board tracker, `ray()` geometry,
  map decode, Pool driver reused verbatim) with seven additions: both-team
  turret ray + live blocked gunner line; core-ring occupancy classified by
  occupant kind; map ore tiles + harvester sites; the kidnap-opportunity scan;
  observed-travel milestones; `distributeResources` interception geometry keyed
  on enemy FIRST-arrival time; live unit count for the 50-unit cap.
  **1,355 files, 0 errors, 34 s at NPROC=10.**
  Emits `ars_{ring,spawn,stile,kid,ore,map,trav,flow,val,haz}.tsv`.
  `ars_haz.tsv` is the per-round hazard panel and is **right-censored**: a round
  contributes to horizon H only when the outcome is observable within H. Do not
  recompute a hazard from the raw series without that, or the last H rounds of
  every replay silently score as survivals.

      NPROC=10 .venv/bin/python arsenal_decode.py OUTDIR corpus/join.tsv

- `validate.py` — the ten checks in the doc's §0.3. Run it before trusting any
  column. Two of them are exact identities against independent corpus streams
  (`econ.ti_collected_end`, `build_agg`), and one — the launcher pickup/throw
  geometry — validated 31,569/31,569.
- `analyse.py`, `analyse2.py` — the tables in the doc.
- `analyse3.py` — the §1.3 time-conditioned re-cut (achievement-round
  conditioning, round-matched control, per-round right-censored hazard) and the
  §5.1 phase-controlled spawn table. **Read this one before citing §1.3:** the
  original §1.3 comparison was uncontrolled and its verdict is withdrawn in the
  doc.
- `diag.py` — the single-file probe that found the V7 root cause (titanium is
  credited to the core's OWNER, whichever team's conveyor pushed it).

TRAPS: the four in `docs/research/corpus-howto.md` all bind. One more found
here — **the throw detector fires on Chebyshev > 1, so a throw landing on a
DIAGONALLY adjacent tile is missed** (76 of 31,645, 0.24%; `replay_throws.py`
catches those). Freeze `corpus/*.tsv` before a run: the keeper appends live.
