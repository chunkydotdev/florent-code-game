#!/usr/bin/env python3
"""PLANK STATUS — does HANDOVER still agree with the plank's own artefacts?

    .venv/bin/python tools/plank_status.py loki17
    .venv/bin/python tools/plank_status.py --all
    .venv/bin/python tools/plank_status.py --selftest

IMPLEMENTS: D41 (a plank's death is written in the same commit that kills it),
D50 (gate on the printed token, never on `$?`), D52 (a false-positive first
firing trains an alarm away).

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

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

ROOT = Path(__file__).resolve().parent.parent

# Words that have actually retired a plank in this repo's log. Matched on commit
# SUBJECTS only.
#
# ⛔ THESE ARE NOW LOAD-BEARING, s30 2026-08-11, AND THE PARAGRAPH THAT USED TO
# SIT HERE SAID THE OPPOSITE: "the STALE verdict never depends on it ... this is
# the annotation." That was true and it is exactly how this tool let a dead plank
# through.
#
# WHAT HAPPENED. LOKI-18 was retracted by its own author at `c91c078`
# 2026-08-10T22:03:16Z ("Corrected: raid.py sentinels are 100.0% shootable-on-
# build. No defect; LOKI-17 and LOKI-18 both dead") and re-confirmed dead at
# `38bc735` 06:08:40Z. At 06:45Z the builder submitted its tree and fired 25
# unrated games on it.
#
# **AND THIS TOOL WAS RUN AT BOOT AND SAID NOTHING**, because HANDOVER had never
# mentioned loki18, so `check()` returned UNMENTIONED and exited BEFORE reaching
# the kill-word scan -- which lived inside the STALE branch and nowhere else.
#
# **THE DEEPER DEFECT: THIS TOOL MEASURED STALENESS AND THE FAILURE MODE IS
# WITHDRAWAL. A withdrawal commit is just another artefact to a recency check, so
# `38bc735` ("LOKI-17/18 ARE DEAD") made the plank look FRESHER, NOT DEADER.**
# It was built after s29 got one commit from activating a withdrawn plank; s30
# then fired one THROUGH it.
#
# So the scan now runs over the plank's WHOLE artefact history, independent of
# HANDOVER, and produces its own non-OK verdict. False positives are the intended
# direction: a subject can say "dead" about something else, and the cost of
# reading one extra commit is nothing against the cost of firing on a retracted
# premise.
# ⛔ PATTERNS, NOT SUBSTRINGS, AND BOTH FORMS OF THAT MISTAKE WERE MADE HERE
# WITHIN TEN MINUTES OF EACH OTHER. The first cut of this guard matched bare
# substrings against commit subjects and produced, on its very first `--all`:
#
#   FALSE POSITIVE: `loki13` -- OUR LIVE SHIPPED INCUMBENT -- read WITHDRAWN,
#   because "LOKI-13 POOLED n=100/100: +18.0pp core_kill_share HELD" contains
#   the substring `kill`. **`core_kill_share` is the PRIMARY CURRENCY OF THIS
#   PROJECT and appears in nearly every verdict we write.** A guard that flags
#   the live bot on its first run is the "alarm trained away" failure this file
#   already documents against itself, one section up.
#
#   FALSE NEGATIVE, worse: the commit that marked LOKI-18 VOID-ON-PREMISE read
#   as a REVIVAL, because its subject contains "reinstated" -- describing the
#   very mistake it was recording. **The document declaring a plank dead cleared
#   the plank's death.**
#
# So: kill patterns are word-boundary regexes chosen to be rare in ordinary
# verdict prose (`kill` and `null` are dropped outright -- `core_kill_share`,
# `kill-speed`, "a null is an iteration"), and REVIVAL REQUIRES AN EXPLICIT
# UPPERCASE TOKEN that cannot occur by accident. The asymmetry is deliberate:
# a missed withdrawal costs a window fired on a retracted premise, a spurious
# one costs reading a commit message.
KILL_PATTERNS = [
    r"\bis dead\b", r"\bare dead\b", r"\bboth dead\b", r"\bnow dead\b",
    r"\bwithdrawn\b", r"\bwithdraw\b", r"\bwithdrew\b",
    r"\bretract(?:ed|ion|ions|s)?\b",
    r"\bretir(?:e|ed|es|ing|ement)\b",
    r"\babandon(?:ed|ing)?\b",
    r"\bsupersed(?:e|ed|es)\b",
    r"\bvoid\b", r"\bstand down\b", r"\boff-programme\b",
    r"\bstruck\b", r"\binert\b",
]
_KILL_RE = [(p, re.compile(p, re.I)) for p in KILL_PATTERNS]

# The ONLY thing that clears a withdrawal. Case-sensitive and deliberately ugly:
# reviving a dead plank is a decision that belongs on the record as a decision,
# not something inferred from a commit that happens to use the word "reopen".
REVIVAL_TOKEN = "PLANK-REVIVED"

# ⛔ AND PROSE ALONE CANNOT CARRY THIS VERDICT. Measured on the first `--all`
# after the patterns were tightened: SIX planks flagged, THREE of them false:
#   loki16b  "WITHDRAW the +0.017: ring_retention.py does NOT reproduce LOKI-16"
#            -- withdrew a NUMBER; the plank cleared its bar the next morning
#   loki9    "PREREG LOKI-9 ... supersedes forward-survival"
#            -- this plank supersedes something ELSE; wrong grammatical direction
#   loki11   "the saturated cells are INERT CONSTANTS"
#            -- "inert" describes the CELLS, not the plank
# **A 50% false-positive rate is how an alarm gets trained away, which this file
# already documents as its own failure mode two sections up.** A subject line
# carries the word but not what the word is ABOUT, and no regex fixes that.
#
# So the flag is a SUSPICION that must be RESOLVED ONCE, on the record:
#   * `PLANK-DEAD` in a commit subject  -> WITHDRAWN outright, no ack needed.
#   * a prose match                     -> SUSPECT until acknowledged in
#                                          tools/plank_ack.tsv, which records
#                                          plank, commit, verdict and reason.
# A dismissal is then a decision someone typed, not a judgement re-made silently
# by every successor. New flags stay loud because old ones stop shouting.
KILL_TOKEN = "PLANK-DEAD"
ACK_FILE = ROOT / "tools" / "plank_ack.tsv"


def load_acks(cwd=ROOT):
    """-> {(plank, commit_hash): (verdict, note)}. Missing file = no acks."""
    f = Path(cwd) / "tools" / "plank_ack.tsv"
    acks = {}
    if not f.exists():
        return acks
    for line in f.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        acks[(parts[0].strip(), parts[1].strip())] = (parts[2].strip(),
                                                      parts[3] if len(parts) > 3 else "")
    return acks

# Kept for the report annotation and for callers that still import it.
KILL_WORDS = ("dead", "withdrawn", "retract", "retire", "abandon",
              "superseded", "void", "inert")


def git(*args, cwd=ROOT):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


# Mirror//probe trees: a DETERMINISTIC COPY of a plank, created to serve as some
# OTHER plank's paired control. `_det_v130loki13` is a copy of loki13 made by a
# LOKI-17 commit; `_v126loki9off` is an ablation arm.
#
# ⛔ EXCLUDED BECAUSE THE GUARD'S FIRST AND ONLY LIVE FIRING WAS A FALSE POSITIVE.
# `--all` reported `1 STALE: loki13`, and the triggering commit was `1f6d779`,
# a LOKI-17 battery commit that CREATED `bots/_det_v130loki13/`. loki13 the plank
# had not moved at all -- somebody made a copy of it to test something else, and
# the path glob caught the copy. **The guard was reading "this tree was used as a
# CONTROL" as "this plank MOVED."**
#
# This is fixed rather than noted, and the reason is the whole point of the tool:
# it exists because attention failed twice, and AN ALARM WHOSE FIRST LIVE FIRING
# IS WRONG GETS TRAINED AWAY. The next `1 STALE: loki13` reads as "that again",
# and that is how the second real one gets skipped. Same family as a monitor that
# restarts on OK: a guard nobody believes is decoration with an exit code.
MIRROR_PREFIXES = ("bots/_det_", "bots/_probe_")
MIRROR_SUFFIXES = ("off",)


def _is_mirror(path):
    if path.startswith(MIRROR_PREFIXES):
        return True
    parts = path.split("/")
    return len(parts) > 1 and parts[1].endswith(MIRROR_SUFFIXES)


def artefact_paths(plank, cwd=ROOT, include_mirrors=False):
    """Every tracked file whose path mentions the plank. Uses git's own index
    rather than a glob so that an untracked scratch file cannot masquerade as a
    durable artefact -- which is the exact class of defect that let an untracked
    `scratchpad/shootable.py` produce the number that killed LOKI-17.

    Mirror trees are excluded (see MIRROR_PREFIXES): a deterministic copy of this
    plank, built as another plank's control, is not this plank moving."""
    out = git("ls-files", cwd=cwd).splitlines()
    p = plank.lower()
    # ⛔ WORD-BOUNDARY, NOT SUBSTRING. Plain `in` makes "loki1" match loki16,
    # loki17 and loki19, so ANY commit to a later plank reported loki1 STALE.
    # Caught at the s29 wrap by the tool's own --all run: `1 STALE: loki1` with
    # no loki1 artefact having moved in two days. A false positive is how an
    # alarm gets trained away, which is the failure this tool exists to prevent
    # -- so it is fixed rather than documented.
    pat = re.compile(rf"(?<![a-z0-9]){re.escape(p)}(?![a-z0-9])")
    hits = [f for f in out
            if pat.search(f.lower()) and (f.startswith("docs/") or f.startswith("bots/"))]
    if include_mirrors:
        return hits
    return [f for f in hits if not _is_mirror(f)]


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



def topic_slugs(plank, paths):
    """Distinct TOPIC slugs among a plank's doc artefacts.

    `PREREG-loki20-guns-not-walls-2026-08-11.md` and
    `PROPOSAL-loki20-healer-eviction-2026-08-11.md` share the plank name and are
    UNRELATED PLANKS. Two lanes committed exactly that 41 seconds apart on
    2026-08-11.
    """
    out = {}
    pat = re.compile(rf"{re.escape(plank.lower())}[-_]([a-z0-9-]+?)(?:-\d{{4}}-\d\d-\d\d)?\.md$")
    for f in paths:
        m = pat.search(f.lower())
        if m:
            out.setdefault(m.group(1), []).append(f)
    return out



def _is_pure_rename(sha, paths, cwd=ROOT):
    """True when this commit only RENAMED/MOVED the plank's artefacts.

    Uses git's own rename detection (`--name-status -M`) rather than reading the
    subject, because the subject is exactly what cannot be trusted here."""
    # Scoped to THIS plank's paths only. A commit may rename the plank's file
    # AND add an unrelated one in the same push -- the first live case did
    # exactly that -- so "every status line in the commit is R" is the wrong
    # test. The right one is "every line TOUCHING THIS PLANK is R".
    out = git("show", "--name-status", "-M", "--format=", sha, cwd=cwd)
    want = set(paths)
    st = []
    for ln in out.splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        if not any(f in want for f in parts[1:]):
            continue
        st.append(parts[0][:1])
    return bool(st) and all(x == "R" for x in st)


def withdrawal_state(paths, cwd=ROOT):
    """-> (killed_commit | None, revival_commit | None).

    Scans EVERY commit touching this plank's artefacts, newest first, for a
    subject that reads as a retirement. If one is found, looks for a LATER
    commit whose subject explicitly revives it. Both are returned so the caller
    can print the pair rather than a bare verdict.
    """
    out = git("log", "--format=%h\x1f%ad\x1f%s", "--date=format-local:%Y-%m-%d %H:%M:%S",
              "--", *paths, cwd=cwd)
    commits = []
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) != 3:
            continue
        commits.append({"hash": parts[0], "date": parts[1], "subject": parts[2]})
    killed = None
    killed_idx = None
    for i, c in enumerate(commits):          # newest first
        subj = c["subject"]
        # REVIVAL IS CHECKED FIRST, and it has to be: a revival commit almost
        # always NAMES the thing it is undoing, so it will also match a kill
        # pattern. Scanning kills first made such a commit its own withdrawal,
        # with nothing newer to clear it.
        if REVIVAL_TOKEN in subj:
            return None, c
        if KILL_TOKEN in subj:
            killed = dict(c, hits=[KILL_TOKEN], hard=True)
            killed_idx = i
            break
        hits = [pat for pat, rx in _KILL_RE if rx.search(subj)]
        if hits and _is_pure_rename(c["hash"], paths, cwd=cwd):
            # ⛔ A COMMIT THAT ONLY RENAMES OR MOVES A PLANK'S FILES CANNOT BE
            # RETIRING IT. Live false positive, 2026-08-11: a rename commit was
            # flagged because it contained the word "withdrawn" -- while
            # DESCRIBING this very gate. The heuristic cannot tell "this commit
            # withdraws the plank" from "this commit mentions the withdrawal
            # mechanism", and a sticky DEAD ack against that SUSPECT would have
            # killed a plank that had no tree, no prereg and no games.
            # The fail-safe asymmetry failing unsafe on a commit whose only sin
            # is talking about the gate.
            continue
        if hits:
            killed = dict(c, hits=hits, hard=False)
            killed_idx = i
            break
    if killed is None:
        return None, None
    # commits[:killed_idx] are strictly NEWER than the withdrawal. Unreachable
    # in practice because the newest-first loop returns on the token, but kept
    # so the function is correct if that loop is ever reordered.
    for c in reversed(commits[:killed_idx]):
        if REVIVAL_TOKEN in c["subject"]:
            return killed, c
    return killed, None


def check(plank, cwd=ROOT, handover="HANDOVER.md", quiet=False):
    """-> (verdict, detail). verdict in {"STALE", "OK", "NO-ARTEFACTS",
    "UNMENTIONED", "WITHDRAWN"}. STALE and WITHDRAWN exit 1."""
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

    # ⛔ NAME COLLISION. Two unrelated planks under one name is not cosmetic
    # once WITHDRAWN is a real gate: a withdrawal commit for either marks BOTH
    # dead (the LOKI-18 failure with the polarity reversed -- a LIVE plank
    # looking dead), and `plank_ack.tsv` keys on the NAME, so one DEAD ack
    # silences both. DEAD is STICKY by design, so **the asymmetry built to fail
    # safe fails UNSAFE under a collision.** Found 2026-08-11 when two lanes
    # committed different LOKI-20s 41 seconds apart.
    topics = topic_slugs(plank, paths)
    if len(topics) > 1:
        say("")
        say(f"  *** NAME COLLISION: {len(topics)} unrelated planks share the name "
            f"'{plank}'. ***")
        for t, fs in sorted(topics.items()):
            say(f"      {t:<28} {fs[0]}")
        say("  A withdrawal for either marks BOTH dead, and a DEAD ack in")
        say("  plank_ack.tsv silences both because it keys on the NAME.")
        say("  RENAME ONE BEFORE ACTING ON EITHER.")
        return "COLLISION", sorted(topics)

    # WITHDRAWAL CHECK -- runs FIRST, over the whole artefact history, and does
    # not depend on HANDOVER having ever mentioned the plank. That dependency is
    # precisely what let LOKI-18 through: no mention -> early return -> the scan
    # never ran. See KILL_WORDS.
    killed, revived = withdrawal_state(paths, cwd=cwd)
    # DEATH IS STICKY. Once a plank has been acknowledged DEAD for ANY commit,
    # later commits about it -- read-outs, post-mortems, HANDOVER blocks -- must
    # not re-open the question. Without this the ack is keyed so tightly that
    # writing up WHY a plank is dead re-flags it as merely SUSPECT, which reads
    # as a downgrade and is how the fix would have unwound itself.
    dead_acks = [(pl, h) for (pl, h), (v, _n) in load_acks(cwd=cwd).items()
                 if pl == plank and v == "DEAD"]
    if dead_acks and not revived:
        say("")
        say("  *** WITHDRAWN: acknowledged DEAD in tools/plank_ack.tsv "
            f"({', '.join(h for _p, h in dead_acks)}). ***")
        say("  DO NOT ACTIVATE, SUBMIT OR FIRE. A committed prereg and a built")
        say(f"  tree both survive a withdrawal. Clear only with {REVIVAL_TOKEN}.")
        return "WITHDRAWN", [killed] if killed else []
    if killed and not revived and not killed.get("hard"):
        verdict, note = load_acks(cwd=cwd).get((plank, killed["hash"]), (None, ""))
        if verdict == "NOT-A-WITHDRAWAL":
            say(f"  (a commit reads like a retirement and was reviewed and "
                f"dismissed: {killed['hash']} — {note.strip()})")
            killed = None
        elif verdict == "DEAD":
            killed = dict(killed, hard=True)
        else:
            say("")
            say("  *** SUSPECT: a commit for this plank READS LIKE a retirement, "
                "and prose cannot settle it. ***")
            say(f"      {killed['hash']}  {killed['date']}  {killed['subject'][:76]}")
            say(f"      matched: {', '.join(killed['hits'])}")
            say("  READ THAT COMMIT before you fire, then record the answer in")
            say(f"  tools/plank_ack.tsv:   {plank}\t{killed['hash']}\t"
                f"DEAD|NOT-A-WITHDRAWAL\t<why>")
            return "SUSPECT", [killed]
    if killed and not revived:
        say("")
        say("  *** WITHDRAWN: an artefact commit for this plank reads as a "
            "RETIREMENT and nothing later revives it. ***")
        say(f"      {killed['hash']}  {killed['date']}  {killed['subject'][:76]}")
        say(f"      matched: {', '.join(killed['hits'])}")
        say("  DO NOT ACTIVATE, SUBMIT OR FIRE THIS PLANK on the strength of a")
        say("  committed prereg or an existing bot tree -- both survive a")
        say("  withdrawal. To clear this, a later commit touching its artefacts")
        say(f"  must carry the explicit token {REVIVAL_TOKEN}.")
        return "WITHDRAWN", [killed]
    if killed and revived:
        say(f"  (withdrawn at {killed['hash']}, revived at {revived['hash']} — "
            f"proceeding)")

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

        # ⛔ EXPECTATION CHANGED s30: this now reads WITHDRAWN, not STALE, and the
        # change is the whole point of that revision. STALE says "HANDOVER is out
        # of date"; WITHDRAWN says "this plank is DEAD" -- and s30 fired 25
        # unrated games on a plank whose HANDOVER was merely SILENT, so silence
        # produced no STALE at all. WITHDRAWN does not depend on HANDOVER.
        v, later = check("lokiXX", cwd=d, quiet=True)
        if v != "SUSPECT":
            print(f"  [FAIL] killed plank should read SUSPECT, read {v}"); ok = False
        else:
            subj = " ".join(c["subject"].lower() for c in later)
            if not any(w in subj for w in KILL_WORDS):
                print("  [FAIL] SUSPECT but the kill word was not surfaced"); ok = False
            else:
                print("  [ok] prose kill, unacknowledged               -> SUSPECT + word")

        # t1-ack-a: acknowledging it DEAD hardens the verdict.
        (d / "tools").mkdir(exist_ok=True)
        kill_hash = later[0]["hash"]
        (d / "tools" / "plank_ack.tsv").write_text(
            f"lokiXX\t{kill_hash}\tDEAD\tits author said so\n")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "WITHDRAWN":
            print(f"  [FAIL] a DEAD ack must harden SUSPECT to WITHDRAWN, read {v}")
            ok = False
        else:
            print("  [ok] acknowledged DEAD                       -> WITHDRAWN")

        # t1-ack-b: THE OTHER DIRECTION. Acknowledging it NOT-A-WITHDRAWAL must
        # clear it — this is the branch that keeps the alarm believable, and its
        # real cases are loki9/loki11/loki16b, where the retirement word was
        # about a number, a fixture, or the wrong grammatical direction.
        (d / "tools" / "plank_ack.tsv").write_text(
            f"lokiXX\t{kill_hash}\tNOT-A-WITHDRAWAL\tit withdrew a number\n")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v in ("WITHDRAWN", "SUSPECT"):
            print(f"  [FAIL] a NOT-A-WITHDRAWAL ack must clear it, read {v}"); ok = False
        else:
            print(f"  [ok] acknowledged NOT-A-WITHDRAWAL           -> {v}")

        # t1-ack-d: DEATH IS STICKY. Once acknowledged DEAD, a LATER commit about
        # the plank -- a read-out, a post-mortem, a HANDOVER block -- must not
        # downgrade it back to SUSPECT. Real case: writing up WHY loki18 was dead
        # created a new kill-word commit with no ack, which re-flagged it as
        # merely SUSPECT. The fix unwinding itself the moment you document it.
        (d / "tools" / "plank_ack.tsv").write_text(
            f"lokiXX\t{kill_hash}\tDEAD\tits author said so\n")
        (d / "docs/prereg/PREREG-lokiXX.md").write_text("bar\npost-mortem\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "lokiXX post-mortem: why it was retracted")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "WITHDRAWN":
            print(f"  [FAIL] a later commit must not un-stick a DEAD ack, read {v}")
            ok = False
        else:
            print("  [ok] later commit after a DEAD ack           -> still WITHDRAWN")
        (d / "tools" / "plank_ack.tsv").unlink()

        # t1-ack-c: an ack for a DIFFERENT commit must NOT silence this one, or
        # one dismissal would deafen the plank forever.
        (d / "tools" / "plank_ack.tsv").write_text(
            "lokiXX\tdeadbeef\tNOT-A-WITHDRAWAL\tsome other commit\n")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "SUSPECT":
            print(f"  [FAIL] an ack for another commit must not clear this one, read {v}")
            ok = False
        else:
            print("  [ok] ack keyed to a different commit         -> still SUSPECT")
        (d / "tools" / "plank_ack.tsv").unlink()

        # t1a: THE OTHER DIRECTION, and without it WITHDRAWN is a verdict that can
        # only ever be reached and never left -- an alarm that cannot be satisfied
        # is one that gets trained away, which is this file's own stated failure
        # mode. An explicit revival commit must CLEAR it.
        (d / "docs/prereg/PREREG-lokiXX.md").write_text("bar: >85%\nrevived\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "lokiXX PLANK-REVIVED: the retraction was itself wrong")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v == "WITHDRAWN":
            print("  [FAIL] an explicit revival commit must clear WITHDRAWN"); ok = False
        else:
            print(f"  [ok] explicit revival commit                 -> {v} (not WITHDRAWN)")

        # t1b: and a revival must be EXPLICIT -- merely touching the tree again
        # after a withdrawal must NOT clear it, or every subsequent commit
        # silently resurrects a dead plank.
        (d / "docs" / "prereg" / "PREREG-lokiYY.md").write_text("bar\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "create lokiYY")
        (d / "docs/prereg/PREREG-lokiYY.md").write_text("bar\ndead now\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "lokiYY is dead, withdrawn")
        (d / "docs/prereg/PREREG-lokiYY.md").write_text("bar\ndead now\nmore work\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "lokiYY: tidy the document")
        v, _ = check("lokiYY", cwd=d, quiet=True)
        if v != "SUSPECT":
            print(f"  [FAIL] a later NON-revival commit must not clear it, read {v}")
            ok = False
        else:
            print("  [ok] later commit without the token          -> still flagged")

        # t1-collision: ⛔ TWO UNRELATED PLANKS UNDER ONE NAME. Real: on
        # 2026-08-11 two lanes committed PREREG-loki20-guns-not-walls and
        # PROPOSAL-loki20-healer-eviction 41 seconds apart. It matters because
        # WITHDRAWN is a real gate and plank_ack keys on the NAME, so one DEAD
        # ack silences both -- the fail-safe asymmetry failing UNSAFE.
        (d / "docs/prereg/PREREG-lokiCC-guns-not-walls-2026-08-11.md").write_text("a\n")
        (d / "docs" / "research").mkdir(exist_ok=True)
        (d / "docs/research/PROPOSAL-lokiCC-healer-eviction-2026-08-11.md").write_text("b\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "two unrelated lokiCC planks")
        v, det = check("lokiCC", cwd=d, quiet=True)
        if v != "COLLISION":
            print(f"  [FAIL] two unrelated planks under one name must read "
                  f"COLLISION, read {v}"); ok = False
        else:
            print(f"  [ok] two unrelated planks, one name           -> COLLISION {det}")

        # ...and the OTHER direction: one plank with several of its OWN docs
        # (prereg + leg read-out) must NOT read as a collision, or the guard
        # fires on every plank that gets written up and is trained away.
        (d / "docs" / "legs").mkdir(exist_ok=True)
        (d / "docs/prereg/PREREG-lokiDD-ring-2026-08-11.md").write_text("a\n")
        (d / "docs/legs/LEG-lokiDD-ring-2026-08-11.md").write_text("b\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "lokiDD prereg and its own leg read-out")
        v, _ = check("lokiDD", cwd=d, quiet=True)
        if v == "COLLISION":
            print("  [FAIL] one plank's own prereg+leg must NOT read COLLISION")
            ok = False
        else:
            print(f"  [ok] one plank, prereg + its own leg doc     -> {v} (not COLLISION)")

        # t1-rename: ⛔ A PURE RENAME CANNOT BE A RETIREMENT. Live false
        # positive, 2026-08-11: a commit renaming a plank's file was flagged
        # because its message contained "withdrawn" -- while DESCRIBING this
        # gate. A sticky DEAD ack against it would have killed a plank with no
        # tree, no prereg and no games. The commit ALSO added an unrelated file,
        # which is why the test is scoped to the plank's own paths.
        (d / "docs/prereg/PREREG-lokiRN-thing-2026-08-11.md").write_text("x\n")
        run(d, "add", "-A"); run(d, "commit", "-q", "-m", "create lokiRN")
        run(d, "mv", "docs/prereg/PREREG-lokiRN-thing-2026-08-11.md",
            "docs/prereg/PREREG-lokiRN2-thing-2026-08-11.md")
        (d / "docs/unrelated.md").write_text("y\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m",
            "RENAME lokiRN -> lokiRN2. Explaining PLANK_STATUS: WITHDRAWN and why "
            "a withdrawn plank stays withdrawn")
        v, _ = check("lokiRN2", cwd=d, quiet=True)
        if v in ("SUSPECT", "WITHDRAWN"):
            print(f"  [FAIL] a pure RENAME must not read as a retirement, read {v}")
            ok = False
        else:
            print(f"  [ok] rename commit saying 'withdrawn'       -> {v} (not flagged)")

        # t1c: ⛔ THE FALSE POSITIVE, TAKEN VERBATIM FROM REAL HISTORY. The first
        # cut of this guard flagged `loki13` -- OUR LIVE SHIPPED INCUMBENT --
        # because `core_kill_share` contains the substring "kill". This is the
        # cell that separates word-boundary patterns from substring matching, and
        # it uses the actual commit subject that produced the false alarm.
        (d / "docs" / "prereg" / "PREREG-lokiZZ.md").write_text("bar\n")
        (d / "HANDOVER.md").write_text(
            (d / "HANDOVER.md").read_text() + "lokiZZ is live.\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m",
            "LOKI-ZZ POOLED n=100/100: +18.0pp core_kill_share HELD, Fisher p=0.016")
        v, _ = check("lokiZZ", cwd=d, quiet=True)
        if v == "WITHDRAWN":
            print("  [FAIL] 'core_kill_share' must NOT read as a withdrawal"); ok = False
        else:
            print(f"  [ok] core_kill_share in a verdict subject   -> {v} (not WITHDRAWN)")

        # t1d: ⛔ THE FALSE NEGATIVE, ALSO FROM REAL HISTORY AND WORSE. The commit
        # that marked LOKI-18 VOID-ON-PREMISE contained the word "reinstated" --
        # describing the mistake it was recording -- and under prose matching THE
        # DOCUMENT DECLARING A PLANK DEAD CLEARED THE PLANK'S DEATH.
        (d / "docs" / "prereg" / "PREREG-lokiWW.md").write_text("bar\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "create lokiWW")
        (d / "docs/prereg/PREREG-lokiWW.md").write_text("bar\nvoid\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m",
            "PREREG-lokiWW AMENDMENT 2 - VOID ON PREMISE: the amendment reinstated "
            "a retracted number and then forbade its revision")
        v, _ = check("lokiWW", cwd=d, quiet=True)
        if v != "SUSPECT":
            print(f"  [FAIL] a VOID commit saying 'reinstated' must still be "
                  f"flagged, read {v}"); ok = False
        else:
            print("  [ok] VOID commit containing 'reinstated'    -> SUSPECT")

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

        # t4: a MIRROR tree of this plank is created by SOME OTHER plank's work.
        # Must NOT read STALE -- this plank did not move, it was COPIED. This is
        # the real false positive the guard produced on its first live run
        # (`1 STALE: loki13`, triggered by a LOKI-17 commit creating
        # `bots/_det_v130loki13/`). Without this branch the exclusion is
        # untested behaviour in an alarm, which is what the tool exists to catch.
        # Reset the baseline by editing a line that NAMES the plank -- rewriting
        # some other line would not match `-G lokiXX` and the baseline would not
        # move, which is what this fixture did on its first run and why it
        # reported a failure that was the TEST's bug and not the exclusion's.
        (d / "HANDOVER.md").write_text(
            "lokiXX IS DEAD -- withdrawn, confirmed, do not fire.\n"
            "Unrelated: monitors are alive.\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "HANDOVER: re-record lokiXX death (reset baseline)")
        (d / "bots" / "_det_v999lokiXX").mkdir(parents=True)
        (d / "bots/_det_v999lokiXX/main.py").write_text("x = 1\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "LOKI-YY battery: create a deterministic control mirror")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "OK":
            print(f"  [FAIL] a MIRROR tree must not read as the plank moving, read {v}")
            ok = False
        else:
            print("  [ok] mirror tree created by another plank    -> OK (not stale)")
        # ...and the exclusion must be narrow: a REAL artefact commit still fires.
        (d / "docs/prereg/PREREG-lokiXX.md").write_text("bar\nWITHDRAWN\nreal edit\n")
        run(d, "add", "-A")
        run(d, "commit", "-q", "-m", "lokiXX: a genuine artefact change")
        v, _ = check("lokiXX", cwd=d, quiet=True)
        if v != "STALE":
            print(f"  [FAIL] exclusion is too broad -- a real artefact edit must still fire, read {v}")
            ok = False
        else:
            print("  [ok] real artefact edit after the mirror     -> STALE")

    print("\nPASS: drives OK -> STALE -> OK, surfaces the kill word, ignores a "
          "mirror tree without going blind to real edits, and an edit that does "
          "not name the plank does not clear it."
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
    withdrawn = []
    suspect = []
    collision = []
    for p in planks:
        v, _ = check(p)
        if v == "STALE":
            worst = 1
            stale.append(p)
        elif v == "WITHDRAWN":
            worst = 1
            withdrawn.append(p)
        elif v == "SUSPECT":
            worst = 1
            suspect.append(p)
        elif v == "COLLISION":
            worst = 1
            collision.append(p)
    if withdrawn:
        print(f"\n*** {len(withdrawn)} WITHDRAWN: {', '.join(withdrawn)} ***")
        print("A committed prereg and an existing bot tree BOTH SURVIVE a")
        print("withdrawal. s30 fired 25 unrated games on loki18 forty minutes")
        print("after this tool ran clean on it, because the kill-word scan sat")
        print("inside the STALE branch and loki18 exited at UNMENTIONED.")
    if collision:
        print(f"\n*** {len(collision)} NAME COLLISION: {', '.join(collision)} ***")
        print("Two unrelated planks share a name. A withdrawal or a DEAD ack for")
        print("either one silences BOTH — rename one before acting on either.")
    if suspect:
        print(f"\n*** {len(suspect)} SUSPECT: {', '.join(suspect)} ***")
        print("Each has a commit that READS LIKE a retirement. Read it, then")
        print("record the answer in tools/plank_ack.tsv so it stops shouting.")
    if stale:
        print(f"\n*** {len(stale)} STALE: {', '.join(stale)} ***")
        print("Do not activate against HANDOVER's word until these are reconciled.")
    # ⛔ GATE ON THIS LINE, NOT ON `$?`. The whole contract of this tool is its
    # exit code, and the natural way anyone runs a long report --
    # `plank_status.py --all | tail` -- makes `$?` the status of `tail`, which is
    # ALWAYS 0. A caller gating on `$?` behind a pipe therefore reads OK forever:
    # a guard that cannot fail, which is the exact class this tool was built to
    # replace. This is the standing repo rule (`fcode status` exits 0 while
    # printing `Error: True`): GATE ON THE PRESENCE OF THE LOAD-BEARING FIELD.
    label = ("COLLISION" if collision else "WITHDRAWN" if withdrawn
             else "SUSPECT" if suspect else "STALE" if stale else "OK")
    print(f"\nPLANK_STATUS: {label}")
    return worst


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
