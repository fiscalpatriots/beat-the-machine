# Second Pass Checker

`checker.html`, live at https://fiscalpatriots.github.io/beat-the-machine/checker.html

The game at [index.html](index.html) trains a reviewer on fourteen lines of one case. This page is
the tool that came out of it. Paste any ledger and any drafted commentary, press **Run Second
Pass**, and the mechanical work is done before a person reads a word. What comes back is a table
of findings and a short queue of questions that a person still has to answer.

One HTML file, no libraries, no build step, no network calls and no storage. **Nothing you paste
leaves the page.** It is read by the script in your own browser, and closing the tab is the whole
retention policy. That line is printed on the page itself, because a controller is entitled to
know it before pasting a trial balance into a web page.

## What goes in

| Pane | What it takes |
| --- | --- |
| Ledger | Four shapes, told apart by the reader itself. **Plain:** one account per line, account number (optional), account name, prior balance, current balance, tab separated, comma separated or column aligned with two or more spaces. **QuickBooks Online Profit and Loss Comparison:** the title block, an account label of the form `4000 Recurring managed services` in the first column, the two period columns and the `$ change` and `% change` columns that the report's Calculations dropdown adds, with `Income`, `Cost of Goods Sold` and `Expenses` as section headers and `Total ...`, `Gross Profit`, `Net Operating Income` and `Net Income` as totals. **Xero Income Statement with a comparison period:** `Income`, `Less Cost of Sales`, `Gross Profit`, `Less Operating Expenses`, `Net Profit`, each section closed by its own `Total` row. **Anything in between.** Dollar signs, thousands commas and (parentheses) for negatives are read. |
| Memo | The drafted commentary as free text. A line beginning with a label such as `S1.`, `1.`, `(a)`, `a)` or a bullet is kept whole, so a numbered item that runs to two sentences stays one unit. Anything else is split at sentence boundaries and labelled S1, S2 and on. Word's curly quotes, en and em dashes and ellipsis are flattened first. |
| Ratios (optional) | One per line, `Name = (4000 - 5000) / 4000`. Account numbers only, with plus, minus, times, divide and parentheses. Each ratio is computed for the prior month, the current month and the change between them, and expressed as a percent. |
| Thresholds | A dollar floor (default $25,000), a percent floor (default 10), and the rule: **both legs** or **either leg**. |
| Close period, memo version, company or file name, reviewer name | Free text. They ride along in the CSV export and print at the head of the review summary, so a filed log says which close it came from and who signed it. |

## The parse preview, before anything is checked

The ledger pane writes a **parse preview** as you type, and it is the first thing to read. It names
the shape it thinks it has, how many account lines it found, how many numeric columns the ledger
runs and which two it took as the periods, how many total rows it held back, the sections it found,
and every row it did not treat as an account line, by line number, with the reason.

Two dropdowns sit above it: **prior period column** and **current period column**, listing every
numeric column the ledger carries, with computed columns marked as such. They are prefilled by the
reader's own guess and changing either one re-runs the checks. The guess reads, in order: a header
word (`prior`, `previous`, `last month`, `PY`, `PP`, `budget` against `current`, `this month`,
`actual`, `YTD`); then the calendar, so `Jul 2026` before `Jun 2026` in a QuickBooks export is
still read as current-then-prior and put the right way round; then left to right. Columns whose
header says `change`, `variance`, `%` or `pct` are never guessed as a period, only offered.

A header row is matched to the numeric columns from the right, so it does not matter how many label
columns sit in front of them or in what order the headers read, only that they are recognisable.

## The six checks, in the order they run

1. **Recompute, and tie the section totals.** Change and percent for every line, from the balances
   only, and whether the line clears the rule. A line with a zero prior balance prints **new line**
   rather than a percent, because a percent of nothing is undefined, and its percent leg is read as
   met by any movement at all. Then every `Total ...` row is recomputed from the lines standing
   under its section and flagged **DOES NOT TIE** when the two disagree by more than a cent, which
   is what a half copied paste looks like. Totals computed across sections, `Gross Profit`,
   `Net Operating Income`, `Net Income`, `Net Profit`, are printed as **KEPT OUT** and not
   recomputed, because they are not the sum of a section.
2. **Sentence to account.** Four tiers, strongest first: an account number written in the
   sentence, a dollar figure equal to a prior, current or change balance, the account name (or
   its first two words) written out, and last a single distinctive word from the account name.
   The strongest tier that hits wins, so an exact figure beats a stray word. A sentence that hits
   nothing is listed **Unmatched, review by hand**.
3. **Arithmetic.** Figures are read as `$65,000`, `65,000`, `(65,000)`, `$65k`, `$65K`, `$1.2M`
   and `65k`, and percents as `7%`, `7 percent`, `7 per cent` and `7 pct`. Every dollar figure in a
   sentence is compared with the prior, current and change of the accounts it matched, to the cent. A figure that matches none is a **FAIL** with
   the nearest ledger figure printed beside it ("memo says $6,500; ledger change is $65,000").
   Every percent is tested first against the matched line's own percent change, then against
   every ratio for both months and for the change between them, within 0.05 of a percentage
   point. A percent that matches nothing is **REVIEW**, never a hard fail: it prints "not a line
   percent" with the three closest candidates, because a ratio the checker was not told about is
   the likeliest explanation.
4. **Direction.** The words rose, rise, increased, grew, growth, up, higher, climbed, gained,
   jumped, advanced, expanded, surged and accelerated against fell, fall, declined, decreased,
   down, lower, dropped, reduced, shrank, eased, softened, slipped and receded, tested against the
   sign of the movement. **Flat is a direction too:** flat, unchanged, steady, level with, unmoved,
   no change, no movement, held flat, held steady and held at, tested against a movement inside
   half a percent of zero, and failed outside it. A sentence that says an account rose or fell when
   the balance did not move at all is a **FAIL**. A direction word is only tested inside a clause that
   carries a figure tying to a matched account, so "on a shift toward lower margin lines" is not
   read as a claim about the account. Where no clause carries such a figure, the sentence's
   direction words are tested against the matched accounts as a whole. A mismatch is a **FAIL**.
5. **Threshold and silence.** Every line that clears the rule with no sentence matched to it is
   **SILENT** and owes an explanation. Every sentence whose accounts all fall below the rule is
   **INFO**, "no commentary owed; fine if correct", and its figures and direction are still
   checked, because a sentence that owes nothing can still say something false.
6. **Reviewer queue.** Every sentence that passed 3 and 4 gets the same two questions printed
   beside it, and a line with two or more sentences on it gets one added row, "Read together: N
   sentences on this account".

Above the table: lines checked, arithmetic fails, direction fails, silent lines, sentences for
the reviewer.

## What it does not do

- **No judgment on drivers.** It cannot tell whether the Tri-State depot ramp is real. That is
  why every surviving sentence carries the question rather than a verdict.
- **No judgment on timing.** Whether revenue belongs in this month is a question about contracts
  and shipping dates, not about balances.
- **No contradiction detection.** Two sentences that cannot both be true will both pass. The
  checker says only that they landed on the same account and must be read together.
- **No fuzzy matching.** No stemming, no synonyms and no guessing: "depot" does not match
  "depots". A sentence that names nothing the ledger names comes back unmatched, on purpose.
- **One currency, one pair of periods.** No translation, no consolidation. A ledger may carry
  more than two numeric columns and the dropdowns will pick any two of them, but only two are ever
  checked, and a twelve month statement is read as whichever pair you name.
- **No opinion on a total it cannot rebuild.** Gross Profit, Net Operating Income, Net Income and
  Net Profit are printed and left alone. Only a `Total ...` row standing directly under a section
  of lines is recomputed.
- **Indentation is not read.** A section header is recognised by its words, not by how far it is
  indented, so a report whose sections are named something the reader does not know comes through
  as lines with no section and no totals tie. Every line is still checked.
- **A closing sentence is unmatched by design.** "Four lines fell below the rule and carry no
  commentary" names no account, so it comes back **Unmatched, review by hand**. That is the right
  answer for a sentence that ties to nothing, and a reviewer glances at it and moves on.
- **No file upload.** Everything arrives by paste. An `.xlsx` is opened in Excel and the cells
  copied across; the reader takes the tabs that come with them.
- **It does not decide.** It never says a memo is fit to release. A reviewer signs.

## Using it in a close

Run it **first**, before anybody reads the memo, and read the findings in order: the FAILs go
back to the preparer, the SILENT lines go to the controller as a question, and then read only the
reviewer queue.

**Print review summary** opens the browser's print dialog on a print stylesheet that hides the
whole working page and prints a single document: a header carrying the company or file name, the
close period, the memo version, the date and the reviewer name, then the summary strip, then the
full results table, then the reviewer's queue with every sentence, its line, and two blank rules to
write the driver answer and the timing answer on, then the silent lines with a blank rule each,
then the evidence list from `PROTOCOL.md`, then a signature block for the second-pass reviewer and
for the controller. Print it to PDF and it is the retained evidence the protocol asks for, in one
file.

**Copy results as table** pastes into a spreadsheet or an email. **Download CSV** writes the column
order of `EVIDENCE-LOG-TEMPLATE.csv`, so an exported run drops into the evidence log with the
reviewer columns left blank for the person who signs. Copy is the reliable path; a download can be
blocked inside an embedded viewer.

## The two prompts

The checker sits between them, and both are on the page with a Copy button.

**Prompt 1, draft the memo**, is used before the memo exists. It carries the ledger and the
threshold to whichever AI tool the firm already uses, and fixes the shape of every line:

> `<n>. <account number> <account name>: prior <prior>, current <current>, <rose or fell or flat>
> <change>, <percent> percent, because <one reason> (source: <the document the reason came from>).`

with instructions to write nothing about a line below the threshold except one closing sentence,
to write figures in full dollars rather than k or M, and to write "no source on file" rather than
invent one. **The shape is not a preference.** An account number written out is the strongest tier
of the match; full-dollar figures tie to the cent; and a direction word standing immediately beside
the change figure is the only place the direction check reads it, because a direction word is only
tested inside a clause that carries a figure. A memo drafted this way runs clean: matched by
account number, arithmetic PASS, direction PASS, and straight into the reviewer's queue.

**Prompt 2, second pass**, is the reviewer prompt, and it needs a run first. It assembles the
ledger, the memo and the two questions for only the surviving sentences, with an instruction not to
recompute what has been computed.

Four links open the page with a case already run: `checker.html?sample=halyard`,
`?sample=brightwater`, `?sample=kestrel` and `?sample=ridgeline`.

## The four samples

The **Samples** dropdown carries four cases, and each one loads both panes, the ratio pane, the
thresholds and the close period, then runs. Every expected result below was confirmed row by row
against the page on 13 September 2026, with no console error on any run.

## The Halyard sample, expected against actual

**Halyard Distribution, June 2026** fills both panes with the fourteen-account June 2026 ledger
and the twelve memo sentences of `EXERCISE-case-01-form-rev4.md`, plus S0, which is the sentence
the game carries on card 1 rather than in the memo block. The ratio pane is prefilled with
`Product gross margin = (4000 - 5000) / 4000`. Thresholds $25,000 and 10 percent, both legs.

Expected, and confirmed row by row against the page again on 13 September 2026:

| Line | Matched | Arithmetic | Direction | Threshold | Reviewer queue |
| --- | --- | --- | --- | --- | --- |
| S0 | 4200, by amount | **FAIL**, memo says $6,500, ledger change is $65,000. The 3.5 percent is **REVIEW**, not a line percent | PASS, "fell" agrees | clears | no, it failed |
| S1 | 6200, by amount | PASS, $118,600 is the current balance | not stated | clears | yes, and read together with S10 |
| S2 | 6400, by name | **FAIL**, memo says $42,000, ledger change is $47,000 | PASS, "increased" agrees | clears | no, it failed |
| S3 | 6300, by amount | PASS, $1,600 is the change | PASS, "rose" agrees | **INFO** | yes |
| S4 | 4000, by amount | PASS, $5,612,000 and 7.1 percent both tie | PASS, "grew" agrees | **INFO** | yes |
| S5 | 4000 and 4100, by a name word | no figures | PASS, "growth" agrees | owed, 4100 clears | yes, and read together |
| S6 | 5100, by amount | PASS, $287,800 is the current balance | **FAIL**, memo says "declined", 5100 rose $73,800 | clears | no, it failed |
| S7 | 7100, by amount | PASS, $31,200 is the change | PASS, "rose" agrees | clears | yes |
| S8 | 6100, by amount | PASS, $5,200 is the change | PASS, "fell" and "lower" agree | **INFO** | yes |
| S9 | 4100, by amount | PASS, $229,000 is the change | PASS, "rose" agrees | clears | yes, and read together with S5 |
| S10 | 6200, by a name word | no figures | not stated | clears | yes, and read together with S1 |
| S11 | 4000 and 5000, by amount | PASS, $348,000 and $372,000 tie, and 25.0 and 23.8 percent tie to the gross margin ratio for May and June | PASS, "rose" and "rise" agree | **INFO** | yes, and read together |
| S12 | 6500, by amount | PASS, $7,500 is the change | PASS, "fell" agrees | **INFO** | yes |
| 6000 Warehouse wages | no sentence | | | **SILENT**, $72,500 and 11.5 percent | asked of the controller |

Summary strip: **14** lines checked, **2** arithmetic fails, **1** direction fail, **1** silent
line, **10** sentences for the reviewer. No console errors on any run.

Three results are worth naming because they are wider than the case that prompted them:

- **S11 passes on the ratio, not on the line.** 25.0 and 23.8 percent are a gross margin across
  two accounts, and neither is the percent change of either line. Without the ratio pane they
  would come back REVIEW with the nearest three candidates printed, which is the honest answer for
  a checker that has not been told what the percent measures.
- **S4 and S11 read INFO alongside S3, S8 and S12.** Accounts 4000 and 5000 clear the dollar leg
  and fail the percent leg, so under the both-legs rule no commentary is owed on either, however
  large the dollars look. The sentences are still checked and still go to the reviewer.
- **Read together fires three times**, on 4000 (S4, S5, S11), on 4100 (S5, S9) and on 6200 (S1,
  S10). Only the last pair is the contradiction the game plants. The checker does not know which
  is which, and says so rather than guessing.

## Brightwater Dental Partners, June 2026, the round two case

**Brightwater Dental Partners** is the five-account, five-sentence dental group the game scores a
player on cold, from `EXERCISE-round-two-rev1.md`. A plain tab separated ledger with a two column
header, `Account / May 2026 / June 2026`, read chronologically. Thresholds $25,000 and 10 percent,
both legs, no ratios.

Expected and confirmed: **5** lines checked, **1** arithmetic fail, **1** direction fail, **0**
silent lines, **3** sentences for the reviewer.

| Line | Result |
| --- | --- |
| 4010 Patient service revenue, net | $61,500 and 8.3 percent, **below the rule**: the largest dollar movement on the statement owes nothing, because the percent leg is not met |
| 4220 Orthodontic plan revenue | $42,400 and 44.2 percent, clears |
| 5210 Dental supplies and lab fees | $52,700 and 38.1 percent, clears |
| 6110 Hygienist wages | $54,900 and 25.7 percent, clears |
| 6610 Marketing and patient outreach | $5,700 and 31.0 percent, **below the rule**: a large percentage of a small balance is still a small number |
| B1, supplies "eased to $191,200" | matched 5210 by amount, arithmetic PASS, direction **FAIL**: the account rose $52,700, 38.1 percent |
| B2, patient revenue rose $61,500, 8.3 percent | matched 4010 by amount, both figures PASS, direction PASS, **INFO**, into the queue |
| B3, orthodontic plans taken to revenue in June | matched 4220 by amount, arithmetic PASS, direction not stated, clears, into the queue |
| B4, marketing rose $5,700, 31.0 percent | matched 6610 by amount, both figures PASS, direction PASS, **INFO**, into the queue |
| B5, hygienist wages "increased $44,900" | matched 6110 by account name, arithmetic **FAIL**: the change is $54,900, so $10,000 is left with no reason attached |

**B3 is the one the checker cannot catch, and it prints that.** The exercise plants a timing error
there: $38,500 of orthodontic fees collected in June pays for treatment that starts in July. Every
figure in the sentence ties and no direction is claimed, so it passes the mechanical checks and
goes to the reviewer with the timing question printed beside it. That is the whole design.

## Kestrel IT Services, July 2026, a QuickBooks export

**Kestrel IT Services** is a six-account managed services firm pasted in the shape QuickBooks
Online's Profit and Loss Comparison exports: a three line title block, the account number and name
in one first column cell, **the current period column before the comparison period**, and the
`$ Change` and `% Change` columns the Calculations dropdown adds. Sections `Income`,
`Cost of Goods Sold` and `Expenses`, with `Total ...` rows, `Gross Profit`, `Net Operating Income`
and `Net Income`. Thresholds $25,000 and 10 percent, both legs, no ratios.

The reader takes four numeric columns, marks `$ Change` and `% Change` as computed, reads
`Jul 2026` and `Jun 2026` off the calendar and puts them the right way round, so the prior is the
second column and the current is the first. Six lines found, six total rows held back, three
sections, four rows ignored as title and header.

Expected and confirmed: **6** lines checked, **1** arithmetic fail, **1** direction fail, **1**
silent line, **4** sentences for the reviewer.

| Line | Result |
| --- | --- |
| 4000 Recurring managed services | $36,900 and 22.8 percent, clears, and **SILENT**: no sentence in the memo touches it |
| 4100 Project and implementation revenue | $57,500 and 147.8 percent, clears |
| 5000 Subcontracted engineering | $46,500 and 111.2 percent, clears |
| 6000 Salaries and wages | $0 and 0.0 percent, below the rule |
| 6200 Software licences and hosting | $35,300 and 156.2 percent, clears |
| 6400 Client acquisition costs | $9,300 and 189.8 percent, below the rule |
| Total Income, Total Cost of Goods Sold, Total Expenses | all three **TIE** to the lines under them |
| Gross Profit, Net Operating Income, Net Income | **KEPT OUT**, computed across sections |
| 1, project revenue rose **$57.5k** to $96,400, up 147.8 percent | matched 4100 by account number, all three figures PASS, direction PASS, into the queue |
| 2, project revenue carries the final Riverbend milestone | matched 4100 by account name, no figures, into the queue, and **read together** with line 1 |
| 3, subcontracted engineering "fell $46,500" | matched 5000 by account number, arithmetic PASS, direction **FAIL**: the account rose $46,500 |
| 4, salaries "held flat at $88,500" | matched 6000 by account number, arithmetic PASS, direction PASS on the flat test, **INFO** |
| 5, software licences rose **$25,300** to $57,900 | matched 6200 by account number, arithmetic **FAIL**: the change is $35,300, and the nearest ledger figure printed is the $22,600 prior balance |
| 6, client acquisition rose $9,300, 189.8 percent | matched 6400 by account number, both PASS, **INFO** |

Two problems are planted, one of each kind the mechanical checks can settle: **line 3 has the
movement backwards** and **line 5 is $10,000 short of the change it claims**. The third finding is
the one nobody wrote: **4000 clears the rule and the memo never mentions it**. The sample exists to
show a QuickBooks paste going in whole, so it also carries the `$57.5k` figure, the `held flat`
direction and the totals tie in the same run.

## A second ledger, to show it is not tuned to Halyard

**Ridgeline Partners, July 2026** runs five made-up accounts and three sentences against June, in a
plain comma separated ledger with no header row at all. Expected and confirmed: 5 lines checked, 1 arithmetic fail, 1 direction
fail, 1 silent line, 1 sentence for the reviewer.

| Line | Result |
| --- | --- |
| T1, consulting revenue rose $61,000 | matched 4300 by amount, arithmetic PASS, direction PASS, into the reviewer queue |
| T2, subcontractor costs "increased" $32,000 | matched 5200 by amount, arithmetic PASS, direction **FAIL**: the account fell $32,000 |
| T3, travel and entertainment rose $9,400 | matched 6600 by name, arithmetic **FAIL**: the change is $7,400. **INFO**, below the rule |
| 6700 Insurance, $52,000 and 118.2 percent | **SILENT**, no sentence anywhere in the memo |
| 1000 Cash, $23,500 and 5.7 percent | below the rule, nothing owed, nothing said |

## Bad input, and what each case prints

Every one of these was run on 13 September 2026. None of them writes to the console, and none of
them leaves a blank page.

| Input | What comes back |
| --- | --- |
| Both panes empty | "Both panes are empty", naming which pane takes what, and pointing at Samples |
| Memo only, no ledger | "There is nothing to check a figure against until a ledger is pasted" |
| Ledger with no numeric columns | The count of rows read, the rule that every account line needs two numbers on it, and the parse preview listing every row it could not use |
| Memo with no figures at all | The run completes. The matching, the direction and the silence all run, and a note says the arithmetic check had nothing to test |
| Duplicate account numbers | A note naming them. Every line is checked on its own, a sentence naming that number matches all of them, and a ratio using it reads the first |
| Negative balances | Read from a minus sign or from (parentheses). A move from -$120,000 to -$180,000 is a change of -$60,000 and -50.0 percent, and a memo that calls it a rise **FAILS** |
| Zero prior balance | The percent prints **new line** rather than a number, because a percent of nothing is undefined, and the percent leg is read as met by any movement |
| A section total that does not tie | **DOES NOT TIE**, with both sums and both totals printed, and a warning above the table to check the paste before reading anything else |
| Prior and current set to the same column | Refused in one line, and the guess is put back |
| A ratio naming an account that is not in the ledger, or dividing by zero | Named, left out, and the rest of the run is unaffected |

Lines the reader could not use are always listed by line number with the reason, in the parse
preview and again above the results, and the run continues on the lines it could read.

---

Built by Khaled Alkurd. A drill for the AI-native accounting student. The protocol a reviewer
works from is [PROTOCOL.md](PROTOCOL.md), the log it fills in is
[EVIDENCE-LOG-TEMPLATE.csv](EVIDENCE-LOG-TEMPLATE.csv), the spreadsheet version is
[Second-Pass-Excel-Template.xlsx](Second-Pass-Excel-Template.xlsx), the guide for running it with a
room is [Second-Pass-Facilitator-Guide.pdf](Second-Pass-Facilitator-Guide.pdf), where every number
came from is [PROVENANCE.md](PROVENANCE.md), and the game is
[index.html](https://fiscalpatriots.github.io/beat-the-machine/).
