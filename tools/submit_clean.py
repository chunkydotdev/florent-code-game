#!/usr/bin/env python3
"""Submit a bot with CODE ONLY — never our documents.

WHY THIS EXISTS. Magnus, 2026-08-09: *"don't leak DESIGN and PREREG into our
submissions please."* It was not a hypothetical. Verified by downloading our own
artifacts back off the platform:

    v94  (THE LIVE LADDER SLOT)  ->  PREREG.md
    v95 v96 v97 v98 v99 v100     ->  PREREG.md AND DESIGN.md

`fcode submit <dir>` zips the whole directory, and every bot dir in this repo
carries its pre-registration beside its code. So every upload today shipped our
pre-registered bars, our falsifiers, the maps we consider lost, opponent-specific
constants, and — in DESIGN.md — the mechanism and a *Known weak points* section,
to a platform other teams can pull from.

ALLOWLIST, NOT BLOCKLIST. Only `*.py` is staged. A blocklist on `*.md` would
have to be extended for every future doc type (.txt, .json notes, .csv fixtures)
and would leak silently the first time someone adds one. An allowlist fails
closed: a new file type is simply absent from the upload, which is visible in
the printed manifest rather than invisible on the platform.

The engine requires `main.py` at the zip root or inside exactly one top-level
directory, and auxiliary modules must travel with it for the imports to resolve
— so this is per-extension and recursive, never main.py-only.

Usage:
    .venv/bin/python tools/submit_clean.py bots/_v124loki8            # submit
    .venv/bin/python tools/submit_clean.py bots/_v124loki8 --dry-run  # manifest only

It PRINTS THE FULL MANIFEST before uploading, every time. The failure mode this
guards against was invisible for an entire session; the fix should be the
opposite of invisible.
"""
from __future__ import annotations

import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FCODE = ROOT / ".venv" / "bin" / "fcode"
ALLOW = (".py",)


def stage(src: Path, dst: Path) -> list[Path]:
    kept = []
    for p in sorted(src.rglob("*")):
        if p.is_dir() or "__pycache__" in p.parts:
            continue
        if p.suffix not in ALLOW:
            continue
        rel = p.relative_to(src)
        out = dst / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)
        kept.append(rel)
    return kept


# LOADER-REJECTED CONSTRUCTS. Reported s28 from a read of the engine binary's
# `ast` rules: `finally`, bare `except:`, and `except BaseException` are
# LOAD-TIME REJECTIONS -- they do not kill a unit, they BRICK THE WHOLE
# SUBMISSION. `Exception` and `GameError` are fine.
#
# WHY THIS IS A HARD BLOCK ON AN UNVERIFIED CLAIM, deliberately. I have NOT
# re-derived the loader rules myself; this is the research arm's binary read.
# Blocking is still correct on the asymmetry: our live trees contain ZERO of
# these three constructs (checked across _v130loki13, _v131loki14, _v124loki8),
# so the guard costs us nothing today, while the failure it prevents is total
# and silent -- a submission that never loads at all. If the claim turns out to
# be wrong we have merely forbidden three constructs we do not use.
# Pass --allow-loader-constructs to override, which is a decision on the record.
_LOADER_BANNED = ("finally", "bare except:", "except BaseException")


def loader_lint(root: Path, files: list[Path]) -> list[str]:
    bad = []
    for rel in files:
        if rel.suffix != ".py":
            continue
        try:
            tree = ast.parse((root / rel).read_text())
        except SyntaxError as e:
            bad.append(f"{rel}:{e.lineno}  SYNTAX ERROR: {e.msg}")
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Try) and node.finalbody:
                bad.append(f"{rel}:{node.lineno}  `finally` — loader rejects the SUBMISSION")
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    bad.append(f"{rel}:{node.lineno}  bare `except:` — loader rejects the SUBMISSION")
                elif isinstance(node.type, ast.Name) and node.type.id == "BaseException":
                    bad.append(f"{rel}:{node.lineno}  `except BaseException` — loader rejects the SUBMISSION")
    return bad


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    dry = "--dry-run" in argv
    if not args:
        sys.exit(__doc__)
    src = Path(args[0]).resolve()
    if not src.is_dir():
        sys.exit(f"not a directory: {src}")

    excluded = [p.relative_to(src) for p in sorted(src.rglob("*"))
                if p.is_file() and p.suffix not in ALLOW
                and "__pycache__" not in p.parts]

    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / src.name
        dst.mkdir(parents=True)
        kept = stage(src, dst)

        if not any(p.name == "main.py" for p in kept):
            sys.exit("REFUSING: no main.py among the staged files — the engine "
                     "requires it at the zip root or in one top-level dir.")

        offences = loader_lint(dst, kept)
        if offences and "--allow-loader-constructs" not in argv:
            print("REFUSING: loader-rejected constructs found. These do not kill a "
                  "unit — they brick the ENTIRE submission at load time:")
            for o in offences:
                print(f"    ** {o}")
            print("  Use `Exception` or `GameError`; restructure to avoid `finally`.")
            print("  Override with --allow-loader-constructs (a decision on the record).")
            return 1
        if offences:
            print(f"  ** {len(offences)} loader-rejected construct(s) OVERRIDDEN by flag:")
            for o in offences:
                print(f"    ** {o}")
        print(f"staging {src.name}: {len(kept)} code file(s) -> upload")
        for rel in kept:
            print(f"    +  {rel}")
        if excluded:
            print(f"  EXCLUDED {len(excluded)} non-code file(s) (this is the point):")
            for rel in excluded:
                print(f"    -  {rel}")
        else:
            print("  (nothing to exclude — dir was already code-only)")

        if dry:
            print("\n--dry-run: nothing uploaded.")
            return 0

        print()
        r = subprocess.run([str(FCODE), "submit", str(dst)], cwd=ROOT)
        return r.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
