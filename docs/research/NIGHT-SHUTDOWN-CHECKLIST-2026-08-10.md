# NIGHT SHUTDOWN — what Magnus does when he kills the sessions

**Written 2026-08-10 ~20:2x Z by the side lane, at Magnus's request.**
Sessions close ~22:00, reopen ~06:00. **Every command below is copy-pasteable
and every step has a CHECK with the expected output.** Run them in order.

> **The one thing that actually matters:** when the sessions die, **nothing can
> roll back the bot.** A prototype left live plays the ladder unattended until
> 06:00. Step 1 and Step 2 exist for that; everything else is optimisation.

---

## STEP 1 — STOP THE LEG RUNNER **BETWEEN CYCLES**, NOT MID-CYCLE

A leg runner activates a prototype, fires, and rolls back. **Killed mid-cycle it
cannot roll back**, and the prototype stays live all night. It is safe to kill
only while it is sleeping between cycles.

```bash
cd ~/Projects/Work/florent-code-game
tail -3 scratchpad/loki16b_run.log
```

**Look for the LAST line to be one of:** `rolled back to vNNN, VERIFIED` ·
`meter says wait …s (incumbent live)` · `cycle N: fired …`
**If instead it says `vNNN LIVE, firing …`, WAIT** — it is mid-cycle. Re-check in
30 seconds. Then:

```bash
pkill -f 'loki1.*_leg.sh'; pkill -f '_cal.sh'; sleep 3
pgrep -fl '_leg.sh|_cal.sh' || echo "ALL LEG RUNNERS STOPPED"
```

**CHECK — must print:** `ALL LEG RUNNERS STOPPED`

---

## STEP 2 — VERIFY THE HOLDER. **THIS IS THE NON-NEGOTIABLE ONE.**

```bash
.venv/bin/fcode status | grep "Active bot"
```

**CHECK — must read exactly:** `Active bot: v104 (Loki v2)`

**If it says anything else**, a prototype is live and would play ~24 unattended
rated matches. Fix it before doing anything else:

```bash
.venv/bin/fcode submission activate 104
sleep 5; .venv/bin/fcode status | grep "Active bot"     # repeat until v104
```

⚠ **Do not gate on the exit code — it lies on this platform.** `fcode status`
exits 0 while printing errors. **Read the `Active bot:` line itself.**

---

## STEP 3 — START THE OVERNIGHT COLLECTOR (optional but recommended)

**Only a NON-ACTIVATING runner may run unattended.** It plays v104 — nothing to
activate, nothing to roll back, cannot leak. An activating rotation overnight is
forbidden, and we measured the cost today: **−24.67 Elo across 3 leaked
matches**, invisible to the version tag.

The builder should leave a launch command in `HANDOVER.md` under the overnight
section. It will look like:

```bash
nohup zsh tools/<collector>.sh > scratchpad/overnight.log 2>&1 &
```

**CHECK — after ~60 seconds:**
```bash
tail -2 scratchpad/overnight.log      # expect a fired/waiting line, no ABORT
.venv/bin/fcode status | grep "Active bot"   # must STILL be v104
```

**If `HANDOVER.md` has no such command, skip this step.** An unattended runner
you cannot verify is worse than no runner.

---

## STEP 4 — CONFIRM THE DETACHED MONITORS SURVIVED

These are separate processes and outlive the sessions. Verified alive at 20:2x Z.

```bash
ps aux | grep -E "keeper.py|ship_watch|while true" | grep -v grep | wc -l
```

**CHECK — expect 5 or more.** These keep the corpus and the Elo tape current
overnight, which is what makes the morning read possible.

---

## STEP 5 — LEAVE THE TREE CLEAN

```bash
git status -sb | head -5
```

Only `corpus/*` and `elo_history.tsv` should be modified — those are
monitor-owned and change by themselves. **If a `bots/` or `docs/` file is
modified or untracked, tell the builder before closing** — uncommitted work dies
with the session.

---

## ⚠ THE DECISION ONLY YOU CAN MAKE

**Nothing can act overnight.** `ship_watch` will faithfully write
`corpus/SHIP_ALERT` at 03:00 and no one will read it until 06:00. So either:

* **(a) accept it** — the exposure is bounded: the ladder now runs every 20
  minutes (halved today), so it is **~24 unattended rated matches**, and v104 is
  currently **+51 above its activation baseline** with the rollback line 26+
  points away; or
* **(b) ask the builder, before close, to arm an auto-rollback** on the
  already-pre-committed conjunction (`net5 <= −21` AND `net_act < 0`).

**DECIDED BY MAGNUS, 2026-08-10 ~20:3x Z: option (a). Verbatim: *"No we dont
need a rollback script, i think it's fine."* No auto-rollback is armed tonight,
and that is a CHOICE, not an oversight — a successor seeing no guard at 06:00
should read it here rather than assume it was forgotten. Sizing he accepted:
~24 unattended rated matches, v104 at +51 net_act, trigger 26+ points away, and
recovering (1641 -> 1666) rather than falling.**

**Either is defensible. Not choosing is not** — "we didn't decide" and "we
decided to hold" look identical at 06:00, and only one of them is a decision.

---

## MAGNUS'S HYPOTHESIS — pre-registered 2026-08-10, TO BE TESTED AT 06:00

**Magnus, verbatim:** *"No we dont need a rollback script, i think it's fine"* →
*"store it as my hypothesis, it can be broken and next night we will do
something different."*

**H1: an unguarded overnight window costs us nothing we would have prevented.**
Stated so it can lose: over ~24 unattended rated matches with no agent able to
act, v104 will not reach the state an armed rollback would have fired on.

**ANCHOR at close (`ship_watch` 22:19:27, the row this is pinned to):**
`rating 1671 · k=54 · net5 +10.0 · net_act +56.0 · drawdown −27 · peak 1698`
Rollback line **1615**; headroom **56 points**.

**FALSIFIER — primary, binary, and checkable from the tape alone:**
> **H1 IS BROKEN if ANY `corpus/ship_watch.log` row between close and 06:00 has
> `net5 <= -21` AND `net_act < 0` simultaneously** — that is the conjunction an
> armed rollback would have acted on, so its truth means the guard was needed
> and absent.

**SECONDARY, recorded whether or not the primary fires** (magnitude, not verdict):
overnight net rating change; lowest rating reached; max drawdown from 1698.

**PRE-COMMITTED RESPONSE, decided now so it is not re-argued at 06:00:**
* **Falsifier fires →** arm the auto-rollback tomorrow night. Not a debate.
* **Falsifier does not fire →** H1 **survives one night. It is not established.**
  n=1, and the exposure is conditional on tonight's specific state (+56 net_act,
  56 points of headroom, a recovering trajectory). **A quiet night at +56 says
  nothing about a night that starts at +5.** Re-test nightly against that
  night's anchor; the hypothesis is only as good as the headroom it was set at.

---

## MORNING — 30 SECONDS, BEFORE ANYTHING ELSE

```bash
.venv/bin/fcode status | grep -E "Active bot|Rank"      # holder + rank
tail -3 elo_history.tsv                                  # overnight trajectory
ls corpus/SHIP_ALERT 2>/dev/null && cat corpus/SHIP_ALERT # did the stop-loss fire?
pgrep -fl '_cal.sh|_leg.sh'                              # collector still up?

# TEST MAGNUS'S HYPOTHESIS H1 — did the conjunction EVER go true overnight?
# DRIVEN TO BOTH VERDICTS BEFORE BEING PUT HERE (2026-08-10): fires on a
# synthetic net5=-31/net_act=-15 row, stays SILENT on a one-sided near-miss
# (net5=-31 but net_act=+26), silent on the real log. No output = H1 survived.
awk -F'\t' '$0 ~ /net5=/ {n=$0; sub(/.*net5=/,"",n); sub(/\t.*/,"",n);
  a=$0; sub(/.*net_act=/,"",a);
  if (n+0 <= -21 && a+0 < 0) print "H1 BROKEN: " $1 " net5=" n " net_act=" a}' corpus/ship_watch.log
```

**Then, before firing any leg: STOP THE COLLECTOR AND WAIT 20 MINUTES.** The
rate limit is a **shared** 5-per-20-minutes budget. A collector that ran all
night has spent the current window, and the first morning leg will eat
rejections — which themselves count against the limit.

```bash
pkill -f '_cal.sh'; .venv/bin/python tools/rate_budget.py    # prints seconds to wait
```
