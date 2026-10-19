#!/usr/bin/env python3
"""Tests for tools/tester_record_parse.py. Standard library only.

    python tools/tests/test_tester_record_parse.py      (from the repository root)
    python -m pytest tools/tests -q                     (also works where pytest is installed)

The sample export is tests/tester-record-sample.csv: six responses in the column layout Microsoft
Forms exports, with three real drill records (one cut to fit the form link), a TEST RESPONSE row,
a response with question 9 left empty, and one attempt submitted twice. The same rows are also
written into an Excel file on the fly, and the drift guard asks the drill itself (through
tests/tester-record-emit.cjs) for records and checks the parser reads back every field.
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import tester_record_parse as p  # noqa: E402

SAMPLE = os.path.join(REPO, "tests", "tester-record-sample.csv")
EMIT = os.path.join(REPO, "tests", "tester-record-emit.cjs")


def sample_rows():
    with open(SAMPLE, encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


def col(n):
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def write_xlsx(path, rows):
    """A minimal workbook the way Excel writes one: the header through shared strings, the body
    as inline strings, and a number cell for the id, so all three cell kinds are read."""
    shared = rows[0]
    sheet = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    for r, row in enumerate(rows, start=1):
        cells = []
        for c, val in enumerate(row):
            ref = "%s%d" % (col(c), r)
            if r == 1:
                cells.append('<c r="%s" t="s"><v>%d</v></c>' % (ref, c))
            elif c == 0 and val.isdigit():
                cells.append('<c r="%s"><v>%s</v></c>' % (ref, val))
            elif val == "":
                continue
            else:
                cells.append('<c r="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, escape(val)))
        sheet.append('<row r="%d">%s</row>' % (r, "".join(cells)))
    sheet.append("</sheetData></worksheet>")
    sst = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="%d" uniqueCount="%d">'
           % (len(shared), len(shared))]
    for s in shared:
        sst.append("<si><r><t>%s</t></r></si>" % escape(s))
    sst.append("</sst>")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr("xl/workbook.xml",
                   '<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                   '<sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                   'Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", "".join(sheet))
        z.writestr("xl/sharedStrings.xml", "".join(sst))


class SampleExport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_counts(self):
        records, stats, problems = p.load(SAMPLE)
        self.assertEqual(stats["responses"], 6)
        self.assertEqual(stats["test rows dropped"], 1)
        self.assertEqual(stats["no drill answers"], 1)
        self.assertEqual(stats["repeat submissions of one attempt, latest kept"], 1)
        self.assertEqual(problems, [])
        self.assertEqual([r["codename"] for r in records], ["Slate Heron", "Teal Wren", "Amber Owl"])
        self.assertNotIn("Coral Lynx", [r["codename"] for r in records], "the TEST RESPONSE row is dropped")

    def test_repeat_keeps_the_latest_response(self):
        records, _, _ = p.load(SAMPLE)
        amber = [r for r in records if r["codename"] == "Amber Owl"]
        self.assertEqual(len(amber), 1)
        self.assertEqual(amber[0]["response_id"], "6")

    def test_truncated_record(self):
        records, _, _ = p.load(SAMPLE)
        teal = [r for r in records if r["codename"] == "Teal Wren"][0]
        self.assertEqual(teal["answered"], 14)
        self.assertEqual(teal["truncated_after_line"], 5)
        self.assertEqual([ln["line"] for ln in teal["lines"]], [1, 2, 3, 4, 5])

    def test_line_fields(self):
        records, _, _ = p.load(SAMPLE)
        slate = [r for r in records if r["codename"] == "Slate Heron"][0]
        self.assertEqual(slate["version"], "1.9.2")
        self.assertEqual(slate["case"], "halyard")
        self.assertEqual((slate["answered"], slate["right"], slate["points"]), (5, 3, 450))
        ln = slate["lines"][1]
        self.assertEqual(ln["line"], 2)
        self.assertEqual(ln["account"], "6200")
        self.assertEqual((ln["call"], ln["key"], ln["outcome"]), ("flag", "flag", "caught"))
        self.assertEqual(ln["chips"], ["wrong period", "no source on file"])
        self.assertEqual(ln["chips_short"], ["period", "source"])
        self.assertTrue(ln["basis_agrees"])
        self.assertEqual(ln["seconds"], 52)
        self.assertEqual(ln["words"], 'accrual, "not" June\'s')
        self.assertEqual(slate["lines"][3]["outcome"], "false flag")
        self.assertEqual(slate["lines"][0]["words"], "")

    def test_summary_numbers(self):
        records, _, _ = p.load(SAMPLE)
        s = p.summarize(records)
        self.assertEqual(s["testers"], 3)
        self.assertEqual(s["lines"], 15)
        self.assertEqual(s["answered_total"], 24)
        self.assertEqual((s["caught"], s["flag_lines"]), (7, 9))
        self.assertEqual((s["false_flags"], s["clean_lines"]), (1, 6))
        self.assertEqual(s["basis_agrees"], 12)
        self.assertEqual(s["median_seconds"], 25)
        self.assertEqual(s["chips_on_missed"], [("the figure and reason hold", 2)])
        self.assertEqual(s["chips_on_false_flags"], [("wrong account", 1)])
        self.assertEqual(list(s["by_line"].keys()), [1, 2, 3, 4, 5])

    def test_tester_lines_csv(self):
        out = os.path.join(self.tmp, "tester_lines.csv")
        records, _, _ = p.load(SAMPLE)
        p.write_lines(records, out)
        with open(out, encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(len(rows), 15)
        self.assertEqual(list(rows[0].keys()), p.OUT_FIELDS)
        self.assertEqual({r["codename"] for r in rows}, {"Amber Owl", "Slate Heron", "Teal Wren"})
        with open(out, encoding="utf-8") as fh:
            self.assertNotIn("anonymous", fh.read(), "no email column rides along")

    def test_main_prints_the_summary(self):
        out = os.path.join(self.tmp, "lines.csv")
        proc = subprocess.run([sys.executable, os.path.join(TOOLS, "tester_record_parse.py"), SAMPLE, "--out", out],
                              capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for want in ("Testers: 3", "Lines answered: 15", "Catch rate, lines with a problem: 7 of 9 (78%)",
                     "False flag rate, clean lines: 1 of 6 (17%)", "Reason agrees with the key, every line: 12 of 15 (80%)",
                     "Median seconds a line: 25", "the figure and reason hold: 2", "Test rows dropped: 1"):
            self.assertIn(want, proc.stdout)
        self.assertTrue(os.path.exists(out))

    def test_q4_by_title(self):
        a, _, _ = p.load(SAMPLE)
        b, stats, _ = p.load(SAMPLE, q4_prefix="Question 4")
        self.assertEqual([r["attempt_id"] for r in a], [r["attempt_id"] for r in b])
        self.assertEqual(stats["test rows dropped"], 1)

    def test_xlsx_reads_the_same(self):
        path = os.path.join(self.tmp, "responses.xlsx")
        write_xlsx(path, sample_rows())
        a, sa, _ = p.load(SAMPLE)
        b, sb, _ = p.load(path)
        self.assertEqual(sa, sb)
        strip = lambda rs: [{k: v for k, v in r.items()} for r in rs]
        self.assertEqual(strip(a), strip(b))

    def test_no_question_9(self):
        path = os.path.join(self.tmp, "old.csv")
        rows = [r[:-1] for r in sample_rows()]
        with open(path, "w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerows(rows)
        with self.assertRaises(SystemExit):
            p.load(path)


class Grammar(unittest.TestCase):
    HEAD = "second-pass-drill 1.9.2 | Amber Owl | att-x | case halyard | answered 2 | right 1 | points 150"

    def test_minimal(self):
        r = p.parse_record(self.HEAD + " || L1 | 4200 | flag | none | key flag | caught | basis differs | 3s")
        self.assertEqual(r["lines"][0]["chips"], [])
        self.assertEqual(r["lines"][0]["words"], "")

    def test_spaces_around_delimiters_are_forgiven(self):
        r = p.parse_record(self.HEAD.replace(" | ", "|") + "||L1|4200|stand|holds|key stand|cleared|basis agrees|7s|fine")
        self.assertEqual(r["codename"], "Amber Owl")
        self.assertEqual(r["lines"][0]["words"], "fine")

    def test_bad_header(self):
        for bad in ("", "hello", "second-pass-drill 1.9.2 | a | b", self.HEAD.replace("answered 2", "answered two")):
            with self.assertRaises(p.RecordError):
                p.parse_record(bad)

    def test_bad_line_is_skipped_and_counted(self):
        r = p.parse_record(self.HEAD + " || L1 | 4200 | maybe | holds | key flag | caught | basis agrees | 3s"
                           " || L2 | 6200 | flag | source | key flag | caught | basis agrees | 4s")
        self.assertEqual(r["bad_lines"], 1)
        self.assertEqual([ln["line"] for ln in r["lines"]], [2])

    def test_truncation_marker(self):
        r = p.parse_record(self.HEAD + " || L1 | 4200 | flag | tie | key flag | caught | basis agrees | 3s"
                           " || truncated after line 1")
        self.assertEqual(r["truncated_after_line"], 1)
        self.assertEqual(len(r["lines"]), 1)


def node():
    return shutil.which("node")


@unittest.skipUnless(node(), "node is not on this machine, so the drill cannot be asked for records")
class DriftGuard(unittest.TestCase):
    """Records the drill writes, read back field for field."""

    @classmethod
    def setUpClass(cls):
        proc = subprocess.run([node(), EMIT], capture_output=True, text=True, encoding="utf-8", cwd=REPO)
        if proc.returncode != 0:
            raise AssertionError("tests/tester-record-emit.cjs failed: " + proc.stderr)
        cls.runs = json.loads(proc.stdout)

    def test_every_field_round_trips(self):
        self.assertGreaterEqual(len(self.runs), 3)
        for run in self.runs:
            r = p.parse_record(run["record"])
            h = run["header"]
            self.assertEqual((r["version"], r["codename"], r["attempt_id"], r["case"], r["answered"], r["right"], r["points"]),
                             (h["version"], h["codename"], h["attempt_id"], h["case"], h["answered"], h["right"], h["points"]))
            self.assertEqual(r["bad_lines"], 0)
            self.assertEqual(len(r["lines"]), run["included"])
            for got, want in zip(r["lines"], run["lines"]):
                self.assertEqual(got["line"], want["line"])
                self.assertEqual(got["account"], want["account"])
                self.assertEqual(got["call"], want["call"])
                self.assertEqual(got["chips"], want["chips"])
                self.assertEqual(got["key"], want["key"])
                self.assertEqual(got["outcome"], want["outcome"])
                self.assertEqual(got["basis_agrees"], want["basis_agrees"])
                self.assertEqual(got["seconds"], want["seconds"])
                self.assertEqual(got["words"], want["words"])
            if run["included"] < h["answered"]:
                self.assertEqual(r["truncated_after_line"], run["included"])
            else:
                self.assertIsNone(r["truncated_after_line"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
