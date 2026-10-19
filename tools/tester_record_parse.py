#!/usr/bin/env python3
"""Read the tester feedback form export and turn question 9 into one row per tester per line.

Standard library only.

    python tools/tester_record_parse.py responses.xlsx
    python tools/tester_record_parse.py responses.csv --out tester_lines.csv
    python tools/tester_record_parse.py responses.xlsx --all-runs
    python tools/tester_record_parse.py responses.xlsx --q4 "Anything else"

The input is the Microsoft Forms export of "Second Pass: tester feedback", either the Excel file
Forms downloads (Responses, Open in Excel) or that sheet saved as CSV. From release 1.9.2 the drill's
tester link opens that form with question 9, "Your drill answers (the drill fills this in for you,
so please leave it as it is)", already holding the tester's locked lines. This script

  1. finds the question 9 column by its title, which starts "Your drill answers",
  2. drops every row with an answer that starts "TEST RESPONSE" in any question but question 9
     (--q4 checks only the question whose title starts with the text given),
  3. parses each record and checks it against the case file it names: the outcome has to follow
     from the call and the key, the account and the key have to be the case file's for that line,
     the basis has to agree or differ as the chips say, line numbers cannot repeat or run out of
     range, and the counts in the header have to match the lines. A record that fails any of these
     was edited by the tester and is left out,
  4. keeps the latest response for any attempt id submitted twice, and
  5. writes tester_lines.csv (one row per tester per line) and prints the summary for the
     scholarship write-up, from first runs only unless --all-runs is given: lines 1 to 5 first,
     then the lines testers who kept going added, the right reason on caught problem lines, median
     active seconds, the commonest reason chips on missed lines and on false flags, and the
     reattempts on their own lines.

A run is the count the drill keeps in the tab: run 1 is the first, and every Play again adds one.
A later run is played after the tester has seen the key, so it is not an independent read.

The record grammar is the one testerRecord() in index.html writes, documented there:

    record  = header { "||" line } [ "||words cut to " N ] [ "||words left off after line " M ]
              [ "||truncated after line " N ]
    header  = stamp "|" codename "|" attemptId "|case " pick "|answered " count
              "|right " count "|points " count "|run " count "|case file " caseVersion
    line    = "L" n "|" account "|" call "|" chips "|key " call "|" outcome
              "|basis " ( "agrees" | "differs" ) "|" seconds "s" [ "|" words ]

Spaces around the delimiters are forgiven, and a header of seven fields (no run, no case file) is
read as run 1 on the case's current file, so records written before the review still parse.

tools/tests/test_tester_record_parse.py runs this against tests/tester-record-sample.csv, against an
Excel file it builds on the fly, and against records the drill itself writes.
"""
import argparse
import collections
import csv
import functools
import io
import json
import os
import re
import statistics
import sys
import zipfile
import xml.etree.ElementTree as ET

Q9_PREFIX = "your drill answers"
TEST_PREFIX = "TEST RESPONSE"
TESTER_LINES = 5
CASES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cases")
# the case file a record means when its header predates the "case file" field
DEFAULT_CASE_FILE = {"halyard": "halyard-v4"}

CHIPS = {
    "holds": "the figure and reason hold",
    "tie": "figure does not tie",
    "direction": "direction wrong",
    "source": "no source on file",
    "period": "wrong period",
    "account": "wrong account",
    "owed": "nothing written where owed",
}
CALLS = ("stand", "flag")
OUTCOMES = ("caught", "missed", "cleared", "false flag")

# The columns Microsoft Forms puts before the questions. Anything else is a question.
META_COLUMNS = {"id", "start time", "completion time", "email", "name", "last modified time",
                "total points", "quiz feedback", "grade posted to learners", "posted time"}
META_PREFIXES = ("points - ", "feedback - ")

LINE_SPLIT = re.compile(r"\s*\|\|\s*")
FIELD_SPLIT = re.compile(r"\s*\|\s*")
TRUNC_RE = re.compile(r"^truncated after line (\d+)\b", re.I)
CUT_RE = re.compile(r"^words cut to (\d+)\b", re.I)
OFF_RE = re.compile(r"^words left off after line (\d+)\b", re.I)
STAMP_RE = re.compile(r"^second-pass-drill\s+(\S+)$", re.I)
SECS_RE = re.compile(r"^(\d+)s\b\s*(.*)$")

OUT_FIELDS = ["response_id", "attempt_id", "codename", "version", "case", "case_file", "run",
              "line", "account", "call", "key", "outcome", "right", "basis_agrees", "seconds",
              "chips", "chips_short", "words", "answered", "lines_in_record", "words_cut_to",
              "words_left_off_after_line", "truncated_after_line"]


class RecordError(ValueError):
    pass


class EditedError(RecordError):
    """A record that parses but cannot be what the drill wrote."""

    def __init__(self, reasons, record=None):
        self.reasons = list(reasons)
        self.record = record
        RecordError.__init__(self, "edited: " + "; ".join(self.reasons))


# ---------- reading the export ----------

_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
_PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"


def _col_index(ref):
    letters = re.match(r"[A-Z]+", ref or "")
    if not letters:
        return None
    n = 0
    for ch in letters.group(0):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _text_of(node):
    """Every <t> under a shared string or inline string, rich text runs included."""
    return "".join(t.text or "" for t in node.iter("{%s}t" % _NS["m"]))


def read_xlsx(path):
    """The first worksheet as a list of rows of strings."""
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            shared = [_text_of(si) for si in root.findall("m:si", _NS)]
        sheet = "xl/worksheets/sheet1.xml"
        if "xl/workbook.xml" in names and "xl/_rels/workbook.xml.rels" in names:
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            first = wb.find("m:sheets/m:sheet", _NS)
            rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
            if first is not None:
                rid = first.get(_REL)
                for rel in rels.findall(_PKG + "Relationship"):
                    if rel.get("Id") == rid:
                        target = rel.get("Target").lstrip("/")
                        sheet = target if target.startswith("xl/") else "xl/" + target
        root = ET.fromstring(z.read(sheet))
    rows = []
    for row in root.iter("{%s}row" % _NS["m"]):
        cells = {}
        for k, c in enumerate(row.findall("m:c", _NS)):
            idx = _col_index(c.get("r"))
            if idx is None:
                idx = k
            kind = c.get("t")
            v = c.find("m:v", _NS)
            if kind == "s" and v is not None:
                val = shared[int(v.text)]
            elif kind == "inlineStr":
                is_ = c.find("m:is", _NS)
                val = _text_of(is_) if is_ is not None else ""
            else:
                val = v.text if v is not None and v.text is not None else ""
            cells[idx] = val
        if cells:
            width = max(cells) + 1
            rows.append([cells.get(i, "") for i in range(width)])
        else:
            rows.append([])
    return rows


def read_csv(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    return [row for row in csv.reader(io.StringIO(text, newline=""))]


def read_export(path):
    if path.lower().endswith((".xlsx", ".xlsm")):
        return read_xlsx(path)
    return read_csv(path)


def question_columns(header):
    out = []
    for i, title in enumerate(header):
        t = (title or "").strip().lower()
        if not t or t in META_COLUMNS or t.startswith(META_PREFIXES):
            continue
        out.append(i)
    return out


def find_columns(header, q4_prefix=None):
    """Question 9, the columns checked for TEST RESPONSE, the response id, the columns that could
    name a respondent, and a note when question 9 is not where the form puts it."""
    q9 = [i for i, t in enumerate(header) if (t or "").strip().lower().startswith(Q9_PREFIX)]
    if not q9:
        raise SystemExit('No column title starts "Your drill answers". Is this the tester feedback '
                         "form export, with question 9 in it?")
    questions = question_columns(header)
    if q4_prefix:
        hits = [i for i, t in enumerate(header) if (t or "").strip().lower().startswith(q4_prefix.strip().lower())]
        if not hits:
            raise SystemExit('No column title starts "%s".' % q4_prefix)
        test_cols = [hits[0]]
    else:
        test_cols = [i for i in questions if i != q9[0]]
    rid = next((i for i, t in enumerate(header) if (t or "").strip().lower() == "id"), None)
    who = [i for i, t in enumerate(header) if (t or "").strip().lower() in ("email", "name")]
    layout = None
    if len(questions) < 9 or questions[8] != q9[0]:
        layout = ("Question 9 is not the ninth question column, so the form's questions have moved or "
                  "one of them exports as several columns. TEST RESPONSE rows are found in any "
                  "question, so nothing is lost; pass --q4 to check one question only.")
    return {"q9": q9[0], "test": test_cols, "rid": rid, "who": who, "layout": layout}


# ---------- the case files ----------

@functools.lru_cache(maxsize=None)
def case_cards(case_file, cases_dir=CASES_DIR):
    """The cards of cases/<case_file>.json, or None when that file is not here."""
    if not case_file or not cases_dir or not re.match(r"^[a-z0-9_-]+$", case_file, re.I):
        return None
    path = os.path.join(cases_dir, case_file + ".json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return tuple({"acct": str(c.get("acct", "")), "key": c.get("key"),
                  "basis": tuple(c.get("basisKey") or (["the figure and reason hold"] if c.get("key") == "stand" else []))}
                 for c in data.get("cards", []))


def outcome_of(call, key):
    if call == key:
        return "caught" if key == "flag" else "cleared"
    return "missed" if key == "flag" else "false flag"


# ---------- parsing one record ----------

def parse_record(text, cases_dir=CASES_DIR, check=True):
    """One question 9 answer as {header..., lines: [...], markers}. With check, a record that cannot
    be what the drill wrote raises EditedError; without it the reasons are in rec["edits"]."""
    text = re.sub(r"[\r\n\t]+", " ", text or "").strip()
    if not text:
        raise RecordError("empty")
    parts = LINE_SPLIT.split(text)
    head = FIELD_SPLIT.split(parts[0])
    if len(head) not in (7, 8, 9):
        raise RecordError("the header has %d fields, not 7 to 9" % len(head))
    stamp = STAMP_RE.match(head[0])
    if not stamp:
        raise RecordError("the header does not start with second-pass-drill and a version")

    def labelled(field, label, number=True):
        m = re.match(r"^%s\s+(.*)$" % label, field, re.I)
        if not m:
            raise RecordError('expected "%s ..." in the header, found "%s"' % (label, field))
        v = m.group(1).strip()
        if number:
            if not re.match(r"^-?\d+$", v):
                raise RecordError('"%s" is not a whole number' % field)
            return int(v)
        return v

    case = labelled(head[3], "case", number=False)
    rec = {
        "version": stamp.group(1),
        "codename": head[1],
        "attempt_id": head[2],
        "case": case,
        "answered": labelled(head[4], "answered"),
        "right": labelled(head[5], "right"),
        "points": labelled(head[6], "points"),
        "run": labelled(head[7], "run") if len(head) >= 8 else 1,
        "case_file": labelled(head[8], "case file", number=False) if len(head) >= 9 else DEFAULT_CASE_FILE.get(case),
        "lines": [],
        "truncated_after_line": None,
        "words_cut_to": None,
        "words_left_off_after_line": None,
        "bad_lines": 0,
        "keys_checked": False,
        "edits": [],
    }
    for seg in parts[1:]:
        s = seg.strip()
        for regex, field in ((TRUNC_RE, "truncated_after_line"), (CUT_RE, "words_cut_to"),
                             (OFF_RE, "words_left_off_after_line")):
            m = regex.match(s)
            if m:
                rec[field] = int(m.group(1))
                break
        else:
            try:
                rec["lines"].append(parse_line(s))
            except RecordError:
                rec["bad_lines"] += 1
    rec["edits"] = edits_of(rec, cases_dir)
    if check and rec["edits"]:
        raise EditedError(rec["edits"], rec)
    return rec


def parse_line(seg):
    f = FIELD_SPLIT.split(seg.strip())
    if len(f) < 8:
        raise RecordError("a line has %d fields, fewer than 8" % len(f))
    m = re.match(r"^L(\d+)$", f[0])
    if not m:
        raise RecordError('a line does not start with "L" and its number')
    call = f[2].lower()
    key = re.match(r"^key\s+(stand|flag)$", f[4], re.I)
    written = f[5].lower()
    basis = re.match(r"^basis\s+(agrees|differs)$", f[6], re.I)
    secs = SECS_RE.match(f[7])
    if call not in CALLS or not key or written not in OUTCOMES or not basis or not secs:
        raise RecordError("a line has a field outside the grammar")
    short = [c for c in f[3].split("+") if c and c != "none"]
    k = key.group(1).lower()
    outcome = outcome_of(call, k)
    # a note typed after the seconds, or on a new line after the last one, becomes words
    words = " ".join(w for w in [secs.group(2).strip()] + [x.strip() for x in f[8:]] if w)
    return {
        "line": int(m.group(1)),
        "account": f[1],
        "call": call,
        "chips_short": short,
        "chips": [CHIPS.get(c, c) for c in short],
        "key": k,
        "outcome": outcome,
        "outcome_written": written,
        "right": outcome in ("caught", "cleared"),
        "basis_agrees": basis.group(1).lower() == "agrees",
        "seconds": int(secs.group(1)),
        "words": words,
    }


def edits_of(rec, cases_dir):
    """Every way the record differs from what the drill would have written."""
    why = []
    if rec["bad_lines"]:
        why.append("%d line %s outside the grammar" % (rec["bad_lines"], "segment" if rec["bad_lines"] == 1 else "segments"))
    cards = case_cards(rec["case_file"], cases_dir) if cases_dir else None
    rec["keys_checked"] = cards is not None
    seen = set()
    last = 0
    for ln in rec["lines"]:
        n = ln["line"]
        if ln["outcome_written"] != ln["outcome"]:
            why.append("line %d says %s, but %s on a %s line is %s" % (n, ln["outcome_written"], ln["call"], ln["key"], ln["outcome"]))
        if n in seen:
            why.append("line %d appears twice" % n)
        elif n <= last:
            why.append("line %d is out of order" % n)
        seen.add(n)
        last = max(last, n)
        if cards is not None:
            if n < 1 or n > len(cards):
                why.append("line %d is not on %s, which has %d lines" % (n, rec["case_file"], len(cards)))
                continue
            card = cards[n - 1]
            if ln["account"] != card["acct"]:
                why.append("line %d names account %s, and %s has %s there" % (n, ln["account"], rec["case_file"], card["acct"]))
            if ln["key"] != card["key"]:
                why.append("line %d says key %s, and %s keys it %s" % (n, ln["key"], rec["case_file"], card["key"]))
            agrees = bool(ln["chips"]) and all(c in card["basis"] for c in ln["chips"])
            if agrees != ln["basis_agrees"]:
                why.append("line %d says the basis %s, and its chips %s" % (
                    n, "agrees" if ln["basis_agrees"] else "differs", "agree" if agrees else "differ"))
    right_in = sum(1 for ln in rec["lines"] if ln["right"])
    t = rec["truncated_after_line"]
    if t is None:
        if len(rec["lines"]) != rec["answered"]:
            why.append("the header says %d answered and the record holds %d lines" % (rec["answered"], len(rec["lines"])))
        if right_in != rec["right"]:
            why.append("the header says %d right and the lines hold %d" % (rec["right"], right_in))
    else:
        if len(rec["lines"]) >= rec["answered"]:
            why.append("the record says it was cut but holds every answered line")
        if (rec["lines"][-1]["line"] if rec["lines"] else 0) != t:
            why.append("the record says it was cut after line %d and its last line is another" % t)
        if right_in > rec["right"]:
            why.append("the lines hold more right calls than the header counts")
    return why


# ---------- the export as a whole ----------

def load(path, q4_prefix=None, cases_dir=CASES_DIR):
    rows = read_export(path)
    if not rows:
        raise SystemExit("The file has no rows.")
    header = rows[0]
    cols = find_columns(header, q4_prefix)
    stats = collections.Counter()
    kept = collections.OrderedDict()
    problems = []
    edited = []
    for n, row in enumerate(rows[1:], start=2):
        if not any((c or "").strip() for c in row):
            continue
        stats["responses"] += 1
        cell = lambda i: (row[i] if i is not None and i < len(row) else "") or ""
        if any(cell(i).strip() and cell(i).strip().lower() != "anonymous" for i in cols["who"]):
            stats["rows that carry a name or email"] += 1
        if any(cell(i).strip().upper().startswith(TEST_PREFIX) for i in cols["test"]):
            stats["test rows dropped"] += 1
            continue
        text = cell(cols["q9"]).strip()
        if not text:
            stats["no drill answers"] += 1
            continue
        try:
            rec = parse_record(text, cases_dir=cases_dir)
        except EditedError as e:
            stats["records edited by the tester"] += 1
            edited.append("sheet row %d: %s" % (n, "; ".join(e.reasons)))
            continue
        except RecordError as e:
            stats["records that did not parse"] += 1
            problems.append("sheet row %d: %s" % (n, e))
            continue
        rec["response_id"] = cell(cols["rid"]).strip() or "row %d" % n
        if not rec["keys_checked"]:
            stats["records whose case file is not here, keys not checked"] += 1
        if rec["attempt_id"] in kept:
            stats["repeat submissions of one attempt, latest kept"] += 1
            del kept[rec["attempt_id"]]
        kept[rec["attempt_id"]] = rec
    return list(kept.values()), stats, {"parse": problems, "edited": edited, "layout": cols["layout"]}


def write_lines(records, out_path):
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_FIELDS)
        w.writeheader()
        blank = lambda v: "" if v is None else v
        for r in records:
            for ln in r["lines"]:
                w.writerow({
                    "response_id": r["response_id"], "attempt_id": r["attempt_id"],
                    "codename": r["codename"], "version": r["version"], "case": r["case"],
                    "case_file": blank(r["case_file"]), "run": r["run"],
                    "line": ln["line"], "account": ln["account"], "call": ln["call"],
                    "key": ln["key"], "outcome": ln["outcome"], "right": int(ln["right"]),
                    "basis_agrees": int(ln["basis_agrees"]), "seconds": ln["seconds"],
                    "chips": "; ".join(ln["chips"]), "chips_short": "+".join(ln["chips_short"]),
                    "words": ln["words"], "answered": r["answered"],
                    "lines_in_record": len(r["lines"]),
                    "words_cut_to": blank(r["words_cut_to"]),
                    "words_left_off_after_line": blank(r["words_left_off_after_line"]),
                    "truncated_after_line": blank(r["truncated_after_line"]),
                })


# ---------- the summary ----------

def rate(num, den):
    if not den:
        return "none on record"
    return "%d of %d (%d%%)" % (num, den, round(100.0 * num / den))


def tally(lines):
    flagged = [ln for ln in lines if ln["key"] == "flag"]
    caught = [ln for ln in flagged if ln["outcome"] == "caught"]
    return {
        "lines": len(lines),
        "flag_lines": len(flagged),
        "caught": len(caught),
        "clean_lines": sum(1 for ln in lines if ln["key"] == "stand"),
        "false_flags": sum(1 for ln in lines if ln["outcome"] == "false flag"),
        "right": sum(1 for ln in lines if ln["right"]),
        "caught_right_reason": sum(1 for ln in caught if ln["basis_agrees"]),
    }


def summarize(records, all_runs=False):
    first = [r for r in records if r["run"] == 1]
    later = [r for r in records if r["run"] != 1]
    used = records if all_runs else first
    lines = [ln for r in used for ln in r["lines"]]
    early = [ln for ln in lines if ln["line"] <= TESTER_LINES]
    late = [ln for ln in lines if ln["line"] > TESTER_LINES]
    by_line = collections.OrderedDict()
    for ln in sorted(lines, key=lambda x: x["line"]):
        by_line.setdefault(ln["line"], []).append(ln)
    missed = [ln for ln in lines if ln["outcome"] == "missed"]
    false_flags = [ln for ln in lines if ln["outcome"] == "false flag"]
    timed = [ln["seconds"] for ln in lines if ln["line"] != 1]
    return {
        "attempts": len(records),
        "first_runs": len(first),
        "reattempts": len(later),
        "used": len(used),
        "all_runs": all_runs,
        "versions": collections.Counter(r["version"] for r in used).most_common(),
        "case_files": collections.Counter(r["case_file"] or "unknown" for r in used).most_common(),
        "lines": len(lines),
        "answered_total": sum(r["answered"] for r in used),
        "truncated": sum(1 for r in used if r["truncated_after_line"] is not None),
        "words_cut": sum(1 for r in used if r["words_cut_to"] is not None or r["words_left_off_after_line"] is not None),
        "early": tally(early),
        "early_attempts": sum(1 for r in used if any(ln["line"] <= TESTER_LINES for ln in r["lines"])),
        "late": tally(late),
        "late_attempts": sum(1 for r in used if any(ln["line"] > TESTER_LINES for ln in r["lines"])),
        "every": tally(lines),
        "median_seconds": statistics.median(timed) if timed else None,
        "by_line": by_line,
        "chips_on_missed": collections.Counter(c for ln in missed for c in ln["chips"]).most_common(),
        "chips_on_false_flags": collections.Counter(c for ln in false_flags for c in ln["chips"]).most_common(),
        "missed": len(missed),
        "false_flags": len(false_flags),
        "later": later,
    }


def _block(p, t):
    p.append("  Caught, lines with a problem: %s." % rate(t["caught"], t["flag_lines"]))
    p.append("  False flags, clean lines: %s." % rate(t["false_flags"], t["clean_lines"]))
    p.append("  Right calls: %s." % rate(t["right"], t["lines"]))
    p.append("  Right reason on a caught problem line: %s." % rate(t["caught_right_reason"], t["caught"]))


def _plural(n, one, many=None):
    return one if n == 1 else (many or one + "s")


def report(path, records, stats, notes, out_path, all_runs=False):
    s = summarize(records, all_runs)
    p = []
    p.append("Second Pass tester answers, from %s" % os.path.basename(path))
    p.append("")
    p.append("Rows read: %d. Test rows dropped: %d. Rows with no drill answers: %d."
             % (stats["responses"], stats["test rows dropped"], stats["no drill answers"]))
    if stats["records that did not parse"]:
        p.append("Records that did not parse: %d (%s)." % (stats["records that did not parse"], "; ".join(notes["parse"])))
    if stats["records edited by the tester"]:
        p.append("Records edited by the tester, left out: %d (%s)." % (stats["records edited by the tester"], "; ".join(notes["edited"])))
    if stats["repeat submissions of one attempt, latest kept"]:
        p.append("Repeat submissions of one attempt: %d, the latest of each kept."
                 % stats["repeat submissions of one attempt, latest kept"])
    if stats["records whose case file is not here, keys not checked"]:
        p.append("Records whose case file is not in cases/, so their accounts and keys were not checked: %d."
                 % stats["records whose case file is not here, keys not checked"])
    if stats["rows that carry a name or email"]:
        p.append("Rows that carry a respondent's name or email: %d. The form should be set to Anyone can "
                 "respond. tester_lines.csv leaves those columns out." % stats["rows that carry a name or email"])
    if notes.get("layout"):
        p.append(notes["layout"])
    p.append("")
    p.append("Attempts with drill answers: %d (first runs %d, reattempts %d)." % (s["attempts"], s["first_runs"], s["reattempts"]))
    if s["reattempts"]:
        if all_runs:
            p.append("Later runs included in the rates: %d, because --all-runs was given." % s["reattempts"])
        else:
            p.append("Later runs excluded: %d. A later run is played after the key was shown. Pass --all-runs to count them."
                     % s["reattempts"])
    p.append("Codenames are random and can repeat, so they do not count people.")
    p.append("Drill versions: %s. Case files: %s." % (
        ", ".join("%s (%d)" % v for v in s["versions"]) or "none",
        ", ".join("%s (%d)" % v for v in s["case_files"]) or "none"))
    if len(s["versions"]) > 1 or len(s["case_files"]) > 1:
        p.append("Warning: more than one drill version or case file is pooled in these rates.")
    p.append("Lines answered: %d in the records%s." % (
        s["lines"], "" if s["answered_total"] == s["lines"] else
        ", of %d locked (%d %s cut to fit the form link)" % (
            s["answered_total"], s["truncated"], "record was" if s["truncated"] == 1 else "records were")))
    if s["words_cut"]:
        p.append("Records whose words were shortened to fit the link: %d." % s["words_cut"])
    if not s["lines"]:
        p.append("")
        p.append("No lines to summarize.")
        return "\n".join(p)
    kind = "attempt" if all_runs else "first-run attempt"
    p.append("")
    p.append("Lines 1 to %d, from %d %s:" % (TESTER_LINES, s["early_attempts"], _plural(s["early_attempts"], kind)))
    _block(p, s["early"])
    if s["late_attempts"]:
        p.append("Lines %d and up, from the %d %s that kept going:" % (
            TESTER_LINES + 1, s["late_attempts"], _plural(s["late_attempts"], kind)))
        _block(p, s["late"])
    p.append("Median active seconds a line: %s, leaving out line 1, whose time includes the tour." % _num(s["median_seconds"]))
    p.append("")
    p.append("By line")
    p.append("%-5s %-8s %-6s %-9s %-28s %-15s %s" % ("Line", "Account", "Key", "Attempts", "Caught or cleared",
                                                    "Reason agrees", "Median seconds"))
    for n, lns in s["by_line"].items():
        key = lns[0]["key"]
        right = sum(1 for ln in lns if ln["right"])
        label = ("caught " if key == "flag" else "cleared ") + rate(right, len(lns))
        agrees = sum(1 for ln in lns if ln["basis_agrees"])
        p.append("%-5s %-8s %-6s %-9d %-28s %-15s %s" % (
            "L%d" % n, lns[0]["account"], key, len(lns), label,
            "%d of %d" % (agrees, len(lns)),
            _num(statistics.median([ln["seconds"] for ln in lns])) + (", includes the tour" if n == 1 else "")))
    p.append("")
    p.append("Reason chips on missed lines (a problem let stand), %d %s:" % (s["missed"], _plural(s["missed"], "line")))
    p.extend(["  %s: %d" % (c, k) for c, k in s["chips_on_missed"]] or ["  none on record"])
    p.append("Reason chips on false flags (a clean line flagged), %d %s:" % (s["false_flags"], _plural(s["false_flags"], "line")))
    p.extend(["  %s: %d" % (c, k) for c, k in s["chips_on_false_flags"]] or ["  none on record"])
    if s["later"]:
        p.append("")
        p.append("Reattempts%s:" % ("" if all_runs else ", left out of the rates above"))
        for r in s["later"]:
            t = tally(r["lines"])
            p.append("  %s, run %d, %s: %d %s, caught %d of %d, false flags %d of %d." % (
                r["codename"], r["run"], r["attempt_id"], t["lines"], _plural(t["lines"], "line"),
                t["caught"], t["flag_lines"], t["false_flags"], t["clean_lines"]))
    p.append("")
    p.append("One row per tester per line, every run included, with a run column: %s" % out_path)
    return "\n".join(p)


def _num(x):
    if x is None:
        return "none"
    return ("%d" % x) if float(x).is_integer() else ("%.1f" % x)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Turn question 9 of the tester feedback export into "
                                             "tester_lines.csv and a summary.")
    ap.add_argument("export", help="the Microsoft Forms export, .xlsx or .csv")
    ap.add_argument("--out", help="where to write tester_lines.csv (default: beside the export)")
    ap.add_argument("--q4", help="check only the question whose title starts with this for TEST RESPONSE")
    ap.add_argument("--all-runs", action="store_true",
                    help="count later runs (Play again, after the key was shown) in the rates as well")
    a = ap.parse_args(argv)
    out_path = a.out or os.path.join(os.path.dirname(os.path.abspath(a.export)), "tester_lines.csv")
    records, stats, notes = load(a.export, a.q4)
    write_lines(records, out_path)
    text = report(a.export, records, stats, notes, out_path, all_runs=a.all_runs)
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
