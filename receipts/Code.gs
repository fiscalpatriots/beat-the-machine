/**
 * Second Pass receipts, a Google Apps Script web app.
 *
 * What it is for. The drill at index.html posts a player's attempt to a Google Form and the
 * form tells the page nothing back, so the page has to say "Sent. The receiver does not confirm
 * receipt to this page." This script is the receiver that does confirm. It takes the attempt
 * record as JSON, writes one row to a Google Sheet, and answers with a receipt the player can
 * read on screen and keep in their own saved record.
 *
 * DEPLOYMENT, four clicks and a paste.
 *   1. New project. Go to script.google.com, click New project, and name it "Second Pass receipts".
 *   2. Paste. Select everything in the editor, delete it, paste this whole file, and save.
 *   3. Deploy as web app. Click Deploy, New deployment, pick Web app as the type, set
 *      "Execute as" to Me and "Who has access" to Anyone, then Deploy. Google asks you to
 *      authorize the script the first time; the permission it wants is to create and write the
 *      spreadsheet it keeps the rows in.
 *   4. Copy the URL. Copy the /exec web app URL Google shows you and paste it into index.html
 *      as the value of RECEIPT_ENDPOINT. That one constant is the whole switch.
 *
 * The sheet. The first attempt that arrives creates a spreadsheet called "Second Pass receipts"
 * in your Drive, owned by you, the same as the form responses sheet. Its id is remembered in the
 * script's properties, so later attempts go to the same file. Run sheetUrl() from the editor any
 * time to print the link in the execution log.
 *
 * CORS. A web app deployed to Anyone answers a cross-origin POST from a static page. The page
 * must send a simple request, which means no custom headers and the default text/plain content
 * type; Apps Script does not answer a CORS preflight, so a JSON content-type header would break
 * it. index.html posts that way on purpose.
 *
 * Redeploying after an edit. Deploy, Manage deployments, pencil icon, Version: New version,
 * Deploy. The /exec URL stays the same, so nothing in index.html changes.
 */

var SERVICE = "second-pass-receipts";
var VERSION = "1.0.0";
var SHEET_FILE_NAME = "Second Pass receipts";
var TAB_NAME = "receipts";
var PROP_SHEET_ID = "receiptsSheetId";

/* Nineteen is the shape of the shipped case: fourteen trained lines and five fresh ones. A case
   that carries a different count is accepted when the record's own scoring block says so, which
   is how a new case file passes without this script being edited. */
var DEFAULT_RESPONSE_COUNT = 19;

/* Sheets stops at 50,000 characters in one cell. The raw record is written across up to four
   cells, in order, so a long record survives whole rather than being cut. */
var CELL_LIMIT = 45000;
var RAW_COLUMNS = 4;

var HEADERS = [
  "receivedAt", "attemptId", "receipt", "productVersion", "noticeVersion",
  "caseId", "caseVersions", "pseudonym", "organizations", "responseCount",
  "roundOneRight", "roundOneOf", "roundTwoRight", "roundTwoOf", "points", "rank",
  "testAttempt", "completedAt", "lapSeconds",
  "rawJson1", "rawJson2", "rawJson3", "rawJson4"
];

/* ---------------------------------------------------------------- the two endpoints */

/** Health check. GET the /exec URL in a browser and this is what comes back. */
function doGet(e) {
  return json({ ok: true, service: SERVICE, version: VERSION });
}

/**
 * The receipt. Takes the attempt record as a JSON body, validates it, appends one row, and
 * answers {ok:true, receipt:<sha256 of the record>, storedAt:<iso>}.
 *
 * Idempotent on the attempt id. A retry of the same attempt finds the row already there and
 * gets the first receipt back without a second row being written, which is what makes a retry
 * safe to press.
 */
function doPost(e) {
  var body;
  try {
    body = (e && e.postData && e.postData.contents) ? e.postData.contents : "";
  } catch (err) {
    return json({ ok: false, error: "no body" });
  }
  if (!body) return json({ ok: false, error: "no body" });

  var parsed;
  try {
    parsed = JSON.parse(body);
  } catch (err) {
    return json({ ok: false, error: "body is not JSON" });
  }

  /* The page posts the record itself. A wrapper of {record: ...} is accepted as well, so a
     future caller that wants to add an envelope does not need this script changed. */
  var record = (parsed && parsed.record && typeof parsed.record === "object")
    ? parsed.record : parsed;

  var problem = validate(record);
  if (problem) return json({ ok: false, error: problem });

  var attemptId = String(record.attempt.id);

  /* One writer at a time. Two tabs finishing together would otherwise both miss the existing
     row and both append one. */
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(30000);
  } catch (err) {
    return json({ ok: false, error: "busy, try again" });
  }

  try {
    var sheet = receiptSheet();
    var existing = findRow(sheet, attemptId);
    if (existing) {
      return json({
        ok: true,
        receipt: existing.receipt,
        storedAt: existing.storedAt,
        duplicate: true,
        note: "This attempt id was already stored. Same receipt, no second row."
      });
    }

    var receipt = sha256Hex(canonical(record));
    var storedAt = new Date().toISOString();
    sheet.appendRow(row(record, receipt, storedAt, body));

    return json({ ok: true, receipt: receipt, storedAt: storedAt, duplicate: false });
  } catch (err) {
    return json({ ok: false, error: "could not store: " + (err && err.message ? err.message : err) });
  } finally {
    lock.releaseLock();
  }
}

/* ---------------------------------------------------------------- validation */

/**
 * Returns a sentence naming what is wrong, or an empty string when the record is fit to store.
 * Four things are checked: an attempt id, a product version, a case id, and a response count
 * that is either nineteen or the count the record's own scoring block says the case carries.
 */
function validate(r) {
  if (!r || typeof r !== "object") return "record is not an object";
  if (!r.attempt || typeof r.attempt !== "object") return "no attempt block";
  if (!nonEmpty(r.attempt.id)) return "no attempt id";
  if (!nonEmpty(r.attempt.productVersion)) return "no product version";
  if (!nonEmpty(r.attempt.caseId)) return "no case id";
  if (!Array.isArray(r.responses)) return "no responses array";

  var expected = caseLineCount(r);
  if (r.responses.length !== DEFAULT_RESPONSE_COUNT && r.responses.length !== expected) {
    return "expected " + DEFAULT_RESPONSE_COUNT + " responses or the case's " + expected +
           ", got " + r.responses.length;
  }
  return "";
}

function nonEmpty(v) {
  return typeof v === "string" ? v.trim().length > 0 : (v !== null && v !== undefined && v !== "");
}

/** Lines the case says it carries: round one plus round two, both read off the record. */
function caseLineCount(r) {
  var s = (r && r.scoring) || {};
  var one = (s.roundOne && typeof s.roundOne.of === "number") ? s.roundOne.of : 0;
  var two = (s.roundTwo && typeof s.roundTwo.of === "number") ? s.roundTwo.of : 0;
  return one + two;
}

/* ---------------------------------------------------------------- the sheet */

/** The receipts tab, created with the spreadsheet on the first attempt that arrives. */
function receiptSheet() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty(PROP_SHEET_ID);
  var book = null;

  if (id) {
    try {
      book = SpreadsheetApp.openById(id);
    } catch (err) {
      book = null; // the file was deleted or moved to the trash, so make a new one
    }
  }
  if (!book) {
    book = SpreadsheetApp.create(SHEET_FILE_NAME);
    props.setProperty(PROP_SHEET_ID, book.getId());
  }

  var sheet = book.getSheetByName(TAB_NAME);
  if (!sheet) {
    sheet = book.getSheets()[0];
    sheet.setName(TAB_NAME);
  }
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

/** Prints the spreadsheet link in the execution log. Run it from the editor when you want it. */
function sheetUrl() {
  var sheet = receiptSheet();
  var url = sheet.getParent().getUrl();
  Logger.log(url);
  return url;
}

/** The stored row for an attempt id, or null. Column B holds the ids. */
function findRow(sheet, attemptId) {
  var last = sheet.getLastRow();
  if (last < 2) return null;
  var ids = sheet.getRange(2, 2, last - 1, 2).getValues(); // attemptId, receipt
  for (var i = ids.length - 1; i >= 0; i--) {
    if (String(ids[i][0]) === attemptId) {
      var stored = sheet.getRange(i + 2, 1).getValue();
      return {
        receipt: String(ids[i][1]),
        storedAt: (stored instanceof Date) ? stored.toISOString() : String(stored)
      };
    }
  }
  return null;
}

/** One row: the key fields in their own columns, then the raw record across up to four cells. */
function row(r, receipt, storedAt, raw) {
  var a = r.attempt || {};
  var s = r.scoring || {};
  var one = s.roundOne || {};
  var two = s.roundTwo || {};
  var t = r.timing || {};
  var versions = a.caseVersions || {};

  var out = [
    storedAt,
    String(a.id),
    receipt,
    String(a.productVersion),
    a.noticeVersion || "",
    String(a.caseId),
    [versions.roundOne || "", versions.roundTwo || ""].join(" / "),
    a.pseudonym || "",
    Array.isArray(a.organizations) ? a.organizations.join(", ") : "",
    r.responses.length,
    numberOr(one.right, ""),
    numberOr(one.of, ""),
    numberOr(two.right, ""),
    numberOr(two.of, ""),
    numberOr(one.points, ""),
    one.rank || "",
    a.testAttempt ? "yes" : "no",
    a.completed || "",
    numberOr(t.roundOneLapSeconds, "")
  ];

  var text = String(raw);
  for (var i = 0; i < RAW_COLUMNS; i++) {
    out.push(text.slice(i * CELL_LIMIT, (i + 1) * CELL_LIMIT));
  }
  /* A record longer than four cells would be cut silently, so say so in the last cell instead. */
  if (text.length > CELL_LIMIT * RAW_COLUMNS) {
    out[out.length - 1] = out[out.length - 1].slice(0, CELL_LIMIT - 200) +
      "\n[cut: the record was " + text.length + " characters, more than the " +
      (CELL_LIMIT * RAW_COLUMNS) + " these four cells hold]";
  }
  return out;
}

function numberOr(v, fallback) {
  return (typeof v === "number") ? v : fallback;
}

/* ---------------------------------------------------------------- the receipt */

/**
 * A stable serialization: object keys in sorted order at every level, so the same record
 * always hashes to the same receipt no matter what order the fields arrived in.
 */
function canonical(v) {
  if (v === null || typeof v !== "object") return JSON.stringify(v === undefined ? null : v);
  if (Array.isArray(v)) {
    var items = v.map(function (x) { return canonical(x); });
    return "[" + items.join(",") + "]";
  }
  var keys = Object.keys(v).sort();
  var parts = keys.map(function (k) {
    return JSON.stringify(k) + ":" + canonical(v[k]);
  });
  return "{" + parts.join(",") + "}";
}

function sha256Hex(text) {
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, text, Utilities.Charset.UTF_8);
  var hex = "";
  for (var i = 0; i < bytes.length; i++) {
    hex += ("0" + (bytes[i] & 0xFF).toString(16)).slice(-2);
  }
  return hex;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

/* ---------------------------------------------------------------- a check you can run */

/**
 * Run this from the editor after pasting. It posts a made-up attempt twice and logs both
 * answers: the first stores a row, the second returns the same receipt and stores nothing.
 * Delete the two rows it writes, or leave them; the codename says what they are.
 */
function selfTest() {
  var record = {
    record: "Second Pass attempt record",
    recordFormat: "btm-attempt-1",
    attempt: {
      id: "att-selftest-" + Date.now().toString(36),
      pseudonym: "selftest-delete",
      organizations: [],
      productVersion: "second-pass-drill 1.6.1",
      noticeVersion: "notice-2026-09-13",
      caseId: "halyard",
      caseVersions: { roundOne: "halyard-v4", roundTwo: "brightwater-v5" },
      testAttempt: true,
      completed: new Date().toISOString()
    },
    responses: [],
    scoring: { roundOne: { right: 0, of: 14, points: 0, rank: "Trainee" }, roundTwo: { right: 0, of: 5 } },
    timing: { roundOneLapSeconds: 0 }
  };
  for (var i = 0; i < 19; i++) record.responses.push({ item: "selftest-" + i });

  var body = JSON.stringify(record);
  var first = doPost({ postData: { contents: body } });
  var again = doPost({ postData: { contents: body } });
  Logger.log("first:  " + first.getContent());
  Logger.log("repeat: " + again.getContent());
  Logger.log("sheet:  " + sheetUrl());
}
