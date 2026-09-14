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
