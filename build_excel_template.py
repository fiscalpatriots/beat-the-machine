"""Build Second-Pass-Excel-Template.xlsx.

The Excel edition of the Second Pass review, version 2.0, aligned to PROTOCOL.md version 1.1
and to the checker's contract in CHECKER.md: the four sentence statuses, coverage counts rather
than a failure count, and the reviewer's two judgment questions answered Yes, No or Not on file.

The workbook recomputes the ledger, decides which lines owe commentary, names the lines nobody
explained, lays the ledger figure beside the figure a sentence states, and counts the reviewer
queue. It does not read a sentence. Every status the sheet suggests is a suggestion and the
reviewer enters the status that stands, which the sheet checks can only be the same or worse.

Run: python build_excel_template.py
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = "Second-Pass-Excel-Template.xlsx"
VERSION = "Version 2.0, 13 September 2026"
PROTOCOL = "Protocol version 1.1, 13 September 2026"
CASE = "halyard-v4, 13 September 2026"
SITE = "https://fiscalpatriots.github.io/beat-the-machine/"

GREEN = "006633"
GOLD = "FFCC33"
PALE_GOLD = "FFF6DA"
PALE_GREEN = "EAF3ED"

MONEY = '$#,##0;($#,##0)'
PCT = '0.0%;(0.0%)'
SHARE = '0.0%'
FIG = '#,##0.##;(#,##0.##)'

head_font = Font(bold=True, color="FFFFFF", size=11)
head_fill = PatternFill("solid", fgColor=GREEN)
gold_head_fill = PatternFill("solid", fgColor=GOLD)
gold_head_font = Font(bold=True, color="333333", size=11)
pale_gold_fill = PatternFill("solid", fgColor=PALE_GOLD)
pale_green_fill = PatternFill("solid", fgColor=PALE_GREEN)
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)

LEDGER_ROWS = 45   # header on 1, data 2..45 (14 prefilled, 30 blank, 1 spare)
MEMO_ROWS = 43     # header on 1, data 2..43 (12 prefilled, 30 blank)
LOG_ROWS_TOTAL = 36

STATUSES = ["Checked within scope", "Needs review", "Not checked", "Failed"]
STATUS_ARRAY = '{"Checked within scope","Not checked","Needs review","Failed"}'  # mild to severe
ANSWERS = ["Yes", "No", "Not on file"]

# ---------------------------------------------------------------- the case, halyard-v4
LEDGER = [
    (4000, "Product revenue, distribution", 5240000, 5612000),
    (4100, "Service revenue, equipment maintenance", 812000, 1041000),
    (4200, "Freight billed to customers", 186000, 121000),
    (5000, "Cost of product sold", 3930000, 4278000),
    (5100, "Inbound freight", 214000, 287800),
    (6000, "Warehouse wages", 630000, 702500),
    (6100, "Fleet fuel", 96400, 91200),
    (6200, "Repairs and maintenance, depots", 41000, 118600),
    (6300, "Software subscriptions", 28500, 30100),
    (6400, "Bad debt expense", 15000, 62000),
    (6500, "Professional fees", 55000, 47500),
    (7000, "Depreciation", 128000, 128000),
    (7100, "Interest expense", 61200, 92400),
    (7400, "Inventory shrink adjustment", 6400, 8900),
]

# line, sentence, account, figure stated, basis, direction stated,
# status the reviewer entered, driver answer, timing answer, document relied on or the ask
MEMO = [
    ("S1",
     "Freight billed to customers fell from $186,000 to $121,000, a decrease of $6,500 and 3.5 "
     "percent, so neither leg of the threshold is met and no commentary is owed on this line.",
     4200, 6500, "Change", "down", "Failed", "", "",
     "Recompute the movement on account 4200 and amend the sentence. The fall is $65,000 and 34.9 "
     "percent, so the line clears both legs and owes a driver the memo never gives."),
    ("S2",
     "Depot repairs and maintenance of $118,600 reflects the roof and dock leveler program, which "
     "finished on June 30. The remaining work on that same roof and dock leveler program is "
     "scheduled to finish in August, and that spend is not yet in these numbers.",
     6200, 118600, "Current", "none", "Needs review", "", "",
     "State what depot work was performed in June, how much of it is recorded, whether any of it "
     "is an improvement rather than a repair, and whether June owes an accrual on the work "
     "finishing in August. One program cannot be both finished and still running."),
    ("S3",
     "Inbound freight declined to $287,800 as carrier fuel surcharges eased.",
     5100, 287800, "Current", "down", "Failed", "", "",
     "State what drove the 34.5 percent rise in inbound freight, and amend the direction word. The "
     "balance rose $73,800."),
    ("S4",
     "Service revenue rose $229,000 as the twelve equipment maintenance contracts signed in the "
     "spring began service in June, and each month's fee is earned in the month it covers.",
     4100, 229000, "Change", "up", "Checked within scope", "Yes", "Yes",
     "The twelve signed maintenance contracts and the June earned revenue bridge, which place the "
     "full $229,000 in June on the service dates."),
    ("S5",
     "Professional fees fell $7,500 because May carried a one-time $7,500 invoice from outside "
     "counsel for the depot lease renewal review, and the movement fails the dollar leg of the "
     "threshold.",
     6500, 7500, "Change", "down", "Checked within scope", "Yes", "Yes",
     "The May invoice from outside counsel for the depot lease renewal review."),
    ("S6",
     "Product revenue of $5,612,000 grew on the Tri-State depot ramp, which management expects to "
     "continue through the third quarter.",
     4000, 5612000, "Current", "up", "Needs review", "", "",
     "Produce the depot revenue bridge or the documented forecast behind the Tri-State ramp. "
     "Account 4000 also carries S10, so settle which sentence the close file releases."),
    ("S7",
     "Bad debt expense increased $42,000 following the reserve taken against the Coastal Grocers "
     "receivable.",
     6400, 42000, "Change", "up", "Failed", "", "",
     "State what the $5,000 above the Coastal Grocers reserve is and produce the June reserve "
     "rollforward, or amend the sentence to $47,000, which is what the ledger moved."),
    ("S8",
     "Fleet fuel fell $5,200, and the movement fails both legs of the threshold, so the line owes "
     "no commentary at all.",
     6100, 5200, "Change", "down", "Checked within scope", "", "",
     "No driver named. The sentence makes a threshold claim only, and the claim recomputes."),
    ("S9",
     "Software subscriptions rose $1,600, which clears neither leg of the threshold, so this line "
     "carries no driver.",
     6300, 1600, "Change", "up", "Checked within scope", "", "",
     "No driver named. The sentence makes a threshold claim only, and the claim recomputes."),
    ("S10",
     "Distribution revenue of $5,612,000 grew 7.1 percent over May on continued customer demand "
     "across all four depots.",
     4000, 5612000, "Current", "up", "Needs review", "", "",
     "Produce the customer level billing bridge behind continued demand across all four depots. "
     "Account 4000 also carries S6."),
    ("S11",
     "Cost of product sold rose $348,000 against a $372,000 rise in product revenue. Product gross "
     "profit rose from $1,310,000 to $1,334,000, while product gross margin fell from 25.0 percent "
     "in May to 23.8 percent in June. The category report points to a shift toward lower margin "
     "produce and dairy lines as the likely cause, and a category sales and cost bridge has been "
     "requested to confirm it.",
     5000, 348000, "Change", "up", "Checked within scope", "Not on file", "Yes",
     "The category report is on file and points to mix. The category sales and cost bridge has "
     "been requested and is not on file, so the cause stands as a hypothesis."),
    ("S12",
     "Interest expense rose $31,200 on the depot equipment additions that also sit in "
     "depreciation.",
     7100, 31200, "Change", "up", "Needs review", "", "",
     "Produce the revolver draw and repayment dates, the daily balances, the rate and the fees. "
     "Account 7000 depreciation did not move at all, so the account the sentence points at cannot "
     "carry the driver."),
]

LOG_HEADERS = ["close period", "memo version", "line", "account", "sentence", "check",
               "result", "finding", "ask to the controller", "reviewer answer",
               "resolved", "reviewer name", "date", "controller sign-off"]

LOG_ROWS = [
    ["June 2026, Halyard training case", "Draft 2", "6400", "Bad debt expense", "S7",
     "arithmetic", "fail",
     "S7 accounts for $42,000. Account 6400 moved $47,000, from $15,000 to $62,000. The difference "
     "is $5,000.",
     "State what the $5,000 above the Coastal Grocers reserve is and produce the June reserve "
     "rollforward, or amend S7 to a figure the ledger supports.",
     "Preparer amended S7 to $47,000, which recomputes against the ledger and ties. What the "
     "$5,000 above the named Coastal Grocers reserve is has not been established and no June "
     "reserve rollforward is on file, so the ask stays open and the sentence is held back from "
     "release.",
     "no", "K. Alkurd", "2026-07-08", "pending"],
    ["June 2026, Halyard training case", "Draft 2", "6000", "Warehouse wages", "none",
     "silence", "fail",
     "The account moved $72,500 and 11.5 percent, which clears both legs, and no sentence in the "
     "memo covers it.",
     "Produce a driver for warehouse wages, or confirm the line is released with no explanation "
     "and why.",
     "", "no", "K. Alkurd", "2026-07-08", "pending"],
    ["June 2026, Halyard training case", "Draft 2", "4000", "Product revenue, distribution", "S6",
     "driver", "reviewer",
     "S6 credits the $372,000 movement to the Tri-State depot ramp. Nothing in the close binder "
     "ties that ramp to the figure, and the pricing memo of 20 May moves freight into the product "
     "price from 1 June, which puts $65,000 of the movement in account 4200 rather than in demand.",
     "Produce the support behind the Tri-State ramp, and state how much of the $372,000 is the "
     "freight reclassification.",
     "Not supported as written. The $65,000 is a reclassification out of account 4200 under the "
     "delivered pricing change, and the rest carries no document. Sentence held back from release.",
     "no", "K. Alkurd", "2026-07-08", "pending"],
    ["June 2026, Halyard training case", "Draft 2", "5100", "Inbound freight", "S3",
     "direction", "fail",
     "S3 says inbound freight declined. The balance rose from $214,000 to $287,800, a rise of "
     "$73,800 and 34.5 percent, which clears both legs.",
     "Amend the direction word and state what drove the rise, because a fuel surcharge easing "
     "cannot produce it.",
     "", "no", "K. Alkurd", "2026-07-08", "pending"],
]

CHANGE_LOG = [
    ["2.0", "13 September 2026",
     "Memo sheet carries a Status column holding the checker's four statuses, the reviewer's two "
     "judgment questions as Yes, No or Not on file, the document relied on or the ask, and a "
     "reviewer queue flag. A Summary sheet counts coverage by status rather than counting "
     "failures. Halyard rows rebuilt on halyard-v4. A Change log sheet was added.",
     "Protocol version 1.1 rewrote steps 3 and 4 to the checker's contract, and version 1.0 of "
     "this workbook predated it. A pass or fail count says nothing about how much of the memo was "
     "settled, which is what coverage is for."],
    ["2.0", "13 September 2026",
     "The workbook now suggests a status and the reviewer enters the one that stands, with a "
     "per-row check that the entered status is never milder than the suggestion.",
     "Protocol step 3: a status is never promoted. A reviewer may demote a sentence the mechanical "
     "checks cleared, and the sheet has to allow that without allowing the reverse."],
    ["2.0", "13 September 2026",
     "Sentence numbering follows halyard-v4 card order, so the bad debt sentence is S7 and the "
     "Tri-State sentence is S6.",
     "EVIDENCE-LOG-TEMPLATE.csv was written against the earlier numbering and calls them S2 and "
     "S5. The columns are unchanged; only the line labels moved."],
    ["2.0", "13 September 2026",
     "Account 4200 now carries a sentence, so the silent list is warehouse wages alone rather "
     "than warehouse wages and freight billed.",
     "halyard-v4 puts the freight sentence in the memo block. The silent list is computed, so it "
     "followed the case."],
    ["1.0", "13 September 2026",
     "First issue: Ledger, Settings, Memo, Silence, Reviewer log and a Read me.",
     "A controller already has Excel open, and the browser checker cannot be pasted into a close "
     "file."],
]


def write_header(ws, headers, gold_cols=(), row=1, height=32):
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=row, column=i, value=h)
        if i in gold_cols:
            c.fill = gold_head_fill
            c.font = gold_head_font
        else:
            c.fill = head_fill
            c.font = head_font
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = box
    ws.row_dimensions[row].height = height
    ws.freeze_panes = "A%d" % (row + 1)


def set_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def prose(ws, lines, col=2, width=105):
    r = 1
    for kind, text in lines:
        c = ws.cell(row=r, column=col, value=text)
        if kind == "h1":
            c.font = Font(bold=True, size=18, color=GREEN)
            ws.row_dimensions[r].height = 26
        elif kind == "h2":
            c.font = Font(bold=True, size=12, color=GREEN)
            ws.row_dimensions[r].height = 22
        elif kind == "sub":
            c.font = Font(size=10, color="555555")
        else:
            c.font = Font(size=11)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if text:
                ws.row_dimensions[r].height = max(15, 15 * (len(text) // width + 1))
        r += 1
    return r - 1


wb = Workbook()

# ================================================================ Read me
ws = wb.active
ws.title = "Read me"
set_widths(ws, [4, 112])
last = prose(ws, [
    ("h1", "Second Pass: the Excel edition"),
    ("sub", VERSION + ". Built by Khaled Alkurd. " + PROTOCOL + ". Case " + CASE + "."),
    ("sub", SITE),
    ("", ""),
    ("h2", "What this workbook checks"),
    ("p", "Three things, and it checks them by arithmetic on the numbers you type."),
    ("p", "Threshold. Change and percent are recomputed on every account from the two balances, each leg is tested against its floor, and the rule on Settings decides which lines owe commentary. Change the rule cell and every line reprices."),
    ("p", "Silence. Every account that clears the rule and carries no sentence is named on the Silence sheet and counted on Summary."),
    ("p", "The figure and the direction, laid beside the ledger. You type the figure a sentence states and pick which ledger figure it claims to be, and the sheet looks that figure up, compares the two within the tolerance on Settings, and compares the direction you read out of the sentence against the sign of the movement. The comparison is the workbook's. The reading is yours."),
    ("", ""),
    ("h2", "What this workbook does not check"),
    ("p", "It does not read English. No sentence is scanned for a figure, an account or a direction word, so a row is worth exactly as much as the account, figure, basis and direction you picked for it."),
    ("p", "It does not decide a status. Column L suggests one from the comparisons it ran. Column M is yours, and the protocol says a status is never promoted, so the sheet lets you enter a worse status than it suggested and flags it in column R if you enter a milder one."),
    ("p", "It does not answer the two judgment questions. Whether the driver a sentence names rests on a document on file, and whether that driver belongs to the period the sentence covers, are yours to answer in columns N and O as Yes, No or Not on file."),
    ("p", "It does not find a contradiction between two sentences, and it does not know that two sentences about the same account disagree. It counts them and sends the account to the queue."),
    ("p", "It does not decide anything about release. Nothing in this file says a memo is fit to go out. A reviewer signs the log and the controller signs the release."),
    ("p", "It does not reach outside itself. No links to other workbooks, no web queries, no macros. Closing the file is the whole retention policy."),
    ("", ""),
    ("h2", "How to use it, six steps"),
    ("p", "1. Settings. Set the dollar floor, the percent floor, the rule, the close period, the memo version and the two tie tolerances."),
    ("p", "2. Ledger. Replace the fourteen Halyard rows with your accounts and the two balances. Thirty blank rows below carry the same formulas."),
    ("p", "3. Memo. One row per sentence. Pick the account, type the figure the sentence states, pick which ledger figure it claims to be, and pick the direction the sentence states. A percent goes in as points, so 7.1 for 7.1 percent. Where a sentence carries more than one testable figure, put in the figure that carries the claim and raise the others on the Reviewer log."),
    ("p", "4. Read column L, then enter column M. Failed means a figure or a direction disagrees with the ledger. Needs review means something is unresolved. Not checked means nothing in the sentence could be tied to the ledger and tested, which is not the same as checked and true. Checked within scope means the figures tie, and it does not mean the sentence is true."),
    ("p", "5. Answer columns N and O on the sentences you checked within scope, and on a sentence at Needs review once the preparer has resolved it. A sentence still unresolved carries an ask in column P instead of an answer."),
    ("p", "6. Work the queue. Summary counts it: every sentence at Failed, Needs review or Not checked, every account carrying two or more sentences, and every silent line. Write each one onto the Reviewer log, sign it with your name and the date, and file it with the memo version it covers."),
    ("", ""),
    ("h2", "The four statuses, and why one is never promoted"),
    ("p", "The statuses are the checker's, in CHECKER.md, and they carry the same meaning here. A later step keeps the worst status any step assigned. A failed sentence stays failed until the preparer answers it, and the corrected sentence comes back in as a new row at step 3 rather than as an edit to the old one."),
    ("", ""),
    ("h2", "What is prefilled"),
    ("p", "The Halyard June 2026 training case at halyard-v4: fourteen accounts on Ledger, the twelve drafted sentences on Memo with the statuses a reviewer entered, the four worked rows on Reviewer log. The bad debt sentence is the one to look at first. It states $42,000 against a ledger movement of $47,000, the preparer amended it, and the ask about the $5,000 above the named reserve is still open, so the row is filed unresolved and the controller sign-off is pending."),
    ("", ""),
    ("h2", "One thing to know about formulas"),
    ("p", "This file was written by a script rather than by Excel, so the formula cells hold formulas and no cached answers. Excel computes them the moment you open the file. If a cell looks empty on first open, press F9."),
    ("", ""),
    ("h2", "The protocol this belongs to"),
    ("p", "PROTOCOL.md in this repository is the page a reviewer works from, EVIDENCE-LOG-TEMPLATE.csv is the log, CHECKER.md sets out the statuses and the coverage counts, and the browser version of the same checks is at " + SITE + "checker.html."),
])
ws.sheet_view.showGridLines = False
ws.print_area = "A1:B%d" % last

# ================================================================ Ledger
lg = wb.create_sheet("Ledger")
write_header(lg, ["Account", "Name", "Prior", "Current", "Change", "Percent",
                  "Clears dollar leg", "Clears percent leg", "Owes commentary"],
             gold_cols=(9,))
set_widths(lg, [11, 40, 15, 15, 15, 11, 13, 13, 15])
for r in range(2, LEDGER_ROWS + 1):
    i = r - 2
    if i < len(LEDGER):
        acct, name, prior, cur = LEDGER[i]
        lg.cell(row=r, column=1, value=acct)
        lg.cell(row=r, column=2, value=name)
        lg.cell(row=r, column=3, value=prior)
        lg.cell(row=r, column=4, value=cur)
    lg.cell(row=r, column=5, value='=IF(OR($C{r}="",$D{r}=""),"",$D{r}-$C{r})'.format(r=r))
    lg.cell(row=r, column=6,
            value='=IF(OR($C{r}="",$D{r}="",$C{r}=0),"",($D{r}-$C{r})/ABS($C{r}))'.format(r=r))
    lg.cell(row=r, column=7,
            value='=IF($E{r}="","",IF(ABS($E{r})>Settings!$B$2,"yes","no"))'.format(r=r))
    lg.cell(row=r, column=8,
            value='=IF($F{r}="","",IF(ABS($F{r})>=Settings!$B$3/100,"yes","no"))'.format(r=r))
    lg.cell(row=r, column=9,
            value=('=IF($E{r}="","",IF(LOWER(Settings!$B$4)="both",'
                   'IF(AND($G{r}="yes",$H{r}="yes"),"yes","no"),'
                   'IF(OR($G{r}="yes",$H{r}="yes"),"yes","no")))').format(r=r))
    for col in (3, 4, 5):
        lg.cell(row=r, column=col).number_format = MONEY
    lg.cell(row=r, column=6).number_format = PCT
    for col in range(1, 10):
        cell = lg.cell(row=r, column=col)
        cell.border = box
        if col in (1, 7, 8, 9):
            cell.alignment = Alignment(horizontal="center")
        if col == 9:
            cell.fill = pale_gold_fill
            cell.font = Font(bold=True)
lg.auto_filter.ref = "A1:I%d" % LEDGER_ROWS
lg.print_area = "A1:I%d" % LEDGER_ROWS

# ================================================================ Settings
st = wb.create_sheet("Settings")
write_header(st, ["Setting", "Value", "Note"])
set_widths(st, [34, 34, 70])
settings = [
    ("Dollar floor", 25000, "A movement must exceed this to clear the dollar leg. The rule is more than, so a movement of exactly the floor does not clear it."),
    ("Percent floor (points)", 10, "A movement must reach this percent of the prior balance to clear the percent leg. The rule is at least, so a movement of exactly the floor does clear it."),
    ("Rule", "both", "both means a line owes commentary only when it clears both legs. either means one leg is enough."),
    ("Close period", "June 2026, Halyard training case", "Rides along on the reviewer log so a filed log says which close it came from."),
    ("Memo version", "Draft 2", "The version of the commentary these results cover. The log and the memo are filed together so a reader can see which words the signature covers."),
    ("Tie tolerance, dollars", 1, "A memo figure ties to the ledger when the two are within this many dollars."),
    ("Tie tolerance, percentage points", 0.05, "A memo percent ties when the two are within this many points."),
]
for i, (k, v, note) in enumerate(settings, start=2):
    st.cell(row=i, column=1, value=k).font = Font(bold=True)
    c = st.cell(row=i, column=2, value=v)
    c.fill = pale_gold_fill
    st.cell(row=i, column=3, value=note).alignment = Alignment(wrap_text=True, vertical="top")
    st.row_dimensions[i].height = 30
    for col in range(1, 4):
        st.cell(row=i, column=col).border = box
st.cell(row=2, column=2).number_format = MONEY
st.cell(row=7, column=2).number_format = MONEY
dv_rule = DataValidation(type="list", formula1='"both,either"', allow_blank=False)
dv_rule.error = "The rule is either both or either."
st.add_data_validation(dv_rule)
dv_rule.add(st["B4"])
st.print_area = "A1:C8"

# ================================================================ Memo
mm = wb.create_sheet("Memo")
MEMO_HEADERS = ["Line", "Sentence", "Account", "Figure in sentence", "Figure basis",
                "Ledger figure", "Figure ties", "Direction stated", "Direction on ledger",
                "Direction ties", "Owes commentary", "Status the sheet suggests",
                "Status", "Is the driver supported by a document on file?",
                "Does the driver belong to the period the sentence covers?",
                "Document relied on, or the ask to the controller",
                "In the reviewer queue", "Status promoted"]
write_header(mm, MEMO_HEADERS, gold_cols=(13, 14, 15))
set_widths(mm, [7, 62, 11, 15, 12, 15, 9, 12, 12, 11, 13, 17, 17, 20, 20, 56, 12, 12])
L_A = "Ledger!$A$2:$A$%d" % LEDGER_ROWS
for r in range(2, MEMO_ROWS + 1):
    i = r - 2
    if i < len(MEMO):
        line, sentence, acct, fig, basis, direction, status, drv, tim, doc = MEMO[i]
        mm.cell(row=r, column=1, value=line)
        mm.cell(row=r, column=2, value=sentence)
        mm.cell(row=r, column=3, value=acct)
        if fig is not None:
            mm.cell(row=r, column=4, value=fig)
        mm.cell(row=r, column=5, value=basis)
        mm.cell(row=r, column=8, value=direction)
        mm.cell(row=r, column=13, value=status)
        if drv:
            mm.cell(row=r, column=14, value=drv)
        if tim:
            mm.cell(row=r, column=15, value=tim)
        mm.cell(row=r, column=16, value=doc)
        mm.row_dimensions[r].height = 62
    mm.cell(row=r, column=6, value=(
        '=IF(OR($C{r}="",$E{r}=""),"",IFERROR(IF($E{r}="Percent",'
        'INDEX(Ledger!$F$2:$F${n},MATCH($C{r},{la},0))*100,'
        'INDEX(Ledger!$C$2:$E${n},MATCH($C{r},{la},0),'
        'MATCH($E{r},{{"Prior","Current","Change"}},0))),""))'
    ).format(r=r, n=LEDGER_ROWS, la=L_A))
    mm.cell(row=r, column=7, value=(
        '=IF(OR($D{r}="",$F{r}=""),"",IF(ABS(ABS($D{r})-ABS($F{r}))<='
        'IF($E{r}="Percent",Settings!$B$8,Settings!$B$7),"yes","no"))'
    ).format(r=r))
    mm.cell(row=r, column=9, value=(
        '=IF($C{r}="","",IFERROR(IF(INDEX(Ledger!$E$2:$E${n},MATCH($C{r},{la},0))="","",'
        'IF(INDEX(Ledger!$E$2:$E${n},MATCH($C{r},{la},0))>0,"up",'
        'IF(INDEX(Ledger!$E$2:$E${n},MATCH($C{r},{la},0))<0,"down","none"))),""))'
    ).format(r=r, n=LEDGER_ROWS, la=L_A))
    mm.cell(row=r, column=10, value=(
        '=IF(OR($H{r}="",$H{r}="none",$I{r}=""),"",IF($H{r}=$I{r},"yes","no"))'
    ).format(r=r))
    mm.cell(row=r, column=11, value=(
        '=IF($C{r}="","",IFERROR(INDEX(Ledger!$I$2:$I${n},MATCH($C{r},{la},0)),""))'
    ).format(r=r, n=LEDGER_ROWS, la=L_A))
    # Suggested status: failed, then unresolved, then checked, then nothing tied.
    mm.cell(row=r, column=12, value=(
        '=IF($C{r}="","",'
        'IF(OR($G{r}="no",$J{r}="no"),"Failed",'
        'IF(OR(AND($D{r}<>"",$E{r}=""),AND($D{r}="",$E{r}<>""),AND($D{r}<>"",$F{r}="")),'
        '"Needs review",'
        'IF(OR($G{r}="yes",$J{r}="yes"),"Checked within scope","Not checked"))))'
    ).format(r=r))
    mm.cell(row=r, column=17, value=(
        '=IF($C{r}="","",IF(OR($M{r}="Failed",$M{r}="Needs review",$M{r}="Not checked",'
        'COUNTIF($C$2:$C${n},$C{r})>1),"yes","no"))'
    ).format(r=r, n=MEMO_ROWS))
    mm.cell(row=r, column=18, value=(
        '=IF(OR($L{r}="",$M{r}=""),"",IF(MATCH($M{r},{a},0)<MATCH($L{r},{a},0),"yes","no"))'
    ).format(r=r, a=STATUS_ARRAY))
    mm.cell(row=r, column=4).number_format = FIG
    mm.cell(row=r, column=6).number_format = FIG
    for col in range(1, 19):
        cell = mm.cell(row=r, column=col)
        cell.border = box
        if col in (2, 16):
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        else:
            cell.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
        if col == 13:
            cell.fill = pale_gold_fill
            cell.font = Font(bold=True)
        elif col in (14, 15):
            cell.fill = pale_gold_fill
        elif col in (12, 17, 18):
            cell.fill = pale_green_fill
dv_acct = DataValidation(type="list", formula1="=%s" % L_A, allow_blank=True)
mm.add_data_validation(dv_acct)
dv_acct.add("C2:C%d" % MEMO_ROWS)
dv_basis = DataValidation(type="list", formula1='"Prior,Current,Change,Percent"', allow_blank=True)
mm.add_data_validation(dv_basis)
dv_basis.add("E2:E%d" % MEMO_ROWS)
dv_dir = DataValidation(type="list", formula1='"up,down,none"', allow_blank=True)
mm.add_data_validation(dv_dir)
dv_dir.add("H2:H%d" % MEMO_ROWS)
dv_status = DataValidation(type="list", formula1='"%s"' % ",".join(STATUSES), allow_blank=True)
dv_status.error = "Use one of the four statuses: Checked within scope, Needs review, Not checked, Failed."
dv_status.promptTitle = "The four statuses"
dv_status.prompt = ("Checked within scope means the figures tie, not that the sentence is true. "
                    "Not checked means nothing could be tied and tested. A status is never promoted.")
mm.add_data_validation(dv_status)
dv_status.add("M2:M%d" % MEMO_ROWS)
dv_answer = DataValidation(type="list", formula1='"%s"' % ",".join(ANSWERS), allow_blank=True)
dv_answer.error = "Answer Yes, No or Not on file."
mm.add_data_validation(dv_answer)
dv_answer.add("N2:N%d" % MEMO_ROWS)
dv_answer2 = DataValidation(type="list", formula1='"%s"' % ",".join(ANSWERS), allow_blank=True)
dv_answer2.error = "Answer Yes, No or Not on file."
mm.add_data_validation(dv_answer2)
dv_answer2.add("O2:O%d" % MEMO_ROWS)
mm.auto_filter.ref = "A1:R%d" % MEMO_ROWS
mm.print_area = "A1:R%d" % MEMO_ROWS

# ================================================================ Silence
si = wb.create_sheet("Silence")
si.cell(row=1, column=1, value="Owes an explanation, none written").font = Font(bold=True, size=14, color=GREEN)
si.cell(row=2, column=1, value=("Every account that clears the rule on Settings and carries no sentence on the Memo "
                                "sheet, and every account carrying two or more. Both go to the reviewer queue."))
si.cell(row=2, column=1).font = Font(size=10, color="555555")
si.cell(row=3, column=1, value="Silent lines:").font = Font(bold=True)
si.cell(row=3, column=2, value='=COUNTIF($G$6:$G${n},"Owes an explanation, none written")'.format(n=LEDGER_ROWS + 4)).font = Font(bold=True)
HDR = 5
si_headers = ["Account", "Name", "Change", "Percent", "Owes commentary",
              "Sentences on this account", "Status"]
for i, h in enumerate(si_headers, start=1):
    c = si.cell(row=HDR, column=i, value=h)
    c.fill = gold_head_fill if i == 7 else head_fill
    c.font = gold_head_font if i == 7 else head_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = box
si.row_dimensions[HDR].height = 32
si.freeze_panes = "A%d" % (HDR + 1)
set_widths(si, [11, 40, 15, 11, 15, 15, 46])
for k in range(2, LEDGER_ROWS + 1):
    r = HDR + k - 1
    si.cell(row=r, column=1, value='=IF(Ledger!$A{k}="","",Ledger!$A{k})'.format(k=k))
    si.cell(row=r, column=2, value='=IF(Ledger!$A{k}="","",Ledger!$B{k})'.format(k=k))
    si.cell(row=r, column=3, value='=IF(Ledger!$A{k}="","",Ledger!$E{k})'.format(k=k))
    si.cell(row=r, column=4, value='=IF(Ledger!$A{k}="","",Ledger!$F{k})'.format(k=k))
    si.cell(row=r, column=5, value='=IF(Ledger!$A{k}="","",Ledger!$I{k})'.format(k=k))
    si.cell(row=r, column=6, value=(
        '=IF(Ledger!$A{k}="","",COUNTIF(Memo!$C$2:$C${m},Ledger!$A{k}))'
    ).format(k=k, m=MEMO_ROWS))
    si.cell(row=r, column=7, value=(
        '=IF($A{r}="","",IF($F{r}>1,"Two or more sentences on this account, reviewer queue",'
        'IF($E{r}<>"yes","No commentary owed",'
        'IF($F{r}=0,"Owes an explanation, none written","Explained, 1 sentence"))))'
    ).format(r=r))
    si.cell(row=r, column=3).number_format = MONEY
    si.cell(row=r, column=4).number_format = PCT
    for col in range(1, 8):
        cell = si.cell(row=r, column=col)
        cell.border = box
        if col != 2:
            cell.alignment = Alignment(horizontal="center")
        if col == 7:
            cell.fill = pale_gold_fill
            cell.alignment = Alignment(horizontal="left")
si.auto_filter.ref = "A%d:G%d" % (HDR, HDR + LEDGER_ROWS - 1)
si.print_area = "A1:G%d" % (HDR + LEDGER_ROWS - 1)
SI_LAST = HDR + LEDGER_ROWS - 1

# ================================================================ Summary
sm = wb.create_sheet("Summary")
set_widths(sm, [3, 52, 14, 12, 14, 14, 16])
M = "Memo!"
MN = MEMO_ROWS
sm.cell(row=1, column=2, value="Coverage, the queue and the signature").font = Font(bold=True, size=18, color=GREEN)
sm.cell(row=2, column=2, value=VERSION + ". " + PROTOCOL + ".").font = Font(size=10, color="555555")
sm.cell(row=3, column=2, value=("Counts, not a pass rate. Coverage says how much of the memo was settled and "
                                "how much a person still owes an answer on.")).font = Font(size=10, color="555555")
sm.cell(row=4, column=2, value="Close period").font = Font(bold=True)
sm.cell(row=4, column=3, value="=Settings!$B$5")
sm.cell(row=5, column=2, value="Memo version").font = Font(bold=True)
sm.cell(row=5, column=3, value="=Settings!$B$6")

row = 7
sm.cell(row=row, column=2, value="Sentence coverage, by status").font = Font(bold=True, size=12, color=GREEN)
row += 1
write_header(sm, ["", "Status", "Count", "Share"], row=row, height=20)
sm.freeze_panes = "A1"
status_first = row + 1
for s in STATUSES:
    row += 1
    sm.cell(row=row, column=2, value=s)
    sm.cell(row=row, column=3, value='=COUNTIF({m}$M$2:$M${n},$B{r})'.format(m=M, n=MN, r=row))
    sm.cell(row=row, column=4, value='=IF($C${t}=0,"",$C{r}/$C${t})'.format(r=row, t=row + (4 - STATUSES.index(s)) + 1))
status_last = row
row += 1
total_row = row
sm.cell(row=row, column=2, value="Sentences read").font = Font(bold=True)
sm.cell(row=row, column=3, value='=COUNTA({m}$C$2:$C${n})'.format(m=M, n=MN)).font = Font(bold=True)
# fix the share denominators now that the total row is known
for r in range(status_first, status_last + 1):
    sm.cell(row=r, column=4, value='=IF($C${t}=0,"",$C{r}/$C${t})'.format(r=r, t=total_row))
    sm.cell(row=r, column=4).number_format = SHARE
row += 1
sm.cell(row=row, column=2, value="No status entered yet")
sm.cell(row=row, column=3, value='=$C${t}-SUM($C${a}:$C${b})'.format(t=total_row, a=status_first, b=status_last))
no_status_row = row

row += 2
sm.cell(row=row, column=2, value="Ledger coverage").font = Font(bold=True, size=12, color=GREEN)
row += 1
write_header(sm, ["", "What", "Count"], row=row, height=20)
ledger_block = []
for label, formula in [
    ("Ledger rows used", '=COUNTA(Ledger!$A$2:$A${n})'.format(n=LEDGER_ROWS)),
    ("Lines that owe commentary", '=COUNTIF(Ledger!$I$2:$I${n},"yes")'.format(n=LEDGER_ROWS)),
    ("Of those, lines carrying at least one sentence",
     '=SUMPRODUCT((Ledger!$I$2:$I${n}="yes")*(COUNTIF(Memo!$C$2:$C${m},Ledger!$A$2:$A${n})>0))'.format(n=LEDGER_ROWS, m=MN)),
    ("Silent lines, owed and never written",
     '=COUNTIF(Silence!$G$6:$G${s},"Owes an explanation, none written")'.format(s=SI_LAST)),
    ("Accounts carrying two or more sentences",
     '=SUMPRODUCT((Ledger!$A$2:$A${n}<>"")*(COUNTIF(Memo!$C$2:$C${m},Ledger!$A$2:$A${n})>1))'.format(n=LEDGER_ROWS, m=MN)),
]:
    row += 1
    sm.cell(row=row, column=2, value=label)
    sm.cell(row=row, column=3, value=formula)
    ledger_block.append(row)
silent_row = ledger_block[3]

row += 2
sm.cell(row=row, column=2, value="The reviewer queue").font = Font(bold=True, size=12, color=GREEN)
row += 1
sm.cell(row=row, column=2, value=("Protocol step 3: what the checks could not settle. A status is never "
                                  "promoted, so a row leaves the queue only when the preparer answers it "
                                  "and the corrected sentence comes back in at step 1.")).font = Font(size=10, color="555555")
sm.row_dimensions[row].height = 28
sm.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
row += 1
write_header(sm, ["", "What", "Count"], row=row, height=20)
row += 1
q_sent = row
sm.cell(row=row, column=2, value="Sentences in the queue (failed, needs review, not checked, or an account with two or more)")
sm.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
sm.row_dimensions[row].height = 28
sm.cell(row=row, column=3, value='=COUNTIF({m}$Q$2:$Q${n},"yes")'.format(m=M, n=MN))
row += 1
sm.cell(row=row, column=2, value="Silent lines in the queue")
sm.cell(row=row, column=3, value='=$C${s}'.format(s=silent_row))
q_silent = row
row += 1
sm.cell(row=row, column=2, value="Reviewer queue, total").font = Font(bold=True)
sm.cell(row=row, column=3, value='=$C${a}+$C${b}'.format(a=q_sent, b=q_silent)).font = Font(bold=True)
sm.cell(row=row, column=3).fill = pale_gold_fill
queue_total_row = row

row += 2
sm.cell(row=row, column=2, value="The reviewer's two judgment questions").font = Font(bold=True, size=12, color=GREEN)
row += 1
sm.cell(row=row, column=2, value=("Protocol step 4. Answered on the sentences checked within scope, and on a "
                                  "sentence at needs review once it is resolved. An unresolved sentence carries "
                                  "an ask in column P instead of an answer.")).font = Font(size=10, color="555555")
sm.row_dimensions[row].height = 28
sm.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
row += 1
write_header(sm, ["", "Question", "Yes", "No", "Not on file", "Not answered"], row=row, height=20)
for label, col in [("Is the driver supported by a document on file?", "N"),
                   ("Does the driver belong to the period the sentence covers?", "O")]:
    row += 1
    sm.cell(row=row, column=2, value=label)
    for j, ans in enumerate(ANSWERS):
        sm.cell(row=row, column=3 + j,
                value='=COUNTIF({m}${c}$2:${c}${n},"{a}")'.format(m=M, c=col, n=MN, a=ans))
    sm.cell(row=row, column=6,
            value='=$C${t}-SUM($C{r}:$E{r})'.format(t=total_row, r=row))

row += 2
sm.cell(row=row, column=2, value="Checks on this sheet itself").font = Font(bold=True, size=12, color=GREEN)
row += 1
write_header(sm, ["", "What", "Count", "Must be"], row=row, height=20)
row += 1
sm.cell(row=row, column=2, value="Sentences whose entered status is milder than the sheet's suggestion")
sm.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
sm.row_dimensions[row].height = 28
sm.cell(row=row, column=3, value='=COUNTIF({m}$R$2:$R${n},"yes")'.format(m=M, n=MN))
sm.cell(row=row, column=4, value="0")
row += 1
sm.cell(row=row, column=2, value="Sentences checked within scope with neither judgment question answered")
sm.cell(row=row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
sm.row_dimensions[row].height = 28
sm.cell(row=row, column=3, value=(
    '=SUMPRODUCT(({m}$M$2:$M${n}="Checked within scope")*({m}$N$2:$N${n}="")*'
    '({m}$O$2:$O${n}=""))'
).format(m=M, n=MN))
sm.cell(row=row, column=4, value="Each one explained in column P")

row += 2
sm.cell(row=row, column=2, value="Signed").font = Font(bold=True, size=12, color=GREEN)
row += 1
sm.cell(row=row, column=2, value=("Protocol step 5. The log goes to the controller with the memo version it "
                                  "covers, and the controller sign-off is recorded on the same file.")).font = Font(size=10, color="555555")
row += 1
for label, value in [("Reviewer name", "K. Alkurd"),
                     ("Date signed", "2026-07-08"),
                     ("Memo version released", "=Settings!$B$6"),
                     ("Controller sign-off", "pending")]:
    row += 1
    sm.cell(row=row, column=2, value=label).font = Font(bold=True)
    c = sm.cell(row=row, column=3, value=value)
    c.fill = pale_gold_fill
    c.border = box
SUMMARY_LAST = row

for r in range(1, SUMMARY_LAST + 1):
    for col in range(2, 8):
        cell = sm.cell(row=r, column=col)
        if cell.value is not None and col >= 3 and r > 6:
            cell.alignment = Alignment(horizontal="center")
sm.sheet_view.showGridLines = False
sm.print_area = "A1:G%d" % SUMMARY_LAST

# ================================================================ Reviewer log
rl = wb.create_sheet("Reviewer log")
write_header(rl, LOG_HEADERS, gold_cols=(7,))
set_widths(rl, [26, 13, 9, 26, 9, 13, 10, 58, 46, 46, 10, 14, 12, 18])
for r in range(2, LOG_ROWS_TOTAL + 1):
    i = r - 2
    if i < len(LOG_ROWS):
        for col, val in enumerate(LOG_ROWS[i], start=1):
            rl.cell(row=r, column=col, value=val)
        rl.row_dimensions[r].height = 64
    for col in range(1, 15):
        cell = rl.cell(row=r, column=col)
        cell.border = box
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        if col == 7:
            cell.fill = pale_gold_fill
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="top")
dv_check = DataValidation(
    type="list",
    formula1='"arithmetic,direction,threshold,silence,driver,timing,contradiction,none"',
    allow_blank=True)
dv_check.error = "Use one of the named checks."
rl.add_data_validation(dv_check)
dv_check.add("F2:F%d" % LOG_ROWS_TOTAL)
dv_result = DataValidation(type="list", formula1='"pass,fail,review,info"', allow_blank=True)
dv_result.error = "Use pass, fail, review or info."
rl.add_data_validation(dv_result)
dv_result.add("G2:G%d" % LOG_ROWS_TOTAL)
dv_yn = DataValidation(type="list", formula1='"yes,no"', allow_blank=True)
rl.add_data_validation(dv_yn)
dv_yn.add("K2:K%d" % LOG_ROWS_TOTAL)
rl.auto_filter.ref = "A1:N%d" % LOG_ROWS_TOTAL
rl.print_area = "A1:N%d" % LOG_ROWS_TOTAL

# ================================================================ Change log
cl = wb.create_sheet("Change log")
write_header(cl, ["Version", "Date", "What changed", "Why"])
set_widths(cl, [11, 20, 74, 74])
cl.cell(row=2, column=1)
for i, rowvals in enumerate(CHANGE_LOG, start=2):
    for col, val in enumerate(rowvals, start=1):
        c = cl.cell(row=i, column=col, value=val)
        c.border = box
        c.alignment = Alignment(wrap_text=True, vertical="top")
    cl.row_dimensions[i].height = 62
CL_LAST = len(CHANGE_LOG) + 1
note_row = CL_LAST + 2
cl.cell(row=note_row, column=1, value=("Every rebuild adds a row, and a version used on a close is never edited. "
                                       "The workbook is generated by build_excel_template.py in this repository, "
                                       "so a correction is a change to the script and a rebuild rather than a hand "
                                       "edit nobody can reproduce."))
cl.cell(row=note_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
cl.cell(row=note_row, column=1).font = Font(size=10, color="555555")
cl.print_area = "A1:D%d" % note_row

# ================================================================ page setup
for sheet in (lg, mm, si, rl, cl, sm):
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
for sheet in (lg, mm, rl, cl):
    sheet.print_title_rows = "1:1"
si.print_title_rows = "%d:%d" % (HDR, HDR)
ws.page_setup.orientation = "portrait"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
sm.page_setup.orientation = "portrait"

wb.move_sheet("Summary", offset=-4)
wb.active = 0

wb.save(OUT)
print("wrote", OUT)
print("sheets:", wb.sheetnames)
