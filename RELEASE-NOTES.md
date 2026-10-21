# Second Pass, release 1.9.5

21 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.9.5, what changed since 1.9.4

Cut 21 October 2026 from the second round of tester feedback on the Mason form: six students on
1.9.3, clarity 4.0 and usefulness 4.3 on average. No answer key, basis key, case file, reason value
or record grammar changed, so the score, question 9's pre-filled record and
`tools/tester_record_parse.py` read a 1.9.5 run exactly as a 1.9.3 or 1.9.4 one. The product stamp
moves to `second-pass-drill 1.9.5`.

| What changed | Why | Where |
| --- | --- | --- |
| **Each call says what it means.** Under Let it stand, inside the same button, "The memo's explanation holds up." Under Flag it, "The memo's explanation has a problem." The intro carries one boxed sentence, "Your job. On each line, decide whether the memo's explanation holds up. Let it stand when the numbers match the ledger and something on file backs the reason. Flag it when either one has a problem." Tour tip 1 now ends "Your job is to decide whether its explanation holds up." and the call tip reads "Make your call here. Let it stand means the memo's explanation holds up. Flag it means the explanation has a problem." The calls' values and what they post are unchanged | A tester rated clarity 2: "I don't really understand the 'Let It Stand' or 'Flag It' options. I think it would be easier to simplify the wording to make it clearer for the audience." | `CALL_HINT`, `JOB_LINE`, `callCard()`, `intro()`, `TOUR_STEPS`, `.jobline` |
| **The tour no longer reads as stuck at 4 of 6.** Tip 4 is the one tip that waits for the tester: it opens the reason rows only once a call is made. Until 1.9.5 its Next button was drawn at 40 percent opacity, and the line saying the tour waits appeared only after Next was pressed, so a tester saw a faded button and nothing to do. Now the waiting line shows from the moment the tip opens, Next is never faded (pressed with no call, it moves focus to Let it stand), a half-second timer moves the tour on once a call is on the card even if the click path fails, the call handler moves the tour on even if drawing the reasons throws, and a tip whose part is missing stays up as a bottom sheet with Next and Skip tour instead of hiding | A tester: "Intro walkthrough got hung up at step 4 of 6. On Firefox with Windows 11." Run in headless Firefox 131 (Playwright build 1465) on 1.9.4 at 1280, 1024, 768 and 375 wide and at 1536x730, 1366x650, 1280x600, 1920x960, 1024x700 and 800x600: by mouse, by Enter and by Space the tour went through all six tips with no script error, so no engine fault reproduced. What did reproduce in every browser is the faded Next on tip 4 that does nothing visible until a call is made, which is the likely stall. The same Firefox walk passes on 1.9.5 | `tourShow()`, `tourPaintNext()`, `tourWatch()`, `tourPlace()`, `select()` in `callCard()` |
| **The note under the question is a labelled box.** After a call, "How to answer: Tap at least one reason, and more than one is fine. The line under each reason says what it means." sits in a green-edged tinted box with its label, not small grey text. The line that heads the six problems on Let it stand is set in ink and semibold. On the answer, the reason note and the still-open note are the same box, labelled "Your reason" and "Still open" | A tester: "I did not realize/see the little notes that popped up under the question." | `.notebox`, `paintCommit()`, `reasonNote()`, `openNote()`, `.basissplit` |
| **The ledger keeps its column heads, and sits beside the line on a wide screen.** In the ledger sheet the May, June, Change and Percent heads stay at the top while the rows scroll. From 1,024 pixels the full ledger also sits beside the line in its own panel, held under the progress line and scrolled to the account on the card, with the same held heads, so the question never leaves the screen; the See the full ledger button is hidden there. Under 1,024 the stacked layout and the sheet are as before. The tour places its tips clear of the panel | One tester: "I would prefer if the headers were frozen so I can scroll down and still be able to see which column is what." Another: "It would also be helpful to have the full ledger available in a pop-out on the side while still being able to see the entire question." | `ledgerSide()`, `lineLayout()`, `fitLedgerSide()`, `render()`, `.ledgerside`, `#sheetbody .scols` |
| **Every answer says why.** A "Why the key says so" section on the answer, read from the case file the line already carries: the key's full explanation (`why`), then one sentence of the account's figures from the ledger and one naming the reason the key gives with its meaning, for example "On the ledger, account 4200 (Freight billed to customers) went from $186,000 in May to $121,000 in June, down $65,000, or 34.9 percent. The reasons the key gives are figure does not tie (a dollar amount or percent in the memo does not match the ledger) and nothing written where owed (the change is big enough to need an explanation, and the memo gives none)." On a missed problem the full explanation takes the place of its one-sentence summary, which it begins with. Scoring is unchanged | A tester: "providing more in-depth explanations of why an answer is correct or incorrect would help students better understand the concepts." | `whyBlock()`, `ledgerFactText()`, `keyReasonText()`, `reveal()`, `.whybox` |
| **Where it fits, in one line.** The line 5 stop and the end screen say "Where this fits: auditing and intermediate accounting courses, as practice in professional skepticism. You test a written explanation against the ledger and the documents on file before you accept it, as an auditor does." | Three testers placed it in audit and intermediate accounting courses, one named professional skepticism, and one asked to see how it relates to the material being taught | `FIT_LINE`, `reveal()`, `done()`, `.fitline` |

The record is unchanged: `tests/tester-record-emit.cjs` writes the same records from 1.9.4 and
1.9.5 apart from the version and the random attempt ids.

Tests: `node tests/run-tester-record-tests.cjs` at 97 of 97, `python
tools/tests/test_tester_record_parse.py` at 34 of 34, the checker suite at 801 of 801 and the
findings tools at 54 of 54.

Firefox: run, in headless Firefox 131 through Playwright, on the local page. On 1.9.5 the tour
goes through all six tips by mouse, by Enter and by Space at 1280 and 375, and the full walk
(intro, tour, a call, the ledger with its heads held, two answers, the stop) passes at 320, 375,
768, 1024, 1280 and 1600 with no script error. Windows 11 Firefox on a real desk was not run.

Screens: `screenshots/verify/1.9.5-<width>-*` at 320, 375, 768, 1024, 1280 and 1600, from the page
served locally and captured in headless Edge: the intro (1), tour tip 4 (2), a question with the
new call labels and the reason box (3), the ledger scrolled with its column heads in view (4, the
side panel from 1,024 and the sheet below it), a right answer and a wrong one with Why the key says
so (5, 5b), the line 5 stop (6) and the tester end screen (7). No sideways scroll at any width.

---

# Second Pass, release 1.9.4

20 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.9.4, what changed since 1.9.3

Cut 20 October 2026 from the first tester feedback on the Mason form, on Khaled's go ahead. No
answer key, basis key, case file, reason value or record grammar changed, so the score, question
9's pre-filled record and `tools/tester_record_parse.py` read a 1.9.4 run exactly as a 1.9.3 one.
The product stamp moves to `second-pass-drill 1.9.4`.

| What changed | Why | Where |
| --- | --- | --- |
| **Every reason says what it means.** Under each reason's name, inside the same row, one plain line: for example "The memo gives a reason, but nothing on file backs that reason up." under no source on file and "The change is big enough to need an explanation, and the memo gives none." under nothing written where owed. The text is visible, so it works on a phone as well as a desk. Tour tip 5 adds "The line under each reason says what it means." | A tester: "It took me a while to understand what the difference between the reasons for flagging the issue, mostly 'no source on file' and 'nothing written where owed'." | `BASIS_HINT`, `paintCommit()`, `.oh` |
| **Let it stand reads as its own list.** On a stand, the figure and reason hold comes first, then the line "Letting it stand even though you saw a problem? Tap the problem as well." and the six problems under it. The reasons themselves are unchanged | A tester asked for different reasons under Let it stand. The answer key gives a stand one right reason, `build-cases.cjs` refuses any other on a stand, and the parser checks every line's basis against the case file, so new stand reasons would have been scored wrong or broken the record check. The facilitator guide also reads a problem tapped on a line let stand. The list is labelled per call instead | `BASIS_STAND_SPLIT`, `.basissplit` |
| **The tour no longer stalls on a keyboard.** Each tip takes focus when it opens, and before 1.9.4 Enter and Space there did nothing, so a tester who pressed Enter sat on tip 1. Now they press Next, and on the call tip they move focus to Let it stand as the Next button does | A tester: "Intro walkthrough got hung." Reproduced in headless Edge: eight presses of Enter left the tour on 1 of 6. The mouse path ran clean at 320, 375, 768, 1024, 1280 and 1600 wide | the tip's keydown handler in `tourStart()` |
| **The checker page is named where the form is.** The line 5 stop and the tester end screen close with "The form also asks about the checker page (checker.html, where you can run your own ledger). It is a separate page from the answer you see after each line." and a link that opens it in a new tab. The How it works sheet calls it the checker page in the same words, and the public intro link reads Checker page | A tester took the form's "Checker Page" for the answer screen after each line. The tester link never showed the checker | `feedbackPanel()`, `howScreen()`, `intro()` |

Tests: `node tests/run-tester-record-tests.cjs` at 97 of 97, `python
tools/tests/test_tester_record_parse.py` at 34 of 34, the checker suite at 801 of 801 and the
findings tools passing.

Screens: `screenshots/verify/1.9.4-<width>-*` at 320, 375, 768, 1024, 1280 and 1600, from the page
served locally and captured in headless Edge: the intro, the tour's first tip, tip 5 over the
stand reasons, both reason lists, the line 5 stop and the tester end screen.

---

# Second Pass, release 1.9.3

20 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.9.3, what changed since 1.9.2

Cut 20 October 2026, on Khaled's ask for a feedback button more testers actually press, and for
the form at the start as well, so a tester can open it alongside the drill. Every change is on the
tester link. The public link plays as 1.9.2 did. No answer key, basis key, case file or record
grammar changed. The product stamp moves to `second-pass-drill 1.9.3`.

| What changed | Why | Where |
| --- | --- | --- |
| **The bare form is linked from the start.** Under the tester band, from the intro until line 5 is locked, a line reads "Open the feedback form in a new tab now so you can see the questions. Send it from the button after line 5, which fills in your answers." Its first eight words are the link, to the bare `FEEDBACK_FORM` in a new tab. With the prefill off the line ends at "after line 5." It goes away at the stop, comes back if Back reopens line 5, and never shows on the public link | Testers are asked to look at the form first, and the line also says which button to send it from, since only that one carries the answers | `paintFormFirst()`, the `#formfirst` markup, `render()`, `reveal()`, `paintTestBand()` |
| **The feedback button says what it does and is the largest thing on the stop.** It reads "Open the feedback form with your answers" over "Opens in a new tab", in Mason green, full width and taller than any other control on the stop. With the prefill off it reads "Open the feedback form". Keep going stays quiet text under it. The note beside it is unchanged | "Open the feedback form" read like one choice among three, and the stop is where the answers have to leave | `feedbackButton()`, `.feedbackgo` |
| **Copy my answers.** An outlined button under the feedback button puts the whole record on the clipboard, read at the press, with the hint "Already have the form open? Paste into question 9." It answers "Copied. Paste it into question 9 of the feedback form." When the clipboard refuses, the browser's copy command is tried on a read-only box, and when that fails too the box stays open with the record selected and the line says "This browser did not let the page copy. Your answers are selected in the box below, so copy them from there." The copy is the full record with nothing cut to fit a link, in the same grammar, so the parser reads a pasted answer as it reads a pre-filled one | A tester who opened the form at the start and sends from that tab would otherwise send an empty question 9 | `feedbackPanel()`, `copyAnswers()`, `testerCopyText()`, `wireCopyAnswers()`, `TESTER_COPY_MAX` |
| **The tester end screen leads with the form.** A panel under the score reads "Your last step is the feedback form." with the same note, button and Copy my answers. Save my record stays in Your record further down, and the end screen still has no Send my results | The button used to sit at the very bottom, under the read out and the record | `testerEndPanel()`, `actionsBlock()` |
| **Nothing else moved.** Nothing is sent from the page, the pre-filled link is still rebuilt at every draw and every press, Enter and Space still carry nobody past the stop, and every new control has a name a screen reader reads: the link says it opens a new tab, the copy button is described by its hint, the copy line is a polite status, and the box is named | The 1.9.1 and 1.9.2 guarantees | unchanged `wireFeedbackLink()`, the stop's key handler |

Tests: `node tests/run-tester-record-tests.cjs` at 97 of 97, up from 74, with new checks T48 to
T54 on the start link (shown before Play, gone at the stop, back on Back, absent on the public
link, never rewritten, no request), the button's face, the copy (the record read at the press,
the fallback box, the copy command path, no request) and the end screen panel. `python
tools/tests/test_tester_record_parse.py` at 34 of 34 (the drift guard now reads the version from
the page), the checker suite at 801 of 801 and the findings tools at 54 of 54.

Screens: `screenshots/verify/1.9.3-375-*` and `1.9.3-1280-*`, from the page served by
`python -m http.server` and captured in headless Chrome: the first screen, the line 5 stop (with
Copied and the fallback box), and the tester end screen. No sideways scroll at either width.

---

# Second Pass, release 1.9.2

19 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.9.2, what changed since 1.9.1

Cut 19 October 2026, on Khaled's ask for every tester's line-by-line answers, kept in Mason
(Microsoft 365) tools rather than Google. Before this release a tester's calls stayed in their own
tab and never reached him. Every change is on the tester link unless the row says otherwise. The
public link plays as 1.9.1 did, except that three taps on the footer no longer turn test mode off.
No answer key, basis key or case file changed. The product stamp moves to `second-pass-drill 1.9.2`.

| What changed | Why | Where |
| --- | --- | --- |
| **The feedback button can carry the tester's answers.** Two new constants beside `FEEDBACK_FORM`, `FEEDBACK_PREFILL_BASE` (the form's pre-filled link up to its id) and `FEEDBACK_PREFILL_PARAM` (question 9's name in that link). With both set, the button at the line 5 stop and on the tester end screen opens the Mason form with question 9, "Your drill answers", already filled in. With either one empty it opens the bare form exactly as 1.9.1 did. A trailing `&` or `?`, the probe answer left on the base, or an `&` or `=` around the name is cleaned off, and a base with no `ResponsePage.aspx?id=` in it counts as empty | The form is the only channel from a tester to Khaled, and he needs each tester's lines to cite | `FEEDBACK_PREFILL_BASE`, `FEEDBACK_PREFILL_PARAM`, `prefillBase()`, `prefillParam()`, `prefillOn()`, `testerPrefill()`, `feedbackHref()`, `feedbackButton()` |
| **The record is one line a person can read and a script can parse.** A header (version, codename, attempt id, case, answered, right, points, run, case file), then one segment per locked round one line: line, account, call, basis chips, key, caught, missed, cleared or false flag, whether the basis agrees with the key, active seconds, and the tester's words trimmed to 80 characters. Fields split on `\|` and lines on `\|\|`, with no spaces, and every free text field loses its pipes. Round two is never carried. The grammar is in the comment above the constants | The tester reads it in question 9 before submitting, and `tools/tester_record_parse.py` reads it back. The run number keeps a second run, played after the key was shown, out of the rates | `testerRecord()`, `testerRecordParts()`, `testerClean()`, `testerChips()`, `testerSecs()`, `TESTER_CHIP` |
| **The link stays under 1,800 characters, and words give way before calls.** Words are cut to 40 characters a line, then 20 ("words cut to N"), then the newest lines give up theirs so the early notes stay ("words left off after line M"), then they go altogether. Only when the calls alone do not fit are lines dropped, newest first ("truncated after line N"). Five lines of plain English, 80 characters of words each, fit whole at 1,342 characters on the tests' stand-in link, and fourteen lines with no words fit at 1,537. Accented letters, other scripts and emoji take six to twelve times the room of a plain letter in the link. Five lines of 80 Arabic letters keep all five calls with notes cut to 20, five lines of 80 emoji keep all five with notes cut to 20 on the first four, and when anything is cut the stop says how much made it in | The review found the old cut dropped whole lines before it shortened any words, so the testers who wrote the most lost the most lines, and the separators alone took a third of the link | `FEEDBACK_URL_MAX`, `TESTER_WORDS_CUTS`, `testerRecordParts()` |
| **The link is rebuilt on every draw.** It is read when the button draws, which follows every lock and every Back, and read again when the button is pressed. A tester who goes back and changes line 5 gets a link with the changed line. Whether Forms shows the new record in a browser that already opened the form and did not submit it is part of the live check below | The link must never carry a line that has since changed | `feedbackButton()`, `wireFeedbackLink()` |
| **The band, the stop and the end screen say what the link carries, and only once it does.** With the prefill set the band reads "Nothing is sent from this page. The feedback form opens with your answers filled in, and Khaled sees them only if you submit it." The stop adds "Your five answers are filled in when the feedback form opens, and Khaled sees them only if you submit it.", with a sentence when notes were cut. The tester end screen carries the same line counted against every locked line, and tells a tester who sent the form at line 5 that sending it again carries the lines since. With the prefill empty all three keep their 1.9.1 words. The hidden band markup drops "TEST MODE, nothing is sent" for the same "Tester link" copy | The answers leave the browser inside the link when the form opens, so "nothing leaves before submit" would not be true | `paintTestBand()`, `testerStopNote()`, `actionsBlock()`, the `#testband` markup, `.stopnote` |
| **Three taps on the footer turn test mode on, one way.** They used to toggle it, and a desktop triple click on the version line was enough to turn it off: the line 5 stop and the feedback button went, and the end screen offered a live Send my results that posted to the Google form with no test attempt tag and a notice the tester never saw. Now nothing on the page turns test mode off, on either link | Test mode must never post, and the tester link must keep its answers in Mason tools | `wireTestTap()` |
| **The tester link never picks up a public run left in the same tab.** A saved run that is not a test attempt is not restored on `?test=1`, so the tester starts fresh under a random codename | A codename typed on the public link can be a real name, and it would have ridden in the tester record | `restoreRun()` |
| **The drill still sends nothing.** No new request of any kind; the answers leave the tab only inside a form the tester opens and submits | Test mode must never post | unchanged `sendResults()` guard |
| **A parser for the export.** `tools/tester_record_parse.py` (standard library only) reads the Forms Excel export or a CSV save of it and finds question 9 by its title. It drops a row with "TEST RESPONSE" at the start of any other question. It checks every record against the case file it names (outcome from call and key, account, key, basis, line numbers, header counts) and leaves an edited record out. It keeps the latest response for an attempt sent twice, counts rows that carry a name or email, and writes `tester_lines.csv` with a run column. The summary counts first runs only unless `--all-runs` is given, leads with lines 1 to 5, puts lines 6 and up under the testers who kept going, reports the right reason on caught problem lines, leaves line 1 out of the median seconds, and warns when versions are pooled | The numbers for the scholarship write-up, from Mason tools, and safe to cite: a second-sight run or a hand-edited record cannot inflate them | `tools/tester_record_parse.py`, `tests/tester-record-sample.csv` |
| **The version prints as 1.9.2** on the footer and in the payload, and `review.html` states it again, where it had stayed at 1.8.0 | One version everywhere it prints | `PRODUCT_VERSION`, `review.html` |

Live check against the real Mason form: not yet run. The two constants stay empty until the seven
steps in the README section "Before the two constants are filled in" are done: the form set to
Anyone can respond, question 9 free of branching, three links opened signed in and signed out on
desktop and phone, the reopen test, and an export read back by the parser. The result goes here
before the constants are merged.

Tests: `node tests/run-tester-record-tests.cjs` (new, 74 checks on a browserless harness of
`index.html`, `tests/index-harness.cjs`, with every network path spied, including tests that test
mode makes no POST and that the footer taps cannot turn it off), `python
tools/tests/test_tester_record_parse.py` (new, 34 tests, among them a drift guard against records
the drill itself writes through `tests/tester-record-emit.cjs`, including a second run after Play
again), the checker suite at 801 of 801 and the findings tools at 54 of 54.

---

# Second Pass, release 1.9.1

19 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.9.1, what changed since 1.9.0

Cut 19 October 2026, on four adversarial reviews of 1.9.0 (a student on a phone, a CPA, a UX and
accessibility reviewer and a scholarship reviewer) and a code review. Every change is on the
tester link unless the row says otherwise, and the public link plays as 1.8.1 did. No answer key,
basis key or case file changed. The product stamp moves to `second-pass-drill 1.9.1`.

| What changed | Why | Where |
| --- | --- | --- |
| **The tester link stops after line 5.** The reveal of line 5 carries one panel in place of Next: "That's five lines, which is all the feedback needs.", a primary Open the feedback form button, and a quiet Keep going that opens line 6. No key carries a tester past it | Every reviewer named the missing stop as the blocker: testers are asked for five lines and had no sign they were done | `reveal()`, `feedbackButton()`, `FEEDBACK_FORM`, `TESTER_LINES` |
| **The feedback form** is https://forms.cloud.microsoft/r/Q2gRni88vR, opened in a new tab with `rel="noopener"` so the drill stays where it was | One constant, used by the stop and the end screen | `FEEDBACK_FORM` |
| **The tester intro asks for five lines and the form.** It drops the fourteen lines and the second company and reads: "Read each line of the memo beside its own figures and flag the ones that do not hold. Do the first five, then the three-minute feedback form. The first line comes with a short tour." | The intro should ask for what the email asks for | `intro()` |
| **The band reads "Tester link" over "Nothing you do here is sent."** | Shorter, and it names the link the tester was sent | `paintTestBand()` |
| **The tester end screen offers the feedback form where Send my results was.** Save my record stays. The heading, the paragraph and the Google Form button are gone from the tester link | The tester link posts nothing, so a Send button there only confused the ask | `actionsBlock()`, `wireActions()` |
| **No case picker on the tester link.** Testers always play Halyard | One case for every tester, so their feedback is about the same lines | `caseControl()` |
| **Tip 5 reads "Now tap every reason that applies, and only those."** and **tip 6 reads "When you are sure, lock it in to see the answer key."** Tip 6 hides Skip tour and keeps Got it | The old tip 5 invited extra chips, which the basis score marks wrong | `TOUR_STEPS`, `tourShow()` |
| **Enter on Let it stand or Flag it presses that row** on the tester link, rather than locking the call already selected | A keyboard tester could lock the wrong call. The public link keeps its 1.8.1 handling, as this release changes nothing there | the Enter branch of `callCard()` |
| **One announcement per tip.** The tip is described by its count and its sentence, the live region is made once at boot, and it stays quiet when focus lands on the tip. It still speaks for the wait on tip 4 and when the tour closes | A screen reader heard every tip twice | `tourStart()`, `tourShow()`, `boot()` |
| **"Tap any time to open the full ledger." is gone under the ledger button** on the tester link | The button already says it | `cardBody()` |
| **A read taken after the memo was shown is never set beside the final calls.** The run records `memoBeforeRead` the first time a memo line draws with no read taken, and keeps it across the footer's change of mode. A tester who turns test mode off there and then takes the read sees "Your read was taken after the memo was already on the screen, so it is not set beside your final calls.", the record carries `memoShownBeforeRead: true` and `beforeAnyCall: false`, and question one adds "Taken after the memo was shown, so not a read before the draft." `tools/findings.py` reads that sentence as a late read, the same as one taken after a call | The code review found the comparison claiming a read came first when the memo had | `lineScreen()`, `readShift()`, `readShiftBlock()`, `prepickLine()`, `attemptRecord()`, `PREPICK_LATE_RE` in `tools/findings.py` |
| **Focus the tour hands back is scrolled into view.** Got it on tip 6 with no reason tapped hands focus to the first reason, which now scrolls clear of the sticky progress line and, while the sheet is up, of the sheet | The code review found that control sitting under the progress line | `tourFocus()`, `tourReveal()` |

Unchanged, and checked: the public link against 1.8.1 at 1,280 and 320 pixels, screen by screen
from the intro to line 1, then the reveal of line 5 (Next still there) and the end screen (Send
my results still there), once the version stamp, the codename and the lap time are set aside. The
checker passes 801 of 801 and the findings tools 54 of 54.

---

# Second Pass, release 1.9.0

19 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.9.0, what changed since 1.8.1

Cut 19 October 2026, on Khaled's ask for the tester link: a one question tutorial with tooltips so
a tester gets the gist of it, and no full ledger before they start, because that much at once is
overwhelming. Every change below is on the tester link (`?test=1`) only. The public link plays as
1.8.1 did. The product stamp moves to `second-pass-drill 1.9.0`.

| What changed | Why | Where |
| --- | --- | --- |
| **The tester link opens on line 1, not on the ledger.** Play goes from the intro straight to the first memo line, and Play again does the same. Each line card already shows its own account's row from the ledger, both months and the change, so nothing a tester needs is lost | A tester asked to try five lines should start on a line, not on fourteen accounts | `intro()`, the Play again handler, `render()` |
| **The read before the draft is recorded as skipped,** and nothing reads it as a read. Play stores an empty read with `prepickSkipped` set, which meets the gate in `render()` honestly. The end screen draws no read-shift block, the record carries `prepicks.skipped: true` and `required: false` with a note, every round one line carries `ledgerOnlyRead: null`, and question one would carry "Prepicks: skipped.", the sentence `tools/findings.py` already reads as a skip. Only the tester link honours a skip. On the public link the read stays required, and a tester run whose test mode is turned off from the footer goes back to the ledger | An empty read would otherwise count as fourteen lines let stand and report a shift off a read nobody took | `prepickSkipped()`, `prepickRead()`, `skipReadForTester()`, `readShift()`, `prepickLine()`, `attemptRecord()` |
| **A six-tip tour runs over line 1.** Each tip sits on the real part it names, with a count such as 2 of 6, a Next button and a Skip tour link. The card stays live: the tester makes the call and taps the basis themselves, choosing a call moves the tour on to the reason rows, and line 1 is scored like any other line and counts as one of the five | His ask: one question, walked through with tips | `TOUR_STEPS`, `tourStart()`, `tourNext()`, `tourAfterCall()` |
| **The tour stays out of the way.** Escape closes it. Focus moves to the tip and back to the part it named, and Tab from Next lands on that part. A polite live region reads each tip out. Enter on Next never locks the call. A tip never sits over the part it points at: it opens beside the card at 1,280 pixels, below the part at 1,024, and under 600 pixels it is a sheet along the bottom with the part scrolled clear above it. Reduced motion drops the fade and the smooth scroll | A tour that covers the control it explains, or traps a keyboard, teaches the wrong thing | `tourPlace()`, `tourKeys()`, `tourFocus()`, the tour block at the foot of the page style |
| **The tour shows once per tab.** `tourSeen` rides in the run state, so a reload mid-run does not repeat it, and Play again leaves it set | A tester who has seen it once should not sit through it twice | `S.tourSeen`, which `freshRun()` leaves alone |
| **The tester copy stops describing a read it does not take.** The intro says each line sits beside its own figures and that the first line comes with a short tour, and the How this works panel drops its paragraph on the read | The words on the tester link should match its screens | `intro()`, `howScreen()` |

The six tips, in order, one sentence each:

| Tip | Points at | Says |
| --- | --- | --- |
| 1 | the memo sentence | This is the sentence the AI wrote about this account, and it is the one you are checking. |
| 2 | the account's figures | These are the ledger figures for the same account, so you can check the memo's numbers for yourself. |
| 3 | On file | This is what is on file, and if nothing here backs the memo's reason, that reason is not established. |
| 4 | Let it stand and Flag it | Make your call here: let it stand if the figure and the reason both hold, or flag it if either one does not. |
| 5 | the basis rows | Now tap the reason behind your call, and you can pick more than one. |
| 6 | Lock it in | When you are sure, lock it in and the answer key comes back to show how you did. |

Next on tip 4 waits for a call, and says so: "Choose Let it stand or Flag it first, and the next
tip opens by itself." Tips 2 and 3 are left out on a line whose card has no figures row or no On
file block, so an authored case never points a tip at nothing.

Unchanged, and checked: the public link screen by screen against 1.8.1 at 1,280 and 320 pixels
(the intro, the notice, the codename filled in, the chapters, the ledger read and line 1 match
once the version stamp is set aside), the read still required there, the scoring, both answer
keys, the Google Form posting and its entry identifiers, the findings tools (54 passed) and the
checker (801 of 801 tests pass).

---

# Second Pass, release 1.8.1

19 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.8.1, what changed since 1.8.0

Cut 19 October 2026, on Khaled's review of the tester link before the AI Native Accounting
Foundation outreach: a tester should land on the drill and nothing else, and a name field should
never hold the Start button shut. The product stamp moves to `second-pass-drill 1.8.1`.

| What changed | Why | Where |
| --- | --- | --- |
| **The tester link shows the drill only.** With `?test=1` the header drops the Drill, Checker, Review and Author row and the wordmark stops being a link, the footer keeps its one line and drops its links, and the intro and the How this works panel drop the checker, author, reviewer and document links | Three more pages one tap away were overload for someone asked to try five lines and answer a form | `assets/nav.js` `drillOnly()`, `intro()`, the How panel |
| **The tester link goes from Play straight into the drill** under a random codename. Test mode posts nothing, so the notice about what gets posted and the codename screen have nothing to ask of a tester; Play again returns to the ledger | One tap from the email to the first screen of work | `intro()`, the Play again handler |
| **Every run gets a random codename,** two words in the style of the old placeholder (Saffron Raven, Copper Puffin), the way a shared sheet names a visitor who is not signed in. On the public link the codename screen shows it filled in, the player can type over it, and a field cleared to nothing gets a fresh one on Start, so the name never holds Start shut | His ask: the name field was stopping Start from being clickable | `randomCodename()`, `identity()` |
| **An empty chapter list reads "none given"** in the organizations line of the local record | A tester skips the chapter chips, and the line should not print "Organizations: ." | `orgLine()` |

Unchanged, and checked: the public drill's flow (notice, codename and chapters, ledger, memo), the
chapters still required on the public link, the scoring, both answer keys, the Google Form posting
and its entry identifiers, and the checker (801 of 801 tests pass).

---

# Second Pass, release 1.8.0

11 October 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.8.0, what changed since 1.7.1

Cut 11 October 2026. The drill's screens change and nothing under them does. Khaled pointed at a
practice quiz he found clean to answer, and the elements of it that fit a review drill came across:
one question on the screen with its choices directly under it, choices as full-width rows of one
height, a selection that fills the whole row, one quiet line of progress, and feedback that
arrives without a show. The product stamp moves to `second-pass-drill 1.8.0`.

| What changed | Why | Where |
| --- | --- | --- |
| **The call is two full-width rows.** Let it stand above Flag it, each with a ring on the left and the whole row as the target. A chosen row fills ink and its ring fills; the other row stays as it was | Two side-by-side buttons read as a toolbar, and the quiz showed how much faster a stacked choice reads on a phone | `callCard()`, the `.opt` rules at the foot of the page style |
| **The basis is one column of rows with a square.** It was a two-up grid of chips of uneven height on a desk | One choice style for every question in the drill, and a square says more than one may be tapped | `paintCommit()` |
| **The read before the draft is a list of rows,** the account number in a small monospace face beside the name, one column on a phone and two beside the legend from 900 pixels | Fourteen chips of fourteen widths were the most ragged block in the product | `prepickBlock()` |
| **One line of progress.** The rank meter leaves the header; the reveal and the end screen keep the rank, the points and the distance to the next rank. "Second Pass" printed under the track on screens with no progress is gone, and on those screens the line takes no room | The header showed the score twice over the card where the player was deciding | `progress()`, the `#bar` markup |
| **The track keeps the 520 pixel column** on every screen | On the wide ledger screen it stretched to 1,048 pixels and stood 119 pixels tall | `#track` |
| **The verdict fades in once.** The card no longer turns over, the points no longer count up and the rank bar no longer flashes gold. Reduced motion shows the face with no fade | Calm feedback; the gold flash was also a fourth use of gold | `reveal()` and its style block |
| **Every screen starts at the same top edge** instead of floating to the middle of the window | A short screen and a long one now begin in the same place, so the card does not jump | `#screen` |
| **The question sits at the lead size directly on its choices,** and the instruction line prints over the first card of a round and not the thirteen after it | A quiz states its rule once and then shows only the question | `.ask`, `callCard()`, `reveal()` |
| **Play sits under the opening text,** before How to play | Play now shows in the first screen at 1,280 by 800 | `intro()` |
| **One type scale.** The verdict and the points numeral take the 28 pixel heading size (they were 32 and 34), and the How to play captions take the 14 pixel small size (they were 13). The How to play frame for the call now draws the two stacked rows | The drill's own scale, applied the same way everywhere | page style, `playFrames()` |

Unchanged, and checked: the scoring and the rank ladder, both answer keys and the case files, the
badges, the Google Form posting and its 38 entry identifiers, the payload, the attempt record (the
two renamed fields still ride beside their new names, now through 1.8.0), the codename band, the
organization chips, test mode, the checker and every fixture, and the copy. The element ids the
audit walks drive (`#stand`, `#flag`, `#lockin`, `#prepicks .chip`, `#commit .chip`) are kept.

The suites at this release, each run on a copy of the branch: the browser checker **801 of 801**;
the findings tools **54 passed**, which includes the written-answer minimum read out of
`index.html`; `node build-cases.cjs` passes its card checks and rewrites the inline case copy with
only its date stamp changed; `audit/prepicks-2026-09-13/walk-prepicks.cjs` **44 of 44** on Halyard
and **44 of 44** on Kestrel; `audit/findings-and-lock-2026-09-13/lock-walk.cjs` **62 passed, 0
failed**; `audit/author-repair-2026-09-13/walk-drill.cjs` at 320, 375, 768, 1,024, 1,280 and 1,600
reaches the end screen with no screen overflowing and no page error. The same commands on 1.7.1
returned the same counts.

### What remains open

Everything listed as open under 1.7.1 below is still open.

---

## 1.7.1, what changed since 1.7.0

Cut 10 October 2026. The checker changes, in the browser and in the command-line package
together, and the drill, the cases, the protocol and the data notice do not. The product stamp
moves to `second-pass-drill 1.7.1` so a record says which checker stood behind the page. Every
change answers the second round of the independent audit of 14 September 2026
(`audit/INDEPENDENT-AUDIT-2026-09-14.md`, N1 to N6), a ChatGPT review of 8 October 2026, or a false
failure found on 10 October 2026 on a made-up practice case. Each rule went in after a commit of
fixtures that failed against the code before it. Commits in the second-pass repository are marked
as such.

The suites at this release: **799 shared fixtures**, 55 more than 1.7.0 with no earlier
expectation changed; the browser checker **801 of 801**; the command-line checker **1,679
passed**, of which 878 stand alone; parity **801 passed**, every fixture on all eleven fields; the
findings script **54 passed**. The audit's 186 probes of 14 September 2026, graded by its own
`grade-probes.cjs`, return the status each one requires on 185, up from 158 at 1.7.0, and the
browser and the command line agree on all eleven fields for all 186. The one left, C019, is a memo
of two sentences whose basis says the second is false; the grader reads only the first, and the
second fails in both checkers. The four sample coverage strips in `CHECKER.md` are unchanged.

| What was wrong | What changed | Commits |
| --- | --- | --- |
| **A season read as a direction.** "On the fall open house mailer" failed as a fall in the line | `fall` in front of a noun is read as the autumn. It is not tested for direction or read as a reason pointing back at the line, and it is held as a weak period word inside the claim, as `spring` and `summer` are. `SEASON01` to `SEASON09` | `e179a78`, `4127ed5`; second-pass `13388e5`, `6b8ebb5` |
| **A quoted document title read as a claim.** A direction word inside a quoted memo title was tested against the line (audit N6, C015) | A span in curly, straight or single quotes of two words or more with no digit is written over before the direction check and the claim and reason boundary read the sentence. A quoted single word and a quoted figure are still read. `TITLE01` to `TITLE06` | `55991a3`, `b17183c`; second-pass `f2e93f2`, `a3ec8c1` |
| **A second financial subject took the first one's figure.** "Rent expense rose $30,000, so gross profit increased $30,000" cleared (ChatGPT review, 8 October 2026), and a percent restating a figure was bound to another line (audit C119) | `gross profit`, `net income`, `operating expenses`, `cost of goods sold`, `cash flow` and their kin, named in the claim in a clause with a figure or a direction word, hold the sentence at needs review unless the subject is a bound line or part of a ratio's name, and that clause's direction word is no longer tested against the line its figure happened to tie to. `$30,000, or 30 percent` binds the percent to the line of the figure it restates. `SUBJ01` to `SUBJ09` | `0318571`, `d56d3aa`; second-pass `9e808b9`, `f2e2255` |
| **Words outside the lists cleared** (audit N1 to N5, and C046 of N6). "Rangebound at $130,000" cleared on a line that rose 30 percent, as did size, share and approximation words after the noun and `$30,000+` | The no-change rule is structural: a sentence whose only figures are balances on one side, with no movement figure, no direction word in its claim and no threshold claim, is held whatever word it uses. `about`, `approximately`, `roughly`, `around`, `circa`, `~`, `give or take`, `or so` and the rest of one approximation class are taken out and the figure is compared unrounded, while bound words such as `nearly`, `north of` and `at least` leave the role unknown and hold. A plus after a figure is a sign. Size and share words are read by their place: after `the increase was`, in a phrase restating the movement, or taking a share `of it`. `STRUCT01` to `STRUCT08`, `APPROX01` to `APPROX08`, `PLUS01` to `PLUS04`, `SIZEST01` to `SIZEST05`, `SHAREST01` to `SHAREST06` | `e0972fd`, `193ed1c`; second-pass `b299820`, `56058b9` |

### What remains open

Everything listed as open under 1.7.0 below is still open. No person outside the build has used
the checker or played the drill.

---

## 1.7.0, what changed since 1.6.1

Frozen 14 September 2026. Every change answers a finding in the third independent review of 13
September 2026, which reviewed 1.6.1 at `b6ba468` and the command line package at `130b6b7`.
Commits in the second-pass repository are marked as such.

The suites at the freeze: **744 shared fixtures**; the browser checker **746 of 746**; the
command-line checker **1,569 passed**, of which 823 stand alone; parity **746 passed**, every
fixture on all eleven fields; the audit's own eight input sets **513 of 513** equal on all eleven
fields; the audit's 175 adversarial probes at **0 false clearances and 0 other misses**; the author
page folding against the checker **751 of 751**; the findings script **54 passed**. The protocol
moves to version 1.2, effective 14 September 2026, and the data notice is restamped
`notice-2026-09-14` with its wording unchanged. All 41 findings of the third review are read again
at this head in `audit/THIRD-REVIEW-STATUS-2026-09-14.md`, where they stand at 34 closed, 2
partial, 4 open and 1 deferred by ruling.

| Finding in the third review | What changed | Commits |
| --- | --- | --- |
| **1. The record counted attempts as players and scored a new case against the old key.** Two attempts under one codename came back as two players, and a Kestrel record was scored against Halyard | `tools/findings.py` scores every record against the case file for the version it names and refuses a version it has no file for. It reports received attempts, completed attempts, distinct codenames and facilitator-confirmed participants as four separate counts, reads only the first eligible attempt under each codename, and lists reattempts in their own table. `READOUT-TEMPLATE.md` defines each count once, and the facilitator guides never report codenames as people. The sample carries brightwater-v6 runs with written explanations | `c6f0088`, `3bdb3ff`, `a42d7af`, `19f4605`, `56b87a7` |
| **2. The reviewer page claimed more than the build shows.** "Reads better than a person writes", "every figure against the ledger", the universal input promise, and a counted unit named two ways | `review.html` claims only what the checker and the evidence show. The drill's scope note, the 404 page, the release notes and the facilitator guides no longer promise any ledger or every figure. The two earlier design variants, `review-a.html` and `review-b.html`, still served and still carrying the old claims, are retired to a noindex pointer at `review.html` | `b956423`, `8abea9e`, `19f4605`, `49767ad` |
| **3. The reason score and the rank.** The case guide said the reason score never moves the rank, and the executed points said it does. Chips measure agreement with accepted categories, not reasoning, and the Brightwater evidence pre-solved item 3 | The case guide, the governance note, both facilitator guides and five strings in the drill now say the reason's fifty points count toward the rank; the scoring code is unchanged. On `brightwater-v6` every assessment call needs a three-part written explanation (the decisive evidence, why it matters for the period, the action or source request) before it locks, the evidence shows document contents without saying what they establish, and `RUBRIC.md` with a blind scoring sheet puts the explanations in front of an educator | `8abea9e`, `f376b84`, `6447d97`, `1fcedbd`, `19f4605` |
| **4. The checker contract.** "Doubled", "remained at", a fraction and Arabic-Indic digits all cleared, Prompt 1's own labels were not read as roles, and the parity claim described the two fixture files as the same when they differed | Multipliers, fractions, digits outside 0 to 9 and scale words are unparsed spans that leave a sentence not checked; "remained at" and other no-change claims no longer clear when the line moved; `prior` and `current` in front of a figure are read as roles. `CHECKER.md` says what the grammar reads and a sentence clears only when every quantitative expression in it is accounted for. The suite holds 744 fixtures: the forty probes and 113 mutations across six classes, the independent audit's 175 probes with the clearance grammar's 159 class mutations, 111 more for the residual classes, sentence boundaries, size words, periods bound to the column labels, account names at the edge of a sentence and the lexicon one step past its words, and 86 for the checker residuals, a direction word a reason governs, an abbreviation inside a name, a quarter against the column labels and a word that says how much of the movement a sentence explains. The Prompt 1 rerun is recorded in `audit/PROMPT1-RERUN-2026-09-13.md` and still stands at 14 of 17. The Python checker mirrors the contract, and one shared file of 744 inputs agrees on every compared field in both implementations: 746 browser checks, 746 parity tests and 1,569 Python tests pass | `d081409`, `71d457b`, `4f89ee1`, `1f9acb7`, `09cec33`; second-pass `acdf580`, `fe8cd49`, `b523044`, `216bd2b`, `dbf0342`, `bb6fd2d` |
| **5. The author page.** An unresolved checker result became a clean suggestion, a save after an edit kept stale figures, and an unbound sentence vanished | The author page reads with the checker's own reader and holds what the checker holds, including a direction word it cannot tie to a line; save and preview are disabled until the inputs are read again; every sentence comes back as a card or an open item that must be settled; the case records whether it is synthetic or a permitted real case, and the drill's introduction follows it. A card checked within scope now names the numbers the checker read and left outside the check | `052fd1f`, `81f92dc`, `1fcedbd`, `5c6f9ab`, `742525a`, `50927f4` |
| **6. The three-ledger evidence.** The runs were not comparable, and unsupported exclusions and forecasts were not counted | Every unsupported claim in the six retained drafts is counted by class with its exact text, the development-session run is labeled apart from the fresh-context runs, and the prediction inference is gone | `a3ada19` |

**The read before the draft.** Not a review finding: Khaled ruled at about 9:40 PM on 13 September
2026 to keep the ledger-only step and make it count, because it is the one point where a player
decides before seeing anything the AI drafted. It is now required with no skip and no cap, locked
once the player goes on, and no later screen draws without it, whether reached by a button, a key,
the step hook or an edited saved run. The end screen says on how many round one lines the final
call moved off that read, and whether each change moved toward the key or away from it, with no
effect on points or rank. The round one question and the record carry the read per line with the
case version, the data notice names it (`notice-2026-09-14`), and `findings.py` reports the
comparison for first attempts in each case set as descriptive agreement on a keyed exercise, with
six new tests. Walked in headless Chrome on Halyard, Kestrel and an authored case, 44 of 44
checks each, with viewport screenshots at six widths looked at by eye, in
`audit/PREPICKS-2026-09-13.md`. Commits `29df0aa`, `bce4a15`, `a4b1538`.

### What remains open

- **Receipt deployment.** `RECEIPT_ENDPOINT` is still empty in `index.html`. A synthetic receipt has
  to reach the real destination, and a retried attempt has to leave one stored record, before any
  collection is described as a verified store.
- **Observed practitioner sessions.** Two or three practitioners on a ledger and memo they did not
  build, uncoached, each ending in a saved review record. None has happened.
- **Educator review.** An independent educator's review of the keys, and blind scoring of the written
  explanations against `RUBRIC.md`, with a second scorer on a subset. Not yet done.
- **Clean-context evidence reruns.** The three paired drafts repeated in fresh contexts under fixed
  instructions, with every output kept and a second reader classifying the unsupported claims. Not
  yet run.
- **Opening a saved case in the author page.** The author page saves a case file but cannot open
  one. Ruled on 13 September 2026 to come after the freeze.

---

## 1.6.1, what changed since 1.6.0

1.6.1 closes the items the release QA of 13 September left open that did not need another person.

| What | Where | Evidence |
| --- | --- | --- |
| A quantity written out in words is read, or the sentence says it was not. Units through millions, hyphenated compounds included: a run becomes a figure where the parser resolves it and the words give it a unit, and otherwise it reaches the reviewer's queue and the sentence is not checked. A count in words beside no claim is left alone | `checker.html`, `CHECKER.md` rule 1c | fixtures `T49` to `T54`, and `T21` now fails a false percentage in words rather than leaving it unparsed. 59 fixtures, 59 pass at 1.6.1; 799 fixtures and 801 checks pass now. Mirrored in `second_pass/checker.py`, 138 pass at 1.6.1 and 1,679 now |
| Three claims on the reviewer page corrected, and five more found reading the page against `CHECKER.md`, `PROTOCOL.md` and the evidence note | `review.html` | the page now says the protocol asks for four steps rather than that the site enforces them, that this checker leaves the driver and the period to a reviewer, and that the machine check is a figure that does not tie to the line it names |
| Two record fields renamed to what they hold, with the old names alongside for this version | `index.html`, `README.md` | `evidenceSupplied` with `evidenceSelected` beside it, `elapsedSecondsOnCard` and `activeSecondsOnCard`, `firstRunInThisTab`, and `renamedFields` on the record |
| The card clock now also reports time with the tab's hidden time taken out of it | `index.html` | `activeSecondsOnCard`, `activeSecondsOnCards` and `hiddenSecondsInRun`, measured on `visibilitychange` |
| Every on-file fact in the fresh case carries a one-line excerpt from a named, dated document, or says the document was requested and is not on file. The wrong-period item rests on a real quoted schedule dated 31 May 2026 | `cases/brightwater-v5.json` | the file's own change log; verified in the page in test mode at card 3 of 5 |
| The facilitator guide no longer decides the accrual from a contradiction, and every percentage in it is attributed or gone | `FACILITATOR-GUIDE.md`, `FACILITATOR-ONE-PAGE.md`, `Second-Pass-Facilitator-Guide.pdf` | the two sample-findings rates are out, because no room has run this yet |

---

## The problem

A month-end close now produces flux commentary faster than a person can read it. The sentences
come back fluent, the arithmetic usually holds, and the reason attached to each movement is the
part nobody checks. A reviewer under a close deadline reads for tone and reads for whether the
numbers look about right, and a sentence that names a cause no document supports goes into the
management report with everything else.

The failure is not that the machine cannot add. It is that a memo which adds up correctly and
explains itself confidently is the hardest thing in a close to argue with, and the accounting
judgment it displaces is exactly the judgment a student is supposed to be learning.

Second Pass is a training instrument and a working tool for the second reading. It teaches the
reviewer's move: recompute the figure, test the direction, find the line nobody wrote about, and
then ask what document would carry the cause the sentence names.

## What was built

Four pages, all static, all free, none behind a sign-in.

**A drill.** A player takes a fourteen-line ledger and a memo drafted against it, one account at a
time, and decides on each whether the sentence stands or gets flagged. Every call is followed by a
basis: which of seven things is wrong, or that the figure and the reason hold. The call and the
basis are scored separately, because agreeing with the answer key while naming the wrong defect is
not judgment. After the fourteen practice lines a second company appears, five lines nobody has
seen, run as an assessment with nothing revealed until all five are committed.

**A checker.** Paste a ledger in a layout it accepts and a memo, set the commentary threshold, and
the page recomputes each figure it can read against the ledger, tests the direction words it can tie
to a line against the sign, names every account that clears the threshold with no sentence written
about it, and returns one of four statuses per sentence: checked within scope, needs review, not
checked, failed. A sentence carrying anything the grammar cannot read is not checked, and what it
could not read goes to the reviewer. It runs entirely in the
visitor's browser. Nothing pasted into it is transmitted anywhere.

**An author page.** Paste your own trial balance and your own memo and the page reads them,
proposes a call and an error type per line, asks you to key each one, and writes a case the drill
will run. The case is a JSON file you keep.

**A reviewer page.** One page that sets out the problem, the governance, the evidence, the
outcomes plan, the scope and the replicability, and links everything else.

## Governance

The checker's headline behavior is abstention. A sentence is cleared only when every figure in it
carries a role the words gave it, a unit, and an unrounded comparison with the ledger that agreed,
every other number in it is a year, a date, a label, an ordinal, a reference or a count, and
nothing the clearance grammar calls risky is left once those claims have been read. A figure whose
role the words do not give stops a clearance before any value is compared. A sentence naming two
accounts is held unless each figure binds inside its own clause. A negation, a foreign currency, a
multiplier, a fraction and a bare number the grammar cannot place each leave the sentence
unresolved rather than passing it, and a currency, a period, a sameness word or a word that sizes
a movement holds it for review with the word named. No unresolved status is promoted to checked by
a later step, and the reviewer prompt the page generates opens by naming the mechanical work that
was **not** done.

The written protocol, `PROTOCOL.md` at version 1.2, states the control: no commentary drafted with
AI assistance is released until a second pass has tied every figure to the ledger and a named
reviewer, never the preparer, has signed the two judgment questions, whether the driver is
supported by a document on file and whether it belongs to the period.

Participant data is handled on the same principle. A data notice appears before a codename is
chosen and says plainly that a codename is a pseudonym and not anonymity. Completing the drill
does not require sharing anything: saving a local record and sending results are two separate
buttons. Four questions the collection form carries are not asked in this version, and the record
says so rather than posting a value that would read as an answer. A send is labeled sent and
unconfirmed, because a hidden frame loading does not prove a receiver stored anything. A test mode
posts nothing at all and stamps the record for exclusion.

`GOVERNANCE-NOTE.md` carries the decisions and who made them. `PROVENANCE.md` states, without
softening it, that the case company does not exist, that the fourteen planted defects were
authored rather than generated, and that the build was carried out by an AI coding agent under
direction.

## The outcomes plan, and what it can support

Nobody has run the drill yet. The release claims nothing about learning, time saved or real close
errors, and the plan is written so that it cannot drift into claiming them.

What a pilot can support is descriptive agreement with an author's key, on completed and eligible
attempts, at a frozen case version. The measures are: right call and right reason by error type;
false flags on the six clean control lines; the fresh five against the trained fourteen, reported
as two item sets rather than as a pre-test and a post-test; and the reasons participants actually
wrote, scored by a person against the three-part rubric in `RUBRIC.md`, which the page does not
attempt itself.

`tools/findings.py` computes exactly those, reads the responses export, drops test rows and
repeats on the attempt identifier, counts each organization separately, and writes every field
`READOUT-TEMPLATE.md` names, the run fields once and one block per case set. A field the
responses cannot support prints *not available* rather than an estimate.

What the record cannot support is written down too: confidence is null because it was not asked;
the evidence list is what the card supplied, not what the participant consulted; elapsed time does
not pause for an inactive tab; a codename is not a reliable way to count people. Those limits are
in the reviewer page and in this file because a measure that outruns its instrument is the failure
the whole project is about.

## Replicability

Everything needed to run this somewhere else is in the repository, and none of it needs the
author present.

A facilitator runs a session from the guide alone. A student authors a case from their own trial
balance in the browser and the drill runs it. An accounting department pastes its own memo into
the checker and gets a review log with evidence identifiers, a proposed conclusion, a human
conclusion, an unresolved issue, an owner and a review time. The answer keys are JSON files with
change logs that name who asked for each change and why. The checker's contract is held by a
regression suite that runs against the page itself with no build step, and the two shared cases the
checker demonstrates are generated from the same files the drill reads, so the two surfaces cannot
drift apart.

## Honest scope

- **No participant has used it.** There are no results, and none are implied anywhere.
- **No practitioner has been observed** running a real memo through it without coaching.
- **No educator has independently reviewed the answer keys.** The keys are defensible under the
  supplied case facts and have survived one external review, which is not the same thing.
- **The checker checks figures, not causes.** All five sentences of the assessment case come back
  checked within scope, four of them name a cause the ledger cannot settle, and the page says so.
- **The fresh case shows one line out of each document,** not the document. Judging evidence from
  an excerpt is a weaker test than judging it from the file it came out of.
- **A sentence that clears has been read, not understood.** The clearance grammar takes out the
  claims and then holds the sentence on any word it knows to be risky, and a word it does not
  carry, or a weak word standing inside a reason, can still clear. The classes left open are listed
  under **Still open** in `audit/CLEARANCE-GRAMMAR-2026-09-13.md`.
- **The case company does not exist.** No client data, no engagement, no real ledger.

---

## Every file in the release

### Pages

| File | What it is |
| --- | --- |
| `index.html` | The drill: fourteen practice lines, then five assessment lines on a company the player has not seen |
| `checker.html` | The checker: paste a ledger and a memo, get a per-sentence status, a reviewer queue, a CSV, a printable sheet and two prompts |
| `author.html` | Build a drill from your own trial balance and your own memo |
| `review.html` | The entry in one page: problem, governance, evidence, outcomes, scope, replicability |
| `404.html` | The custom not-found page, with the three ways back |
| `review-a.html`, `review-b.html` | Retired. Two earlier design variants of the reviewer page, now a short noindex page each that points to `review.html`, kept so old links do not end on a 404 |

### Shared assets

| File | What it is |
| --- | --- |
| `assets/second-pass.css` | Every rule two pages share: the tokens, the controls, the focus ring, the tables, the action bar |
| `assets/nav.js` | The header, the footer and the skip link, printed onto every page from one template |
| `assets/second-pass-core.js` | The ledger and memo reader the checker and the author page both run |
| `assets/favicon.svg`, `assets/favicon-32.png` | The tab icon in both formats |
| `assets/og-image.png`, `assets/og-image.svg` | The share card |
| `robots.txt`, `sitemap.xml` | Everything public, nothing disallowed, five URLs listed |

### Cases

| File | What it is |
| --- | --- |
| `cases/README.md` | How a case file is shaped, how to pick one, how to author one, and what changed in each version |
| `cases/halyard-v4.json` | Halyard Provisioning Group, fourteen accounts, eight problem lines and six clean ones. The practice case |
| `cases/brightwater-v6.json` | Brightwater Dental Partners, five accounts, three problem lines and two clean ones. The assessment case. Every on-file fact carries a dated document excerpt, and every call asks for a three-part written explanation |
| `cases/brightwater-v5.json` | The version before it, kept because responses were scored against it. Same calls, same figures, evidence that read the documents for the player |
| `cases/kestrel-v1.json` | Kestrel IT Services, twelve accounts, seven problem lines and five clean ones. The second practice case |
| `cases/halyard-v3.json`, `cases/brightwater-v4.json`, `cases/brightwater-v3.json`, `cases/brightwater-v2.json` | Superseded versions, kept because a response scored against one of them is not comparable to a response scored against the current pair |
| `build-cases.cjs` | Validates a case file and refuses one whose reveal text is missing |
| `build-checker-cases.cjs` | Regenerates the checker's Halyard and Brightwater samples from the same case files the drill reads |

### The written record

| File | What it is |
| --- | --- |
| `README.md` | The whole build: every screen, every rule, every number and where it comes from |
| `CHECKER.md` | What the checker checks, what it refuses to check, and the expected output for all four samples |
| `PROTOCOL.md` | The two-page control, version 1.2 |
| `Second-Pass-Review-Protocol.pdf` | The same protocol, printable |
| `PROVENANCE.md` | Where the case came from, who wrote the memo, and what was authored rather than generated |
| `GOVERNANCE-NOTE.md` | The decisions taken during the build and who took them |
| `INTRO-CANDIDATES.md` | The intro lines considered on 12 September, kept as history; none of them is the live intro |
| `RELEASE-NOTES.md` | This file |

### Running a session

| File | What it is |
| --- | --- |
| `FACILITATOR-GUIDE.md`, `Second-Pass-Facilitator-Guide.docx`, `.pdf`, `-p1.png` | Run a session from the guide alone, in three formats |
| `FACILITATOR-ONE-PAGE.md` | The same, cut to one page |
| `EVIDENCE-LOG-TEMPLATE.csv` | The review log a practitioner fills, with two worked rows |
| `EXCEL-TEMPLATE.md`, `Second-Pass-Excel-Template.xlsx`, `build_excel_template.py` | The same log as a workbook, and the script that builds it |
| `READOUT-TEMPLATE.md`, `Second-Pass-Results-Readout.docx` | The readout a facilitator fills after a session, three pages: the counts, each defined once, then one block for each case set, naming the field for every cell |
| `RUBRIC.md` | The three criteria an independent educator will score the written explanations against, the scoring sheet that hides the key, and how the second scorer's rows are drawn |
| `build-facilitator-pdf.py` | Builds the guide's docx and pdf from the markdown |

### Evidence

| File | What it is |
| --- | --- |
| `evidence/EVIDENCE-NOTE.md` | What six real AI drafting runs claimed, bounded to those runs and those three ledgers |
| `evidence/UNSUPPORTED-CLAIMS.md` | Every unsupported claim in the six drafts, by class, with the exact text behind each count |
| `evidence/ai-draft-*-raw.md` | Six raw model drafts, three ledgers, blind and under Prompt 1, unedited |
| `evidence/*-run.csv`, `*-recheck.csv` | Each draft put through the checker, exported |
| `evidence/ledger-paste.txt` | The exact input the drafts were given |

### Tests and tools

| File | What it is |
| --- | --- |
| `tests/checker-fixtures.json` | 799 fixtures: the original defect set, the adversarial probe sets, the forty probes and 113 mutations from the third review, the independent audit's 175 probes, 159 mutations of the clearance grammar's classes, 111 of the residual classes, 86 of the checker residuals, 55 of the 10 October 2026 classes (a season word, a quoted title, a financial subject, and the structural, approximation, sign, size and share classes), the boundary cases, and the four sample cases end to end |
| `tests/run-checker-tests.cjs` | Runs them against `checker.html` itself, with no browser |
| `tools/findings.py` | Reads the responses export and writes the findings and every field the readout names |
| `tools/make-sample-csv.py`, `tools/findings-sample.csv` | A synthetic response set in the shapes the page posts, so the script can be proved without waiting for participants |

### Audit

| File | What it is |
| --- | --- |
| `audit/RELEASE-QA-2026-09-13.md` | This release's QA: 38 screens at six widths, both independent reviews item by item, and the consistency sweep |
| `audit/INDEPENDENT-AUDIT-2026-09-13.md` | The independent adversarial audit: the third review's findings at the tested head, and 19 new defects with their inputs |
| `audit/CLEARANCE-GRAMMAR-2026-09-13.md` | What the clearance grammar changed, the audit's 175 probes before and after, and the classes it left open |
| `audit/AUTHOR-REPAIR-2026-09-13.md`, `audit/PREPICKS-2026-09-13.md`, `audit/FINDINGS-AND-LOCK-2026-09-13.md`, `audit/USABILITY-BY-EYE-2026-09-13.md` | The repairs to the author page, the read before the draft, the findings and the written-answer lock, and what looking at every page at six widths found |
| `audit/accessibility-2026-09-13.md` | The accessibility pass |
| `audit/performance-2026-09-13.md` | The performance pass |
| `screenshots/release/` | 76 screens at 375 and 1280, one per state walked |
| `screenshots/` | Earlier passes, kept as the record of what each revision looked like |
