#!/usr/bin/env python3
"""v603 static scans, each with a DIRTY CONTROL.

⛔ THE RULE THIS FILE EXISTS FOR: "a check that has never produced the other
verdict has not been seen to check" (CLAUDE.md, instruments).  Every scan below
is run TWICE -- once on the real tree, once on a copy mutated to break exactly
what the scan looks for -- and a scan that passes BOTH is reported as BROKEN,
not as a pass.

usage: static_scan.py [tree]        (default bots/_v603skalman)
"""
from __future__ import annotations
import ast
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path("/Users/junghard/Projects/Work/florent-code-game")

MUTATORS = {                     # engine call -> its can_* twin
    "build_conveyor": "can_build_conveyor", "build_splitter": "can_build_splitter",
    "build_harvester": "can_build_harvester", "build_barrier": "can_build_barrier",
    "build_gunner": "can_build_gunner", "build_sentinel": "can_build_sentinel",
    "build_launcher": "can_build_launcher", "build": "can_build",
    "move": "can_move", "fire": "can_fire", "heal": "can_heal",
    "destroy": "can_destroy", "rotate": "can_rotate",
    "spawn_builder": "can_spawn", "convert_ammo": "can_convert_ammo",
    "launch": "can_launch",
}
V603_FLAGS = ("SK_NEST_PAIR", "SK_TRUNK_NEAR", "SK_EVICT_ARMED",
              "SK_COLLAR_GUNS", "SK_CAGE_CEIL")


def files(tree: Path):
    return sorted(p for p in tree.glob("*.py"))


def src(tree: Path) -> str:
    return "\n".join(p.read_text() for p in files(tree))


# --------------------------------------------------------------------------
# S1 -- sandbox AST constraints
# --------------------------------------------------------------------------
def s1_ast_constraints(tree: Path):
    bad = []
    for p in files(tree):
        t = ast.parse(p.read_text())
        for n in ast.walk(t):
            if isinstance(n, ast.Try) and n.finalbody:
                bad.append(f"{p.name}:{n.lineno} finally:")
            for h in getattr(n, "handlers", []) or []:
                nm = getattr(h.type, "id", None)
                if nm in ("BaseException", "SystemExit", "KeyboardInterrupt"):
                    bad.append(f"{p.name}:{h.lineno} except {nm}")
    return not bad, bad


# --------------------------------------------------------------------------
# S2 -- every mutating engine call is gated by its can_* twin IN THE SAME def
# --------------------------------------------------------------------------
def s2_can_gates(tree: Path):
    bad = []
    for p in files(tree):
        t = ast.parse(p.read_text())
        for fn in [n for n in ast.walk(t)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            calls = set()
            for n in ast.walk(fn):
                if (isinstance(n, ast.Call)
                        and isinstance(n.func, ast.Attribute)):
                    calls.add(n.func.attr)
            for m, twin in MUTATORS.items():
                if m in calls and twin not in calls:
                    bad.append(f"{p.name}:{fn.lineno} {fn.name}() calls "
                               f"{m}() with no {twin}()")
    return not bad, bad


# --------------------------------------------------------------------------
# S3 -- ONE WRITER PER SLOT (each SK_SLOT_* appears in wstore/beat from at most
#       one role's method family; here: at most one distinct writing method)
# --------------------------------------------------------------------------
WRITE_RE = re.compile(r"self\.(?:wstore|beat)\(ct,\s*([A-Za-z_0-9\[\]]+)")


def s3_one_writer(tree: Path):
    owners = {}
    bad = []
    for p in files(tree):
        t = ast.parse(p.read_text())
        for fn in [n for n in ast.walk(t)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            seg = ast.get_source_segment(p.read_text(), fn) or ""
            for slot in WRITE_RE.findall(seg):
                if slot.startswith("SK_SLOT_BEAT"):
                    continue            # per-role by construction
                owners.setdefault(slot, set()).add(f"{p.name}:{fn.name}")
    for slot, who in sorted(owners.items()):
        if len(who) > 1:
            bad.append(f"{slot} written by {sorted(who)}")
    return not bad, bad


# --------------------------------------------------------------------------
# S4 -- v603 flags are READ INSIDE A FUNCTION, never captured at module scope
# --------------------------------------------------------------------------
def s4_flag_read_site(tree: Path):
    bad = []
    body = tree / "sk_roles.py"
    t = ast.parse(body.read_text())
    fnlines = []
    for fn in [n for n in ast.walk(t)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        fnlines.append((fn.lineno, max(getattr(x, "lineno", fn.lineno)
                                       for x in ast.walk(fn))))
    for flag in V603_FLAGS:
        seen_in_fn = False
        for n in ast.walk(t):
            if isinstance(n, ast.Name) and n.id == flag and isinstance(n.ctx, ast.Load):
                if any(a <= n.lineno <= b for a, b in fnlines):
                    seen_in_fn = True
                else:
                    bad.append(f"{flag} read at MODULE scope line {n.lineno}")
        if not seen_in_fn and flag != "SK_TRUNK_NEAR":
            bad.append(f"{flag} never read inside any function of sk_roles.py")
    return not bad, bad


# --------------------------------------------------------------------------
# S5 -- the five v603 fixes are actually PRESENT
# --------------------------------------------------------------------------
def s5_fixes_present(tree: Path):
    s = src(tree)
    bad = []
    if "self.nest_turret2" not in s or "SK_NEST_PAIR_N" not in s:
        bad.append("FIX1: no second nest turret slot / pair count")
    if "_terminus_tiles" not in s or "SK_TRUNK_TERM_WEIGHT" not in s:
        bad.append("FIX2: no terminus term in the cover set")
    if "_evict_seal" not in s:
        bad.append("FIX3: no unified seal eviction verb")
    if re.search(r"if not empty_seals and self\._clear_tile", s) and \
            "SK_EVICT_ARMED" not in s:
        bad.append("FIX3: the `not empty_seals` interlock is still unconditional")
    if "_route_gaps" not in s or "SK_COLLAR_PECK_CAP" not in s:
        bad.append("FIX4: no route-gap gate / no collar peck budget")
    if "collar_pecks" not in s:
        bad.append("FIX4: no collar peck ledger")
    if not re.search(r"accept\s*=\s*8\s*-\s*belt_seats", s):
        bad.append("FIX5: accept bar is not the dynamic ceiling")
    return not bad, bad


SCANS = [("S1 sandbox AST constraints", s1_ast_constraints),
         ("S2 can_* gate on every mutator", s2_can_gates),
         ("S3 one writer per store slot", s3_one_writer),
         ("S4 v603 flags read at read site", s4_flag_read_site),
         ("S5 the five v603 fixes present", s5_fixes_present)]

# DIRTY CONTROLS: (scan index, description, mutation applied to a temp copy)
DIRT = [
    (0, "inject `finally:` into main.py",
     lambda t: _sub(t / "main.py",
                    "        except Exception:\n            if not self.reported_error:",
                    "        except Exception:\n            pass\n        finally:\n            pass\n        if not self.reported_error:\n            if True:")),
    (1, "drop the can_build_barrier gate in _seal_tile",
     lambda t: _sub(t / "sk_roles.py",
                    "            if not ct.can_build_barrier(q):\n                return False\n            ct.build_barrier(q)\n        except Exception:\n            return False\n        self.cage_sealed.add((q.x, q.y))",
                    "            ct.build_barrier(q)\n        except Exception:\n            return False\n        self.cage_sealed.add((q.x, q.y))")),
    (2, "add a SECOND writer to SK_SLOT_CAGE",
     lambda t: _sub(t / "sk_roles.py",
                    "    def _lap_free(self, ct, q):",
                    "    def _dirty_second_writer(self, ct):\n"
                    "        self.wstore(ct, SK_SLOT_CAGE, 0)\n\n"
                    "    def _lap_free(self, ct, q):")),
    (3, "capture SK_EVICT_ARMED into a module-scope derived default",
     lambda t: _sub(t / "sk_roles.py",
                    "SEAT_MASK = 0xFF          # slot 0 b0-7",
                    "_DIRTY_DERIVED = SK_EVICT_ARMED and SK_CAGE_CEIL\n"
                    "SEAT_MASK = 0xFF          # slot 0 b0-7")),
    (4, "delete the dynamic accept bar (revert FIX 5)",
     lambda t: _sub(t / "sk_roles.py", "accept = 8 - belt_seats",
                    "accept = SK_CAGE_ACCEPT")),
]


def _sub(path: Path, old: str, new: str):
    s = path.read_text()
    if old not in s:
        raise SystemExit(f"DIRTY CONTROL COULD NOT APPLY in {path.name}: "
                         f"anchor not found -- the control itself is stale.")
    path.write_text(s.replace(old, new, 1))


def main(tree: Path):
    print(f"STATIC SCANS on {tree}\n")
    clean = {}
    for i, (name, fn) in enumerate(SCANS):
        ok, bad = fn(tree)
        clean[i] = ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        for b in bad[:8]:
            print(f"          {b}")
    print("\nDIRTY CONTROLS (each MUST flip its scan to FAIL)\n")
    allgood = all(clean.values())
    for (idx, desc, mut) in DIRT:
        with tempfile.TemporaryDirectory() as td:
            dirty = Path(td) / tree.name
            shutil.copytree(tree, dirty,
                            ignore=shutil.ignore_patterns("__pycache__"))
            mut(dirty)
            ok, bad = SCANS[idx][1](dirty)
            flipped = (not ok)
            print(f"  [{'OK ' if flipped else 'BROKEN'}] {SCANS[idx][0]}"
                  f"  <- {desc}")
            if not flipped:
                allgood = False
                print("          !! the scan PASSED a tree that breaks it -- "
                      "this scan is not checking anything")
            elif bad:
                print(f"          fired on: {bad[0]}")
    print("\nVERDICT:", "ALL SCANS PASS AND ALL CONTROLS FIRE" if allgood
          else "SEE FAILURES ABOVE")
    return 0 if allgood else 1


if __name__ == "__main__":
    t = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "bots" / "_v603skalman"
    sys.exit(main(t))
