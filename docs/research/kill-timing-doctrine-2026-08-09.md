# When do cores die, and should ours be the one killing? — Magnus's question, answered

**Research arm, session 21, 2026-08-09.** Commissioned by the builder after
Magnus asked: *"Should our new target be to kill the core? Could we use the
highest-Elo players as a guideline on WHEN they kill cores?"*

Live at time of writing: **v88 "Thor 1 gunline"** (`0fde5029`, `bots/_v102thor`),
baseline 1524.026641 @ 483. Corpus: **482 matches / 2,410 games**, our v1–87,
free metadata already cached (`scratchpad/matchinfo.jsonl` +
`matchlist.json`). **ZERO replay downloads, ZERO new API calls.**

Classifier **B** throughout: mean `ratingBefore` per **(opponent name, opponent
version)**. See §0 — the first version of this analysis used the wrong key.

---

## 0. A correction to my own item (ii), made before anything is built on it

`fcode match info --json` returns **the opponent's version as `null`** — a trap
already on the tape in HANDOVER's tooling section. I built classifier B from
that payload, so every key was `(opponent, None)`, which is **classifier C
(per-name), not B (per-binary)**. I argued for B over C on principle and then
shipped C under B's label.

Rebuilt with the version joined from `match list` (482/482 non-null, 132
distinct binaries vs 52 names). **The conclusions of
`kill-game-split-recompute-2026-08-09.md` are unaffected; the numbers move by
under 1pp:**

```
same 500 games, threshold 1550        STRONG    WEAK    kill-game win% S/W
B per-(opp,VERSION)  [corrected]       44.6%   66.7%      40.9% / 62.3%
C per-name           [what I shipped]  45.4%   66.7%      41.9% / 61.4%
A at-match                             42.9%   67.8%      39.8% / 63.0%
X current rating     [the doc's field] 49.1%   46.7%      44.4% / 46.7%
```

**Standing numbers stand: carry ~45% / ~67% for the split and ~41% / ~62% for
the kill-game mixture.** The label was wrong, the conclusion was not.

## 1. The rate decomposition — this is the actual answer

Full corpus, classifier B:

```
band          games   WE kill them   THEY kill us   r1000 share   our win%
1650+           120       45.8%          43.3%         10.8%        52.5%
1550-1649      1015       27.9%          44.2%         27.9%        42.4%
1500-1549       530       44.2%          30.0%         25.8%        59.4%
<1500           745       19.6%          14.4%         66.0%        56.8%

BINARY    STRONG >=1550  n=1135   WE kill 29.8%   THEY kill 44.1%   r1000 26.1%
          WEAK  <1550    n=1275   WE kill 29.8%   THEY kill 20.9%   r1000 49.3%
```

> **Our core-kill production is 29.8% against strong opposition and 29.8%
> against weak opposition. Identical. What changes with opponent strength is
> how often THEY kill US — 20.9% → 44.1%.**

This reframes the premise. The observation that started the commission — *the
top band rarely enters r1000, so we may be optimising for a game state they
rarely enter* — is arithmetically right but attributes it backwards. **The grind
share collapses against strong teams because they kill us, not because either
side converts faster.** We already produce core kills at the same rate against
everyone.

## 2. When do they kill? LATE. They do not rush.

Kill rounds, classifier B, strong band (n=507 kills against us):

```
STRONG >=1550   THEY kill us   median r296   (q1 r166, q3 r475)
                WE kill them   median r148   (q1 r99,  q3 r251)
WEAK  <1550     THEY kill us   median r188
                WE kill them   median r156

share of strong-band kills against us landing by round:
   r100  12%      r150  22%      r200  32%      r300  51%      r400  66%
```

**Only 12% of the kills the strong field lands on us arrive by round 100, and
half arrive after round 300.** Whatever the top tier is doing, it is not a rush.

This is consistent with — not contradictory to — `top-tier-decode-2026-08-09.md`
finding they open gunners at r19 against our r53. **They invest in military
early and convert late.** Early guns and early kills are different claims, and
only the first one is supported.

**Our own kill round is ~r148–156 regardless of opponent.** We already kill
*earlier* than they do. We simply do it in under 30% of games.

### Selection warning, stated because it limits the comparison

"They kill at r296, we kill at r148" compares **our slow losses against our fast
wins** — both figures are conditioned on who won. It is *not* a speed gap
between two bots. For the question asked ("when do the top players kill cores")
conditioning on them killing is correct, so §2's headline stands; the
cross-comparison does not.

## 3. Q4 — does our kill production move with our version? No. Survival does.

Mix-controlled: the **7 opponents played in all three lineages** with ≥15
strong-band games each (CtrlAltDefeat, Kings College Munich, Lunds Stallions,
OopsGotYourElo, Ouroboros, Powerpuff Girls, Team 48). **770 games.**

```
lineage          games   WE kill%   med rnd   THEY kill%   med rnd   r1000%   WIN%
v53-70             320     20.0%      163       52.2%       280     27.8%   33.8%
v71-76             185     23.8%      179       47.0%       343     29.2%   37.8%
v77-84 (Eir E)     250     17.6%      132       38.8%       387     43.6%   39.6%
```

**Read down the columns:**

- **Our kill production: 20.0 → 23.8 → 17.6%. No trend, and it ends lower than
  it started.**
- **Their kill rate against us: 52.2 → 47.0 → 38.8%. Monotone improvement.**
- **Their median kill round: r280 → r343 → r387. We survive 107 rounds longer.**
- **Grind share: 27.8 → 43.6%.** We convert kills into grinds.
- **Win rate: 33.8 → 37.8 → 39.6%.** +5.8pp across ~40 shipped versions.

> **Every plank from v53 to v84 bought survival. None bought kills.** The
> survival lever is real — it produced +5.8pp — but it has been worked for forty
> versions and the kill lever has never been pulled.

That is the evidence-backed case for a doctrine change rather than another dial.
It is **not** a claim that our planks did nothing.

### Confound, stated rather than waved at

The opponents shipped too (13 / 9 / 14 distinct binaries per lineage). For
*their* falling kill rate the confound pushes **against** the observed
direction — improving opponents should kill us more, and they killed us less, so
that half is robust. For **our flat kill production it does not clear**:
"their defence improved" is a live alternative to "our offence didn't". This
data cannot separate them.

## 4. Do NOT read a top-band advantage from the 1650+ cell

The 1650+ row reads 52.5% win rate — *above* the band below it (42.4%,
z = +2.12). It is an artifact of one opponent:

```
Leviathan v25    n=30  win 53%        kladde v75      n=10  win 10%
Banminary v41    n=30  win 77%  <--   Coreflood v63   n=10  win 40%
gsxWins v22      n=25  win 56%        Landers v62/v93 n=10  win 30%
                                      SmartFridge v55 n= 5  win 40%
```

120 games = **24 matches across 8 binaries**, and **Banminary v41 alone (6
matches, 77%) carries the entire apparent advantage** — drop it and the cell
reads **44.3%**, in line with the band below. The z-statistic also overstates:
games come 5 to a match and are not independent.

**Report the ≥1550 binary, not a band ladder.** This supersedes my earlier
"thin cell" caveat with a specific cause.

## 5. What this supports, and what it does not

**Supports:**
- Kill production is the untouched lever. Forty versions of survival work
  produced +5.8pp and the grind share nearly doubled. (§3)
- If timing is copied from the top tier, copy **r200–300**, not a rush. Only
  12% of their kills land by r100. (§2)
- The v88 gunline direction is aimed at the right variable.

**Does not support:**
- *"We are bad at killing cores."* We kill at 29.8% against everyone,
  band-invariant, at median r148 — earlier than the field does. (§1, §2)
- *"The top band is easier than the band below."* One opponent. (§4)
- *"Delivered titanium is wasted effort."* The grind is still 26% of strong-band
  games and 49% of weak ones, and `grind-pocket-audit-2026-08-09.md`'s caveat
  (58.2% is real; "therefore losing a grind is a cost" is unsupported) is
  untouched by anything here.

**The sharpest single sentence available from this corpus:** *we die 44% of the
time against strong opposition and 21% against weak, while killing at 29.8%
against both — so our result against the strong field is set by our death rate,
not our kill rate, and it is the death rate we have already spent forty versions
improving.*

That tension is real and I am not going to resolve it by picking a side: §3 says
the survival lever is near exhausted, §1 says the death rate is still what
decides the games. **Those are compatible only if the remaining survival gains are
cheaper to buy through offence — killing them first — than through more
defence.** That is a build question, not a measurement one, and it is the
builder's to answer.
