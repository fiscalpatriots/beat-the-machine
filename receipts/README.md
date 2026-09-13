# The receipt path

## What this is

When a player presses **Send my results**, the drill posts to a Google Form. A form post tells
the page nothing back, so the page has only ever been able to say "Sent. The receiver does not
confirm receipt to this page." That sentence is honest and it is also the last thing in the
product a person cannot check for themselves.

This folder closes that. `Code.gs` is a Google Apps Script web app that takes the attempt record,
writes one row to a Google Sheet, and answers with a receipt: the sha256 of the record it stored
and the time it wrote the row. The page prints the first twelve characters on screen and writes
the whole receipt into the file the player saves, so the player's copy and the sheet's copy carry
the same string and can be matched line for line.

Nothing here replaces the form. The record goes to the receipt endpoint first and to the form
straight after, every time, so the form responses sheet keeps filling exactly as it does today.

| File | What it is |
| --- | --- |
| `Code.gs` | the web app: `doPost` stores and answers, `doGet` is a health check |
| `mock-endpoint.cjs` | a stand-in for it on this machine, for testing the page without Google |
| `receipts-to-form-csv.py` | turns a receipts sheet export into the shape `tools/findings.py` reads |

## The four clicks

1. **New project.** Open [script.google.com](https://script.google.com), click **New project**,
   name it "Second Pass receipts".
2. **Paste.** Select everything in the editor, delete it, paste the whole of `receipts/Code.gs`,
   and save.
3. **Deploy as web app.** Click **Deploy**, **New deployment**, choose **Web app**, set
   **Execute as** to *Me* and **Who has access** to *Anyone*, then **Deploy**. Google asks for
   authorization the first time. The permission it wants is to create and write the spreadsheet
   it keeps the rows in, which lands in your Drive and is owned by you.
4. **Copy the URL.** Copy the `/exec` address Google shows and paste it into `index.html`, into
   this one line near the top of the script:

   ```js
   var RECEIPT_ENDPOINT = "";
   ```

   It becomes `var RECEIPT_ENDPOINT = "https://script.google.com/macros/s/…/exec";`. That is the
   whole switch. Commit, push, and the next player who finishes gets a receipt.

Two things worth doing once: paste the `/exec` URL into a browser tab to see
`{"ok":true,"service":"second-pass-receipts","version":"1.0.0"}`, which proves the deployment is
live, and run `selfTest()` from the Apps Script editor, which stores a made-up attempt twice and
logs the sheet's link so you can see the row and the repeat that wrote no second row.

To undo it, empty the constant again. The page goes straight back to the wording it has today and
nothing else changes.

## The privacy line

The data notice has to describe what the page actually does, so a fourth bullet appears in it the
moment the constant is filled in, and only then:

> If you send your results, the same record is also stored in the Second Pass receipts sheet,
> owned by Khaled Alkurd, the same as the form responses sheet. That sheet answers this page with
> a receipt, so you can see your results were stored and keep the receipt in your own file.

It is in `index.html` as `NOTICE_RECEIPT_LINE`, printed from `noticeItems()`. The same sentence
belongs in the notice section of the repository `README.md` when the endpoint goes live, so the
two readings of the notice stay the same. The point it has to carry is the one the rest of the
notice already carries: this is a second sheet in the same person's Drive, not a third party.

## What the sheet holds

The spreadsheet is created on the first attempt that arrives, called **Second Pass receipts**, and
its id is remembered in the script's properties so every later attempt lands in the same file. One
row per attempt:

`receivedAt`, `attemptId`, `receipt`, `productVersion`, `noticeVersion`, `caseId`, `caseVersions`,
`pseudonym`, `organizations`, `responseCount`, `roundOneRight`, `roundOneOf`, `roundTwoRight`,
`roundTwoOf`, `points`, `rank`, `testAttempt`, `completedAt`, `lapSeconds`, then `rawJson1` to
`rawJson4`.

The record runs to about 55,000 characters and a sheet cell stops at 50,000, so the raw JSON is
written across four cells in order and put back together by joining them. A record too long even
for those four says so in the last cell rather than being cut in silence.

**Validation.** A post is stored only if it carries an attempt id, a product version, a case id,
and either nineteen responses or the count the record's own scoring block says the case carries.
Anything else comes back as `{"ok":false,"error":"…"}` and no row is written.

**Idempotent on the attempt id.** A retry finds the row already there, gets the first receipt
back, and writes nothing. Two rows can never be one attempt counted twice, which is what makes
**Send again** safe to press.

## What the player sees

| Case | On screen |
| --- | --- |
| The endpoint stores it | "Receipt 4db5710dfcaa. Stored at 8:53:45 AM." and the receipt in the saved record |
| The endpoint fails or times out | the wording it has today: "Sent. The receiver does not confirm receipt to this page." plus a line saying the receipt endpoint did not confirm it |
| The player presses Send again | the same receipt, because the attempt id is the same |

The form post runs in all three cases. A player whose receipt fails is exactly where they were
before any of this existed and never worse off. Test mode posts nothing anywhere.

## Testing it without Google

```
node receipts/mock-endpoint.cjs                      # on 8899, the repository is served from it too
node receipts/mock-endpoint.cjs --port 8900 --fail   # every receipt POST answers a 500
```

Then open the drill from the mock with test mode on, pointing both posts at the machine:

```
http://localhost:8899/index.html?test=1
  &receipt=http%3A%2F%2Flocalhost%3A8899%2Freceipt
  &form=http%3A%2F%2Flocalhost%3A8899%2FformResponse
```

The `receipt` and `form` parameters are read only while test mode is on and only when they point
at `localhost` or `127.0.0.1`. Anything else is ignored, so a link handed to a player cannot send
their attempt somewhere it does not belong. `--save <dir>` writes each accepted record to a file,
which is how a receipts CSV can be built for the converter below.

The three runs proved on 13 September 2026 are in `screenshots/release/`:
`drill-375-21-receipt-stored.png` and `drill-375-23-receipt-failed-form-fallback.png`, with the
repeat case standing in the mock's log, where it prints `repeat of att-…, same receipt …, no
second row` against a store that stayed at one row.

## Reading the sheet instead of the form

`tools/findings.py` matches columns by the form's question titles. The receipts export does not
carry those titles, it carries something better, so the converter puts the record back into the
shape findings.py reads:

```
python receipts/receipts-to-form-csv.py receipts-export.csv --out responses-from-receipts.csv
python tools/findings.py responses-from-receipts.csv
```

Download the receipts sheet as CSV the same way you download the form's: **File**, **Download**,
**Comma-separated values**. The converter reads the entry ids out of `index.html` at run time, so a
renumbered question needs no edit here, and it reports every row whose raw JSON will not parse
rather than guessing at it. Test attempts are dropped unless `--keep-test` is passed. Checked on
13 September 2026 against a stored record: every question title matched a column.

Three things the receipts export gives that the form export does not: the attempt id in its own
column, so repeats are one query rather than a read of question B; the whole record, including the
fields the form never carried; and the receipt itself, so a player asking "did you get mine" is
answered by searching one column.
