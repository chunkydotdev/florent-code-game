#!/usr/bin/env python3
"""Build an ARM TREE: copy bots/_v622nestfall and rewrite named flag defaults.

⛔ IT REWRITES A FLAG, THEN RE-READS IT BY IMPORT AND ASSERTS THE VALUE.  A
sed that silently matches nothing is how an "arm" ships as its own control --
this session's own S15 class.  Every name must exist and every value must come
back changed, or the build fails loudly.

  usage: mkarm.py <outdir> FLAG=True FLAG2=False ...
"""
import ast
import os
import re
import shutil
import subprocess
import sys

ROOT = "/Users/junghard/Projects/Work/florent-code-game"
SRC = os.path.join(ROOT, "bots/_v622nestfall")


def main(argv):
    out = argv[1]
    want = {}
    for kv in argv[2:]:
        k, v = kv.split("=")
        want[k] = ast.literal_eval(v)
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(SRC, out, ignore=shutil.ignore_patterns("__pycache__"))
    path = os.path.join(out, "sk_maps.py")
    src = open(path).read()
    for k, v in want.items():
        pat = re.compile(r"^(%s\s*=\s*)(True|False|\d+)" % re.escape(k), re.M)
        new, n = pat.subn(lambda m: m.group(1) + repr(v), src)
        if n != 1:
            raise SystemExit("!! %s matched %d assignment lines (want 1)" % (k, n))
        src = new
    open(path, "w").write(src)
    # --- re-read by IMPORT, in a fresh interpreter: the file on disk is the
    # only thing that ships, and a regex is not evidence about it.
    chk = ("import sys; sys.path.insert(0,%r); import sk_maps as m; "
           "print(' '.join('%%s=%%r'%%(k,getattr(m,k)) for k in %r))"
           % (out, sorted(want)))
    got = subprocess.run([os.path.join(ROOT, ".venv/bin/python"), "-c", chk],
                         capture_output=True, text=True)
    if got.returncode != 0:
        raise SystemExit("!! import failed:\n" + got.stderr)
    seen = dict(kv.split("=") for kv in got.stdout.split())
    for k, v in want.items():
        if seen.get(k) != repr(v):
            raise SystemExit("!! %s reads %s, wanted %r" % (k, seen.get(k), v))
    print("ARM %s  %s" % (out, got.stdout.strip()))


main(sys.argv)
