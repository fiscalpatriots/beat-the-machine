#!/usr/bin/env python3
"""Read the tester feedback form export and turn question 9 into one row per tester per line.

Standard library only.

    python tools/tester_record_parse.py responses.xlsx
    python tools/tester_record_parse.py responses.csv --out tester_lines.csv
    python tools/tester_record_parse.py responses.xlsx --q4 "Anything else"

The input is the Microsoft Forms export of "Second Pass: tester feedback", either the Excel file
Forms downloads (Responses, Open in Excel) or that sheet saved as CSV. From release 1.9.2 the drill's
tester link opens that form with question 9, "Your drill answers (the drill fills this in for you,
so please leave it as it is)", already holding the tester's locked lines. This script

  1. finds the question 9 column by its title, which starts "Your drill answers",
  2. drops every row whose question 4 answer starts "TEST RESPONSE" (question 4 is the fourth
     question column; --q4 picks it by the start of its title instead),
  3. parses each record, keeps the latest response for any attempt id submitted twice, and
  4. writes tester_lines.csv (one row per tester per line) and prints the summary for the
     scholarship write-up: testers, lines answered, catch rate per line and overall, false flag
     rate, reason agreement, median seconds per line, and the commonest reason chips on missed
     lines.

The record grammar is the one testerRecord() in index.html writes, documented there:

    record  = header { " || " line } [ " || truncated after line " N ]
    header  = stamp " | " codename " | " attemptId " | case " pick
              " | answered " count " | right " count " | points " count
    line    = "L" n " | " account " | " call " | " chips " | key " call " | " outcome
              " | basis " ( "agrees" | "differs" ) " | " seconds "s" [ " | " words ]

tests/test_tester_record_parse.py runs this against tests/tester-record-sample.csv, against an Excel
file it builds on the fly, and against records the drill itself writes.
"""
import argparse
import collections
import csv
import io
import os
import re
import statistics
import sys
import zipfile
import xml.etree.ElementTree as ET

Q9_PREFIX = "your drill answers"
TEST_PREFIX = "TEST RESPONSE"

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
TRUNC_RE = re.compile(r"^truncated after line (\d+)$", re.I)
STAMP_RE = re.compile(r"^second-pass-drill\s+(\S+)$", re.I)

OUT_FIELDS = ["response_id", "attempt_id", "codename", "version", "case", "line", "account",
              "call", "key", "outcome", "right", "basis_agrees", "seconds", "chips",
              "chips_short", "words", "answered", "lines_in_record", "truncated_after_line"]


class RecordError(ValueError):
    pass


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
    q9 = [i for i, t in enumerate(header) if (t or "").strip().lower().startswith(Q9_PREFIX)]
    if not q9:
        raise SystemExit('No column title starts "Your drill answers". Is this the tester feedback '
                         "form export, with question 9 in it?")
    questions = question_columns(header)
    if q4_prefix:
        hits = [i for i, t in enumerate(header) if (t or "").strip().lower().startswith(q4_prefix.strip().lower())]
        if not hits:
            raise SystemExit('No column title starts "%s".' % q4_prefix)
        q4 = hits[0]
    else:
        if len(questions) < 4:
            raise SystemExit("The export has fewer than four question columns, so question 4 cannot be found.")
        q4 = questions[3]
    rid = next((i for i, t in enumerate(header) if (t or "").strip().lower() == "id"), None)
    return q9[0], q4, rid


# ---------- parsing one record ----------

def parse_record(text):
    """One question 9 answer as {header..., lines: [...], truncated_after_line}."""
    text = (text or "").strip()
    if not text:
        raise RecordError("empty")
    parts = LINE_SPLIT.split(text)
    head = FIELD_SPLIT.split(parts[0])
    if len(head) != 7:
        raise RecordError("the header has %d fields, not 7" % len(head))
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

    rec = {
        "version": stamp.group(1),
        "codename": head[1],
        "attempt_id": head[2],
        "case": labelled(head[3], "case", number=False),
        "answered": labelled(head[4], "answered"),
        "right": labelled(head[5], "right"),
        "points": labelled(head[6], "points"),
        "lines": [],
        "truncated_after_line": None,
        "bad_lines": 0,
    }
    for seg in parts[1:]:
        t = TRUNC_RE.match(seg.strip())
        if t:
            rec["truncated_after_line"] = int(t.group(1))
            continue
        try:
            rec["lines"].append(parse_line(seg))
        except RecordError:
            rec["bad_lines"] += 1
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
    outcome = f[5].lower()
    basis = re.match(r"^basis\s+(agrees|differs)$", f[6], re.I)
    secs = re.match(r"^(\d+)s$", f[7])
    if call not in CALLS or not key or outcome not in OUTCOMES or not basis or not secs:
        raise RecordError("a line has a field outside the grammar")
    short = [c for c in f[3].split("+") if c and c != "none"]
    return {
        "line": int(m.group(1)),
        "account": f[1],
        "call": call,
        "chips_short": short,
        "chips": [CHIPS.get(c, c) for c in short],
        "key": key.group(1).lower(),
        "outcome": outcome,
        "right": outcome in ("caught", "cleared"),
        "basis_agrees": basis.group(1).lower() == "agrees",
        "seconds": int(secs.group(1)),
        "words": " | ".join(f[8:]).strip(),
    }


# ---------- the export as a whole ----------

def load(path, q4_prefix=None):
    rows = read_export(path)
    if not rows:
        raise SystemExit("The file has no rows.")
    header = rows[0]
    q9, q4, rid = find_columns(header, q4_prefix)
    stats = collections.Counter()
    kept = collections.OrderedDict()
    problems = []
    for n, row in enumerate(rows[1:], start=2):
        if not any((c or "").strip() for c in row):
            continue
        stats["responses"] += 1
        cell = lambda i: (row[i] if i is not None and i < len(row) else "") or ""
        if cell(q4).strip().upper().startswith(TEST_PREFIX):
            stats["test rows dropped"] += 1
            continue
        text = cell(q9).strip()
        if not text:
            stats["no drill answers"] += 1
            continue
        try:
            rec = parse_record(text)
        except RecordError as e:
            stats["records that did not parse"] += 1
            problems.append("row %d: %s" % (n, e))
            continue
        rec["response_id"] = cell(rid).strip() or "row %d" % n
        if rec["attempt_id"] in kept:
            stats["repeat submissions of one attempt, latest kept"] += 1
            del kept[rec["attempt_id"]]
        kept[rec["attempt_id"]] = rec
        stats["bad line segments skipped"] += rec["bad_lines"]
    return list(kept.values()), stats, problems


def write_lines(records, out_path):
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_FIELDS)
        w.writeheader()
        for r in records:
            for ln in r["lines"]:
                w.writerow({
                    "response_id": r["response_id"], "attempt_id": r["attempt_id"],
                    "codename": r["codename"], "version": r["version"], "case": r["case"],
                    "line": ln["line"], "account": ln["account"], "call": ln["call"],
                    "key": ln["key"], "outcome": ln["outcome"], "right": int(ln["right"]),
                    "basis_agrees": int(ln["basis_agrees"]), "seconds": ln["seconds"],
                    "chips": "; ".join(ln["chips"]), "chips_short": "+".join(ln["chips_short"]),
                    "words": ln["words"], "answered": r["answered"],
                    "lines_in_record": len(r["lines"]),
                    "truncated_after_line": "" if r["truncated_after_line"] is None else r["truncated_after_line"],
                })


# ---------- the summary ----------

def rate(num, den):
    if not den:
        return "none on record"
    return "%d of %d (%d%%)" % (num, den, round(100.0 * num / den))


def summarize(records):
    lines = [ln for r in records for ln in r["lines"]]
    flagged = [ln for ln in lines if ln["key"] == "flag"]
    clean = [ln for ln in lines if ln["key"] == "stand"]
    by_line = collections.OrderedDict()
    for ln in sorted(lines, key=lambda x: x["line"]):
        by_line.setdefault(ln["line"], []).append(ln)
    missed = [ln for ln in lines if ln["outcome"] == "missed"]
    false_flags = [ln for ln in lines if ln["outcome"] == "false flag"]
    chip_miss = collections.Counter(c for ln in missed for c in ln["chips"])
    chip_false = collections.Counter(c for ln in false_flags for c in ln["chips"])
    return {
        "testers": len(records),
        "codenames": len(set(r["codename"] for r in records)),
        "lines": len(lines),
        "answered_total": sum(r["answered"] for r in records),
        "truncated": sum(1 for r in records if r["truncated_after_line"] is not None),
        "caught": sum(1 for ln in flagged if ln["outcome"] == "caught"),
        "flag_lines": len(flagged),
        "false_flags": len(false_flags),
        "clean_lines": len(clean),
        "basis_agrees": sum(1 for ln in lines if ln["basis_agrees"]),
        "right": sum(1 for ln in lines if ln["right"]),
        "right_basis_agrees": sum(1 for ln in lines if ln["right"] and ln["basis_agrees"]),
        "median_seconds": statistics.median([ln["seconds"] for ln in lines]) if lines else None,
        "by_line": by_line,
        "chips_on_missed": chip_miss.most_common(),
        "chips_on_false_flags": chip_false.most_common(),
        "missed": len(missed),
    }


def report(path, records, stats, problems, out_path):
    s = summarize(records)
    p = []
    p.append("Second Pass tester answers, from %s" % os.path.basename(path))
    p.append("")
    p.append("Rows read: %d. Test rows dropped: %d. Rows with no drill answers: %d."
             % (stats["responses"], stats["test rows dropped"], stats["no drill answers"]))
    if stats["records that did not parse"]:
        p.append("Records that did not parse: %d (%s)." % (stats["records that did not parse"], "; ".join(problems)))
    if stats["repeat submissions of one attempt, latest kept"]:
        p.append("Repeat submissions of one attempt: %d, the latest of each kept."
                 % stats["repeat submissions of one attempt, latest kept"])
    if stats["bad line segments skipped"]:
        p.append("Line segments outside the grammar, skipped: %d." % stats["bad line segments skipped"])
    p.append("")
    p.append("Testers: %d (%d distinct codenames)." % (s["testers"], s["codenames"]))
    p.append("Lines answered: %d in the records%s." % (
        s["lines"], "" if s["answered_total"] == s["lines"] else
        ", of %d locked (%d %s cut to fit the form link)" % (
            s["answered_total"], s["truncated"], "record was" if s["truncated"] == 1 else "records were")))
    if not s["lines"]:
        p.append("")
        p.append("No lines to summarize.")
        return "\n".join(p)
    p.append("Catch rate, lines with a problem: %s." % rate(s["caught"], s["flag_lines"]))
    p.append("False flag rate, clean lines: %s." % rate(s["false_flags"], s["clean_lines"]))
    p.append("Right calls, every line: %s." % rate(s["right"], s["lines"]))
    p.append("Reason agrees with the key, every line: %s." % rate(s["basis_agrees"], s["lines"]))
    p.append("Reason agrees on a right call: %s." % rate(s["right_basis_agrees"], s["right"]))
    p.append("Median seconds a line: %s." % _num(s["median_seconds"]))
    p.append("")
    p.append("By line")
    p.append("%-5s %-8s %-6s %-8s %-28s %-15s %s" % ("Line", "Account", "Key", "Testers", "Caught or cleared",
                                                    "Reason agrees", "Median seconds"))
    for n, lns in s["by_line"].items():
        key = lns[0]["key"]
        right = sum(1 for ln in lns if ln["right"])
        label = ("caught " if key == "flag" else "cleared ") + rate(right, len(lns))
        agrees = sum(1 for ln in lns if ln["basis_agrees"])
        p.append("%-5s %-8s %-6s %-8d %-28s %-15s %s" % (
            "L%d" % n, lns[0]["account"], key, len(lns), label,
            "%d of %d" % (agrees, len(lns)), _num(statistics.median([ln["seconds"] for ln in lns]))))
    p.append("")
    p.append("Reason chips on missed lines (a problem let stand), %d %s:" % (
        s["missed"], "line" if s["missed"] == 1 else "lines"))
    p.extend(["  %s: %d" % (c, k) for c, k in s["chips_on_missed"]] or ["  none on record"])
    p.append("Reason chips on false flags (a clean line flagged), %d %s:" % (
        s["false_flags"], "line" if s["false_flags"] == 1 else "lines"))
    p.extend(["  %s: %d" % (c, k) for c, k in s["chips_on_false_flags"]] or ["  none on record"])
    p.append("")
    p.append("One row per tester per line: %s" % out_path)
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
    ap.add_argument("--q4", help="the start of question 4's title, when it is not the fourth question column")
    a = ap.parse_args(argv)
    out_path = a.out or os.path.join(os.path.dirname(os.path.abspath(a.export)), "tester_lines.csv")
    records, stats, problems = load(a.export, a.q4)
    write_lines(records, out_path)
    text = report(a.export, records, stats, problems, out_path)
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
