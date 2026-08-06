# Strategy log

The point of this file: in a ladder game, the thing that compounds is knowing which changes
moved the rating and which didn't. Memory is unreliable and the ladder is noisy — write it down.

**One entry per deployed bot version.** Write the hypothesis *before* deploying, the result
*after* the ladder has settled. Keep dead ends — a documented failure is worth as much as a win.

Rules of thumb:
- Change one meaningful thing per version, or you can't attribute the result.
- Give the ladder enough matches to be meaningful before calling it. Note the sample size.
- If the result surprises you, that's a fact for [game-model.md](game-model.md), not a tweak.

---

## Template

### v0 — name

- **Date deployed:**
- **Commit / tag:**
- **Hypothesis:** what we believe and why we believe it
- **Change:** what's actually different from the previous version
- **Predicted effect:** stated before deploying, so we can be wrong on the record
- **Result:** rating before → after, over N matches
- **Read:** did the hypothesis hold? what did we learn regardless?
- **Next:** what this points at

---

<!-- newest entries at the top, below this line -->
