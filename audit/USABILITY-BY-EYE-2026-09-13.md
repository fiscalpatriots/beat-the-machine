# Usability by eye, 13 September 2026

Lane U1, written at 11:06 PM EDT. The source is Khaled's report of about 10:15 PM. On `review.html`, under
"How a review runs", the four steps were "basically vertical bars, and everything is cut off" at
a desktop window about 1,025 pixels wide.

**How it was verified.** Headless Chrome 152 ran over the DevTools protocol with its own
throwaway profile, against a local static server. The drill ran in test mode, so nothing was
posted. Every screenshot named below was opened and looked at, and none was only measured.
Tall pages were read as contact sheets at 47 to 100 percent scale, with 1:1 crops wherever
something looked wrong.

Chrome repeats content in a single capture taller than 16,384 pixels. That hit the checker's
results page, which is up to 49,595 pixels tall. Any page over 12,000 pixels is therefore
captured in 3,000 pixel segments and stitched. The scripts are in `audit/usability-2026-09-13/`:

| Script | What it does |
| --- | --- |
| `sweep.cjs <root> <outdir> [widths] [states]` | Full-page shot of every page and state, with in-page checks for sideways overflow, clipped content, text under 12px and squashed images |
| `drive.cjs` | Clicks each state: the drill landing, the read screen with three lines tapped, Halyard line 1, Kestrel line 1, Brightwater line 1 with a call and a basis chosen (the explanation step), the end screen, the checker empty and after both samples are loaded and run, and the author page empty and after the Kestrel sample is read |
| `runs.cjs <root> <outdir> <label> [widths]` | The "How a review runs" section alone, with card sizes, the smallest type and the caption position |
| `viewport.cjs <root> <outdir> [width]` | Phone viewport shots, where fixed and sticky bars really sit |
| `tall.cjs`, `stitch.py`, `sheet.py`, `combine.py`, `crop.py`, `checks.js`, `shoot.cjs`, `measure.cjs` | Segment capture, stitching, contact sheets and the checks |

## 1. The four steps: why they collapsed

The live site at `b6ba468` and the local head up to `2177445^` carried the same strip markup and
CSS, so the local head had the defect too. Measured before the repair:

| Width | Card | Image box | What showed |
| --- | --- | --- | --- |
| 375 | 255 x 1,060 | 253 x 960 | a sliver of each capture |
| 768 | 272 x 1,081 | 270 x 960 | a sliver |
| 1,024 | 152 x 1,123 | 150 x 960 | "mers", "1,000", "son 2 of 1" |
| 1,280 and 1,600 | 158 x 1,102 | 156 x 960 | a sliver |

Three causes stacked:

1. **Each card was a `<figure>` with no margin rule.** It kept the browser's default margin of 16px by 40px, which took 80px out of a grid cell about 230px wide. That is why a card was 152px at 1,024.
2. **Each `<img>` kept `height="960"` (or `840`), and nothing in the CSS set `height:auto`.** The height attribute overrode `aspect-ratio:4/3`, so each image box was 150px by 960px. `object-fit:cover` then filled it from the middle of a full-size capture. That produced the vertical bars and the cut words.
3. **Even a correct 4:3 box could not have been read.** The captures were 1,280px of interface, so a 230px card would have shown it at about 18 percent, with 16px text at under 3px. Four across can never be readable here, because the page column stops at 1,048px.

Overflow checks had passed because nothing overflowed. The defect was only visible to someone looking.

## 2. The four steps: the repair (`2177445`, and the dollar signs in the commit that carries this file)

**Drawn, not cropped.** A crop that stays legible in a card 290px to 490px wide can show only about
330px to 470px of interface. That rules out step 01's two panes side by side, and step 03's
account with both calls. So each step now sits over a small drawing in live HTML text, in the
product's own words and numbers, set in the page's paper, hairline and Mason green language. The
type does not shrink with the card: labels are 12px, content 14px to 15px, and captions 17.5px
(the page's body size).

| Step | The drawing, and where its words come from | Caption |
| --- | --- | --- |
| 01 | The checker's ledger pane with Halyard accounts 4200, 5100 and 6100 ($186,000 to $121,000, $214,000 to $287,800, $96,400 to $91,200), and the memo pane with sentence 1, all as the checker's Load sample fills them | Paste the ledger and the memo beside it. |
| 02 | The coverage bar and the four counts from the checker's own run on the Halyard sample (12 sentences: 4 checked within scope, 5 need review, 0 not checked, 3 failed, read from `__secondPass().stats` at 11:03 PM), and the failed finding on sentence 1 ($6,500 against the ledger's -$65,000) | Four checks run, and the checker prints a status for every sentence it recognizes and says what it could not read. |
| 03 | The read screen's chips (4200 tapped, 5100 not), then the card for 4200 with May, June, the change in red, and Let it stand and Flag it | The committed wording from `bce4a15`, left unchanged |
| 04 | Two lines of the round two results screen as the drill printed them (5210 agrees with the key, reason does not agree; 6110 agrees on both), and Save my record | The drill scores each call and its basis separately, and the record you keep holds every call with its basis. |

Each drawing carries `role="img"` with an `aria-label` that says what it shows, which replaces the four
old alt texts. The four PNGs under `screenshots/review/strip-0*.png` are no longer loaded. They stay
on disk because `audit/performance-2026-09-13.md` lists them as history.

**Layout by width.**

| Band | What the section does |
| --- | --- |
| 320 to 699 | One column. At 320 each card is 292px wide and the ledger figures wrap under the account name. |
| 700 and up | Two by two, with the drawing and the caption rows shared across each pair (subgrid) so the two captions start on one line. Cards are 316px at 700, 350px at 768, 471px at 1,009 (1,025 with a scrollbar), 478px at 1,024 and 490px from 1,048. |
| Four across | Not used. The 1,048px column would leave each card about 230px wide. |

Nothing clips or scrolls at any width. The smallest type in the section is 12px, and the document
width equals the viewport at 320, 375, 768, 1,009, 1,024, 1,280 and 1,600 (`after/steps-after.json`).

**Before and after.**

| Width | Before | After |
| --- | --- | --- |
| 1,024 | `audit/usability-2026-09-13/before/steps-1024-before.png` | `audit/usability-2026-09-13/after/steps-1024-after.png` |
| 375 | `audit/usability-2026-09-13/before/steps-375-before.png` | `audit/usability-2026-09-13/after/steps-375-after.png` |

The pair also exists at 320, 768, 1,280 and 1,600 in the same folders, and at 1,009 in `after/`.

## 3. Everything else, by eye

`sweep-final/` holds 72 full-page shots, 12 states at 320, 375, 768, 1,024, 1,280 and 1,600, all taken after the
fixes below. `sweep-before-css/` keeps the shots that show the four shared-sheet defects before their
fix, and `viewport-before/` and `viewport-after/` hold the phone viewport pair.
`review-extra-widths/` adds `review.html` at 480, 600, 700, 740, 761 and 900, around its breakpoints.

In the final sweep no page scrolled sideways at any width, and no element clipped its text. The only live
type under 12px is item L2 below. Item L7 is a picture of type, which the checks cannot measure.

### Fixed in `review.html`

| # | Defect | Width | Fix | Evidence after |
| --- | --- | --- | --- | --- |
| R1 | The four steps, section 1 above | all | Rebuilt | `after/` |
| R2 | The hero's "Second Pass" heading ran into its box's right edge | 721 to 1,600 | Headings set at 32 instead of 36 | `sweep-final/review-1280.png` |
| R3 | The narrow hero cut off the Sign-off box's bottom edge | 320 to 760 | viewBox 563 tall | `sweep-final/review-320.png` |
| R4 | "THE CHECKER TESTS FOUR" and "A REVIEWER SIGNS TWO" at 10px | 320 to 375 | Labels 16 units, 12px at 320 | `sweep-final/review-320.png` |
| R5 | The evidence tally was a scaled drawing with lines at 10px on a phone and 11.8px on a desk | all | Set in live text at 14px and 16px | `sweep-final/review-375.png` |
| R6 | The quoted draft lines were 11.5px | all | 13px. They follow the tally inside the 640px column, so a draft line holds whole, and sit beside it only where the box is 700px or wider | `sweep-final/review-1024.png` |
| R7 | Narrow drawings grew to about 1.8 times at 600 to 720, with list items near 36px. The wide hero's small lines fell to 11.6px at 721 to 760. | 600 to 760 | Narrow drawings stop at 440px, and the hero keeps its narrow drawing, centered, up to 760 | `review-extra-widths/review-700.png`, `review-761.png` |

### Fixed in `assets/second-pass.css` (CSS only, no markup or script touched)

| # | Page | Defect | Width | Fix | Before and after |
| --- | --- | --- | --- | --- | --- |
| S1 | drill, every screen | "Second Pass" sat 6px below the header links, because `index.html` line 152 styles `.mark` with a 12px top margin, and the shared header's wordmark is `.mark` | all | `#sp-nav .mark{margin:0}` | `sweep-before-css/halyard-1024.png`, `sweep-final/halyard-1024.png` |
| S2 | drill, every screen after the codename | The codename was placed 3px above the band's foot with 16px of padding, so it sat on "Costello College of Business" and touched the gold rule | all | The band grows an 18px lane when a codename shows | `sweep-before-css/halyard-320.png`, `sweep-final/halyard-320.png` |
| S3 | checker Run button, drill call and lock buttons | Keyboard hints at 11px | 521 and up | 12px | `sweep-before-css/checker-empty-1024.png`, `sweep-final/checker-empty-1024.png` |
| S4 | drill read screen | The fixed onward bar covered the site footer's links at the end of the page. The drill pads its own column, but the footer comes after it. | 320 to 899 | `body:has(.stickygo){padding-bottom:84px}` under 900 | `viewport-before/read-bottom-375.png`, `viewport-after/read-bottom-375.png` |

S1 to S4 were rechecked on every page that loads the sheet, in `sweep-final/`.

### Listed for the owning lanes (not edited here)

| # | Owner | Page | Defect | Width | Evidence |
| --- | --- | --- | --- | --- | --- |
| L1 | F2 | `index.html`, explanation step | The "Why it matters for this period" placeholder wraps to three lines in a box sized for two, and its last word, "month", is cut. `.explain textarea{min-height:64px}` (line 288). About 100px at 480 and below would hold it. | 320 | `sweep-final/explain-320.png` |
| L2 | index owner | `index.html`, every call card | The May and June labels on the two-bar chart render at 10.8px (a scaled drawing) | 320 | `sweep-final/halyard-320.png`, `kestrel-320.png`, `explain-320.png` |
| L3 | P1 | `index.html`, end screen | "1 false flags" | all | `sweep-final/end-320.png` |
| L4 | P1 | `index.html`, read screen | From 1,280 up the column widens to 1,320px. Its band and ledger start 20px from the edge at 1,280 and 160px at 1,600, while the header wordmark sits at 136px and 296px. The screen's edges line up with neither the header nor the other drill screens. | 1,280 to 1,600 | `sweep-final/read-1280.png`, `read-1600.png` |
| L5 | P1 | `index.html`, read screen | The sticky track bar (91px) and the fixed onward bar (72px) take 163px of a 740px phone screen, 22 percent of it, while the ledger is being read | 375 | `viewport-after/read-mid-375.png` |
| L6 | index owner | `index.html`, masthead | `placeCodename()` clamps the codename 6px from the band's edge, while the band's text sits at the 14px to 20px gutter, so on line 1 the name starts left of the words above it | all | `sweep-final/halyard-375.png` |
| L7 | F1 | `checker.html` | The "See it on a real case" figure, `screenshots/checker/hero-results.png`, is a 1,280px capture shown at 258px (320), 694px (768) and 950px (1,024). Its 14px text renders near 3px, 8px and 10px, so it cannot be read below a desk width. It is also stale: it prints "13 In the reviewer queue" and run `run-1-cu9t7t`, and the same Halyard run now prints 16. This is the class of defect Khaled reported on the review page. | 320 to 1,024 | `sweep-final/checker-empty-320.png`, `checker-empty-768.png` |
| L8 | F1 | `checker.html`, results | Every check repeats the whole memo sentence. On a phone each check is a stacked card, so sentence 1 (32 words) prints eight times. The results page is 49,595px tall at 320, 45,830 at 375 and 23,759 at 1,024. | all, worst on phones | `sweep-final/checker-run-320.png`, `checker-run-1024.png` |
| L9 | F2 | `author.html`, after a read | The prefilled "Why, the line the reveal prints" and "On file, one fact per line" boxes hold more than their height, so the text stops mid-sentence and must be scrolled inside the box. Line 5 ends at "prior balance on 6200", and line 7 at "Silence on a line that owes". | all | `sweep-final/author-read-320.png`, `author-read-1024.png` |
| L10 | F2 | `author.html` | The Period placeholder "July close, prepared from the general ledger" is cut off in its input | all | `sweep-final/author-empty-1024.png` |
| L11 | F2 | `author.html` | In the four-column case grid, "Owes commentary" wraps onto two lines, and that control stands taller than Both legs beside it | 768 to 1,600 | `sweep-final/author-empty-1024.png` |

No defect was found on `404.html` at any width, on the drill landing screen, or on `review.html`
after the repairs at any of the 12 widths checked.

## 4. Commits, local, not pushed

| Hash | Line |
| --- | --- |
| `2177445` | The four steps on the review page read at every width, drawn in the product's own words instead of cropped screenshots |
| the commit that carries this file | The shared sheet fixes four defects found by eye, the ledger drawing shows its dollar signs, and the usability record |
