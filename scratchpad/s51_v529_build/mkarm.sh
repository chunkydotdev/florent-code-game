#!/bin/zsh
# mkarm.sh <destdir> <src> [KEY=VALUE ...]
# ⛔ Overrides are applied IN PLACE at the DEFINITION SITE, never appended --
# v515 finding 3: an appended `X = False` after a module-level `Y = f(X)`
# freezes the value the module body saw.  flagoff_ast.py proves there are no
# such derived defaults for the v528 set, and this script keeps it that way by
# never creating an append in the first place.
set -e
DEST=$1; SRC=$2; shift 2
rm -rf "$DEST"; cp -R "$SRC" "$DEST"; rm -rf "$DEST/__pycache__"
for kv in "$@"; do
  K=${kv%%=*}; V=${kv#*=}
  python3 - "$DEST/doctrine.py" "$K" "$V" <<'PY'
import re, sys
p, k, v = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(p).read()
pat = re.compile(r'^(%s\s*=\s*)(\S+)' % re.escape(k), re.M)
n = len(pat.findall(s))
if n != 1:
    sys.exit("mkarm: %s matched %d definition sites in %s (need exactly 1)" % (k, n, p))
s = pat.sub(lambda m: m.group(1) + v, s, count=1)
open(p, 'w').write(s)
PY
done
