# Release QA, 13 September 2026

Second Pass 1.6.0. Every page walked at six widths, both independent reviews taken item by
item, and the whole release read for consistency.

**How it was driven.** Headless Chrome over the DevTools protocol against a local server on the
working tree, one real click per control rather than a function call, with the drill in test mode
(`?test=1`) the whole way, so no run reached the live form. The harness records, at every screen:
the document and every element whose content is wider than its box, every element whose box
crosses the viewport edge, console errors, and failed requests. An element inside an
`overflow:hidden` or `clip` ancestor is not counted, because its overflow cannot scroll anything.

**What is not mine.** `Second-Pass-Excel-Template.xlsx`, `EXCEL-TEMPLATE.md`,
`build_excel_template.py`, `FACILITATOR-*.md`, `Second-Pass-Facilitator-Guide.*`,
`build-facilitator-pdf.py`, `READOUT-TEMPLATE.md` and `Second-Pass-Results-Readout.docx` belong to
the materials lane. Findings that land in those files are listed under **Still open** and left for
that lane.

---

## 1. The three fixes

### 1.1 The checker overflowed 14px inside `#out` at 320

Reproduced: at 320 with the Halyard sample run, `#out` measured `clientWidth` 292 and
`scrollWidth` 306. The element pushing it was `.actionbar`, the sticky bar under the results,
which was laid out full bleed on `margin: … calc(var(--gut) * -1)` and so ran from x=0 to x=320
while `#out` ran from 14 to 306.

The bar's background is the page background, so the only thing that bleed ever showed was where
its hairline started and stopped. It now sits inside the page gutter like every other rule on the
page. Re-measured at 320 after a run: `#out` 292 wide with 292 of content, and every scrollable
ancestor up to `<html>` is clean on all four samples.

Evidence: `assets/second-pass.css`, commit `49f433c`. Screens
`screenshots/release/checker-375-03-results-*.png`.

### 1.2 The rank ladder read absolute points, so a perfect Kestrel run stopped at Manager

Reproduced: Kestrel is twelve lines and can give 2,200 points; Manager sat at 2,000 and Partner at
2,500, so a run that agreed with the key on every line and every basis could not reach the top.

The ladder is now a share of what the case in front of the player can give. At load the page
computes two numbers from the case itself:

- **the maximum attainable**, from the right call, the right basis, every streak step from the
  third correct call onward, and every cover-story bonus;
- **the blanket-call ceiling**, the most a player can score by calling every line the same way
  without reading one of them, taking the better of flag-everything and stand-everything and
  granting that player the basis points too.

Staff, Senior, Manager and Partner start at 34, 57, 76 and 95 percent of the maximum, and the
Senior line is additionally held above the blanket ceiling. Verified by driving each case in the
page and reading `window.__BTM_POINTS`:

| Case | Lines | Max | Blanket ceiling | Ladder | Perfect | Flag every line | Stand every line | Every call wrong |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `halyard-v4` | 14 | 2,625 | 1,450 | 0 / 893 / 1,496 / 1,995 / 2,494 | 2,625 **Partner** | 1,450 **Staff** | 925 **Staff** | 0 Trainee |
| `kestrel-v1` | 12 | 2,200 | 1,200 | 0 / 748 / 1,254 / 1,672 / 2,090 | 2,200 **Partner** | 1,200 **Staff** | 750 **Staff** | 0 Trainee |
| An own case written in `author.html` | 7 | 1,175 | 600 | 0 / 400 / 670 / 893 / 1,116 | 1,175 **Partner** | 450 **Staff** | 600 **Staff** | 0 Trainee |

The attempt record now exports `maxAttainable`, `blanketCallCeiling` and a `ladderBasis` sentence
beside the ladder, so a rank in an export can be read without the page.

Evidence: `index.html`, commit `9d1813f`.

### 1.3 `assets/nav.js` carries Author as a fourth link

Added, marked current on `author.html` by the same filename match the other three use, and the two
narrow breakpoints were retuned to pull the gaps in rather than wrap the row. Measured on all five
pages at 320, 340, 360, 375, 390, 414, 768 and 1280: one row at every width, no row scroll, and at
320 the mark plus the four links occupy 263px inside a 292px content box.

Evidence: `assets/nav.js`, commit `b37e844`. `sitemap.xml` gained `author.html` in the same commit.

---

## 2. A. The walk

38 screens, each measured at 320, 375, 390, 768, 1280 and 1600, which is 228 measured states.
Screenshots at 375 and 1280 into `screenshots/release/`, 76 files.

| Surface | Screens walked |
| --- | --- |
| Drill | intro, the practitioner note, the data notice, codename and chips, orientation and the ledger pre-picks, a card, a first call, a changed call before locking, a right reveal, Back to the line before, a wrong reveal, a level-up, the fresh-case bridge, a fresh card, the fresh results, the end screen, Save my record, Send my results in test mode, Play again |
| Checker | empty, the parse preview, results on Halyard, Brightwater, Kestrel and Ridgeline, the reviewer queue answered, Copy table, Download CSV, Print summary, both prompts open |
| Author | empty, the Kestrel paste, Read it, every card keyed, Save the case, the saved case previewed in the drill |
| Review, 404 | the whole page |

The case control on the intro was read at every width and offers Halyard and Kestrel, with
**My own case** appearing only once `author.html` has written one into that browser.

**Result: no page or ancestor horizontal scroll at any width, no console errors, no failed
requests, on any of the 228 states.**

Interactions confirmed rather than assumed:

- Changing a call before locking replaces the selection and the first call is kept separately.
- Back returns to the previous line and the run rescoring is recomputed, not decremented.
- The level-up fires on the crossing, Trainee to Staff, at every width.
- Save my record writes `second-pass-att-…json` and names the file on screen.
- Send my results in test mode posts nothing: the would-be payload is written to the local record
  and the record is stamped `testAttempt: true`. Verified by reading `window.__BTM_LAST_POST`
  after the click at all six widths.
- Play again returns to the codename screen with a new attempt identifier.
- The checker's Copy table falls back to "Select it and copy by hand" where the clipboard is not
  granted, rather than failing silently.
- Print summary builds a 105-row printable sheet and calls `print()`.

**Keyboard and focus.** Driven with real Tab key events, not programmatic focus, on all five
pages. The first Tab lands on the skip link, which is visible on focus and moves the caret into
the main region. Every control reached carries a visible ring and an accessible name: 0 without a
ring and 0 without a name across index, checker, review, author and 404. In the drill, `2` selects
Flag on a card and Enter locks the line in.

**Reduced motion.** With `prefers-reduced-motion: reduce` emulated, the checker, review and author
pages animate nothing. The drill keeps one 200ms opacity fade on the reveal face, which is the
authored substitute for the 3D card turn: no transform, no movement, and the rank flash, the
trophy, the medals and the call transitions are all off.

### Defects found during the walk and fixed

| # | Defect | Where | Fix | Commit |
| --- | --- | --- | --- | --- |
| 1 | The three money columns on a card needed 278px inside a 250px card at 320 and leaked 12px past it | `index.html`, `.stripnums` | the figures step down to the body size below 360 and the gap closes | `9d1813f` |
| 2 | The saved record box was `white-space:pre` and put 5,571px of sideways scroll inside a phone card | `index.html`, `.recordbox`; `assets/second-pass.css`, `textarea.code` | `pre-wrap` with `overflow-wrap:anywhere`, which keeps the JSON indentation and wraps the long line | `9d1813f`, `49f433c` |
| 3 | Every text input, textarea and select had `outline:none` on focus and only a darker border to replace it, and `input:focus` outranked the shared `:focus-visible` ring, so a keyboard had no indicator on any form field on any page | `assets/second-pass.css` | the ring is restored for `:focus-visible` and stays off for a pointer | `49f433c` |

---

## 3. B. Regression

| Check | Result |
| --- | --- |
| `node tests/run-checker-tests.cjs` | **53 passed, 0 failed, 53 run** |
| Open Graph and Twitter tags | complete on all five pages: `og:title`, `og:description`, `og:image`, `og:url`, `og:type`, `twitter:card` and `description`. Every `og:url` is the live URL for that page and every canonical points at its own page |
| Favicon | `assets/favicon.svg` and `assets/favicon-32.png` linked in the head of all five pages, and both are byte-identical to the files served live |
| `robots.txt` | `User-agent: *`, `Allow: /`, and the sitemap line. Nothing disallowed |
| `sitemap.xml` | five entries, and `author.html` was added. Every listed URL resolves to a file in the tree |
| 404 | the live host returns status 404 and serves the custom page |
| Links | 56 local links across the five pages and `assets/nav.js` all resolve. The only external hosts referenced are `fonts.googleapis.com`, `fonts.gstatic.com`, `github.com/fiscalpatriots/second-pass`, `github.com/fiscalpatriots/beat-the-machine` and the site's own canonical URLs |
| Local against live | before this release: `checker.html`, `author.html`, `404.html`, `robots.txt`, all three case files, the favicon in both formats and the share image were byte-identical to the live copies after line-ending normalization. `index.html`, `review.html`, `assets/nav.js`, `assets/second-pass.css` and `sitemap.xml` differed by exactly this release's edits |

The two sample fixtures were updated rather than repaired. `T18` is the same set of assertions
against `halyard-v4`, whose ledger, memo and keys are the `halyard-v3` ones. `T18b` is a new set,
because `brightwater-v4` is a different memo with a different key on three of its five lines; the
new assertions are set out in section 5.

---

## 4. C. The two reviews, item by item

Two documents, read line by line. **Done** means I ran it or read it in the file today.
**Partial** means part of it holds and the rest is named. **Open** means it does not hold.
**N/A** means it names a surface outside this repository.

### 4.1 `Second-Pass-Claude-Build-Handoff.md`

#### First release requirements

| # | Requirement | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Repair cases 2, 4, 8, 12, 13 and fresh 5 | Done | `cases/halyard-v4.json`, `cases/brightwater-v4.json`, both with a `changeLog` naming the review and the change |
| 2 | Prevent false mechanical clearance and require visible resolution | Done | the 16 live probes in section 4.2 below; `tests/run-checker-tests.cjs` 53/53 |
| 3 | Remove legacy placeholder participant data; separate decisions, actual reasons and computed metadata | Done | `index.html` `attemptRecord()`: `confidence: null` with `confidenceNote: "not asked in this version"`; the basis chips and the free line are the player's, the key and the verdict are the page's, in separate fields |
| 4 | Reuse commitment and response handling, with a ledger-only judgment before the narrative | Done | the orientation screen collects up to three ledger-only picks before a memo sentence is read, and posts them as `Prepicks: …` |
| 5 | Replace the fresh assessment with one testing supported and unsupported causes, revealing nothing until completion | Partial | `brightwater-v4` replaced the empty-memo item with a numerically correct causal claim and keys four of five on evidence. Nothing is revealed until all five are committed, verified on the walk. The remaining gap is scoring: see 4.2 §3 |
| 6 | Participant record, case packet and facilitator guide usable without the author | Partial | the record and the case packet are; the guide is the materials lane's and still names a version and figures listed under **Still open** |
| 7 | Demonstrate the configured model workflow with preserved inputs, raw outputs and human adjudication | Done | `evidence/` carries six raw drafts across three ledgers, blind and under Prompt 1, with the checker results and a note; `PROVENANCE.md` states plainly that the case's own fourteen challenges were authored, not generated |

#### The nineteen accounting repairs

All nineteen recomputed from the case ledgers today, independently of the reveal copy:

| Line | Movement | Percent | Key |
| --- | --- | --- | --- |
| H1 4200 | -$65,000 | 34.9 | flag |
| H2 6200 | +$77,600 | 189.3 | flag |
| H3 5100 | +$73,800 | 34.5 | flag |
| H4 4100 | +$229,000 | 28.2 | stand |
| H5 6500 | -$7,500 | 13.6 | stand |
| H6 7400 | +$2,500 | 39.1 | stand |
| H7 4000 | +$372,000 | 7.1 | flag |
| H8 6400 | +$47,000 | 313.3 | flag |
| H9 6100 | -$5,200 | 5.4 | stand |
| H10 6300 | +$1,600 | 5.6 | stand |
| H11 6000 | +$72,500 | 11.5 | flag |
| H12 4000 | +$372,000 | 7.1 | flag |
| H13 5000 | +$348,000 | 8.9 | stand |
| H14 7100 | +$31,200 | 51.0 | flag |
| F1 5210 | +$52,700 | 38.1 | flag |
| F2 6110 | +$54,900 | 25.7 | stand |
| F3 4220 | +$42,400 | 44.2 | flag |
| F4 4010 | +$61,500 | 8.3 | flag |
| F5 6610 | +$5,700 | 31.0 | stand |

Every figure agrees with the review's own table. The product margin ties as well: gross profit
$1,310,000 to $1,334,000, margin 25.0 percent to 23.7705 percent, and the memo states 23.8. The
required-commentary accounts are 4100, 4200, 5100, 6000, 6200, 6400 and 7100 on Halyard and 4220,
5210 and 6110 on Brightwater, which is what the ledgers give under the magnitude rule.

The three copy repairs the handoff asked for by name are in `halyard-v4`'s change log and in the
reveal text: card 4 no longer says billing in arrears decides when revenue is earned, card 14's
on-file facts no longer supply the 3 June draw date and then deny it, and card 13 carries a
`stillOpen` line saying the stand is provisional and the bridge request is not closed. **Done.**

#### Shared case consistency

| Item | Status | Evidence |
| --- | --- | --- |
| The checker's sample memo is a different version from the game's | **Fixed today** | `build-checker-cases.cjs` pointed at `halyard-v3` and `brightwater-v2`; it now reads `halyard-v4` and `brightwater-v4`, and the block in `checker.html` was regenerated. Commit `52ac4f2` |
| Do not port clean verdicts from the game to the checker sample | Done | `CHECKER.md`: "The checker supplies none of the case's On file facts. A clean verdict in the game does not transfer to the checker" |
| Check company-wide consistency before releasing a packet | Done | section 6 below |

#### The checker fixtures, T01 to T17

All seventeen are in `tests/checker-fixtures.json` and pass. The suite has grown to 53 and now also
carries N01 to N24 and the boundary cases. Status **Done**, evidenced by
`node tests/run-checker-tests.cjs`: 53 passed, 0 failed.

#### Export and prompt repairs

| Item | Status | Evidence |
| --- | --- | --- |
| `csv()` put `r.label` in the sentence column | Done | the CSV header is `run id, run timestamp, close period, reviewed memo version, source version, evidence id, sentence id, sentence text, line, account, check, status, finding, proposed conclusion, human conclusion, unresolved issue, action owner, review time` |
| Escape spreadsheet formula-like text | Done | probed today: an account named `=1+1` exports as `"'=1+1"`, and no cell begins `=`, `+`, `-` or `@` |
| Include evidence ids, source version, proposed and human conclusion, unresolved issue, owner, review time | Done | all seven are columns above |
| A changed input invalidates the prior review status | Done | the input handlers call `invalidate()` on every threshold and column control |
| `reviewerPrompt()` claimed every figure was checked and told the reviewer not to recompute | Done | the prompt now opens "Reviewer questions, and the mechanical work that was NOT done", prints the four coverage counts, defines "checked within scope" narrowly, and lists unresolved items verbatim. No instruction not to recompute |
| A proposed evidence request is not a verified citation | Done | requested evidence is a separate column from the finding |
| Remove the universal no-network and guaranteed-deletion copy | Done | the page says "Everything you paste is processed by the script in your own browser. This page is served from GitHub Pages and loads one Google font; anything you copy into another AI service goes to that service under its terms" |

#### Local trainer reuse and repairs

The four reproduced issues, the provider routing and the session export all name
`github.com/fiscalpatriots/second-pass`, a different repository. **N/A here**, and the reviewer
page now links that repository so a reader can reach it.

#### Learning and data implementation, and the minimum attempt record

| Item | Status | Evidence |
| --- | --- | --- |
| A ledger-only judgment recorded before the narrative | Done | the pre-picks, posted in the round one question |
| Actual reasons recorded for causal decisions | Done | a basis chip set plus an optional free line per card, on stands as well as flags |
| Separate practice and assessment modes, with no correctness signal between items | Done | `CASE2.mode === "assessment"`; the track, the score, the streak and the rank meter all go quiet through round two, verified on the walk |
| Three-dimension reasoning rubric | Partial | the record carries `humanRubricScores`, `scorerId`, `outOfKeyFinding` and `adjudication` as nulls for a person to fill, and says so in `rubricNote`. The page does not score reasoning, and does not claim to |
| The minimum attempt record | Done | the record carries the attempt id, pseudonym, consent and notice version, product and case versions, form, practice or assessment, first attempt, assistance source, start and completion, submission state and test flag; per item the original and final decision, the actual reason, evidence references, elapsed seconds, skip reason and reveal time; and the scoring block with key versions and the null adjudication fields |
| No fabricated demographic or confidence values | Done | `confidence: null` with a note, in place of the fixed 3, 5, 5 and "Once or twice" |

#### Submission and participant usability

| Item | Status | Evidence |
| --- | --- | --- |
| Completion not gated on consenting to share | Done | Save my record and Send my results are two separate buttons on the end screen; the record saves with nothing sent |
| A truthful external practitioner route | Done | "Outside Mason" is in the organization chips, and the source says why |
| A concise data notice before collection | Done | the notice screen, stamped `notice-2026-09-13`, before the codename step |
| A codename is pseudonymity, not anonymity | Done | said in those words on the notice screen |
| The hidden-frame load does not prove storage | Done | after a send the page says "Sent. The receiver does not confirm receipt to this page" |
| Retries reuse the attempt identifier | Done | one identifier per run, reused by every retry; `findings.py` now dedupes on it |
| Test mode prevents any external submission and is excluded | Done | walked at all six widths: nothing posted, and the record carries `testAttempt: true` and `exclusionReason: "test attempt"` |
| Widths 320, 375, 390 and 768, keyboard, focus, labels, long reasons, reduced motion | Done | section 2, plus 1280 and 1600 |
| Correct score language and no seniority claim | Done | the end screen says "Trainee through Partner are ranks in this drill. They say nothing about professional seniority" |

#### Completion evidence for Claude, the eight items

| # | Item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Revised case packet and answer rationale | Done | `cases/*.json` change logs, `cases/README.md` |
| 2 | Regression output for the documented failures | Done | 53/53 today |
| 3 | Full browser walkthrough with collection disabled, plus a verified receipt path | Partial | the walkthrough is section 2 and is complete with collection disabled. There is no separately verified receipt in a test destination: the page labels a send as unconfirmed instead. **Open** |
| 4 | Consistent case, prompt and product identifiers on every surface | Done today | section 6 |
| 5 | Participant export with actual reasoning and no fabricated values | Done | above |
| 6 | Independent assessment with causal coverage and no interim leakage | Partial | no leakage, and four of five items are causal; the scoring gap is 4.2 §3 |
| 7 | A preserved model workflow with the key withheld and human adjudication | Done | `evidence/` |
| 8 | Real user observations, changes and a retest record | **Open** | no participant has run it. Nothing in the release claims otherwise |

### 4.2 `Second-Pass-Live-Release-Review-2026-09-13.docx`

#### §1 Are the nineteen keys defensible

| Item | Status | Evidence |
| --- | --- | --- |
| Halyard 4, the billing-in-arrears clause | Done | reveal rewritten to the service dates and the earned revenue bridge; change log entry |
| Halyard 14, a draw date supplied and then denied | Done | the on-file fact reads "Other draw and repayment dates, daily balances, rates and fees were not supplied" |
| Halyard 13, stand must not mean the cause is verified | Done | the reveal, the over-flag note and a new `stillOpen` line all say the stand is provisional |
| Halyard 2, flagging a contradiction is not knowing the accrual | Done | the reveal asks what June work was performed, how much is recorded and whether it is a repair or an improvement, and stops there |

#### §2 Does the checker close the false assurance class

Re-run today against the release build, on the review's own two-row ledger (rent 100,000 to
130,000; insurance 50,000 to 95,000) with the review's thresholds:

| Probe | Sentence | Review saw | Now |
| --- | --- | --- | --- |
| N09 | Rent rose $45,000 and Insurance rose $30,000 | checked within scope | **failed**, both figures failed, 2 queue items |
| N07 | Rent rose $30,000 and increased by -30000 | checked within scope | **failed**, the signed figure failed |
| N22 | Rent expense changed 30% | checked within scope with the role unknown | **needs review**, the percent is reported role unknown |
| N01 | Rent expense did not increase by $30,000 | checked within scope | **needs review**, 4 queue items |
| N02 | Rent rose $30,000, a change of ninety percent | checked within scope | **not checked** |
| X1 | …and increased by 800 | silently dropped | **not checked** |
| X2 | …and increased by 1999 | dropped as a year | **not checked** |
| X3 | …and increased by 6200, with 6200 in the ledger | read as an account reference | **not checked** |
| X4 | increased by £30,000 | cleared as dollars | **not checked**, no figure read |
| C1 | Rent $30,000 and Insurance $45,000, both true | passed | **checked within scope**, queue empty |
| C2 | Rent rose $30,000, or 90% | failed | **failed** |
| C3 | Insurance fell $45,000 | failed | **failed** |

Mutation properties, which the review named as the acceptance criteria rather than the five
examples: swapping the amount (`M2`) fails, changing the sign (`M3`) fails, and the base sentence
(`M1`) still clears. **Status: the class is closed for every form the review demonstrated.**

One residue, found today and **open**: a spelled-out quantity with no unit word still clears.
`Rent expense rose $30,000, a rise of thirty thousand.` and
`Rent expense rose $30,000, one third of the prior balance.` both come back checked within scope,
and the second is false. The same sentence with a unit word is caught:
`…a rise of thirty thousand dollars.` and `…a change of ninety percent.` both come back not
checked. A fix has a trap in it: the Brightwater memo says "the thirty-one new orthodontic plans",
which is a count, not a figure about the account, so a naive number-word detector would make a
good sentence unresolved. Recorded as a fixture to write, not a change to make at release.

The four defect locations the review named were repaired before this QA: the figure reader keeps
the span and the sign, sentence binding holds a multi-account sentence unless each figure binds
within its own clause, and an unknown role stops a checked conclusion before any value comparison.

#### §3 Is the fresh case a valid causal judgment test

| Item | Status | Evidence |
| --- | --- | --- |
| The empty orthodontic memo tested omission, not cause | Done | `brightwater-v4` line 3 carries a numerically correct causal claim; four of the five now turn on evidence |
| "A threshold-only participant scores no better than chance" was false | Done | the claim is gone from the source description, and the v4 change log says the split was rebalanced so no degenerate strategy scores |
| Two items called accounts that "clear neither" | Done | the description now says patient revenue clears the dollar condition and marketing clears the percentage condition |
| Scoring did not test the chosen reason: 14 of 14 with "wrong account" everywhere | Done | every card carries a `basisKey`, the reason is scored separately from the call, and the run that motivated this scores 0 of 14 on reason. The reveal prints "Reason agrees" or "Reason does not agree" per line |
| Require a reason on stands as well as flags | Done | `basisChips.stand` offers the hold chip and the six defect chips, and a stand is scored the same way |
| Short source excerpts, and one document that is incomplete or wrong-period | **Open** | the fresh case still gives author-summarized facts |
| An educator reviews the keys and independently scores a subset | **Open** | not run |
| A rubric from zero to two, scored by a person | Partial | the record carries the fields and names the rubric; nobody has scored one |
| Do not call the result a learning gain | Done | the end screen and `README.md` both say the fresh five are a second unseen set, not a post-test |

#### §4 What the participant record can support

| Proposed interpretation | Status | Evidence |
| --- | --- | --- |
| Catch rate and false flags | Done | reported as answer-key agreement with its denominators; `tools/findings.py` prints the counts and the denominators, never a bare rate |
| Better causal reasoning | Done | the reason score is separate, and `rubricNote` says the three-dimension rubric is scored by a person outside the page |
| Confidence calibration | Done | `confidence: null`, `confidenceNote: "not asked in this version"` |
| Evidence the participant used | **Open** | `evidenceReferences` still copies the card's whole supplied file list under that name. The review asked it be renamed "evidence supplied" and participant-selected evidence collected separately |
| Unique first-time participants | Partial | `firstAttempt` is still the tab-session run counter; the attempt identifier now makes a retry countable once, which is the half of the problem the page can solve |
| Active review time | **Open** | `elapsedActiveSeconds` still measures elapsed time without pausing for tab inactivity |
| Student versus practitioner | Partial | `role` is null and stays null; the organization chips now include an honest external route |
| Learning gains | Done | not claimed anywhere |

#### §5 How the reviewer page reads to a practitioner

| Item | Status | Evidence |
| --- | --- | --- |
| The score screenshot said "12 of your fourteen calls match the ledger" | Done | that wording is gone; the page says a run can agree with the answer key and give a basis that does not |
| "Nothing is released until all four are done" describes a procedure the page does not enforce | **Open** | the caption still reads that way |
| "Two of the six cannot be settled by a machine" is a universal claim | **Open** | still on the page. The review's smallest repair is to say this checker leaves those judgments to a reviewer |
| "Wrong account" sits among the machine checks in the diagram | **Open** | still there, and it now disagrees with the v4 key, which classifies cards 12 and 14 as unsupported attribution and unsupported driver. Re-cutting the four-and-two split changes copy on three surfaces and is a content decision, not a QA fix |
| A three-person roles assumption | Done | the diagram says "a named reviewer, never the preparer", which is two roles rather than three |
| The page should reach the whole entry | **Fixed today** | the rail gained Build and code: the author page, the code repository, and this site's source. Commit `ee9a1a7` |

#### The supporting files

| Item | Status | Evidence |
| --- | --- | --- |
| Protocol step 3 told the reviewer to read only what passed | Done | `PROTOCOL.md` step 3 now reads "Work the reviewer queue, which holds what the checks could not settle: failures, …" |
| The example evidence log signed off on an invented $5,000 provision | Done | `EVIDENCE-LOG-TEMPLATE.csv` now resolves the arithmetic and leaves the cause open pending a reserve rollforward |
| The facilitator guide restores the accrual error and prints unattributed percentages | **Open** | the materials lane's file |
| The guide tells the reader to run `findings.py`, which was not in the repository | **Fixed today** | `tools/findings.py`, `tools/make-sample-csv.py` and `tools/findings-sample.csv`, proved on the sample. Commit `b8a7bd7` |
| The governance note opened "CHECKER.md does not exist in this repository yet" | Done | that line is gone |
| The case instructions described obsolete checker differences | Done | that passage is gone, and the checker now runs the same case versions |

#### §6 The five weaknesses

| Rank | Weakness | Status |
| --- | --- | --- |
| 1 | False mechanical clearance | Done for every demonstrated form; one narrow residue named above |
| 2 | No demonstrated practitioner benefit | **Open**, no practitioner has been observed |
| 3 | Perfect scores without defensible reasons | Partial: the reason is scored and reported separately; no educator review and no human rubric scoring yet |
| 4 | Contradictory operating materials | Mostly closed today; the facilitator guide and the workbook are the materials lane's |
| 5 | Claims outrun the demonstration | Partial: the claims on the pages are bounded. The write-up and script word counts are not this repository |

### Checklist totals

| Status | Count |
| --- | --- |
| Done | 66 |
| Partial | 11 |
| Open | 12 |
| N/A | 1 |

**The twelve open items, named:** a receipt verified in a test destination; real user observations
and a retest record; short source excerpts and a wrong-period document in the fresh case; an
educator's independent review of the keys; a unit-less spelled-out quantity still clearing the
checker; `evidenceReferences` naming the whole supplied list rather than what the participant used;
`elapsedActiveSeconds` not pausing for tab inactivity; "Nothing is released until all four are
done" on the reviewer page; "Two of the six cannot be settled by a machine" on the reviewer page;
"wrong account" among the machine checks in the reviewer page diagram; the facilitator guide's
accrual wording and its unattributed percentages; and an observed practitioner.

---

## 5. The two sample fixtures

`T18b` was rewritten rather than repaired, because the case under it changed.

`brightwater-v4` is the sample where the checker clears everything and settles nothing. Every
figure ties and every direction word agrees with the sign, so five of five come back checked
within scope with an empty queue, and four of the five sentences still need a person, because each
names a cause the ledger has no opinion about. The new assertions are: the version stamp, five
rows and five sentences with none skipped, all five checked within scope, the threshold claims on
lines 4 and 5 verified, and zero failed, zero needing review, zero silent and an empty mechanical
queue. `CHECKER.md`'s Brightwater section was rewritten to match, and it now carries the warning
not to read an empty queue as a clean memo.

---

## 6. D. The consistency sweep

One pass over all five pages and every document in the release.

| Check | Found | Done |
| --- | --- | --- |
| Product version | `review.html` carried `second-pass-drill 1.4.0` | bumped with `index.html` to 1.6.0. `FACILITATOR-GUIDE.md` still says 1.4.0 and is the materials lane's |
| Case versions | `build-checker-cases.cjs`, `checker.html` and `CHECKER.md` all named `halyard-v3` and `brightwater-v2` | repointed, regenerated and rewritten. The remaining mentions are in `README.md` and `cases/README.md`, where they correctly describe retired files |
| Protocol version | the checker's printed sheet cited `Protocol version 1.0` while `PROTOCOL.md` reads **Version 1.1, effective 13 September 2026** | the sheet now cites 1.1, which is the document it points at. One displayed string in the release, and it agrees |
| Split counts | Halyard 8 and 6, Kestrel 7 and 5, Brightwater 3 and 2 | counted from the JSON and agreed everywhere they are stated |
| Reason-score wording | 31 statements across seven files | all say the same thing: a reason counts as right when at least one chip was tapped and every chip tapped is in the card's basis key, scored apart from the call, and it does not move the rank |
| Employer names | none | grep over every page and document: 0 hits |
| American spelling | `licence`/`licences` in the Kestrel case and both samples that quote it; `colour`, `recognise`, `behaviour` in the prose | changed in `cases/kestrel-v1.json`, `checker.html`, `author.html`, `README.md`, `CHECKER.md` and `cases/README.md`. `FACILITATOR-GUIDE.md` keeps two and is the materials lane's |
| Em dashes | 8 in the copy the checker generates, 5 `&mdash;` entities in the sample names and one review quote, one in `robots.txt` | all removed. The one left is the input normalizer that folds a pasted en dash, em dash or minus sign into a hyphen, which is code reading a paste |
| Exclamation marks | none in copy | the only match in the release is a sentence-splitter character class |
| "Cover story" in the intro | none | 0 occurrences before the case data in `index.html`. It survives only as the badge name on the points row, which is the use that was accepted |
| Month labels | May, June and July 2026 throughout | Halyard and Brightwater are May against June, Kestrel and Ridgeline are June against July, consistently on every surface |
| Every link resolves | 56 local links | all resolve; four external hosts, all expected |

---

## 7. Evidence

| What | Where |
| --- | --- |
| Screens at 375 and 1280 | `screenshots/release/`, 76 files |
| The regression suite | `node tests/run-checker-tests.cjs`, 53 passed |
| The analysis script and its proof | `tools/findings.py`, `tools/make-sample-csv.py`, `tools/findings-sample.csv` |
| Commits | `9d1813f` the ladder and two 320 repairs, `b37e844` the Author link and the sitemap, `49f433c` the action bar and the focus ring, `52ac4f2` the checker samples on v4, `ee9a1a7` versions, spelling and the reviewer page's links, `b8a7bd7` `tools/` |
