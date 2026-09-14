# Second Pass Checker

`checker.html`, live at https://fiscalpatriots.github.io/beat-the-machine/checker.html

The game at [index.html](index.html) trains a reviewer on fourteen lines of one case. This page is
the tool that came out of it. Paste a ledger in one of the layouts below and the commentary drafted
about it, press **Run Second Pass**, and the checks it can make are made before a person reads a
word. What comes back is a coverage strip, a table of findings and a queue of questions that a
person still has to answer. **Read the coverage before the findings.** A run says what it checked
and what it could not read; a sentence it could not read is never reported as a sentence that was
checked.

One HTML file and no libraries. **Where your data goes**, printed on the page itself because a
controller is entitled to know it before pasting a trial balance into a web page: this page is
served from GitHub Pages and loads one Google font from fonts.googleapis.com; everything you paste
is processed by the script in your own browser, this page stores nothing on a server, and anything
you copy from here into another AI service goes to that service under its terms. The font request is
the one network call the page makes, and it carries no ledger data.

## What goes in

| Pane | What it takes |
| --- | --- |
| Ledger | Three accepted layouts, told apart by the reader itself. **Plain:** one account per line, account number (optional), account name, prior balance, current balance, tab separated, comma separated with quoted fields, or column aligned with two or more spaces. **QuickBooks Online Profit and Loss Comparison:** the title block, an account label of the form `4000 Recurring managed services` in the first column, the two period columns and the `$ change` and `% change` columns that the report's Calculations dropdown adds, with `Income`, `Cost of Goods Sold` and `Expenses` as section headers and `Total ...`, `Gross Profit`, `Net Operating Income` and `Net Income` as totals. **Xero Income Statement with a comparison period:** `Income`, `Less Cost of Sales`, `Gross Profit`, `Less Operating Expenses`, `Net Profit`, each section closed by its own `Total` row. Numbers are read in whole dollars with the digits 0 to 9: dollar signs, thousands commas, decimals and (parentheses) or a minus sign for negatives. A layout outside these three is read only as far as its rows look like account lines, and every row it cannot use is listed. |
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

## Inputs it refuses or reads only in part

These are refused or held rather than guessed at, and each one is listed on the page:

| Input | What happens |
| --- | --- |
| A comma separated line with unquoted thousands, `6100,Rent,100,000,130,000` | The ledger is refused, with a request for tabs or quoted fields |
| A row with fewer than two numbers, or with digits outside 0 to 9 | The row is skipped and listed by line number with the reason, and the coverage line says the ledger was not covered in full |
| A duplicated account number | Every sentence naming it is held at **needs review** until a consolidation decision is made |
| More numeric columns than two, with no header row | The columns not read are named as discarded and no sentence reads better than **needs review** until the two period columns are confirmed |
| A total the reader cannot rebuild, such as Gross Profit or Net Income | Printed and left alone |
| A spreadsheet file | Not opened. Copy the cells from Excel and paste them |

## Choosing the two periods

Only two columns are ever compared, the prior and the current. The reader picks them in this order,
and the parse preview shows the pick with a dropdown for each so a person can change it:

1. A header word: `prior`, `previous`, `last month`, `PY`, `PP` or `budget` for the prior column,
   and `current`, `this month`, `actual` or `YTD` for the current one.
2. The calendar: two month headings such as `Jul 2026` and `Jun 2026` are put in date order, so a
   QuickBooks export that prints the current month first is still read the right way round.
3. Left to right, with the mapping marked **unconfirmed** when no header named it.

A column headed `change`, `variance`, `%` or `pct` is never picked as a period.

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
   **separate unit**, read from `pp` and `percentage point`. A figure carries **its own sign** when
   the words write one: a minus or a plus in front of it (`-$30,000`, `+$60,000`, `-30,000`,
   `+25 percent`, and a minus in front of a bare number), a minus or a plus just after the dollar
   sign (`$-30,000`, `$+60,000`), a minus written straight after it (`30,000-`), or a closed pair of
   parentheses. A dash or a Unicode minus in front of a figure reads as a minus. A plus or a minus
   glued to a digit or a letter in front of it, as in `25,000-35,000`, is a range or a hyphen, not a
   sign. A lone opening bracket, as in `rose $30,000 (30%)`, is punctuation and the percent inside it
   is read normally.
1b. **What the grammar reads, and what it does not.** The figure reader reads the dollar and
   percent forms in step 1 and the quantities in words in 1c, and nothing else. Every other piece of
   quantitative language in a sentence is an **unparsed span**: it is recorded with its reason, it
   goes to the reviewer's queue, and it marks the sentence **not checked** whatever else in the
   sentence agreed. A sentence is checked within scope only when every quantitative expression in
   it is accounted for. The unparsed kinds are:
   - a **currency that is not the dollar**: `€30,000`, `£30,000`, `USD 90000`, `US$30,000`, and a
     currency named in words or a dollar that is someone else's standing beside the figure:
     `30,000 euros`, `30,000 pesos`, `30,000 Canadian dollars`, `$30,000 in Canadian currency`;
   - a **debit or credit marker** beside a figure: `30,000 CR`, `30,000 Cr.`, `$30,000 DR`,
     `$30,000 credit`, because which way it points depends on the account's normal balance, which a
     two column ledger does not say;
   - a **scale or unit word the grammar does not carry**: `$30.0 thousand`, `30 thousand`, `0.30
     times`, `30 basis points`, `90.0 per mille`, `3 points`;
   - a **multiplier**: `doubled`, `tripled`, `halved`, `twice`, `twofold`, `two-fold`, `three
     times`, `3x`;
   - a **fraction**: `one and a half`, `a quarter of`, `half a percent`, `half the prior balance`,
     `two thirds`, `cut in half`, `1/2`, `½`;
   - a **decimal written in words**: `thirty point five percent`, `point five percent`;
   - a **digit outside 0 to 9** or a numeral from another writing system: Arabic-Indic `٣٠٠٠٠`,
     fullwidth `３０`, superscript `²`, `‰`, `三十`;
   - a **unit word with no figure the reader took in front of it**: `trente pour cent`, `XXX
     percent`, `thousands of dollars`;
   - a **number glued to letters, underscores, dots or slashes** that the reader does not take:
     `9e1 percent`, `30_000`, `.5 percent`;
   - a **quantity in words the parser cannot resolve**, or one with no unit where the words put a
     claim: `a rise of thirty thousand`, `two billion dollars`;
   - **any other run of digits** the figure reader did not take, unless it is one of the forms in
     the next paragraph: `increased by 800`, `increased by 1999`, `or 30.`

   A number is accounted for without being a figure only as one of these, and the sentence's own
   explanation names each one as **read and left outside the check**: a **year** (`in 2026`,
   `June 2025`), a **date** (`June 30`, `31 July`, `on 6/1`), a **label or reference** (`invoice
   4471`, `Suite 200`, `line 5`), an **ordinal** (`3rd`), a **time of day**, an **account number**
   standing as a reference, and a **count** written in front of the thing it counts (`12 new
   leases`, `the thirty-one new plans`). A count is not verified against the ledger. Being
   accounted for is not the same as clearing: a label that names a period, `Q2`, `H1`, `FY26`, and a
   year or a month the ledger's column labels contradict, are then held by the clearance grammar
   below. A year or
   an account number spent as an amount, `increased by 1999`, `increased by 6200`, is not a
   reference and is unparsed. The external review of 13 September 2026 asked for *needs review* on
   unparsed spans; the page says **not checked**, which says that nothing in the sentence was
   settled.
1c. **Quantities written in words.** Whole numbers through millions are read: `thirty`,
   `thirty-one`, `ninety`, `one hundred twenty-five thousand`, `two million`. A run is parsed to a
   figure and compared like any other **only where both hold**: the parser resolves the run, and
   the words beside it give it a unit (`dollars`, `percent`, `per cent`, `pct`, `%`, `percentage
   points`, `pp`). So `rose thirty thousand dollars` is compared as $30,000 and `a change of ninety
   percent` is compared as 90 percent and fails a ledger that moved 30 percent. Fractions, decimals
   in words, multipliers and anything above a million are unparsed wherever they stand (1b). A
   resolved run with **no unit word** is accounted for only as a count in front of a noun (`the
   thirty-one new orthodontic plans`, `across three sites`), a label (`phase two`), or `one` as a
   pronoun or idiom (`one of the larger moves`, `one-time`). Anywhere else, `or thirty`, `a rise of
   thirty thousand`, it is unparsed.
1d. **Roles Prompt 1 writes.** `prior` and `previous` standing in front of a figure give it the
   prior balance role, and `current` gives it the current balance role, so a line drafted in the
   Prompt 1 shape, `prior $96,000, current $138,400`, is checked on both balances. `prior year
   $96,000` is not a prior balance: the word between them breaks the role, and the figure is held.
   A figure followed by `or more`, `or less`, `at most`, `at least` and the like is a bound, not a
   figure, and its role is unknown.
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
   exempt, because no account binding settled it. `respectively` pairs figures with accounts by
   position, which no clause shows, so in a sentence carrying it no figure is bound by its clause:
   `Rent expense and Insurance expense rose $30,000 and $45,000 respectively` is held at needs review,
   never failed on a pairing that is true, and a figure that ties to neither line still fails. An
   account number the memo **spends as an amount**, `increased by 6200`, is a claim and not a
   reference: it binds nothing, and it does not take that line off the silent list.
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

**No-change claims.** `unchanged`, `remained at`, `remains at`, `stayed at`, `held at`, `kept at`,
`continued at`, `maintained at`, `remained unchanged`, `stayed the same`, `remained constant`, `no
change`, `no movement`, `level with`, and `remained` or `stayed` written straight in front of a
figure, assert that the account did not move. They are tested against a movement of zero to the half
cent: on a line that moved, the sentence **fails**; on a line that did not, the claim passes. A flat
claim, `flat`, `held flat`, `steady`, `remained flat`, is looser and is tested against a
movement inside half a percent of zero. Those are the only no-change words the direction check
tests. Any other, `stable`, `level`, `static`, `consistent`, `in line with May`, `the same as May`,
`on par with`, `matched`, `little changed`, is not read as a claim at all: the clearance grammar
below holds the sentence at needs review and names the word.

**Negation.** `not`, `no`, `never`, `neither`, `nor`, `without`, `rather than`, `instead of`,
`failed to` and the contracted forms **void** the direction claim and the figure claims in the
clause they attach to, and force **needs review**. A negation is not read as the claim it would be
without it and not as its opposite: the checker says it cannot settle the clause and a person does.
The threshold idioms a memo uses to say a line owes nothing, "no commentary is owed", "clears
neither leg", "carries no driver", "no change", are taken out before the test, and a clause with no
figure and no direction word is inert.

Two checks sit outside the six and are reported the same way. **Direction** tests rose, fell, flat
and the no-change words against the sign of the movement, inside a clause that carries a figure
tying to a bound account. A direction word in a clause of its own is tested against the line that
clause names; where it names none, stands beside a clause the figures did tie, and disagrees with
every bound line, the sentence is held at **needs review** as **not tied to a line**. A clause
opened by `as`, `because`, `while`, `but`, `after`, `before`, `so` or `though` describes a cause or
a contrast, so its direction word is left alone unless it points back with `it` or names the line. **Threshold claims** test a sentence that asserts something about the rule itself, "fails
the dollar leg", "clears neither leg", "carries no driver", against the rule as set; it is the one
case where a sentence can be checked on its words rather than on a figure.

The ledger is checked first and separately: every line recomputed from its two balances, every
`Total ...` row rebuilt from the lines standing under its section, and every row the reader could
not use listed by line number with the reason.

## The clearance grammar

The six steps say what the checker reads. The clearance grammar says when a sentence may be called
**checked within scope**, and it works the other way round from a list of bad words: a sentence
clears only when **nothing risky is left once every claim in it is read**. The independent audit of
13 September 2026 found 48 of 175 new probes clearing one step to the side of classes the previous
repair had closed by listing words, and the third review asked for exactly this rule: accounted-for
financial assertions under a defined grammar, and ambiguous quantitative language left unresolved.

**What is read and taken out first.** The account names and numbers the sentence is bound by; every
figure the reader took; every unparsed span and every number left outside the check; the direction
words and the no-change and flat words the direction check tests; the movement nouns (`increase`,
`change`, `movement`, `variance`); `changed by` and `moved by` standing in front of a figure; and the
period frame of the ledger's own two columns, `month over month`, `from the prior month`, or a month
the column labels name (`over May` on a ledger headed `May 2026 / June 2026`).

**What is left is read against the risk lexicon.** Twenty-two entries, about 930 alternatives when
every spelling and ending a pattern allows is counted, in the classes below. A **strong** entry holds the sentence wherever it stands. A
**weak** entry holds it only inside the claim, which runs from the start of the sentence to the first
word that opens a reason after its last figure (`because`, `as`, `since`, `on`, `due to`, `driven
by`, `after`, `with`, `while` and kin, or an opening bracket), unless the reason points straight back
at the line (`because it`, `as the balance`). A reason is already a question for a person, so a word
that only describes the cause stays with that question: `rose $30,000 on sharply higher rates`
clears, `rose sharply, by $30,000` does not.

| Class | Strength | What it catches, with examples |
| --- | --- | --- |
| Currency | strong | 40 currency names (`euros`, `pounds sterling`, `yen`, `rupees`, `pesos`, `francs`, `quid`, `cents`), a dollar someone else issues (`Canadian dollars`, `US dollars`, `in Australian dollar terms`, 62 qualifiers), `currency`, `exchange rate`, `foreign exchange`, `FX`, 64 ISO codes written in capitals, and every currency symbol but `$` |
| Sign | strong | `CR`, `DR`, `Cr.`, `Dr.` (not a title before a name), `credit balance`, `in credit`, `net debit`, `credited`, `favourable`, `unfavorable`, `adverse`, `(F)`, `(U)`, a sign standing apart from its figure (`- $30,000`, `(-)`, `+/-`, `±`) |
| Sign | weak | `plus`, `minus`, `negative`, `positive` |
| Another account | strong | `so did`, `as did`, `as was`, `neither did`, `likewise`, `similarly`, `the same was true of`, `respectively`, `followed suit`, `in tandem`, `in step`, `the rest`, `the other lines`, `every other account` |
| Another account | weak | `also`, `too`, `as well`, `together`, `alongside`, `equally` |
| Sameness | strong | `same`, `identical`, `equal`, `equivalent`, `matched`, `comparable`, `similar`, `consistent`, `in line with`, `on par with`, `no different`, `even with`, `in keeping with`, `ditto`, `stable`, `stabilized`, `steady`, `static`, `constant`, `flattish`, `flatlined`, `stagnant`, `stalled`, `plateaued`, `sideways`, `little changed`, `level`, `barely`, `hardly`, `scarcely` (a tested no-change phrase such as `held steady` or `remained constant` is read first and never reaches this list) |
| Sameness | weak | `virtually`, `essentially`, `broadly`, `largely`, `maintained`, `sustained`, `remained`, `stayed`, `held`, `kept`, `continued`, `still`, `mirrored`, `tracked` |
| Comparison | strong | `compared with`, `versus`, `vs`, `against`, `relative to`, `than`, `outpaced`, `outperformed`, `exceeded`, `ahead of`, `behind`, `short of`, `lagged`, except where they introduce the ledger's own prior column |
| Ranking | weak | `largest`, `biggest`, `smallest`, `highest`, `lowest`, `greatest`, `most`, `least`, `record`, `top`, `ranked`, `leading`, `all-time` |
| Basis | strong | `budget`, `forecast`, `reforecast`, `outlook`, `guidance`, `projection`, `pro forma`, `run rate`, `annualized`, `like-for-like`, `constant currency`, `normalized`, `seasonally adjusted`, `basis`, `cumulative`, `to date`, `so far`, `as expected`, `as planned`, and `plan`, `target`, `estimate`, `expectations`, `consensus` or `goal` after `versus`, `against`, `over`, `under`, `above`, `below`, `ahead of`, `behind`, `missed` or `beat` |
| Period | strong | `year`, `years`, `yr`, `year over year`, `year to date`, `YoY`, `YTD`, `QTD`, `MTD`, `PY`, `LY`, `annual`, `fiscal`, `FY26`, `quarter`, `quarterly`, `quarter-end`, `Q2`, `H1`, `half-year`, `semiannual`, `trailing`, `TTM`, `LTM`, `rolling`, `twelve months`, `months`, `weeks`, `three months`, `30 days`, `consecutive months`, `in a row`, `week over week`, `sequentially`, `prior period`, `same period`, `since December`, `since the start`, `last June`, `over the summer`, `first half` (not `first half of June`), `ago`, `per month`, a year the column labels do not carry. A period word that only gives the length of a lease, a contract, a fee or a renewal (`a one-year lease`, `a half-year term`) is left alone |
| Period | weak | `week`, `day`, `spring`, `summer`, `seasonal`, `holiday`, `through`, `until`, `during`, `first half of June`, `third month`, `mid-month`, `early`, `late`, `recently`, `previously`, `typically`, `usually`, `again`, `yet`, a month the column labels do not carry |
| Change | weak | a change verb the direction check does not test: `soared`, `spiked`, `leapt`, `plunged`, `tumbled`, `slumped`, `dipped`, `contracted`, `rebounded`, `recovered`, `reversed`, `swung`, `moved`, `shifted`, `fluctuated`, `varied`, `widened`, `narrowed`, `improved`, `worsened`, `peaked`, `ramped`, `slowed`, `ticked up`, `edged down`, `trended`, `changed`, `followed` |
| Size | weak | `sharply`, `significantly`, `substantially`, `materially`, `markedly`, `dramatically`, `modestly`, `slightly`, `marginally`, `steeply`, `strongly`, `huge`, `large`, `small`, `major`, `minor`, `massive`, `negligible`, `heavy`, `unusual`, `robust` and kin |
| Share and quantity | weak | `mostly`, `mainly`, `primarily`, `partly`, `entirely`, `wholly`, `fully`, `solely`, `in part`, `bulk`, `majority`, `portion`, `share`, `offset`, `net of`, `several`, `many`, `much`, `numerous`, `multiple`, `few`, `more`, `less`, `dozens`, `hundreds`, `thousands`, `various`, `additional`, `incremental`, `excess`, `shortfall`, `gap`, `difference`, `delta`, `spread`, `margin`, `ratio`, `rate`, `proportion` |

**Two rules that are structural rather than lexical.** Where a sentence binds more than one
account, every account it names needs a figure or a tested direction word in its own clause, so
`Rent expense rose $30,000, and Insurance expense followed` is held even though no listed word
carries the second account. And where the ledger's column labels name no month, two months in the
claim that are not neighbours are held: `from May to June` clears, `from May to August` does not.

**What holding means.** A word left from the lexicon holds a sentence that would otherwise clear at
**needs review**. The row reads `Wording <the word>`, **OUTSIDE THE GRAMMAR**, with a plain
sentence naming the word and why it is held, and the reviewer's queue carries an **Unread wording**
item asking what the word claims and whether the ledger supports it. A sentence that a figure, a
binding, a negation or an unparsed span has already failed, held or left unchecked keeps that status
and gets no wording row, because the word is not what stops it clearing; a person reads it anyway,
and the word is named once the other problem is fixed. A sentence whose figures tie gets its wording
rows even when its direction word then fails. The
author page reads the same grammar through `assets/second-pass-core.js` and puts the same sentence
under **What the checks found**.

**Refused and still clearing, on a ledger where Rent expense rose from $100,000 to $130,000.**

| Sentence | Status |
| --- | --- |
| `Rent expense rose 30,000 euros.` | not checked, a currency beside the figure |
| `Rent expense rose $30,000 at the current exchange rate.` | needs review, `exchange rate` |
| `Rent expense changed by $-30,000.` | failed, the sign is read and clashes |
| `Rent expense changed by 30,000 CR.` | not checked, a credit marker beside the figure |
| `Rent expense was stable at $130,000.` | needs review, `stable` |
| `Rent expense was in line with May at $130,000.` | needs review, `in line with` |
| `Rent expense rose $30,000, or 30 percent, year over year.` | needs review, `year over year` |
| `Rent expense rose $30,000 against budget.` | needs review, `against` and `budget` |
| `Quarter to date, rent expense rose $30,000.` | needs review, `Quarter to date` |
| `Rent expense rose $30,000; so did Insurance expense.` | needs review, `so did` |
| `Rent expense and Insurance expense rose $30,000 and $45,000 respectively.` | needs review, a binding conflict on each figure, never failed |
| `Rent expense rose $30,000, the largest movement on the statement.` | needs review, `largest` |
| `Rent expense rose $30,000, or 30 percent, on the Suite 200 lease.` | checked within scope |
| `Rent expense changed by +$30,000.` | checked within scope, the sign agrees |
| `Rent expense rose $30,000 month over month.` | checked within scope |
| `Rent expense rose $30,000 as the one-year lease began.` | checked within scope |

The lexicon is a fence, not a proof. A sentence that clears under it has had every word the grammar
knows to be risky taken out or read; it has not been understood. The regression suite holds 159
mutations of these classes, each refusing and accepting, and a new way of writing a quantity is
compared only once it is added there.

## The four statuses

Every sentence gets exactly one, and **no later step may promote one upward**. The run keeps the
worst status any step assigned and the summary, the exports and the prompt all carry that one.

| Status | What it means |
| --- | --- |
| **Checked within scope** | Every quantitative expression in the sentence was accounted for: each figure carried a role the words gave it and agreed with the pasted ledger unrounded, every other number was a year, a date, a label, an ordinal, a reference or a count, named in the sentence's explanation as left outside the check, and once those claims were read nothing from the clearance grammar's risk lexicon was left. The explanation lists the figures that were checked, says whether a direction word was tested, and names what was left outside. It does not mean the sentence is true. |
| **Needs review** | Something is unresolved: a role the words do not give, a binding the checker will not settle by coincidence or by a clause naming two accounts, a duplicate account number, a percent it cannot compute, a clause the words negate, a column mapping nobody confirmed, or a word the clearance grammar leaves: a currency, a sign or debit or credit marker, a sameness, comparison, period or basis word, or a claim carried to another account. A person has to answer it. |
| **Not checked** | The sentence could not be tied to the ledger and tested in full. An unmatched sentence, a sentence with no figures, and a sentence carrying an unparsed span all land here, even when every figure the reader did take agreed. This is **not** the same as a sentence that was checked and found true, and the page never prints it as one. |
| **Failed** | At least one check on the sentence failed. |

A sentence carrying no figures is **not checked** unless it makes a threshold claim, in which case
the claim itself is checked.

## Coverage, not a failure count

The results open with a **stacked bar** of the four sentence statuses in proportion, drawn in the
page's own tokens, which fills once when a run lands. Under it sit **four tiles** carrying the four
marks and their counts: a green check for checked within scope, an ink square for needs review, a
soft ring for not checked, a red cross for failed. Each count runs up to its number over a fifth of
a second, and a reader whose system asks for less motion gets the number with no run-up. The same
four marks lead every sentence and every check, so a sentence, a tile and the bar say the same thing.
A line under the tiles carries the counts the bar does not: sentences read, ledger rows used, rows
skipped, silent lines, and the size of the reviewer queue. Under it the run identifier and the
source version, and, when a row was skipped, the statement that the ledger was not covered in full.

Then four links, each with its count, to the four parts below, and the parts in the order a reviewer
works them. **Every sentence, worst first**: failed, then needs review, then not checked, then checked
within scope, each group headed with its count and each sentence in memo order inside it. Every
sentence is one line that opens: its mark, its label, its status, the sentence once, and what its
checks found, as in `7 checks · 3 failed (Figure $6,500, Figure 3.5 percent, Threshold claim) · 4
passed`. Opened, it shows the sentence's status explanation and a table of its checks, each with its
result, its finding and what to ask, and the role dropdown where a role needs confirming. **Open
every sentence** opens them all. **Silent lines** are never folded. **Every ledger line, recomputed**
folds under its counts (lines, how many clear the rule, the section totals that tie and those kept
out) and opens by itself when a section total does not tie. **The reviewer's queue** is never folded,
and it says how many of its entries are items the run left open, how many are sentences checked
within scope carrying the two judgment questions, and how many are lines to read together. A **Back
to the top of the results** link closes the sentences and the queue. On the Halyard sample this
took the results from 44,311 pixels tall to 12,962 at 320 and from 19,636 to 7,163 at 1,280, with
every check still one tap away.

A row the ledger reader could not use is printed under the strip in a red box, by line number, with
the reason, on every run. Rows the reader drops on purpose, the header row and the title block above
a report, are not counted as skipped; a row that looks like an account line and could not be read is.

The **reviewer queue** carries every failure, every binding conflict, every unmatched sentence,
every skipped source row, every refused row, every malformed ratio, every unsupported numeric form,
every discarded numeric column, every silent line and every account carrying two or more sentences.
It is printed **after the sentences, the silent lines and the ledger as a plain numbered list**, each item carrying the sentence, the
finding and the questions beneath it. Every question carries **Yes, No and Not on file** beside it,
and what a reviewer ticks rides out with the run: into the human conclusion column of the CSV, into
the JSON record as `reviewerAnswer`, and onto the line in the printed summary where an untouched
question prints a blank rule for a pen. The queue is also repeated verbatim in Prompt 2. Each
check's **Ask the controller** column carries the instruction in one imperative, and the
question itself is asked in full in the queue, which is where it gets answered. The reviewer queue also carries **unparsed
figures**, **negated claims**, **binding conflicts**, **unresolved directions**, **unread wording** the clearance grammar held, and a **no source on file** item for
every bound sentence that says no source is on file, owned by the controller, so a missing source stays a question
for a person however well the figures tie.

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

`tests/checker-fixtures.json` holds **546** fixtures and **all 546 pass**, and the suite adds two
more checks: every reader function `assets/second-pass-core.js` shares with `checker.html` must be the
same function, and every one-line constant they share and the clearance grammar's block must be the
same text, so the author page and the checker cannot read one memo two ways. The same file sits in
the second-pass repository, where `tests/test_parity_shared_inputs.py` runs all 546 inputs through
this page under Node and through the Python checker and compares the outputs, and a further test
holds the risk lexicon identical in both, entry for entry.

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
- **T32 and T43** were written as controls for `remained at`. The third review of 13 September 2026
  showed that label was wrong: `remained at` asserts no movement, and the line moved, so both now
  assert **failed**.
- **P01 to P40**, the forty probes from the third review of 13 September 2026, entered exactly as
  that bundle supplied them, each asserting the status the repaired contract requires.
- **Six mutation classes, 113 fixtures**, written so each repaired class is proven closed from both
  sides, with synonyms, word order, hyphenation, currency and percent placement and negation:
  **MUL01 to MUL22** multipliers (18 refused, 4 accepted), **STILL01 to STILL28** no-change and flat
  claims (21 refused, 7 accepted), **FRAC01 to FRAC26** fractions and
  number words in percents (22 refused, 4 accepted), **DIGIT01 to DIGIT16** digits outside 0 to 9 and
  numbers glued to letters (14 refused, 2 accepted), **COUNT01 to COUNT15** numbers that are not
  figures (8 refused, 7 accepted), and **ROLE01 to ROLE06** the Prompt 1 line shape (3 refused, 3
  accepted). Four of them moved from checked within scope to **needs review** when the clearance
  grammar arrived, each with a note in the fixture: FRAC21 `in the first half of June` and FRAC23 `at
  quarter-end` put the movement inside or across a period the two month-end columns do not show,
  COUNT10 `in Q2` frames it on a quarter, and COUNT13 `one of the larger moves` ranks the line
  against the others. Each still carries no fraction and no unparsed number, which is what it was
  written to show.
- **A001 to A139 and B001 to B036**, the 175 probes of the independent adversarial audit of 13
  September 2026 (`audit/INDEPENDENT-AUDIT-2026-09-13.md`), entered as the audit supplied them. 48 of
  them came back checked within scope at the audited heads; every one now returns a status the audit
  accepts, and each fixture's `required` field names what the audit accepts.
- **Seven clearance classes, 159 fixtures**, written against the grammar above from both sides:
  **CUR01 to CUR24** currencies (20 refused, 4 accepted), **SIGN01 to SIGN26** sign forms and debit or
  credit markers (21 refused, 5 accepted), **SAME01 to SAME28** no-change and sameness words (24
  refused, 4 accepted), **PER01 to PER33** periods and bases (24 refused, 9 accepted), **ANA01 to
  ANA20** claims carried to another account (16 refused, 4 accepted), **RESP01 to RESP14**
  `respectively` (11 refused, 3 accepted), and **QTY01 to QTY14** words that size, rank or share a
  movement (10 refused, 4 accepted).

The runner lifts the script out of `checker.html` and runs it against a document stub, so there is
no build step and no dependency; a change to the page that breaks a probe fails the suite. After the
third review's repairs the four samples keep their sentence statuses; the Halyard queue grows from
13 items to 14, because card 13's "a shift toward lower margin produce" now comes back as a direction
word the checker cannot tie to a line. The clearance grammar moves no sample's sentence statuses and
no coverage strip: every word it would hold in the samples stands in a sentence that already failed,
needs review or carries no figure.

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
- **No second currency and no scale words.** `€30,000`, `USD 90000`, `30,000 euros`, `30,000
  Canadian dollars`, `$30.0 thousand`, `30 basis points` and `0.30 times the prior balance` are
  recorded as unparsed and the sentence is left unchecked, and a currency named anywhere else in the
  sentence holds it at needs review. The page reads one currency, written in whole units with a
  dollar sign or the word dollars.
- **No reading of sameness, comparison, period or basis words.** `stable at $130,000`, `in line
  with May`, `year over year`, `against budget`, `quarter to date`, `run rate`, `so did Insurance
  expense` and `30,000 CR` are not worked out. The clearance grammar holds the sentence and names the
  word, and a person reads it.
- **No multipliers, fractions or other scripts.** `doubled`, `twice`, `one and a half percent`, `a
  quarter of`, `½`, `thirty point five` and digits outside 0 to 9 are recorded as unparsed and the
  sentence is left unchecked. It does not work out what they assert.
- **No check on counts.** `12 new leases` and `the thirty-one new plans` are named as left outside
  the check. Nothing in a ledger balance can confirm a count of leases, plans or people.
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

Run it **first**, before anybody reads the memo, and read the coverage strip before the sentences: how
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
its figures checked within scope, direction PASS, and each "no source on file" straight into the
reviewer's queue as a question for the controller. The three Prompt 1 drafts retained in `evidence/`
went from 0 of 17 sentences checked within scope to 14 of 17 once `prior` and `current` were read as
roles; the counts, inputs and revisions are in `audit/PROMPT1-RERUN-2026-09-13.md`.

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
and `cases/brightwater-v5.json`, which are the same files the game reads, so the checker and the
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
**14** in the reviewer queue.

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

**Brightwater Dental Partners** is generated from `cases/brightwater-v5.json`, the five-account,
five-sentence dental group the game scores a player on cold. The Memo version field carries
`brightwater-v5 memo, 13 September 2026`. A plain tab separated ledger with a two column header,
`Account / May 2026 / June 2026`, read chronologically. Thresholds $25,000 and 10 percent, both
legs, no ratios.

Coverage strip: **5** sentences read, **5** checked within scope, **0** needs review,
**0** not checked, **0** failed, **5** ledger rows used, **0** rows skipped, **0** silent lines,
**0** in the reviewer queue.

This is the sample where the checker clears everything and settles nothing, and that is the point
of it. Every figure in the memo is right and every direction word agrees with the sign, so the
mechanical pass has no finding to make. The counts in it, `thirty-one new orthodontic plans` and `two
associate dentists`, and the dates, `1 June`, are named in each explanation as left outside the check. What each sentence then asserts is a cause, and a cause is
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
