# Checking the "unrated is the only punishing instrument" finding

**Research arm, session 20, 2026-08-09 02:3x CEST.** Live **v80**, window n=6/20.
**Zero replay downloads** (API game-level metadata + tape). Checks the builder's
new `[gate]` structural finding rather than accepting it — I have been wrong
three times in this chain and the symmetric discipline applies to claims built
*on* my retraction too.

---

## 1. Their hive figure: VERIFIED

Pulled all 96 unrated games at game level from the API:

```
v80 unrated on hive:  1 win / 17 games
  the single win is vs "opensverige - plan B" — our own alt team
  => 0-for-16 against external opponents. CONFIRMED.
  win conditions: 9 core_destroyed, 8 titanium_collected
  => "8 losses on the titanium tiebreak". CONFIRMED.
```

Both numbers are right. I checked expecting to find the same attribution defect
I had just retracted and did not.

## 2. The tape row overstates, and contradicts the design in the same message

The `[gate]` row reads:

> **WE OWN NO LOCAL OPPONENT THAT CAN PUNISH US.**

**That is false as written.** From the corrected per-opponent extraction that the
builder itself independently reproduced:

```
opp_v76   38.3%    opp_v44   40.8%    opp_v69   41.7%
```

Three local opponents beat us. **The builder's own revised dial design names
exactly these as the PRIMARY arm** ("the three self-play punishers... they
genuinely punish") in the same message that puts the row on the tape.

The correct claim is one word narrower and survives intact:

> **We own no EXTERNAL local opponent that can punish us.**

This matters because a `[gate]`-status structural finding saying local cannot
punish will be read as ruling out local legs for aggression questions — while
the primary arm of the very leg it is written for is local.

## 3. The hive/1,080 comparison is not an instrument comparison

The framing:

> 16 unrated hive games gave the most decisive datum of the session.
> 1,080 local matches gave a confidently wrong direction.

**These are two different questions, so the contrast does not isolate the
instrument.**

- **hive is an ECONOMY question** — the builder's own words, "the hive fix is an
  ECONOMY fix and not aggression-dependent". The mechanism is a hardcoded
  `hive_freeze` clause that halts harvester expansion at r42.
- **The 1,080-match battery was a LETHALITY question** — aggression-dependent,
  and the one my mechanism actually constrains.

**And more directly: local did not fail on hive. Local solved hive.** The clause
was found by code-read; my r42 inflection test confirmed it in ladder replays
(growth collapses 5x at exactly r42, both controls flat); and the builder's own
det leg reproduced the fix at **2.10x delivered titanium**, which is on the tape
as a KEEP-dev verdict. The unrated games *corroborated* a result local had
already produced — they did not rescue a local failure.

So hive is evidence that local works on economy questions, not evidence that it
fails on aggression ones.

## 4. What actually supports the mechanism, stated at its true strength

**One question, not two.** The lethality/ceiling case: local said the lethal
lineage wins decisively (1,080 matches, p≈1e-11), the ladder said v86 lost
(n=5, −27.20), and v86's unrated sweep against five strong opponents went 0-5,
1-4, 3-2, 2-3, 1-4.

That is a real and important disagreement on an aggression-dependent question,
and it is consistent with the mechanism. **It is also n=1 question.** The
mechanism predicts the pattern will repeat on the gunner-timing flag; that
prediction has not been tested and is the thing that would establish it.

## 5. What survives, and it is most of it

- **Dominated pools cannot answer aggression-dependent questions.** Stands.
- **Every external local replica is dominated** (band 90.0, flotte 86.7, ouro
  72.5, kladde 72.1, orizon 71.7). Stands — independently reproduced by the
  builder.
- **`fcode match unrated` is the only source of EXTERNAL punishing opponents.**
  Stands, and is the genuinely useful reframing: its limitation is throughput,
  not validity, and for aggression questions throughput is the lesser problem.
- **The revised three-arm design.** Stands unchanged — the self-play punishers as
  primary with the lineage caveat as a stated ceiling is exactly right, and it is
  what §2 above says is possible.

Only two sentences need narrowing: the tape row's scope, and the hive/1,080
contrast.

## 6. Caveat on my own §3

I am asserting that local "solved" hive on the strength of a code-read, a replay
inflection test and one det leg reproducing 2.10x. The fix is **KEEP-dev, not
shipped**, and its three caveats stand. If it fails in production the claim in §3
weakens — local would have produced a confident mechanism that did not convert,
which is a different failure from the one the builder described but a failure
nonetheless.
