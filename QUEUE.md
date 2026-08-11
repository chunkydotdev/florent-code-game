# BUILD QUEUE — ideas to TEST, in fire order

**Magnus, 2026-08-11 (s31), standing directive:** *"you need to be constantly
putting experiments to test, there should be a queue with ideas to build, the
researcher will be responsible to make sure there are ideas to build."*

**OWNERSHIP.** RESEARCH keeps this stocked — it is their deliverable that this
file is never empty. BUILDER fires from the top and never idles waiting for
analysis. **An empty queue is a research failure, not a builder pause.**

**THE CLOCK.** ~420 rated matches remain in the entire game (~84/day, measured
646->749 in 29.5 h). Rating converges in ~100 matches ⇒ **about four
ship-and-converge cycles left.** A ship converges in the BACKGROUND, so an
unshipped plank is a certain zero and every idle hour on the slot is spent.

**ADMISSION — an item is queueable only with all four:**
1. the CHANGE, named to the constant or branch
2. the MECHANISM METRIC only that change can move
3. the FIXTURE it is measured on, and whether that fixture can resolve it
4. why it is worth a slot **now** (`tools/target_value.py` band if it is a live leg)

---

## FIRING NOW
| # | plank | change | mechanism metric | status |
|---|---|---|---|---|
| 1 | **LOKI-27 ferry-first** | ferry request outranks home exile | INSERT:EXILE ratio | **SHIPPED-PENDING** — v112 uploaded, activation blocked on a permission; Magnus runs `fcode submission activate 112` |

## NEXT UP — ready to build
| # | plank | change | mechanism metric | why now |
|---|---|---|---|---|
| 2 | **Idle-builder defence** | re-task builders already alive+idle when core HP falls | median kill round MUST NOT rise (`DEFENCE_ADMISSION_BAR`) | **The first plank under the amended defence field.** Measured: when our core dies ~5 builders are ALIVE (median 5.0) with 0.38 deaths in the 40 rounds prior — they are not in combat. Costs the kill nothing BY CONSTRUCTION. Our median kill 174 vs median death 187 = a 13-round race. |
| 3 | **Arrive without traversing** | launcher delivery instead of walking the raider forward | forward builder deaths per forward build | Hazard is ~3.5x the field in EVERY round band (not a phase problem), so no round-gated constant touches it. Skipping the traverse attacks it directly. ⚠ traverse-vs-destination split is ASSUMED not measured — research's attribution cut settles it first. |

## BLOCKED / NEEDS A NUMBER FIRST
| # | plank | blocker |
|---|---|---|
| 4 | forward-death attribution | what actually kills our forward builders vs the field's — tile exposure explains only 1.53x of a 3.47x gap; ~2.3x is unaccounted and nothing has measured it. **~1h cut off surfaces that already exist.** |

## DEAD THIS SESSION — do not re-queue without new evidence
* **cap6** (`LOKI_FWD_GUN_CAP` 3->6) — **INERT BY CONSTRUCTION**: we build 1.6-1.9
  forward sentinels/game, so a cap of 3 was never binding. *(Structural argument
  only. Its paired dose check is NOT evidence — see the RNG note below.)*
* **best-fit sentinel placement** — **CPU-COST REGRESSION**: with the 10 ms limit
  disabled it wins 6/6; with it on it loses 5/6. n=12, worth one repeat before
  the road is closed permanently rather than just this implementation.
* **gunner-axis / LOKI-25** — died s30 on a resolved mechanism falsifier
  (deaths -24%, presence -23%, ratio flat -2.3%). ROAD open, implementation dead.
* **forward-efficiency 880-game screen** — DROPPED for this horizon. Its protected
  denominator needs 700-900 games/arm and at 440 misses LOKI-25's own magnitude
  (3.21 vs a 3.278 threshold). Also: dwell is 17% of the gap, not 54% — the
  headline was a 120-game sampling artefact.

---

## ⛔ READ BEFORE TRUSTING ANY LOCAL NUMBER IN THIS FILE
**Our bot reseeds an UNSEEDED RNG every game.** `bots/_v130loki13/main.py:276`:
`self.spawn_salt = random.Random().randrange(97) if NOISE_ON else 0`, with
`NOISE_ON = True`. **`--seed` never controlled it.** Identical seed/map/bots gave
kill turns 109, 118, 227, 302, 527, 118.

⇒ **"SEED-MATCHED PAIRING" IS AN ILLUSION IN EVERY LOCAL BATTERY WE RUN**, including
s30's 8x1024 screens, the 4,096-game null, and `dose.py`. The noise is unbiased so
POOLED estimates stand; PAIRED designs buy nothing they claim to buy.

**`gate.py` HAS WARNED ABOUT THIS ALL ALONG** — *"paired fixtures do not pair
against a bot that reseeds"* — **and `h2h.sh` and `dose.py` both bypass gate.py,
which the standing rule calls the sole entry to a battery.** The check existed;
the tools that needed it skipped it. **Fix: pin `NOISE_ON = False` in the measured
COPIES, or route every battery through the gate.**
