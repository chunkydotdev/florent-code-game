# PREREG — PANEL-CAL-3: v125 band-refreshed calibration panel (unrated, incumbent)

**Committed 2026-08-13T14:57:19Z (`date -u`), BEFORE any leg of this panel is created (two-clock).**
**Authorisation: Magnus, direct — *"We need to update the band of opponents we
run unrated against."*** Successor to PANEL-CAL-2, which is CLOSED at its
current n (see below). Design, discipline and operational lessons inherited
whole from CAL-1 Amendment 1 + CAL-2.

## Why a NEW panel and not an amendment
Swapping cells mid-panel breaks pooling semantics: CAL-2's totals would mix
two different opponent sets under one n and one look schedule. **CAL-2 is
closed at its games-to-date and reads DESCRIPTIVE ONLY (it never reached its
n=150 comparative look); CAL-3 starts a fresh n.** Retained cells' games are
NOT pooled across panels — same reason.

## What changed in the field (why the band moved)
Our rating climbed 1646 → **1710 live** (`fcode status`, v125 Loki v8) while
three CAL-2 cells left the admissible band: **The Bisons collapsed ~1690 →
1525** (Magnus reads them still falling), **Focalground and Lunds Stallions
fell out below**. A cell outside the pairing band measures a matchup the
ladder cannot produce — at a sixth of fixture capacity each.

## Cells — 6, stratified, gaps FROZEN at this commit (ours 1710 live; theirs = newest `league_matches` observation 13:52Z)
| cell | team | rating | gap (E frozen here) | stratum | team_id |
|---|---|---|---|---|---|
| C1 | team lazy | 1781 | −71 | stretch (profiled: point-blank sentinel) | 648d1d5b-5443-4257-a0aa-7048661b612d |
| C2 | Big O | 1778 | −68 | stretch (unprofiled — new information) | f3362833-2d7a-4636-9a3c-e4f10fcebdc1 |
| C3 | **Leviathan** | 1776 | −66 | **core-tank class we are building against** | 26286680-d861-4f9e-9073-a6201bd48d3b |
| C4 | Jython | 1716 | −6 | even | 8cf9b751-00d3-484a-b0ed-e3073ae1d46f |
| C5 | Juusto | 1704 | +6 | even | 32087804-2dde-4265-acb2-b6ec9039fbee |
| C6 | Coreflood | 1663 | +47 | below | ea0d33c8-ca2b-497a-9be0-1837379eab1e |
**C3 rationale (builder's, adopted):** Leviathan is in band AND is the
opponent class every current offensive plank (#42 volume, #37 tap, #40 seal,
UNDERECO) is aimed at — so every C3 window doubles as free field evidence for
the build programme. Their churn (v55→v63+ in 24h) argues for continuous
rather than one-shot sampling. **C6 chosen over arsonist duck (−0) because
the even stratum is already covered twice (C4/C5); Coreflood widens spread.**

## ⭐ NEW STANDING RULE — RE-FREEZE AT PANEL n BOUNDARIES
*(Magnus's design point, adopted.)* **Gaps re-freeze at the pre-committed look
boundaries (n=150, n=300) and NOWHERE ELSE.** At each boundary: re-read the
band, record the new gap table in an ADD-only amendment, and use it for the
NEXT segment's E. Rationale: a frozen table ages in both directions (their
churn, our climb) and an un-refrozen table silently mis-states E; a
continuously-refreshed one is an unlogged researcher degree of freedom.
**Cell MEMBERSHIP changes require a new panel, not a re-freeze.**

## Looks, statistics, obligations — unchanged from CAL-2
Descriptive any time · **no comparative sentence below 25 games/cell** ·
comparative reads at panel totals **n=150 and n=300 exactly**; wrap below 150
= descriptive only · **MATCH-level clustering primary** (game-level binomial
labeled ANTI-CONSERVATIVE) · obligation 13 **N/A by construction** (no arms,
no treatment diff) · oppver pinned per game and reported as a mix · verdict
sentences are the builder's · **not rated evidence.**

## Operational (inherited, all measured s36)
Fire-registration gates on `match info <id>` status (never the CLI accept,
never the completes-only `match list`) · accepts consume rate-limit slots from
CREATION · rejections do not count · platform runner can back up 25+ min · the
team account has a second live operator (foreign accepts tolerated).

## Obligation 14 — opponent version churn at selection time (`league_matches`, 48h)
team lazy **13+ versions/48h** (v195→v213, extreme — C1 measures a moving
target, per-oppver subcells where n permits) · Leviathan v55→v63+ in 24h
(high) · Jython non-monotone (live rollbacks) · Big O / Juusto / Coreflood
moderate. **Any pooled cell figure carries its version mix inline.**
