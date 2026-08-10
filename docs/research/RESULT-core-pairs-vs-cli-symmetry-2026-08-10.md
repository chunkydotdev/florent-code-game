# RESULT — `CORE_PAIRS` vs the CLI's "rotational" label. **NO DEFECT. ACTING ON THE FLAG WOULD HAVE CREATED ONE.**

**Flag (side lane, s28):** `fcode maps list` declares all 15 pool maps
`rotational`, but point reflection `(w-2-x, h-2-y)` reproduces only **23 of 31**
`CORE_PAIRS` entries. Mismatches have the shape of a MIRROR. Priced as a
possible live offensive defect — raiders sent to the wrong corner on `antler`,
`nordkap` and `meander`, ~24 rounds of a 250-round window, paid at the far end.

**Test, as specified: read BOTH cores off the wire from archived ladder replays
and ask which transform maps one to the other.** `map_admits.map_facts` already
does this; the maps were resolved by exact terrain fingerprint.

| map | dims | wire cores | in `CORE_PAIRS`? | point-rotational? |
|---|---|---|---|---|
| antler | 14x18 | A(6,4) B(6,12) | **YES, exact** | yes |
| nordkap | 20x26 | A(9,6) B(9,18) | **YES, exact** | yes |
| **meander** | 25x15 | **A(11,3) B(11,10)** | **YES, exact** | **NO** |

## ⇒ THE VERDICT INVERTS. `CORE_PAIRS` IS RIGHT AND THE CLI LABEL IS THE IMPRECISE ONE.

**`meander`'s real cores are mirror-symmetric in y, not point-rotational.** The
rotation transform predicts `(12,10)`; the engine says `(11,10)`. **Our table
carries `(25, 15, 11, 3, 11, 10)` — exactly what the wire shows.** So the
incumbent's comment — *"Several maps are mirror-symmetric rather than
180-degree symmetric"* — **is TRUE, and the platform's blanket `rotational`
column is what does not survive contact with the replays.**

**AND THE STAKES RUN THE OTHER WAY FROM THE FLAG.** *"Fixing" `CORE_PAIRS` to
agree with the CLI would have MOVED meander's B core from the correct `(11,10)`
to `(12,10)` and introduced the exact defect the flag was raised to prevent.*
**A live pool map would have been broken by trusting a label over the wire.**

## WHY THE FLAG LOOKED RIGHT — the reasoning error is worth more than the result

`CORE_PAIRS` holds **multiple entries per dimension**, because different arenas
share dimensions. For each flagged map the table contains **both** an older
entry and the current one:

```
(14, 18, 2, 2, 2, 14)  and  (14, 18, 6, 4, 6, 12)   <- antler, current
(20, 26, 2, 2, 2, 22)  and  (20, 26, 9, 6, 9, 18)   <- nordkap, current
(25, 15, 0, 0, 0, 13)  and  (25, 15, 11, 3, 11, 10) <- meander, current
```

**Testing every entry against a rotation formula flags the ones describing
mirror-symmetric arenas — which are correct records of asymmetric maps, not
errors.** The audit measured *"does this table agree with a formula"* when the
question was *"does this table agree with the engine."* **A table can disagree
with a rule and still be right, if the rule is the thing that is wrong.**

## What is worth taking from the flag anyway

* **`fcode maps list` / `fcode maps sync` exist and nobody was querying them** —
  fourth instance today of *we had the tool and were not pointing it at this*.
  Exact dimensions for all 15 pool maps are available directly, which
  `map_admits` currently reconstructs from replays.
* **`map_admits` is hard-wired to the 5 pinned maps.** The capability generalises
  to any map with an archived replay; only the argument handling is missing.
* **The CLI's `Symmetry` column is not a reliable input for geometry.** Treat it
  as documentation, not as data. **The wire is the authority.**
