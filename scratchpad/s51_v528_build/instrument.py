#!/usr/bin/env python3
"""Inject the v526 M-METRIC TAPE into a COPY of a bot tree.

⛔ EVERY substitution asserts its own match count.  A patcher that silently
matched nothing is the failure mode that produced this build's first blind
instrument (the WALK tape emitted 0 lines across 5 games because `sys` is not
imported in eco.py and the print sat inside a bare `except Exception: pass`).

Tape lines, all stderr:
  RC MAP    w H h H ours x,y theirs x,y                 (once, from the Core)
  RC SEAT   <rnd> id <id> seat <n>                      (roster)
  RC POS    <rnd> id <id> seat n role r fs 0/1 body b pos x,y stuck s
  RC ECO    <rnd> harvstore <n> harvseen <n> ti <n> units <n> scale <f>
  RC TEMPO  <rnd> id .. body .. born .. lp .. must .. why .. ride .. ti ..
  RC HOP    <rnd> lid <launcher id> body <fs_body> at x,y dsq <d>
  RC THROW  <rnd> lid <launcher id> body <rider id> n <riders thrown so far>
  RC SPLIT  <rnd> lid <launcher id> body <rider id> arc <1 front|2 back>
  RC ARRIVE <rnd> id <id> body <b> dsq <d>              (once per body)

Usage: instrument.py <tree-dir>
"""
import ast
import sys
from pathlib import Path

MARK = "# --- s51 v526 M-METRIC TAPE ---"


def sub(s, old, new, n=1):
    got = s.count(old)
    assert got == n, "expected %d matches, got %d for:\n%s" % (n, got, old[:200])
    return s.replace(old, new)


def patch(tree):
    tree = Path(tree)
    assert tree.is_dir(), tree

    # ---- doctrine.py: the tape flag -------------------------------------
    d = (tree / "doctrine.py").read_text()
    assert MARK not in d, "already instrumented"
    d += ("\n\n" + MARK + "\nV526RC = True\nV526RC_MAXRND = 60\n")
    (tree / "doctrine.py").write_text(d)

    # ---- eco.py: `import sys` (absent in the parent -- see docstring) ----
    e = (tree / "eco.py").read_text()
    e = sub(e, "import math\nfrom collections import deque",
            "import math\nimport sys\nfrom collections import deque")
    (tree / "eco.py").write_text(e)

    # ---- main.py: roster seat, per-round position, eco census, map ------
    m = (tree / "main.py").read_text()
    m = sub(m,
            "            n = ct.read_store(SLOT_ROLE_N) & FS_ROLE_N_MASK\n"
            "            self.role_n = n\n",
            "            n = ct.read_store(SLOT_ROLE_N) & FS_ROLE_N_MASK\n"
            "            self.role_n = n\n"
            "            if V526RC:\n"
            "                try:\n"
            "                    print('RC SEAT', ct.get_current_round(),\n"
            "                          'id', ct.get_id(), 'seat', n,\n"
            "                          file=sys.stderr)\n"
            "                except Exception:\n"
            "                    pass\n")
    m = sub(m,
            "        if self.fs_raider and not self.fs_off:\n"
            "            self._fs_turn(ct)\n",
            "        if V526RC:\n"
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
            "        if self.map_grid is None:\n"
            "            self.map_grid = known_map_for(w, h, p, ct)\n",
            "        if self.map_grid is None:\n"
            "            self.map_grid = known_map_for(w, h, p, ct)\n"
            "        if V526RC:\n"
            "            try:\n"
            "                _r = ct.get_current_round()\n"
            "                if _r == 0:\n"
            "                    print('RC MAP', 'w', w, 'h', h,\n"
            "                          'ours', '%d,%d' % (p.x, p.y),\n"
            "                          'theirs', '%d,%d' % enemy_core_for(w, h, p),\n"
            "                          file=sys.stderr)\n"
            "                if _r <= V526RC_MAXRND or _r % 25 == 0:\n"
            "                    print('RC ECO', _r,\n"
            "                          'harvstore', ct.read_store(SLOT_HARVESTERS),\n"
            "                          'harvseen', -1,\n"
            "                          'ti', ct.get_global_resources(),\n"
            "                          'units', ct.get_unit_count(),\n"
            "                          'scale', ct.get_scale_percent(),\n"
            "                          file=sys.stderr)\n"
            "            except Exception:\n"
            "                pass\n")
    (tree / "main.py").write_text(m)

    # ---- siege.py: tempo, hop (with the launcher ID), throws, arrival ---
    s = (tree / "siege.py").read_text()
    s = sub(s,
            "        if self.fs_body_born is None:\n"
            "            self.fs_body_born = rnd\n",
            "        if self.fs_body_born is None:\n"
            "            self.fs_body_born = rnd\n"
            "        if V526RC and rnd <= V526RC_MAXRND:\n"
            "            try:\n"
            "                _m = self._fs_relay_mustered(ct, p, rnd)\n"
            "                print('RC TEMPO', rnd, 'id', ct.get_id(),\n"
            "                      'body', getattr(self, 'fs_body', 1),\n"
            "                      'born', self.fs_body_born,\n"
            "                      'lp', 1 if lp is not None else 0,\n"
            "                      'must', 1 if _m else 0,\n"
            "                      'why', getattr(self, 'v526_must_why', '-'),\n"
            "                      'ride', self.fs_ride_rnd,\n"
            "                      'ti', ct.get_global_resources(),\n"
            "                      'lcost', ct.get_launcher_cost(),\n"
            "                      'acd', ct.get_action_cooldown(),\n"
            "                      'mcd', ct.get_move_cooldown(),\n"
            "                      'pos', '%d,%d' % (p.x, p.y),\n"
            "                      'dsq', dsq_core(p, E), file=sys.stderr)\n"
            "            except Exception:\n"
            "                pass\n")
    # muster reasons
    s = sub(s, "        if rnd - self.fs_body_born >= ",
            "        self.v526_must_why = 'waitexp'\n"
            "        if rnd - self.fs_body_born >= ")
    s = sub(s,
            "        if not rid:\n"
            "            return False                     # body 2 has not reported at all\n",
            "        if not rid:\n"
            "            self.v526_must_why = 'norid'\n"
            "            return False                     # body 2 has not reported at all\n")
    s = sub(s,
            "                return ct.get_position(eid).distance_squared(p) <= FS_MUSTER_DSQ\n",
            "                _dd = ct.get_position(eid).distance_squared(p)\n"
            "                self.v526_must_why = 'near%d' % _dd\n"
            "                return _dd <= FS_MUSTER_DSQ\n")
    # hop build: capture the launcher entity id
    s = sub(s,
            "        try:\n"
            "            ct.build_launcher(best)\n"
            "        except Exception:\n"
            "            return False\n"
            "        self._fs_draw_dot(ct, best, 0, 200, 255)\n",
            "        try:\n"
            "            _lid = ct.build_launcher(best)\n"
            "        except Exception:\n"
            "            return False\n"
            "        self._fs_draw_dot(ct, best, 0, 200, 255)\n"
            "        if V526RC:\n"
            "            try:\n"
            "                print('RC HOP', ct.get_current_round(),\n"
            "                      'lid', _lid,\n"
            "                      'body', getattr(self, 'fs_body', 1),\n"
            "                      'at', '%d,%d' % (best.x, best.y),\n"
            "                      'dsq', dsq_core(best, E) if E is not None else -1,\n"
            "                      file=sys.stderr)\n"
            "            except Exception:\n"
            "                pass\n")
    # split throw
    s = sub(s,
            "                            if site is not None:\n"
            "                                self.v520_split_n += 1\n"
            "                                self.fs_thrown.append(me_id)\n",
            "                            if site is not None:\n"
            "                                self.v520_split_n += 1\n"
            "                                self.fs_thrown.append(me_id)\n"
            "                                if V526RC:\n"
            "                                    try:\n"
            "                                        print('RC SPLIT', rnd,\n"
            "                                              'lid', ct.get_id(),\n"
            "                                              'body', me_id,\n"
            "                                              'arc', arc,\n"
            "                                              'n', len(self.fs_thrown),\n"
            "                                              file=sys.stderr)\n"
            "                                    except Exception:\n"
            "                                        pass\n")
    # ordinary throw
    s = sub(s,
            "                if thrown:\n"
            "                    self.fs_thrown.append(me_id)\n",
            "                if thrown:\n"
            "                    self.fs_thrown.append(me_id)\n"
            "                    if V526RC:\n"
            "                        try:\n"
            "                            print('RC THROW', rnd,\n"
            "                                  'lid', ct.get_id(),\n"
            "                                  'body', me_id,\n"
            "                                  'n', len(self.fs_thrown),\n"
            "                                  file=sys.stderr)\n"
            "                        except Exception:\n"
            "                            pass\n")
    # ring arrival, once per body
    s = sub(s,
            "    def _fs_ferry_turn(self, ct, E, p, rnd):\n",
            "    def _v526_arrive(self, ct, E, p, rnd):\n"
            "        if not V526RC or getattr(self, 'v526_arrived', False):\n"
            "            return\n"
            "        try:\n"
            "            _d = dsq_core(p, E)\n"
            "        except Exception:\n"
            "            return\n"
            "        if _d > FS_RING_DSQ:\n"
            "            return\n"
            "        self.v526_arrived = True\n"
            "        try:\n"
            "            print('RC ARRIVE', rnd, 'id', ct.get_id(),\n"
            "                  'body', getattr(self, 'fs_body', 1),\n"
            "                  'dsq', _d, file=sys.stderr)\n"
            "        except Exception:\n"
            "            pass\n"
            "\n"
            "    def _fs_ferry_turn(self, ct, E, p, rnd):\n")
    (tree / "siege.py").write_text(s)

    # ARRIVE hook: call it from the ferry-siege turn head
    s = (tree / "siege.py").read_text()
    s = sub(s,
            "        p = ct.get_position()\n"
            "        d = dsq_core(p, E)\n",
            "        p = ct.get_position()\n"
            "        d = dsq_core(p, E)\n"
            "        if V526RC:\n"
            "            self._v526_arrive(ct, E, p, rnd)\n")
    (tree / "siege.py").write_text(s)

    for f in ("doctrine.py", "eco.py", "main.py", "siege.py", "raid.py"):
        ast.parse((tree / f).read_text())
    print("INSTRUMENTED %s (AST OK on 5 modules)" % tree)


if __name__ == "__main__":
    patch(sys.argv[1])
