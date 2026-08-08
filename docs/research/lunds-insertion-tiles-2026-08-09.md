# Lunds insertion tiles: invariant to our version, and a correction to "absolutely oriented"

**Research arm, session 20, 2026-08-09 03:2x CEST.** Live **v80**, window n=9/20.
**Zero downloads** — 45 archived Lunds replays, 1,124 throws extracted. Retires
the one unknown left on the builder's Lunds fixture.

**Method** (per tooling.md, s14 ferry-loop re-check): a launcher throw is a
**long `moveBuilderBot`** — a move update with Chebyshev distance > 1 — never a
FireTurret. Ownership attributed to a launcher adjacent to the source tile.

---

## 1. The fixture's remaining unknown is retired: the tile does not move under us

Lunds's first throw lands on **round 3** (median 3 over 44 games) and the tiles
are a pure function of (map, seat), **identical across every one of our versions
that played them**:

```
map          seat   from -> to            our versions            invariant?
snowflake     a     (18,18) -> (14,14)    v74, v75, v76, v80      YES  (4 heads)
nordkap       b     ( 9, 8) -> ( 9,14)    v74, v76, v80, v81      YES  (4 heads)
snowflake     b     ( 7, 7) -> (11,11)    v74, v76, v79           YES  (3)
moonrise      b     ( 7, 4) -> (13, 3)    v79, v80, v81           YES  (3)
hive          a     (20, 4) -> (15, 8)    v75, v76, v80           YES  (3)
eider         a     (18, 9) -> (12, 9)    v74, v76                YES
eider         b     ( 9, 9) -> (15, 9)    v74, v79                YES
heart         a     (18, 9) -> (12, 9)    v76, v80                YES
heart         b     ( 9, 9) -> (15, 9)    v80, v81                YES
atoll         a     (14, 4) -> ( 9, 8)    v74, v76                YES
saga          b     ( 6, 6) -> (10,10)    v79, v80                YES
drumlin       a     (17,17) -> (13,13)    v74                     n=1
drumlin       b     ( 7, 7) -> (11,11)    v76                     n=1
nordkap       a     ( 9,17) -> ( 9,11)    v80                     n=1
archipelago   a     (20,18) -> (16,14)    v75                     n=1
archipelago   b     ( 6, 7) -> (11,10)    v81                     n=1
jackpot       b     ( 1, 2) -> ( 5, 7)    v80                     n=1
lighthouse    b     ( 5, 5) -> ( 9, 9)    v81                     n=1
meander       b     (12, 6) -> (13, 2)    v76                     n=1
```

**Not one cell varies across our versions.** Five cells are confirmed over three
or four of our heads, spanning the E-family bundle, the hive fix and PIECE MAG.
This is the post-contact half I flagged as unverified when lifting the block —
**it is now verified, and it behaves like the pre-contact half.**

**The fixture can hard-code these tiles.**

## 2. Correction to `lunds-switch-decode-2026-08-08.md`

That document claims the insertion is **absolutely oriented** — the same absolute
tile regardless of seat — and reasons from there that "the mirror landing tiles
are verified free, so the trigger is in THEIR code, not the geometry."

**Tested properly, that is true on a minority of maps.** Each map's symmetry was
derived from its own tile grid (the transform that maps the grid onto itself),
not assumed, then the seat-a tiles were mapped through it and compared to the
seat-b tiles:

```
map           grid symmetry    tiles follow it?
drumlin       ROT180           YES
eider         XREFL            YES
heart         XREFL            YES
nordkap       YREFL            YES
snowflake     ROT180           YES
--------------------------------------------------
atoll         ROT180           NO — absolute
archipelago   ROT180           NO — absolute
fjordgate     ROT180           NO — but see caveat
```

**Five of seven comparable maps follow the map's own symmetry.** The insertion is
predominantly *mirrored correctly*, not absolutely oriented.

**Scope limits, stated because they matter here:**
- **fjordgate should be excluded**: seat a's first throw is round 2 and seat b's
  is round 8. Those are probably not the same behaviour, so the comparison is
  invalid. That leaves **5 symmetric / 2 absolute**.
- **archipelago is n=1 per seat**, measured under our v75 and v81 respectively.
  Weak.
- **I cannot test moonrise**, which is the map the original claim was made about
  — only seat b appears in the archive. **The specific moonrise claim is
  untested by this work; only the general property is corrected.**

So: the general statement "Lunds's insertion is absolutely oriented" does not
hold. Whether it holds *on moonrise* is still open, and that is where the
original seat-split argument lived.

## 3. Incidental: we throw twice as much as they do

```
throws in 45 Lunds games:  OURS 759   THEIRS 365
```
Not the question asked, and not analysed. Recorded because it is a large
asymmetry sitting in the same data and someone will want it.

## 4. Caveats

- Ownership is attributed to a launcher within Chebyshev 1 of the source tile.
  If both teams had a launcher adjacent to the same tile the attribution would
  be ambiguous; that case was not checked for.
- "First throw" is restricted to round ≤ 10 for the tile table, to isolate the
  r3-class insertion from late-game ferrying. Games whose only throws are late
  (moonrise r152, antler r156, antler r120) are excluded from the tile table and
  appear only in the round distribution.
- 1,124 throws across 45 games is a large sample of throws but only 44 games with
  a Lunds-owned throw, so per-(map,seat) cells are 1–4 games.
