#!/usr/bin/env python3
"""Render a `.replay26` match into a single self-contained HTML page you can
screenshot and point at, round by round.

Built for exactly one job: "a replays runner that i can screenshot and use to
show you what i mean" (Magnus, 2026-08-16). Not an analysis tool — it does not
compute chains, timings, or verdicts. It draws the map, the entities, and a
round slider, and lets you drop numbered markers on tiles that persist while
you scrub through rounds so a screenshot carries the coordinates you meant.

Usage:
    .venv/bin/python tools/replay_view.py replay_archive/<id>_game_1.replay26
    .venv/bin/python tools/replay_view.py --match <match_id> [--game N]
    .venv/bin/python tools/replay_view.py --latest
    .venv/bin/python tools/replay_view.py <replay> --out /some/path.html

Writes scratchpad/replay_view/<name>.html by default (repo-root scratchpad/,
not the session tmp one) and PRINTS THE PATH. Never opens a browser.

THIS VIEWER IS NOT AN INSTRUMENT. It draws a picture for a human to look at
and point at; it computes no verdict, and nothing in it is measured against
a control. The moment a claim in any doc cites something seen here, that
claim needs a measured source or it is an eyeball claim — and eyeball claims
are labelled as such.

THE `.replay26` FORMAT
=======================
Protobuf, message `battlecode.Replay` — full schema and gotchas in
tools/replay_schema.md; read that before changing the parsing below. This
tool reuses the wire-level primitives (fields/scalars/read_pos/parse_entity/
KIND_FIELDS/...) from tools/replay_census.py rather than re-deriving them.
Facts this tool leans on that census's own decoder does NOT need but this one
does:

  * `UpdateHp { id, delta }` (Update oneof field 5) is a HP DELTA, not an
    absolute value. census never reads it (it only needs final HP off the
    last placeEntity). This tool applies every delta in round order to keep
    a live HP bar accurate mid-game.
  * A `placeEntity` for an ALREADY-KNOWN id (rotate() re-emits one, and
    apparently so do other in-place state refreshes) is treated here as an
    UPDATE (position/hp/direction refresh) rather than discarded — census
    discards these on purpose to avoid inflating build counts, but a viewer
    that discards them would show a gunner's rotate() as invisible.
  * Not rendered at all: FireTurret / BuilderAttack / BuilderHeal /
    BuilderBuild / CoreConvertAmmo / IndicatorLine / IndicatorDot /
    DistributeResources / BotOutput / cooldown updates. Their SIDE EFFECTS
    still show up (an attack shows as the target's HP bar dropping via
    UpdateHp; a kill shows as removeEntity), but the discrete action events
    themselves are not drawn as beams/highlights. Said again in the report
    for whoever reads this next: this is a map+entity+HP viewer, not a
    combat-log viewer.

PER-ROUND DATA IS STORED AS DELTAS, NOT SNAPSHOTS. The embedded JSON block
has one `initial` entity list (the two Cores, seeded at 500/500 HP per the
schema's "cores are never placed by an update" gotcha) and then one list of
OPS per round (add/upd/mv/rm/hp/pl). The page's JS replays those ops forward
to reconstruct any round's state, with checkpoints every 50 rounds so
scrubbing to round 900 doesn't replay 900 rounds of history from scratch.
This keeps a 1000-round match's HTML in the low single-digit MB instead of
however big 1000 independent full-board snapshots would be.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---- `--help` CONTRACT (house style; see replay_census.py for the incident
# this guards against) ---------------------------------------------------
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

from replay_census import (  # noqa: E402  (import after sys.path fixup, and after --help guard)
    WIRE_LEN,
    WIRE_VARINT,
    fields,
    packed_varints,
    parse_entity,
    read_pos,
    scalars,
)

ARCHIVE_DIR = REPO_ROOT / "replay_archive"
DEFAULT_OUT_DIR = REPO_ROOT / "scratchpad" / "replay_view"

MATCH_FILE_RE = re.compile(r"^([0-9a-fA-F-]{36})_game_(\d+)\.replay26$")


# --- map parsing (standalone copy of Replay._parse_map's logic; census keeps
#     it as a method, this tool needs it before any Turn/HP walking) --------

def parse_map(buf: bytes) -> dict:
    width = height = 0
    tiles: list[list[int]] = []
    cores: list[dict] = []
    for num, wire, value in fields(buf):
        if num == 1:
            width = value
        elif num == 2:
            height = value
        elif num == 3:
            row: list[int] = []
            for rnum, rwire, rvalue in fields(value):
                if rnum == 1:
                    row.extend(packed_varints(rvalue) if rwire == WIRE_LEN else [rvalue])
            tiles.append(row)
        elif num == 4:
            core = {"id": 0, "team": 0, "pos": (0, 0)}
            for cnum, _cw, cvalue in fields(value):
                if cnum == 1:
                    core["id"] = cvalue
                elif cnum == 2:
                    core["team"] = cvalue
                elif cnum == 3:
                    core["pos"] = read_pos(cvalue)
            cores.append(core)
    return {"width": width, "height": height, "tiles": tiles, "cores": cores}


def peek_outcome(path: Path) -> dict:
    """Cheap read: map size, winner, win condition, round count. No turn walk.

    For a list view over many replays (tools/dash's Replays page) at a time —
    `build_view_data` replays every Update in every Turn to reconstruct
    per-round state, which is the right cost for ONE replay you are about to
    look at and the wrong cost for scanning thousands to build a table row
    each. This only descends into `map` (bounded by width*height, a few
    hundred to under a thousand varints) and counts top-level Turn fields
    without opening them — O(file size) but O(1) work per turn instead of
    O(updates in that turn).
    """
    data = path.read_bytes()
    map_buf = None
    n_turns = 0
    winner = None
    win_condition = ""
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            n_turns += 1
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            win_condition = value.decode("utf-8", "replace")
    width = height = None
    if map_buf is not None:
        gmap = parse_map(map_buf)
        width, height = gmap["width"], gmap["height"]
    return {
        "width": width, "height": height, "rounds": n_turns,
        "winner": {0: "A", 1: "B"}.get(winner),
        "win_condition": win_condition or None,
    }


# --- full replay -> {initial entities, per-round op deltas} ----------------

def _entity_dict(ent) -> dict:
    x, y = ent.pos
    return {
        "id": ent.id, "team": ent.team, "kind": ent.kind,
        "x": x, "y": y, "hp": ent.hp, "maxHp": ent.max_hp,
        "dir": ent.direction,
    }


def build_view_data(path: Path) -> dict:
    data = path.read_bytes()
    map_buf = None
    turn_bufs: list[bytes] = []
    winner = None
    win_condition = ""
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
        elif num == 6 and wire == WIRE_LEN:
            win_condition = value.decode("utf-8", "replace")
    if map_buf is None:
        raise ValueError(f"{path}: no battlecode.Map (field 1) — not a replay?")

    gmap = parse_map(map_buf)

    # Cores exist from round 0 and are never emitted as a placeEntity —
    # schema gotcha. Seed them at 500/500 as the "initial" entity set.
    entities: dict[int, dict] = {}
    initial: list[dict] = []
    for core in gmap["cores"]:
        x, y = core["pos"]
        e = {"id": core["id"], "team": core["team"], "kind": "core",
             "x": x, "y": y, "hp": 500, "maxHp": 500, "dir": None}
        entities[core["id"]] = e
        initial.append(e)

    round_ops: list[list[dict]] = []
    for turn_buf in turn_bufs:
        ops: list[dict] = []
        for _num, _wire, update_buf in fields(turn_buf):
            for unum, _uwire, ubuf in fields(update_buf):
                if unum == 1:  # placeEntity
                    for enum_, _ew, ebuf in fields(ubuf):
                        if enum_ != 1:
                            continue
                        ent = parse_entity(ebuf, 0)
                        if ent is None:
                            continue
                        was_known = ent.id in entities
                        d = _entity_dict(ent)
                        entities[ent.id] = d
                        if was_known:
                            ops.append({"op": "upd", "id": d["id"], "x": d["x"],
                                        "y": d["y"], "hp": d["hp"],
                                        "maxHp": d["maxHp"], "dir": d["dir"]})
                        else:
                            ops.append({"op": "add", **d})
                elif unum == 2:  # moveBuilderBot
                    eid = to = None
                    for mnum, _mw, mval in fields(ubuf):
                        if mnum == 1:
                            eid = mval
                        elif mnum == 2:
                            to = read_pos(mval)
                    if eid is not None and to is not None:
                        ent = entities.get(eid)
                        if ent is not None:
                            ent["x"], ent["y"] = to
                        ops.append({"op": "mv", "id": eid, "x": to[0], "y": to[1]})
                elif unum == 3:  # removeEntity
                    for rnum, _rw, rval in fields(ubuf):
                        if rnum == 1:
                            entities.pop(rval, None)
                            ops.append({"op": "rm", "id": rval})
                elif unum == 5:  # updateHp — a DELTA, census never reads this
                    d = scalars(ubuf)
                    eid, delta = d.get(1), d.get(2, 0)
                    if eid is not None:
                        ent = entities.get(eid)
                        if ent is not None and ent.get("maxHp"):
                            ent["hp"] = max(0, min(ent["maxHp"], ent["hp"] + delta))
                        ops.append({"op": "hp", "id": eid, "delta": delta})
                elif unum == 6:  # updatePlayers
                    pl = {"a": None, "b": None}
                    for pnum, _pw, pval in fields(ubuf):
                        if pnum != 1:
                            continue
                        for tnum, _tw, tval in fields(pval):
                            if tnum in (1, 2):
                                td = scalars(tval)
                                pl["a" if tnum == 1 else "b"] = {
                                    "ti": td.get(1, 0),
                                    "collected": td.get(4, 0),
                                    "ammo": td.get(7, 0),
                                }
                    if pl["a"] or pl["b"]:
                        ops.append({"op": "pl", **pl})
                # Everything else (fire/attack/heal/build/convert/indicators/
                # botOutput/cooldowns) is intentionally not rendered — see
                # module docstring.
        round_ops.append(ops)

    return {
        "map": {"width": gmap["width"], "height": gmap["height"], "tiles": gmap["tiles"]},
        "winner": {0: "A", 1: "B"}.get(winner),
        "winCondition": win_condition or None,
        "rounds": len(turn_bufs),
        "initial": initial,
        "roundOps": round_ops,
        # kept for the python-side control check only; stripped before embed
        "_finalEntities": list(entities.values()),
    }


# --- sidecar metadata --------------------------------------------------------

def load_meta(replay_path: Path) -> tuple[dict | None, int | None]:
    """Return (meta.json dict or None, 1-based game index or None)."""
    m = MATCH_FILE_RE.match(replay_path.name)
    if not m:
        return None, None
    match_id, game_idx = m.group(1), int(m.group(2))
    meta_path = replay_path.with_name(f"{match_id}.meta.json")
    if not meta_path.exists():
        return None, game_idx
    try:
        return json.loads(meta_path.read_text()), game_idx
    except Exception:
        return None, game_idx


# --- file resolution (--match / --game / --latest) --------------------------

def resolve_replay(args) -> Path:
    if args.replay is not None:
        p = Path(args.replay)
        if not p.exists():
            raise SystemExit(f"no such file: {p}")
        return p

    if args.latest:
        candidates = [e for e in ARCHIVE_DIR.iterdir() if e.suffix == ".replay26"]
        if not candidates:
            raise SystemExit(f"no .replay26 files in {ARCHIVE_DIR}")
        newest = max(candidates, key=lambda e: e.stat().st_mtime)
        return newest

    if args.match:
        game = args.game or 1
        exact = ARCHIVE_DIR / f"{args.match}_game_{game}.replay26"
        if exact.exists():
            return exact
        pattern = f"{args.match}*_game_{game}.replay26"
        hits = sorted(ARCHIVE_DIR.glob(pattern))
        if len(hits) == 1:
            return hits[0]
        if not hits:
            raise SystemExit(f"no replay matching {pattern} in {ARCHIVE_DIR}")
        raise SystemExit(f"ambiguous --match prefix {args.match!r}, "
                          f"{len(hits)} candidates: " + ", ".join(h.name for h in hits[:10]))

    raise SystemExit("need a replay path, --match, or --latest (see --help)")


# --- HTML rendering -----------------------------------------------------------

PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<style>
  :root {
    --bg: #f4f5f7; --panel: #ffffff; --ink: #1b1f24; --muted: #5b6472;
    --border: #d7dbe1; --teamA: #0072B2; --teamB: #E69F00;
    --empty: #eef0f3; --wall: #2b2f36; --ore: #009E73; --ore-ax: #CC79A7;
    --hpgood: #2e9e5b; --hpbad: #d64545; --marker: #ff2fb0;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
  #app { display: flex; gap: 16px; padding: 14px; align-items: flex-start; flex-wrap: wrap; }
  #left { flex: 0 0 auto; }
  #right { flex: 1 1 320px; min-width: 280px; }
  .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 10px;
    padding: 12px 14px; margin-bottom: 12px; }
  h1 { font-size: 15px; margin: 0 0 4px; color: var(--muted); font-weight: 600;
    text-transform: uppercase; letter-spacing: .04em; }
  .round-huge { font-size: 64px; font-weight: 800; line-height: 1; margin: 2px 0 6px;
    font-variant-numeric: tabular-nums; }
  .round-huge .rlabel { font-size: 22px; font-weight: 600; color: var(--muted);
    vertical-align: middle; margin-right: 8px; }
  .subhead { font-size: 13px; color: var(--muted); margin-bottom: 2px; }
  .teamline { display: flex; gap: 18px; margin-top: 8px; flex-wrap: wrap; }
  .teamchip { display: flex; align-items: center; gap: 8px; font-size: 13px; }
  .swatch { width: 14px; height: 14px; border-radius: 3px; display: inline-block; flex: none; }
  .econ { font-size: 12px; color: var(--muted); margin-left: 4px; }
  /* Comparison table (Magnus, s46-viewer-ux refinement, 2026-08-16): the
     original inline per-team strings were too small to compare side by
     side — "the numbers matter a lot". Big mono numbers, one row per stat,
     two team columns, updates every render(). */
  .cmp-table { width: 100%; border-collapse: collapse; margin-top: 2px; }
  .cmp-table th, .cmp-table td { padding: 3px 8px; }
  .cmp-rowlabel-head { width: 1%; }
  .cmp-teamhead { font-size: 13px; font-weight: 700; text-align: right;
    white-space: nowrap; }
  .cmp-teamhead .swatch { margin-right: 5px; vertical-align: -1px; }
  .cmp-label { font-size: 11px; color: var(--muted); text-align: left;
    white-space: nowrap; padding-right: 12px; }
  .cmp-val { font-family: "SF Mono", Menlo, Consolas, monospace; font-weight: 800;
    text-align: right; font-variant-numeric: tabular-nums; color: var(--ink); }
  .cmp-val.cmp-econ { font-size: 22px; }
  .cmp-val.cmp-unit { font-size: 18px; }
  .cmp-val.cmp-core { font-size: 26px; }
  .cmp-val.lead { color: var(--hpgood); }
  .cmp-sub { font-size: .5em; font-weight: 600; color: var(--muted); margin-left: 2px; }
  .cmp-val.dead { color: var(--hpbad); }
  .cmp-dead-tag { font-size: 10px; font-weight: 700; color: var(--hpbad);
    text-transform: uppercase; letter-spacing: .03em; line-height: 1.2; }
  .cmp-table tr + tr td { border-top: 1px solid var(--border); }
  /* Core HP is the win-condition headline — set it apart from the stat rows below. */
  .cmp-table tbody tr:first-child td { padding-top: 6px; padding-bottom: 9px;
    border-bottom: 2px solid var(--border); }
  .lead-arrow { font-size: .55em; margin-left: 3px; vertical-align: 4px; color: var(--hpgood); }
  #controls { display: flex; align-items: center; gap: 10px; margin-top: 8px; flex-wrap: wrap; }
  #roundSlider { flex: 1 1 260px; min-width: 200px; }
  .btn { background: var(--panel); border: 1px solid var(--border); border-radius: 6px;
    padding: 5px 10px; font-size: 13px; cursor: pointer; color: var(--ink); }
  .btn:hover { background: var(--empty); }
  .hint { font-size: 11px; color: var(--muted); margin-top: 4px; }
  #gridWrap { position: relative; user-select: none; }
  #xlabels { display: flex; margin-left: var(--ylabelw, 22px); }
  .xlabel { flex: none; font-size: 9px; color: var(--muted); text-align: left; overflow: visible; }
  #gridRow { display: flex; }
  #ylabels { display: flex; flex-direction: column; flex: none; width: var(--ylabelw, 22px); }
  .ylabel { font-size: 9px; color: var(--muted); display: flex; align-items: flex-start;
    justify-content: flex-end; padding-right: 3px; }
  #board { position: relative; border: 1px solid var(--border); background: var(--empty); }
  .tile { position: absolute; box-sizing: border-box; border: 1px solid rgba(0,0,0,0.05); }
  .tile.wall { background: var(--wall); }
  .tile.ore { background: var(--ore); }
  .tile.ore-ax { background: var(--ore-ax); }
  .tile.clickable { cursor: crosshair; }
  /* PAINT LAYERS (Magnus, s46: "builders seem to be hidden some rounds") —
     entities render in ascending-id order, so a builder standing ON a belt
     tile (passable to builders) was painted UNDER the later-built conveyor
     and vanished for exactly the rounds it walked the belt. Units above
     buildings, buildings above the core footprint; ids only break ties. */
  .ent { z-index: 1; }
  .ent.core { z-index: 0; }
  .ent.builder_bot { z-index: 3; }
  .ent { position: absolute; display: flex; align-items: center; justify-content: center;
    font-weight: 700; color: #fff; overflow: hidden; box-shadow: 0 0 0 1px rgba(0,0,0,.25) inset; }
  .ent.builder_bot { border-radius: 50%; }
  .ent.core { border-radius: 4px; font-size: 10px; letter-spacing: .02em; }
  .ent.harvester { border-radius: 3px; background-image:
    repeating-linear-gradient(45deg, rgba(255,255,255,.18) 0 2px, transparent 2px 6px); }
  .ent.barrier { border-radius: 2px; background-image:
    repeating-linear-gradient(-45deg, rgba(0,0,0,.28) 0 2px, transparent 2px 6px); }
  .ent.conveyor { border-radius: 2px; }
  .ent.splitter { border-radius: 2px; }
  .ent.gunner, .ent.sentinel { clip-path: polygon(50% 0%, 100% 100%, 0% 100%); }
  .ent.launcher { clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%); }
  .ent .lab { pointer-events: none; }
  .ent .hpbar { position: absolute; left: 8%; right: 8%; bottom: 6%; height: 12%;
    background: rgba(0,0,0,.35); border-radius: 2px; overflow: hidden; }
  .ent .hpbar > i { display: block; height: 100%; background: var(--hpgood); }
  .arrow { position: absolute; top: 2px; right: 2px; width: 0; height: 0;
    border-left: 4px solid transparent; border-right: 4px solid transparent;
    border-bottom: 7px solid rgba(255,255,255,.95); transform-origin: 4px 5px; }
  .marker { position: absolute; border-radius: 50%; border: 3px solid var(--marker);
    box-shadow: 0 0 0 2px #fff, 0 0 6px rgba(0,0,0,.4); display: flex; flex-direction: column;
    align-items: center; justify-content: center; font-weight: 800; color: var(--marker);
    background: rgba(255,255,255,.85); pointer-events: none; line-height: 1; }
  .marker .mk-idx { font-size: 1em; }
  .marker .mk-r { font-size: .5em; font-weight: 700; opacity: .85; }
  #legend { font-size: 12px; margin-top: 8px; }
  #legend .row { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
  #legendDetails > summary { font-size: 15px; color: var(--muted); font-weight: 600;
    text-transform: uppercase; letter-spacing: .04em; cursor: pointer; }
  #legendDetails > summary:hover { color: var(--ink); }
  #legend .ex { width: 20px; height: 20px; flex: none; border-radius: 3px; background: #888;
    color: #fff; display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; box-shadow: 0 0 0 1px rgba(0,0,0,.25) inset; }
  #markerList { font-size: 12px; line-height: 1.8; }
  #markerList .mkrow { display: flex; align-items: center; gap: 6px; margin: 2px 0; }
  #markerList .mk { color: var(--marker); font-weight: 700; flex: none; }
  #markerList .mkpos { color: var(--muted); flex: none; }
  #markerList input.mkcomment { border: none; background: transparent; font: inherit;
    color: var(--ink); flex: 1 1 auto; min-width: 80px; outline: none; padding: 1px 3px;
    border-radius: 3px; }
  #markerList input.mkcomment:hover, #markerList input.mkcomment:focus { background: var(--empty); }
  #markerList input.mkcomment::placeholder { color: var(--muted); font-style: italic; }
  code { background: var(--empty); border-radius: 3px; padding: 1px 4px; }
  table.meta td { font-size: 12px; padding: 1px 6px 1px 0; color: var(--muted); }
  table.meta td.v { color: var(--ink); font-weight: 600; }
</style>
</head>
<body>
<div id="app">
  <div id="left">
    <div id="gridWrap">
      <div id="xlabels"></div>
      <div id="gridRow">
        <div id="ylabels"></div>
        <div id="board"></div>
      </div>
    </div>
  </div>
  <div id="right">
    <div class="panel">
      <h1>Round</h1>
      <div class="round-huge"><span class="rlabel">R</span><span id="roundNum">0</span>
        <span class="econ">/ <span id="roundMax">0</span></span></div>
      <div id="controls">
        <button class="btn" id="btnHome">⏮ Home</button>
        <button class="btn" id="btnPlay">▶ Play</button>
        <input type="range" id="roundSlider" min="0" max="0" step="1" value="0">
        <button class="btn" id="btnEnd">End ⏭</button>
        <select class="btn" id="speedSelect" title="autoplay speed">
          <option value="1">1x</option>
          <option value="2">2x</option>
          <option value="4">4x</option>
        </select>
      </div>
      <div class="hint">← → step 1 · shift+← → step 10 · Home/End jump to first/last round ·
        space play/pause</div>
    </div>
    <div class="panel">
      <h1>Match</h1>
      <div id="matchInfo"></div>
      <div class="teamline" id="teamLine"></div>
    </div>
    <div class="panel">
      <h1>Comparison</h1>
      <table class="cmp-table" id="cmpTable">
        <thead>
          <tr>
            <th class="cmp-rowlabel-head"></th>
            <th class="cmp-teamhead" id="cmpHeadA"></th>
            <th class="cmp-teamhead" id="cmpHeadB"></th>
          </tr>
        </thead>
        <tbody id="cmpBody"></tbody>
      </table>
    </div>
    <div class="panel">
      <h1>Markers (click a tile)</h1>
      <div id="markerList">none placed</div>
    </div>
    <div class="panel">
      <details id="legendDetails">
        <summary>Legend (hover any piece for its details)</summary>
        <div id="legend"></div>
      </details>
    </div>
  </div>
</div>
<script id="replay-data" type="application/json">__DATA_JSON__</script>
<script id="page-meta" type="application/json">__META_JSON__</script>
<script>
(function () {
  "use strict";
  const DATA = JSON.parse(document.getElementById("replay-data").textContent);
  const META = JSON.parse(document.getElementById("page-meta").textContent);
  const W = DATA.map.width, H = DATA.map.height, TILES = DATA.map.tiles;
  const N_ROUNDS = DATA.rounds;
  const TEAM_COLOR = { 0: "var(--teamA)", 1: "var(--teamB)" };
  const TEAM_COLOR_HEX = { 0: "#0072B2", 1: "#E69F00" };
  const KIND_LABEL = {
    builder_bot: "b", core: "CORE", conveyor: "c", splitter: "Y",
    harvester: "H", barrier: "▩", gunner: "G", sentinel: "S", launcher: "L",
  };
  // Fallback core max HP when a core is destroyed (its maxHp is no longer in
  // state.entities to read) — GameConstants: core max HP is 500, fixed.
  const CORE_MAX_HP = 500;
  // Rows for the Comparison table (Magnus, s46-viewer-ux refinement — inline
  // strings were too small to compare side-by-side, "the numbers matter a
  // lot"; Core HP row added as the win-condition headline; always-show set
  // widened per Magnus's follow-up — a 0-count on a row someone is watching
  // FOR (e.g. "no guns yet") is information, not noise).
  // `always: true` rows render every round regardless of value (Core HP and
  // the three econ rows always did; builders/harvesters/conveyors/gunners/
  // sentinels never meaningfully hit 0-0 in a real game and a stable row set
  // scans better than one that appears/disappears). Only splitters/launchers/
  // barriers are omitted when BOTH teams are at 0 for that kind.
  // Cores are excluded from unit counts (every match has exactly one per
  // team; the Core HP row is the dedicated place for core state).
  const CMP_ROWS = [
    { label: "Core HP", core: true, always: true },
    { label: "Ti", econ: true, field: "ti", always: true },
    { label: "collected", econ: true, field: "collected", always: true },
    { label: "ammo", econ: true, field: "ammo", always: true },
    { label: "builders", kind: "builder_bot", always: true },
    { label: "harvesters", kind: "harvester", always: true },
    { label: "conveyors", kind: "conveyor", always: true },
    { label: "splitters", kind: "splitter" },
    { label: "gunners", kind: "gunner", always: true },
    { label: "sentinels", kind: "sentinel", always: true },
    { label: "launchers", kind: "launcher" },
    { label: "barriers", kind: "barrier" },
  ];
  const DIR_DELTA = { 0:[0,0],1:[0,-1],2:[1,-1],3:[1,0],4:[1,1],5:[0,1],6:[-1,1],7:[-1,0],8:[-1,-1] };
  const DIR_DEG = { 1:0, 2:45, 3:90, 4:135, 5:180, 6:225, 7:270, 8:315 };

  // ---- layout ----
  const MAX_BOARD_PX = 900;
  const cellSize = Math.max(10, Math.min(46, Math.floor(MAX_BOARD_PX / Math.max(W, H))));
  const ylabelw = String(H - 1).length * 7 + 10;
  document.documentElement.style.setProperty("--ylabelw", ylabelw + "px");

  const board = document.getElementById("board");
  board.style.width = (W * cellSize) + "px";
  board.style.height = (H * cellSize) + "px";

  const xlabels = document.getElementById("xlabels");
  const ylabels = document.getElementById("ylabels");
  xlabels.style.marginLeft = ylabelw + "px";
  const xStep = W > 20 ? 5 : 1;
  const yStep = H > 20 ? 5 : 1;
  for (let x = 0; x < W; x++) {
    const d = document.createElement("div");
    d.className = "xlabel";
    d.style.width = cellSize + "px";
    d.textContent = (x % xStep === 0 || x === W - 1) ? String(x) : "";
    xlabels.appendChild(d);
  }
  for (let y = 0; y < H; y++) {
    const d = document.createElement("div");
    d.className = "ylabel";
    d.style.height = cellSize + "px";
    d.textContent = (y % yStep === 0 || y === H - 1) ? String(y) : "";
    ylabels.appendChild(d);
  }

  // tiles (static)
  const ENV_CLASS = { 0: "", 1: "wall", 2: "ore", 3: "ore-ax" };
  for (let y = 0; y < H; y++) {
    const row = TILES[y] || [];
    for (let x = 0; x < W; x++) {
      const env = row[x] || 0;
      const t = document.createElement("div");
      t.className = "tile clickable " + (ENV_CLASS[env] || "");
      t.style.left = (x * cellSize) + "px";
      t.style.top = (y * cellSize) + "px";
      t.style.width = cellSize + "px";
      t.style.height = cellSize + "px";
      t.dataset.x = x; t.dataset.y = y;
      t.addEventListener("click", () => toggleMarker(x, y));
      board.appendChild(t);
    }
  }

  // entity layer
  const entLayer = document.createElement("div");
  entLayer.style.position = "absolute"; entLayer.style.left = "0"; entLayer.style.top = "0";
  entLayer.style.pointerEvents = "none";
  board.appendChild(entLayer);
  const markerLayer = document.createElement("div");
  markerLayer.style.position = "absolute"; markerLayer.style.left = "0"; markerLayer.style.top = "0";
  markerLayer.style.pointerEvents = "none";
  board.appendChild(markerLayer);

  // ---- state reconstruction from ops (checkpointed) ----
  const CK_EVERY = 50;
  function freshState() {
    const entities = {};
    for (const e of DATA.initial) entities[e.id] = Object.assign({}, e);
    return { entities, players: { a: null, b: null } };
  }
  function cloneState(s) {
    const entities = {};
    for (const k in s.entities) entities[k] = Object.assign({}, s.entities[k]);
    return { entities, players: { a: s.players.a ? Object.assign({}, s.players.a) : null,
                                   b: s.players.b ? Object.assign({}, s.players.b) : null } };
  }
  function applyOps(state, ops) {
    for (const op of ops) {
      if (op.op === "add") {
        state.entities[op.id] = { id: op.id, team: op.team, kind: op.kind,
          x: op.x, y: op.y, hp: op.hp, maxHp: op.maxHp, dir: op.dir };
      } else if (op.op === "upd") {
        const e = state.entities[op.id];
        if (e) { e.x = op.x; e.y = op.y; e.hp = op.hp; e.maxHp = op.maxHp; e.dir = op.dir; }
      } else if (op.op === "mv") {
        const e = state.entities[op.id];
        if (e) { e.x = op.x; e.y = op.y; }
      } else if (op.op === "rm") {
        delete state.entities[op.id];
      } else if (op.op === "hp") {
        const e = state.entities[op.id];
        if (e && e.maxHp) e.hp = Math.max(0, Math.min(e.maxHp, e.hp + op.delta));
      } else if (op.op === "pl") {
        if (op.a) state.players.a = op.a;
        if (op.b) state.players.b = op.b;
      }
    }
  }
  const checkpoints = [{ round: -1, state: freshState() }];
  (function buildCheckpoints() {
    let cur = cloneState(checkpoints[0].state);
    for (let r = 0; r < N_ROUNDS; r++) {
      applyOps(cur, DATA.roundOps[r]);
      if (r % CK_EVERY === CK_EVERY - 1 || r === N_ROUNDS - 1) {
        checkpoints.push({ round: r, state: cloneState(cur) });
      }
    }
  })();
  function stateAtRound(r) {
    let best = checkpoints[0];
    for (const c of checkpoints) { if (c.round <= r) best = c; else break; }
    const s = cloneState(best.state);
    for (let rr = best.round + 1; rr <= r; rr++) applyOps(s, DATA.roundOps[rr]);
    return s;
  }

  // ---- markers (persist across rounds; independent of replay state) ----
  // "x,y" -> { idx: 1..8, round: <round placed>, comment: <free text> }
  const markers = {};
  function toggleMarker(x, y) {
    const key = x + "," + y;
    if (markers[key] !== undefined) { delete markers[key]; }
    else {
      const used = new Set(Object.values(markers).map((m) => m.idx));
      let idx = 1;
      while (used.has(idx) && idx <= 8) idx++;
      if (idx > 8) { alert("Max 8 markers. Click one to remove it first."); return; }
      markers[key] = { idx: idx, round: round, comment: "" };
    }
    renderMarkers();
    renderMarkerList();
  }
  function renderMarkers() {
    markerLayer.innerHTML = "";
    const entries = Object.entries(markers).sort((a, b) => a[1].idx - b[1].idx);
    for (const [key, mk] of entries) {
      const [x, y] = key.split(",").map(Number);
      const m = document.createElement("div");
      m.className = "marker";
      const sz = Math.max(cellSize - 4, 14);
      m.style.width = sz + "px"; m.style.height = sz + "px";
      m.style.left = (x * cellSize + (cellSize - sz) / 2) + "px";
      m.style.top = (y * cellSize + (cellSize - sz) / 2) + "px";
      m.style.fontSize = Math.max(10, Math.floor(sz * 0.5)) + "px";
      m.title = mk.idx + " @ (" + x + "," + y + ") placed r" + mk.round +
        (mk.comment ? " — " + mk.comment : "");
      const numSpan = document.createElement("span");
      numSpan.className = "mk-idx";
      numSpan.textContent = mk.idx;
      const rSpan = document.createElement("span");
      rSpan.className = "mk-r";
      rSpan.textContent = "@r" + mk.round;
      m.appendChild(numSpan);
      m.appendChild(rSpan);
      markerLayer.appendChild(m);
    }
  }
  function renderMarkerList() {
    const el = document.getElementById("markerList");
    el.innerHTML = "";
    const entries = Object.entries(markers).sort((a, b) => a[1].idx - b[1].idx);
    if (!entries.length) { el.textContent = "none placed"; return; }
    for (const [key, mk] of entries) {
      const [x, y] = key.split(",");
      const row = document.createElement("div");
      row.className = "mkrow";
      const label = document.createElement("span");
      label.className = "mk";
      label.textContent = mk.idx + ":";
      const pos = document.createElement("span");
      pos.className = "mkpos";
      pos.textContent = "(" + x + "," + y + ") r" + mk.round;
      const input = document.createElement("input");
      input.type = "text";
      input.className = "mkcomment";
      input.placeholder = "add a comment…";
      input.value = mk.comment || "";
      input.maxLength = 140;
      input.addEventListener("input", () => { mk.comment = input.value; });
      row.appendChild(label);
      row.appendChild(pos);
      row.appendChild(input);
      el.appendChild(row);
    }
  }

  // ---- rendering ----
  function cmpValCell(text, sizeClass, lead) {
    return "<td class=\"cmp-val " + sizeClass + (lead ? " lead" : "") + "\">" + text +
      (lead ? "<span class=\"lead-arrow\">▲</span>" : "") + "</td>";
  }
  // Core HP cell is its own shape: big number + small "/max", and a distinct
  // dead-state style (red, "destroyed" tag) when this side's core is gone —
  // `hp` is already 0 in that case (see the coreHp[] default below), so the
  // lead comparison still does the right thing against a surviving core.
  function cmpCoreCell(hp, maxHp, dead, lead) {
    const cls = "cmp-val cmp-core" + (lead ? " lead" : "") + (dead ? " dead" : "");
    return "<td class=\"" + cls + "\">" + hp + "<span class=\"cmp-sub\">/" + maxHp + "</span>" +
      (lead ? "<span class=\"lead-arrow\">▲</span>" : "") +
      (dead ? "<div class=\"cmp-dead-tag\">destroyed</div>" : "") + "</td>";
  }
  // Comparison table: rebuilt every render() (round-boundary values only,
  // ~12 rows — trivial vs. the per-entity draw loop above). counts/pa/pb/
  // coreHp all come from the SAME stateAtRound(round) call render() already
  // made, so this is a read of already-derived per-round state, not a
  // recompute.
  function renderCmpTable(counts, pa, pb, coreHp) {
    const tbody = document.getElementById("cmpBody");
    if (!tbody) return;
    let html = "";
    for (const r of CMP_ROWS) {
      let cellA, cellB;
      if (r.core) {
        const ca = coreHp[0], cb = coreHp[1];
        const hpA = ca ? ca.hp : 0, hpB = cb ? cb.hp : 0;
        const maxA = ca ? ca.maxHp : CORE_MAX_HP, maxB = cb ? cb.maxHp : CORE_MAX_HP;
        const aLead = hpA > hpB, bLead = hpB > hpA;
        cellA = cmpCoreCell(hpA, maxA, !ca, aLead);
        cellB = cmpCoreCell(hpB, maxB, !cb, bLead);
      } else if (r.econ) {
        const va = pa ? pa[r.field] : null, vb = pb ? pb[r.field] : null;
        const numA = typeof va === "number" ? va : -Infinity;
        const numB = typeof vb === "number" ? vb : -Infinity;
        const aLead = numA > numB && numA !== -Infinity;
        const bLead = numB > numA && numB !== -Infinity;
        cellA = cmpValCell(va == null ? "–" : String(va), "cmp-econ", aLead);
        cellB = cmpValCell(vb == null ? "–" : String(vb), "cmp-econ", bLead);
      } else {
        const va = counts[0][r.kind] || 0, vb = counts[1][r.kind] || 0;
        if (!r.always && va === 0 && vb === 0) continue; // omit only for the non-"always" kinds
        const aLead = va > vb, bLead = vb > va;
        cellA = cmpValCell(String(va), "cmp-unit", aLead);
        cellB = cmpValCell(String(vb), "cmp-unit", bLead);
      }
      html += "<tr><td class=\"cmp-label\">" + r.label + "</td>" + cellA + cellB + "</tr>";
    }
    tbody.innerHTML = html;
  }
  let round = 0;
  function render() {
    document.getElementById("roundNum").textContent = round;
    const state = stateAtRound(round);
    entLayer.innerHTML = "";
    const ids = Object.keys(state.entities).sort((a, b) => a - b);
    const counts = { 0: {}, 1: {} };
    // null until this round's core is seen for that team — stays null (read
    // as destroyed/0-hp by renderCmpTable) if the core was removed by now.
    const coreHp = { 0: null, 1: null };
    for (const id of ids) {
      const e = state.entities[id];
      if (e.kind === "core") {
        if (coreHp[e.team] !== undefined) coreHp[e.team] = { hp: e.hp, maxHp: e.maxHp };
      } else if (counts[e.team]) {
        counts[e.team][e.kind] = (counts[e.team][e.kind] || 0) + 1;
      }
      const div = document.createElement("div");
      div.className = "ent " + e.kind;
      const isCore = e.kind === "core";
      const w = isCore ? cellSize * 2 : cellSize - 2;
      const h = isCore ? cellSize * 2 : cellSize - 2;
      div.style.left = (e.x * cellSize + (isCore ? 0 : 1)) + "px";
      div.style.top = (e.y * cellSize + (isCore ? 0 : 1)) + "px";
      div.style.width = w + "px";
      div.style.height = h + "px";
      div.style.background = TEAM_COLOR_HEX[e.team] || "#888";
      div.style.fontSize = (isCore ? Math.max(9, cellSize * 0.28) : Math.max(8, cellSize * 0.5)) + "px";
      div.title = e.kind + " #" + e.id + " team " + (e.team === 0 ? "A" : "B") +
        "  hp " + e.hp + "/" + e.maxHp + "  @(" + e.x + "," + e.y + ")" +
        (e.dir ? "  facing " + e.dir : "");
      const lab = document.createElement("span");
      lab.className = "lab";
      lab.textContent = KIND_LABEL[e.kind] || "?";
      div.appendChild(lab);
      if (e.maxHp) {
        const bar = document.createElement("div");
        bar.className = "hpbar";
        const frac = Math.max(0, Math.min(1, e.hp / e.maxHp));
        const i = document.createElement("i");
        i.style.width = (frac * 100) + "%";
        i.style.background = frac > 0.5 ? "var(--hpgood)" : (frac > 0.2 ? "#d6a72e" : "var(--hpbad)");
        bar.appendChild(i);
        div.appendChild(bar);
      }
      // Conveyors show just the "c" glyph (facing is on hover via .title above) —
      // the rotating arrow was confusing at a glance. Splitters/turrets keep it.
      if (e.dir && DIR_DEG[e.dir] !== undefined &&
          (e.kind === "splitter" || e.kind === "gunner" || e.kind === "sentinel")) {
        const ar = document.createElement("div");
        ar.className = "arrow";
        ar.style.transform = "rotate(" + DIR_DEG[e.dir] + "deg)";
        ar.style.borderBottomColor = "rgba(255,255,255,.95)";
        div.appendChild(ar);
      }
      entLayer.appendChild(div);
    }
    // comparison table (Core HP + Ti/collected/ammo + per-kind unit counts, A vs B)
    renderCmpTable(counts, state.players.a, state.players.b, coreHp);
  }
  function setRound(r) {
    round = Math.max(0, Math.min(N_ROUNDS - 1, r));
    document.getElementById("roundSlider").value = round;
    render();
  }

  // ---- autoplay ----
  let playing = false;
  let playTimer = null;
  let speed = 1;
  const btnPlay = document.getElementById("btnPlay");
  const speedSelect = document.getElementById("speedSelect");
  const AUTOPLAY_BASE_MS = 250;
  function tick() {
    if (round >= N_ROUNDS - 1) { pausePlay(); return; }
    setRound(round + 1);
  }
  function startPlay() {
    if (playing || N_ROUNDS <= 1) return;
    if (round >= N_ROUNDS - 1) setRound(0);
    playing = true;
    btnPlay.textContent = "⏸ Pause";
    playTimer = setInterval(tick, AUTOPLAY_BASE_MS / speed);
  }
  function pausePlay() {
    playing = false;
    btnPlay.textContent = "▶ Play";
    if (playTimer) { clearInterval(playTimer); playTimer = null; }
  }
  function togglePlay() { if (playing) pausePlay(); else startPlay(); }
  btnPlay.addEventListener("click", togglePlay);
  speedSelect.addEventListener("change", () => {
    speed = parseFloat(speedSelect.value) || 1;
    if (playing) { clearInterval(playTimer); playTimer = setInterval(tick, AUTOPLAY_BASE_MS / speed); }
  });

  // ---- header / match info ----
  document.getElementById("roundMax").textContent = N_ROUNDS - 1;
  const slider = document.getElementById("roundSlider");
  slider.max = N_ROUNDS - 1;
  slider.addEventListener("input", () => { pausePlay(); setRound(parseInt(slider.value, 10)); });
  document.getElementById("btnHome").addEventListener("click", () => { pausePlay(); setRound(0); });
  document.getElementById("btnEnd").addEventListener("click", () => { pausePlay(); setRound(N_ROUNDS - 1); });
  window.addEventListener("keydown", (ev) => {
    const tag = (ev.target && ev.target.tagName) || "";
    const inField = tag === "INPUT" || tag === "TEXTAREA";
    if (ev.key === " " || ev.code === "Space") {
      if (inField) return; // let the comment box type a space normally
      ev.preventDefault();
      togglePlay();
      return;
    }
    if (inField) return; // don't hijack arrow/Home/End while editing a marker comment
    if (ev.key === "ArrowLeft") { pausePlay(); setRound(round - (ev.shiftKey ? 10 : 1)); ev.preventDefault(); }
    else if (ev.key === "ArrowRight") { pausePlay(); setRound(round + (ev.shiftKey ? 10 : 1)); ev.preventDefault(); }
    else if (ev.key === "Home") { pausePlay(); setRound(0); ev.preventDefault(); }
    else if (ev.key === "End") { pausePlay(); setRound(N_ROUNDS - 1); ev.preventDefault(); }
  });

  const matchInfo = document.getElementById("matchInfo");
  const rows = [];
  rows.push(["Map", W + " x " + H]);
  rows.push(["Rounds", String(N_ROUNDS)]);
  rows.push(["Winner", DATA.winner ? ("Team " + DATA.winner) : "none (unfinished?)"]);
  rows.push(["Win condition", DATA.winCondition || "–"]);
  if (META.matchId) rows.push(["Match id", META.matchId + (META.gameIndex ? ("  game " + META.gameIndex) : "")]);
  if (META.completedAt) rows.push(["Completed", META.completedAt]);
  matchInfo.innerHTML = "<table class='meta'>" + rows.map(r =>
    "<tr><td>" + r[0] + "</td><td class='v'>" + r[1] + "</td></tr>").join("") + "</table>";

  const teamLine = document.getElementById("teamLine");
  const teamAName = META.teamAName ? (META.teamAName + (META.teamAVersion != null ? (" v" + META.teamAVersion) : "")) : "Team A";
  const teamBName = META.teamBName ? (META.teamBName + (META.teamBVersion != null ? (" v" + META.teamBVersion) : "")) : "Team B";
  teamLine.innerHTML =
    '<div class="teamchip"><span class="swatch" style="background:' + TEAM_COLOR_HEX[0] + '"></span>' +
    '<div>A &middot; ' + teamAName + '</div></div>' +
    '<div class="teamchip"><span class="swatch" style="background:' + TEAM_COLOR_HEX[1] + '"></span>' +
    '<div>B &middot; ' + teamBName + '</div></div>';

  // ---- comparison table header (built once; team identity doesn't change
  // per round — only the cell values do, refreshed every render()) ----
  const cmpHeadA = document.getElementById("cmpHeadA");
  const cmpHeadB = document.getElementById("cmpHeadB");
  if (cmpHeadA) {
    cmpHeadA.style.color = TEAM_COLOR_HEX[0];
    cmpHeadA.innerHTML = '<span class="swatch" style="background:' + TEAM_COLOR_HEX[0] + '"></span>A';
  }
  if (cmpHeadB) {
    cmpHeadB.style.color = TEAM_COLOR_HEX[1];
    cmpHeadB.innerHTML = '<span class="swatch" style="background:' + TEAM_COLOR_HEX[1] + '"></span>B';
  }

  // ---- legend ----
  const legend = document.getElementById("legend");
  const tiles = [
    ["wall", "wall — impassable, blocks building"],
    ["ore", "ore (titanium) — build harvesters here"],
    ["ore-ax", "ore (axionite) — build harvesters here"],
  ];
  const kinds = [
    ["core", "CORE", "2x2 footprint, 500 HP"],
    ["builder_bot", "b", "mobile, only unit that builds"],
    ["conveyor", "c", "hover for facing direction"],
    ["splitter", "Y", "arrow = facing (output side)"],
    ["harvester", "H", "hatched, built on ore"],
    ["barrier", "▩", "cheap HP wall"],
    ["gunner", "G", "triangle, arrow = facing"],
    ["sentinel", "S", "triangle, longer range"],
    ["launcher", "L", "diamond, facing-independent"],
  ];
  legend.innerHTML =
    tiles.map(([cls, note]) =>
      '<div class="row"><span class="swatch tile-' + cls + '" style="background:var(--' + cls + ')"></span>' +
      '<span>' + note + '</span></div>').join("") +
    '<div class="row"><span class="swatch" style="background:var(--empty)"></span><span>empty tile</span></div>' +
    kinds.map(([k, l, note]) =>
    '<div class="row"><span class="ex ' + k + '" style="background:#888">' + l + '</span>' +
    '<span>' + k.replace("_", " ") + ' — ' + note + '</span></div>').join("") +
    '<div class="row" style="margin-top:8px"><span class="swatch" style="background:' + TEAM_COLOR_HEX[0] + '"></span>Team A' +
    '&nbsp;&nbsp;<span class="swatch" style="background:' + TEAM_COLOR_HEX[1] + '"></span>Team B</div>' +
    '<div class="row">HP bar under each unit (green &gt;50%, amber &gt;20%, red below)</div>' +
    '<div class="row" style="color:var(--marker)">Click any tile to drop/remove a numbered marker (max 8, shows index@round placed) — persists across rounds. Add a comment per marker in the list below.</div>';

  renderMarkerList();
  setRound(0);
})();
</script>
</body>
</html>
"""


def render_html(view_data: dict, meta: dict | None, match_id: str | None, game_idx: int | None) -> str:
    embed = {k: v for k, v in view_data.items() if not k.startswith("_")}
    data_json = json.dumps(embed, separators=(",", ":"))
    page_meta = {
        "matchId": match_id,
        "gameIndex": game_idx,
        "teamAName": (meta or {}).get("teamAName"),
        "teamAVersion": (meta or {}).get("teamAVersion"),
        "teamBName": (meta or {}).get("teamBName"),
        "teamBVersion": (meta or {}).get("teamBVersion"),
        "completedAt": (meta or {}).get("completedAt"),
        "scoreA": (meta or {}).get("scoreA"),
        "scoreB": (meta or {}).get("scoreB"),
    }
    meta_json = json.dumps(page_meta, separators=(",", ":"))
    title_bits = []
    if meta:
        title_bits.append(f"{meta.get('teamAName','A')} vs {meta.get('teamBName','B')}")
    if match_id:
        title_bits.append(f"{match_id[:8]} game {game_idx}")
    title = " — ".join(title_bits) or "replay"
    html = PAGE_TEMPLATE.replace("__TITLE__", title)
    html = html.replace("__DATA_JSON__", data_json)
    html = html.replace("__META_JSON__", meta_json)
    return html


# --- the one generator, shared by the CLI and tools/dash's Replays page -----

def generate_html(path: Path) -> str:
    """Build the full standalone viewer page for one replay file.

    THE ONE IMPLEMENTATION. `main()` below calls this for the CLI; the
    dashboard's `/replay` route (tools/dash/replays.py) imports and calls the
    exact same function rather than re-deriving the parse+render — that is
    the whole point of "reuse replay_view.py's generator" in the brief this
    was built against. Do not fork this into a second copy for the dashboard.
    """
    view_data = build_view_data(path)
    meta, game_idx = load_meta(path)
    m = MATCH_FILE_RE.match(path.name)
    match_id = m.group(1) if m else None
    return render_html(view_data, meta, match_id, game_idx)


# --- main ---------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n\nTHE `.replay26`")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("replay", nargs="?", help=".replay26 file path")
    ap.add_argument("--match", help="match id (or unique prefix); looks in replay_archive/")
    ap.add_argument("--game", type=int, default=None, help="game number within --match (default 1)")
    ap.add_argument("--latest", action="store_true", help="newest .replay26 in replay_archive/")
    ap.add_argument("--out", type=Path, default=None, help="output HTML path (default scratchpad/replay_view/<name>.html)")
    args = ap.parse_args()

    path = resolve_replay(args)
    html = generate_html(path)

    out_path = args.out
    if out_path is None:
        DEFAULT_OUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = DEFAULT_OUT_DIR / f"{path.stem}.html"
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html)
    print(str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
