# The findings script and the written-answer lock, 13 September 2026

Lane F2's record, written by the claims pass at 1:10 AM EDT on 14 September 2026 from the runs and
the commits F2 left behind, because that lane ran out of tokens before it wrote one. Every line
below was checked against a file, a run in `audit/findings-and-lock-2026-09-13/` or a commit read
out of git. Every participant row, codename and written answer in the runs is synthetic and none of
it is participant evidence. Nothing was posted or pushed.

**What this closes.** The independent adversarial audit of 13 September
(`audit/INDEPENDENT-AUDIT-2026-09-13.md`) found seven defects in the findings script and the drill's
explanation step: D7 formula injection, D8 a lock that accepted non-answers, D12 a reused attempt id
discarded as a resend, D13 a v6 record reported complete with no explanations, D15 codename
normalisation, D16 over-broad exclusions, D18 a sample origin that outlived its sample, and D19
boxes that announced nothing. The usability pass by eye added four visual defects in the same two
pages.

**Commits.**

| Commit | Time | What it carries |
| --- | --- | --- |
| `5a61807` | 11:40 PM, 13 Sep | The lock's minimum and its refusals, the record's prompts, and four visual fixes in `index.html` |
| `4efa859` | 11:40 PM, 13 Sep | `tools/findings.py`: the spreadsheet-safe sheet, the minimum, conflicts, codename normalisation and the narrowed exclusions, with 17 new tests |
| `986db6e` | 11:40 PM, 13 Sep | `author.html`: the sample's origin is taken back when its ledger goes, and the prefilled boxes read whole |
| `c3be5a8` | 11:40 PM, 13 Sep | The audit's own runners follow the current drill without changing what they expect |
| `c76f5b8` | 12:01 AM, 14 Sep | The rubric, the readout and both facilitator guides say the educator scoring will happen, and name the minimum, the conflicts and `brightwater-v6` |
| `8741e75` | 12:10 AM, 14 Sep | The runs behind all of it: the lock walk, the send read back, 60 screenshots, and the audit's runners before and after |

## 1. A written answer can no longer carry a formula into the educator's sheet

The audit typed `=HYPERLINK("http://example.invalid","click")`, `+1+1`, `-2+3`, `@SUM(1,1)` and
`=1+1` into the three explanation boxes on two assessment lines. The drill stored them as typed, and
`write_scoring_sheet()` wrote them raw: **14 non-empty cells in `scoring-sheet-injection.csv` began
with `=`, `+`, `-` or `@`**, which is what `CHECKER.md` promises never to write for the checker's own
CSV.

Every text cell in the scoring sheet and in the facilitator key now passes through `sheet_cell()`,
which puts a leading apostrophe in front of a cell opening with `=`, `+`, `-`, `@`, a tab or a line
break, or a full-width or small-form sign, and leaves the four numeric columns as numbers. Counted
in the before and after files under `audit/findings-and-lock-2026-09-13/`: **14 unsafe cells before,
0 after, and 14 cells now carrying the apostrophe**. The apostrophe is not part of what the player
wrote, and `RUBRIC.md` says so on the page an educator reads.

`SheetSafetyTest` in `tools/tests/test_findings.py` holds it: **4 tests**, covering the sheet, the
key, the numeric columns and a codename written as a formula.

## 2. The lock refuses a non-answer on every path there is

`lock-walk.cjs` plays Halyard's fourteen practice lines by clicking, then tries every way past the
lock on the first assessment line before answering it properly. **62 of 62 checks pass**
(`runs/lock-walk.json`, rerun at this head). The ways tried, each with `a b`, `...` or `none`:

| The way past | What happened |
| --- | --- |
| No basis chip | No call locked, no step taken, focus on the chip |
| Empty boxes | No call locked, focus on the first empty box |
| Whitespace only | No call locked |
| Punctuation, with the Enter key on the page | No call locked, and the error names punctuation |
| `a b`, with Enter on the lock button | No call locked, and the error names the minimum |
| `a b`, with Space on the lock button | No call locked |
| `none`, `n/a` and kin, with a forced click on a button stripped of `aria-disabled` | No call locked, and the error says they do not count |
| Pasted text | No call locked |
| One short part in the middle | No call locked, only that box marked, focus on it |
| A reload in the middle of the item | The same item comes back with what was typed, still not ready |
| A state edit through the step hook | The line reopens with the call unlocked and the errors showing |
| A state edit jumping to the end screen | No end screen drawn |
| A state edit in the saved run, then a reload | The call comes back unlocked |

Every refusal names the missing part in the status line ("Not locked yet. Still needed: the decisive
evidence, why it matters for this period and the action or source request."), moves focus to the
first part that is short, marks that box `aria-invalid` and prints a visible error under it in
words. With three real answers the lock is ready, the call locks and the page moves on.

**The minimum, in one place.** Each part needs at least two words and eight letters or digits, and a
stock non-answer such as `none`, `n/a` or `same as above` does not count. The rule sits between the
`explain-minimum` markers in `index.html`, `tools/findings.py` applies the same rule to every record
it reads, and `tools/tests/explain-minimum.cjs` runs the page's own function against the shared
cases in `tools/tests/explanation-minimum.json`, so the two cannot drift.

**The findings keep a non-answer rather than erasing it.** The audit found `parse_explanations()`
turning `Evidence: none | Period: None. | Action: n/a` into a single answer, so two answers the page
had accepted disappeared. A run sent with `a b`, `...` and `none` on line 2 now comes back as
`completed: false` with the gap named part by part, evidence short, period no words and action a
stock non-answer, and the scoring sheet carries each answer as posted with `below_minimum` naming
the parts (`runs/payload-findings.txt`).

## 3. A reused attempt id with different content is a conflict, not a resend

Two rows carrying attempt `dup-1` and differing in their first call, its why and the round two
string were discarded as one send sent twice, and the file-order row was kept with no note that the
contents differed. Now they are **held out of every count until a person decides**:
`n_attempts_received: 0`, and a conflict naming the attempt id, both sheet rows and the three
columns they differ in. `--resolve-conflict ID=ROW` keeps the named sheet row. Rows that share an id
and match in every cell but the timestamp are still one send, kept once at its earliest time.
`ConflictTest`, 5 tests.

## 4. A `brightwater-v6` record is complete only with every written answer

The audit sent a v6 row with line 3 blank and a v6 row with no explanations at all, and both came
back `completed: true` with nothing flagged. Now both are **`completed: false`**, with
`explanation_gaps` naming the codename, the line and the reason: line 3 stock on all three parts for
the first, and fifteen parts marked `not posted` for the second. A `brightwater-v5` record carrying
explanations is still complete without them, because that version never asked.
`READOUT-TEMPLATE.md` states the rule in the completed attempts row.

## 5. Two spellings of one codename are one codename

`Zoe` with a diaeresis, written in NFC and in NFD, counted as two codenames, both first attempts.
`norm()` now applies NFC and case folding before comparing, so the six-row probe comes back as
**6 received attempts under 5 distinct codenames**, with the second spelling counted as a reattempt
rather than as a second person. `CodenameAndExclusionTest`, 4 tests.

## 6. An exclusion names the row it dropped and the rule that dropped it

The audit found three over-broad exclusions, each of which silently dropped a real row. All three
are narrowed, and every exclusion now prints its sheet row and its rule.

| Probe | Before | After |
| --- | --- | --- |
| A real codename `Test Pilot` | dropped as a test codename | kept: a test codename is on the known list or made only of test words |
| A player who writes "the memo reads like a synthetic test only" | the whole row dropped | kept: a synthetic row opens its codename with `Synthetic` or carries the marker as a whole cell or Words line |
| An attempt id beginning `audit-` | the whole row dropped | kept: an attempt id alone excludes nothing |

A refused version still enters no count, and a refusal prints its reason: "unsupported case version
brightwater-v9: there is no cases/brightwater-v9.json, so no key exists to score it against".

## 7. The sample's origin does not outlive the sample

Loading the Kestrel sample on `author.html` presses **Made up for this drill**, which is true of the
sample. The audit replaced both panes with its own figures and the origin still read `synthetic`,
which would have shipped a made-up label on a real close. Now the answer belongs to the sample only:
once the ledger is no longer the sample's the choice is unset and the page asks again, Clear always
unsets it and empties any field the sample filled that was not typed over, and a choice the author
made by hand is left alone.

## 8. The three boxes announce themselves

Each box carries a `<label for>`, `aria-required`, a visible hint tied by `aria-describedby`, and
its error tied the same way when it has one. The lock carries `aria-disabled` and points at a
`role="status"` line with `aria-live="polite"` that says what is still needed, which is the one live
region on that screen. Read back in the browser at `a11y` in
`rerun-a1/a1-browser-author-drill.json`.

**A note for anyone reading the lock from the outside.** The button is never `disabled` in the DOM;
it stays pressable so a keyboard and a screen reader can reach it and hear why. Readiness is
`aria-disabled`, and a runner that reads `button.disabled` reports an empty answer as unblocked.
`audit/author-repair-2026-09-13/walk-drill.cjs` did exactly that and was repaired by the claims pass
on 14 September: it reads `aria-disabled` now and proves each refusal by pressing the lock and
finding the step and the stored call unmoved.

## The visual defects fixed in the same commits

Found by eye by the usability pass, each one in `audit/USABILITY-BY-EYE-2026-09-13.md`:

- **The two-bar picture's month labels rendered at about 10.8 pixels on a 320 pixel phone**, because
  they were text inside a drawing that scaled with the card. They are page text now, at the page's
  14 pixel small size at every width.
- **The end screen printed "1 false flags".** Every count the drill prints now agrees with its noun.
- **The read screen widened to 1,320 pixels** while the header's own box is 1,048, so at 1,280 and
  1,600 its edges lined up with nothing else on the site. It is the header's box now.
- **The codename in the masthead sat 6 pixels from the band's edge** while the words above it sat at
  the gutter. It stays inside the gutter.
- On `author.html`, the case settings run one column on a phone, two from 600 and four from 900, so
  the period example and "Owes commentary" read whole, and a card's why, tell, facts on file and
  left-out reason grow to what they hold instead of stopping mid-sentence.

## What was run, and where it is

| Run | Result |
| --- | --- |
| `node audit/findings-and-lock-2026-09-13/lock-walk.cjs . <dir>` | **62 of 62**, no page error |
| `python tools/tests/test_findings.py` and `python -m pytest tools/tests -q` | **54 pass**, 17 of them new in `4efa859` |
| `node tools/tests/explain-minimum.cjs` | the page's own function against the shared cases |
| `python audit/findings-and-lock-2026-09-13/payload-findings.py <dir>` | the drill's own send read back by `findings.py`: complete with no gap, and cut short with three gaps named |
| `python audit/independent-2026-09-13/runners/findings-probes.py . <dir>` | every audit probe before and after, in `before/findings/` and `rerun-a1/outputs/findings/` |
| `node audit/independent-2026-09-13/runners/a1-browser.cjs . <out>` | the audit's own drill and author walk at this head |
| `node audit/author-repair-2026-09-13/walk-drill.cjs . halyard 1280 <out>` and `. kestrel 375 <out>` | intro to end with no error and no overflow, and the lock refusing an empty and a stock answer on all five assessment lines of both cases |
| Screenshots | **60**, six widths each of the read screen, the explanation step empty, refused and ready, the end screen's counts, the codename band, the two-bar chart, and the author page's case grid and card. All opened and looked at, with the measurements in `shots/measure.json` |

The three runners agree on the lock. `lock-walk.cjs` reports no call locked on every path,
`a1-browser.cjs` reports the lock not available on empty, whitespace, `a b`, `...` and the `none`
words, and `walk-drill.cjs` reports the same refusals on all five lines of two cases.

## Where the third review's 41 findings stand

The independent audit graded the third review into 41 findings and printed each one's status at the
heads it tested, `71d457b` and `fe8cd49`: 25 closed, 11 partial, 4 open and 1 deferred by ruling.
Re-verified at `c369dc7` by the fourth review packet, they stand at **32 closed, 4 partial, 4 open
and 1 deferred**. The claims pass closes two of those four partials in the commits beside this file,
finding 7, educator scoring described in the present tense on `review.html`, `README.md` and
`cases/README.md`, and finding 39, the stale fixture count in the application copy. The four open
ones are unchanged and each waits on a person or a deployment: the receipt endpoint, a clean-context
rerun of the drafting evidence with a second reader, a timed recording, and an observed practitioner
record.

## Still open after this lane

- **Nothing has been scored.** `RUBRIC.md` is the sheet an educator will score against, and the
  finding that asked for scored explanations stays partial until a scored sheet exists.
- **The receipt endpoint is still empty**, so a stored participant record is still unverified.
- **The lock's minimum is a floor against an empty box, not a judgment of quality.** An answer that
  clears it can still earn a 0, which is the rubric's own sentence.
