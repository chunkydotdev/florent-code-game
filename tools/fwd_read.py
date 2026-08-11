#!/usr/bin/env python3
"""FORWARD EFFICIENCY READ-OUT — the numerator, the denominator, and the guard.

WHY THIS EXISTS, AND WHY IT IS NOT A ONE-LINER
----------------------------------------------
`QUEUE-forward-efficiency-2026-08-11.md:93-94` said the read-out "needs no new
decoder and the builder's 64-game self-play harness can compute both". **That is
false and both arms found it independently on 2026-08-11 (s31):**

  * `tools/arena.py:53` runs every match with `--replay /dev/null`. `h2h.sh` is
    downstream of it and parses only the engine's `Winner:` line. **h2h/arena can
    emit win rate and score.py. Zero forward quantities.**
  * `tools/mech_battery.py` DOES keep replays, but its decoder reads builder-bot
    deaths by round band and spawns only — **no position tracking at all**, and
    `removeEntity` carries an id and nothing else, so even a DEATH cannot be
    classified forward without a move-event pass.

So the quantities the primary bar is denominated in were not obtainable from any
local battery. This is the assembly: `scratchpad/dwell.py::walk()`'s core-read
and position tracking, plus `tools/corpus/replay_events.py`'s build/death
classification, in one decoder that runs on a LOCAL `fcode run --replay` file.

THE THREE TRAPS THIS DECODER PAYS FOR (all previously paid for elsewhere)
------------------------------------------------------------------------
1. **`rotate()` RE-EMITS `placeEntity` FOR AN EXISTING id.** Only the FIRST
   placement of an id is a build. Without this the forward-build DENOMINATOR
   inflates ~3x on gunners — and this bar's whole design is that the denominator
   is protected, so an inflated denominator silently PASSES a plank that should
   fail. Guarded by the `e.id not in seen` test.
2. **`removeEntity` CARRIES AN id ONLY.** A death is classified forward from the
   entity's LAST TRACKED position, which requires consuming `unum==2` move
   events. A decoder that skips moves classifies every builder death at its
   SPAWN tile — i.e. always at home, i.e. zero forward deaths.
3. **THE MAP BUFFER HOLDS BOTH CORES** (field 4 -> team, pos). "Forward" is
   `d2(pos, enemy_core) < d2(pos, own_core)`, evaluated per team, so both sides
   of one game are measured against their OWN geometry.

DEFINITIONS — identical to the ones the 4.57x headline was computed under
------------------------------------------------------------------------
  forward build   first placeEntity for an id, kind != builder_bot, forward.
                  (Mixes turrets with conveyors — the same definitional caveat
                  LOKI-25's read-out carried. Kept deliberately: changing it here
                  would make this run incomparable with the corpus figure.)
  forward death   removeEntity of a builder_bot whose last tracked position is
                  forward.
  forward round   a living builder_bot standing forward at end of round.

  PRIMARY BAR         deaths per forward build = fwd_deaths / fwd_builds,
                      POOLED (sum/sum), game-resampled bootstrap.
  PROTECTED DENOM     forward builds/game must NOT fall. LOKI-25 died buying its
                      numerator: deaths -24%, presence -23%, ratio flat -2.3%.
                      **A ratio improvement with a fallen denominator is a FAIL,
                      not a pass** — that is the entire design contribution.

Usage:
  fwd_read.py --selftest
  fwd_read.py decode  OUT.tsv  replay1.replay26 [replay2 ...]
  fwd_read.py analyse GAMES.tsv --treat-team 0     # pooled ratio + bootstrap
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------
# decode
# --------------------------------------------------------------------------
def _cores_and_turns(data):
    """Map buffer -> {team: core_pos}; plus the per-round turn buffers."""
    mapbuf, turns = None, []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mapbuf = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    if mapbuf is None:
        return None, []
    cores = []
    for n, w, v in fields(mapbuf):
        if n == 4 and w == WIRE_LEN:
            d = {a: b for a, _c, b in fields(v)}
            if 3 in d:
                cores.append((d.get(2, 0), read_pos(d[3])))
    if len(cores) != 2:
        return None, []
    return {t: p for t, p in cores}, turns


def _d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def walk(path, home=None):
    """Decode one replay. Returns {team: {...counts...}} or None.

    `home` overrides the core positions — used ONLY by the selftest's mutation
    cell, where swapping the cores MUST change the answer.
    """
    data = Path(path).read_bytes()
    parsed_home, turns = _cores_and_turns(data)
    if parsed_home is None:
        return None
    if home is None:
        home = parsed_home

    pos, team, kind = {}, {}, {}
    seen = set()                       # TRAP 1: ids ever placed
    out = {t: {"fwd_builds": 0, "fwd_deaths": 0, "fwd_rounds": 0,
               "all_builds": 0, "all_deaths": 0, "rounds": 0} for t in home}

    def forward(p, t):
        return _d2(p, home[1 - t]) < _d2(p, home[t])

    for rnd, tb in enumerate(turns):
        for _a, _b, ub in fields(tb):
            for un, _w, ubuf in fields(ub):
                if un == 1:                                   # placeEntity
                    for en, _e, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        first = e.id not in seen              # TRAP 1
                        seen.add(e.id)
                        pos[e.id], team[e.id], kind[e.id] = e.pos, e.team, e.kind
                        if first and e.team in out:
                            out[e.team]["all_builds"] += 1
                            if e.kind != "builder_bot" and forward(e.pos, e.team):
                                out[e.team]["fwd_builds"] += 1
                elif un == 2:                                 # TRAP 2: moves
                    d = {k: v for k, _x, v in fields(ubuf)}
                    if 1 in d and 2 in d and d[1] in pos:
                        pos[d[1]] = read_pos(d[2])
                elif un == 3:                                 # removeEntity
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos:
                            continue
                        p, t, k = pos.pop(rv), team.pop(rv, None), kind.pop(rv, None)
                        if t not in out:
                            continue
                        out[t]["all_deaths"] += 1
                        if k == "builder_bot" and forward(p, t):
                            out[t]["fwd_deaths"] += 1
        for eid, p in pos.items():
            t = team.get(eid)
            if kind.get(eid) == "builder_bot" and t in out:
                out[t]["rounds"] += 1
                if forward(p, t):
                    out[t]["fwd_rounds"] += 1
    return out


COLS = ("fwd_builds", "fwd_deaths", "fwd_rounds", "all_builds", "all_deaths", "rounds")


def cmd_decode(argv):
    outp, files = argv[0], argv[1:]
    with open(outp, "w") as fh:
        fh.write("file\tteam\t" + "\t".join(COLS) + "\n")
        bad = 0
        for i, f in enumerate(files):
            try:
                r = walk(f)
            except Exception as exc:                          # noqa: BLE001
                print(f"ERR {f}: {exc}", file=sys.stderr)
                bad += 1
                continue
            if r is None:
                bad += 1
                continue
            for t in sorted(r):
                fh.write(f"{Path(f).name}\t{t}\t"
                         + "\t".join(str(r[t][c]) for c in COLS) + "\n")
            if (i + 1) % 200 == 0:
                print(f"  ...{i+1}/{len(files)} ({bad} bad)", file=sys.stderr, flush=True)
    print(f"decoded {len(files)-bad}/{len(files)} -> {outp}", file=sys.stderr)


# --------------------------------------------------------------------------
# analyse — pooled ratio, game-resampled bootstrap, protected denominator
# --------------------------------------------------------------------------
def _pooled(games):
    b = sum(g["fwd_builds"] for g in games)
    d = sum(g["fwd_deaths"] for g in games)
    return (d / b) if b else float("nan")


def bootstrap(games, reps=2000, seed=17):
    """GAME-resampled: the resampling unit is the GAME, not the build.

    A build-resampled interval would understate the SE because builds within a
    game are correlated. Named here because `PROGRAMME.md` D1 requires the
    aggregation and the resampling unit in the same sentence as the bar.
    """
    rng = random.Random(seed)
    n = len(games)
    if n == 0:
        return float("nan"), float("nan")
    out = []
    for _ in range(reps):
        s = [games[rng.randrange(n)] for _ in range(n)]
        v = _pooled(s)
        if v == v:
            out.append(v)
    if not out:
        return float("nan"), float("nan")
    out.sort()
    mean = sum(out) / len(out)
    sd = (sum((x - mean) ** 2 for x in out) / max(len(out) - 1, 1)) ** 0.5
    return sd, out[int(0.025 * len(out))], out[int(0.975 * len(out))]


def verdict(treat, ctrl):
    """THE ONE DEFINITION. Both the report and the selftest call THIS.

    ⛔ IT WAS DUPLICATED. Until 2026-08-11 the selftest carried its own `_verdict`
    whose PASS rule was `dr < 0` — ANY improvement passes, no threshold — while
    production required `dr < -2*se`, and the selftest's copy had NO
    NO-INFORMATION branch at all. The denominator cells therefore validated the
    COPY: breaking production's threshold logic left the selftest green.

    **AND THE DUPLICATION WAS INVISIBLE BECAUSE THE FIXTURE WAS DEGENERATE.**
    The synthetic games were identical, so per-game sd = 0, so se = 0, so
    `dr < -2*se` DEGENERATED TO `dr < 0` — the two implementations coincided on
    the only fixture that ever exercised them and diverged everywhere else.
    A fixture degenerate enough that two different definitions agree cannot
    distinguish them, and no amount of making the cells stricter would have
    caught it. (Side lane, s31 — same signature as `ring_retention`.)

    ⛔ THE DENOMINATOR GATE IS SIZED. It used to be a bare `db < 0`.
    **On two arms drawn from the SAME distribution that fires about half the
    time** — caught 2026-08-11 by the NO-INFORMATION cell the moment the fixture
    stopped being degenerate. An unsized gate on a noisy statistic is a coin
    flip, and this one's coin flip lands on "kill the plank". That is obligation
    12 ("a gate is a bar and must be sized like one") failing inside the tool
    built to enforce the protected denominator.

    **The conservative default is PRESERVED, not traded away:** a denominator
    that cannot be resolved does NOT return a clean PASS. It returns
    `PASS-DENOM-UNRESOLVED`, which is not shippable — it means buy more n.
    """
    import statistics
    n_t, n_c = len(treat), len(ctrl)
    if not n_t or not n_c:
        return "NO-INFORMATION"
    dr = _pooled(treat) - _pooled(ctrl)
    bt = [g["fwd_builds"] for g in treat]
    bc = [g["fwd_builds"] for g in ctrl]
    db = sum(bt) / n_t - sum(bc) / n_c
    se_db = ((statistics.pvariance(bt) / n_t + statistics.pvariance(bc) / n_c)
             ** 0.5) if n_t > 1 and n_c > 1 else 0.0
    se = (bootstrap(treat)[0] ** 2 + bootstrap(ctrl)[0] ** 2) ** 0.5

    if db < -2 * se_db:                      # a RESOLVED fall — LOKI-25's shape
        return "FAIL-DENOM"
    denom_ok = db >= 0 or db >= -2 * se_db   # held, or fall not resolved
    if dr < -2 * se:
        return "PASS" if db >= 0 else "PASS-DENOM-UNRESOLVED"
    if dr > 2 * se:
        return "FAIL-WORSE"
    return "NO-INFORMATION" if denom_ok else "FAIL-DENOM"


def cmd_analyse(argv):
    path = argv[0]
    treat = 0
    if "--treat-team" in argv:
        treat = int(argv[argv.index("--treat-team") + 1])
    rows = [l.split("\t") for l in Path(path).read_text().splitlines()[1:] if l.strip()]
    arms = {0: [], 1: []}
    for r in rows:
        t = int(r[1])
        arms[t].append({c: int(r[2 + i]) for i, c in enumerate(COLS)})
    print(f"\nFORWARD EFFICIENCY — {path}")
    print(f"  treatment team = {treat}   control team = {1-treat}\n")
    res = {}
    for t, label in ((treat, "TREAT"), (1 - treat, "CTRL")):
        g = arms[t]
        n = len(g)
        if not n:
            continue
        ratio = _pooled(g)
        sd, lo, hi = bootstrap(g)
        bpg = sum(x["fwd_builds"] for x in g) / n
        dpg = sum(x["fwd_deaths"] for x in g) / n
        rpg = sum(x["fwd_rounds"] for x in g) / n
        dwell = (sum(x["fwd_rounds"] for x in g) / sum(x["fwd_builds"] for x in g)
                 if sum(x["fwd_builds"] for x in g) else float("nan"))
        res[label] = dict(n=n, ratio=ratio, sd=sd, lo=lo, hi=hi, bpg=bpg, dpg=dpg,
                          rpg=rpg, dwell=dwell)
        print(f"  {label}  n={n} games")
        print(f"     forward builds/game        {bpg:8.2f}   <-- PROTECTED DENOMINATOR")
        print(f"     forward deaths/game        {dpg:8.2f}")
        print(f"     forward builder-rounds/gm  {rpg:8.1f}   (dwell/build {dwell:.1f})")
        print(f"     DEATHS PER FORWARD BUILD   {ratio:8.4f}   "
              f"bootstrap SE {sd:.4f}  95% [{lo:.4f}, {hi:.4f}]")
    if "TREAT" in res and "CTRL" in res:
        t, c = res["TREAT"], res["CTRL"]
        dr = t["ratio"] - c["ratio"]
        db = t["bpg"] - c["bpg"]
        se = (t["sd"] ** 2 + c["sd"] ** 2) ** 0.5
        print(f"\n  RATIO  treat - ctrl = {dr:+.4f}   (SE_diff {se:.4f}; "
              f"lower is better)")
        print(f"  DENOM  treat - ctrl = {db:+.2f} forward builds/game")
        print(f"  informative band: |ratio diff| >= {2*se:.4f}")
        # ⛔ ONE DEFINITION, called here and by the selftest. Never re-implemented.
        v = verdict(arms[treat], arms[1 - treat])
        if v == "FAIL-DENOM":
            print("\n  ⛔ PROTECTED DENOMINATOR BREACHED — forward builds/game FELL.")
            print("     A ratio improvement bought by going forward LESS is the "
                  "LOKI-25 failure mode.")
            print("  FWD_VERDICT: FAIL denominator-breach")
        elif v == "PASS":
            print("\n  FWD_VERDICT: PASS ratio improved, denominator held")
        elif v == "FAIL-WORSE":
            print("\n  FWD_VERDICT: FAIL ratio worsened")
        else:
            print("\n  FWD_VERDICT: NO-INFORMATION back to the pool, NOT demoted")
        # research asked for this FIRST, before trusting n=440/arm
        import statistics
        per = [g["fwd_deaths"] / g["fwd_builds"] for g in arms[treat] if g["fwd_builds"]]
        if len(per) > 1:
            print(f"\n  per-game ratio sd (self-play, empirical) = "
                  f"{statistics.pstdev(per):.4f} over {len(per)} games")
            print("     ^ compare to the LADDER-derived 0.4007 that set n=440/arm.")


# --------------------------------------------------------------------------
# selftest — every cell must be able to come out the other way
# --------------------------------------------------------------------------
def _events_census(path):
    """Independent path: the SHIPPED corpus decoder, used as the cross-check.

    Same file, two code paths, same numbers. This is the only inversion
    available for a decoder, and `mech_battery`'s decoder never had one.
    """
    import io
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "replay_events", ROOT / "tools" / "corpus" / "replay_events.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    buf = io.StringIO()
    mod.census(Path(path), buf)
    fb = {0: 0, 1: 0}
    fd = {0: 0, 1: 0}
    for line in buf.getvalue().splitlines():
        f = line.split("\t")
        ev, team, knd = f[1], int(f[3]), f[4]
        d2o, d2e = int(f[7]), int(f[8])
        if ev == "BUILD" and knd != "builder_bot" and d2e < d2o:
            fb[team] += 1
        elif ev == "DEATH" and knd == "builder_bot" and d2e < d2o:
            fd[team] += 1
    return fb, fd


def selftest():
    ok = True

    def cell(name, got, want, forced):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  [{'ok' if good else 'FAIL'}] {name:<46} got={got} want={want}")
        print(f"         forced by: {forced}")

    ar = ROOT / "replay_archive"
    reps = sorted(ar.glob("*.replay26"))[:6]
    if not reps:
        print("SELFTEST: no archived replays; cannot cross-check.")
        return False

    # CELL 1 — cross-check against the SHIPPED decoder on real files.
    agree = disagree = 0
    for p in reps:
        mine = walk(p)
        if mine is None:
            continue
        fb, fd = _events_census(p)
        for t in (0, 1):
            if mine[t]["fwd_builds"] == fb[t] and mine[t]["fwd_deaths"] == fd[t]:
                agree += 1
            else:
                disagree += 1
                print(f"         MISMATCH {p.name} team{t}: "
                      f"mine b={mine[t]['fwd_builds']} d={mine[t]['fwd_deaths']} "
                      f"vs events b={fb[t]} d={fd[t]}")
    cell("agrees with replay_events.py on real replays", disagree, 0,
         "two independent code paths on the same bytes must agree; "
         f"{agree} team-files compared")

    # CELL 2 — MUTATION. Swap the cores; forward/home invert, so the answer MUST
    # change. A classifier that ignored geometry would return the same numbers.
    p = reps[0]
    base = walk(p)
    home, _ = _cores_and_turns(Path(p).read_bytes())
    swapped = walk(p, home={0: home[1], 1: home[0]})
    changed = any(base[t]["fwd_builds"] != swapped[t]["fwd_builds"] for t in (0, 1))
    cell("swapping the cores CHANGES the forward counts", changed, True,
         "forward is defined by core geometry; if swapping cores changes "
         "nothing, the classifier is not reading geometry at all")

    # CELL 3 — the rotate() re-emit trap, BEHAVIOURALLY.
    # ⛔ WAS `"e.id not in seen" in src` — a GREP OF THE SOURCE TEXT. Renaming the
    # variable turned it red while the guard worked; writing the string in a
    # comment turned it green while the logic was broken. Checking that a rule is
    # CITED verifies nothing. Now: a twin without the guard must count MORE
    # forward builds on real replays.
    guarded = unguarded = 0
    for q in reps:
        g = walk(q)
        u = walk_norotguard(q)
        if g is None or u is None:
            continue
        guarded += sum(g[t]["fwd_builds"] for t in (0, 1))
        unguarded += sum(u[t] for t in (0, 1))
    cell("rotate re-emit INFLATES builds without the guard", unguarded > guarded,
         True,
         f"rotate() re-emits placeEntity; the unguarded twin must over-count the "
         f"PROTECTED DENOMINATOR ({guarded} guarded vs {unguarded} unguarded)")

    # CELL 4 — move events must be consumed, or every death reads as home.
    # ⛔ POOLED ACROSS THE SAMPLE, NOT reps[0]. First written against a single
    # replay, it FAILED on 2026-08-11 because that game had 0 forward deaths in
    # BOTH arms, so `0 < 0` was False. The decoder was correct; the CELL was
    # unable to distinguish "the guard is broken" from "this fixture cannot test
    # the guard". A cell must not fail for lack of a dose -- it must SAY so.
    base_fd = nomove_fd = 0
    for q in reps:
        bq = walk(q)
        if bq is None:
            continue
        base_fd += sum(bq[t]["fwd_deaths"] for t in (0, 1))
        nq = walk_nomoves(q)
        nomove_fd += sum(nq[t]["fwd_deaths"] for t in (0, 1))
    if base_fd == 0:
        print("  [SKIP] ignoring move events LOSES forward deaths — "
              "NO DOSE: 0 forward deaths in the whole sample, cell cannot resolve")
        ok = False                       # an unresolvable cell is not a pass
    else:
        cell("ignoring move events LOSES forward deaths", nomove_fd < base_fd, True,
             f"removeEntity carries an id only; without the move pass a builder "
             f"dies at its spawn tile, i.e. never forward "
             f"({base_fd} forward deaths with the move pass, {nomove_fd} without)")

    # ⛔ CELLS 5-8 ALL CALL PRODUCTION `verdict()`. They used to call a test-only
    # `_verdict` copy whose PASS rule was `dr < 0` (any improvement passes, no
    # threshold) and which had NO NO-INFORMATION branch — so breaking production
    # left the selftest green. Side lane, s31.

    # CELL 5 — the denominator guard must FIRE. "A guard that has only ever seen
    # builds/game hold is a guard nobody has watched refuse."
    cell("denominator guard FIRES on a fallen denominator",
         verdict(_synth(200, 10, 1, seed=1), _synth(200, 14, 2, seed=2)),
         "FAIL-DENOM",
         "LOKI-25's exact signature (ratio improves 0.143->0.100 while forward "
         "builds fall 14->10) must produce FAIL, not PASS")

    # CELL 6 — and it must NOT fire when the denominator holds.
    cell("denominator guard SILENT when denominator holds",
         verdict(_synth(400, 20, 1, spread=2, seed=3),
                 _synth(400, 14, 3, spread=2, seed=4)) in ("PASS", "NO-INFORMATION"),
         True,
         "a guard that fires on everything is not a guard")

    # ⭐ CELL 7 — THE NO-INFORMATION BRANCH, TESTED AS A RATE, NOT ON ONE DRAW.
    # It is the D61 fix, it is the reason this tool is a generator rather than
    # another filter, and until now NOTHING DROVE IT: the string appeared exactly
    # once in the file, in production.
    #
    # ⛔ FIRST WRITTEN AS A SINGLE SEED PAIR AND IT FAILED — on a draw with
    # db = -0.950 against a 2*se_db of 0.944, a genuine ~5% tail event. **A one
    # -draw cell cannot distinguish "the tool manufactures verdicts" from "this
    # pair was unlucky", which is the same defect as cell 4's reps[0].** The
    # property under test is a RATE, so the cell measures the rate.
    #
    # THIS CELL IS WHAT CAUGHT THE PRODUCTION DEFECT, AND IT WAS DRIVEN TO THE
    # OTHER VERDICT RATHER THAN ASSUMED TO BE STRICT. MEASURED, both oracles on
    # the same 120 null pairs:
    #     old test-copy `_verdict` (no NO-INFORMATION branch)  120/120 = 100%
    #     sized production gate                                 13/120 =  10.8%
    # The bare `db < 0` gate ALONE reads ~50% (two null arms differ in the wrong
    # direction half the time); the 100% is that gate plus the missing branch.
    # Threshold is 20%, so the old oracle FAILS this cell loudly.
    fp = 0
    TRIALS = 120
    for k in range(TRIALS):
        v = verdict(_synth(60, 14, 2, spread=4, seed=1000 + 2 * k),
                    _synth(60, 14, 2, spread=4, seed=1001 + 2 * k))
        if v != "NO-INFORMATION":
            fp += 1
    rate = fp / TRIALS
    cell("null pairs return NO-INFORMATION at ~the nominal rate", rate <= 0.20,
         True,
         f"two arms from the SAME distribution must land inside the band except "
         f"at the nominal tail rate; measured {fp}/{TRIALS} = {rate:.1%} "
         f"(an UNSIZED denominator gate reads ~50% here)")

    # CELL 8 — and the other side of the same boundary: a LARGE ratio move with
    # the denominator held must NOT be filed as NO-INFORMATION.
    big = verdict(_synth(400, 20, 0, spread=2, seed=13),
                  _synth(400, 14, 6, spread=2, seed=14))
    cell("a large improvement is NOT filed as NO-INFORMATION", big, "PASS",
         "the band must be crossable; a tool that never leaves NO-INFORMATION "
         "is D61 in the opposite direction")

    print("\nFWD_READ_SELFTEST: " + ("PASS" if ok else "FAIL"))
    return ok


def walk_nomoves(path):
    """Deliberately broken twin used by CELL 4 — never call it for real data."""
    data = Path(path).read_bytes()
    home, turns = _cores_and_turns(data)
    pos, team, kind, seen = {}, {}, {}, set()
    out = {t: {"fwd_deaths": 0} for t in home}
    for rnd, tb in enumerate(turns):
        for _a, _b, ub in fields(tb):
            for un, _w, ubuf in fields(ub):
                if un == 1:
                    for en, _e, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None or e.id in seen:
                            continue
                        seen.add(e.id)
                        pos[e.id], team[e.id], kind[e.id] = e.pos, e.team, e.kind
                elif un == 3:                       # moves NOT consumed
                    for _rn, _rw, rv in fields(ubuf):
                        if rv not in pos:
                            continue
                        p, t, k = pos.pop(rv), team.pop(rv, None), kind.pop(rv, None)
                        if t in out and k == "builder_bot" and \
                                _d2(p, home[1 - t]) < _d2(p, home[t]):
                            out[t]["fwd_deaths"] += 1
    return out


def _synth(n, builds, deaths, spread=3, seed=5):
    """⛔ MUST PRODUCE VARIANCE.

    The first version returned n IDENTICAL games. Per-game sd was 0, so the
    bootstrap SE was 0, so production's `dr < -2*se` collapsed to `dr < 0` and
    the NO-INFORMATION branch was UNREACHABLE — no fixture could ever land
    inside a zero-width band. A degenerate fixture does not merely weaken a
    test; it makes a whole branch untestable while every cell stays green.
    """
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        b = max(1, builds + rng.randint(-spread, spread))
        d = max(0, deaths + rng.randint(-1, 1))
        out.append({"fwd_builds": b, "fwd_deaths": d, "fwd_rounds": 0,
                    "all_builds": 0, "all_deaths": 0, "rounds": 0})
    return out


def walk_norotguard(path):
    """Deliberately broken twin: counts EVERY placeEntity as a build.

    Used by the rotate cell. `rotate()` re-emits placeEntity for an existing id,
    so without the first-placement test the PROTECTED DENOMINATOR inflates —
    and an inflated denominator makes the guard look SATISFIED, i.e. the error
    lands on the safe-looking side of the one gate built to be unfoolable.
    """
    data = Path(path).read_bytes()
    home, turns = _cores_and_turns(data)
    if home is None:
        return None
    out = {t: 0 for t in home}
    for rnd, tb in enumerate(turns):
        for _a, _b, ub in fields(tb):
            for un, _w, ubuf in fields(ub):
                if un != 1:
                    continue
                for en, _e, eb in fields(ubuf):
                    if en != 1:
                        continue
                    e = parse_entity(eb, rnd)
                    if e is None or e.team not in out:
                        continue
                    if e.kind != "builder_bot" and \
                            _d2(e.pos, home[1 - e.team]) < _d2(e.pos, home[e.team]):
                        out[e.team] += 1          # NO first-placement test
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    elif a[0] == "decode":
        cmd_decode(a[1:])
    elif a[0] == "analyse":
        cmd_analyse(a[1:])
    else:
        print(__doc__)
