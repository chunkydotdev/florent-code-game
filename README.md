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

## Status

Project scaffolded and **running matches locally**. `fcode` 2.3.6 installed in `.venv`
(Python 3.13), starter bot at `bots/starter/main.py`, six self-generated maps in `maps/`.

**Not yet registered on the platform** — no account, so no ladder matches, no real map pool,
and no submissions. That's the only remaining blocker; everything else is unblocked, because
`tools/make_map.py` generates `.map26` maps offline (see [docs/tooling.md](docs/tooling.md)).

## Docs

| File | Purpose |
| --- | --- |
| [docs/game-model.md](docs/game-model.md) | Ground truth: rules, API, costs, limits. Facts only. |
| [docs/strategy-notes.md](docs/strategy-notes.md) | Derived analysis — the arithmetic on those facts, and what it implies. |
| [docs/strategy-log.md](docs/strategy-log.md) | One entry per bot version: what changed, what the ladder did. |
| [docs/tooling.md](docs/tooling.md) | Local setup, offline map generation, reading `print()` from replays. |
| [docs/opponents.md](docs/opponents.md) | Patterns we observe in other players' bots. |
| [docs/open-questions.md](docs/open-questions.md) | What we still don't know, and how to find out. |
| [docs/reference/](docs/reference/) | Verbatim scrape of all 23 official docs pages and 24 tutorial steps, plus the scraper. |
| [program.md](program.md) | Protocol for running the bot-improvement loop unattended. |

`AGENTS.md` (and its copy `CLAUDE.md`) is the organisers' own context file for AI coding
tools, taken verbatim from `docs/agents-md`. It's the most compact accurate summary of the
rules and API that exists — but note it has two known errors, flagged in
[docs/game-model.md](docs/game-model.md) and [docs/open-questions.md](docs/open-questions.md):
it says the cost scale starts at 1.0 (the API returns 100.0) and gives the Core a spawn radius
that contradicts the rules page.

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
