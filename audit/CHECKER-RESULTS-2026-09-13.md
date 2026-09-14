# The checker's results, readable on a phone, 13 September 2026

Lane F1, written at 11:55 PM EDT on 13 September 2026, for defects L7 and L8 in
`audit/USABILITY-BY-EYE-2026-09-13.md`. Every sample is synthetic. Nothing was posted or pushed.

## What was wrong

- **L7.** The "See it on a real case" figure was a 1,280 pixel screenshot of a run, shown at 258
  pixels on a 320 phone, so its text rendered near 3 pixels, and it printed a queue count and a run
  identifier from an older build.
- **L8.** The results were one table in which every check repeated its whole sentence, and below 760
  pixels each row stacked into a card. The Halyard sample's results ran to 44,311 pixels at 320.

## What changed, all in `checker.html`

- **The figure is words and a button.** "See it on a real case" names the Halyard case in reading
  size and carries **Run the Halyard sample**, which loads and runs the real case and brings the
  results into view. It holds no count, so it cannot go stale.
- **The results are ordered the way a reviewer works them.** After the coverage bar, the tiles and
  the counts line come four links with their counts: the sentences, the silent lines, the ledger lines
  and the reviewer's queue.
- **Every sentence, worst first.** Failed, then needs review, then not checked, then checked within
  scope, each group headed with its count. Each sentence is one disclosure whose summary carries its
  mark, label and status, the sentence once, and a tally such as `7 checks · 3 failed (Figure $6,500,
  Figure 3.5 percent, Threshold claim) · 4 passed`. Opened, it shows the status explanation and a
  table of that sentence's checks, with the role dropdown where one is needed. **Open every
  sentence** opens them all.
- **Silent lines** are never folded. **Every ledger line, recomputed** folds under its counts and opens
  by itself when a section total does not tie. **The reviewer's queue** is never folded, and now says
  how its entries divide: items left open, sentences carrying the judgment questions, and lines to
  read together, since the list runs longer than the queue count on the tiles.
- **Back to the top of the results** closes the sentences and the queue.
- Nothing that was on the page is gone. Every check row, finding and question is where it was one
  tap ago, the exports, the printed summary and Prompt 2 are unchanged, and the test suite, which
  reads the page text, passes 548 of 548.

## Heights, before and after

Document height and results height in pixels, on each sample run from its link. Before is `49ba98d`;
after is the working tree committed with this record.

| Sample | Width | Page before | Page after | Results before | Results after |
| --- | --- | --- | --- | --- | --- |
| Halyard | 320 | 48,380 | 17,065 | 44,311 | **12,962** |
| Halyard | 375 | 44,763 | 15,250 | 41,008 | **11,490** |
| Halyard | 768 | 28,653 | 10,675 | 25,566 | **7,819** |
| Halyard | 1,024 | 23,320 | 9,596 | 20,644 | **7,250** |
| Halyard | 1,280 | 22,338 | 9,510 | 19,636 | **7,163** |
| Halyard | 1,600 | 22,338 | 9,510 | 19,636 | **7,163** |
| Brightwater | 320 | 21,294 | 9,268 | 17,226 | **5,164** |
| Brightwater | 1,280 | 10,481 | 5,367 | 7,779 | **3,020** |
| Kestrel | 320 | 26,545 | 12,049 | 21,527 | **6,996** |
| Kestrel | 1,280 | 12,675 | 6,982 | 9,526 | **4,188** |
| Ridgeline | 320 | 12,938 | 7,747 | 9,050 | **3,824** |
| Ridgeline | 1,280 | 6,532 | 4,578 | 3,945 | **2,347** |

What is left on a phone is mostly the queue: Halyard's 19 entries, each with its sentence, its
finding and a Yes, No, Not on file row per question, are about 8,000 of the 12,962 pixels at 320. They
are the reviewer's work, so they stay open.

## Looked at

`checker-results-widths.cjs` ran each sample in headless Chrome with a throwaway profile at 320, 375,
768, 1,024, 1,280 and 1,600, and at every width captured the figure, the top of the results, the first
sentence opened, the silent lines, the ledger opened and the start of the queue. Every Halyard image
was opened and read at every width, and Kestrel's at 375 and 1,280; the images are in `after/`, and
the Halyard before images are in `before/`.

- At every width the document and every element stay inside the window, closed and opened, with no
  text under 12 pixels in the results. Every link in the results points at an element that exists.
- The first pass found one defect by eye and it was fixed before this record: in the opened ledger at
  768 the line number column was 7 percent wide, so `LINE` and `4000` broke onto two lines. Each table
  now carries only its own columns, with the line column at 76 pixels.
- A second defect found by eye, a middle dot written as a broken escape in the summary's "Show the
  checks", was fixed the same way.

No defect was found in `assets/second-pass.css` that needs its owner.

## Reproduction

```
node audit/checker-results-2026-09-13/checker-results-widths.cjs <beat-the-machine> <out.json> <screenshot dir> <sample> <label>
```
