# Second Pass Checker

`checker.html`, live at https://fiscalpatriots.github.io/beat-the-machine/checker.html

The game at [index.html](index.html) trains a reviewer on fourteen lines of one case. This page is
the tool that came out of it. Paste any ledger and any drafted commentary, press **Run Second
Pass**, and the mechanical work is done before a person reads a word. What comes back is a table
of findings and a short queue of questions that a person still has to answer.

One HTML file and no libraries. **Where your data goes**, printed on the page itself because a
controller is entitled to know it before pasting a trial balance into a web page: this page is
served from GitHub Pages and loads one Google font from fonts.googleapis.com; everything you paste
is processed by the script in your own browser, this page stores nothing on a server, and anything
you copy from here into another AI service goes to that service under its terms. The font request is
the one network call the page makes, and it carries no ledger data.

## What goes in

| Pane | What it takes |
| --- | --- |
| Ledger | Four shapes, told apart by the reader itself. **Plain:** one account per line, account number (optional), account name, prior balance, current balance, tab separated, comma separated or column aligned with two or more spaces. **QuickBooks Online Profit and Loss Comparison:** the title block, an account label of the form `4000 Recurring managed services` in the first column, the two period columns and the `$ change` and `% change` columns that the report's Calculations dropdown adds, with `Income`, `Cost of Goods Sold` and `Expenses` as section headers and `Total ...`, `Gross Profit`, `Net Operating Income` and `Net Income` as totals. **Xero Income Statement with a comparison period:** `Income`, `Less Cost of Sales`, `Gross Profit`, `Less Operating Expenses`, `Net Profit`, each section closed by its own `Total` row. **Anything in between.** Dollar signs, thousands commas and (parentheses) for negatives are read. |
| Memo | The drafted commentary as free text. A line beginning with a label such as `S1.`, `1.`, `(a)`, `a)` or a bullet is kept whole, so a numbered item that runs to two sentences stays one unit. Anything else is split at sentence boundaries and labelled S1, S2 and on. Word's curly quotes, en and em dashes and ellipsis are flattened first. |
| Ratios (optional) | One per line, `Name = (4000 - 5000) / 4000`. Account numbers only, with plus, minus, times, divide and parentheses. Each ratio is computed for the prior month, the current month and the change between them, and expressed as a percent. |
| Thresholds | A dollar floor (default $25,000) and a percent floor (default 10), each wearing its unit, and the rule as a two-way control: **both legs** or **either leg**. The dollar rule is **more than** the floor and the percent rule is **at least** the floor, both decided unrounded. |
| Zero prior balance | An explicit policy on a two-way control, because a percent of nothing does not exist: **owes commentary** on any movement (the default) or **excluded** from the rule. |
| Close period, memo version, company or file name, reviewer name | Free text. They ride along in the CSV export and print at the head of the review summary, so a filed log says which close it came from and who signed it. |

## The controls on the page

The page opens on one sentence and three numbered steps, paste the ledger, paste the memo, read the
queue, and then shows a screenshot of the Halyard run under them, so a first-time reader sees what
comes back before deciding whether to paste anything.

| Control | Where it is, and what it does |
| --- | --- |
| **Load sample** | In each pane's own header. It fills that pane alone with the Halyard case, which is the way to see one shape without disturbing the other pane. |
| **Character count** | Beside it, so a long paste is visibly in the box. |
| **Placeholder** | Two lines in each pane, showing the shapes that are accepted: a tab separated ledger line and a comma separated one, a numbered memo line and a labelled one. |
| **Dollar floor, percent floor** | Numbers wearing their `$` and `%`. |
| **Rule, zero prior balance** | Two-way controls rather than dropdowns, because each has exactly two settings and both are worth reading at a glance. |
| **Run Second Pass** | The green button, with **Ctrl and Enter** beside it, which runs from anywhere on the page; on a Mac it reads Command and Enter. A run that ever took longer than a tenth of a second draws a line across the top of the page, and on anything a student pastes it never does. |
| **Samples** | The four cases, loaded and run in one step. |
| **Clear** | Empties every pane and every name, and puts the empty state back. |
| **Before a run** | A quiet panel with a ledger sheet, a memo sheet and a check mark, and one line saying nothing has been checked yet. It goes as soon as a run paints results over it. |

**Nothing on this page scrolls sideways**, at 320, 375, 390, 768, 1024, 1280 or 1600. The ledger
pane keeps a monospace face and wraps a long line under itself rather than shrinking the type or
running off the edge; the results table and the parse preview sit on percentage columns above 760
and stack into labelled rows below it. It is verified by measuring `scrollWidth` against
`clientWidth` on every element at every one of those widths, not just on the page.

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

## The contract

Six steps, kept apart on purpose, and each one reported in its own right on the page. A number that
appears in both the memo and the ledger proves only that the number exists in both places. It does
not prove that the sentence uses it correctly, and an earlier version of this page treated the two
as the same thing. They are not.

1. **Extraction.** Every figure is read with the span of text it came from, its value and its unit.
   Dollars are read as `$65,000`, `65,000`, `(65,000)`, `$65k`, `$65K`, `$1.2M`, `65k` and, since an
   ordinary number is still a number, `90000` and `-30000`; a bare number is read only at four digits
   or more. Percents are read as `7%`, `7 percent`, `7 per cent` and `7 pct`. Percentage points are a
   **separate unit**, read from `pp` and `percentage point`. A figure is negative when a minus sign
   or a closed pair of parentheses says so, **and a minus sign in front of a bare number is part of
   the figure**; a lone opening bracket, as in `rose $30,000 (30%)`, is punctuation and the percent
   inside it is read normally.
1b. **Unparsed spans.** Anything numeric the accepted grammar cannot read is recorded rather than
   dropped. Four kinds: a **currency that is not the dollar** (`€30,000`, `£30,000`, `USD 90000`), a
   **scale or multiplier word the grammar does not carry** (`$30.0 thousand`, `30 thousand`, `0.30
   times`, `30 basis points`), a **quantity in words the grammar cannot resolve or that carries no
   unit** (`a rise of thirty thousand`, `one third of the prior balance`, `two billion dollars`), and
   a **run of digits standing where the words put a claim** that the figure reader did not take
   (`increased by 800`, `increased by 1999`, `increased by 6200`). An unparsed span marks the
   sentence **not checked** and goes to the reviewer's queue with the reason. A year or an account
   number standing in an ordinary position, `finished on June 30`, `billed on 31 July`, `against
   $18,000 in June 2025`, is not a claim and is left where it stands. The external review of 13
   September 2026 asked for *needs review* here; the page says **not checked**, which is the
   stronger of the two: nothing in the sentence was settled.
1c. **Quantities written in words.** Units through millions are read: `thirty`, `thirty-one`,
   `ninety`, `one hundred twenty-five thousand`, `two million`. A run is parsed to a figure and
   compared like any other **only where both hold**: the parser resolves the run, and the words
   beside it give it a unit (`dollars`, `percent`, `per cent`, `pct`, `%`, `percentage points`,
   `pp`). So `rose thirty thousand dollars` is compared as $30,000 and `a change of ninety percent`
   is compared as 90 percent and fails a ledger that moved 30 percent. A run the parser cannot
   resolve, a fraction (`one third`), and anything above a million go to the queue wherever they
   stand. A resolved run with **no unit word** goes to the queue where the words put a claim
   (`a rise of thirty thousand`) and is left alone where they do not: `the thirty-one new
   orthodontic plans` is a count, not a figure about the account, and it does not make a true
   sentence unresolved. That is the same test a bare run of digits gets in 1b.
2. **Account binding.** Three routes, each named on the page: **by account number**, **by account
   name**, and **by an exact figure**. The figure route is accepted only when the sentence also
   carries a word from that account's name that no named account shares. Where a figure ties to an
   account the sentence does not name in any other way, that is a **numeric coincidence**, and it is
   printed as an unresolved conflict rather than being bound. A duplicated account number binds
   nothing on its own: the sentence is held at needs review until a consolidation decision is made.
   A sentence that names **more than one account** binds each figure inside the **clause it was
   written in**, split on commas, semicolons and the joining words (`and`, `or`, `but`, `while`,
   `against`, `compared with`, `rather than`, `instead of`). A figure whose clause names exactly one
   of the bound accounts is tested against that one; a figure whose clause names none of them, or
   more than one, is a **binding conflict** and is held at needs review however well it agrees with
   the sentence read as a whole. A percent settled against a ratio supplied in the ratio pane is
   exempt, because no account binding settled it. An account number the memo **spends as an
   amount**, `increased by 6200`, is a claim and not a reference: it binds nothing, and it does not
   take that line off the silent list.
3. **Numeric role.** What the sentence says each figure *is*, read from the words beside it and
   never from the fact that it matches something: **prior balance** (`from $186,000`), **current
   balance** (`to $121,000`, `at $88,500`, `now`), **absolute movement** (`by $30,000`, `rose
   $31,200`, `a decrease of $6,500`, `a $372,000 rise`), **relative movement** (`grew 7.1 percent`,
   `or 31.0 percent`, `(30%)`, `8.3 percent of May`), **ratio** (`from 25.0 percent ... to 23.8
   percent`), or **unknown**. A role the words do not give is *unknown*, and a figure with an unknown
   role is never counted as checked, whatever it happens to equal: the row says so, a dropdown
   appears beside it listing the five roles, the reviewer confirms it, and the run is stamped again
   with the confirmation in it. A **sign** written into a figure is a claim the words did give, so a
   sign that disagrees with the ledger **fails** before an unknown role can hold it for review.
4. **Units.** Dollars, percent and percentage points are held apart. Percentage points measure a
   change in a rate, so a claim in points against a dollar balance is never tested against that
   balance's percent change; with no ratio supplied it is returned as needs review with that reason.
5. **Calculation.** Every comparison is unrounded. The **display tolerance** is half a cent on a
   dollar figure and 0.05 of a percentage point on a percent, which is what the rounding on screen
   needs and nothing more. Signs are preserved: a figure the memo writes with its own sign is
   compared as written and a sign clash is a failure that names both sides; a figure written as a
   magnitude is compared as a magnitude and the sign is left to the direction check, which owns it.
6. **Conclusion.** One status per sentence, below.

**Negation.** `not`, `no`, `never`, `neither`, `nor`, `without`, `rather than`, `instead of`,
`failed to` and the contracted forms **void** the direction claim and the figure claims in the
clause they attach to, and force **needs review**. A negation is not read as the claim it would be
without it and not as its opposite: the checker says it cannot settle the clause and a person does.
The threshold idioms a memo uses to say a line owes nothing, "no commentary is owed", "clears
neither leg", "carries no driver", "no change", are taken out before the test, and a clause with no
figure and no direction word is inert.

Two checks sit outside the six and are reported the same way. **Direction** tests rose, fell and
flat against the sign of the movement, inside a clause that carries a figure tying to a bound
account. **Threshold claims** test a sentence that asserts something about the rule itself, "fails
the dollar leg", "clears neither leg", "carries no driver", against the rule as set; it is the one
case where a sentence can be checked on its words rather than on a figure.

The ledger is checked first and separately: every line recomputed from its two balances, every
`Total ...` row rebuilt from the lines standing under its section, and every row the reader could
not use listed by line number with the reason.

## The four statuses

Every sentence gets exactly one, and **no later step may promote one upward**. The run keeps the
worst status any step assigned and the summary, the exports and the prompt all carry that one.

| Status | What it means |
| --- | --- |
| **Checked within scope** | Every figure in the sentence carried a role the words gave it, and the unrounded comparison with the pasted ledger agreed. It does not mean the sentence is true. |
| **Needs review** | Something is unresolved: a role the words do not give, a binding the checker will not settle by coincidence or by a clause naming two accounts, a duplicate account number, a percent it cannot compute, a clause the words negate, a column mapping nobody confirmed. A person has to answer it. |
| **Not checked** | Nothing in the sentence could be tied to the ledger and tested. An unmatched sentence, a sentence with no figures, and a sentence carrying an unparsed span all land here. This is **not** the same as a sentence that was checked and found true, and the page never prints it as one. |
| **Failed** | At least one check on the sentence failed. |

A sentence carrying no figures is **not checked** unless it makes a threshold claim, in which case
the claim itself is checked.

## Coverage, not a failure count

The results open with a **stacked bar** of the four sentence statuses in proportion, drawn in the
page's own tokens, which fills once when a run lands. Under it sit **four tiles** carrying the four
marks and their counts: a green check for checked within scope, an ink square for needs review, a
soft ring for not checked, a red cross for failed. Each count runs up to its number over a fifth of
a second, and a reader whose system asks for less motion gets the number with no run-up. The same
four marks are the first column of the table, so a row, a tile and the bar say the same thing. A
line under the tiles carries the counts the bar does not: sentences read, ledger rows used, rows
skipped, silent lines, and the size of the reviewer queue. Under it the run identifier and the
source version, and, when a row was skipped, the statement that the ledger was not covered in full.

A row the ledger reader could not use is printed under the strip in a red box, by line number, with
the reason, on every run. Rows the reader drops on purpose, the header row and the title block above
a report, are not counted as skipped; a row that looks like an account line and could not be read is.

The **reviewer queue** carries every failure, every binding conflict, every unmatched sentence,
every skipped source row, every refused row, every malformed ratio, every unsupported numeric form,
every discarded numeric column, every silent line and every account carrying two or more sentences.
It is printed **below the table as a plain numbered list**, each item carrying the sentence, the
finding and the questions beneath it. Every question carries **Yes, No and Not on file** beside it,
and what a reviewer ticks rides out with the run: into the human conclusion column of the CSV, into
the JSON record as `reviewerAnswer`, and onto the line in the printed summary where an untouched
question prints a blank rule for a pen. The queue is also repeated verbatim in Prompt 2. The
table's own **Ask the controller** column carries the instruction in one imperative, and the
question itself is asked in full in the queue, which is where it gets answered. The reviewer queue now also carries **unparsed
figures**, **negated claims** and **binding conflicts**.

## The boundary policy

Stated on the page above the panes, and used unrounded:

- The **dollar rule is "more than"**. A change of exactly the floor does not clear the dollar leg.
- The **percent rule is "at least"**. A change of exactly the floor does clear the percent leg.
- Both legs are decided on the unrounded values, not on the figures as they print. A movement that
  displays as 10.0 percent and computes to 9.9997 percent does not clear a 10 percent floor.
- A **zero prior balance** has no percent at all, so it is settled by an explicit selected policy
  rather than a default nobody chose. The dropdown offers **owes commentary on any movement**, which
  is the default, and **excluded from the rule**. Whichever is selected is printed on the line, in
  the printed summary and in Prompt 2.

## The regression suite

```
node tests/run-checker-tests.cjs          every fixture
node tests/run-checker-tests.cjs T02      one fixture
node tests/run-checker-tests.cjs --dump T02
```

`tests/checker-fixtures.json` holds **fifty-nine** fixtures and **all fifty-nine pass**.

- **T01 to T17**, the seventeen probes from the external audit of 13 September 2026, each carrying
  the required behavior from that audit as the assertion, plus four boundary and export companions.
- **T18, T18b, T19**, the end-to-end sample runs, Halyard, Brightwater and Kestrel, which assert the
  expected outputs printed further down this file.
- **T20 to T43**, the twenty-four probes from the live release review of 13 September 2026, N01 to
  N24, entered exactly as that bundle supplied them. Seven of them are the review's own positive and
  negative controls and still clear or still fail; the rest are the clearances the review found. The
  five it named in its table are T20 (negation), T21 (a percentage written in words, which is now
  read and fails rather than being left unparsed), T26 (a dropped
  minus sign), T28 (amounts swapped between two named accounts) and T41 (a percent whose role the
  words do not give).
- **T44 to T48**, five further adversarial probes written against the repaired contract: a units
  mismatch (percentage points against a dollar line), a figure standing in a different sentence from
  its account, a percent of a subtotal the checker was never given, a currency written in thousands
  against a ledger in whole dollars, and a memo line quoting last year.
- **T49 to T54**, six probes on quantities written in words, written for the residue the release QA
  of 13 September 2026 found open: a resolved quantity with no unit standing where a claim stands
  (queued, sentence not checked), a fraction in words (queued), a quantity with a unit word that is
  true (cleared) and one that is false (failed), a hyphenated compound through the hundreds and
  thousands (`one hundred twenty-five thousand dollars`, read as $125,000), and a count in words
  standing where no claim stands, which must stay out of the queue.

The runner lifts the script out of `checker.html` and runs it against a document stub, so there is
no build step and no dependency; a change to the page that breaks a probe fails the suite. The four
sample cases produce output identical to the release the review examined.

## What it does not do

- **No judgment on drivers.** It cannot tell whether the Tri-State depot ramp is real. That is
  why every surviving sentence carries the question rather than a verdict.
- **No judgment on timing.** Whether revenue belongs in this month is a question about contracts
  and shipping dates, not about balances.
- **No contradiction detection.** Two sentences that cannot both be true can both be checked
  within scope. The checker says only that they landed on the same account and must be read
  together, and it puts that in the queue.
- **No reading of a negation.** It detects one and refuses the clause. It does not work out what
  "rent expense did not rise $30,000" asserts, and it never reads a negated claim as its opposite.
- **No second currency and no scale words.** `€30,000`, `USD 90000`, `$30.0 thousand`, `30 basis
  points` and `0.30 times the prior balance` are recorded as unparsed and the sentence is left
  unchecked. The page reads one currency, written in whole units with a dollar sign.
- **No quantities in words above a million, and none without a unit.** Units through millions are
  read where a unit word stands beside them (rule 1c). `two billion dollars`, `one third of the
  prior balance` and `a rise of thirty thousand` are unparsed spans, and the sentence is left
  unchecked.
- **No resolution of a clause naming two accounts.** It reports the binding conflict; it does not
  decide which line the figure belongs to.
- **No fuzzy matching.** No stemming, no synonyms and no guessing: "depot" does not match
  "depots". A sentence that names nothing the ledger names comes back unmatched, on purpose.
- **One currency, one pair of periods.** No translation, no consolidation. A ledger may carry
  more than two numeric columns and the dropdowns will pick any two of them, but only two are ever
  checked, and a twelve month statement is read as whichever pair you name.
- **No opinion on a total it cannot rebuild.** Gross Profit, Net Operating Income, Net Income and
  Net Profit are printed and left alone. Only a `Total ...` row standing directly under a section
  of lines is recomputed.
- **Indentation is not read.** A section header is recognized by its words, not by how far it is
  indented, so a report whose sections are named something the reader does not know comes through
  as lines with no section and no totals tie. Every line is still checked.
- **A closing sentence is unmatched by design.** "Four lines fell below the rule and carry no
  commentary" names no account, so it comes back **Unmatched, review by hand** and is counted as
  **not checked**. That is the right answer for a sentence that ties to nothing, and a reviewer
  glances at it and moves on.
- **It never promotes a status.** A sentence that failed or that needs review at any step stays
  there. Nothing later in the run, and nothing in the export or the prompt, can make it read as
  checked.
- **No file upload.** Everything arrives by paste. An `.xlsx` is opened in Excel and the cells
  copied across; the reader takes the tabs that come with them.
- **It does not decide.** It never says a memo is fit to release. A reviewer signs.

## Using it in a close

Run it **first**, before anybody reads the memo, and read the coverage strip before the table: how
much of the memo was checked at all is the first fact, not how many findings came back. Then read
the findings in order: the failures go back to the preparer, the silent lines go to the controller
as a question, the needs-review rows get a role confirmed or an ambiguity settled, and only then
read the sentences that were checked within scope.

The four things you do with a finished run sit in one **Actions** bar at the foot of the results:
Copy table, Download CSV, Print summary, Copy prompt. On a phone that bar sticks to the bottom of
the window while the results are on screen, so the actions never sit below a long table. The JSON
record is the underlined word beneath it.

**Print summary** opens the browser's print dialog on a print stylesheet that hides the
whole working page and prints a single document: a header carrying the company or file name, the
close period, the memo version, the date, the reviewer name, the run identifier and the source
version, then the rule with both boundary words and the zero prior balance policy spelled out, then
the coverage strip with the line saying what "checked within scope" does and does not mean, then the
full results table, then **every unresolved item carried out of the run**, then the sentences that
were checked within scope with the driver answer and the timing answer under each one, printed if
they were ticked in the queue and left as a blank rule if they were not, then the silent lines with
a blank rule each, then the evidence list from `PROTOCOL.md`, then a
signature block for the second-pass reviewer and for the controller. Print it to PDF and it is the
retained evidence the protocol asks for, in one file.

**Copy table** pastes into a spreadsheet or an email, and confirms with the word *Copied* for two
seconds. **Copy prompt** copies Prompt 2 for the run that is on the page. **Download CSV** writes
one row per finding, in this column order: run id, run timestamp, close period, reviewed memo
version, source version, evidence id, sentence id, sentence text, line, account, check, status,
finding, proposed conclusion, human conclusion, unresolved issue, action owner, review time. The
human conclusion carries whatever was ticked in the queue and is otherwise blank for the person who
signs, the review time is always theirs, and that is what `EVIDENCE-LOG-TEMPLATE.csv` is for; the
columns are wider than that template because a sentence identifier, the exact sentence text and the
source version now ride with every row.

**Any cell that begins with `=`, `+`, `-` or `@` is written with a leading apostrophe**, so a
spreadsheet reads an account named `=1+1` as text rather than evaluating it. **Download JSON
record** writes the same run with every cell exactly as it was typed, plus the roles, the units, the
text spans, the policy in force and the queue, which is the machine-readable record the CSV
neutralisation would otherwise alter. Copy is the reliable path; a download can be blocked inside an
embedded viewer.

**Changing any input clears the statuses.** Edit the ledger, the memo, a ratio, a floor, the rule,
the zero prior balance policy, the period or the memo version and the results table is cleared, a
line says which input changed, and the run that was on the page moves into **Previous runs** with
its own run identifier, its coverage counts and a button to copy its CSV. The next run is stamped
with a new identifier. Confirming a numeric role in a dropdown does the same, so a status always
names the inputs it was computed from.

## The two prompts

The checker sits between them, and both are on the page with a Copy button.

**Prompt 1, draft the memo**, is used before the memo exists. It carries the ledger and the
threshold to whichever AI tool the firm already uses, and fixes the shape of every line:

> `<n>. <account number> <account name>: prior <prior>, current <current>, <rose or fell or flat>
> <change>, <percent> percent, because <one reason> (source: <the document the reason came from>).`

with instructions to write nothing about a line below the threshold except one closing sentence,
to write figures in full dollars rather than k or M, to say in words what each figure is, and to
write "no source on file" rather than invent one. **The shape is not a preference.** An account
number written out is the strongest binding route; full-dollar figures tie to the cent; "prior",
"current", "by" and "percent" are what give each figure its role, without which it comes back with
the role unknown; and a direction word standing immediately beside the change figure is the only
place the direction check reads it. A memo drafted this way runs clean: bound by account number,
every figure checked within scope, direction PASS, and straight into the reviewer's queue.

**Prompt 2, second pass**, is the reviewer prompt, and it needs a run first. It carries the run
identifier and the source version, the rule as set with both boundary words spelled out, the
**coverage counts**, a sentence saying what "checked within scope" does and does not mean, the
**list of sources actually supplied to the run** and nothing else, the ledger and the memo as
pasted, **every unresolved item verbatim**, and then the sentences that were checked within scope
with the two judgment questions. It does not claim every figure was checked and it does not tell
the reviewer to leave the arithmetic alone; it says to recompute anything they doubt and not to
treat a status as evidence.

Four links open the page with a case already run: `checker.html?sample=halyard`,
`?sample=brightwater`, `?sample=kestrel` and `?sample=ridgeline`.

## The four samples

The **Samples** dropdown carries four cases, and each one loads both panes, the ratio pane, the
thresholds and the close period, then runs.

**Halyard and Brightwater are generated from the shared case definitions**, `cases/halyard-v4.json`
and `cases/brightwater-v4.json`, which are the same files the game reads, so the checker and the
game run the same ledger and the same memo version rather than two drifting copies of one case.
The generated block sits in `checker.html` between `BUILD:CHECKER-CASES-START` and
`BUILD:CHECKER-CASES-END`, and it is rewritten by:

```
node build-checker-cases.cjs
```

which refuses to write when a card points at an account the ledger does not carry, when a card's
figures do not tie to its ledger row, or when a case has no version or no date. Never hand-edit the
generated block. The checker holds the generated copy inline rather than fetching the JSON at load,
so the page still makes exactly one network call, for its font. Each sample's **Memo version** field
carries the case version, and it rides into the CSV, the JSON record, the printed summary and
Prompt 2, so a filed log says which version of the case it came from. Kestrel and Ridgeline are the
checker's own cases and are written into the page by hand.

Every expected result below was confirmed row by row against the page on 13 September 2026, with no
console error on any run, and Halyard, Brightwater and Kestrel are asserted end to end by fixtures
T18, T18b and T19 in `tests/checker-fixtures.json`, so a change that moves them fails the suite.

## The Halyard sample, expected against actual

**Halyard Provisioning Group, June 2026** is generated from `cases/halyard-v4.json`, the same case
definition the game runs, so the checker and the game now read the same fourteen accounts and the
same memo version. The Memo version field carries the case version, `halyard-v4 memo, 13 September
2026`, and it rides into the CSV, the JSON record, the printed summary and Prompt 2. Two of the
fourteen cards carry no memo sentence, which is how the case plants its silent lines, so the memo is
twelve sentences numbered by card. The ratio pane is prefilled with
`Product gross margin = (4000 - 5000) / 4000`. Thresholds $25,000 and 10 percent, both legs, zero
prior balances owing commentary.

Coverage strip: **12** sentences read · **4** checked within scope · **5** needs review ·
**0** not checked · **3** failed · **14** ledger rows used · **0** rows skipped · **1** silent line ·
**13** in the reviewer queue.

| Card | Bound | Figures, with the role read from the words | Direction | Threshold claim | Status |
| --- | --- | --- | --- | --- | --- |
| 1, freight | 4200, by account name | $186,000 **prior balance** ✓; $121,000 **current balance** ✓; $6,500 **absolute movement** **FAIL**, the movement is -$65,000; 3.5 percent **relative movement** **FAIL**, it is -34.9 percent | PASS, "fell" agrees | "neither leg is met" **FAIL**: 4200 clears both legs | **failed** |
| 2, depot repairs | 6200, by account name | $118,600 **role unknown**, "of" says nothing; it equals the current balance and the dropdown asks a person to confirm that | not stated | none | **needs review** |
| 3, inbound freight | 5100, by account name | $287,800 **current balance** ✓ | **FAIL**, the memo says "declined" and 5100 rose $73,800 | none | **failed** |
| 4, service revenue | 4100, by account name | $229,000 **absolute movement** ✓ | PASS, "rose" agrees | none | **checked within scope** |
| 5, professional fees | 6500, by account name | $7,500 **absolute movement** ✓; the second $7,500, the outside counsel invoice, **role unknown**, and it happens to equal the change | PASS, "fell" agrees | "fails the dollar leg" **PASS** | **needs review** |
| 7, product revenue | 4000, by account name | $5,612,000 **role unknown**, "revenue of" says nothing | PASS, "grew" agrees | none | **needs review** |
| 8, bad debt | 6400, by account name | $42,000 **absolute movement** **FAIL**, the movement is $47,000 | PASS, "increased" agrees | none | **failed** |
| 9, fleet fuel | 6100, by account name | $5,200 **absolute movement** ✓ | PASS, "fell" agrees | "fails both legs" **PASS** | **checked within scope** |
| 10, software | 6300, by account name | $1,600 **absolute movement** ✓ | PASS, "rose" agrees | "clears neither leg, carries no driver" **PASS** | **checked within scope** |
| 12, distribution revenue | 4000, by an exact figure with "distribution" beside it | 7.1 percent **relative movement** ✓; $5,612,000 **role unknown** | PASS, "grew" agrees | none | **needs review** |
| 13, cost of product sold | 5000 by name, 4000 by an exact figure with "revenue" beside it | $348,000 and $372,000 **absolute movement** ✓ on 5000 and 4000; $1,310,000 and $1,334,000 **computed across two lines**, the current and prior balance on 4000 less the same on 5000, reported and left open; 25.0 percent **ratio, prior** ✓ and 23.8 percent **ratio, current** ✓ | PASS, "rose", "rise" and "fell" agree | none | **needs review** |
| 14, interest | 7100, by account name | $31,200 **absolute movement** ✓ | PASS, "rose" agrees | none | **checked within scope** |
| 6000 Warehouse wages | no sentence | | | $72,500 and 11.5 percent | **SILENT** |
| 7400 Inventory shrink | no sentence | | | $2,500 and 39.1 percent, below the dollar leg | nothing owed |

Four results are worth naming because they are wider than the case that prompted them:

- **Card 1's threshold claim is false, and the checker says so.** The sentence asserts that neither
  leg is met on 4200. The movement is $65,000 and 34.9 percent, so both legs are met. A sentence
  that asserts something about the rule is checked against the rule as set, and this one fails on
  three counts: the movement figure, the percent, and the claim about the threshold.
- **Card 13's gross profit figures are right and the checker still will not pass them.** $1,310,000
  and $1,334,000 are correct, and they are a subtraction across two ledger lines, not a balance on
  either. The page reports exactly that, "it is the prior balance on 4000 less the prior balance on
  5000", and leaves it open. Reporting a true figure as unverified is honest; passing it on a
  coincidence would not be.
- **"Of" is not a role.** Cards 2, 7 and 12 each write "of $118,600" or "revenue of $5,612,000",
  which says nothing about whether the figure is a balance, a movement or a target. Each one equals
  a ledger value, and an equality is not a check. The dropdown beside the row lists the five roles;
  confirming one restamps the run and keeps the earlier one under Previous runs.
- **Read together fires on 4000**, which carries cards 7, 12 and 13. The checker does not test them
  against each other and says so rather than guessing.

The checker supplies none of the case's **On file** facts. A clean verdict in the game does not
transfer to the checker, and a status here is never evidence that a driver is supported.

## Brightwater Dental Partners, June 2026, the round two case

**Brightwater Dental Partners** is generated from `cases/brightwater-v4.json`, the five-account,
five-sentence dental group the game scores a player on cold. The Memo version field carries
`brightwater-v4 memo, 13 September 2026`. A plain tab separated ledger with a two column header,
`Account / May 2026 / June 2026`, read chronologically. Thresholds $25,000 and 10 percent, both
legs, no ratios.

Coverage strip: **5** sentences read, **5** checked within scope, **0** needs review,
**0** not checked, **0** failed, **5** ledger rows used, **0** rows skipped, **0** silent lines,
**0** in the reviewer queue.

This is the sample where the checker clears everything and settles nothing, and that is the point
of it. Every figure in the v4 memo is right and every direction word agrees with the sign, so the
mechanical pass has no finding to make. What each sentence then asserts is a cause, and a cause is
not a figure. Four of the five name a driver the ledger cannot confirm or deny, which is why the
game keys three of them `flag` and one `stand` on evidence a person has to weigh. A checker that
reported a failure on this sample would be wrong, and a reader who took an empty queue as a clean
memo would be making the mistake the whole project is about.

| Line | Result |
| --- | --- |
| 4010 Patient service revenue, net | $61,500 and 8.3 percent, **below the rule**: the largest dollar movement on the statement owes nothing, because the percent leg is not met |
| 4220 Orthodontic plan revenue | $42,400 and 44.2 percent, clears |
| 5210 Dental supplies and lab fees | $52,700 and 38.1 percent, clears |
| 6110 Hygienist wages | $54,900 and 25.7 percent, clears |
| 6610 Marketing and patient outreach | $5,700 and 31.0 percent, **below the rule**: a large percentage of a small balance is still a small number |

| Sentence | What the checker did with it |
| --- | --- |
| 1, supplies rose $52,700, or 38.1 percent, on the implant cases the new surgical suite took on | bound 5210 by name; $52,700 **absolute movement**, the role read from the direction word "rose", ties; 38.1 percent **relative movement**, the role read from "or" restating the figure before it, ties. **Checked within scope** |
| 2, hygienist wages rose $54,900, or 25.7 percent, on a second hygiene chair | bound 6110 by name; both figures tie, both roles read the same way. **Checked within scope** |
| 3, orthodontic plan revenue rose $42,400, or 44.2 percent, as thirty-one new plans began billing | bound 4220 by name; both figures tie. **Checked within scope** |
| 4, patient revenue rose $61,500, or 8.3 percent, as two associates reached a full schedule | bound 4010 by name; both figures tie, and the claim "fails the percentage leg" **PASS**. **Checked within scope** |
| 5, marketing rose $5,700, or 31.0 percent, on a mailer delivered in the first week of June | bound 6610 by name; both figures tie, and the claim "fails the dollar leg" **PASS**. **Checked within scope** |

**Nothing here reaches the reviewer queue, and four of the five sentences still need a reviewer.**
The queue holds what the mechanical pass could not resolve, and on this memo it resolved everything
it is able to resolve. The surgical suite, the thirty-one plans, the two associates and the second
hygiene chair are each a cause the ledger has no opinion about. Read the coverage strip as what was
checked, never as what was established: the scope is set out at the top of this file, and a status
here is never evidence that a driver is supported.

## Kestrel IT Services, July 2026, a QuickBooks export

**Kestrel IT Services** is the checker's own case, not the game's, and a six-account managed
services firm pasted in the shape QuickBooks Online's Profit and Loss Comparison exports: a three
line title block, the account number and name in one first column cell, **the current period column
before the comparison period**, and the `$ Change` and `% Change` columns the Calculations dropdown
adds. Sections `Income`, `Cost of Goods Sold` and `Expenses`, with `Total ...` rows, `Gross Profit`,
`Net Operating Income` and `Net Income`. Thresholds $25,000 and 10 percent, both legs, no ratios.

The reader takes four numeric columns, marks `$ Change` and `% Change` as computed, reads
`Jul 2026` and `Jun 2026` off the calendar and puts them the right way round, so the prior is the
second column and the current is the first. Six lines found, six total rows held back, three
sections, four rows ignored as title and header, **and the two computed columns reported as
discarded** in the queue, because a column that is read and dropped is a decision a reviewer is
entitled to see. The header names every column, so the mapping counts as confirmed and the statuses
stand on their own.

Coverage strip: **6** sentences read · **3** checked within scope · **0** needs review ·
**1** not checked · **2** failed · **6** ledger rows used · **0** rows skipped · **1** silent line ·
**6** in the reviewer queue.

| Line | Result |
| --- | --- |
| 4000 Recurring managed services | $36,900 and 22.8 percent, clears, and **SILENT**: no sentence in the memo touches it |
| 4100 Project and implementation revenue | $57,500 and 147.8 percent, clears |
| 5000 Subcontracted engineering | $46,500 and 111.2 percent, clears |
| 6000 Salaries and wages | $0 and 0.0 percent, below the rule |
| 6200 Software licenses and hosting | $35,300 and 156.2 percent, clears |
| 6400 Client acquisition costs | $9,300 and 189.8 percent, below the rule |
| Total Income, Total Cost of Goods Sold, Total Expenses | all three **TIE** to the lines under them |
| Gross Profit, Net Operating Income, Net Income | **KEPT OUT**, computed across sections |
| 1, project revenue rose **$57.5k** to $96,400, up 147.8 percent | bound 4100 by account number; $57.5k **absolute movement** ✓, $96,400 **current balance** ✓, 147.8 percent **relative movement** ✓. **Checked within scope** |
| 2, project revenue carries the final Riverbend milestone | bound 4100 by account name, no figures and no threshold claim. **Not checked**, and **read together** with line 1 |
| 3, subcontracted engineering "fell $46,500" | bound 5000 by number; $46,500 **absolute movement** ✓ and $88,300 **current balance** ✓; direction **FAIL**, the account rose. **Failed** |
| 4, salaries "held flat at $88,500" | bound 6000 by number; $88,500 **current balance** ✓, the role read from "at"; direction PASS on the flat test. **Checked within scope** |
| 5, software licenses rose **$25,300** to $57,900 | bound 6200 by number; $57,900 **current balance** ✓; $25,300 **absolute movement** **FAIL**, the movement is $35,300. **Failed** |
| 6, client acquisition rose $9,300, or 189.8 percent | bound 6400 by number; both ✓; claim "fails the dollar leg" **PASS**. **Checked within scope** |

Two problems are planted, one of each kind the mechanical checks can settle: **line 3 has the
movement backwards** and **line 5 is $10,000 short of the change it claims**. The third finding is
the one nobody wrote: **4000 clears the rule and the memo never mentions it**. The sample exists to
show a QuickBooks paste going in whole, so it also carries the `$57.5k` figure, the `held flat`
direction, the totals tie and the discarded-column report in the same run. The account numbers
written into the memo, `4100`, `5000`, `6000`, `6200`, `6400`, are read as references and never as
dollar figures.

## A second ledger, to show it is not tuned to Halyard

**Ridgeline Partners, July 2026** is the checker's own case too: five made-up accounts and three
sentences against June, in a plain comma separated ledger with no header row at all.

Coverage strip: **3** sentences read · **1** checked within scope · **0** needs review ·
**0** not checked · **2** failed · **5** ledger rows used · **0** rows skipped · **1** silent line ·
**3** in the reviewer queue.

| Line | Result |
| --- | --- |
| T1, consulting revenue rose $61,000 | bound 4300 by name, **absolute movement** ✓, direction PASS. **Checked within scope** |
| T2, subcontractor costs "increased" $32,000 | bound 5200 by name, the figure ✓ as a magnitude, direction **FAIL**: the account fell $32,000. **Failed** |
| T3, travel and entertainment rose $9,400 | bound 6600 by name, **absolute movement** **FAIL**: the movement is $7,400. **Failed** |
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
| Duplicate account numbers | A note naming them, a queue item saying no consolidation decision has been made, and every sentence naming that number held at **needs review**, because it cannot be tied to one line |
| Negative balances | Read from a minus sign or from (parentheses). A move from -$120,000 to -$180,000 is a change of -$60,000 and -50.0 percent, and a memo that calls it a rise **FAILS** |
| Zero prior balance | No percent is computed and none is claimed. The selected policy settles the rule: **owes commentary on any movement** (the default) or **excluded from the rule**, and whichever is in force is printed on the line and carried into Prompt 2 |
| A comma separated ledger with unquoted thousands, `6100,Rent,100,000,130,000` | Refused, not guessed at. The page says a three digit field stands after a numeric field, which is what an unquoted thousands separator looks like, and asks for tabs or quoted fields |
| More numeric columns than the two periods, with no header row | Every column not read as a period is named as **discarded**, the mapping is marked unconfirmed, and no sentence on that ledger reads better than needs review until the two period columns are confirmed in the parse preview |
| A formula-like account name, `=1+1` | Written to the CSV as `'=1+1` so a spreadsheet reads it as text, and kept exactly as typed in the JSON record |
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
