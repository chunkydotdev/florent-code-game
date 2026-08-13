#!/usr/bin/env python3
"""Submit a bot with CODE ONLY — never our documents.

IMPLEMENTS: D46 -- `fcode submit` AUTO-ACTIVATES, so submitting IS shipping and
this restores the holder itself rather than relying on anyone knowing that.

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

NAMING IS ENFORCED, NOT REMEMBERED (Magnus, 2026-08-13):
    a SHIP        -> --name 'Loki vN'      and --activate
    an UNRATED LEG-> --name 'Loki rcX.Y'   and NO --activate
`--name` is REQUIRED and the format must match the ship/leg mode, or this exits 2.
It exists because this tool never passed `-n` at all and **v123 shipped UNNAMED**
while v116/v122 carried "Loki v5"/"Loki v6" -- a known convention that lapsed the
moment submitting moved into a script.

Usage:
    .venv/bin/python tools/submit_clean.py bots/_vX --name 'Loki rc7.1'
    .venv/bin/python tools/submit_clean.py bots/_vX --name 'Loki v8' --activate
    .venv/bin/python tools/submit_clean.py bots/_vX --name 'Loki rc7.1' --dry-run

It PRINTS THE FULL MANIFEST before uploading, every time. The failure mode this
guards against was invisible for an entire session; the fix should be the
opposite of invisible.
"""
from __future__ import annotations

import ast
import re
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


def _holder() -> str | None:
    """The live submission, read off the platform. Returns None if it cannot be
    read -- and None is treated as UNKNOWN, never as 'unchanged'. Parses the
    `Active bot:` line rather than the exit code, because `fcode status` exits 0
    while printing `Error: True` (standing repo rule: gate on the presence of the
    load-bearing field)."""
    try:
        r = subprocess.run([str(FCODE), "status"], cwd=ROOT,
                           capture_output=True, text=True, timeout=60)
    except Exception:
        return None
    for line in r.stdout.splitlines():
        if "Active bot:" in line:
            return line.split("Active bot:", 1)[1].strip() or None
    return None


def _update_incumbent(prog: Path, new_tree: str) -> tuple[str, str]:
    """Rewrite PROGRAMME.md's INCUMBENT (and PREVIOUS_INCUMBENT) after a ship.

    DELEGATED AUTHORITY, NOT DRIFT. PROGRAMME.md is edit-on-Magnus's-directive
    -only. Magnus delegated exactly this field to this script on 2026-08-13
    (lane-structure review R3, "could you apply your fixes" — after the field
    went stale at four consecutive ships; it goes stale at exactly one event,
    and that event IS this script). Everything else in the file stays
    Magnus-only.

    Returns (status, message), status in:
      updated — field rewritten, PREVIOUS_INCUMBENT set to the old value
      noop    — already correct, file untouched
      frozen  — INCUMBENT_FROZEN: yes, refused (a frozen incumbent is a Magnus
                hold; a ship over it is loud, not silent)
      error   — field missing/unreadable. Caller exits 3: a ship whose control
                tree cannot be recorded must not read as a clean ship.
    """
    try:
        lines = prog.read_text().splitlines(keepends=True)
    except OSError as e:
        return "error", f"cannot read {prog}: {e}"
    inc_i = prev_i = None
    frozen = None
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("INCUMBENT:"):
            inc_i = i
        elif s.startswith("PREVIOUS_INCUMBENT:"):
            prev_i = i
        elif s.startswith("INCUMBENT_FROZEN:"):
            frozen = s.split(":", 1)[1].strip()
    if inc_i is None:
        return "error", f"no `INCUMBENT:` line found in {prog}"
    cur = lines[inc_i].strip().split(":", 1)[1].strip()
    if frozen == "yes":
        return "frozen", (f"INCUMBENT_FROZEN: yes — leaving INCUMBENT: {cur} "
                          f"untouched; new live tree is {new_tree}")
    if cur == new_tree:
        return "noop", f"INCUMBENT already reads {new_tree}"
    indent = lines[inc_i][:len(lines[inc_i]) - len(lines[inc_i].lstrip())]
    lines[inc_i] = f"{indent}INCUMBENT: {new_tree}\n"
    if prev_i is not None:
        lines[prev_i] = f"{indent}PREVIOUS_INCUMBENT: {cur}\n"
    prog.write_text("".join(lines))
    return "updated", (f"INCUMBENT: {cur} -> {new_tree}; "
                       f"PREVIOUS_INCUMBENT: {cur}")


SHIP_NAME_RE = re.compile(r"^Loki v\d+$")
LEG_NAME_RE = re.compile(r"^Loki rc\d+\.\d+$")


def _name_from(argv: list[str]) -> str | None:
    """`--name "Loki v7"` or `--name=Loki v7`."""
    for i, a in enumerate(argv):
        if a == "--name" and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith("--name="):
            return a.split("=", 1)[1]
    return None


def check_name(name: str | None, activate: bool) -> tuple[bool, str]:
    """Enforce Magnus's naming convention (2026-08-13). Returns (ok, message).

    ⛔ WHY THIS IS ENFORCED IN CODE AND NOT WRITTEN DOWN. This tool never passed
    `-n` at all, so **v123 shipped UNNAMED** while v116 and v122 carried "Loki v5"
    and "Loki v6" — the convention existed, was known, and silently lapsed the
    moment submitting moved into a script. This repo's own finding is that
    *every prose-only rule here has a recorded violation by its own author*, and
    that the durable surfaces are the always-loaded file and **tools that exit 1**.

    THE CONVENTION, Magnus 2026-08-13:
      * a SHIP (`--activate`) is named  `Loki vN`     e.g. "Loki v7"
      * an UNRATED LEG (no --activate) is `Loki rcX.Y` e.g. "Loki rc7.1"
        — a release candidate off ship lineage X, leg Y.

    ⭐ AND THE DISTINCTION IS LOAD-BEARING RATHER THAN COSMETIC. `fcode submit`
    AUTO-ACTIVATES, so an unrated leg is a version that briefly held the live slot
    and can appear in the rated record (measured once at -24.67 Elo across three
    leaked matches). **A prototype indistinguishable from a ship in the submission
    list is one an autopsy cannot separate from a ship** — and per-match `ourver`
    is the only ground truth we have. The `rc` tag makes the leg legible in the
    one place both a human and `ladder_games.tsv` will look.
    """
    if not name:
        return False, (
            "NAME REQUIRED. --name is not optional:\n"
            "  ship          : --name 'Loki v8'    (with --activate)\n"
            "  unrated leg   : --name 'Loki rc7.1' (without --activate)\n"
            "v123 shipped unnamed because this tool never passed one.")
    if activate and not SHIP_NAME_RE.match(name):
        return False, (f"SHIP NAME MUST MATCH 'Loki vN' — got {name!r}.\n"
                       "  --activate means this takes the live slot.")
    if not activate and not LEG_NAME_RE.match(name):
        return False, (f"UNRATED-LEG NAME MUST MATCH 'Loki rcX.Y' — got {name!r}.\n"
                       "  No --activate means this is a leg, not a ship.\n"
                       "  X = the ship lineage it descends from, Y = the leg number.")
    return True, f"name OK: {name!r} ({'SHIP' if activate else 'unrated leg'})"


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    # the value of --name is not a flag but must not be read as the bot dir
    _nm = _name_from(argv)
    if _nm and _nm in args:
        args.remove(_nm)
    dry = "--dry-run" in argv
    activate = "--activate" in argv
    ok, msg = check_name(_nm, activate)
    print(msg)
    if not ok:
        return 2
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

        # ⛔⛔ `fcode submit` ACTIVATES WHAT IT UPLOADS. MEASURED, s29 2026-08-11.
        #
        # Submitting `_v136loki19` printed "Submitted! Version 108" and the very
        # next `fcode status` read `Active bot: v108`. NOTHING in this script or
        # in that command line asks for activation. The holder had been v104 for
        # ~20 hours.
        #
        # WHY THIS IS A REAL HAZARD AND NOT A CURIOSITY: the standing procedure in
        # CLAUDE.md is "serve the rate-limit wait with the INCUMBENT live;
        # activate only in the instant before firing". That procedure is written
        # as though SUBMIT and ACTIVATE were separable. THEY ARE NOT. A session
        # that submits a prototype an hour before its window -- the obviously
        # careful thing to do -- has silently put an unmeasured bot on the rated
        # ladder for that hour, at a measured ~-8 Elo per leaked match.
        #
        # The s29 leak was ~15 seconds and cost ZERO rated matches, verified on
        # the match COUNTER (724 before, 724 after) rather than assumed. That was
        # luck plus watching, and neither is a control.
        #
        # SO THIS SCRIPT NOW RESTORES THE HOLDER ITSELF. Pass --activate to keep
        # the new version live (a real ship); the default is that submitting is
        # not shipping.
        holder_before = _holder()
        print()
        r = subprocess.run([str(FCODE), "submit", str(dst), "-n", _nm], cwd=ROOT)
        if r.returncode != 0:
            return r.returncode

        holder_after = _holder()
        print(f"\nHOLDER: before={holder_before or '?'}  after={holder_after or '?'}")
        if activate:
            print("--activate given: leaving the new submission live. THIS IS A SHIP.")
            # PROGRAMME.md's INCUMBENT went stale at four consecutive ships
            # because it goes stale at exactly one event and that event is this
            # script. As of 2026-08-13 Magnus delegated THIS FIELD (and only
            # this field) to this script — see _update_incumbent's docstring.
            status, msg = _update_incumbent(ROOT / "PROGRAMME.md", f"bots/{src.name}")
            print()
            if status == "updated":
                print(f"PROGRAMME.md {msg}")
                print("   -> COMMIT PROGRAMME.md WITH THE SHIP COMMIT — an "
                      "uncommitted update is the committed-stale bug's twin.")
            elif status == "noop":
                print(f"PROGRAMME.md: {msg}")
            elif status == "frozen":
                print("=" * 68)
                print(f"⛔ {msg}")
                print("   A frozen incumbent is a Magnus hold. This ship just "
                      "displaced it on the platform — tell Magnus NOW.")
                print("=" * 68)
            else:  # error
                print("=" * 68)
                print(f"⛔ PROGRAMME.md INCUMBENT COULD NOT BE MAINTAINED: {msg}")
                print("   COMPARE_AGAINST: previous_line_iteration reads this "
                      "field, so every new arm is controlled on the WRONG tree "
                      "until it is fixed BY HAND.")
                print("=" * 68)
                return 3
            return 0
        if holder_after and holder_before and holder_after != holder_before:
            print(f"** `fcode submit` ACTIVATED {holder_after}. Restoring {holder_before}. **")
            ver = "".join(c for c in holder_before.split()[0] if c.isdigit())
            if not ver:
                print(f"** CANNOT PARSE A VERSION FROM '{holder_before}' -- "
                      f"RESTORE IT BY HAND NOW. **")
                return 1
            subprocess.run([str(FCODE), "submission", "activate", ver], cwd=ROOT)
            # Gate on the LOAD-BEARING FIELD, never on the exit code: `fcode`
            # exits 0 while printing `Error: True` (standing repo rule).
            back = _holder()
            print(f"HOLDER NOW: {back or '?'}")
            if not back or not back.startswith(holder_before.split()[0]):
                print("** ROLLBACK NOT CONFIRMED. THE LADDER IS RUNNING AN "
                      "UNINTENDED BOT. FIX THIS BEFORE ANYTHING ELSE. **")
                return 1
            print("rollback confirmed against the holder, not the exit code.")
        elif holder_after == holder_before:
            print("holder unchanged by submit.")
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
