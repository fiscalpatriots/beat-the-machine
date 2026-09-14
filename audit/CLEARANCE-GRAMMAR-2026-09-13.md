# The clearance grammar, 13 September 2026

Lane F1, written at 11:10 PM EDT on 13 September 2026. The inputs in every run are synthetic and none
of them is participant evidence. Nothing was posted or pushed.

**Heads tested.** Code behavior was run on `git archive` snapshots of the committed heads, with the
independent audit's own runners copied from `audit/independent-2026-09-13/runners/`, unchanged.

| Repository | Commit |
| --- | --- |
| beat-the-machine | `4f89ee1`, the checker, the shared reader and the fixtures |
| second-pass | `216bd2b`, the Python checker, the fixtures and the parity tests |

## What changed

The independent audit found 48 of its 175 new probes checked within scope, each one step to the side
of a class the previous repair had closed by listing words. The third review had asked for the
opposite: accounted-for financial assertions under a defined grammar, and ambiguous quantitative
language left unresolved. The checker now works that way round.

- **A sentence clears only when nothing risky is left once its claims are read.** The reader takes
  out the binding, every figure, every unparsed or outside span, the tested direction and no-change
  words, the movement nouns and the ledger's own month-over-month frame. Whatever is left is read
  against a risk lexicon, and a word from it holds a sentence that would otherwise clear at **needs
  review**, named in a `Wording` row and an **Unread wording** queue item. The grammar, the lexicon
  and the refused examples are in `CHECKER.md` under **The clearance grammar**.
- **Two structural rules.** An account named with no figure or tested direction word in its own
  clause holds the sentence, and on a ledger whose columns name no month, two months that are not
  neighbours hold it.
- **The figure reader.** `$-30,000`, `+$60,000`, `$+60,000`, `+60,000`, `+25 percent`, a trailing
  minus and a dash read as a minus are the figure's own sign, compared as written. A debit or credit
  marker beside a figure, a currency name or a qualified dollar beside a figure, a CJK numeral, and a
  unit word with no figure in front of it are unparsed spans. `respectively` no longer binds a figure
  by its clause. Every ledger line carries its two column labels, so a month or year they contradict
  holds the sentence.

## The audit's 175 probes, before and after

Before is the audit's own graded output at `71d457b` and `fe8cd49`. After is the same runner on the
heads above. A false clearance is checked within scope where the audit requires otherwise. Both
implementations return the same status on every probe, before and after.

| Audit class | Probes | False clearances before | After | Other misses before | After |
| --- | --- | --- | --- | --- | --- |
| multiplier | 15 | 0 | 0 | 0 | 0 |
| no change | 29 | 11 | **0** | 0 | 0 |
| approximation | 11 | 0 | 0 | 0 | 0 |
| range | 6 | 0 | 0 | 0 | 0 |
| scale | 13 | 0 | 0 | 0 | 0 |
| sign | 19 | 9 | **0** | 0 | 0 |
| units | 8 | 0 | 0 | 0 | 0 |
| period | 13 | 12 | **0** | 0 | 0 |
| two accounts | 9 | 2 | **0** | 1 | **0** |
| negation | 10 | 1 | **0** | 0 | 0 |
| currency | 19 | 9 | **0** | 0 | 0 |
| digits | 6 | 3 | **0** | 0 | 0 |
| typing | 13 | 1 | **0** | 0 | 0 |
| long memo | 4 | 0 | 0 | 0 | 0 |
| **Total** | **175** | **48** | **0** | **1** | **0** |

By the audit's defect numbers, after:

| Defect | Probes | Status now, in both |
| --- | --- | --- |
| D1, currency words | 9 | not checked, 9 |
| D2, sign forms | 10 | failed, 7 (`$-30,000`, `30,000-`, a dash, and the four plus forms on a line that fell); not checked, 3 (`CR`, `Cr.`, `credit`) |
| D3, no-change words outside the list | 11 | needs review, 11 |
| D4, period mismatch | 12 | needs review, 12 |
| D5, unread quantities (`三十`, `trente pour cent`, `XXX percent`) | 3 | not checked, 3 |
| D10, a claim about another account, and `hardly moved` | 3 | needs review, 3 |
| D11, `respectively` on a true sentence | 1 | needs review, never failed |

**D6, the author page.** The audit's four-sentence memo now reads on `author.html`: sentence 1 not
checked, sentence 2 failed with `flag` suggested, sentences 3 and 4 needs review with no call
suggested and the held word named under What the checks found. No stand key and no clean line.

## Everything else that had to hold

| Check | Result |
| --- | --- |
| Browser suite, `node tests/run-checker-tests.cjs` | **548 of 548**: 546 fixtures, the shared functions check (80 functions) and the shared constants check (77 constants and the clearance block) |
| Python suite, `python -m pytest tests/ -q` with beat-the-machine beside it | **1,173 passed**; 625 passed and 548 skipped without it |
| Parity, `tests/test_parity_shared_inputs.py` | **548 passed**: all 546 fixtures on all 11 fields, the fixture file identity, and a new test holding the risk lexicon and its patterns identical entry for entry |
| Parity on the audit's input sets | 40, 24, 6, 139 and 36 inputs, **245 of 245** equal on all 11 fields |
| The review's 40 probes and 24 prior probes | **0 moved** against the audit's head statuses |
| Prompt 1 rerun | **14 of 17** checked within scope, unchanged: Halyard 7 of 8, Brightwater 3 of 4, Kestrel 4 of 5 |
| The four samples | statuses and coverage strips unchanged, Halyard queue 14, Kestrel 6, Brightwater 0, Ridgeline 3 |
| Author fold against the checker, `audit/author-repair-2026-09-13/parity-node.cjs` | **554 of 554** inputs match |
| Author page in headless Chrome on every audit probe and class mutation, plus the D6 memo | 335 inputs, 294 sentences the checker holds, **0** where the author page disagrees or suggests a stand. The grammar holds 108 of them: the 103 that end at needs review name the word on the card, and the other 5 fail on their direction word and carry that failure |
| Widths 320, 375, 1,024 and 1,600, checker and author page | no document or element overflow at any width; every screenshot opened and read, text wraps inside its column and nothing is clipped |

## Fixtures

212 became **546**. The 175 audit probes are `A001` to `A139` and `B001` to `B036`, each asserting
the status both implementations now return, which is one the audit accepts. The 159 class mutations,
refused and accepted by the status each asserts:

| Class | Ids | Refused | Accepted |
| --- | --- | --- | --- |
| Currency | CUR01 to CUR24 | 20 | 4 |
| Sign and debit or credit | SIGN01 to SIGN26 | 21 | 5 |
| No change and sameness | SAME01 to SAME28 | 24 | 4 |
| Period and basis | PER01 to PER33 | 24 | 9 |
| Another account | ANA01 to ANA20 | 16 | 4 |
| respectively | RESP01 to RESP14 | 11 | 3 |
| Size, rank and share | QTY01 to QTY14 | 10 | 4 |

**Four existing expectations moved**, checked within scope to needs review, each justified in the
fixture's note and in commit `4f89ee1`: `FRAC21` "in the first half of June" and `FRAC23` "at
quarter-end" put the movement inside or across a period two month-end columns cannot show, `COUNT10`
"in Q2" frames it on a quarter, and `COUNT13` "one of the larger moves" ranks the line against the
others. None of them carries a fraction or an unparsed number, which is what each was written to show.

## The risk lexicon, by class

22 entries and about 930 alternatives. The count is of the alternatives each entry's patterns
allow, so a stem written with three endings counts three times; it measures the lexicon's reach, not
a vocabulary.

| Class | Strong entries | Weak entries | About |
| --- | --- | --- | --- |
| Currency | 4 | 0 | 177: 40 names, 62 qualifiers of a dollar, 64 ISO codes, `currency`, `exchange rate`, `FX`, and every currency symbol but `$` |
| Sign and debit or credit | 4 | 1 | 30 |
| Another account | 1 | 1 | 38, plus the rule that every named account needs a claim of its own |
| Sameness | 1 | 1 | 87 |
| Comparison and ranking | 1 | 1 | 46 |
| Basis | 1 | 0 | 55 |
| Period | 2 | 1 | 205, plus the month and year checks against the column labels |
| Change and size | 0 | 2 | 228 |
| Share and quantity | 0 | 1 | 61 |

## The blind drafts

Four sentences in the review's blind drafts move from checked within scope to needs review. They are
not fixtures and not the Prompt 1 drafts, and each move is the grammar doing what it says:

- **halyard-blind S9**, "Movement tracks the increase in product revenue", ties this line to another.
- **kestrel-blind S2**, "the largest movement on the statement", ranks the line.
- **kestrel-blind S4**, "moving with project revenue in the same month", ties it to another line.
- **kestrel-blind S6** reads on to "an annual or multi-month renewal", a period the two months do not
  show, because the sentence splitter does not break after `$57,900.`

## Still open

- **Weak words inside a reason are allowed by design.** `rose $30,000 on sharply higher rates`
  clears, and a writer who tucks a magnitude or a sameness claim that the lexicon calls weak into a
  reason gets it past the grammar. The reviewer's driver question still covers it, and every strong
  word is held wherever it stands.
- **An account name that ends a sentence is not bound by name**, because the binder keeps the full
  stop. `on the lease that also covers Insurance expense.` clears, since the second account is never
  bound and the structural rule does not see it. The listed carry-over words (`so did`, `as did`,
  `likewise`) still hold such a sentence. This is older than the grammar and was left as it was.
- **A ledger with no month in its column labels** cannot contradict a month. The grammar holds only
  two months that are not neighbours; `rose $30,000 in December` on such a ledger clears, as `in 2026`
  did under the review's ruling.
- **The sentence splitter** still breaks after `vs.` and `Rs.`, and not after a figure ending in a
  full stop. Both are older than the grammar.
- **Wording on an already held sentence is not listed.** A sentence a figure, a binding, a negation
  or an unparsed span has already failed or held gets no `Wording` row, so the word appears only once
  the other problem is fixed. This keeps the samples' queues as published.
- **Copy outside this lane still counts 212 fixtures.** `RELEASE-NOTES.md:264` in beat-the-machine is
  lane S1's. The second-pass `README.md` and `CONTRACT-DIVERGENCE.md` counts were brought to 546 here.

## Reproduction

```
bash audit/clearance-grammar-2026-09-13/runners/verify.sh 4f89ee1 216bd2b <scratch dir>
node audit/clearance-grammar-2026-09-13/runners/author-and-widths.cjs <beat-the-machine> <out.json> <screenshot dir>
```

`verify.sh` archives both heads, runs both suites, runs the audit's `run-browser.cjs`, `run-python.py`,
`compare.py` and `grade-probes.cjs` on the audit's five input sets, runs the author fold parity, and
writes `outputs/summary.json` with the before and after counts above. The graded files, the parity
files, the suite logs and `summary.json` are in `outputs/`; the full per-input exports it also writes,
about 13 MB, are left out of the repository and come back on a rerun. `author-and-widths.cjs` drives
the author page and both pages' widths in a throwaway headless Chrome profile through the audit's own
driver, and the eight screenshots it wrote are in `screenshots/`.

---

# The residual classes, 14 September 2026

Lane F3, written at 12:45 AM EDT on 14 September 2026. The lane above left four classes open under
**Still open**, and they are closed below in both implementations: size words inside a reason, the
account name that ends a sentence, a ledger with no month in its labels, and the sentence splitter.
A weak sameness or share word inside a reason is still left to the reason, as that list says. Every
input is synthetic and none of it is participant evidence. Nothing was posted or pushed.

**Heads tested.** Code behavior was run on `git archive` snapshots, with the independent audit's own
runners, unchanged, against the heads before this lane as the before.

| Repository | Before | After |
| --- | --- | --- |
| beat-the-machine | `e7b5994` | `09cec33`, over `1f9acb7`: the checker, the shared reader and the fixtures |
| second-pass | `ced24e5` | `bb6fd2d`, over `dbf0342`: the Python checker, the fixtures and the tests |

## What each class closed

- **Sentence boundaries.** The splitter reads abbreviations. A full stop no longer ends a sentence
  after `vs.`, `approx.`, `e.g.`, `Accum.` and the other listed shorthands, after `No.`, `Rs.`,
  `Inc.` or `U.S.` before a figure, or after a title or an initial before a name, and it does end one
  after a figure a capital follows, `$57,900. An annual renewal`, and after a closing bracket or quote.
  A decimal broken by a space, `rose 7. 5 percent`, stays in one sentence and is an unparsed span, so
  it can neither clear nor fail on the half it would otherwise read. The lists and the two readings
  that stay ambiguous are in `CHECKER.md` under **Sentence boundaries**. 44 sentences written to test a
  person's reading split as a person reads them, and 704 memos split the same way in both
  implementations.
- **Size words.** The contract documents no threshold for "sharply", so none is invented: a word that
  sizes a movement holds the sentence at needs review wherever it stands, reasons included, and names
  the word. That covers adverbs of degree, a degree word on a comparative (`much higher`), movement
  verbs and nouns that carry their own size (`surged`, `edged up`, `eased`, `a jump`), which are still
  tested for direction, and a size adjective standing on a movement, in front of the noun or after it
  with a copula between (`a significant increase`, `the change was small`). An adjective that sizes
  something else, `a large new office`, stays with the reason.
- **Periods the labels cannot bind.** A month, a date, a year and the words `month`, `this month`,
  `month over month` and `month-end` are bound only by the column labels, anywhere in the sentence. A
  ledger whose labels name no period, a plain paste or one headed `Prior / Current`, binds none of
  them, so each is held with the word named; labels that name other months, another year or two
  months not in a row contradict them. `over June` on a ledger whose current column is June is held as
  measuring from the wrong column. The same sentences clear on a ledger that names the months.
- **An account name that ends a sentence.** The binder treats a full stop, a comma, a question mark,
  an exclamation mark or a quote after a name as punctuation, so position no longer matters. A colon
  no longer splits a binding clause, which keeps a name that trails a label's figures from failing
  them: `5000 Cost of product sold: +$348,000 - Movement tracks the increase in product revenue.` is
  held as a binding conflict, never failed against product revenue.
- **The lexicon, one step past its words.** Probing every class the way the next review will found
  and closed `30,000 kr`, `Fr. 30,000`, `30,000 zł` and `RM 30,000` (currencies now unparsed beside a
  figure), `as both lines did`, `eclipsing` and `in lockstep with`, `below the industry average` and
  `above pre-pandemic levels`, `to a new high` and `from a low base`, `as of today`, `yesterday` and
  `overnight`, `30 pct pts` (points after a percent, unparsed), and `No. 4471` read as a negation. Of
  178 neighbour probes, 100 had a sentence checked within scope before and 38 after, and each of the 38
  was read by hand: what clears in it is what a person would let clear.

## Fixtures

546 became **658**. The 111 new ones, with T19b, the Ridgeline sample end to end:

| Class | Ids | Refused | Accepted | Mixed |
| --- | --- | --- | --- | --- |
| Sentence boundaries | SPLIT01 to SPLIT27 | 11 | 13 | 3 |
| Size words | SIZE01 to SIZE22 | 16 | 5 | 1 |
| Periods and the column labels | PLAB01 to PLAB24 | 14 | 8 | 2 |
| Account names at the edge of a sentence | BIND01 to BIND17 | 12 | 4 | 1 |
| The lexicon, one step past its words | LEX01 to LEX21 | 16 | 4 | 1 |

A SPLIT fixture asserts the number of sentences and each one's status; a mixed fixture carries a clause
that clears beside one that does not. **Fifteen expectations moved** from checked within scope to needs
review, each justified in the fixture's note and in commit `1f9acb7`:

| Fixture | Sentence | Why it is held now |
| --- | --- | --- |
| P39, COUNT14 | `Rent expense rose $30,000 in 2026.` | the year is still read as a year, not a figure; the ledger has no header row, so no label names a year |
| COUNT08, COUNT09 | `on the lease signed on June 30.`, `on 30 June 2026.` | the day and year are still read as a date; no label names June |
| FRAC26 | `on the lease that started on 6/1.` | still a date, not a fraction; no label names a month |
| MUL20 | `after the double count in May was reversed.` | `double count` is still not a multiplier; no label names May |
| SAME22 | `remained at $130,000 month over month.` | `remained at` still agrees with a line that did not move; the columns are not labelled as months |
| PER19, PER24, PER25 | `a month`, `month over month`, `from the prior month` | the month frame is bound only where the labels show two months in a row (PLAB18, PLAB20, PLAB22 clear) |
| PER26, PER33 | `from May to June`, `in June versus May` | neither month is named by the labels (PLAB17 clears) |
| PER29 | `on the lease signed in the first half of June.` | `first half of June` still stands in a reason; `June` is bound wherever it stands |
| ANA18 | `on the lease that also covers Insurance expense.` | the name at the end now binds, and the figure's clause names two lines |
| QTY09 | `on sharply higher rates at the new site.` | a size word in a reason is held |

P39 is one of the review's forty probes. The review observed not checked on it and required nothing more
specific; the repair lane had asserted checked within scope. It is the only one of the review's 40 and
24 probes that moves. T18 gains three assertions, card 14 held and a queue of 17, and A115 one, a single
sentence; neither had asserted those before.

## Everything that had to hold

| Check | Result |
| --- | --- |
| Browser suite, `node tests/run-checker-tests.cjs` | **660 of 660**: 658 fixtures, the shared functions check (82 functions) and the shared constants check (89 constants and the clearance block) |
| Python suite, `python -m pytest tests/ -q` with beat-the-machine beside it | **1,397 passed**; 737 passed and 660 skipped without it |
| Parity, `tests/test_parity_shared_inputs.py` | **660 passed**: all 658 fixtures on all 11 fields, the fixture file identity, and the lexicon test, which now also holds the size lists, the period binding's patterns, the splitter's abbreviation lists, what the splitter does at every stop in ten sentences, and how eight pairs of column labels are read |
| Parity on the audit's input sets, the samples and the neighbour probes | 40, 24, 6, 139, 36, 4 and 178 inputs, **427 of 427** equal on all 11 fields |
| The audit's 175 probes | **0 false clearances and 0 other misses**, before and after; no probe's status moved, and A115 now reads as one sentence |
| The review's 40 probes and 24 prior probes | **P39 moved**, as above; nothing else |
| Prompt 1 rerun | **14 of 17** checked within scope, unchanged: Halyard 7 of 8, Brightwater 3 of 4, Kestrel 4 of 5 |
| The four samples | Brightwater and Kestrel unchanged. Halyard 3 checked, 6 needs review, 3 failed, queue 17, from 4, 5, 3 and 14: card 14 binds 7000 Depreciation, which its sentence ends on, and the case keys that card as an unsupported driver; the queue adds its binding conflict and unresolved figure, and `eased` on card 3, which had already failed. Ridgeline 0 checked, 1 needs review, 2 failed, queue 4, from 1, 0, 2 and 3: T1's `began in July` on a ledger with no header row |
| Author fold against the checker, `audit/author-repair-2026-09-13/parity-node.cjs` | **665 of 665** inputs match |
| Author page in headless Chrome on every audit probe and every class mutation | 445 inputs and 459 sentences; the checker holds 376 of them; **0** where the author page splits a memo differently, gives a different status or suggests a stand on a held sentence |
| Checker Halyard sample and author Kestrel sample at 320, 375, 768, 1,024, 1,280 and 1,600 | no document or element overflow at any width, with card 14's checks opened; all 18 screenshots opened and read: the counts, card 14's binding conflict and card 3's `eased` row wrap inside their columns and nothing is clipped |

## The six retained drafts

Sentence statuses per draft, before at `e7b5994` and after at `09cec33`, from the audit's
`six-drafts-as-fixtures.json`, for the claims pass to carry into the evidence note:

| Draft | Sentences | Checked within scope | Needs review | Not checked | Failed | Queue |
| --- | --- | --- | --- | --- | --- | --- |
| halyard-blind, before | 30 | 1 | 14 | 13 | 2 | 55 |
| halyard-blind, after | **29** | **0** | **15** | **12** | 2 | **59** |
| halyard-prompt1, before and after | 8 | 7 | 0 | 1 | 0 | 9 |
| brightwater-blind, before | 6 | 3 | 1 | 2 | 0 | 5 |
| brightwater-blind, after | 6 | **0** | **4** | 2 | 0 | **8** |
| brightwater-prompt1, before and after | 4 | 3 | 0 | 1 | 0 | 4 |
| kestrel-blind, before | 7 | 0 | 5 | 2 | 0 | 14 |
| kestrel-blind, after | **9** | **2** | **3** | **4** | 0 | **13** |
| kestrel-prompt1, before and after | 5 | 4 | 0 | 1 | 0 | 6 |

The blind drafts are not fixtures. Every change is one of the classes above:

- **halyard-blind.** `**June 2026 vs.` and `May 2026**` are now one sentence, `**June 2026 vs. May
  2026**`, still not checked. S5, `4100 Service revenue ... during the warmer month ...`, moves from
  checked within scope to needs review on `month`: the ledger is headed `Prior / Current`, which names no
  month. S8, `5000 Cost of product sold ... Movement tracks the increase in product revenue.`, stays at
  needs review, now as a binding conflict because `product revenue.` binds. S27's totals sentence stays
  failed and now also binds `warehouse wages.`. The queue grows by those items.
- **brightwater-blind.** S1, S3 and S5, `... rose $42,400, or 44.2 percent, over May.` and its two
  kin, move from checked within scope to needs review on `May`: the ledger is four plain columns with no
  header row. S4 stays at needs review and names `far ahead`, a size, rather than `ahead of`.
- **kestrel-blind.** S1 and S6 each ran two sentences together across a figure's full stop. They split:
  `4000 Recurring managed services rose $36,900, or 22.85 percent, to $198,400.` and `6200 Software
  licences and hosting rose $35,300, or 156.19 percent, to $57,900.` are checked within scope, and the
  sentences after them, `The statement does not carry the cause ...` and `Confirm whether an annual or
  multi-month renewal was paid inside July.`, are unmatched and not checked. The lane above recorded S6
  as needs review because of that splitter defect.
- **The Prompt 1 drafts** do not move, sentence for sentence.

## Still open, after this lane

- **Direction words in a reason that no clause word opens are tested.** `Rent expense rose $30,000 on a
  decrease in vacancy` fails on `decrease`: `on` opens a reason for the lexicon but not a clause for the
  direction check. After a comma the word is held, and after `as`, `because` or `while` it is left to
  the reason. This is older than the grammar, and it fails rather than clears.
- **Two splits stay ambiguous.** An initialism before a capitalized word, `U.S. Treasury`, and an initial
  after a capitalized first name, `John J. Smith`, are read as sentence ends, and an abbreviation outside
  the lists is read as an ordinary word.
- **A name that is bound but claims nothing takes that line off the silent list.** `Rent expense rose
  $30,000; so did Insurance expense.` now binds Insurance expense, so the sentence is held and the line
  is not listed as silent. The held sentence carries it to a person; before, the line was silent and the
  sentence was held on `so did`. A mid-sentence mention always behaved this way.
- **Quarters, halves and fiscal years are never bound**, even on a ledger whose labels name them.
- **Prompt 1 on a ledger with no header row.** A drafted reason that names a month, `because the lease
  renewed on 1 June`, is held unless the pasted ledger carries its header. Prompt 1's text was not
  changed in this lane.
- **A weak sameness or share word inside a reason is still allowed**, `rose $30,000 as rents stayed
  high` or `on leases that were mostly renewals`, by the design the lane above describes. Only size words
  moved out of that allowance.
- **Wording on an already held sentence is not listed**, as above.

## Reproduction

```
bash audit/clearance-grammar-2026-09-13/residual/runners/verify.sh 09cec33 bb6fd2d e7b5994 ced24e5 <scratch dir>
node audit/clearance-grammar-2026-09-13/residual/runners/pages.cjs <beat-the-machine> <out.json> <screenshot dir>
```

`verify.sh` archives both heads after and before, runs both suites and the parity test alone, runs the
audit's `run-browser.cjs`, `run-python.py`, `compare.py` and `grade-probes.cjs` on the audit's five input
sets, the four samples and the 178 neighbour probes at both heads, runs `split-parity.cjs` on the 44
readings in `inputs/split-readings.json` and every memo, runs the author fold parity, and writes
`residual/outputs/summary.json` with every count above. The graded files, parity files, suite logs and
summary are in `residual/outputs/`; the full per-input exports stay in the scratch directory. `pages.cjs`
drives the author page on every class input and both samples at six widths in a throwaway headless
Chrome profile through the audit's driver, and the 18 screenshots are in `residual/screenshots/`.

---

# The checker residuals, 14 September 2026

Lane F4, written at 1:55 AM EDT on 14 September 2026. The lane above left three classes open under
**Still open**, and a fourth was handed to this lane by the claims pass. All four are closed below
in both implementations: a direction word a reason governs, an abbreviation inside a name, a quarter
the column labels never bound, and a word that says how much of the movement a sentence explains.
Every input is synthetic and none of it is participant evidence. Nothing was posted or pushed.

**Heads tested.** Code behavior was run on `git archive` snapshots, with the independent audit's own
runners, unchanged, against the heads before this lane as the before.

| Repository | Before | After |
| --- | --- | --- |
| beat-the-machine | `c369dc7` | `28c273b`, over `b733040` and `7735836`: the checker, the shared reader, the fixtures and the samples |
| second-pass | `f9348ff` | `5c1d3be`, over `884ee43` and `deb7f76`: the Python checker, the fixtures, the tests and the shared case |

## What each class closed

- **A direction word a reason governs.** The direction check now reads a clause in two parts. The
  **claim** runs to the first word that opens a reason, and only the claim is tested against the line
  the figures tied. A direction or no-change word inside the **reason** belongs to what the reason
  names, so `rose $30,000 on a decrease in vacancy`, `fell despite an increase in volume`, `rose
  $30,000 on flat volumes` and `rose $30,000 with lower occupancy` are no longer failed on the second
  word: a sentence that is true never fails on a word that belongs to the cause. Where the reason
  names exactly one bound line, `on the decrease in Insurance expense`, the word is tested against
  that line, which is the subject the words give it, and the finding names the right account. The
  clearance grammar and the direction check now read one reason boundary, `reasonAt` over `claimEnd`,
  and that boundary gained the contrast openers `despite`, `in spite of` and `notwithstanding` and
  the attribution openers `offset by`, `helped by`, `aided by`, `boosted by` and `attributable to`. A
  back-pointer that points at another line, `the decrease in Insurance expense`, no longer counts as
  pointing back at this one. A direction word in a clause of its own that names no line is still held
  at needs review with the word named, which is what `, driven by a drop in landlord credits` gets.
- **An abbreviation inside a name.** After an initialism, a company suffix or a title, a capitalized
  word is read as the rest of a name, so `U.S. Treasury`, `U.K. Subsidiary`, `J.P. Morgan`, `St.
  Louis`, `Ft. Worth`, `Co. Ltd.` and `Mr. J. Smith` are one sentence. The stop still ends one where
  the word after it opens a sentence rather than continuing a name (`The`, `It`, `Management`, `A`),
  or where the text in front of it is already a sentence, carrying a figure, a direction word or a
  finite verb, **and** what follows makes a claim of its own. That is the difference between
  `Interest expense on U.S. Treasury bills rose $31,200.`, one sentence, and `Revenue grew in the
  U.S. Rent expense rose $30,000.`, two. 24 sentences written to test a person's reading of a name
  split as a person reads them, and every memo in the suite and the drafts splits the same way in
  both implementations.
- **Quarters bound by the column labels.** `Q2`, `2Q`, `2Q26`, `Qtr 2` and `the second quarter` bind
  where either label names that quarter; `the quarter`, `quarterly`, `quarter-end`, `quarter over
  quarter` and a three-month span bind where the labels show two quarters in a row. On a ledger kept
  in months, or one whose labels name no period, none of them binds, so a quarter reference is held
  at needs review with the period named and never clears there. The reading runs the other way too: a
  column that covers a quarter names no single month, so `in June`, `for the month` and `month over
  month` are held on a quarterly ledger instead, and a quarter in a label also orders the two
  periods, so `Q2 2026` printed before `Q1 2026` is read the right way round. `QTD`, `quarter to
  date`, halves and fiscal years stay held whatever the labels say. Two readings behind the class
  were repaired: `$30,000 quarter over quarter` no longer has `000 quarter` taken out of it as a
  fraction, and `in Q2, and` reads the label `Q2` rather than the number `2,`.
- **A word that says how much of the movement a sentence explains.** The lanes above allowed a weak
  share word inside a reason by design, and the claims pass asked for that to be decided the way the
  size words were decided. It is: nothing a close uses documents what `mostly` or `partly` covers, so
  the checker invents no share and tests nothing. A share word now holds the sentence at needs review
  wherever it stands, in a reason as much as in the claim, and the queue names it: `mostly`, `mainly`,
  `primarily`, `principally`, `chiefly`, `predominantly`, `largely`, `broadly`, `partly`, `partially`,
  `entirely`, `wholly`, `solely`, `exclusively`, `virtually`, `essentially`, `practically`,
  `basically`, `in part`, `in large part`, `for the most part`, `on the whole`, `to some extent`,
  `more or less`, and `most of`, `much of`, `the bulk of`, `the majority of` and kin where what
  follows is a movement or a figure. A share of something that is not the movement is left with the
  reason and still clears: `all of the partners`, `a share of the new lease costs`, `fully loaded
  rent`, `the whole-floor lease`.

## The Brightwater sample

The checker stamped `brightwater-v5` while the drill ran `brightwater-v6`. `build-checker-cases.cjs`
now reads `cases/brightwater-v6.json`, and `cases/shared/brightwater.json` in second-pass carries the
same stamp with the v6 definition beside it. v6 rewrote the evidence and the reveals on the cards and
left the ledger and every memo sentence as v5 wrote them, so **no status, count or queue item on the
sample moves**: 5 sentences, all checked within scope, an empty queue, before and after. `T18b`
asserts the new case version and the same outputs, with the reason in the fixture's note.

## Fixtures

658 became **744**. The 86 new ones:

| Class | Ids | Refused | Accepted | Mixed |
| --- | --- | --- | --- | --- |
| A direction word a reason governs | REAS01 to REAS19 | 10 | 7 | 2 |
| An abbreviation inside a name | NAME01 to NAME25 | 10 | 13 | 2 |
| A quarter against the column labels | QTR01 to QTR22 | 14 | 7 | 1 |
| A share of the movement | HEDGE01 to HEDGE20 | 13 | 5 | 2 |

Five neighbours of each class were probed and kept: in REAS, `offset by` after a comma, `given`,
`amid`, `because it fell in the prior period` and a reason that names a bound line; in NAME, `Mr. J.
Smith`, `Acme Co. Ltd.`, `etc.` before a capital, `Schedule A.` and `Oak St. The`; in QTR, `the
third qtr.`, `2Q`, `on a quarterly cycle`, `the three-month period` and `quarter to date`; in HEDGE,
`the whole-floor lease`, `all of the partners`, `a share of the new lease costs`, `fully loaded rent`
and `the bulk of the new lease costs`, all five of which still clear because none of them apportions
the movement.

**One expectation moved**, justified in the fixture's note and in commit `b733040`:

| Fixture | Sentence | Why it moved |
| --- | --- | --- |
| A086 | `Rent expense rose $30,000 quarter over quarter.` | not checked to **needs review**: the reader no longer takes `000 quarter` out of the figure as a fraction, which no person reads there, so the sentence is held on the quarter frame instead of left unchecked on an unparsed span. The audit's own basis for A086 is a period mismatch and it accepts needs review or not checked |

`T18b` also asserts `brightwater-v6` rather than `brightwater-v5`, which is the sample's stamp and
not a status.

## Everything that had to hold

| Check | Result |
| --- | --- |
| Browser suite, `node tests/run-checker-tests.cjs` | **746 of 746**: 744 fixtures, the shared functions check (89 functions) and the shared constants check (97 constants and the clearance block) |
| Python suite, `python -m pytest tests/ -q` with beat-the-machine beside it | **1,569 passed**; 823 passed and 746 skipped without it |
| Parity, `tests/test_parity_shared_inputs.py` | **746 passed**: all 744 fixtures on all 11 fields, the fixture file identity, and the lexicon test, which now also holds the quarter patterns, the splitter's name lists, what it does at eight more stops, how eight pairs of column labels read as months or as quarters, and where the claim ends and the reason begins in six sentences |
| Parity on the audit's input sets, the samples, the neighbour probes and this lane's class probes | 40, 24, 6, 139, 36, 178, 4 and 86 inputs, **513 of 513** equal on all 11 fields |
| The audit's 175 probes | **0 false clearances and 0 other misses**, before and after; one probe moved, A086, to a status the audit accepts |
| The review's 40 probes and 24 prior probes | **nothing moved** against the heads before this lane. P39 still stands where lane F3 put it |
| Prompt 1 rerun | **14 of 17** checked within scope, unchanged: Halyard 7 of 8, Brightwater 3 of 4, Kestrel 4 of 5 |
| The four samples | **unchanged**, sentence for sentence and queue for queue: Halyard 3 checked, 6 needs review, 0 not checked, 3 failed, queue 17; Brightwater 5, 0, 0, 0, queue 0; Kestrel 3, 0, 1, 2, queue 6; Ridgeline 0, 1, 0, 2, queue 4 |
| Lane F3's 178 neighbour probes | 38 cleared before, 38 after; **one moved**, NB052 `Rent expense rose $30,000 on a tiny decrease in vacancy.`, from failed to needs review, which is this lane's first class: the sentence is true, and `tiny` holds it as a size word |
| The sentence splitter against a person's reading | 24 name readings and lane F3's 44, **68 of 68** as a person reads them; 770 texts in the first run and 790 in the second, every one split the same way in both implementations |
| Author fold against the checker, `audit/author-repair-2026-09-13/parity-node.cjs` | **751 of 751** inputs match |
| Author page in headless Chrome on every audit probe and every class mutation, this lane's four included | 531 inputs and 553 sentences; the checker holds 430 of them; **0** where the author page splits a memo differently, gives a different status or suggests a stand on a held sentence |
| The checker at 375 and 1,024, the Halyard sample and a quarterly ledger carrying three classes in one memo | no document or element overflow at either width, closed or with every sentence open; all four screenshots opened and read: the coverage strip, the wording row naming `June` against a quarterly column, and the cleared sentence carrying `Q2`, a reason and `U.S. Treasury` all wrap inside their columns and nothing is clipped |

## The six retained drafts

**No draft moved.** Sentence statuses and queue sizes are the same at `c369dc7` and at `28c273b`,
from the audit's `six-drafts-as-fixtures.json`: halyard-blind 29 sentences, 0 checked within scope,
15 needs review, 12 not checked, 2 failed, queue 59; halyard-prompt1 8, 7, 0, 1, 0, queue 9;
brightwater-blind 6, 0, 4, 2, 0, queue 8; brightwater-prompt1 4, 3, 0, 1, 0, queue 4; kestrel-blind
9, 2, 3, 4, 0, queue 13; kestrel-prompt1 5, 4, 0, 1, 0, queue 6. No drafted sentence carries a
quarter, an abbreviation inside a name, a share word the grammar had allowed, or a direction word
inside a reason that the checker had been testing, so the counts the claims pass carries into the
evidence note do not change.

## Still open, after this lane

- **A sentence that reads as one to a person but carries no figure, no direction word and no listed
  finite verb does not end at a name's full stop.** `The lease was signed in the U.S. Rent expense
  rose $30,000.` runs on. Running on holds a sentence rather than clearing a fragment, which is the
  safer error, and everything in the merged sentence is still read.
- **A direction word after a comma is held, not tested.** `, driven by a drop in landlord credits`
  comes back as a direction word the checker cannot tie to a line. That is the reviewer's question
  rather than a failure, and it is the behavior lane F3 recorded.
- **Halves, fiscal years and `quarter to date` are never bound**, whatever the labels say, and a
  ledger kept in weeks or in years binds no period at all.
- **`three months` in the plural is held on any ledger**, a quarterly one included, because the
  period lexicon reads it as a multi-month span; the singular `three-month` belongs to the quarter
  class and binds on a quarterly ledger.
- **A weak sameness word inside a reason is still allowed**, `rose $30,000 as rents stayed high`, and
  so are the weak change, period, ranking and quantity words the lexicon lists. Only the size words
  and now the share words were moved out of that allowance.
- **Wording on an already held sentence is not listed**, as the lanes above describe.

## Reproduction

```
bash audit/clearance-grammar-2026-09-13/checker-residuals/runners/verify.sh 28c273b 5c1d3be c369dc7 f9348ff <scratch dir>
node audit/clearance-grammar-2026-09-13/checker-residuals/runners/pages.cjs <beat-the-machine> <out.json> <screenshot dir>
```

`verify.sh` archives both heads after and before, runs both suites and the parity test alone, runs
the audit's `run-browser.cjs`, `run-python.py`, `compare.py` and `grade-probes.cjs` on the audit's
five input sets, the four samples, lane F3's 178 neighbour probes and this lane's 86 class probes at
both heads, runs `split-parity.cjs` on the 24 name readings and on lane F3's 44, runs the author fold
parity, and writes `checker-residuals/outputs/summary.json` with every count above. The graded files,
parity files, suite logs and summary are in `checker-residuals/outputs/`; the full per-input exports
stay in the scratch directory. `pages.cjs` drives the author page on every class input and the
checker at both widths in a throwaway headless Chrome profile through the audit's driver, and the
four screenshots are in `checker-residuals/screenshots/`.
