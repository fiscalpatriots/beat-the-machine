# Performance audit, 13 September 2026

Measured in Chrome against the three pages served over HTTP on a local static server, read
off the network panel and cross-checked against `performance.getEntriesByType('resource')`
plus the navigation entry for the document itself. The server sends everything uncompressed,
so the transfer figures below are the worst case; GitHub Pages gzips HTML, CSS, JS and JSON,
and the gzipped column is what a visitor actually pulls.

## First load, page by page

Screenshots are excluded from the budget, as the brief asks. The budget is 500 KB a page.

| Page | Requests | Uncompressed | As GitHub Pages serves it | Screenshots on first load |
| --- | --- | --- | --- | --- |
| `index.html` | 7 | 242.9 KB | 89.9 KB | none |
| `checker.html` | 5 | 201.3 KB | 74.9 KB | 86.7 KB, one hero figure |
| `review.html` | 7 | 117.3 KB | 41.6 KB | none on first load, all four are lazy |

Every page is inside the budget, the largest by uncompressed transfer being `index.html` at
242.9 KB, which is 49 percent of the allowance. Counting the checker's hero figure as well,
which the budget does not, that page still lands at 288 KB.

What each page pulls:

| File | Bytes | Gzipped | On which page |
| --- | --- | --- | --- |
| `index.html` | 167,852 | 49,345 | drill |
| `checker.html` | 159,200 | 49,162 | checker |
| `review.html` | 32,054 | 8,545 | review |
| `404.html` | 4,486 | 1,612 | the missing-path page |
| `assets/second-pass.css` | 18,841 | 5,792 | all |
| `assets/nav.js` | 6,801 | 2,452 | all |
| Figtree stylesheet from Google | 427 to 727 | — | all |
| One Figtree woff2 | 20,156 | — | all |
| `cases/halyard-v4.json` | 27,114 | 6,973 | drill, review |
| `cases/brightwater-v4.json` | 13,077 | 3,525 | drill, review |
| `screenshots/checker/hero-results.png` | 88,770 | — | checker |

The two case files are fetched by the drill to play and by the review page only to stamp a
version number on the rail; the review page prints the same text already, so a failed fetch
changes nothing on screen.

## Fonts

Both of my pages preconnect to `fonts.googleapis.com` and to `fonts.gstatic.com` with
`crossorigin`, and the font request carries `display=swap`, so the page sets in Open Sans or
the system face immediately and swaps to Figtree when it lands. One woff2 is pulled, 20 KB.
The fallback stack behind it is the one the Mason typography guidance names.

## Images

| Image | Intrinsic | `width`/`height` | Loading |
| --- | --- | --- | --- |
| `screenshots/checker/hero-results.png` | 1280x600 | yes | eager, `fetchpriority="high"` |
| `screenshots/review/strip-01-checker-empty.png` | 1280x960 | yes | `lazy` |
| `screenshots/review/strip-02-checker-results.png` | 1280x960 | yes | `lazy` |
| `screenshots/review/strip-03-drill-card.png` | 1120x840 | yes | `lazy` |
| `screenshots/review/strip-04-drill-end.png` | 1120x840 | yes | `lazy` |

Every image carries its true pixel dimensions, so the box is reserved before the bytes arrive
and nothing below it moves. The checker's hero figure sits 460px down a 1280 by 800 screen,
inside the first view, so it is fetched eagerly and at high priority; lazy-loading the one
image most likely to be the largest contentful paint would have cost time, not saved it. The
four review thumbnails start around 1,500px down and are all lazy. Everything else drawn on
either page is inline SVG, which costs no request at all.

## Scripts

Nothing blocks rendering on either page. `assets/nav.js` is the only external script and it
carries `defer`. The checker's own script is one inline block at the end of the body, and the
review page's version stamp is a short inline block in the same place. No third-party script
is loaded anywhere; the only third-party request on any page is the Google font.

## Stylesheet

`assets/second-pass.css` is 18,841 bytes, 5,792 gzipped, against a 40 KB ceiling. It is at 46
percent of the budget, so nothing had to come out to meet it.

## Unused CSS, and why almost none was cut

Selectors were tested by walking the sheet, pulling every selector out of it, and asking each
of the three pages, at 375 and at 1280, whether anything matched, with the checker driven
through four sample cases so the results table, the stat tiles, the action bar and the
reviewer's queue all existed. That pass is not proof on its own: it cannot see a hover or
focus state, and a state the run had cleared reads as dead when it is not. Every candidate it
produced was therefore checked a second time by grepping the literal class name across
`index.html`, `checker.html`, `review.html` and `assets/nav.js`.

Three names survived both passes and appear nowhere in any of the three pages:
`.stmt-fig`, `.btn.ghost` and `.btn.block`. Together they are about sixty bytes of a sheet
already at 46 percent of its ceiling, and two of the three are tokens inside rules the live
buttons share, so cutting them means editing a rule that three pages depend on. The sheet is
a design standard another lane is building against while this was written. They were left in
place deliberately; the saving does not pay for the risk. Everything else the first pass
flagged was proved to be in use.

## Horizontal scroll and console

Checked at 320, 375, 768 and 1280 on `checker.html` (empty and after a run), `review.html`
and `404.html`. At every width the document element, the body and every scrollable ancestor
report a scroll width equal to the viewport width, and the maximum horizontal scroll offset
is zero. The only elements whose boxes reach past the viewport are the `th` and `tr` inside
the results table's `<thead>`, which is clipped to one pixel and read aloud rather than drawn
once the table stacks on a phone. No console errors and no thrown exceptions on any page at
any width. All 53 checker fixtures pass.
