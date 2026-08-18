#!/usr/bin/env python3
import collections
import os
import pickle
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
rows, meta = pickle.load(open(os.path.join(HERE, "rows.pkl"), "rb"))


def med(v):
    return statistics.median(v) if v else None


def block(sel, name):
    print("\n" + "=" * 118)
    print("### %s   n=%d deaths" % (name, len(sel)))
    print("=" * 118)
    hdr = ("tag             id   born died dpos      d2ec  killer     kpos      fatalR fd2  penR pd2  "
           "warn gap dmgR hits VIS minD2 firstD2 raySame rayAny hpPen atHP retreat")
    print(hdr)
    for r in sel:
        print("%-15s %-4d %-4d %-4d %-9s %-5s %-10s %-9s %-6s %-4s %-4s %-4s %-4s %-3s %-4s %-4s %-3s %-5s %-7s %-7s %-6s %-5s %-4s %s" % (
            r["tag"], r["rid"], r["born"], r["died"], str(r["deathpos"]), r["d2_to_ecore"],
            r["killer_kind"], str(r["killer_pos"]), r["fatal_rnd"], r["fatal_d2"],
            r["pen_rnd"], r["pen_d2"], r["warn_first"], r["gap_pen_fatal"],
            r["n_dmg_rounds_before"], r["n_hits"],
            "Y" if r["vis_ever"] else "n", r["vis_min"], r["d2_firstdmg"],
            r["ray_same"], r["ray_any"], r["hp_after_pen"], r["rounds_at_hp"],
            r["retreat_steps"]))

    print("\n-- SUMMARY (n=%d)" % len(sel))
    kk = collections.Counter(r["killer_kind"] for r in sel)
    print("   killer kind: %s" % dict(kk))
    fd = [r["fatal_d2"] for r in sel if r["fatal_d2"] is not None]
    print("   fatal-shot d2 (n=%d): min=%s median=%s max=%s   values=%s" %
          (len(fd), min(fd) if fd else None, med(fd), max(fd) if fd else None, sorted(fd)))
    pd = [r["pen_d2"] for r in sel if r["pen_d2"] is not None]
    print("   penultimate-hit d2 (n=%d): min=%s median=%s max=%s" %
          (len(pd), min(pd) if pd else None, med(pd), max(pd) if pd else None))
    ve = [r for r in sel if r["killer_pos"]]
    never = [r for r in ve if not r["vis_ever"]]
    print("   killer NEVER inside raider vision (d2<=20) in the 10 rounds before the fatal shot: %d/%d (%.0f%%)"
          % (len(never), len(ve), 100.0 * len(never) / len(ve) if ve else 0))
    vm = [r["vis_min"] for r in ve if r["vis_min"] is not None]
    print("   min d2 raider->killer over that 10-round window: min=%s median=%s max=%s" %
          (min(vm) if vm else None, med(vm), max(vm) if vm else None))
    warn2 = [r for r in sel if r["gap_pen_fatal"] is not None and r["gap_pen_fatal"] >= 2]
    warn1 = [r for r in sel if r["gap_pen_fatal"] == 1]
    warn0 = [r for r in sel if r["gap_pen_fatal"] is None]
    print("   >=2 rounds between penultimate and fatal hit (i.e. >=1 free own-turn): %d/%d" % (len(warn2), len(sel)))
    print("   exactly 1 round gap: %d ; NO earlier hit at all (one-shot / first-blood kill): %d"
          % (len(warn1), len(warn0)))
    gaps = [r["gap_pen_fatal"] for r in sel if r["gap_pen_fatal"] is not None]
    print("   pen->fatal gap: %s" % collections.Counter(gaps))
    wf = [r["warn_first"] for r in sel if r["warn_first"] is not None]
    print("   first-ever-hit -> death gap (rounds): min=%s median=%s max=%s  dist=%s"
          % (min(wf) if wf else None, med(wf), max(wf) if wf else None, collections.Counter(wf)))
    dr = [r["n_dmg_rounds_before"] for r in sel]
    print("   distinct damage rounds BEFORE the fatal round: %s" % collections.Counter(dr))
    nh = [r["n_hits"] for r in sel]
    print("   total damaging events on the raider: %s" % collections.Counter(nh))
    rs = collections.Counter(r["ray_same"] for r in sel)
    ra = collections.Counter(r["ray_any"] for r in sel)
    print("   fatal tile on a PREVIOUSLY-observed ray of the SAME turret: %s" % dict(rs))
    print("   fatal tile on a PREVIOUSLY-observed ray of ANY enemy turret: %s" % dict(ra))
    rt = [r["retreat_steps"] for r in sel if r["retreat_steps"] is not None]
    print("   cardinal steps to leave the killer's attack range (from the penultimate-hit tile), n=%d: %s"
          % (len(rt), collections.Counter(rt)))
    rf = [r["retreat_from_fatal"] for r in sel if r["retreat_from_fatal"] is not None]
    print("   same, measured from the FATAL tile, n=%d: %s" % (len(rf), collections.Counter(rf)))
    esc = [r for r in sel if r["retreat_steps"] is not None and r["gap_pen_fatal"] is not None
           and r["retreat_steps"] <= r["gap_pen_fatal"]]
    print("   deaths where a straight retreat WOULD have fit in the pen->fatal gap "
          "(steps <= gap): %d/%d" % (len(esc), len([r for r in sel if r["retreat_steps"] is not None])))
    hp = [r["hp_after_pen"] for r in sel if r["hp_after_pen"] is not None]
    print("   HP after penultimate hit (n=%d): %s" % (len(hp), sorted(hp)))
    ath = [r["rounds_at_hp"] for r in sel if r["rounds_at_hp"] is not None]
    print("   rounds spent at that HP before dying: %s" % collections.Counter(ath))


raid = [r for r in rows if r["is_raider"]]
b_only = [r for r in rows if not r["is_raider"]]
block(raid, "SET A - RAIDERS (our builder_bots emitting draw indicators)")
block([r for r in rows if r["in_setB"]], "SET B - ALL our builder deaths with death pos d2<=60 from ENEMY core")
block(rows, "UNION (A or B)")
print("\n-- overlap: raiders that are also in setB: %d ; raiders NOT in setB (died far from enemy core): %d ; setB non-raiders: %d"
      % (len([r for r in rows if r["is_raider"] and r["in_setB"]]),
         len([r for r in rows if r["is_raider"] and not r["in_setB"]]),
         len([r for r in rows if r["in_setB"] and not r["is_raider"]])))
