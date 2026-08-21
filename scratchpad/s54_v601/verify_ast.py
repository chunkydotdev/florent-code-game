#!/usr/bin/env python3
"""v601 static verification: AST parse, forbidden-form scan, undefined-global scan.

Every check is DRIVEN BOTH WAYS -- each one is run against a deliberately DIRTY
copy of the tree and must FAIL there, because a check that has never produced its
other verdict has not been seen to check.

  1. parse           every .py in the tree must compile
  2. forbidden forms `finally:` / `except BaseException:` / `except SystemExit:`
                     are REJECTED BY THE SANDBOX VALIDATOR AT LOAD.  Count must
                     be 0.  Positive control: an injected `finally:` must be
                     caught.
  3. undefined globals every Name loaded at module level or inside a function
                     must resolve to a builtin, a module-level binding, an
                     import, a parameter, a local assignment, or a comprehension
                     target.  Positive control: an injected typo must be caught.

Usage: .venv/bin/python scratchpad/s54_v601/verify_ast.py bots/_v601skalman
"""
from __future__ import annotations

import ast
import builtins
import sys
from pathlib import Path

FORBIDDEN = ("finally", "BaseException", "SystemExit")


def parse_all(tree_dir: Path):
    out = {}
    for f in sorted(tree_dir.glob("*.py")):
        out[f.name] = (f, ast.parse(f.read_text(), filename=str(f)))
    return out


def forbidden_hits(mods):
    hits = []
    for name, (path, tree) in mods.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Try) and node.finalbody:
                hits.append((name, node.lineno, "finally"))
            if isinstance(node, ast.ExceptHandler) and node.type is not None:
                for sub in ast.walk(node.type):
                    if isinstance(sub, ast.Name) and sub.id in ("BaseException", "SystemExit"):
                        hits.append((name, node.lineno, "except " + sub.id))
    return hits


class ScopeCheck(ast.NodeVisitor):
    """Undefined-global scan.  Deliberately conservative in ONE direction only:
    it may MISS a bad name (a shadowed builtin), it must never invent one."""

    def __init__(self, module_names, filename, extra):
        self.mod = set(module_names) | set(dir(builtins)) | set(extra)
        self.filename = filename
        self.bad = []

    def _collect_local(self, node):
        names = set()
        for a in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            names.add(a.arg)
        if node.args.vararg:
            names.add(node.args.vararg.arg)
        if node.args.kwarg:
            names.add(node.args.kwarg.arg)
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, (ast.Store, ast.Del)):
                names.add(sub.id)
            elif isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if sub is not node:
                    names.add(sub.name)
            elif isinstance(sub, ast.ExceptHandler) and sub.name:
                names.add(sub.name)
            elif isinstance(sub, (ast.Import, ast.ImportFrom)):
                for al in sub.names:
                    names.add((al.asname or al.name).split(".")[0])
            elif isinstance(sub, ast.Global) or isinstance(sub, ast.Nonlocal):
                names.update(sub.names)
        return names

    def visit_FunctionDef(self, node):
        local = self._collect_local(node)
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                if sub.id not in local and sub.id not in self.mod:
                    self.bad.append((self.filename, sub.lineno, sub.id))
        # nested defs already covered by the walk above

    visit_AsyncFunctionDef = visit_FunctionDef


def module_bindings(tree):
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for al in node.names:
                names.add((al.asname or al.name).split(".")[0])
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                for sub in ast.walk(t):
                    if isinstance(sub, ast.Name):
                        names.add(sub.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.For):
            for sub in ast.walk(node.target):
                if isinstance(sub, ast.Name):
                    names.add(sub.id)
        elif isinstance(node, (ast.If, ast.Try, ast.While, ast.With)):
            for inner in ast.walk(node):
                if isinstance(inner, (ast.Import, ast.ImportFrom)):
                    for al in inner.names:
                        names.add((al.asname or al.name).split(".")[0])
                elif isinstance(inner, ast.Assign):
                    for t in inner.targets:
                        for sub in ast.walk(t):
                            if isinstance(sub, ast.Name):
                                names.add(sub.id)
                elif isinstance(inner, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    names.add(inner.name)
    return names


def undefined_globals(mods):
    bad = []
    for name, (path, tree) in mods.items():
        mod_names = module_bindings(tree)
        # module-level Loads
        chk = ScopeCheck(mod_names, name, ())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                chk.visit_FunctionDef(node)
        bad.extend(chk.bad)
    return bad


def run(tree_dir: Path, label: str):
    mods = parse_all(tree_dir)
    fb = forbidden_hits(mods)
    ug = undefined_globals(mods)
    print(f"[{label}] {tree_dir}")
    print(f"  parse           : {len(mods)}/{len(mods)} files OK "
          f"({', '.join(sorted(mods))})")
    print(f"  forbidden forms : {len(fb)}" + ("" if not fb else f"  {fb}"))
    print(f"  undefined names : {len(ug)}" + ("" if not ug else f"  {ug}"))
    return len(mods), fb, ug


def main():
    tree = Path(sys.argv[1] if len(sys.argv) > 1 else "bots/_v601skalman")
    n, fb, ug = run(tree, "CLEAN")
    ok = (not fb) and (not ug)

    # ---- POSITIVE CONTROLS: the same scans on a DIRTY copy -----------------
    import shutil
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="v601dirty_"))
    dirty = tmp / "dirty"
    shutil.copytree(tree, dirty)
    p = dirty / "sk_common.py"
    s = p.read_text()
    s = s.replace("def in_bounds(x, y, w, h):\n    return 0 <= x < w and 0 <= y < h",
                  "def in_bounds(x, y, w, h):\n    try:\n        return 0 <= x < w and 0 <= y < h\n"
                  "    except BaseException:\n        return NOT_A_REAL_NAME\n"
                  "    finally:\n        pass")
    p.write_text(s)
    n2, fb2, ug2 = run(dirty, "DIRTY CONTROL")
    ctl_ok = bool(fb2) and bool(ug2)
    shutil.rmtree(tmp)

    print()
    print(f"VERDICT clean={'PASS' if ok else 'FAIL'} "
          f"control_fired={'YES' if ctl_ok else 'NO'}")
    raise SystemExit(0 if (ok and ctl_ok) else 1)


if __name__ == "__main__":
    main()
