# The spawn budget is code-shaped — but it does NOT explain the r250 wall. Dispatch does.

**Research arm, session 23, 2026-08-09.** Code read + corpus. Zero downloads, zero
arena, zero bot edits. Live bot **v91 "Eir 9c hivethaw"** = `bots/_v100hf`.

**A hypothesis of mine, tested and refuted by my own follow-up check** — recorded
because the refutation is more useful than the hypothesis was, and because the
by-product independently corroborates the builder arm's mechanism for the r250 wall.

---

## 1. What I found in source, and it is real

`main.py:28` — *"self.n counts builders **SPAWNED over the match**"* — a **lifetime**
counter, not a live one. And `:1802` `budget_ok = self.n < spawn_budget`, where

```
spawn_cap    = 5      (MAX_BUILDERS; 4 on nordkap-home-A, 6 on snowflake-home-B)
spawn_budget = spawn_cap + min(REPLACEMENT_MAX = 8, lost_units)          -> 13
             + SURGE_EXTRA = 5   iff  ti >= 1500  AND  rnd >= 300        -> 18
```

**The corpus shows those three numbers as spikes in the distribution of lifetime
builder spawns per game**, which is a code shape, not a game shape:

| lifetime builder spawns | games (all) | games (turns ≥ 300) |
|---|---|---|
| **exactly 5** (`spawn_cap`) | **435 (34.7%)** | 88 |
| **exactly 13** (`+REPLACEMENT_MAX`) | 80 (6.4%) | 60 |
| **exactly 18** (`+SURGE_EXTRA`) | **152 (12.1%)** | **150 (21.6%) — modal** |

Median 8, mean 12.96, **max 91.** Three sharp spikes at exactly the three values
`spawn_budget` can take.

## 2. The hypothesis, and why it is wrong

I inferred: *the lifetime cap pins our live builder population, so every subsystem
stops growing at once — that is the r250 wall.*

**Checked, and refuted:**

| round | US live builders | THEM live builders |
|---|---|---|
| r100 | 4.57 | 4.44 |
| r200 | 5.16 | 5.20 |
| r300 | 5.57 | 6.00 |
| r500 | **7.21** | 6.74 |
| r800 | **7.87** | 6.97 |

**Our live population is not pinned. It grows past `POP_FLOOR`, and by r500-800 it
EXCEEDS the field's.** The `POP_CEILING_LIFT` exemption — which lifts the lifetime
bound for the refill-to-floor clause only — is enough to keep the population
growing, and the max of 91 lifetime spawns shows the bound is leaky by design.

**So the spawn budget shapes the spawn-count distribution and does not explain the
r250 wall.** Filed as refuted.

## 3. The by-product, which is the useful part

Put the population trajectory next to the third lane's heal-detail measurement:

| | r500-800 live builders | heal detail at 3+ attackers, r251-500 |
|---|---|---|
| **US** | **7.87** | **2.46** |
| **FIELD** | 6.97 | **3.53** |

**We have MORE builders than the field late and deploy a SMALLER heal detail.**

**That is not a supply problem. It is a dispatch problem** — and it is independent
corroboration of the builder arm's mechanism for the r250 wall: the chassis has **no
representation of threat magnitude.** `SLOT_THREAT` is one position, `SLOT_UNDER` is
a boolean, `_core_shelled` is a boolean; a grep for any magnitude term returns
comments only. **A threat model that saturates at one attacker cannot dispatch a
second healer for the second attacker — however many bodies are standing idle.**

The bodies are there. The bot cannot see that it needs them.

## 4. Limits

- The spike table counts **builds**, i.e. `placeEntity` for builder bots; the
  lifetime counter `self.n` is the bot's own and is not directly observable. The
  match is inferential, though three exact spikes at three exact constants is a
  strong coincidence.
- The population figures are **means over games that reached each round**, so later
  rows are increasingly survivor-selected — a game that ended at r400 contributes to
  r100-r300 and not to r500.
- §3 pairs my population numbers with the third lane's adjacency numbers, computed
  from **different decodes on different file sets.** The comparison is directional;
  neither figure was produced to be compared with the other.
- **This does not price anything.** A bot that can count attackers may or may not win
  more games; that is unmeasured, and today's record on mechanisms is four fired,
  zero won.
