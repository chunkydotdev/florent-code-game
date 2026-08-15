# FLEET AUDIT — the centralized queue and the shard pollers, 2026-08-15

**Audited 2026-08-15T16:3x–16:5xZ (`date -u`) at `d5e0cf86`.** Every finding below was
reproduced by running the command printed under it, on the live system, today.

**⚠ FIRST, THE THING THAT IS NOT A DEFECT AND MATTERS MOST: THE DESIGN IS SOUND.** Guards 1–4 in
`corefill.sh`, the one-way state machine in `fleet_queue.tsv`, the `.started` markers, the
`NULLHOST` per-host certification cell, `auto_gate`'s deliberate refusal to act on remote shards
— all of it works and all of it is doing real protective work right now. **156 shards started,
zero relaunched. Zero seed collisions across three hosts.** The failures below are in the
SUPERVISION layer, not the execution layer.

---

## ⛔ 1. THE SUPERVISOR WAS DEAD FOR 22 HOURS, AND THE BOX WAS SET TO GO IDLE TONIGHT

**The most expensive finding. Fixed.**

```
corefill_forever.log last line   2026-08-14T18:35:53Z  PAUSED (COREFILL_STOP present)
scratchpad/COREFILL_STOP         absent  (the pause ended; the supervisor never resumed)
corefill_forever processes       0
corefill.sh running              pid 84779, launched 15:40:28Z with DEADLINE_H=12
unstarted worklist items         55
```

`corefill_forever.sh` exists for exactly one reason, stated in its own header: `corefill.sh` has
**two terminal exits** (deadline reached; all work started and finished) and **neither re-arms
anything**. It was paused by `COREFILL_STOP` on 2026-08-14, the session that would have resumed
it ended, and **nothing anywhere was responsible for noticing.**

⇒ The live runner would have hit its 12-hour deadline at **~2026-08-16T03:40Z** and stopped
launching, with **55 items unstarted and eight cores going idle** — a near-exact replay of the
2026-08-13 incident (`exit at 01:52:15Z`, box idle until `04:36:04Z`, 14 consecutive idle polls
before a human looked) that this supervisor was written to prevent.

**FIXED:** supervisor relaunched (`16:43:03Z`), confirmed alive, and confirmed **not** to have
disturbed the running runner (pid 84779 unchanged, 8 shards still running). Restarting the
supervisor is safe by construction — it never touches a `.started` marker or a row; it restarts
the RUNNER, never the WORK.

**⭐ THE DURABLE LESSON, and it is the same one as the whole usability review:** the
`ALWAYS_BE_RUNNING` guarantee lived in a process with no watchdog above it. **Nothing in the
Claude Code harness supervises these daemons** — they are detached (`PPID 1`) repo-local
processes. A supervisor with nothing supervising *it* is a single point of failure wearing the
costume of a safety net.

---

## ⛔ 2. TWO `auto_gate --apply` LOOPS ARE RUNNING — THE CANCELLER IS DUPLICATED

**NOT FIXED — the `kill` was blocked by the permission classifier. This one needs you.**

```
pid 15578  etime 02:32  zsh -c while true; do auto_gate.py --apply ...; sleep 600; done
pid 61319  etime 06:39  zsh -c while true; do auto_gate.py --apply ...; sleep 600; done
```

Two independent loops, both armed with `--apply`, both evaluating every live shard every 600 s
and both able to write cancel flags. `auto_gate` is the tool that **stops batteries**; running
two of it is the one duplication with a destructive edge. Both append to the same log, so the
log reads as one loop polling twice as often.

**To fix (kill the newer, keep the original):**
```bash
kill 15578 && sleep 2 && ps ax -o pid=,command= | grep '[a]uto_gate.py --apply'   # expect ONE
```

---

## ⛔ 3. EVERY LINE IN TWO RUN LOGS IS WRITTEN TWICE — ONE RUNNER READS AS TWO

**Fixed in both tools.**

```
scratchpad/corefill.log        5,133 "hold:" lines, each duplicated
                               TWO identical `COREFILL up` banners at 15:40:28Z — for ONE process
scratchpad/fleet_dispatch.log  every queue/host line duplicated
```

Cause, identical in both: the tool's own `say()` writes to the log **and** the launcher
redirects stdout into the same file.
* `corefill.sh:85` — `say(){ ... | tee -a $LOG }` under `>> scratchpad/corefill.log`
* `fleet_dispatch.py:266` — `print()` + `LOG_F.open("a")` under `>> scratchpad/fleet_dispatch.log`

**This is not cosmetic.** During this audit the doubled banner is what first suggested two
runners existed; it took a PID-level check to disprove. **A log that doubles its own startup
banner is a log that lies about the most alarming thing it can report.**

**FIXED:**
* `fleet_dispatch.py` — `_stdout_is_the_log()` compares `os.fstat(1)` against the log's inode and
  suppresses the duplicate write. Detection, not convention: correct however it is launched.
* `corefill_forever.sh` — launches the runner with `>/dev/null 2>> corefill.log`, since `say()`
  already tees. (The shell cannot use the inode trick: on macOS `stat /dev/fd/1` reports the
  devfs node, not the target — verified.)

---

## ⛔ 4. NOTHING STOPPED A SECOND RUNNER FROM SERVING THE SAME WORKLIST

**Fixed — new guard 5 in `corefill.sh`.**

Guards 1–4 all protect a **shard** from being started twice. Nothing protected the **worklist**
from being *served* twice. Two runners each enforce `MAX_SHARDS` independently → the box silently
runs `2 × MAX_SHARDS`, and **`--tle 10` is wall-clock**, so oversubscription does not merely slow
the batch, it **corrupts every row both runners produce**. The `.started` marker makes a double
launch look *harmless* in the log, which is why it needed a refusal rather than a note.

Driven to both verdicts:
```
second runner on the LIVE worklist  -> exit 3, names pid 84779   ✅ refuses
runner on a FRESH worklist          -> passes guard 5, proceeds  ✅ does not refuse
```
⭐ **The first draft of this guard FAILED verdict B** — it matched its own invoking shell, whose
argv contained the strings. It now excludes ancestor PIDs *and* requires argv adjacency
(`…corefill.sh` immediately followed by the worklist). **A guard watched only to fire has not
been watched to pass.**

---

## ⚠ 5. FOUR HOST-KEYS FOR TWO MACHINES, AND NO COLLISION GUARD

**NOT FIXED — flagged. No live corruption; the exposure is latent.**

The seed offset is `crc32(hostkey) % 50 * 1e6`, and the generated worklist header promises *"this
host plays DIFFERENT seeds from every other host … so its rows are independent draws that POOL."*
**The guarantee is per-MACHINE; the key is per-STRING.** Both machines have been addressed under
two names:

| hostkey used | offset | generated | source worklist |
|---|---:|---|---|
| `worker@work-server-1` | 32,000,000 | 15:12:02Z | `worker@work-server-1.fleet_src.txt` |
| `work-server-1` | **48,000,000** | 07:40:33Z | `launcher_work.txt` |
| `worker@work-server-2` | 14,000,000 | 04:53:20Z | `work-server-2-r.txt` |
| `work-server-2` | **24,000,000** | 12:56:50Z | `ws2_work.txt` |

`scratchpad/vps/hosts.txt` lists only the two `worker@` forms. There is **no collision check** in
`orchestrate.sh`. Note `fleet_dispatch.py:278` already carries `bare_host()` with the docstring
*"`worker@work-server-1` and `work-server-1` name the SAME machine"* — **the aliasing is handled
in the dispatcher and not in the seed derivation.**

**MEASURED, and this is the honest part: there is no actual collision.**
```
ws1 mirror   48,620 rows   1,625 distinct seeds   [32,253,000 .. 81,900,153]
ws2 mirror   39,681 rows   1,324 distinct seeds   [14,320,000 .. 40,100,044]
LOCAL       491,746 rows  27,592 distinct seeds   [    20,000 ..    308,091]
pairwise intersections: 0, 0, 0
```
⚠ **But disjointness is ACCIDENTAL, not structural.** Offsets are spaced 1,000,000 apart while
seedbases in the worklists span **tens of millions** — ws1's range alone covers 49.6M and runs
straight through the 48M slot its own alias would occupy. **The offset scheme cannot enforce what
its header promises; today it holds by luck of allocation.**

⇒ **Recommended:** canonicalise the hostkey through `bare_host()` before deriving the offset, and
refuse to generate when two live hosts resolve to the same offset **or** when a host's
`[offset, offset + max_seedbase]` window overlaps another's.

---

## ⚠ 6. "ONE CENTRAL QUEUE" IS TWO QUEUES, AND THE DISPATCHER SEES ONLY ONE

**NOT FIXED — flagged; it is currently failing safe.**

`fleet_queue.tsv`'s header says *"ONE central queue"*. In practice each worker runs a worklist
generated by `orchestrate.sh gen`, and those interleave **fleet rows** with **hand-added rows**:

```
worker-2 worklist:  NULLHOST NULL140B PINRND1 LNCHERL2 AWRSPAWN RNDSPAWN   <- hand rows
                    F201LAUNCH0 F211PAVEFIR F232COLLARM F250HOMEEAR F253CATAPUL  <- fleet rows
```

`host_queue_depth()` counts only `CLAIMED`/`RUNNING` **fleet** rows. Right now worker-2 reads
`depth=2/2 FULL` on two CLAIMED fleet rows while it is actually executing `RNDSPAWN`, a hand row
the dispatcher cannot see. **The error direction is safe today** (it under-dispatches), and the
two CLAIMED rows are legitimately queued behind `RNDSPAWN` in worklist order — they are not
stuck. But the model is wrong, and `reconcile()` cannot advance a row whose host is busy with
work it has no visibility into.

**Also:** `F232COLLARM` appears **twice** in `fleet_queue.tsv`, both `FAILED`, on different hosts
— which the file's own header forbids: *"To retry a row, ADD A NEW ROW with a new shard_id and a
fresh seed_lo — never edit a state backwards."*

---

## ✅ WHAT I VERIFIED IS WORKING

| | evidence |
|---|---|
| `corefill.sh` launch-once | 206 worklist items, 156 `.started` markers, **0 relaunches**, cancel dir empty |
| load ceiling | `hold: running=8/8 load=10.25` — holding at the ceiling, not exceeding it |
| worklist live re-read | `unstarted=55` tracks appends within one poll |
| `fleet_dispatch` reconcile + depth | `QUEUED=26 CLAIMED=3 RUNNING=1 FAILED=2`, refuses to over-dispatch |
| `auto_gate` remote refusal | **deliberate and tested** — `chk("remote apply is REFUSED", done_r, False)` at `:1160`; it reports the manual 3-step sequence instead |
| `NULLHOST` certification | present and first on both hosts' worklists |
| seed disjointness | 0 collisions across 30,541 distinct seeds (see §5 for why this is luck) |
| monitors | keeper + elo/match/opp/replay watchers + ship_watch + cores_idle all alive |

---

## THE PATTERN ACROSS ALL SIX

**Five of the six are supervision or naming, none is execution.** The shard runner is careful,
well-guarded and correct. What failed is the layer that answers *"is the careful thing still
running, and is it the only one?"* — a dead supervisor, a duplicated canceller, a log that
double-counts itself, a missing singleton check, an alias that splits one machine into two, and a
queue that calls itself central while a second queue feeds the same workers.

⇒ **The instrument that was missing is the one that says WHAT IS SUPPOSED TO BE RUNNING AND IS
IT.** `corefill_status.sh` reports shards; nothing reported *supervisors*. That is the same
shape as `tools/now.py`'s finding on the state surfaces: the system tells you the numbers and
leaves you to know which process should have produced them.

**Suggested next build (not done):** `tools/fleet_health.py` — one screen, expected daemons vs
actual, duplicates flagged, each with the exact relaunch command. It would have caught findings
1, 2 and 4 at a glance, and it is the natural companion to `now.py`.
