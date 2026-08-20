#!/usr/bin/env python3
"""Inject the v528 M4 WALK TAPE into a COPY of a bot tree, and switch on the
in-tree M5 CONN tape.

⛔ EVERY substitution asserts its own match count -- the v526 lesson: a patcher
that silently matched nothing produced a blind instrument whose tape read as
"no stalls" (`BUILD-REPORT-v526transit` §7).  `sub()` raises rather than
returning an unmodified string.

⛔ SECOND v526 LESSON, AND IT IS WHY `import sys` IS PATCHED IN: eco.py does NOT
import sys, so a `print(..., file=sys.stderr)` inside a bare `except: pass`
raises NameError, is swallowed, and the tape is empty while looking healthy.

Tape lines (stderr), deliberately the SAME NAMES the v526 scanner reads, so
`stallscan2.py` runs on this build's tapes unmodified:
  RC MAP  w H h H ours x,y theirs x,y                    (once, from the Core)
  RC POS  <rnd> id <id> seat n role r fs 0/1 body b pos x,y stuck s
  RC WALK <rnd> id <id> role r pos x,y tgt x,y want <dir>

The M5 CONN tape is already in the shipped tree behind `FS_V528_LOG`; this
patcher only flips that flag, so the instrumented and fired code paths are the
same code.

Usage: instrument528.py <tree-dir>
"""
import sys
from pathlib import Path

MARK = "# --- s51 v528 M-METRIC TAPE ---"


def sub(s, old, new, n=1):
    got = s.count(old)
    assert got == n, "expected %d matches, got %d for:\n%s" % (n, got, old[:200])
    return s.replace(old, new)


def flag(s, name, value):
    import re
    pat = re.compile(r'^(%s\s*=\s*)(\S+)' % re.escape(name), re.M)
    got = len(pat.findall(s))
    assert got == 1, "flag %s matched %d definition sites" % (name, got)
    return pat.sub(lambda m: m.group(1) + value, s, count=1)


def patch(tree):
    tree = Path(tree)
    assert tree.is_dir(), tree

    d = (tree / "doctrine.py").read_text()
    assert MARK not in d, "already instrumented"
    d = flag(d, "FS_V528_LOG", "True")          # the in-tree M5 CONN tape
    d += ("\n\n" + MARK + "\nV528RC = True\n")
    (tree / "doctrine.py").write_text(d)

    # ---- eco.py: `import sys` (absent in the parent) + the WALK tape -----
    e = (tree / "eco.py").read_text()
    # ⭐ `import sys` is now IN THE SHIPPED TREE (v528 added it precisely so the
    # v526 NameError-in-a-bare-except trap cannot recur), so this patcher no
    # longer injects it -- it ASSERTS it instead.  A tree without it would give
    # a silently empty tape.
    assert "\nimport sys" in e, "eco.py does not import sys -- tape would be blind"
    e = sub(e,
            "    def _nav(self, ct, pave=True):\n"
            "        if self.tgt is None or ct.get_move_cooldown() != 0:\n"
            "            return\n"
            "        desired = self._bfs_direction(ct, self.tgt)\n",
            "    def _nav(self, ct, pave=True):\n"
            "        if self.tgt is None or ct.get_move_cooldown() != 0:\n"
            "            return\n"
            "        desired = self._bfs_direction(ct, self.tgt)\n"
            "        if V528RC:\n"
            "            try:\n"
            "                _p = ct.get_position()\n"
            "                print('RC WALK', ct.get_current_round(),\n"
            "                      'id', ct.get_id(), 'role', self.role,\n"
            "                      'pos', '%d,%d' % (_p.x, _p.y),\n"
            "                      'tgt', '%d,%d' % (self.tgt.x, self.tgt.y),\n"
            "                      'want', desired.name, file=sys.stderr)\n"
            "            except Exception:\n"
            "                pass\n")
    (tree / "eco.py").write_text(e)

    # ---- main.py: RC MAP once, RC POS every round -----------------------
    m = (tree / "main.py").read_text()
    m = sub(m,
            "            self.role_n = n\n",
            "            self.role_n = n\n"
            "            if V528RC:\n"
            "                try:\n"
            "                    print('RC SEAT', ct.get_current_round(),\n"
            "                          'id', ct.get_id(), 'seat', n,\n"
            "                          file=sys.stderr)\n"
            "                except Exception:\n"
            "                    pass\n")
    m = sub(m,
            "        if self.fs_raider and not self.fs_off:\n"
            "            self._fs_turn(ct)\n",
            "        if V528RC:\n"
            "            try:\n"
            "                print('RC POS', ct.get_current_round(),\n"
            "                      'id', ct.get_id(), 'seat', self.role_n,\n"
            "                      'role', self.role,\n"
            "                      'fs', 1 if self.fs_raider else 0,\n"
            "                      'body', getattr(self, 'fs_body', 1),\n"
            "                      'pos', '%d,%d' % (p.x, p.y),\n"
            "                      'stuck', getattr(self, 'stuck', 0),\n"
            "                      file=sys.stderr)\n"
            "            except Exception:\n"
            "                pass\n"
            "        if self.fs_raider and not self.fs_off:\n"
            "            self._fs_turn(ct)\n")
    m = sub(m,
            "            self.map_grid = known_map_for(w, h, p, ct)\n",
            "            self.map_grid = known_map_for(w, h, p, ct)\n"
            "        if V528RC:\n"
            "            try:\n"
            "                if ct.get_current_round() == 0:\n"
            "                    print('RC MAP', 'w', w, 'h', h,\n"
            "                          'ours', '%d,%d' % (p.x, p.y),\n"
            "                          'theirs', '%d,%d' % enemy_core_for(w, h, p),\n"
            "                          file=sys.stderr)\n"
            "            except Exception:\n"
            "                pass\n")
    (tree / "main.py").write_text(m)
    print("instrumented", tree)


if __name__ == "__main__":
    patch(sys.argv[1])
