#!/usr/bin/env python3
"""PLANK STATUS — does HANDOVER still agree with the plank's own artefacts?

    .venv/bin/python tools/plank_status.py loki17
    .venv/bin/python tools/plank_status.py --all
    .venv/bin/python tools/plank_status.py --selftest

RUN THIS BEFORE ANY ACTIVATION. It exits 1 when HANDOVER's claim about a plank
is older than the plank's own artefacts, which is the only state that matters.

===== WHY THIS EXISTS, AND IT IS A MEASURED INCIDENT, NOT A TIDINESS RULE =====
2026-08-11 06:0x. The s29 builder booted, read HANDOVER's top block, ran the
target-value gate, picked panel cells, verified the bot tree, and got within one
commit of ACTIVATING A PROTOTYPE for LOKI-17 -- a plank the s28 builder had
withdrawn five hours earlier at `c91c078`: *"No defect; LOKI-17 and LOKI-18 both
dead."* HANDOVER's block was written at 17:31, the kill landed at 22:03, and the
block was never updated.

**A HANDOVER BLOCK IS A CLAIM WITH AN EXPIRY DATE, AND THE ONE THING A SUCCESSOR
CANNOT DO IS NOTICE THAT IT EXPIRED.** The successor has no prior to compare
against -- that is the definition of a successor.

The catch came from the side lane reading the plank's git log while auditing
something else. That is the SECOND firing of drift-watch rule D14 and the second
one to be INCIDENTAL. Its enforcement row has said `attention -- MECHANISABLE`
since it was written. **A rule caught twice by luck is not enforced, it is being
got away with**, which is what this file is for.

===== THE DEFECT IS STRUCTURAL AND THIS TOOL ONLY MITIGATES IT =====
HANDOVER holds its own COPY of "what fires next". **A copy cannot be
stale-checked, only contradicted.** The real fix is one authoritative surface per
plank with every other mention a pointer to it. Until that exists, this compares
the two surfaces and shouts when they disagree. Do not mistake the mitigation for
the fix.

===== WHAT IT COMPARES =====
  newest commit touching the plank's own artefacts
      docs/prereg/*<plank>*  docs/legs/*<plank>*  bots/_v*<plank>*/**
  vs
  newest commit that changed a HANDOVER line CONTAINING the plank's name
      (`git log -S`, so a commit that edited HANDOVER elsewhere does not count
       as having refreshed this plank's claim)

Artefacts newer than the claim -> STALE -> exit 1. Any intervening commit
subject carrying a kill word is reported verbatim, because that is the case that
costs a window.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Words that have actually retired a plank in this repo's log. Matched on commit
# SUBJECTS only. This list is a convenience for the human reading the output --
# the STALE verdict never depends on it, because a plank can die in a commit
# whose subject says none of these, and a subject can say "dead" about something
# else entirely. The verdict is the timestamp comparison; this is the annotation.
KILL_WORDS = ("dead", "kill", "withdraw", "retire", "abandon", "null",
              "superseded", "off-programme", "stand down", "struck")


def git(*args, cwd=ROOT):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


def artefact_paths(plank, cwd=ROOT):
    """Every tracked file whose path mentions the plank. Uses git's own index
    rather than a glob so that an untracked scratch file cannot masquerade as a
    durable artefact -- which is the exact class of defect that let an untracked
    `scratchpad/shootable.py` produce the number that killed LOKI-17."""
    out = git("ls-files", cwd=cwd).splitlines()
    p = plank.lower()
    return [f for f in out
            if p in f.lower() and (f.startswith("docs/") or f.startswith("bots/"))]


def newest_commit(paths, cwd=ROOT):
    if not paths:
        return None
    line = git("log", "-1", "--format=%h\t%at\t%ad\t%s", "--date=iso",
               "--", *paths, cwd=cwd)
    if not line:
        return None
    h, at, ad, subj = line.split("\t", 3)
    return {"hash": h, "at": int(at), "date": ad, "subject": subj}


def newest_handover_mention(plank, cwd=ROOT, handover="HANDOVER.md"):
    """Last commit that added or removed a HANDOVER line containing `plank`.

    Scoping to lines that NAME the plank is deliberate. `git log -- HANDOVER.md`
    would report any HANDOVER edit as though it had refreshed every plank's
    claim, which is precisely the false-negative that makes this tool worthless:
    HANDOVER is edited constantly and almost never about the plank you are
    asking about.

    ⚠ `-G`, NOT `-S`, AND THE SELFTEST IS WHY. `-S` is the pickaxe: it fires only
    when the NUMBER of occurrences of the string changes. Rewriting
    "lokiXX is ready to fire" into "lokiXX IS DEAD" leaves the count at one, so
    `-S` did not see the very edit that records a death -- the tool then called
    a correctly-updated HANDOVER stale forever, and an alarm that cannot be
    satisfied is one everybody learns to ignore. `-G` matches any added or
    removed line containing the pattern, which is the actual question."""
    line = git("log", "-1", "-i", f"-G{plank}", "--format=%h\t%at\t%ad\t%s",
               "--date=iso", "--", handover, cwd=cwd)
    if not line:
        return None
    h, at, ad, subj = line.split("\t", 3)
    return {"hash": h, "at": int(at), "date": ad, "subject": subj}


def commits_since(paths, since_hash, cwd=ROOT):
    """Commits touching `paths` that are strictly NEWER than `since_hash`, by
    COMMIT ORDER rather than by timestamp.

    ⚠ THIS WAS A TIMESTAMP COMPARISON AND THE SELFTEST CAUGHT IT. Two commits
    made in the same second compared EQUAL, so a plank killed moments after a
    HANDOVER edit read OK -- the tool's one job, failed on the one case that
    costs a window. Worse, the tie resolves toward silence, which is the
    direction you cannot notice. `<hash>..HEAD` is exact: it asks whether any
    such commit exists in history after that point, and a commit that changed
    BOTH HANDOVER and the artefacts is correctly excluded (it is the boundary,
    not after it)."""
    if not paths:
        return []
    out = git("log", f"{since_hash}..HEAD", "--format=%h\t%ad\t%s",
              "--date=iso", "--", *paths, cwd=cwd)
    rows = []
    for line in out.splitlines():
        if not line.strip():
            continue
        h, ad, subj = line.split("\t", 2)
        rows.append({"hash": h, "date": ad, "subject": subj})
    return rows


def check(plank, cwd=ROOT, handover="HANDOVER.md", quiet=False):
    """-> (verdict, detail). verdict in {"STALE", "OK", "NO-ARTEFACTS",
    "UNMENTIONED"}. Only STALE exits 1."""
    paths = artefact_paths(plank, cwd=cwd)
    art = newest_commit(paths, cwd=cwd)
    men = newest_handover_mention(plank, cwd=cwd, handover=handover)

    def say(*a):
        if not quiet:
            print(*a)

    say(f"\n=== {plank} ===")
    if art is None:
        say("  no tracked artefacts under docs/ or bots/ -- nothing to compare")
        return "NO-ARTEFACTS", None
    say(f"  newest artefact  {art['hash']}  {art['date']}  {art['subject'][:88]}")
    say(f"    ({len(paths)} tracked path(s): {', '.join(paths[:3])}"
        f"{' ...' if len(paths) > 3 else ''})")
    if men is None:
        say(f"  {handover} has NEVER mentioned this plank.")
        say("  -> not stale, but nothing points at it either. If it is live, say so there.")
        return "UNMENTIONED", None
    say(f"  newest HANDOVER  {men['hash']}  {men['date']}  {men['subject'][:88]}")

    later = commits_since(paths, men["hash"], cwd=cwd)
    if not later:
        say("  OK -- no artefact commit lands after HANDOVER last named this plank.")
        return "OK", None

    say("")
    say("  *** STALE: the plank moved AFTER HANDOVER last spoke about it. ***")
    say(f"  {len(later)} commit(s) touched its artefacts since {men['hash']}:")
    flagged = []
    for c in later:
        low = c["subject"].lower()
        hit = [w for w in KILL_WORDS if w in low]
        mark = "  <== " + "/".join(hit).upper() if hit else ""
        if hit:
            flagged.append(c)
        say(f"      {c['hash']}  {c['date']}  {c['subject'][:76]}{mark}")
    if flagged:
        say("")
        say("  ONE OF THOSE SUBJECTS READS LIKE A RETIREMENT. Read it before you activate.")
    say("  Verify against the artefacts, not against HANDOVER, then update HANDOVER.")
    return "STALE", later


def discover_planks(cwd=ROOT):
    names = set()
    for f in git("ls-files", cwd=cwd).splitlines():
        for m in re.finditer(r"(loki\d+[a-z]?)", f.lower()):
            names.add(m.group(1))
    return sorted(names, key=lambda s: (len(s), s))


# --------------------------------------------------------------------------
# SELFTEST. Builds a throwaway git repo and drives the checker to BOTH verdicts.
# A check that has never produced the other verdict has not been seen to check --
# and this tool's failure mode is silence, which is indistinguishable from health.
def selftest():
    import tempfile, os
    ok = True

    def run(cwd, *a):
        subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        run(d, "init", "-q", "-b", "main")
        run(d, "config", "user.email", "t@t")
        run(d, "config", "user.name", "t")
        (d / "docs" / "prereg").mkdir(parents=True)
        (d / "bots" / "_v999lokiXX").mkdir(parents=True)

        # t0: plank created, HANDOVER announces it. -> OK
        (d / "docs/prereg/PREREG-lokiXX.md").write_text("bar: >85%\n")
        (d / "bots/_v999lokiXX/main.py").write_text("x = 1\n")
        (d / "HANDOVER.md").write_text("NEXT: lokiXX is built and ready to fire.\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "create lokiXX and announce it in HANDOVER")

        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "OK":
            print(f"  [FAIL] fresh plank should read OK, read {v}"); ok = False
        else:
            print("  [ok] plank announced and unchanged since        -> OK")

        # t1: the plank is KILLED and HANDOVER is not touched. -> STALE
        os.utime(d / "docs/prereg/PREREG-lokiXX.md")
        (d / "docs/prereg/PREREG-lokiXX.md").write_text("bar: >85%\nWITHDRAWN\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "No defect; lokiXX is dead")

        v, later = check("lokiXX", cwd=d, quiet=True)
        if v != "STALE":
            print(f"  [FAIL] killed-but-unannounced should read STALE, read {v}"); ok = False
        else:
            subj = " ".join(c["subject"].lower() for c in later)
            if not any(w in subj for w in KILL_WORDS):
                print("  [FAIL] STALE but the kill word was not surfaced"); ok = False
            else:
                print("  [ok] plank killed, HANDOVER silent            -> STALE + kill word")

        # t2: HANDOVER is updated to record the death. -> back to OK.
        # This is the branch that matters most: if the tool cannot be SATISFIED,
        # it becomes an alarm everyone learns to ignore.
        (d / "HANDOVER.md").write_text("lokiXX IS DEAD -- withdrawn, do not fire.\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "HANDOVER: record that lokiXX is dead")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "OK":
            print(f"  [FAIL] after HANDOVER records the death it must clear, read {v}"); ok = False
        else:
            print("  [ok] HANDOVER updated to match                -> OK again")

        # t3: a HANDOVER edit that does NOT mention the plank must NOT clear it.
        # This is the false-negative the `-S` flag exists to prevent, and without
        # it the tool would silently pass every plank on any HANDOVER commit.
        (d / "docs/prereg/PREREG-lokiXX.md").write_text("bar: >85%\nWITHDRAWN\nmore\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "touch lokiXX artefacts again")
        (d / "HANDOVER.md").write_text(
            "lokiXX IS DEAD -- withdrawn, do not fire.\nUnrelated: monitors are alive.\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "HANDOVER: unrelated monitor note")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "STALE":
            print(f"  [FAIL] a HANDOVER edit not mentioning the plank must not clear it, read {v}")
            ok = False
        else:
            print("  [ok] unrelated HANDOVER edit does not clear   -> STALE")

    print("\nPASS: drives OK -> STALE -> OK, surfaces the kill word, and an edit "
          "that does not name the plank does not clear it."
          if ok else "\n*** SELFTEST FAILED ***")
    return 0 if ok else 1


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--selftest":
        return selftest()
    planks = discover_planks() if argv[0] == "--all" else argv
    worst = 0
    stale = []
    for p in planks:
        v, _ = check(p)
        if v == "STALE":
            worst = 1
            stale.append(p)
    if stale:
        print(f"\n*** {len(stale)} STALE: {', '.join(stale)} ***")
        print("Do not activate against HANDOVER's word until these are reconciled.")
    return worst


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
