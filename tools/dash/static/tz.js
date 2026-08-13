/* LOCAL-TIME RENDERING — ONE implementation, loaded by every dashboard page.
 *
 * ⛔ WHY THIS FILE EXISTS. Every stamp this dashboard serves is UTC, and every
 * page printed it raw. Magnus reads Stockholm time (UTC+2) and misread the match
 * list as running HOURS BEHIND — a dashboard whose whole premise is that a
 * healthy line and a blind line must not look alike had made a current line look
 * stale. The clock was right and the reader was wrong, which is the dashboard's
 * fault, not the reader's.
 *
 * ⛔⛔ AND THE UTC ORIGINAL IS NEVER DESTROYED. `docs/coordination.md`, every
 * monitor log, `fcode match list` and the platform itself are ALL in UTC, so a
 * page that only shows local time makes cross-referencing a mental arithmetic
 * problem — trading one misreading for another. Every converted stamp carries
 * its exact source string in `title=`, so hover gives back the value you can
 * grep for.
 *
 * ⭐ THE TRAILING `Z` IS THE DISCRIMINATOR. A converted stamp renders as
 * `2026-08-13 13:44:20` with NO zone letter; anything still ending in `Z` on
 * these pages is a verbatim quote out of a file (a heartbeat line, a server-side
 * sentence) and is still UTC. So the two are told apart by looking, not by
 * remembering.
 *
 * ⛔ A STAMP WITH NO ZONE MARKER IS NOT CONVERTED. `new Date("2026-08-13T11:00")`
 * silently reads as LOCAL, so converting an unmarked stamp would shift it by the
 * offset twice and produce a plausible wrong time. `serve.py`'s own parser
 * carries the identical warning (elo_history.tsv writes local wall-clock with no
 * marker and reading it as UTC produced a negative age). Unmarked stamps render
 * raw, flagged, and unconverted.
 */
'use strict';

const TZ = (function () {
  // getTimezoneOffset() is minutes BEHIND UTC, i.e. sign-flipped from the label.
  const off = -new Date().getTimezoneOffset();
  const a = Math.abs(off);
  const label = 'UTC' + (off < 0 ? '-' : '+') + Math.floor(a / 60)
    + (a % 60 ? ':' + String(a % 60).padStart(2, '0') : '');
  let name = '';
  try { name = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) { name = ''; }
  return {offsetMin: off, label: label, name: name};
})();

const TZ_ZONED = /(?:Z|[+-]\d{2}:?\d{2})$/;

function tzEsc(s) {
  return String(s === null || s === undefined ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* The local wall-clock of `iso`, as `YYYY-MM-DD HH:MM:SS`.
 *
 * Built from the Date's own local getters rather than toLocaleString: the
 * format is then identical in every browser and every locale, sortable, and
 * re-parseable — which is what lets `match_diffcheck.py` re-derive it in Python
 * and prove the page is not printing UTC with a local label on it.
 * Returns null when the stamp cannot be converted; callers must handle that
 * rather than substituting something plausible.
 */
function tzLocalStamp(iso, opts) {
  opts = opts || {};
  if (!iso || !TZ_ZONED.test(String(iso).trim())) return null;
  const d = new Date(iso);
  if (isNaN(d.getTime())) return null;
  const p = n => String(n).padStart(2, '0');
  const date = d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
  const time = p(d.getHours()) + ':' + p(d.getMinutes())
    + (opts.sec === false ? '' : ':' + p(d.getSeconds()));
  return opts.timeOnly ? time : date + ' ' + time;
}

/* One timestamp, rendered local, with the UTC original on hover.
 *
 * `class="ts"` is load-bearing: match_diffcheck finds every converted stamp by
 * it and checks the visible text against the title. An unclassed timestamp is
 * one nothing verifies.
 */
function tzTime(iso, opts) {
  opts = opts || {};
  if (!iso) {
    return '<span class="badge b-blind" title="the server sent no timestamp for '
      + 'this field">NO STAMP</span>';
  }
  const local = tzLocalStamp(iso, opts);
  if (local === null) {
    return '<span class="badge b-blind" title="this stamp carries no UTC marker, '
      + 'so converting it could shift it by the offset twice — shown raw and '
      + 'unconverted">NO ZONE</span> <span class="mono">' + tzEsc(iso) + '</span>';
  }
  const cls = opts.cls === undefined ? 'ts mono' : ('ts ' + opts.cls);
  return '<span class="' + cls + '" title="' + tzEsc(iso) + ' — the source value, '
    + 'in UTC. Logs, coordination.md and the platform are all UTC; this page '
    + 'shows ' + tzEsc(TZ.label) + '.">' + tzEsc(local) + '</span>';
}

/* The standing note that belongs beside every data-age line. */
function tzNote() {
  return '<span class="badge b-dim" title="Converted from the UTC the server '
    + 'sends. Hover any timestamp for its original value.' + (TZ.name
      ? ' Browser zone: ' + tzEsc(TZ.name) + '.' : '')
    + '">times shown in your local timezone (' + tzEsc(TZ.label) + ')</span>'
    + ' <span class="vs">hover any timestamp for the UTC original; anything still '
    + 'ending in <code>Z</code> is a verbatim quote from a file and stays UTC</span>';
}
