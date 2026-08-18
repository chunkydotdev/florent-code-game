#!/usr/bin/env python3
"""Instrument the COPY under diagC/arm with stderr diagnostics. Idempotent-ish:
run only on a fresh copy."""
import os
import sys

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arm")


def sub(path, old, new, n=1):
    p = os.path.join(D, path)
    s = open(p).read()
    assert s.count(old) == n, (path, s.count(old), old[:60])
    s = s.replace(old, new)
    open(p, "w").write(s)


# ---------------------------------------------------------------- eco.py
# 1. _eco_spendable: expose the FS reserve and the verdict.
sub("eco.py", """    def _eco_spendable(self, ct, cost):
        ti = ct.get_global_resources()""",
    """    def _eco_spendable(self, ct, cost):
        ti = ct.get_global_resources()
        _raw = ti
        _res = 0""")
sub("eco.py", """                    ti -= 8 * ct.get_barrier_cost() + FS_SEAL_MARGIN
            except Exception:
                pass""",
    """                    _res = 8 * ct.get_barrier_cost() + FS_SEAL_MARGIN
                    ti -= _res
            except Exception:
                pass
        self._dc_spend = (_raw, _res, cost, ti >= cost)""")

# 2. _build_next_link: why did it not fire.
sub("eco.py", """    def _build_next_link(self, ct):
        if not self.link_queue or not self._eco_spendable(ct, ct.get_conveyor_cost()):
            return False""",
    """    def _build_next_link(self, ct):
        import sys as _s
        if not self.link_queue:
            return False
        if not self._eco_spendable(ct, ct.get_conveyor_cost()):
            _r, _v, _c, _ = getattr(self, "_dc_spend", (0, 0, 0, 0))
            _h = self.link_queue[0]
            print("DIAGC BNL_POOR rnd=%d id=%d seat=%s ti=%d res=%d cost=%d "
                  "qlen=%d head=%d,%d dcore=%d" % (
                      ct.get_current_round(), ct.get_id(), self.role_n, _r, _v, _c,
                      len(self.link_queue), _h.x, _h.y, dist_core(_h, self.core)),
                  file=_s.stderr)
            return False""")
sub("eco.py", """        if ct.can_build_conveyor(tile, f):
            ct.build_conveyor(tile, f)
            self.link_queue.pop(0)
            return True
        return False""",
    """        if ct.can_build_conveyor(tile, f):
            ct.build_conveyor(tile, f)
            self.link_queue.pop(0)
            import sys as _s
            print("DIAGC BNL_OK rnd=%d id=%d seat=%s tile=%d,%d dcore=%d left=%d" % (
                ct.get_current_round(), ct.get_id(), self.role_n, tile.x, tile.y,
                dist_core(tile, self.core), len(self.link_queue)), file=_s.stderr)
            return True
        import sys as _s
        print("DIAGC BNL_ILLEGAL rnd=%d id=%d seat=%s tile=%d,%d dcore=%d" % (
            ct.get_current_round(), ct.get_id(), self.role_n, tile.x, tile.y,
            dist_core(tile, self.core)), file=_s.stderr)
        return False""")

# 3. _l4_repair: blocked by the reserve.
sub("eco.py", """        if not self._eco_spendable(ct, ct.get_conveyor_cost()):
            return False
        p = ct.get_position()
        px, py = p.x, p.y
        ban = self._pave_ban()""",
    """        if not self._eco_spendable(ct, ct.get_conveyor_cost()):
            _r, _v, _c, _ = getattr(self, "_dc_spend", (0, 0, 0, 0))
            if _v:
                import sys as _s
                print("DIAGC L4_POOR rnd=%d id=%d seat=%s ti=%d res=%d cost=%d" % (
                    ct.get_current_round(), ct.get_id(), self.role_n, _r, _v, _c),
                    file=_s.stderr)
            return False
        p = ct.get_position()
        px, py = p.x, p.y
        ban = self._pave_ban()""")
sub("eco.py", """                ct.build_conveyor(g, acc_dir)
            except Exception:
                continue""",
    """                ct.build_conveyor(g, acc_dir)
            except Exception:
                continue
            import sys as _s
            print("DIAGC L4_OK rnd=%d id=%d seat=%s tile=%d,%d dcore=%d feed=%s" % (
                ct.get_current_round(), ct.get_id(), self.role_n, g.x, g.y,
                dist_core(g, self.core), feeder), file=_s.stderr)""")

# 4. _expand: one line per eco turn, so idle bodies are countable.
sub("eco.py", """    def _expand(self, ct):
        p = ct.get_position()
        has_launch = ct.read_store(SLOT_LAUNCHER) != 0""",
    """    def _expand(self, ct):
        p = ct.get_position()
        import sys as _s
        print("DIAGC EXP rnd=%d id=%d seat=%s role=%s pos=%d,%d ti=%d acd=%d "
              "mcd=%d qlen=%d harv=%d" % (
                  ct.get_current_round(), ct.get_id(), self.role_n, self.role,
                  p.x, p.y, ct.get_global_resources(), ct.get_action_cooldown(),
                  ct.get_move_cooldown(), len(self.link_queue),
                  ct.read_store(SLOT_HARVESTERS)), file=_s.stderr)
        has_launch = ct.read_store(SLOT_LAUNCHER) != 0""")

# 5. harvester build
sub("eco.py", """                        ct.build_harvester(bp)
                        ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)""",
    """                        ct.build_harvester(bp)
                        import sys as _s
                        print("DIAGC HARV rnd=%d id=%d seat=%s tile=%d,%d" % (
                            ct.get_current_round(), ct.get_id(), self.role_n,
                            bp.x, bp.y), file=_s.stderr)
                        ct.write_store(SLOT_HARVESTERS, ct.read_store(SLOT_HARVESTERS) + 1)""")

# 6. link plan published
sub("eco.py", """            self.link_source = bp
            plan = self._link_path(ct, bp)
            self.link_queue = plan""",
    """            self.link_source = bp
            plan = self._link_path(ct, bp)
            self.link_queue = plan
            import sys as _s
            print("DIAGC PLAN rnd=%d id=%d seat=%s src=%d,%d len=%d" % (
                ct.get_current_round(), ct.get_id(), self.role_n, bp.x, bp.y,
                len(plan)), file=_s.stderr)""")

# ---------------------------------------------------------------- main.py
# 7. core: phase / budget / ti_floor each round.
sub("main.py", """        if ct.get_action_cooldown() != 0:
            return
        if self.n >= budget or units >= GameConstants.MAX_TEAM_UNITS - 2:
            return
        cost = ct.get_builder_bot_cost()""",
    """        import sys as _s
        print("DIAGC CORE rnd=%d ph=%d budget=%d n=%d ti=%d ammo=%d floor=%s "
              "acd=%d" % (
                  rnd, fs_ph, budget, self.n, ct.get_global_resources(),
                  ct.get_global_ammo(), ti_floor, ct.get_action_cooldown()),
              file=_s.stderr)
        if ct.get_action_cooldown() != 0:
            return
        if self.n >= budget or units >= GameConstants.MAX_TEAM_UNITS - 2:
            return
        cost = ct.get_builder_bot_cost()""")

print("patched")
