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

Docs absorbed, nothing built. **Not yet registered on the platform** — no `fcode` account,
no matches run. Everything in [docs/strategy-notes.md](docs/strategy-notes.md) is derived from
published numbers, not observed play.

## Docs

| File | Purpose |
| --- | --- |
| [docs/game-model.md](docs/game-model.md) | Ground truth: rules, API, costs, limits. Facts only. |
| [docs/strategy-notes.md](docs/strategy-notes.md) | Derived analysis — the arithmetic on those facts, and what it implies. |
| [docs/strategy-log.md](docs/strategy-log.md) | One entry per bot version: what changed, what the ladder did. |
| [docs/opponents.md](docs/opponents.md) | Patterns we observe in other players' bots. |
| [docs/open-questions.md](docs/open-questions.md) | What we still don't know, and how to find out. |
| [docs/reference/](docs/reference/) | Verbatim scrape of the official docs and tutorials, plus the scraper. |

`docs/reference/` is vendored so the full Controller API is available offline and so we can
diff it if the organisers change the rules mid-competition. Re-run with
`python3 docs/reference/scrape.py`.

## Getting set up

```bash
pip install fcode          # needs Python 3.12 or 3.13 — NOT 3.14
fcode login                # browser OAuth; requires an approved platform account
fcode starter              # scaffolds fcode.toml, bots/starter/main.py, maps/
fcode run starter starter --tle 10   # local mirror match, WITH the ladder's time limit
fcode watch replay.replay26
```

Always pass `--tle 10`. `fcode run` does not enforce the CPU limit by default, so without it
you'll happily develop a bot that dies on the ladder.
