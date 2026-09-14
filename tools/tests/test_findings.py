#!/usr/bin/env python3
"""Tests for tools/findings.py. Standard library only.

    python tools/tests/test_findings.py          (from the repository root)
    python -m pytest tools/tests -q              (also works where pytest is installed)

Every response file here is built on the fly in a temporary folder from the case files in
cases/, so a test never depends on a participant export. The third independent review's own
synthetic files are read too when that evidence folder is on this machine, and those tests are
skipped where it is not; set SECOND_PASS_REVIEW3_EVIDENCE to point at another copy.
"""
import csv
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import findings as f  # noqa: E402

CASES = os.path.join(REPO, "cases")
REVIEW3 = os.environ.get("SECOND_PASS_REVIEW3_EVIDENCE", os.path.join(
    os.path.expanduser("~"), "Documents", "Codex", "2026-09-12",
    "https-ainativeaccounting-org-https-ainativeaccounting-org", "outputs",
    "Second-Pass-Third-Review-Evidence-2026-09-13", "work", "review-v3-evidence"))


def load(version):
    case, why = f.CaseLibrary(CASES).lookup(version)
    if not case:
        raise AssertionError(why)
    return case


def why_cell(card, call, chips=None, words="", reason=None):
    if not card["basis_key"]:
        # a case filed before basis keys existed: the metadata half only
        return ("Line %d, account %s. Called: %s. Key: %s. Type: %s. %s"
                % (card["n"], card["acct"], call, card["key"], card["type"],
                   "Correct." if call == card["key"] else "Missed."))
    chips = chips if chips is not None else (card["basis_key"][:1] if call == card["key"]
                                             else ["no source on file"])
    agrees = f.reason_agrees(chips, card["basis_key"]) if reason is None else reason
    return ("Basis: %s | Words: %s || Line %d, account %s. Called: %s. Key: %s. Type: %s. %s "
            "Reason: %s. Key basis: %s."
            % ("; ".join(chips), words or "none", card["n"], card["acct"], call, card["key"],
               card["type"], "Correct." if call == card["key"] else "Missed.",
               "agrees" if agrees else "does not agree", "; ".join(card["basis_key"])))


def response(code, attempt, one, two=None, calls=None, ts="2026-09-15 10:00:00",
             line=None, fresh_calls=None, marker="", run_id=None, extra=None, posted=False):
    """One row the way index.html posts it, keyed from the named case versions."""
    case1 = load(one)
    cards = case1["cards"]
    calls = calls or [c["key"] for c in cards]
    r = {f.CODENAME_TITLE: code, f.TIMESTAMP_TITLE: ts,
         f.QB_TITLE: "Attempt id: %s, run 1 in this tab." % attempt}
    if line is None:
        if two:
            line = ("Case: %s, version %s (practice, %d lines) and %s (assessment, 5 lines), "
                    "dated 2026-09-13, loaded from cases/ files."
                    % (run_id or one.split("-")[0], one, len(cards), two))
        else:
            line = ("Case: %s, version %s (practice, %d lines), no fresh case, dated "
                    "2026-09-13, loaded from cases/ files." % (run_id or one.split("-")[0],
                                                               one, len(cards)))
    r[f.QA_TITLE] = "Organizations: ACFE. Product: second-pass-drill 1.6.1. " + line
    for i, card in enumerate(cards):
        r[f.WHY_TITLES[i]] = why_cell(card, calls[i], words=marker)
        if posted:
            r[f.CALL_TITLES[i]] = card["post_flag"] if calls[i] == "flag" else card["post_stand"]
    if two:
        case2 = load(two)
        letters = f.key_letters(case2)
        got = fresh_calls or letters
        right = sum(1 for a, b in zip(got, letters) if a == b)
        r[f.QC_TITLE] = ("Round2: right call %d/5, right reason 0/5; calls %s; key %s; seconds 60."
                         % (right, got, letters))
    if extra:
        r.update(extra)
    return r


class Folder(object):
    def __init__(self):
        self.path = tempfile.mkdtemp(prefix="findings-test-")

    def csv(self, name, rows):
        heads = list(dict.fromkeys(k for r in rows for k in r))
        path = os.path.join(self.path, name)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=heads)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def close(self):
        shutil.rmtree(self.path, ignore_errors=True)


class FindingsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Folder()

    def tearDown(self):
        self.tmp.close()

    def run_rows(self, rows, **kw):
        path = self.tmp.csv("responses.csv", rows)
        kw.setdefault("cases_dir", CASES)
        return f.analyze(path, **kw)

    # --- version routing -------------------------------------------------------
    def test_perfect_kestrel_scores_twelve_of_twelve(self):
        rows = [response("Kestrel Perfect", "att-k1", "kestrel-v1")]
        report = self.run_rows(rows)
        self.assertEqual(len(report["sets"]), 1)
        s = report["sets"][0]
        self.assertEqual(s["case1"]["version"], "kestrel-v1")
        a = s["attempts"][0]
        self.assertEqual((a["score"], len(a["answered"])), (12, 12))
        self.assertEqual(a["reason_right"], 12)
        self.assertEqual(report["disagreements"], [])

    def test_mixed_versions_are_scored_apart_against_their_own_keys(self):
        rows = [response("Hal One", "att-h1", "halyard-v4", "brightwater-v5"),
                response("Kes One", "att-k1", "kestrel-v1", "brightwater-v5")]
        report = self.run_rows(rows)
        labels = sorted(s["label"] for s in report["sets"])
        self.assertEqual(labels, ["halyard-v4 with brightwater-v5",
                                  "kestrel-v1 with brightwater-v5"])
        for s in report["sets"]:
            a = s["attempts"][0]
            self.assertEqual(a["score"], len(s["case1"]["cards"]))
            self.assertEqual(s["fresh"]["right"], 5)
        self.assertEqual(report["disagreements"], [])
        fields = f.readout_fields(report, "responses.csv")
        self.assertEqual(len(fields["sets"]), 2)

    def test_posted_column_decodes_by_the_case_post_mapping(self):
        # Halyard line 1 posts Reject for a flag; Kestrel line 1 posts Accept for a flag.
        hal = response("Hal Posted", "att-hp", "halyard-v4", posted=True)
        kes = response("Kes Posted", "att-kp", "kestrel-v1", posted=True)
        for r in (hal, kes):
            for title in f.WHY_TITLES:
                r.pop(title, None)
        self.assertEqual(hal[f.CALL_TITLES[0]], "Reject")
        self.assertEqual(kes[f.CALL_TITLES[0]], "Accept")
        report = self.run_rows([hal, kes])
        scores = {s["case1"]["version"]: s["attempts"][0]["score"] for s in report["sets"]}
        self.assertEqual(scores, {"halyard-v4": 14, "kestrel-v1": 12})

    def test_fresh_case_is_scored_against_its_own_recorded_version(self):
        v2 = load("brightwater-v2")
        rows = [response("Old Fresh", "att-of", "halyard-v3", "brightwater-v2",
                         fresh_calls=f.key_letters(v2))]
        report = self.run_rows(rows)
        s = report["sets"][0]
        self.assertEqual(s["case2"]["version"], "brightwater-v2")
        self.assertEqual(s["fresh"]["right"], 5)
        self.assertNotEqual(f.key_letters(v2), f.key_letters(load("brightwater-v5")))

    def test_record_key_that_contradicts_the_case_file_is_reported(self):
        r = response("Wrong Key", "att-wk", "kestrel-v1")
        halyard_line_three = load("halyard-v4")["cards"][2]
        r[f.WHY_TITLES[2]] = why_cell(halyard_line_three, "flag")
        report = self.run_rows([r])
        self.assertTrue(any("Why names account 5100" in d for d in report["disagreements"]))
        self.assertTrue(any("key is flag, kestrel-v1 carries stand" in d
                            for d in report["disagreements"]))

    # --- refusals --------------------------------------------------------------
    def test_unknown_version_is_refused_and_never_scored(self):
        rows = [response("Future Key", "att-fk", "halyard-v4",
                         line="Case: halyard, version halyard-v99 (practice, 14 lines), no "
                              "fresh case, dated 2026-12-01, loaded from cases/ files.")]
        report = self.run_rows(rows)
        self.assertEqual(report["sets"], [])
        self.assertEqual(len(report["refused"]), 1)
        self.assertIn("unsupported case version halyard-v99", report["refused"][0]["refusal"])
        self.assertEqual(report["initial"], [])
        self.assertEqual(report["n_attempts_received"], 1)

    def test_unknown_fresh_version_refuses_the_attempt(self):
        rows = [response("Future Fresh", "att-ff", "halyard-v4", "brightwater-v5",
                         line="Case: halyard, version halyard-v4 (practice, 14 lines) and "
                              "brightwater-v99 (assessment, 5 lines), dated 2026-09-13, loaded "
                              "from cases/ files.")]
        report = self.run_rows(rows)
        self.assertEqual(report["sets"], [])
        self.assertIn("brightwater-v99", report["refused"][0]["refusal"])

    def test_authored_case_and_missing_case_line_are_refused(self):
        own = response("Own Case", "att-oc", "halyard-v4",
                       line="Case: own:Ridgeline:2, version halyard-v4 (practice, 14 lines), no "
                            "fresh case, dated 2026-09-13, loaded from this browser, written by "
                            "author.html.")
        none = response("No Line", "att-nl", "halyard-v4")
        none[f.QA_TITLE] = "Organizations: ACFE."
        report = self.run_rows([own, none])
        reasons = sorted(a["refusal"] for a in report["refused"])
        self.assertEqual(len(reasons), 2)
        self.assertTrue(any(r.startswith("authored case own:Ridgeline:2") for r in reasons))
        self.assertIn("no case version recorded in question A", reasons)
        self.assertEqual(report["sets"], [])

    def test_no_cases_directory_refuses_rather_than_guessing(self):
        rows = [response("Kestrel Perfect", "att-k1", "kestrel-v1")]
        path = self.tmp.csv("responses.csv", rows)
        report = f.analyze(path, cases_dir=os.path.join(self.tmp.path, "no-such-dir"))
        self.assertEqual(report["sets"], [])
        self.assertIn("no cases directory found", report["refused"][0]["refusal"])

    def test_case_file_whose_inner_version_differs_is_refused(self):
        folder = os.path.join(self.tmp.path, "cases")
        os.makedirs(folder)
        with open(os.path.join(CASES, "kestrel-v1.json"), encoding="utf-8") as handle:
            data = json.load(handle)
        data["version"] = "kestrel-v1"
        with open(os.path.join(folder, "kestrel-v2.json"), "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        rows = [response("Renamed File", "att-rf", "kestrel-v1",
                         line="Case: kestrel, version kestrel-v2 (practice, 12 lines), no "
                              "fresh case, dated 2026-09-13, loaded from cases/ files.")]
        report = self.run_rows(rows, cases_dir=folder)
        self.assertIn("carries version 'kestrel-v1' inside it", report["refused"][0]["refusal"])

    # --- attempts and people ---------------------------------------------------
    def test_two_attempts_by_one_codename(self):
        rows = [response("Same Person", "att-a", "halyard-v4", ts="2026-09-15 10:00:00"),
                response("Same Person", "att-b", "halyard-v4", ts="2026-09-15 11:00:00")]
        report = self.run_rows(rows)
        self.assertEqual(report["n_attempts_received"], 2)
        self.assertEqual(report["n_attempts_completed"], 2)
        self.assertEqual(report["n_codenames"], 1)
        self.assertEqual(len(report["initial"]), 1)
        self.assertEqual(len(report["reattempts"]), 1)
        self.assertEqual(report["initial"][0]["attempt_id"], "att-a")
        self.assertEqual(report["reattempts"][0]["attempt_number"], 2)
        self.assertEqual(report["sets"][0]["n_attempts"], 1)
        run = dict(f.readout_fields(report, "responses.csv")["run"])
        self.assertEqual((run["run.attempts_received"], run["run.codenames_distinct"],
                          run["run.first_attempts"], run["run.reattempts"]), (2, 1, 1, 1))
        self.assertIsNone(run["run.participants_confirmed"])

    def test_first_attempt_follows_the_timestamp_not_the_file_order(self):
        rows = [response("Late Row", "att-late", "halyard-v4", ts="2026/09/15 12:00:00"),
                response("Late Row", "att-early", "halyard-v4", ts="2026/09/15 9:00:00")]
        report = self.run_rows(rows)
        self.assertEqual(report["order_basis"], "timestamp")
        self.assertEqual(report["initial"][0]["attempt_id"], "att-early")

    def test_same_attempt_sent_twice_counts_once(self):
        rows = [response("Retry Sender", "att-r", "halyard-v4"),
                response("Retry Sender", "att-r", "halyard-v4")]
        report = self.run_rows(rows)
        self.assertEqual(report["n_attempts_received"], 1)
        self.assertEqual(len(report["duplicate_sends"]), 1)
        self.assertEqual(report["reattempts"], [])

    def test_incomplete_attempt_is_received_but_not_completed(self):
        r = response("Half Done", "att-h", "halyard-v4")
        for title in f.WHY_TITLES[7:]:
            r[title] = ""
        report = self.run_rows([r])
        self.assertEqual(report["n_attempts_received"], 1)
        self.assertEqual(report["n_attempts_completed"], 0)

    def test_roster_confirms_consented_participants_only(self):
        rows = [response("Alpha One", "att-1", "halyard-v4"),
                response("Alpha Two", "att-2", "kestrel-v1"),
                response("Bravo", "att-3", "halyard-v4"),
                response("Charlie", "att-4", "halyard-v4"),
                response("Unlisted", "att-5", "halyard-v4")]
        roster = self.tmp.csv("roster.csv", [
            {"participant": "P01", "codename": "Alpha One", "consent": "yes", "role": "student"},
            {"participant": "P01", "codename": "alpha two", "consent": "Yes", "role": "student"},
            {"participant": "P02", "codename": "Bravo", "consent": "yes", "role": "practitioner"},
            {"participant": "P03", "codename": "Charlie", "consent": "no", "role": "student"},
            {"participant": "P04", "codename": "Never Played", "consent": "yes", "role": ""},
        ])
        report = self.run_rows(rows, roster_path=roster)
        r = report["roster"]
        self.assertEqual(report["n_participants_confirmed"], 2)
        self.assertEqual(sorted(r["confirmed"]), ["P01", "P02"])
        self.assertEqual(r["rows_without_consent"], 1)
        self.assertEqual(r["roster_codenames_without_attempt"], 1)
        self.assertEqual(r["attempt_codenames_not_on_roster"], 2)
        self.assertEqual(r["roles"], {"practitioner": 1, "student": 1})
        self.assertEqual(report["n_codenames"], 5)
        hal = [s for s in report["sets"] if s["case1"]["version"] == "halyard-v4"][0]
        self.assertEqual(hal["participants_confirmed"], 2)

    def test_roster_codename_claimed_twice_is_not_confirmed(self):
        rows = [response("Shared Name", "att-1", "halyard-v4")]
        roster = self.tmp.csv("roster.csv", [
            {"participant": "P01", "codename": "Shared Name", "consent": "yes"},
            {"participant": "P02", "codename": "Shared Name", "consent": "yes"}])
        report = self.run_rows(rows, roster_path=roster)
        self.assertEqual(report["n_participants_confirmed"], 0)
        self.assertEqual(report["roster"]["codename_conflicts"], ["shared name"])

    def test_roster_without_required_columns_is_rejected(self):
        roster = self.tmp.csv("roster.csv", [{"participant": "P01", "name": "x"}])
        with self.assertRaises(f.RosterError):
            self.run_rows([response("Anyone", "att-1", "halyard-v4")], roster_path=roster)

    # --- exclusions ------------------------------------------------------------
    def test_synthetic_and_test_rows_are_excluded_with_counts(self):
        rows = [response("Synthetic Kestrel participant", "att-s1", "kestrel-v1"),
                response("Quiet Heron", "audit-c", "kestrel-v1"),
                response("Marked Words", "att-s3", "kestrel-v1", marker="Synthetic test only"),
                response("Test Play", "att-t1", "halyard-v4"),
                response("Field Check", "att-t2", "halyard-v4"),
                response("", "att-t3", "halyard-v4"),
                response("Real Player", "att-ok", "halyard-v4")]
        rows[4][f.QA_TITLE] += " TEST ATTEMPT, exclude from reports."
        report = self.run_rows(rows)
        counts = {k: len(v) for k, v in report["excluded"].items()}
        self.assertEqual(counts, {"synthetic_by_rule": 3, "test_codename": 1,
                                  "marked_test_by_page": 1, "blank_codename": 1})
        self.assertEqual(report["n_excluded"], 6)
        self.assertEqual(report["n_attempts_received"], 1)
        run = dict(f.readout_fields(report, "responses.csv")["run"])
        self.assertEqual(run["run.rows_excluded.synthetic_by_rule"], 3)
        text = f.build_markdown(report, "responses.csv")
        self.assertIn("Synthetic row, excluded by rule: 3", text)

    def test_codename_words_that_merely_contain_test_are_kept(self):
        report = self.run_rows([response("Contest Falcon", "att-cf", "halyard-v4"),
                                response("Audit Hawk", "att-ah", "halyard-v4")])
        self.assertEqual(report["n_excluded"], 0)
        self.assertEqual(report["n_attempts_received"], 2)

    def test_synthetic_check_scores_synthetic_rows_and_stamps_the_output(self):
        rows = [response("Synthetic Kestrel participant", "audit-c", "kestrel-v1",
                         marker="Synthetic test only")]
        report = self.run_rows(rows, synthetic_check=True)
        self.assertEqual(report["n_excluded"], 0)
        self.assertEqual(report["initial"][0]["score"], 12)
        text = f.build_markdown(report, "probe.csv")
        self.assertIn("Synthetic verification run. Not participant evidence.", text)
        run = dict(f.readout_fields(report, "probe.csv")["run"])
        self.assertIn("not participant evidence", run["run.evidence_status"])

    # --- reason chip agreement -------------------------------------------------
    def test_fresh_case_reason_limitation_is_stated(self):
        lim = f.reason_limitation(load("brightwater-v5"))
        self.assertEqual((lim["flags_no_source"], lim["flags"], lim["stands_hold_only"],
                          lim["stands"]), (3, 3, 2, 2))
        self.assertIn("three of the three flag lines accept \"no source on file\"", lim["text"])
        self.assertIn("not as reasoning quality", lim["text"])

    def test_readout_labels_never_call_counts_players(self):
        rows = [response("Label Check", "att-lc", "halyard-v4", "brightwater-v5")]
        report = self.run_rows(rows)
        fields = f.readout_fields(report, "responses.csv")
        names = [n for n, _ in fields["run"]] + [n for _, vals in fields["sets"] for n, _ in vals]
        self.assertFalse([n for n in names if "player" in n])
        self.assertFalse([n for n in names if "right_reason" in n])
        text = f.build_markdown(report, "responses.csv")
        self.assertNotIn("Distinct players", text)
        self.assertIn("game rank, not a credential", text)
        self.assertIn("does not establish learning gain", text)

    # --- the shipped sample and the review's own files -------------------------
    def test_sample_builds_end_to_end(self):
        sample = os.path.join(TOOLS, "findings-sample.csv")
        roster = os.path.join(TOOLS, "findings-sample-roster.csv")
        if not os.path.exists(sample):
            self.skipTest("findings-sample.csv not built")
        report = f.analyze(sample, roster_path=roster, cases_dir=CASES)
        self.assertEqual(report["n_excluded"], 6)
        self.assertEqual(len(report["reattempts"]), 1)
        self.assertEqual(len(report["refused"]), 2)
        self.assertGreaterEqual(len(report["sets"]), 2)
        out = f.build_markdown(report, sample) + f.fields_block(
            f.readout_fields(report, sample), report["missing"])
        self.assertIn("## Case set kestrel-v1 with brightwater-v5", out)

    def review_file(self, name):
        path = os.path.join(REVIEW3, name)
        if not os.path.exists(path):
            self.skipTest("third review evidence folder not on this machine")
        return path

    def test_review_kestrel_perfect_file(self):
        path = self.review_file("kestrel-perfect.csv")
        default = f.analyze(path, cases_dir=CASES)
        self.assertEqual(default["excluded"]["synthetic_by_rule"],
                         ["Synthetic Kestrel participant (codename says synthetic)"])
        self.assertEqual(default["initial"], [])
        checked = f.analyze(path, cases_dir=CASES, synthetic_check=True)
        a = checked["initial"][0]
        self.assertEqual((a["score"], len(a["answered"])), (12, 12))
        self.assertEqual(checked["sets"][0]["case1"]["version"], "kestrel-v1")
        self.assertEqual(checked["disagreements"], [])

    def test_review_two_attempt_file(self):
        path = self.review_file("same-person-two-attempts.csv")
        default = f.analyze(path, cases_dir=CASES)
        self.assertEqual(len(default["excluded"]["synthetic_by_rule"]), 2)
        checked = f.analyze(path, cases_dir=CASES, synthetic_check=True)
        self.assertEqual(checked["n_attempts_received"], 2)
        self.assertEqual(checked["n_codenames"], 1)
        self.assertEqual(len(checked["initial"]), 1)
        self.assertEqual(len(checked["reattempts"]), 1)
        self.assertEqual(checked["initial"][0]["score"], 14)


def fixture_cases(folder):
    """cases/ plus a brightwater-v6.json built from v5 with the same key and a marked memo,
    so a test can see which file a row was routed to. Lane R3 ships the real v6; once it is in
    cases/ the copy from cases/ is used and only the marked memo check is skipped."""
    target = os.path.join(folder, "cases")
    shutil.copytree(CASES, target)
    v6 = os.path.join(target, "brightwater-v6.json")
    if not os.path.exists(v6):
        with open(os.path.join(CASES, "brightwater-v5.json"), encoding="utf-8") as handle:
            data = json.load(handle)
        data["version"] = "brightwater-v6"
        for card in data["cards"]:
            card["memo"] = "V6 FIXTURE. " + card["memo"]
        with open(v6, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
    return target


def explained(code, attempt, fresh="brightwater-v6", ts="2026-09-20 10:00:00", texts=None,
              words=False):
    """A brightwater-v6 run with question C written the way r2Line() writes it in 6447d97."""
    r = response(code, attempt, "halyard-v4", fresh, ts=ts)
    case2 = load(fresh)
    texts = texts or {}
    lines = []
    for n, card in enumerate(case2["cards"], start=1):
        parts = texts.get(n, {"evidence": "the document on line %d" % n,
                              "period": "the month it covers on line %d" % n,
                              "action": "the request that follows on line %d" % n})
        chips = card["basis_key"][:1]
        lines.append("%d: Basis: %s%s | Evidence: %s | Period: %s | Action: %s | Reason: agrees "
                     "| Key basis: %s"
                     % (n, "; ".join(chips), " | Words: short note" if words else "",
                        parts.get("evidence") or "none", parts.get("period") or "none",
                        parts.get("action") or "none", "; ".join(card["basis_key"])))
    r[f.QC_TITLE] += (" Round2 basis, by line: " + " || ".join(lines) + ". Fresh case: "
                      "Brightwater Dental Partners, PLLC, case version %s, 5 lines." % fresh)
    return r


class ExplanationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Folder()
        self.cases = fixture_cases(self.tmp.path)

    def tearDown(self):
        self.tmp.close()

    def run_rows(self, rows, **kw):
        path = self.tmp.csv("responses.csv", rows)
        return f.analyze(path, cases_dir=self.cases, **kw)

    def read_csv(self, path):
        with open(path, encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_brightwater_v6_routes_to_its_own_file_and_v5_stays_on_v5(self):
        rows = [response("On Five", "att-5", "halyard-v4", "brightwater-v5"),
                explained("On Six", "att-6")]
        report = self.run_rows(rows)
        fresh = {s["case2"]["version"]: s for s in report["sets"]}
        self.assertEqual(sorted(fresh), ["brightwater-v5", "brightwater-v6"])
        self.assertEqual(fresh["brightwater-v6"]["case2"]["path"], "cases/brightwater-v6.json")
        self.assertEqual(fresh["brightwater-v5"]["case2"]["path"], "cases/brightwater-v5.json")
        self.assertEqual(fresh["brightwater-v5"]["fresh"]["right"], 5)
        self.assertEqual(fresh["brightwater-v6"]["fresh"]["right"], 5)
        self.assertEqual(fresh["brightwater-v5"]["explain"]["items"], 0)
        self.assertEqual(fresh["brightwater-v6"]["explain"]["items"], 5)
        v6_memo = fresh["brightwater-v6"]["case2"]["cards"][0]["memo"]
        v5_memo = fresh["brightwater-v5"]["case2"]["cards"][0]["memo"]
        if v6_memo.startswith("V6 FIXTURE."):
            self.assertFalse(v5_memo.startswith("V6 FIXTURE."))

    def test_scoring_sheet_is_blind_and_the_key_joins_on_response_id(self):
        rows = [explained("Hidden Name", "att-a"), explained("Other Name", "att-b"),
                response("On Five", "att-5", "halyard-v4", "brightwater-v5")]
        rows[0][f.QC_TITLE] = rows[0][f.QC_TITLE].replace("calls FSFFS", "calls SSFFS")
        report = self.run_rows(rows)
        sheet = os.path.join(self.tmp.path, "sheet.csv")
        key = os.path.join(self.tmp.path, "key.csv")
        self.assertEqual(f.write_scoring_sheet(report, sheet, key), 10)
        with open(sheet, encoding="utf-8") as handle:
            raw = handle.read()
        for leak in ("Hidden Name", "att-a", "agrees", "keyed", "no source on file", "codename"):
            self.assertNotIn(leak, raw)
        rows_sheet = self.read_csv(sheet)
        self.assertEqual(list(rows_sheet[0].keys()), f.SHEET_COLUMNS)
        self.assertEqual([r["line"] for r in rows_sheet], sorted(r["line"] for r in rows_sheet))
        self.assertTrue(all(r["case_version"] == "brightwater-v6" for r in rows_sheet))
        self.assertTrue(all(r["memo_sentence"] for r in rows_sheet))
        rows_key = {r["response_id"]: r for r in self.read_csv(key)}
        self.assertEqual(set(rows_key), {r["response_id"] for r in rows_sheet})
        hidden_line1 = [r for r in rows_key.values()
                        if r["codename"] == "Hidden Name" and r["line"] == "1"][0]
        self.assertEqual(hidden_line1["participant_call"], "stand")
        self.assertEqual(hidden_line1["keyed_call"], "flag")
        self.assertEqual(hidden_line1["call_result"], "does not agree with key")
        self.assertEqual(hidden_line1["attempt"], "first")

    def test_explanations_and_chips_are_both_read_from_question_c(self):
        texts = {2: {"evidence": "the June register", "period": "", "action": "sign it"}}
        report = self.run_rows([explained("Question C", "att-q", texts=texts, words=True)])
        a = report["initial"][0]
        self.assertEqual(sorted(a["explanations"]), [1, 2, 3, 4, 5])
        self.assertEqual(a["explanations"][3]["period"], "the month it covers on line 3")
        self.assertEqual(a["explanations"][5]["action"], "the request that follows on line 5")
        self.assertEqual(a["explanations"][2], {"evidence": "the June register",
                                                "action": "sign it"})
        self.assertEqual([r[1] for r in a["r2_basis"]],
                         [["no source on file"], ["the figure and reason hold"],
                          ["wrong period"], ["no source on file"],
                          ["the figure and reason hold"]])
        self.assertEqual([r[2] for r in a["r2_basis"]], ["short note"] * 5)
        self.assertTrue(all(r[3] for r in a["r2_basis"]))

    def test_second_scorer_draw_is_stable_and_reaches_every_line(self):
        rows = [explained("Writer %02d" % k, "att-w%02d" % k) for k in range(12)]
        first = self.run_rows(rows)["explanation_items"]
        for n in range(1, 6):
            self.assertGreaterEqual(sum(1 for i in first if i["line"] == n and i["second"]), 2)
        by_hash = {i["response_id"] for i in first
                   if i["draw"] % f.SECOND_SCORER_MODULUS == 0}
        more = rows + [explained("Writer %02d" % k, "att-w%02d" % k) for k in range(12, 30)]
        again = {i["response_id"]: i for i in self.run_rows(more)["explanation_items"]}
        self.assertTrue(all(again[rid]["second"] for rid in by_hash))
        self.assertEqual(len(again), 150)

    def test_scores_merge_into_a_separate_result_with_second_scorer_agreement(self):
        rows = [explained("Writer %02d" % k, "att-w%02d" % k) for k in range(4)]
        report = self.run_rows(rows)
        sheet = os.path.join(self.tmp.path, "sheet.csv")
        f.write_scoring_sheet(report, sheet, os.path.join(self.tmp.path, "key.csv"))
        blank = self.read_csv(sheet)
        filled, second = [], []
        for k, r in enumerate(blank):
            one = dict(r, score_evidence="2", score_period="1", score_action="2", scorer="E1")
            if k == 0:
                one["key_disagreement"] = "The 31 May schedule could support a stand."
            if k == 1:
                one["score_action"] = "3"
            filled.append(one)
            if r["second_scorer"] == "yes":
                second.append(dict(r, score_evidence="2", score_period="2", score_action="2",
                                   scorer="E2"))
        first_path = self.tmp.csv("first.csv", filled)
        second_path = self.tmp.csv("second.csv", second)
        report = self.run_rows(rows, scores_path=first_path, second_scores_path=second_path)
        e = report["sets"][0]["explain"]
        self.assertEqual(e["items"], 20)
        self.assertEqual(e["scored"], 19)
        self.assertAlmostEqual(e["evidence_avg"], 2.0)
        self.assertAlmostEqual(e["period_avg"], 1.0)
        self.assertAlmostEqual(e["total_avg"], 5.0)
        drawn_scored = sum(1 for i in report["explanation_items"]
                           if i["second"] and i["first_scores"]["scores"])
        self.assertEqual(e["double_scored"], drawn_scored)
        self.assertAlmostEqual(e["exact_rate"], 100.0 * 2 / 3)
        self.assertAlmostEqual(e["within_one_rate"], 100.0)
        self.assertEqual(len(e["key_disagreements"]), 1)
        self.assertEqual(report["scores"]["invalid_rows"], 1)
        fields = dict(f.readout_fields(report, "responses.csv")["sets"][0][1])
        self.assertAlmostEqual(fields["explain.total_avg_of_6"], 5.0)
        self.assertEqual(f.fmt_field(fields["explain.total_avg_of_6"],
                                     "explain.total_avg_of_6"), "5")
        self.assertIn("explain.second_exact_agreement_rate", fields)
        self.assertIn("reason.limitation", fields)
        text = f.build_markdown(report, "responses.csv")
        self.assertIn("### Educator-scored explanations", text)
        self.assertIn("A separate result from reason chip agreement", text)
        self.assertIn("do not establish learning gain", text)
        self.assertIn("The 31 May schedule could support a stand.", text)

    def test_scored_sheet_without_score_columns_is_rejected(self):
        rows = [explained("Writer", "att-w")]
        bad = self.tmp.csv("bad.csv", [{"response_id": "R1", "total": "5"}])
        with self.assertRaises(f.InputError):
            self.run_rows(rows, scores_path=bad)


if __name__ == "__main__":
    unittest.main(verbosity=1)
