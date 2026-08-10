# NO PRE-REGISTRATION IN THIS TREE. See `docs/prereg/`.

**This file previously contained LOKI-8's pre-registration**, inherited when the
tree was copied from `bots/_v124loki8`. Emptied deliberately.

**This is the SECOND time tonight a copied tree carried its parent's prereg**
(the first was `bots/_v131loki14`), and this time it was caught by a live
consequence rather than by a reading: **`tools/preflight.py bots/_v132loki15`
read LOKI-8's bars and printed "READY TO SHIP".** A ship gate answering a
question about a bot it was not looking at.

**The class, not the instance:** copying a bot directory copies its
pre-registration, and every downstream tool that greps `bots/*/PREREG.md`
inherits the stale bars silently. **Leg preregs live in `docs/prereg/` with both
clocks. A bot directory is code.**

LOKI-15 = v102 + a per-builder conveyor quota (`LOKI15_CONV_CAP_ON`,
`LOKI15_CONV_MAX = 3`). Its pre-registration is
`docs/prereg/PREREG-loki15-conveyor-quota-2026-08-10.md`.
