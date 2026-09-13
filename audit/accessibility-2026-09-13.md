# Accessibility audit, 13 September 2026

Pages audited: `checker.html` and `review.html`. Tool: axe-core 4.10.2, loaded into each
page from cdnjs and run against the whole document with `axe.run(document)`. Every page was
run twice, once at a 375 by 812 viewport and once at 1280 by 900, and the checker was run in
both of its states: the empty page a visitor lands on, and the page after the Halyard sample
has been loaded and checked, which is when the results table, the status marks, the stat
tiles and the reviewer's queue exist.

Counts are nodes, not rules: one rule failing on nine selects counts as nine.

## Before

| Page and state | Critical | Serious | Moderate | Minor |
| --- | --- | --- | --- | --- |
| checker.html, empty, 375 | 0 | 0 | 22 | 0 |
| checker.html, empty, 1280 | 0 | 0 | 22 | 0 |
| checker.html, results, 375 | 9 | 0 | 467 | 1 |
| checker.html, results, 1280 | 9 | 0 | 467 | 1 |
| review.html, 375 | 0 | 16 | 6 | 0 |
| review.html, 1280 | 0 | 16 | 6 | 0 |

## After

| Page and state | Critical | Serious | Moderate | Minor |
| --- | --- | --- | --- | --- |
| checker.html, empty, 375 | 0 | 0 | 0 | 0 |
| checker.html, empty, 1280 | 0 | 0 | 0 | 0 |
| checker.html, results, 375 | 0 | 0 | 0 | 0 |
| checker.html, results, 1280 | 0 | 0 | 0 | 0 |
| review.html, 375 | 0 | 0 | 0 | 0 |
| review.html, 1280 | 0 | 0 | 0 | 0 |

Every finding at every level was fixed, not only the serious and critical ones.

## What was wrong, and what was done about it

**Nine selects with no name. Critical, `select-name`, checker results.** Every row in the
reviewer's queue that asks what a figure is carries a dropdown, and the label above it was a
bare `<label>` pointing at nothing. A screen reader read nine controls called "combo box"
with no idea which figure each one belonged to. Each select now takes an id of its own and
its label points at it, so the control announces as "Confirm what this figure is".

**Sixteen numerals below the contrast floor. Serious, `color-contrast`, review.** The ordinal
numerals on the review page (01 through 06 on the sections, 01 through 04 on the strip) were
set in gold, which reads at 1.88:1 on the paper and 2.08:1 on a white card against a floor of
4.5:1. They are now Mason green, 8.4:1 on paper. This is also what the Mason brand guide asks
for: gold is not allowed to set type on white, so it now appears only as the rule under the
band, the trophy and the underline beneath a headline numeral.

**Neither page had a main landmark, and most of both pages sat outside any landmark.
Moderate, `landmark-one-main` and `region`, 465 nodes on the checker and 6 on the review.**
The checker's outer container is now `<main id="app">`. The review page had a `<main>` but it
opened halfway down, after the rail, so the title, the hero, the statement and the strip were
all outside it; it now opens above the Mason band and closes at the end of the page, and the
column that used to be the main element is a plain div.

**A heading level skipped. Moderate, `heading-order`, checker.** "Parse preview" was an `h3`
sitting directly under the `h1` with no `h2` between them. It and "Previous runs" are now
`h2`, drawn at the size they were drawn at before.

**A table header with nothing in it. Minor, `empty-table-header`, checker.** The status column
of the results table had an `aria-label` on the `th` and no text. It now carries the word
Status as text that is read and not drawn, and every `th` in that table carries `scope="col"`
so each cell is tied to its column.

## Fixed beyond what axe reports

**The status marks were pictures with no words.** The tick, the square, the circle and the
cross in the first column are `aria-hidden` SVGs. The status word now sits beside each mark
in text that is read and not drawn, so a row reads "checked within scope" rather than
skipping the column.

**The run had no voice.** A run rewrites a results table a long way down the page and said
nothing. There is now one polite live region that speaks a single sentence when a run ends:
the run identifier, the sentences read, the four counts, the silent lines and the queue
length. The table itself is not a live region, so nothing is announced cell by cell. The
error notes above the panes are a status region as well, so an empty ledger is spoken.

**No skip link.** `assets/nav.js` now prints a skip link as the first thing in the body on
every page that loads it, points it at that page's main region, and gives that region
`tabindex="-1"` so focus actually lands there. It is off-screen until it takes focus, and
then it paints in Mason green with a gold focus ring. Because it is in the shared script,
`index.html` gets it too without the drill lane wiring anything.

**Focus order.** Tab order is document order on both pages; nothing carries a positive
`tabindex`. The skip link is first, then the wordmark and the three navigation links, then
the page. The segmented controls were already a labelled `role="group"` of buttons carrying
`aria-pressed`, and the script keeps that attribute in step with the hidden input behind it.

**Print.** The shared header, footer and skip link are hidden in print media, so the
checker's summary sheet prints as the summary sheet and nothing else.
