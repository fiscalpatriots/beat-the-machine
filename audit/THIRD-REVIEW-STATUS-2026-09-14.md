# The third review, finding by finding, at the 14 September 2026 freeze

The independent audit graded the third independent review of 13 September 2026 into 41 findings.
At the heads it first tested they stood at 25 closed, 11 partial, 4 open and 1 deferred by ruling.
The fourth review packet of 14 September re-verified them at `c369dc7` and `f9348ff` and reported
32 closed, 4 partial, 4 open and 1 deferred.

Every row below was read again against the freeze head, with the suites rerun rather than quoted.
**They stand at 34 closed, 2 partial, 4 open and 1 deferred.** Rows 7 and 39 moved, both of them
on the claims pass that was named as in progress in the fourth packet and has now landed.

Unless a row says otherwise, "both" means `checker.html` and `second_pass/checker.py` returned the
same result on every one of the eleven compared fields.

## What the suites returned at this head

| Suite | Command | Result |
| --- | --- | --- |
| Browser checker | `node tests/run-checker-tests.cjs` | **746 of 746**: 744 shared fixtures, the shared reader check and the shared constants check |
| Command-line checker | `python -m pytest tests/ -q` in second-pass, beat-the-machine beside it | **1,569 passed**, of which 823 stand alone |
| Parity | `python -m pytest tests/ -q -k parity` | **746 passed**: every shared fixture on all eleven fields, the fixture file identity and the lexicon |
| The audit's own input sets | the audit runners over eight sets of 40, 24, 6, 139, 36, 178, 4 and 86 | **513 of 513** equal on all eleven fields |
| The audit's 175 adversarial probes | `run-browser.cjs`, `run-python.py`, `compare.py`, `grade-probes.cjs` | **0 false clearances, 0 other contract misses, 0 parity differences** |
| Author fold against the checker | `node audit/author-repair-2026-09-13/parity-node.cjs .` | **751 of 751** inputs match |
| The findings script | `python -m pytest tools/tests/ -q` | **54 passed** |

The fixture counts in rows 24, 26 and 39 below were written when the file held 658. It holds 744,
and the rows carry the current numbers.

## Section 1, the four open items and the record

| # | The finding | Status | Where it stands at the freeze |
| --- | --- | --- | --- |
| 1 | "Nothing in the code or the documents holds any of them up" | **PARTIAL** | Every code defect the sentence contradicted is repaired, rows 3 to 31. The receipt is still not deployed, so the sentence remains right about one of the four. |
| 2 | `var RECEIPT_ENDPOINT = "";`, the receipt is unverified | **OPEN** | `index.html` still reads `var RECEIPT_ENDPOINT = "";`, with `PLACEHOLDER_MODE = "numeric"` below it. Both wait on the endpoint being deployed and four form questions being made optional. |
| 3 | Attempts are reported as players | **CLOSED** | `findings.py` reports received attempts, completed attempts, distinct codenames and facilitator-confirmed participants as four separate counts, reads only the first eligible attempt under each codename, and lists reattempts apart. |
| 4 | The new case is scored against the old case's hardcoded key | **CLOSED** | Every record is scored against the case file for the version it names. |
| 5 | Unsupported or mixed versions enter the readout | **CLOSED** | A version with no case file is refused by name, and records of different versions land in separate case sets. |
| 6 | The role field and affiliation chips cannot establish identity | **CLOSED** | A consented roster carries the participant, codename, consent and role. Roster codenames without an attempt and codenames two people claim are both reported. |
| 7 | The records cannot support learning gains or scored reasoning yet | **CLOSED**, moved from partial | The three strings that still read in the present tense are corrected. `review.html` says the educator scoring "has not been done yet", `README.md` and `cases/README.md` both say an independent educator "will score them against, blind" and that "none has been scored yet". `RUBRIC.md` and `READOUT-TEMPLATE.md` say the same. No result is claimed anywhere. |

## Section 2, the reviewer page

| # | The finding | Status | Where it stands at the freeze |
| --- | --- | --- | --- |
| 8 | "it reads better than a person writes on deadline" | **CLOSED** | Zero occurrences in the product. The two earlier design variants that carried it are retired to noindex pointer pages at `review.html`. |
| 9 | "Every figure against the ledger." and "Every direction word against the sign." | **CLOSED** | Zero occurrences on any served page. The author page's direction line prints only when every sentence is checked within scope and every direction word was tested, decided by the checker's own reader. Author fold parity at this head: **751 of 751**. |
| 10 | "Three columns are the whole ledger contract." | **CLOSED** | `review.html` says the three columns are the minimum a plain ledger needs, with the accepted-input rules linked. |
| 11 | "2 named a document that is not on file" | **CLOSED** | `evidence/EVIDENCE-NOTE.md` counts four defined classes instead, and `evidence/UNSUPPORTED-CLAIMS.md` carries the exact text behind every count. |
| 12 | The Excel workbook was on the future-work list while it existed | **CLOSED** | `review.html` lists the separate Excel workbook as something that exists. |
| 13 | The accessible description said the columns "come from any general ledger export" | **CLOSED** | Fixed on `review.html`, and the wording that survived in the two variants went with them. |

## Section 3, what the reason score measures

| # | The finding | Status | Where it stands at the freeze |
| --- | --- | --- | --- |
| 14 | Require a short explanation on the five assessment items and have an educator score it | **PARTIAL** | The three answers are required, posted and exported, and the lock refuses an answer that is too short or a stock non-answer, naming which part is short. `RUBRIC.md` scores each part 0, 1 or 2 with anchors and draws about one response in five for a second scorer. **Nothing has been scored**, which is why this is partial. |
| 15 | The rank documentation contradicted the executed scoring | **CLOSED** | The case guide, the governance note, both facilitator guides and the drill all say an agreeing reason adds fifty points and the rank reads total points. The scoring code is unchanged. |
| 16 | Item 3's evidence pre-solves the call | **CLOSED** | The reading moved into the reveal on all five lines. The drill loads `brightwater-v6`. |
| 17 | The video's "On a keyed exercise you can measure that" | **CLOSED** | The script now names the narrower thing that can be measured and gives the real memo its own sentence saying there is no key. |

## Section 4, the checker contract and the four counterexamples

Every probe uses the review's own ledger: account 6100, Rent expense, prior 100,000, current 130,000.

| # | The probe or finding | Status | Result at the freeze |
| --- | --- | --- | --- |
| 18 | P05 "Rent expense increased by $30,000 and doubled." | **CLOSED** | **not checked**, in both. The multiplier is an unparsed span. |
| 19 | P13 "Rent expense remained at $130,000." | **CLOSED** | **failed**, in both. A no-change claim on a line that moved. |
| 20 | P23 "Rent expense rose $30,000, or one and a half percent." | **CLOSED** | **not checked**, in both. |
| 21 | P25 "Rent expense rose $30,000 and increased by ٣٠٠٠٠." | **CLOSED** | **not checked** in both, with no exception thrown. |
| 22 | "Anything numeric the accepted grammar cannot read is recorded rather than dropped" | **CLOSED** | Rewritten as contract 1b and then made true. A sentence clears only when nothing risky is left once its claims are read, against a risk lexicon that holds an otherwise clearing sentence at needs review and names the word. |
| 23 | T32 and T43 were labelled as controls, preserving the misunderstanding | **CLOSED** | Both assert failed. |
| 24 | Fix the classes with mutations, not three more examples | **CLOSED** | Of the audit's 175 adversarial probes, 48 cleared falsely before the repair and **0** clear now, with **0** other misses, rerun at this head. The fixture file went from 59 to **744**: the review's 40 probes, 113 mutations across six classes, the audit's 175 probes, 159 clearance-class mutations, 111 residual-class fixtures, 86 checker-residual fixtures and the end-to-end samples. Refused and accepted cases are both asserted. |
| 25 | Prompt 1's drafts do not pass through their own reader | **CLOSED** | "prior" and "current" in front of a figure are read as roles. The three retained Prompt 1 drafts stand at **14 of 17** sentences checked within scope: Halyard 7 of 8, Brightwater 3 of 4, Kestrel 4 of 5. The one left in each is the closing line, which names no account. |
| 26 | The parity claim, the differing fixture files, the P25 crash | **CLOSED** | The two fixture files are identical once line endings are normalized, and a test asserts that identity. Parity at this head is **746 passed**: all **744** fixtures on all eleven fields, the file identity and the lexicon. On the audit's eight input sets, **513 of 513** inputs agree on all eleven fields. The claim is stated as agreement on every compared field, not as identical files. |
| 27 | Remove the universal input promises | **CLOSED** | "Paste any ledger and any drafted commentary", "Anything in between", "any ledger and memo" and "any general ledger export" return zero hits across every page and document in the product. |

## Section 5, what a controller encounters on the author page

| # | The finding | Status | Where it stands at the freeze |
| --- | --- | --- | --- |
| 28 | Defect A, an unresolved checker result becomes a clean author suggestion | **CLOSED** | A call is suggested only on checked within scope or failed. Needs review and not checked get no suggestion and the card says the call is the author's. Fold parity against the checker at this head: **751 of 751**. |
| 29 | Defect B, saving after an input edit uses stale figures | **CLOSED** | A read is stamped with the ledger, the memo, both floors, the rule and the zero-prior policy, and any change afterwards disables Save and Preview with two notices. Rereading marks each changed line and holds the save until the key is confirmed. |
| 30 | Defect C, an unbound sentence gets no card but the save completes | **CLOSED** | An unbound sentence comes back as an open item with the checker's status and reasons, and leaving it out with no written reason is refused. |
| 31 | The custom-case drill hardcodes "[case name] is a made-up company" | **CLOSED** | The case section asks where the figures come from with nothing preselected, a real close also needs the permission line, and the drill introduction follows the choice. |
| 32 | "Open a saved case" and restoring the editable fields | **DEFERRED** | Ruled on 13 September 2026 to come after the freeze, and not counted as a defect. The saved file already carries everything the control would read back. |

## Section 6, what the three-ledger evidence establishes

| # | The finding | Status | Where it stands at the freeze |
| --- | --- | --- | --- |
| 33 | Label Halyard as the retained development-session run | **CLOSED** | `evidence/EVIDENCE-NOTE.md` says so, and records that the Halyard blind draft names a case fact the ledger block did not contain. |
| 34 | The missed unsupported exclusion in Brightwater | **CLOSED** | Counted as one cause ruled out, with the reasoning recorded. |
| 35 | Distinguish the classes and count the claims with their exact text | **CLOSED** | Four classes with a written counting rule, and the exact text behind every count. |
| 36 | Do not describe the seven Halyard checker failures as numerical mistakes | **CLOSED** | The note says none of them is a numerical mistake and explains what the checker bound. |
| 37 | "so a reviewer cannot predict which memo carries invented causes" | **CLOSED** | Not in the write-up body. The sentence now says a cautious memo still needs its explanations checked. |
| 38 | Repeat the three paired drafts in clean contexts, with a second reader | **OPEN** | No new runs exist and the classification is still one reader's. `UNSUPPORTED-CLAIMS.md` says so and lists the items most likely to move. |

## Section 7, the five weaknesses

| # | The finding | Status | Where it stands at the freeze |
| --- | --- | --- | --- |
| 39 | Correct the stale fixture count wherever it appears | **CLOSED**, moved from partial | The product and the application copy of record both read **744 fixtures, 746 browser checks, 746 parity tests and 1,569 command-line tests**. The reviewer page's 724, which was the count on the night of 13 September, is corrected, and no stale count survives the sweep. |
| 40 | Time one complete recording with the real screen movements | **OPEN** | No recording exists. The script is a word count and says so. |
| 41 | An observed practitioner record | **OPEN** | None exists. |

**The five headline weaknesses at this head.** Rank 1, false mechanical clearance, is closed on
every class the review and the audit demonstrated. Rank 3, the findings miscounting people and
mis-scoring cases, is closed in the code and waits only on the educator. Rank 4, the author
workflow manufacturing a misleading training case, is closed. Ranks 2 and 5, the observed
practitioner outcome and the evidence reruns, are untouched, because both need people rather than
commits.

**Source.** The finding-by-finding grading is the fourth review packet of 14 September 2026,
section 2, held in the application folder. Every row above was read again against the freeze head
and the status, the counts and the file references are this repository's, not the packet's.
