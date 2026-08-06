# Tooling

Local setup and the two workarounds that let us develop without a platform account.

## Environment

The machine's default `python3` is **3.14, which `fcode` does not support**. Use 3.13:

```bash
python3.13 -m venv .venv
.venv/bin/pip install fcode        # 2.3.6 as of 2026-08-06
```

`fcode` ships the engine as a compiled `.so` (`fcode_engine.cpython-313-darwin.so`, exporting
one function, `run_game`) plus the CLI and visualiser in plain Python/JS. The wheel is
version-specific — a 3.13 venv gets the `cp313` wheel.

Always run local matches with `--tle 10`. Without it `fcode run` enforces **no** CPU limit,
so you can develop a bot that dies on the ladder.

## Generating maps offline

`fcode starter` leaves `maps/` empty and tells you to log in and run `fcode maps sync` — the
competition pool lives on the platform. Without an account there are no maps, and without maps
you can't run a single match.

`tools/make_map.py` fixes that. `.map26` is protobuf; the schema is recoverable from the
bundled map editor's JS (`fcode/data/visualiser/assets/map-editor-*.js`, message
`battlecode.Map`), and the script writes the format directly with a ~30-line varint encoder —
no protobuf dependency.

```bash
.venv/bin/python tools/make_map.py          # writes six maps into maps/
.venv/bin/fcode run starter starter maps/mid20.map26 --tle 10
```

The defaults deliberately span the pool's full 8×8–30×30 range, since map size is likely the
biggest single variable in strategy choice. Schema, constraints, and the symmetry rules are
documented in the script's docstring.

**These are our guesses at maps, not the real pool.** Replace them with `fcode maps sync`
output the moment we have an account — a strategy tuned against home-made maps is tuned
against the wrong distribution.

Two other routes to a map, for reference:
- `fcode map-editor` serves the real editor from `localhost` with no login, and it can export
  `.map26` — usable, but it's a GUI, so no good for scripted generation.
- The editor also imports/exports **PNG** maps, one pixel per tile, palette:
  `#000000` empty, `#44465E` wall, `#5AD4FF` titanium ore, `#FFBF40` core A, `#6EAAFF` core B.
  Handy for eyeballing or hand-drawing a map; the engine itself only reads `.map26`.

## Reading `print()` output from a match

`print()` inside `run()` does **not** appear on stdout — it's captured into the replay and
shown in the visualiser. For headless work, the replay is protobuf with the debug strings
stored plainly, so:

```bash
.venv/bin/fcode run mybot starter maps/duel16.map26 --tle 10 --replay /tmp/p.replay26
strings /tmp/p.replay26 | grep "MYTAG"
```

Prefix every probe line with a unique tag and this becomes a usable instrumentation channel
for offline experiments — it's how the turret-firing and starting-titanium questions in
[game-model.md](game-model.md) got settled.

Uncaught exception tracebacks, by contrast, *do* go to stderr during `fcode run` — which is
how the starter bot's crash bug was spotted (see [strategy-log.md](strategy-log.md)).
