# Independent adversarial audit of Second Pass, second pass, 14 September 2026

Lane A1, written at 2:40 AM EDT on 14 September 2026. I built none of this. Every result was run, not
read. All memos and ledgers below are synthetic. Nothing was posted or pushed, and no browser was
driven: the director's wind-down arrived mid-run, so the author page, the explanation lock, the
required read and the findings export were **not rerun tonight**, and neither was the public copy.
Those carry their 13 September status.

**Heads tested**, from `git archive` snapshots of the committed heads, so no working-tree edit could
reach a result:

| Repository | Commit |
| --- | --- |
| beat-the-machine | `64bea178561d4d4c929f1a5241f16e09a09260c8` |
| second-pass | `5c1d3be5b4aac0d825d58ad65e5a0d1704ac7a35` |

Supplied suites at those heads: `node tests/run-checker-tests.cjs` **746 passed, 0 failed**;
`python -m pytest tests/ -q` in second-pass with `BEAT_THE_MACHINE` set **1,569 passed**;
`tools` **54 passed**. The fixture file holds **744** inputs, and 175 of them are this audit's own
probes from 13 September.

## Verdict

The clearance grammar closed every hole the 13 September audit found. All 48 former false clearances
now hold or fail, the "respectively" false failure is held as the contract requires, and the review's
own 64 probes return the required status in both implementations. Parity is exact on 431 inputs
across 11 compared fields. The remaining problem is the same shape as before, one word further out:
the grammar still decides by lists of words, so a no-change claim written in words the sameness list
does not carry clears on a line that moved 30 percent. **`Rent expense was rangebound at $130,000.`
returns checked within scope**, and eight more like it. That is the third review's central class,
open at a lower frequency: 34 of 186 new probes, against 48 of 175 on 13 September, and none of tonight's
escapes is a numeric claim the checker read wrongly.

## Replays

| Set | Inputs | Result |
| --- | --- | --- |
| The third review's 40 new probes | 40 | Every one at the status the repaired contract requires. 12 differ from what the review observed, all in the safe direction (P05 to P10, P13, P23, P25, P37 hold or fail; P39 is held as an unbound year). `outputs/replay-64-summary.json` |
| The third review's 24 prior probes | 24 | Every one required; N13 and N24 moved from cleared to failed. |
| A1's 175 probes of 13 September | 175 | **0 false clearances, 0 contract misses, 0 parity differences.** All 48 former false clearances moved: 11 sameness and 12 period claims to needs review, 10 currency and 5 sign or digit forms to not checked, 6 sign clashes to failed. A093 (`respectively`) moved from failed to needs review. `outputs/a1-status-change.json` |
| The six retained model drafts | 6 | The three Prompt 1 drafts still read 14 of 17 sentences checked within scope. The three blind drafts now hold more than they did: halyard-blind 2 checked to 0, brightwater-blind 3 to 0, kestrel-blind 3 to 2, and the sentence counts move with the new boundary rules (halyard 30 to 29, kestrel 7 to 9). Any published count taken from the old reader needs re-deriving; the copy check was not rerun. `outputs/six-drafts-summary.json` |
| Parity, every set | 431 | status, role, stats, queueKinds, queue, finding, survivors, csv, tsv, json, prompt: **no difference on any input**. |

## The third review's 41 findings

Nine were re-verified tonight against the checker: **eight CLOSED, one PARTIAL**. The other 32 were
not rerun under the wind-down and carry their 13 September status (17 CLOSED, 10 PARTIAL, 4 OPEN, one
deferred by ruling). Carried forward, the table stands at **25 CLOSED, 11 PARTIAL, 4 OPEN**.

| # | Finding | Status tonight | Proof |
| --- | --- | --- | --- |
| 18 to 21 | P05, P13, P23, P25 | CLOSED | not checked, failed, not checked, not checked, in both implementations, no exception |
| 22 | "Anything numeric the grammar cannot read is recorded rather than dropped" | CLOSED | Every currency, sign, digit and orphan-unit probe from 13 September now records its span: 23 moved to not checked or failed |
| 23 | T32 and T43 mislabelled as controls | CLOSED | 746 of 746 |
| 24 | Fix the classes with mutations, not a list of words | PARTIAL | The grammar now clears only what it can read, but the risk lexicon is still a word list: 34 of 186 new probes clear where a reviewer would not (N1 to N5 below) |
| 25 | Prompt 1 through its own reader | CLOSED | 7 of 8, 3 of 4 and 4 of 5 sentences checked within scope |
| 26 | Parity and the fixture files | CLOSED | 431 inputs, 11 fields, no difference |

## New defects, ranked

186 new probes, all run in both implementations with no parity difference. `outputs/c-graded.json`
and `outputs/d-graded.json` carry every input and output.

### High

**N1. A no-change claim written outside the sameness list clears on a line that moved 30 percent.**
Ledger `6100 Rent expense 100,000 to 130,000`. Each returns **checked within scope** in both
implementations, with `$130,000` read as the current balance and no direction tested:

- `Rent expense was rangebound at $130,000.` (C133, D001)
- `Rent expense was unremarkable at $130,000.` (D002)
- `Rent expense went nowhere, ending at $130,000.` (D003)
- `Rent expense was quiet at $130,000.` (D004)
- `Rent expense was untouched at $130,000.` (D005)
- `Rent expense was as before, at $130,000.` (D006)
- `Rent expense was at a standstill at $130,000.` (D009)
- `Rent expense was unvaried at $130,000.` (D011)
- `Rent expense showed no real movement, ending at $130,000.` (D012)

Required: needs review or failed. This is the class of P13 and of `stable`, which the sameness entry
now catches; `CHECKER.md:283` names ten words and these are the next ten. Neighbours that do hold:
`where it was in May`, `held its ground`, `uniform with May`. The smallest repair that ends the class
is structural rather than lexical: a sentence whose only figure is a balance, with no movement figure
and no tested direction word, cannot be called checked within scope.

### Medium

**N2. A size word standing after the movement noun clears.** `Rent expense rose $30,000; the increase
was manageable.` (C027, D013) and, in the same shape, `tolerable`, `decent`, `noteworthy`, `chunky`,
and as adjectives in front of the noun `a beefy increase`, `a whopping increase`, `a punchy increase`
(D014 to D021). Eight clear; `a sizeable increase` holds, and so does `the change was not small`.
Required by `CHECKER.md:369`: a size adjective on a movement is held.

**N3. Share-of-the-movement neighbours clear.** `Rent expense rose $30,000, a good chunk of it on the
new lease.` and the same with `nearly all of it`, `the remainder`, `the balance of it`, `a fair bit of
it`, `a slice of the increase` (D022 to D028). Six clear; `the lion's share of it`, `some of the
increase` and `the rest of the increase` hold. Required by `CHECKER.md:371`.

**N4. Hedges are handled two ways, and the contract names neither.** On a figure that ties,
`about $30,000`, `approximately $30,000`, `roughly $30,000`, `~$30,000`, `some $30,000`, `give or
take`, `or thereabouts`, `in round numbers` and `about 30 percent` clear (D030 to D041), while
`circa`, `a ballpark $30,000`, `north of`, `upwards of`, `in the region of`, `on the order of`, `a
touch over` and `just shy of` are held. `CHECKER.md` lists no approximation class, so neither
behaviour is documented, and a reader cannot predict which they get.

**N5. A plus written after a figure is not read as a sign.** `Rent expense rose $30,000+.` (D042) and
`Rent expense rose $30,000 +.` (D043) clear, while `Rent expense changed by 30,000-.` (D047) fails, as
contract 1 requires for a minus written straight after a figure. `$30,000-plus`, `30,000(+)` and
`$30,000 plus` hold.

**N6. Two false failures.** `Rent expense rose $30,000 per the “decline in vacancy” memo.` (C015)
**fails**: `per` opens no reason, so a direction noun inside a quoted document title is tested against
the line. `Rent expense rose close to $30,000.` (C046) **fails**: `to $30,000` is read as the current
balance. Both would reach the author page as a suggested flag on a true sentence.

### Low

**N7. A proper name carrying a lexicon word holds.** `at the Stable Yard depot` (C114), `on the
Constant Contact subscription` (C115) and `at the Level 3 data centre` (C116) are held on `stable`,
`constant` and `level`. The bound account's own name is taken out first, so `Rent expense, level 3,
rose $30,000.` clears (C113); other names are not.

**N8. A reason in front of the claim is read two ways.** `Because vacancy decreased, rent expense rose
$30,000.` clears (C012); `Due to a decrease in vacancy, rent expense rose $30,000.` is held as an
unresolved direction (C013).

## What the new probes confirm as closed

Reason-governed direction words behave as the contract says: a reason that points back with `it`, `the
balance` or the bound line's own name is tested and fails or holds (C001 to C011, C017), and a reason
naming something else is left alone (C014, C018). Quarters and halves bind only to the column labels
(C075 to C087), months and dates bind to them the same way (C088 to C103), a name at the end of a
sentence binds and needs a claim of its own (C107 to C112), abbreviations do not split a sentence
(C098, C117), and a failed figure keeps its status with no wording row (C118, C122).

## Not rerun tonight

The author page and its stale-save paths, the explanation lock and its minimum, the required read and
its changed-after-the-draft measure, `tools/findings.py` and its scoring sheet, and every public
sentence and the copy of record. The 13 September audit's rows for those stand until they are rerun,
and the six drafts above show that counts published from the old reader need re-deriving at the
freeze.

## Reproduction

```
git -C <beat-the-machine> archive 64bea17 | tar -x -C <G>
git -C <second-pass> archive 5c1d3be | tar -x -C <T>
node <G>/tests/run-checker-tests.cjs
(cd <T> && BEAT_THE_MACHINE=<G> python -m pytest tests/ -q)
node runners/make-c-probes.cjs && node runners/make-d-probes.cjs
node runners/run-browser.cjs <G> inputs/<set>.json outputs/<set>-browser.json
python runners/run-python.py <T> inputs/<set>.json outputs/<set>-python.json
python runners/compare.py outputs/<set>-browser.json outputs/<set>-python.json outputs/<set>-parity.json
node runners/grade-probes.cjs inputs/<set>.json outputs/<set>-browser.json outputs/<set>-python.json outputs/<set>-parity.json outputs/<set>-graded.json
```

`<set>` is `new-40-probes`, `prior-24-probes`, `six-drafts-as-fixtures`, `a1-probes`,
`a1-sizing-probes`, `c-probes` or `d-probes`. `run-browser.cjs` runs `checker.html` under Node with
the suite's own document stub; no browser was launched. `SHA256SUMS.json` fingerprints every file in
`audit/independent-2026-09-14/`.
