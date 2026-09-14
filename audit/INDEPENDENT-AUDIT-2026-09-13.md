# Independent adversarial audit of Second Pass, 13 September 2026

Lane A1, written at 10:00 PM EDT on 13 September 2026. I built none of this. Every result below was run,
not read, unless a row says otherwise. All participant rows, codenames and memos in the runs are synthetic
and are not participant evidence. Nothing was posted or pushed.

**Heads tested.** Code behaviour was tested on `git archive` snapshots of the committed heads, so the
sweep lane's uncommitted edits could not leak into a result:

| Repository | Commit |
| --- | --- |
| beat-the-machine | `71d457b5f820a833862cd5793f3c2e7c900d3c7e` |
| second-pass | `fe8cd49de7491550c4aaa6a87b586cc8ef459cbd` |

Public copy was re-read at 9:58 PM EDT. The committed heads had not moved, but 20 files in beat-the-machine
and 3 in second-pass carried uncommitted edits by lanes S1 and P1. Where a claim below differs in that
working tree, the row says so, and those rows should be re-verified at the freeze. The pre-picks flow and
`tools/findings.py` changed during the audit, so re-verify both at the freeze. The "Open a saved case"
control is deferred by ruling and is not counted as a defect. The live GitHub Pages site runs the old
build and was not audited.

## Verdict

The repairs the third review asked for are real, and they hold on its own inputs. All 40 new probes and
all 24 prior probes now return the required status. The command line matches the browser on every
compared field. The stale save, the unresolved-to-clean suggestion and the unbound sentence are closed in
a real browser, and findings scores each record against its own case version. The false-clearance class
is still open, though, one step to the side of every repaired example. The mutations the build added
change word order and hyphenation, but they reuse the words the fix already listed. Of 175 new probes,
48 came back "checked within scope" where the published contract, or the plain meaning of a green
result, requires otherwise, and both implementations agree on every one:

- "Rent expense rose 30,000 euros."
- "Rent expense changed by $-30,000." (the ledger rose)
- "Consulting revenue changed by +$60,000." (the ledger fell)
- "Rent expense was stable at $130,000." (the ledger moved 30 percent)
- "Rent expense rose $30,000, or 30 percent, year over year." (a monthly ledger)

Four of these, run together on the author page, came back as suggested stand keys under "Every figure
recomputes." The application copy still says a sentence clears "only when every quantity in it is accounted for." The
educator scoring sheet writes participant text into a spreadsheet unneutralised. **Not ready for a
practitioner validation on the claim as written. It is one focused repair away, and the repair is to
narrow the grammar's clearance, not to add more listed words.**

## The third review's findings, at the tested heads

41 findings: **25 CLOSED, 11 PARTIAL, 4 OPEN**, and one deferred by ruling. The outputs named are in
`audit/independent-2026-09-13/outputs/`.

| # | Review finding (section) | Status | Proof, observed at the tested head |
| --- | --- | --- | --- |
| 1 | "Nothing in the code or the documents holds any of them up" (1) | PARTIAL | The code defects it contradicted are repaired (rows 3 to 31). The receipt is still not live (row 2). |
| 2 | `var RECEIPT_ENDPOINT = "";`, receipt unverified (1) | OPEN | `index.html:578` still reads `var RECEIPT_ENDPOINT = "";`. `PLACEHOLDER_MODE = "numeric"` is at `:2504`. It waits on deployment. |
| 3 | Attempts reported as players (1) | CLOSED | Replaying `same-person-two-attempts.csv` with `synthetic_check=True` gives `n_codenames: 1` and `repeat_runs: ["Synthetic same participant (attempt 2, audit-b)"]`. The exact replay with defaults excludes both rows as synthetic. `findings/findings-probes.json` |
| 4 | Kestrel scored against Halyard's key (1) | CLOSED | `kestrel-perfect.csv` with `synthetic_check=True` gives `score: 12, answered: 12` against `kestrel-v1` and no disagreements. |
| 5 | Unsupported or mixed versions (1) | CLOSED | `brightwater-v9` is refused with "unsupported case version brightwater-v9: there is no cases/brightwater-v9.json". `halyard-v7` is refused. v5 and v6 records land in separate sets. |
| 6 | Role field and chips cannot establish identity (1) | CLOSED | `--roster` reads participant, codename, consent and role. A ghost codename is counted in `roster_codenames_without_attempt: 1`, and a codename two people claim is listed in `codename_conflicts`. |
| 7 | Records cannot support learning gains or scored reasoning yet (1) | PARTIAL | Readout wording is narrowed. Copy still states educator scoring in the present tense where none has happened (new defect D9). |
| 8 | "it reads better than a person writes on deadline" (2) | PARTIAL | Gone from `review.html`. Still at `review-b.html:311` at the tested head, a page served publicly with no noindex while `robots.txt` says "Nothing is disallowed". The S1 working tree removes it, uncommitted. |
| 9 | "Every figure against the ledger." / "Every direction word against the sign." (2) | PARTIAL | Gone from `review.html`. Still at `review-b.html:318-319` and `review-a.html:136,194` at the tested head. `author.html:916` prints "Every direction word agrees with the sign." on a memo carrying D1 to D4 clearances. |
| 10 | "Three columns are the whole ledger contract." (2) | PARTIAL | `review.html:479` now says "the minimum a plain ledger needs". `review-b.html:375,392` still say "are the whole input, and they come from any general ledger export". |
| 11 | "2 named a document that is not on file" (2) | CLOSED | `evidence/EVIDENCE-NOTE.md:23` retires the unit and counts four classes. |
| 12 | Excel template on the future-work list (2) | CLOSED | `review.html:470` lists "a separate Excel workbook" as existing. |
| 13 | Accessible description "come from any general ledger export" (2) | PARTIAL | Fixed in `review.html:479,496`. Present at `review-b.html:375,392,405` ("Any general ledger"). |
| 14 | Chip score is a construct limit; add short explanations and educator scoring (3) | PARTIAL | Three required answers are posted and exported (browser: record `writtenExplanation` on all five v6 items). Nothing has been scored. The lock accepts "a b", "..." and "none" (D8). |
| 15 | Rank documentation contradicts scoring (3) | CLOSED | `reason-and-rank.json`: Halyard keyed 2,625 Partner, wrong 1,925 Senior. `cases/README.md:36-41` and `README.md:818-819` now say the same. |
| 16 | Item 3 evidence pre-solves the call (3) | CLOSED | "It lists no plan that started in June" occurs 0 times in `brightwater-v6.json` and once in v5. The drill loads v6 (`index.html:652`). |
| 17 | Video "On a keyed exercise you can measure that" (3) | CLOSED | `SCRIPT-rev10.md` Q4 now names call agreement and educator scoring. |
| 18 | P05 "increased by $30,000 and doubled." (4) | CLOSED | not checked, in both implementations. `new-40-summary.json` |
| 19 | P13 "remained at $130,000." (4) | CLOSED | failed, in both. Its neighbours are open (D3). |
| 20 | P23 "or one and a half percent." (4) | CLOSED | not checked, in both. |
| 21 | P25 Arabic-Indic digits: browser cleared, command line crashed (4) | CLOSED | not checked, in both, with no exception. |
| 22 | Clause "Anything numeric the grammar cannot read is recorded rather than dropped" (4) | PARTIAL | Rewritten as 1b. Quantities are still dropped with no unparsed span: currency words (D1), signs (D2), and "or 三十 percent", "or trente pour cent" and "or XXX percent" (D5). |
| 23 | T32 and T43 labelled as controls (4) | CLOSED | Both now assert failed. The suite passes 213 of 213. |
| 24 | Fix the classes with mutations, not three more examples (4) | PARTIAL | 113 mutations were added (`CHECKER.md:327-334`). The STILL set varies only listed words. 48 of A1's 175 new probes clear (D1 to D5, D10). |
| 25 | Prompt 1 drafts pass through their own reader (4) | CLOSED | Retained drafts: halyard 7 of 8, brightwater 3 of 4, kestrel 4 of 5 checked, so 14 of 17, down from 0. Each "no source on file" stays a queue item. `six-drafts-browser.json` |
| 26 | Parity claim, fixture files differ, P25 crash (4) | CLOSED | The fixture files are identical after line endings. All 245 audit inputs (64 replayed, 6 drafts, 175 new) match on status, role, stats, queue kinds, queue, finding, survivors, csv, tsv, json and prompt. |
| 27 | Universal input promises (4) | PARTIAL | Gone from `checker.html` and `CHECKER.md`. Remaining at the tested head: `index.html:1463` "the four mechanical checks run on any ledger and memo in the checker on this site", `FACILITATOR-GUIDE.md:123` "on any ledger and memo pasted into it", and `review-b.html:405`. The working tree removes the `index.html` line, uncommitted. |
| 28 | Author defect A: unresolved becomes a clean suggestion (5) | CLOSED | The review case reads sentence 1 **needs review**, card key "" and basis [], with no praise line. It holds only while the checker's status is right (D6). |
| 29 | Author defect B: stale save (5) | CLOSED | Browser: typing through CDP `Input.insertText`, Ctrl+Z then Ctrl+Y, a paste-shaped `insertText`, the rule control and a typed dollar floor each disabled Save. A direct `__SPA.save()` downloaded 0 files each time. A value set with no event also refused. The clean save wrote `100000 130000`. The author page has no column-mapping control. |
| 30 | Author defect C: unbound sentence gets no card (5) | CLOSED | The covenant sentence is an open item (`res: "open"`, needs review) and holds the save until it is excluded with a reason. |
| 31 | Drill says "made-up company" whatever the origin (5) | CLOSED, read in code | `index.html:1631-1635` branches on synthetic, permitted and unrecorded. The saved `origin` was verified in the browser. The intro was not driven in the browser. |
| 32 | "Open a saved case" (5, preference) | DEFERRED | Ruled after the freeze. Not counted. |
| 33 | Label Halyard as the development-session run (6) | CLOSED | `EVIDENCE-NOTE.md:9` |
| 34 | Missed Brightwater unsupported exclusion (6) | CLOSED | `EVIDENCE-NOTE.md:20`: Brightwater fresh context, causes ruled out 1. |
| 35 | Count claims by class with exact text (6) | CLOSED | `EVIDENCE-NOTE.md:15-23` |
| 36 | Seven Halyard failures are not numerical mistakes (6) | CLOSED | `EVIDENCE-NOTE.md:35` "none of them is a numerical mis[take]" |
| 37 | "cannot predict which memo carries invented causes", "in all three was remove the summary paragraph" (6) | CLOSED | Neither is in the `WRITEUP-rev11` body. |
| 38 | Repeat the paired drafts in clean contexts, with a second reader (6) | OPEN | No new runs or second-reader classification were found. |
| 39 | Stale fixture count (7) | PARTIAL | `WRITEUP-rev11` holds the placeholder "[FIXTURE COUNT FROM R1]". `RELEASE-NOTES.md:14` "59 fixtures, 59 pass ... 138 pass" and `:216` "59 fixtures" remain in the working tree at 9:58 PM. The count is 212 fixtures, 213 checks, and 504 command-line tests. |
| 40 | Time one complete recording under 4:00 (7) | OPEN | No recording in the evidence. |
| 41 | Observed practitioner record (7) | OPEN | None exists. |

**Replays not tied to one finding.** The six drafts reproduce the review's blind-draft sentence statuses
exactly. The halyard-blind queue is 54 against the review's 55. The supplied suites at the tested heads
report `node tests/run-checker-tests.cjs` 213 passed, 0 failed. `python -m pytest tests/ -q` in second-pass
reports 504 passed with `BEAT_THE_MACHINE` set, or 291 passed and 213 skipped without it (D17).
`tools/tests` reports 31 passed.

## New defects, ranked by severity

Requirements cite `CHECKER.md` at `71d457b`. "Both" means `checker.html` and `second_pass/checker.py`
gave the same output on every compared field. The full inputs and outputs are in `outputs/a1-graded.json`
and `outputs/a1-sizing-graded.json`.

### High

**D1. Currency words clear as dollars. 9 false clearances, in both.**

- Inputs, all on ledger 6100 Rent expense 100,000 to 130,000:
  - "Rent expense rose 30,000 euros." (B001)
  - "30,000 pounds", "30,000 yen", "30,000 rupees", "30,000 francs" (B002, B003, B004, B009)
  - "30,000 pesos" (A114)
  - "30,000 Canadian dollars", "30,000 Australian dollars" (B005, B006)
  - "Rent expense rose $30,000 in Canadian currency." (B010)
- Observed: **checked within scope**, role `30,000=dollars/absolute movement`, empty queue.
- Required: **not checked**. Contract 1b makes "a **currency that is not the dollar**" an unparsed span, and `CHECKER.md:369` says "The page reads one currency".
- Where: `checker.html:893-894` (`FOREIGN_BEFORE` and `FOREIGN_AFTER` list symbols and ISO codes only) and `second_pass/checker.py:604-605`. The codes and symbols themselves are held correctly (A108 to A113, B007, B008).

**D2. A sign written any way but a leading minus or enclosing parentheses is dropped, and the magnitude
clears. 10 false clearances, in both.**

- Inputs, on a line that rose:
  - "Rent expense changed by $-30,000." (A068)
  - "changed by 30,000-." (A069)
  - "changed by —30,000." with an em dash (A127)
  - "rose 30,000 CR.", "changed by 30,000 Cr.", "changed by $30,000 credit." (A065, B018, B019)
- Inputs, on 4300 Consulting revenue 240,000 to 180,000 (it fell):
  - "Consulting revenue changed by +60,000." (A073)
  - "changed by +$60,000.", "changed by $+60,000.", "changed by +25 percent." (B013, B014, B015)
- Observed: **checked within scope**, the figure read unsigned. The explanation says "No direction word was tested."
- Required: **failed**. Contract step 1 says "A figure is negative when a minus sign ... says so". Step 5 says "a figure the memo writes with its own sign is compared as written and a sign clash is a failure that names both sides". `-$30,000`, `−$30,000` and `–$30,000` do fail (A067, A125, A126).
- Where: `hasSign()` at `checker.html:1137` and `assets/second-pass-core.js:648` accepts only `^\s*-` or a closed pair of parentheses. Python has the same at `second_pass/checker.py:959`.

**D3. No-change claims outside the enumerated word list clear on a line that moved 30 percent.
11 false clearances, in both.**

- Inputs:
  - "Rent expense was stable at $130,000." (B020)
  - "was broadly stable at", "was level at", "was consistent with May at", "was in line with May at" (A020 to A023)
  - "was the same as May at", "was static at", "was on par with May at", "was equal to May at", "matched May at" (B023, B025, B027, B028, B029)
  - "Consulting revenue was stable at $180,000." (A033)
- Observed: **checked within scope**, `$130,000=dollars/current balance`, no direction tested.
- Required: failed or needs review. This is P13's class. The review asked to "add mutations around those classes", and the green result's own definition is "every quantitative expression in the sentence was accounted for".
- The contract enumerates its words (`CHECKER.md:199-205`), so this is contract-silent, and it is the same false assurance the review named. STILL01 to STILL28 vary only listed words ("remained", "stayed", "held", "unchanged", "flat", "constant").
- Where: `STILLW` and `FLATW` at `checker.html:1680-1688`.

**D4. Period-mismatch claims clear against a single month-over-month pair. 12 false clearances, in both.**

- Inputs:
  - "Rent expense rose $30,000, or 30 percent, year over year." (A082)
  - "rose $30,000 compared with June 2025." (A083)
  - "over the last twelve months." (A084)
  - "Year to date, rent expense rose $30,000." (A085)
  - "rose $30,000 against budget." (A087)
  - "Consulting revenue fell 25 percent from last year." (A088)
  - "versus the prior year", "on a trailing twelve month basis", "since December", "compared with last June", "or 30 percent, over two years", "in the first half" (B031 to B036)
- Observed: **checked within scope**.
- Required: needs review or not checked. The contract says "only two columns are ever compared" and "One currency, one pair of periods". A figure that ties to May-to-June is not a year-over-year figure.
- T48 ("against $18,000 in June 2025") fails only on its stale $18,000 figure, and asserts that the year is not read as a figure. The same period claim with no second figure clears. The grammar is silent on period words, so this is contract-silent.

**D5, the application claim this contradicts.** `WRITEUP-rev11.md:45`: "A sentence clears only when
every quantity in it is accounted for, whatever it cannot read stays with the reviewer, and no later step
moves a status upward."

- `LINKEDIN-POST-rev2.md:23` says it "leaves whatever it cannot read with the reviewer instead of passing it".
- `SCRIPT-rev10.md` Q2 says "whatever it can't read stays with the reviewer".
- `CHECKER.md:260-262` says the queue carries "every unsupported numeric form".
- D1, D2 and the unread quantities below are direct counterexamples: "Rent expense rose $30,000, or 三十 percent.", "or trente pour cent." and "or XXX percent." (A119 to A121) each return **checked within scope** with no unparsed span and an empty queue, in both. The requirement for those three is not checked, under 1b's "every other piece of quantitative language".

**D6. Checker clearances become author-suggested stand keys and praise lines. Browser.**

- Input: ledger 6100 and 6200 with the memo "1. Rent expense rose 30,000 euros. 2. Insurance expense changed by $-45,000. 3. Rent expense was stable at $130,000. 4. Insurance expense rose $45,000, or 90 percent, year over year."
- Observed on `author.html`: all four sentences **checked within scope**. All four cards suggest `key: "stand"`, `type: "clean line"` and `basis: ["the figure and reason hold"]`. The readout prints "Every figure recomputes."
- Required: no stand suggestion on any of them. The review's rank 4 weakness, a misleading training case, returns through the reader rather than the fold.
- Where: `author.html:916` and `:1157`. Output: `a1-browser-author-drill.json` `author.falseClearanceMemo`.

**D7. Formula injection into the educator's scoring sheet and key.**

- Input: the three explanation answers on v6 line 1 are `=HYPERLINK("http://example.invalid","click")`, `+1+1` and `-2+3`. Line 2 carries `@SUM(1,1)` and `=1+1`.
- Observed:
  - The drill enables Lock it in, stores the strings as typed, and they survive a reload (browser, `drill.lock[0].afterReload`).
  - `write_scoring_sheet()` writes them raw. 14 non-empty cells in `scoring-sheet-injection.csv` begin with `=`, `+`, `-` or `@`.
  - The key file writes the codename column the same way. That was read in the code; no formula codename was run.
- Required: the neutralisation `CHECKER.md:424` promises for the checker CSV, a leading apostrophe on any cell starting `=`, `+`, `-` or `@`.
- Where: `tools/findings.py:1434-1465`. The drill's `explainClean` (`index.html:1874`) strips only `|` and line breaks.

### Medium

**D8. The explanation lock accepts non-answers, and findings erases some of them.**

- Observed in the browser: Lock it in is enabled by "a b", by "...", and by "none", "None." and "n/a".
- `parse_explanations()` on `Evidence: none | Period: None. | Action: n/a` returns `{1: {'action': 'n/a'}}`, so two answers the page accepted become "no answer" in the scoring sheet.
- The whitespace-only, Enter-key and forced-click bypasses were blocked.
- Where: `index.html:1873-1879` (`EXPLAIN_MIN = 3`) and `tools/findings.py:178,600`.

**D9. Educator scoring is described in the present tense before any has happened.**

- `review.html:464`: "a short written explanation is scored blind by an independent educator against a rubric".
- `README.md:838`: "Those explanations are scored blind by an independent educator".
- `WRITEUP-rev11.md:49`: "an independent educator scores it blind against a rubric".
- `SCRIPT-rev10.md:107`: "an educator scores each written explanation blind".
- Required: future or conditional wording until a scored sheet exists.

**D10. A comparative claim about a second named account clears. 2 false clearances, in both.**

- Inputs: "Rent expense rose $30,000; so did Insurance expense." and "Rent expense rose $30,000, the same increase as Insurance expense." (A094, A096). 6200 moved $45,000.
- Observed: **checked within scope**. 6200 stays in the queue as a silent line, which limits the harm.
- Required: needs review or failed.
- Related: "Rent expense rose $30,000 and hardly moved." (A104) also clears.

**D11. "respectively" fails a true sentence.**

- Input: "Rent expense and Insurance expense rose $30,000 and $45,000 respectively." (A093)
- Observed: **failed**, in both. The finding reads "memo says $30,000 as the absolute movement; the absolute movement on 6200 Insurance expense is $45,000".
- Required: **needs review**. Contract 2 says "a figure whose clause names ... more than one [account] is a binding conflict and is held at needs review".

**D12. A repeated attempt ID with different content is discarded as a resend.**

- Input: two rows, attempt `dup-1`. The first row in the file is timestamped 9:40, with a different call on line 1 and different explanations. The second is timestamped 9:02.
- Observed: `duplicate_sends: ["Twin Lark (attempt dup-1 sent again)"]`. The file-order row was kept (`score: 13`), and nothing says the contents differed.
- Required: compare the contents and report a conflict, or keep by timestamp and say so.
- Where: `tools/findings.py:1057-1063`.

**D13. A v6 record missing required explanations is reported complete with no flag.**

- Input: a v6 row with line 3's answers blank, and a v6 row with no Round2 explanations at all.
- Observed: `completed: true`, `disagreements: []`, and `n_explanation_items` is 4 and 0.
- Required: flag a missing required explanation, since the page cannot post one.
- Where: `completion_of()` at `tools/findings.py:920-945`.

**D14. Stale version and count claims at the tested head.**

- `review.html:326` and `:550` show the assessment case as `brightwater-v5`, while the drill loads v6 (`index.html:652`).
- `CHECKER.md:477-479` says v5 is among "the same files the game reads".
- `CHECKER.md:554`, `README.md:14`, and `FACILITATOR-GUIDE.md:4` and `:276` also name v5.
- `FACILITATOR-GUIDE.md:60` still has "leaderboard".
- `RELEASE-NOTES.md:14,216` has "59 fixtures".
- Every one of these is still present in the 9:58 PM working tree.

### Low

**D15. Codename normalisation.** "Zoë" in NFC (`Zo\xc3\xab`) and in NFD (`Zoe\xcc\x88`) count as two
codenames, both first attempts. The NFD form arose by accident while authoring and was confirmed byte by
byte. `norm()` at `tools/findings.py:253-261` does not apply `unicodedata.normalize`.

**D16. Exclusion rules are over-broad and inconsistent.**

- "Test Pilot" is dropped as a test codename, while the fullwidth "Ｔｅｓｔ Pilot" is kept.
- A real row is dropped whole when an explanation contains "synthetic test only", or when its attempt ID begins `audit-`.
- A refused unknown version still counts in `n_attempts_completed`.
- Where: `tools/findings.py:182-191` and `:788-806`.

**D17. The divergence note's test count.** `CONTRACT-DIVERGENCE.md` says `python -m pytest tests/ -q` gave
"504 passed". A standalone second-pass checkout gives 291 passed and 213 skipped. The test docstring says
so honestly, but the note does not name the `BEAT_THE_MACHINE` requirement.

**D18. Sample origin persists.** "Load the Kestrel sample" presses "Made up for this drill"
(`author.html:1322`). After both panes were replaced with other figures, the origin still read `synthetic`.

**D19. Explanation boxes announce nothing.** Each box has a `<label for>`, but no `aria-describedby`, no
`aria-required`, and no live region saying why Lock it in is disabled. The browser probe found
`describedby: null` and `liveRegions: 0` (`index.html:1880-1890`). The author page's fields are all
labelled, and its four messages are `role="status"` with `aria-live="polite"`.

## Preferences, not defects

- **Approximations fail rather than hold.** "about $32,000" and "roughly $29,000" fail. That is safe, but the finding names a wrong figure for what the writer called approximate.
- **Scale words fail silently.** "$30 grand", "$30 thou" and "$0.06MM" read as $30 and $0.06 and fail, with no unparsed span. "3,00,000" reads as "00,000". Contract 1b would record the span. The status is safe.
- **Ranges fail twice.** "between $25,000 and $35,000" fails twice rather than holding once as a range.
- **The chip score is still a compatibility check.** `cases/README.md:36-45` now says so and keeps the three-part rubric with a person, which is the honest framing.
- **The audit folder is about 15 MB.** Most of it is both implementations' full exports for the 60,000-character probe. Do not publish it to Pages if size matters.

Parity differences found: **none**, on 245 inputs and 11 compared fields.

## Reproduction

From `audit/independent-2026-09-13/`, with Node 24, Python 3.9 and pytest. Headless Chrome was driven
over CDP with a throwaway profile. `runners/cdp.cjs` is lane R3's driver, copied unchanged, and every step
run with it is A1's own.

```
git -C <beat-the-machine> archive 71d457b | tar -x -C <G>
git -C <second-pass> archive fe8cd49 | tar -x -C <T>
node <G>/tests/run-checker-tests.cjs
(cd <T> && BEAT_THE_MACHINE=<G> python -m pytest tests/ -q)
(cd <G>/tools && python -m pytest tests -q)
node runners/make-new-probes.cjs && node runners/make-sizing-probes.cjs
node runners/run-browser.cjs <G> inputs/<set>.json outputs/<set>-browser.json
python runners/run-python.py <T> inputs/<set>.json outputs/<set>-python.json
python runners/compare.py outputs/<set>-browser.json outputs/<set>-python.json outputs/<set>-parity.json
node runners/grade-probes.cjs inputs/a1-probes.json outputs/a1-browser.json outputs/a1-python.json outputs/a1-parity.json outputs/a1-graded.json
node runners/reason-and-rank.cjs <G> outputs/reason-and-rank.json
python runners/findings-probes.py <G> .
node runners/a1-browser.cjs <G> outputs/a1-browser-author-drill.json
```

`<set>` is `new-40-probes`, `prior-24-probes`, `six-drafts-as-fixtures`, `a1-probes` or
`a1-sizing-probes`. Their outputs are `new-40`, `prior-24`, `six-drafts`, `a1` and `a1-sizing`.
`inputs/` keeps the review's 24 and 40 probe inputs with the statuses the review observed, the six draft
inputs, both review CSVs, the review's downloaded author file and its command-line, findings and rank
outputs. `SHA256SUMS.json` fingerprints every file in the folder.
