# Florent Code League 2026

Our entry in the Florent Code League — a Python bot competing on a live Nordic ladder.
Top 16 teams qualify for the Stockholm finals; €20K prize pool across category winners.

Public site: https://code.florent.vc/ · Platform: https://game.code.florent.vc

## The game in one paragraph

Two teams on a symmetric grid (8×8 to 30×30). Each has one Core (500 HP, 2×2, stationary).
You write a single Python `Player` class; the engine instantiates it **per unit** and calls
`run(ct)` once per round for each one, for 1000 rounds. The Core spawns Builder Bots — the only
mobile unit — which mine titanium by building Harvesters on ore and routing the output back
with conveyor chains, and which build the three turret types. Win by destroying the enemy Core,
or on tiebreak by **titanium collected**, then harvester count, then titanium stored.

Full details in [docs/game-model.md](docs/game-model.md).

## Start here

```bash
.venv/bin/python tools/now.py          # what is live, what is the control, how stale each surface is
.venv/bin/python tools/queue_check.py  # what is startable today
```

**Then read [HANDOVER.md](HANDOVER.md) — the TOP BLOCK ONLY** (stop at `===== PRIOR STATE`).
If this session is a protocol lane, invoke `/builder`, `/research` or `/sidelane` **first**:
the charter and hard limits live in `.claude/commands/` and are not auto-loaded.

⚠ **Do not read a state number out of this file.** Everything about ratings, holders and
incumbents moves hourly; `tools/now.py` reads it live and labels each surface with its age.
This section said *"not yet registered on the platform"* and *"current best bot is `bots/v4`"*
for nine days after both stopped being true — which is exactly the failure the router below
exists to prevent.

## Which surface answers which question

**The dominant error in this repo is reading a surface that is correct — for a different
question.** Five files answer "what is live" and three of them are right about something else.

| Question | Read this | Never use instead |
| --- | --- | --- |
| What holds the ladder slot **right now**? | `fcode status` (`Active bot:`) | any poller — between polls a healthy line and a blind line are byte-identical |
| Which way is the rating **moving**? | `corpus/ship_watch.log` | — (it is a 10-min poller; fine for trend, never for identity) |
| Rating **history** | `elo_history.tsv` | its version tag is poll-time, not per-match |
| What did we play, **per rated match**? | `corpus/ladder_games.tsv` | `meta_join` — it pools rated with unrated |
| What are queued arms **scored against**? | `PROGRAMME.md: INCUMBENT` | the live holder — they diverge when a teammate ships |
| Any **rated win-rate denominator** | `corpus/ladder_games.tsv` | `meta_join` (missing ~38% of ladder matches) |
| An opponent's **version timeline** | `corpus/league_matches.tsv` | — |

Run `tools/now.py` rather than memorising the table.

## Where the work is queued

Three separate queues — only the first is surfaced at session start:

| File | Holds | Runner |
| --- | --- | --- |
| `QUEUE.md` | ideas / planks to build | `tools/queue_check.py` |
| `scratchpad/corefill_work.txt` | local shard batteries | `tools/corefill.sh`, supervised by `tools/corefill_forever.sh` |
| `scratchpad/fleet_queue.tsv` | remote-worker shards | `tools/fleet_dispatch.py` |

None of this is part of the Claude Code harness — it is all repo-local files and daemons.
The daemons are detached (`PPID 1`) and **nothing outside this repo restarts them**;
`corefill_forever.sh` is the supervisor and it is the thing to check first when cores go idle.

## Docs

| File | Purpose |
| --- | --- |
| [docs/game-model.md](docs/game-model.md) | Ground truth: rules, API, costs, limits. Facts only. |
| [docs/strategy-notes.md](docs/strategy-notes.md) | Derived analysis — the arithmetic on those facts, and what it implies. |
| [docs/strategy-log.md](docs/strategy-log.md) | One entry per bot version: what changed, what the ladder did. |
| [docs/tooling.md](docs/tooling.md) | Local setup, offline map generation, probe bots, reading `print()` from replays. |
| [docs/runbook.md](docs/runbook.md) | Approval-day checklist and the rules-change recalibration procedure. |
| [docs/opponents.md](docs/opponents.md) | Patterns we observe in other players' bots. |
| [docs/open-questions.md](docs/open-questions.md) | What we still don't know, and how to find out. |
| [docs/reference/](docs/reference/) | Verbatim scrape of all 23 official docs pages and 24 tutorial steps, plus the scraper. |
| [program.md](program.md) | Protocol for running the bot-improvement loop unattended. |

`CLAUDE.md` is **this project's own standing directive** — the programme, the measurement
rules and the engine facts we have verified ourselves. It began as the organisers' context
file and has long since diverged; several of its sections exist specifically to correct the
organisers' docs. **`AGENTS.md` is a GENERATED COPY of `CLAUDE.md`** for non-Claude tools
(regenerate with `cp CLAUDE.md AGENTS.md`, then restore its header) — the dependency runs that
way round, not the other. The organisers' verbatim pages are vendored under
[docs/reference/](docs/reference/), and the known errors in them are flagged in
[docs/game-model.md](docs/game-model.md) and [docs/open-questions.md](docs/open-questions.md).

`docs/reference/` is vendored so the full Controller API is available offline and so we can
diff it if the organisers change the rules mid-competition. Re-run with
`python3 docs/reference/scrape.py`.

## Getting set up

**Gotcha on this machine:** the default `python3` is **3.14.3, which `fcode` does not support**.
`python3.13` (3.13.7) and `python3.12` (3.12.9) are both installed — use one of those.

```bash
python3.13 -m venv .venv && source .venv/bin/activate
pip install fcode          # needs Python 3.12 or 3.13 — NOT 3.14
fcode login                # browser OAuth; requires an approved platform account
fcode starter              # scaffolds fcode.toml, bots/starter/main.py, maps/
fcode run starter starter --tle 10   # local mirror match, WITH the ladder's time limit
fcode watch replay.replay26
```

Always pass `--tle 10`. `fcode run` does not enforce the CPU limit by default, so without it
you'll happily develop a bot that dies on the ladder.
