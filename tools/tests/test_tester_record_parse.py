#!/usr/bin/env python3
"""Tests for tools/tester_record_parse.py. Standard library only.

    python tools/tests/test_tester_record_parse.py      (from the repository root)
    python -m pytest tools/tests -q                     (also works where pytest is installed)

The sample export is tests/tester-record-sample.csv: eight responses in the column layout Microsoft
Forms exports, built from records the drill wrote. Three are first runs (one tester kept going to
line 14, with words cut to fit the link), one is a second run of the same tab after Play again, one
is a TEST RESPONSE row, one left question 9 empty, one attempt is submitted twice, and one record
was edited by hand before sending. The same rows are also written into an Excel file on the fly,
and the drift guard asks the drill itself (through tests/tester-record-emit.cjs) for records and
checks the parser reads back every field.
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
SCRIPT = os.path.join(TOOLS, "tester_record_parse.py")


def sample_rows():
    with open(SAMPLE, encoding="utf-8-sig", newline="") as fh:
        return list(csv.reader(fh))


def write_csv(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


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


def run_main(*args):
    proc = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True, encoding="utf-8")
    return proc


class SampleExport(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_counts(self):
        records, stats, notes = p.load(SAMPLE)
        self.assertEqual(stats["responses"], 8)
        self.assertEqual(stats["test rows dropped"], 1)
        self.assertEqual(stats["no drill answers"], 1)
        self.assertEqual(stats["repeat submissions of one attempt, latest kept"], 1)
        self.assertEqual(stats["records edited by the tester"], 1)
        self.assertEqual(stats["rows that carry a name or email"], 0, "the sample's Email column reads anonymous")
        self.assertEqual(notes["parse"], [])
        self.assertIn("line 1 says caught", notes["edited"][0])
        self.assertEqual([(r["codename"], r["run"]) for r in records],
                         [("Slate Heron", 1), ("Teal Wren", 1), ("Amber Owl", 1), ("Amber Owl", 2)])
        names = [r["codename"] for r in records]
        self.assertNotIn("Coral Lynx", names, "the TEST RESPONSE row is dropped")
        self.assertNotIn("Jade Puffin", names, "the edited record is left out")

    def test_repeat_keeps_the_latest_response(self):
        records, _, _ = p.load(SAMPLE)
        amber = [r for r in records if r["codename"] == "Amber Owl" and r["run"] == 1]
        self.assertEqual(len(amber), 1)
        self.assertEqual(amber[0]["response_id"], "6")

    def test_second_run_is_its_own_attempt(self):
        records, _, _ = p.load(SAMPLE)
        one, two = [r for r in records if r["codename"] == "Amber Owl"]
        self.assertNotEqual(one["attempt_id"], two["attempt_id"])
        self.assertEqual((one["run"], two["run"]), (1, 2))

    def test_words_cut_record(self):
        records, _, _ = p.load(SAMPLE)
        teal = [r for r in records if r["codename"] == "Teal Wren"][0]
        self.assertEqual(teal["answered"], 14)
        self.assertIsNone(teal["truncated_after_line"])
        self.assertEqual(teal["words_cut_to"], 20)
        self.assertEqual([ln["line"] for ln in teal["lines"]], list(range(1, 15)))
        self.assertTrue(all(len(ln["words"]) <= 20 for ln in teal["lines"]))

    def test_line_fields(self):
        records, _, _ = p.load(SAMPLE)
        slate = [r for r in records if r["codename"] == "Slate Heron"][0]
        self.assertEqual(slate["version"], "1.9.2")
        self.assertEqual((slate["case"], slate["case_file"], slate["run"]), ("halyard", "halyard-v4", 1))
        self.assertEqual((slate["answered"], slate["right"], slate["points"]), (5, 3, 450))
        self.assertTrue(slate["keys_checked"])
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
        self.assertEqual((s["attempts"], s["first_runs"], s["reattempts"]), (4, 3, 1))
        self.assertEqual(s["lines"], 24, "first runs only: 5 + 14 + 5")
        e, l = s["early"], s["late"]
        self.assertEqual((e["caught"], e["flag_lines"], e["false_flags"], e["clean_lines"], e["right"], e["lines"]),
                         (7, 9, 1, 6, 12, 15))
        self.assertEqual((e["caught_right_reason"], s["early_attempts"]), (7, 3))
        self.assertEqual((l["caught"], l["flag_lines"], l["false_flags"], l["clean_lines"], s["late_attempts"]), (4, 5, 0, 4, 1))
        self.assertEqual(s["median_seconds"], 18, "line 1 is left out of the median")
        self.assertEqual(s["chips_on_missed"], [("the figure and reason hold", 3)])
        self.assertEqual(s["chips_on_false_flags"], [("wrong account", 1)])
        self.assertEqual(list(s["by_line"].keys()), list(range(1, 15)))
        self.assertEqual(s["versions"], [("1.9.2", 3)])
        self.assertEqual(s["words_cut"], 1)

    def test_all_runs_counts_the_second_run(self):
        records, _, _ = p.load(SAMPLE)
        s = p.summarize(records, all_runs=True)
        self.assertEqual(s["lines"], 29)
        self.assertEqual((s["early"]["caught"], s["early"]["flag_lines"]), (10, 12))
        self.assertEqual(s["early_attempts"], 4)

    def test_tester_lines_csv(self):
        out = os.path.join(self.tmp, "tester_lines.csv")
        records, _, _ = p.load(SAMPLE)
        p.write_lines(records, out)
        with open(out, encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        self.assertEqual(len(rows), 29, "every run is written, with a run column")
        self.assertEqual(list(rows[0].keys()), p.OUT_FIELDS)
        self.assertEqual(sum(1 for r in rows if r["run"] == "2"), 5)
        self.assertEqual({r["codename"] for r in rows}, {"Amber Owl", "Slate Heron", "Teal Wren"})
        self.assertEqual({r["words_cut_to"] for r in rows if r["codename"] == "Teal Wren"}, {"20"})
        with open(out, encoding="utf-8") as fh:
            self.assertNotIn("anonymous", fh.read(), "no email column rides along")

    def test_main_prints_the_summary(self):
        out = os.path.join(self.tmp, "lines.csv")
        proc = run_main(SAMPLE, "--out", out)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        for want in ("Attempts with drill answers: 4 (first runs 3, reattempts 1).",
                     "Later runs excluded: 1.",
                     "Records edited by the tester, left out: 1 (sheet row 9: line 1 says caught",
                     "Lines 1 to 5, from 3 first-run attempts:",
                     "  Caught, lines with a problem: 7 of 9 (78%).",
                     "  False flags, clean lines: 1 of 6 (17%).",
                     "  Right reason on a caught problem line: 7 of 7 (100%).",
                     "Lines 6 and up, from the 1 first-run attempt that kept going:",
                     "Median active seconds a line: 18, leaving out line 1",
                     "30, includes the tour",
                     "Records whose words were shortened to fit the link: 1.",
                     "Reattempts, left out of the rates above:",
                     "Amber Owl, run 2,",
                     "the figure and reason hold: 3", "Test rows dropped: 1"):
            self.assertIn(want, proc.stdout)
        self.assertNotIn("Testers:", proc.stdout)
        self.assertNotIn("distinct codenames", proc.stdout)
        self.assertNotIn("Warning", proc.stdout)
        self.assertTrue(os.path.exists(out))

    def test_main_all_runs(self):
        proc = run_main(SAMPLE, "--out", os.path.join(self.tmp, "lines.csv"), "--all-runs")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Later runs included in the rates: 1", proc.stdout)
        self.assertIn("Lines 1 to 5, from 4 attempts:", proc.stdout)
        self.assertIn("  Caught, lines with a problem: 10 of 12 (83%).", proc.stdout)

    def test_q4_by_title(self):
        a, _, _ = p.load(SAMPLE)
        b, stats, _ = p.load(SAMPLE, q4_prefix="Question 4")
        self.assertEqual([r["attempt_id"] for r in a], [r["attempt_id"] for r in b])
        self.assertEqual(stats["test rows dropped"], 1)

    def test_test_response_in_any_question_is_dropped(self):
        rows = sample_rows()
        rows[1][5] = "TEST RESPONSE typed into question 1"
        path = os.path.join(self.tmp, "q1.csv")
        write_csv(path, rows)
        records, stats, _ = p.load(path)
        self.assertEqual(stats["test rows dropped"], 2)
        _, stats4, _ = p.load(path, q4_prefix="Question 4")
        self.assertEqual(stats4["test rows dropped"], 1, "--q4 checks that question only")

    def test_likert_before_question_4(self):
        """A Likert question exports one column per statement, which moves question 4 along."""
        rows = sample_rows()
        head = rows[0]
        i2 = head.index("Question 2")
        rows = [r[:i2] + ([r[i2], r[i2]] if n else ["Question 2.Statement A", "Question 2.Statement B"]) + r[i2 + 1:]
                for n, r in enumerate(rows)]
        path = os.path.join(self.tmp, "likert.csv")
        write_csv(path, rows)
        records, stats, notes = p.load(path)
        self.assertEqual(stats["test rows dropped"], 1, "the TEST RESPONSE row is still dropped")
        self.assertNotIn("Coral Lynx", [r["codename"] for r in records])
        self.assertTrue(notes["layout"] and "ninth question column" in notes["layout"])
        proc = run_main(path, "--out", os.path.join(self.tmp, "lines.csv"))
        self.assertIn("Question 9 is not the ninth question column", proc.stdout)

    def test_rows_with_a_name_or_email_are_counted(self):
        rows = sample_rows()
        rows[1][3] = "someone@gmu.edu"
        rows[2][4] = "Some One"
        path = os.path.join(self.tmp, "named.csv")
        write_csv(path, rows)
        records, stats, _ = p.load(path)
        self.assertEqual(stats["rows that carry a name or email"], 2)
        out = os.path.join(self.tmp, "lines.csv")
        proc = run_main(path, "--out", out)
        self.assertIn("Rows that carry a respondent's name or email: 2.", proc.stdout)
        with open(out, encoding="utf-8") as fh:
            body = fh.read()
        self.assertNotIn("gmu.edu", body)
        self.assertNotIn("Some One", body)

    def test_xlsx_reads_the_same(self):
        path = os.path.join(self.tmp, "responses.xlsx")
        write_xlsx(path, sample_rows())
        a, sa, _ = p.load(SAMPLE)
        b, sb, _ = p.load(path)
        self.assertEqual(sa, sb)
        self.assertEqual(a, b)

    def test_no_question_9(self):
        path = os.path.join(self.tmp, "old.csv")
        write_csv(path, [r[:-1] for r in sample_rows()])
        with self.assertRaises(SystemExit):
            p.load(path)


# the first five Halyard lines: account, key
L = {1: ("4200", "flag"), 2: ("6200", "flag"), 3: ("5100", "flag"), 4: ("4100", "stand"), 5: ("6500", "stand")}


def record(lines, answered=None, right=None, tail=(), sep="|", lsep="||", head_fields=9, run=1):
    """A record in the drill's form, its header counted from its lines unless told otherwise."""
    def outcome(call, key):
        return p.outcome_of(call, key)
    segs = []
    for ln in lines:
        segs.append(sep.join(ln))
    ans = len(lines) if answered is None else answered
    rt = sum(1 for ln in lines if outcome(ln[2], ln[4].split()[-1]) in ("caught", "cleared")) if right is None else right
    head = ["second-pass-drill 1.9.2", "Amber Owl", "att-x", "case halyard", "answered %d" % ans, "right %d" % rt, "points 150"]
    if head_fields >= 8:
        head.append("run %d" % run)
    if head_fields >= 9:
        head.append("case file halyard-v4")
    return lsep.join([sep.join(head)] + segs + list(tail))


def line(n, call, chips, basis, secs="3s", words=None, outcome=None):
    acct, key = L[n]
    out = [("L%d" % n), acct, call, chips, "key " + key, outcome or p.outcome_of(call, key), "basis " + basis, secs]
    if words:
        out.append(words)
    return out


class Grammar(unittest.TestCase):
    def test_minimal(self):
        r = p.parse_record(record([line(1, "flag", "none", "differs")]))
        self.assertEqual(r["lines"][0]["chips"], [])
        self.assertEqual(r["lines"][0]["words"], "")
        self.assertEqual((r["run"], r["case_file"], r["keys_checked"]), (1, "halyard-v4", True))

    def test_spaces_around_delimiters_are_forgiven(self):
        r = p.parse_record(record([line(4, "stand", "holds", "agrees", words="fine")], sep=" | ", lsep=" || "))
        self.assertEqual(r["codename"], "Amber Owl")
        self.assertEqual(r["lines"][0]["words"], "fine")

    def test_seven_field_header_reads_as_run_one(self):
        r = p.parse_record(record([line(1, "flag", "tie+owed", "agrees")], sep=" | ", lsep=" || ", head_fields=7))
        self.assertEqual((r["run"], r["case_file"], r["keys_checked"]), (1, "halyard-v4", True))

    def test_eight_field_header_carries_the_run(self):
        r = p.parse_record(record([line(1, "flag", "tie+owed", "agrees")], head_fields=8, run=3))
        self.assertEqual((r["run"], r["case_file"]), (3, "halyard-v4"))

    def test_bad_header(self):
        for bad in ("", "hello", "second-pass-drill 1.9.2|a|b",
                    record([line(1, "flag", "tie", "agrees")]).replace("answered 1", "answered one"),
                    record([line(1, "flag", "tie", "agrees")]).replace("run 1", "run one")):
            with self.assertRaises(p.RecordError):
                p.parse_record(bad)

    def test_bad_line_marks_the_record_edited(self):
        text = record([["L1", "4200", "maybe", "holds", "key flag", "caught", "basis agrees", "3s"],
                       line(2, "flag", "source", "agrees")], answered=2, right=1)
        with self.assertRaises(p.EditedError):
            p.parse_record(text)
        r = p.parse_record(text, check=False)
        self.assertEqual(r["bad_lines"], 1)
        self.assertEqual([ln["line"] for ln in r["lines"]], [2])

    def test_markers(self):
        r = p.parse_record(record([line(1, "flag", "tie", "agrees", words="short")], answered=3,
                                  tail=["words cut to 20", "words left off after line 1", "truncated after line 1"]))
        self.assertEqual((r["words_cut_to"], r["words_left_off_after_line"], r["truncated_after_line"]), (20, 1, 1))
        self.assertEqual(len(r["lines"]), 1)

    def test_note_after_the_seconds_becomes_words(self):
        r = p.parse_record(record([line(4, "stand", "holds", "agrees", secs="9s thanks")]))
        self.assertEqual((r["lines"][0]["seconds"], r["lines"][0]["words"]), (9, "thanks"))
        r = p.parse_record(record([line(4, "stand", "holds", "agrees")]) + "\r\nthanks, this was fun")
        self.assertEqual((r["lines"][0]["seconds"], r["lines"][0]["words"]), (3, "thanks, this was fun"))
        self.assertEqual(r["bad_lines"], 0)

    def edited(self, text, reason):
        with self.assertRaises(p.EditedError) as cm:
            p.parse_record(text)
        self.assertTrue(any(reason in w for w in cm.exception.reasons), cm.exception.reasons)

    def test_an_outcome_that_does_not_follow_is_an_edit(self):
        self.edited(record([line(1, "stand", "holds", "differs", outcome="caught")], right=1), "line 1 says caught")

    def test_an_account_or_key_off_the_case_file_is_an_edit(self):
        bad = line(1, "flag", "tie", "agrees")
        bad[1] = "9999"
        self.edited(record([bad]), "names account 9999")
        bad = ["L4", "4100", "flag", "source", "key flag", "caught", "basis differs", "3s"]
        self.edited(record([bad]), "keys it stand")

    def test_a_basis_the_chips_do_not_support_is_an_edit(self):
        self.edited(record([line(1, "flag", "account", "agrees")]), "line 1 says the basis agrees")
        self.edited(record([line(4, "stand", "holds", "differs")]), "line 4 says the basis differs")

    def test_repeated_out_of_order_and_out_of_range_lines_are_edits(self):
        self.edited(record([line(1, "flag", "tie", "agrees"), line(1, "flag", "tie", "agrees")]), "line 1 appears twice")
        self.edited(record([line(2, "flag", "period", "agrees"), line(1, "flag", "tie", "agrees")]), "line 1 is out of order")
        far = ["L15", "4200", "flag", "tie", "key flag", "caught", "basis agrees", "3s"]
        self.edited(record([far]), "line 15 is not on halyard-v4")

    def test_header_counts_must_match_an_uncut_record(self):
        self.edited(record([line(1, "flag", "tie", "agrees")], answered=2), "says 2 answered")
        self.edited(record([line(1, "flag", "tie", "agrees")], right=0), "says 0 right")
        r = p.parse_record(record([line(1, "flag", "tie", "agrees")], answered=4, right=3, tail=["truncated after line 1"]))
        self.assertEqual(r["truncated_after_line"], 1)
        self.edited(record([line(1, "flag", "tie", "agrees")], answered=4, tail=["truncated after line 2"]), "cut after line 2")

    def test_a_case_file_not_here_skips_the_key_check(self):
        text = record([line(1, "flag", "tie", "agrees")]).replace("case file halyard-v4", "case file halyard-v9")
        r = p.parse_record(text)
        self.assertFalse(r["keys_checked"])
        r = p.parse_record(record([line(1, "flag", "tie", "agrees")]), cases_dir=None)
        self.assertFalse(r["keys_checked"])
        self.assertEqual(r["edits"], [])


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
        self.assertGreaterEqual(len(self.runs), 5)
        for run in self.runs:
            r = p.parse_record(run["record"])
            h = run["header"]
            self.assertEqual((r["version"], r["codename"], r["attempt_id"], r["case"], r["answered"], r["right"],
                              r["points"], r["run"], r["case_file"]),
                             (h["version"], h["codename"], h["attempt_id"], h["case"], h["answered"], h["right"],
                              h["points"], h["run"], h["case_file"]))
            self.assertEqual(r["bad_lines"], 0)
            self.assertEqual(r["edits"], [])
            self.assertTrue(r["keys_checked"])
            self.assertEqual(len(r["lines"]), run["included"])
            cut = run["words_cap"] < 80 or run["words_off_after"] is not None
            for got, want in zip(r["lines"], run["lines"]):
                self.assertEqual(got["line"], want["line"])
                self.assertEqual(got["account"], want["account"])
                self.assertEqual(got["call"], want["call"])
                self.assertEqual(got["chips"], want["chips"])
                self.assertEqual(got["key"], want["key"])
                self.assertEqual(got["outcome"], want["outcome"])
                self.assertEqual(got["basis_agrees"], want["basis_agrees"])
                self.assertEqual(got["seconds"], want["seconds"])
                if not cut:
                    self.assertEqual(got["words"], want["words"])
                else:
                    self.assertTrue(want["words"].startswith(got["words"]))
            self.assertEqual(r["words_cut_to"], run["words_cap"] if run["words_cap"] < 80 else None)
            self.assertEqual(r["words_left_off_after_line"], run["words_off_after"])
            if run["included"] < h["answered"]:
                self.assertEqual(r["truncated_after_line"], run["included"])
            else:
                self.assertIsNone(r["truncated_after_line"])

    def test_the_drill_writes_compact_delimiters(self):
        for run in self.runs:
            self.assertNotIn(" | ", run["record"])
            self.assertNotIn(" || ", run["record"])

    def test_a_link_record_with_long_words_keeps_every_line(self):
        teal = [run for run in self.runs if run["header"]["codename"] == "Teal Wren"][0]
        self.assertEqual(teal["included"], 14)
        self.assertLess(teal["words_cap"], 80)

    def test_play_again_is_run_two_and_left_out_of_the_rates(self):
        amber = [run for run in self.runs if run["header"]["codename"] == "Amber Owl"]
        self.assertEqual([run["header"]["run"] for run in amber], [1, 2])
        self.assertNotEqual(amber[0]["header"]["attempt_id"], amber[1]["header"]["attempt_id"])
        records = [p.parse_record(run["record"]) for run in self.runs]
        self.assertIn("|run 2|", amber[1]["record"])
        s = p.summarize(records)
        self.assertEqual((s["first_runs"], s["reattempts"]), (len(self.runs) - 1, 1))
        self.assertEqual(s["lines"], sum(len(r["lines"]) for r in records if r["run"] == 1))
        self.assertEqual(p.summarize(records, all_runs=True)["lines"], sum(len(r["lines"]) for r in records))


if __name__ == "__main__":
    unittest.main(verbosity=1)
