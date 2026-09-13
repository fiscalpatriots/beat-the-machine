"""Build Second-Pass-Excel-Template.xlsx.

The Excel edition of the Second Pass checks: threshold, silence, and a reviewer log.
Arithmetic and direction are checked by the reviewer against the figures the workbook
lays beside each memo line. The workbook does not read memo sentences.

Run: python build_excel_template.py
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT = "Second-Pass-Excel-Template.xlsx"
VERSION = "Version 1.0, 13 September 2026"
SITE = "https://fiscalpatriots.github.io/beat-the-machine/"

GREEN = "006633"
GOLD = "FFCC33"
PALE_GOLD = "FFF6DA"
GREY = "F2F2F2"

MONEY = '$#,##0;($#,##0)'
PCT = '0.0%;(0.0%)'
FIG = '#,##0.##;(#,##0.##)'

head_font = Font(bold=True, color="FFFFFF", size=11)
head_fill = PatternFill("solid", fgColor=GREEN)
gold_head_fill = PatternFill("solid", fgColor=GOLD)
gold_head_font = Font(bold=True, color="333333", size=11)
pale_gold_fill = PatternFill("solid", fgColor=PALE_GOLD)
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)

LEDGER_ROWS = 45  # header on 1, data 2..45 (14 prefilled + 30 blank + 1 spare)
MEMO_ROWS = 43    # header on 1, data 2..43 (12 prefilled + 30 blank)

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

# line, sentence, account, figure in sentence, basis, direction stated
MEMO = [
    ("S1", "Depot repairs and maintenance of $118,600 reflects the roof and dock leveler program, which finished on June 30.", 6200, 118600, "Current", "none"),
    ("S2", "Bad debt expense increased $42,000 following the reserve taken against the Coastal Grocers receivable.", 6400, 42000, "Change", "up"),
    ("S3", "Software subscriptions rose $1,600, which clears neither leg of the threshold, so this line carries no driver.", 6300, 1600, "Change", "up"),
    ("S4", "Distribution revenue of $5,612,000 grew 7.1 percent over May on continued customer demand across all four depots.", 4000, 5612000, "Current", "up"),
    ("S5", "The growth in both revenue lines is driven by the Tri-State depot ramp, which management expects to continue through the third quarter.", 4100, None, "", "up"),
    ("S6", "Inbound freight declined to $287,800 as carrier fuel surcharges eased.", 5100, 287800, "Current", "down"),
    ("S7", "Interest expense rose $31,200 on the depot equipment additions that also sit in depreciation.", 7100, 31200, "Change", "up"),
    ("S8", "Fleet fuel fell $5,200 on lower pump prices through June, and the movement fails both legs of the threshold, so the line owes no commentary at all. Every June fuel invoice from the fleet servicer was received and recorded before the books closed.", 6100, 5200, "Change", "down"),
    ("S9", "Service revenue rose $229,000 as the equipment maintenance contracts signed in the spring moved onto monthly billing in June, and each month's fee is earned in the month it covers.", 4100, 229000, "Change", "up"),
    ("S10", "The remaining depot repairs are scheduled to finish in August, and that spend is not yet in these numbers.", 6200, None, "", "none"),
    ("S11", "Cost of product sold rose $348,000 against a $372,000 rise in revenue, so product gross margin fell from 25.0 percent in May to 23.8 percent in June on a shift toward lower margin lines.", 5000, 348000, "Change", "up"),
    ("S12", "Professional fees fell $7,500 because May carried a one-time $7,500 invoice from outside counsel for the depot lease renewal review, and the movement fails the dollar leg of the threshold.", 6500, 7500, "Change", "down"),
]

LOG_HEADERS = ["close period", "memo version", "line", "account", "sentence", "check",
               "result", "finding", "ask to the controller", "reviewer answer",
               "resolved", "reviewer name", "date", "controller sign-off"]

LOG_ROWS = [
    ["June 2026, Halyard training case", "Draft 2", "6400", "Bad debt expense", "S2", "arithmetic", "fail",
     "S2 accounts for $42,000. Account 6400 moved $47,000, from $15,000 to $62,000. The difference is $5,000.",
     "State what the $5,000 above the Coastal Grocers reserve is and produce the June reserve rollforward, or amend S2 to a figure the ledger supports.",
     "Preparer amended S2 to $47,000, which recomputes against the ledger and ties. What the $5,000 above the named Coastal Grocers reserve is has not been established and no June reserve rollforward is on file, so the ask stays open and the sentence is held back from release.",
     "no", "K. Alkurd", "2026-07-08", "pending"],
    ["June 2026, Halyard training case", "Draft 2", "6000", "Warehouse wages", "none", "silence", "fail",
     "The account moved $72,500 and 11.5 percent, which clears both legs, and no sentence in the memo covers it.",
     "Produce a driver for warehouse wages, or confirm the line is released with no explanation and why.",
     "", "no", "K. Alkurd", "2026-07-08", "pending"],
    ["June 2026, Halyard training case", "Draft 2", "4000", "Product revenue, distribution", "S5", "driver", "reviewer",
     "S5 credits the $372,000 movement to the Tri-State depot ramp. Nothing in the close binder ties that ramp to the figure, and the pricing memo of 20 May moves freight into the product price from 1 June, which puts $65,000 of the movement in account 4200 rather than in demand.",
     "Produce the support behind the Tri-State ramp, and state how much of the $372,000 is the freight reclassification.",
     "Not supported as written. The $65,000 is a reclassification out of account 4200 under the delivered pricing change, and the rest carries no document. Sentence held back from release.",
     "no", "K. Alkurd", "2026-07-08", "pending"],
]


def write_header(ws, headers, gold_cols=()):
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=1, column=i, value=h)
        if i in gold_cols:
            c.fill = gold_head_fill
            c.font = gold_head_font
        else:
            c.fill = head_fill
            c.font = head_font
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = box
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "A2"


def set_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


wb = Workbook()

# ---------------------------------------------------------------- Read me
ws = wb.active
ws.title = "Read me"
set_widths(ws, [4, 112])
lines = [
    ("h1", "Second Pass: the Excel edition"),
    ("sub", VERSION + ". Built by Khaled Alkurd."),
    ("sub", SITE),
    ("", ""),
    ("h2", "What this workbook does"),
    ("p", "It runs the two checks a spreadsheet can run honestly. The threshold check recomputes the change and the percent on every account from the two balances and says which lines owe commentary under the rule on the Settings sheet. The silence check names every account that owes commentary and carries no sentence in the memo. The reviewer log is the evidence the close file keeps."),
    ("p", "It does not read your sentences. Nothing in here parses English, so arithmetic and direction are checked by you: the Memo sheet puts the figure the sentence states beside the figure the ledger carries, and beside the direction the balance actually moved, and you decide whether they agree. The comparison is arithmetic the workbook does; the reading is yours."),
    ("p", "Judgment stays where the protocol puts it. Whether a driver is supported by a document on file, and whether it belongs to the period the sentence covers, are questions for the reviewer and they never appear here as a verdict."),
    ("", ""),
    ("h2", "How to use it, five steps"),
    ("p", "1. Open Settings and set the dollar floor, the percent floor, the rule, the close period and the memo version for the close you are working."),
    ("p", "2. Replace the fourteen Halyard rows on Ledger with your own accounts, prior and current balances. Thirty blank rows below carry the same formulas. Change, percent and the two threshold legs compute themselves."),
    ("p", "3. Paste the memo on the Memo sheet, one sentence per row. Pick the account from the dropdown, type the figure the sentence states, pick which ledger figure it claims to be, and pick the direction the sentence states. Percent figures go in as points, so 7.1 for 7.1 percent."),
    ("p", "4. Read the Result column. FAIL means a figure or a direction does not agree with the ledger and the sentence goes back to the preparer. INFO means the account owes no commentary, and the sentence is still checked because a sentence that owes nothing can still say something false. REVIEW means the mechanical checks cleared it and it is yours to judge. Then read Silence, which lists every account that owes an explanation and has none written."),
    ("p", "5. Work every FAIL, every silent line and every REVIEW into the Reviewer log, sign it with your name and the date, and file it with the memo version it covers."),
    ("", ""),
    ("h2", "Privacy"),
    ("p", "Nothing leaves this file. There are no links to other workbooks, no web queries and no macros. The workbook computes with Excel's own formulas on the numbers you type, and closing the file is the whole retention policy."),
    ("", ""),
    ("h2", "What is prefilled"),
    ("p", "The Halyard June 2026 training case: fourteen accounts on Ledger, the twelve drafted sentences on Memo, and the three example rows on Reviewer log. Delete them once you have seen how the sheet behaves, or keep the file as the worked example and start a copy."),
    ("", ""),
    ("h2", "One thing to know about formulas"),
    ("p", "This file was written by a script rather than by Excel, so the formula cells hold formulas but no cached answers. Excel computes them the moment you open the file, and every figure below the headers appears then. If a cell looks empty on first open, press F9."),
    ("", ""),
    ("h2", "The protocol this belongs to"),
    ("p", "PROTOCOL.md in this repository is the one page a reviewer works from, EVIDENCE-LOG-TEMPLATE.csv is the log, and the browser version of the same checks is at " + SITE + "checker.html."),
]
r = 1
for kind, text in lines:
    c = ws.cell(row=r, column=2, value=text)
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
            ws.row_dimensions[r].height = max(15, 15 * (len(text) // 105 + 1))
    if kind == "p":
        c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1
ws.sheet_view.showGridLines = False
ws.print_area = "A1:B%d" % (r - 1)

# ---------------------------------------------------------------- Ledger
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
    lg.cell(row=r, column=5,
            value='=IF(OR($C{r}="",$D{r}=""),"",$D{r}-$C{r})'.format(r=r))
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

# ---------------------------------------------------------------- Settings
st = wb.create_sheet("Settings")
write_header(st, ["Setting", "Value", "Note"])
set_widths(st, [34, 34, 70])
settings = [
    ("Dollar floor", 25000, "A movement must exceed this to clear the dollar leg."),
    ("Percent floor (points)", 10, "A movement must reach this percent of the prior balance to clear the percent leg."),
    ("Rule", "both", "both means a line owes commentary only when it clears both legs. either means one leg is enough."),
    ("Close period", "June 2026, Halyard training case", "Rides along on the reviewer log so a filed log says which close it came from."),
    ("Memo version", "Draft 2", "The version of the commentary these results cover."),
    ("Tie tolerance, dollars", 1, "A memo figure ties to the ledger when the two are within this many dollars."),
    ("Tie tolerance, percentage points", 0.05, "A memo percent ties when the two are within this many points."),
]
for i, (k, v, note) in enumerate(settings, start=2):
    st.cell(row=i, column=1, value=k).font = Font(bold=True)
    c = st.cell(row=i, column=2, value=v)
    c.fill = pale_gold_fill
    st.cell(row=i, column=3, value=note).alignment = Alignment(wrap_text=True, vertical="top")
    for col in range(1, 4):
        st.cell(row=i, column=col).border = box
st.cell(row=2, column=2).number_format = MONEY
st.cell(row=7, column=2).number_format = MONEY
dv_rule = DataValidation(type="list", formula1='"both,either"', allow_blank=False)
dv_rule.error = "The rule is either both or either."
st.add_data_validation(dv_rule)
dv_rule.add(st["B4"])
st.print_area = "A1:C8"

# ---------------------------------------------------------------- Memo
mm = wb.create_sheet("Memo")
write_header(mm, ["Line", "Sentence", "Account", "Figure in sentence", "Figure basis",
                  "Ledger figure", "Ties", "Direction stated", "Direction on ledger",
                  "Direction ties", "Owes commentary", "Result"], gold_cols=(12,))
set_widths(mm, [7, 78, 11, 16, 13, 16, 8, 14, 14, 11, 14, 11])
L_A = "Ledger!$A$2:$A$%d" % LEDGER_ROWS
for r in range(2, MEMO_ROWS + 1):
    i = r - 2
    if i < len(MEMO):
        line, sentence, acct, fig, basis, direction = MEMO[i]
        mm.cell(row=r, column=1, value=line)
        mm.cell(row=r, column=2, value=sentence)
        mm.cell(row=r, column=3, value=acct)
        if fig is not None:
            mm.cell(row=r, column=4, value=fig)
        mm.cell(row=r, column=5, value=basis)
        mm.cell(row=r, column=8, value=direction)
        mm.row_dimensions[r].height = 42
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
    mm.cell(row=r, column=12, value=(
        '=IF($C{r}="","",IF(OR($G{r}="no",$J{r}="no"),"FAIL",'
        'IF($K{r}="no","INFO","REVIEW")))'
    ).format(r=r))
    mm.cell(row=r, column=4).number_format = FIG
    mm.cell(row=r, column=6).number_format = FIG
    mm.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    for col in range(1, 13):
        cell = mm.cell(row=r, column=col)
        cell.border = box
        if col not in (2,):
            cell.alignment = Alignment(horizontal="center", vertical="top")
        if col == 12:
            cell.fill = pale_gold_fill
            cell.font = Font(bold=True)
rng = "2:%d" % MEMO_ROWS
dv_acct = DataValidation(type="list", formula1="=%s" % L_A, allow_blank=True)
mm.add_data_validation(dv_acct)
dv_acct.add("C2:C%d" % MEMO_ROWS)
dv_basis = DataValidation(type="list", formula1='"Prior,Current,Change,Percent"', allow_blank=True)
mm.add_data_validation(dv_basis)
dv_basis.add("E2:E%d" % MEMO_ROWS)
dv_dir = DataValidation(type="list", formula1='"up,down,none"', allow_blank=True)
mm.add_data_validation(dv_dir)
dv_dir.add("H2:H%d" % MEMO_ROWS)
mm.auto_filter.ref = "A1:L%d" % MEMO_ROWS
mm.print_area = "A1:L%d" % MEMO_ROWS

# ---------------------------------------------------------------- Silence
si = wb.create_sheet("Silence")
si.cell(row=1, column=1, value="Owes an explanation, none written").font = Font(bold=True, size=14, color=GREEN)
si.cell(row=2, column=1, value=("Every account that clears the rule on Settings and carries no sentence on the Memo sheet. "
                                "These go to the controller as a question, not to the preparer as a correction."))
si.cell(row=2, column=1).font = Font(size=10, color="555555")
si.cell(row=3, column=1, value="Silent lines:").font = Font(bold=True)
si.cell(row=3, column=2, value='=COUNTIF($G$6:$G${n},"Owes an explanation, none written")'.format(n=LEDGER_ROWS + 4)).font = Font(bold=True)
HDR = 5
headers = ["Account", "Name", "Change", "Percent", "Owes commentary", "Sentences on this account", "Status"]
for i, h in enumerate(headers, start=1):
    c = si.cell(row=HDR, column=i, value=h)
    c.fill = gold_head_fill if i == 7 else head_fill
    c.font = gold_head_font if i == 7 else head_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = box
si.row_dimensions[HDR].height = 32
si.freeze_panes = "A%d" % (HDR + 1)
set_widths(si, [11, 40, 15, 11, 15, 15, 38])
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
        '=IF($A{r}="","",IF($E{r}<>"yes","No commentary owed",'
        'IF($F{r}=0,"Owes an explanation, none written",'
        '"Explained, "&$F{r}&" sentence(s) on this account")))'
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

# ---------------------------------------------------------------- Reviewer log
rl = wb.create_sheet("Reviewer log")
write_header(rl, LOG_HEADERS, gold_cols=(7,))
set_widths(rl, [26, 13, 9, 26, 9, 13, 10, 60, 48, 48, 10, 14, 12, 18])
LOG_TOTAL = 34
for r in range(2, LOG_TOTAL + 1):
    i = r - 2
    if i < len(LOG_ROWS):
        for col, val in enumerate(LOG_ROWS[i], start=1):
            rl.cell(row=r, column=col, value=val)
        rl.row_dimensions[r].height = 60
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
dv_check.add("F2:F%d" % LOG_TOTAL)
dv_result = DataValidation(type="list", formula1='"pass,fail,review,info"', allow_blank=True)
dv_result.error = "Use pass, fail, review or info."
rl.add_data_validation(dv_result)
dv_result.add("G2:G%d" % LOG_TOTAL)
dv_yn = DataValidation(type="list", formula1='"yes,no"', allow_blank=True)
rl.add_data_validation(dv_yn)
dv_yn.add("K2:K%d" % LOG_TOTAL)
rl.auto_filter.ref = "A1:N%d" % LOG_TOTAL
rl.print_area = "A1:N%d" % LOG_TOTAL

for sheet in (lg, mm, si, rl):
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.print_title_rows = "1:1"
si.print_title_rows = "%d:%d" % (HDR, HDR)

wb.save(OUT)
print("wrote", OUT)
