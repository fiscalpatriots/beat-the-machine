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
| Ledger | One account per line: account number (optional), account name, prior balance, current balance. Tab separated, comma separated, or column aligned with two or more spaces. Dollar signs, thousands commas and (parentheses) for negatives are read. A header row is ignored and named in a note. Extra trailing columns such as variance and percent are ignored, since both are recomputed. |
| Memo | The drafted commentary as free text. A line beginning with a label such as `S1.` or `T3)` is kept whole, so a sentence that runs to two sentences stays one unit. Anything else is split at sentence boundaries and labelled S1, S2 and on. |
| Ratios (optional) | One per line, `Name = (4000 - 5000) / 4000`. Account numbers only, with plus, minus, times, divide and parentheses. Each ratio is computed for the prior month, the current month and the change between them, and expressed as a percent. |
| Thresholds | A dollar floor (default $25,000), a percent floor (default 10), and the rule: **both legs** or **either leg**. |
| Close period, memo version | Free text. They ride along in the CSV export so a filed log says which close it came from. |

## The six checks, in the order they run

1. **Recompute.** Change and percent for every line, from the balances only, and whether the line
   clears the rule.
2. **Sentence to account.** Four tiers, strongest first: an account number written in the
   sentence, a dollar figure equal to a prior, current or change balance, the account name (or
   its first two words) written out, and last a single distinctive word from the account name.
   The strongest tier that hits wins, so an exact figure beats a stray word. A sentence that hits
   nothing is listed **Unmatched, review by hand**.
3. **Arithmetic.** Every dollar figure in a sentence is compared with the prior, current and
   change of the accounts it matched, to the cent. A figure that matches none is a **FAIL** with
   the nearest ledger figure printed beside it ("memo says $6,500; ledger change is $65,000").
   Every percent is tested first against the matched line's own percent change, then against
   every ratio for both months and for the change between them, within 0.05 of a percentage
   point. A percent that matches nothing is **REVIEW**, never a hard fail: it prints "not a line
   percent" with the three closest candidates, because a ratio the checker was not told about is
   the likeliest explanation.
4. **Direction.** The words rose, rise, increased, grew, growth, up, higher, climbed, gained and
   jumped against fell, fall, declined, decreased, down, lower, dropped, reduced and shrank,
   tested against the sign of the movement. A direction word is only tested inside a clause that
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
- **One currency, one pair of periods.** No translation, no consolidation, no three-month
  columns.
- **It does not decide.** It never says a memo is fit to release. A reviewer signs.

## Using it in a close

Run it **first**, before anybody reads the memo, and read the findings in order: the FAILs go
back to the preparer, the SILENT lines go to the controller as a question, and then read only the
reviewer queue. **Copy results as table** pastes into a spreadsheet or an email. **Download CSV**
writes the column order of `EVIDENCE-LOG-TEMPLATE.csv`, so an exported run drops into the evidence
log with the reviewer columns left blank for the person who signs. **Copy the reviewer prompt**
assembles the ledger, the memo and the two questions for the surviving sentences into a prompt for
whichever AI tool the firm already uses, with an instruction not to recompute what has been
computed. Copy is the reliable path; a download can be blocked inside an embedded viewer.

Two links open the page with a case already run: `checker.html?sample=halyard` and
`checker.html?sample=ridgeline`.

## The Halyard sample, expected against actual

The **Load the Halyard sample** button fills both panes with the fourteen-account June 2026 ledger
and the twelve memo sentences of `EXERCISE-case-01-form-rev4.md`, plus S0, which is the sentence
the game carries on card 1 rather than in the memo block. The ratio pane is prefilled with
`Product gross margin = (4000 - 5000) / 4000`. Thresholds $25,000 and 10 percent, both legs.

Expected, and confirmed row by row against the page on 12 September 2026:

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

## A second ledger, to show it is not tuned to Halyard

**Load a second, unrelated ledger** runs five made-up accounts and three sentences for Ridgeline,
July 2026 against June. Expected and confirmed: 5 lines checked, 1 arithmetic fail, 1 direction
fail, 1 silent line, 1 sentence for the reviewer.

| Line | Result |
| --- | --- |
| T1, consulting revenue rose $61,000 | matched 4300 by amount, arithmetic PASS, direction PASS, into the reviewer queue |
| T2, subcontractor costs "increased" $32,000 | matched 5200 by amount, arithmetic PASS, direction **FAIL**: the account fell $32,000 |
| T3, travel and entertainment rose $9,400 | matched 6600 by name, arithmetic **FAIL**: the change is $7,400. **INFO**, below the rule |
| 6700 Insurance, $52,000 and 118.2 percent | **SILENT**, no sentence anywhere in the memo |
| 1000 Cash, $23,500 and 5.7 percent | below the rule, nothing owed, nothing said |

## Bad input

An empty or unreadable ledger returns a message naming what the pane expects, never a blank page.
Lines the reader could not use are listed by line number with the reason, and the run continues on
the lines it could read. A ratio naming an account that is not in the ledger, or dividing by zero,
is named and left out, and the rest of the run is unaffected.

---

Built by Khaled Alkurd. A drill for the AI-native accounting student. The protocol a reviewer
works from is [PROTOCOL.md](PROTOCOL.md), the log it fills in is
[EVIDENCE-LOG-TEMPLATE.csv](EVIDENCE-LOG-TEMPLATE.csv), and the game is
[index.html](https://fiscalpatriots.github.io/beat-the-machine/).
