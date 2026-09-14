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
                # an attempt id beginning audit- is no marker on its own since 13 September
                response("Quiet Heron", "audit-c", "kestrel-v1"),
                response("Marked Words", "att-s3", "kestrel-v1", marker="Synthetic test only"),
                response("Test Play", "att-t1", "halyard-v4"),
                response("Field Check", "att-t2", "halyard-v4"),
                response("", "att-t3", "halyard-v4"),
                response("Real Player", "att-ok", "halyard-v4")]
        rows[4][f.QA_TITLE] += " TEST ATTEMPT, exclude from reports."
        report = self.run_rows(rows)
        counts = {k: len(v) for k, v in report["excluded"].items()}
        self.assertEqual(counts, {"synthetic_by_rule": 2, "test_codename": 1,
                                  "marked_test_by_page": 1, "blank_codename": 1})
        self.assertEqual(report["n_excluded"], 5)
        self.assertEqual(sorted(a["codename"] for a in report["attempts"]),
                         ["Quiet Heron", "Real Player"])
        run = dict(f.readout_fields(report, "responses.csv")["run"])
        self.assertEqual(run["run.rows_excluded.synthetic_by_rule"], 2)
        text = f.build_markdown(report, "responses.csv")
        self.assertIn("Synthetic row, excluded by rule: 2", text)
        # every exclusion names its sheet row and its rule
        self.assertIn("Test Play (sheet row 5, rule: a known test codename)", text)
        self.assertIn("Field Check (sheet row 6, rule: the page marked it TEST ATTEMPT)", text)
        self.assertIn("Marked Words (sheet row 4, rule: a cell or a Words line reads Synthetic "
                      "test only)", text)

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
        self.assertEqual(len(report["duplicate_sends"]), 1)
        self.assertEqual([c["attempt_id"] for c in report["conflicts"]], ["att-twinlark-01"])
        self.assertIn("Test Pilot", [a["codename"] for a in report["attempts"]])
        signoff = [a for a in report["attempts"] if a["codename"] == "SIGNOFF"][0]
        self.assertFalse(signoff["completed"])
        self.assertEqual(len(signoff["explanation_gaps"]), 3)
        out = f.build_markdown(report, sample) + f.fields_block(
            f.readout_fields(report, sample), report["missing"])
        self.assertIn("## Case set kestrel-v1 with brightwater-v5", out)
        self.assertIn("**Unresolved: attempt att-twinlark-01**", out)

    def review_file(self, name):
        path = os.path.join(REVIEW3, name)
        if not os.path.exists(path):
            self.skipTest("third review evidence folder not on this machine")
        return path

    def test_review_kestrel_perfect_file(self):
        path = self.review_file("kestrel-perfect.csv")
        default = f.analyze(path, cases_dir=CASES)
        self.assertEqual(default["excluded"]["synthetic_by_rule"],
                         ["Synthetic Kestrel participant (sheet row 2, rule: the codename "
                          "begins with Synthetic)"])
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
        # every posted part is kept as written, the page's "none" for an empty box included
        self.assertEqual(a["explanations"][2], {"evidence": "the June register",
                                                "period": "none", "action": "sign it"})
        self.assertEqual([(g["line"], g["part"], g["problem"]) for g in a["explanation_gaps"]],
                         [(2, "period", "stock"), (2, "action", "short")])
        self.assertFalse(a["completed"])
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


def keyed_calls(version, off=()):
    """The key's call on every line, turned over on the zero-based lines named in off."""
    out = []
    for i, card in enumerate(load(version)["cards"]):
        call = card["key"]
        if i in off:
            call = "stand" if call == "flag" else "flag"
        out.append(call)
    return out


def read_cell(version, picks, calls, late=False, counts=None, letters=None):
    """The round one cell the way prepickLine() in index.html writes the required read."""
    cards = load(version)["cards"]
    read = ["flag" if c["acct"] in picks else "stand" for c in cards]
    toward = away = held = 0
    for r, final, card in zip(read, calls, cards):
        if final == r:
            held += 1
        elif final == card["key"]:
            toward += 1
        else:
            away += 1
    counts = counts or (toward, away, held)
    letters = letters or "".join("F" if r == "flag" else "S" for r in read)
    cell = ("Prepicks: %s. Required read before the AI draft, case %s, by line, F tapped for a "
            "second look and S left untapped: %s. Final calls after the draft: %s. Against the "
            "key: %d changed toward it, %d changed away from it, %d held."
            % ("; ".join(picks), version, letters,
               "".join("F" if c == "flag" else "S" for c in calls),
               counts[0], counts[1], counts[2]))
    if late:
        cell += " Taken after a call was locked, so not a read before the draft."
    return cell


def with_read(code, attempt, version, picks, off=(), ts="2026-09-15 10:00:00", **kw):
    calls = keyed_calls(version, off)
    cell = kw.pop("cell", None) or read_cell(version, picks, calls, **kw)
    return response(code, attempt, version, calls=calls, ts=ts, extra={f.ROUND1_TITLE: cell})


class PrepickTest(unittest.TestCase):
    """The required read before the draft, set against the final calls in the findings."""

    def setUp(self):
        self.tmp = Folder()

    def tearDown(self):
        self.tmp.close()

    def run_rows(self, rows, **kw):
        path = self.tmp.csv("responses.csv", rows)
        kw.setdefault("cases_dir", CASES)
        return f.analyze(path, **kw)

    def test_cell_shapes_parse_old_and_required(self):
        old = f.parse_prepicks("Prepicks: 4200; 6000; 6400.")
        self.assertEqual((old["picks"], old["required"]), (["4200", "6000", "6400"], False))
        self.assertTrue(f.parse_prepicks("Prepicks: skipped.")["skipped"])
        self.assertTrue(f.parse_prepicks("Prepicks: not recorded.")["not_recorded"])
        self.assertIsNone(f.parse_prepicks(""))
        cell = read_cell("halyard-v4", ["4200", "4000"], keyed_calls("halyard-v4"), late=True)
        new = f.parse_prepicks(cell)
        self.assertEqual(new["picks"], ["4200", "4000"])
        self.assertTrue(new["required"] and new["late"])
        self.assertEqual(new["version"], "halyard-v4")
        self.assertEqual(new["read"], "FSSSSSFSSSSFSS")
        self.assertEqual(new["posted"], (5, 0, 9))

    def test_required_read_is_set_against_final_calls_toward_away_and_held(self):
        # line 5 is a clean line called flag: untapped before the draft, flagged after it
        rows = [with_read("NORTHSTAR", "att-n1", "halyard-v4", ["4200", "6200", "4100"], off=(4,)),
                with_read("TIEOUT", "att-t1", "halyard-v4", ["6000"])]
        report = self.run_rows(rows)
        self.assertEqual(report["disagreements"], [])
        one = next(a for a in report["initial"] if a["codename"] == "NORTHSTAR")
        self.assertEqual((one["read"]["toward"], one["read"]["away"], one["read"]["held"]),
                         (7, 1, 6))
        self.assertEqual(one["read"]["moves"][3], "toward")    # tapped, then let stand, key stand
        self.assertEqual(one["read"]["moves"][4], "away")      # untapped, then flagged, key stand
        self.assertEqual(one["read"]["moves"][0], "held")
        r = report["sets"][0]["read"]
        self.assertEqual((r["n"], r["changed_any"], r["compared"], r["changed"], r["toward"],
                          r["away"], r["held"]), (2, 2, 28, 15, 14, 1, 13))
        line5 = r["per_line"][4]
        self.assertEqual((line5["compared"], line5["tapped"], line5["away"], line5["held"]),
                         (2, 0, 1, 1))
        line11 = r["per_line"][10]
        self.assertEqual((line11["tapped"], line11["held"], line11["toward"]), (1, 1, 1))
        fields = dict(f.readout_fields(report, "responses.csv")["sets"][0][1])
        self.assertEqual(fields["prepick.first_attempts_with_read"], 2)
        self.assertEqual(fields["prepick.lines_changed"], 15)
        self.assertAlmostEqual(fields["prepick.changed_toward_key_rate"], 100.0 * 14 / 15)
        self.assertEqual(f.fmt_field(fields["prepick.lines_changed_rate"],
                                     "prepick.lines_changed_rate"), "53.6%")
        self.assertNotIn("r1.prepicks_given", fields)

    def test_first_attempts_only_and_each_case_version_apart(self):
        rows = [with_read("REDLINE", "att-r1", "halyard-v4", ["6000"], ts="2026-09-15 09:00:00"),
                # a reattempt by the same codename, with a different read: in no count
                with_read("REDLINE", "att-r2", "halyard-v4", ["4100"], off=(0, 1, 2),
                          ts="2026-09-15 11:00:00"),
                with_read("KITE", "att-k1", "kestrel-v1", ["4100"], ts="2026-09-15 10:00:00")]
        report = self.run_rows(rows)
        self.assertEqual(len(report["reattempts"]), 1)
        by_version = {s["case1"]["version"]: s["read"] for s in report["sets"]}
        self.assertEqual(by_version["halyard-v4"]["n"], 1)
        self.assertEqual((by_version["halyard-v4"]["toward"], by_version["halyard-v4"]["away"],
                          by_version["halyard-v4"]["held"]), (7, 0, 7))
        # kestrel-v1 carries account 4100 on lines 4 and 8, both keyed flag, so one tap reads
        # as a flag on both
        kestrel = by_version["kestrel-v1"]
        self.assertEqual((kestrel["n"], kestrel["toward"], kestrel["away"], kestrel["held"]),
                         (1, 5, 0, 7))
        self.assertEqual((kestrel["per_line"][3]["tapped"], kestrel["per_line"][7]["tapped"]),
                         (1, 1))
        self.assertEqual(report["disagreements"], [])

    def test_optional_era_late_and_missing_reads_enter_no_count(self):
        calls = keyed_calls("halyard-v4")
        rows = [with_read("ONE", "att-1", "halyard-v4", ["4200"]),
                with_read("TWO", "att-2", "halyard-v4", [], cell="Prepicks: 4200; 6000; 6400."),
                with_read("THREE", "att-3", "halyard-v4", [], cell="Prepicks: skipped."),
                with_read("FOUR", "att-4", "halyard-v4", ["6000"], late=True),
                response("FIVE", "att-5", "halyard-v4", calls=calls)]
        report = self.run_rows(rows)
        r = report["sets"][0]["read"]
        self.assertEqual((r["n"], r["n_before_required"], r["n_late"], r["n_missing"]),
                         (1, 2, 1, 1))
        self.assertEqual(r["compared"], 14)
        fields = dict(f.readout_fields(report, "responses.csv")["sets"][0][1])
        self.assertEqual(fields["prepick.first_attempts_before_required"], 2)
        self.assertEqual(fields["prepick.first_attempts_read_after_a_call"], 1)
        text = f.build_markdown(report, "responses.csv")
        self.assertIn("two posted before the read was required; one locked in after a call; "
                      "one with no read in the round one question", text)

    def test_posted_letters_and_counts_are_checked_and_the_case_file_decides(self):
        calls = keyed_calls("halyard-v4")
        bad = read_cell("halyard-v4", ["4200"], calls, counts=(9, 0, 5), letters="SSSSSSSSSSSSSS")
        report = self.run_rows([with_read("DRIFT", "att-d", "halyard-v4", ["4200"], cell=bad)])
        a = report["initial"][0]
        self.assertEqual((a["read"]["toward"], a["read"]["away"], a["read"]["held"]), (7, 0, 7))
        joined = " ".join(report["disagreements"])
        self.assertIn("the page posted the read SSSSSSSSSSSSSS", joined)
        self.assertIn("the page posted 9 toward, 0 away and 5 held", joined)

    def test_no_read_block_says_so_and_labels_never_claim_learning(self):
        rows = [with_read("LABEL", "att-l", "halyard-v4", ["7100", "6400"], off=(3,))]
        report = self.run_rows(rows)
        text = f.build_markdown(report, "responses.csv")
        self.assertIn("### The read before the draft, against the final calls", text)
        self.assertIn("Descriptive agreement on a keyed exercise, first attempts only.", text)
        self.assertIn("it is not a learning gain", text)
        self.assertNotIn("learning gain from", text.lower())
        names = [n for _, vals in f.readout_fields(report, "responses.csv")["sets"]
                 for n, _ in vals if n.startswith("prepick.")]
        self.assertEqual(len(names), 13)
        self.assertFalse([n for n in names if "player" in n or "gain" in n or "learn" in n])
        empty = self.run_rows([response("NOREAD", "att-x", "halyard-v4")])
        self.assertIn("No first attempt on this case set carries the required read",
                      f.build_markdown(empty, "responses.csv"))
        fields = dict(f.readout_fields(empty, "responses.csv")["sets"][0][1])
        self.assertIsNone(fields["prepick.lines_changed_rate"])
        self.assertEqual(f.fmt_field(fields["prepick.lines_changed"], "prepick.lines_changed"),
                         "not available")


AUDIT_INPUTS = os.path.join(REPO, "audit", "independent-2026-09-13", "inputs", "findings")
VECTORS = os.path.join(HERE, "explanation-minimum.json")


def audit_input(test, name):
    """One of the independent audit's own synthetic CSVs, or a skip where the folder is absent."""
    path = os.path.join(AUDIT_INPUTS, name)
    if not os.path.exists(path):
        test.skipTest("audit/independent-2026-09-13 inputs not on this machine")
    return path


def csv_cells(path):
    with open(path, encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return rows[0], rows[1:]


class SheetSafetyTest(unittest.TestCase):
    """Item 1: nothing findings.py writes to a CSV runs as a formula when a spreadsheet opens it."""

    LEADS = ("=", "+", "-", "@", "\t", "\r", "\n", chr(0xff1d), chr(0xff0b), chr(0xff0d),
             chr(0xff20))

    def setUp(self):
        self.tmp = Folder()

    def tearDown(self):
        self.tmp.close()

    def assert_safe(self, path, numeric):
        heads, rows = csv_cells(path)
        self.assertTrue(rows)
        for row in rows:
            for head, value in zip(heads, row):
                if head in numeric:
                    self.assertRegex(value, r"^(-?\d+(\.\d+)?)?$", "%s holds %r" % (head, value))
                else:
                    self.assertFalse(value[:1] in self.LEADS,
                                     "%s begins with a formula lead: %r" % (head, value))
        return heads, rows

    def test_sheet_cell_neutralizes_text_and_keeps_numbers(self):
        for lead in self.LEADS:
            self.assertEqual(f.sheet_cell(lead + "1+1"), "'" + lead + "1+1")
        self.assertEqual(f.sheet_cell("ok answer"), "ok answer")
        self.assertEqual(f.sheet_cell("'already quoted"), "'already quoted")
        # a legitimate negative number in a numeric column is left a number
        self.assertEqual(f.sheet_cell(-3, numeric=True), "-3")
        self.assertEqual(f.sheet_cell("-3", numeric=True), "-3")
        self.assertEqual(f.sheet_cell("-2.5", numeric=True), "-2.5")
        self.assertEqual(f.sheet_cell(4, numeric=True), "4")
        # the same text in a text column is neutralized, and a formula in a numeric column too
        self.assertEqual(f.sheet_cell("-3"), "'-3")
        self.assertEqual(f.sheet_cell("-2+3", numeric=True), "'-2+3")
        self.assertEqual(f.sheet_cell("=1+1", numeric=True), "'=1+1")
        self.assertEqual(f.sheet_cell(None), "")

    def test_the_audits_injection_file_writes_a_safe_sheet_and_key(self):
        path = audit_input(self, "csv-injection-in-explanations.csv")
        report = f.analyze(path, cases_dir=CASES)
        sheet = os.path.join(self.tmp.path, "sheet.csv")
        key = os.path.join(self.tmp.path, "key.csv")
        self.assertEqual(f.write_scoring_sheet(report, sheet, key), 5)
        heads, rows = self.assert_safe(sheet, f.SHEET_NUMERIC)
        self.assert_safe(key, f.KEY_NUMERIC)
        by_line = {row[heads.index("line")]: dict(zip(heads, row)) for row in rows}
        self.assertEqual(by_line["1"]["decisive_evidence"],
                         "'=HYPERLINK(\"http://example.invalid\",\"click\")")
        self.assertEqual(by_line["1"]["why_it_matters_for_this_period"], "'+1+1")
        self.assertEqual(by_line["1"]["action_or_source_request"], "'-2+3")
        self.assertEqual(by_line["2"]["decisive_evidence"], "'@SUM(1,1)")
        self.assertEqual(by_line["5"]["action_or_source_request"], "'-A1")
        # the findings keep the answer as posted; only the sheet cell carries the apostrophe
        self.assertEqual(report["initial"][0]["explanations"][1]["evidence"],
                         "=HYPERLINK(\"http://example.invalid\",\"click\")")
        self.assertEqual(sorted(by_line), ["1", "2", "3", "4", "5"])

    def test_a_formula_codename_and_attempt_id_are_neutralized_in_the_key(self):
        leads = ["=cmd|' /C calc'!A0", "+Heron", "-Heron", "@Heron", "\tHeron",
                 chr(0xff1d) + "Heron"]
        rows = [explained(code, "att-f%d" % k) for k, code in enumerate(leads)]
        rows.append(explained("Plain Heron", "-att-minus"))
        report = f.analyze(self.tmp.csv("responses.csv", rows), cases_dir=fixture_cases(
            self.tmp.path))
        self.assertEqual(report["n_attempts_received"], 7)
        sheet, key = (os.path.join(self.tmp.path, n) for n in ("s.csv", "k.csv"))
        f.write_scoring_sheet(report, sheet, key)
        self.assert_safe(sheet, f.SHEET_NUMERIC)
        heads, rows_key = self.assert_safe(key, f.KEY_NUMERIC)
        codes = sorted(r[heads.index("codename")] for r in rows_key)
        self.assertIn("'=cmd|' /C calc'!A0", codes)
        self.assertIn("'" + chr(0xff1d) + "Heron", codes)
        self.assertIn("'-att-minus", [r[heads.index("attempt_id")] for r in rows_key])

    def test_a_score_handed_back_with_a_text_apostrophe_still_reads(self):
        rows = [explained("Writer", "att-w")]
        report = f.analyze(self.tmp.csv("responses.csv", rows), cases_dir=fixture_cases(
            self.tmp.path))
        sheet = os.path.join(self.tmp.path, "sheet.csv")
        f.write_scoring_sheet(report, sheet, os.path.join(self.tmp.path, "key.csv"))
        with open(sheet, encoding="utf-8", newline="") as handle:
            blank = list(csv.DictReader(handle))
        filled = [dict(r, score_evidence="'2", score_period="1", score_action="'0") for r in blank]
        scores = f.read_score_sheet(self.tmp.csv("filled.csv", filled))
        self.assertEqual({v["scores"]["evidence"] for v in scores.values()}, {2})


def page_minimum(texts):
    """explainProblem() from index.html, run by node on each text, or None without node."""
    node = shutil.which("node")
    if not node:
        return None
    import subprocess
    script = os.path.join(HERE, "explain-minimum.cjs")
    blob = subprocess.run([node, script, os.path.join(REPO, "index.html")],
                          input=json.dumps(texts).encode("utf-8"), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=True).stdout
    return json.loads(blob.decode("utf-8"))


class MinimumRuleTest(unittest.TestCase):
    """Item 2: one minimum for the three written parts, the same in index.html and findings.py."""

    def setUp(self):
        self.tmp = Folder()
        with open(VECTORS, encoding="utf-8") as handle:
            self.vectors = json.load(handle)

    def tearDown(self):
        self.tmp.close()

    def test_findings_applies_the_rule_to_every_shared_case(self):
        self.assertGreaterEqual(len(self.vectors), 30)
        for v in self.vectors:
            self.assertEqual(f.explanation_problem(v["text"]), v["problem"],
                             "%r (%s)" % (v["text"], v["why"]))

    def test_the_page_applies_the_same_rule_word_for_word(self):
        texts = [v["text"] for v in self.vectors]
        extra = ["The 31 May schedule stops before June.", "  ", "tbd", "Ask the controller",
                 chr(0x3000) + "none" + chr(0x3000), "Invoice #20614 on file", "x y z w",
                 "don" + chr(0x02bc) + "t know", "ok ok ok ok", "Payroll register"]
        got = page_minimum(texts + extra)
        if got is None:
            self.skipTest("node is not on this machine")
        self.assertEqual(got[:len(texts)], [v["problem"] for v in self.vectors])
        self.assertEqual(got[len(texts):], [f.explanation_problem(t) for t in extra])

    def test_the_audits_non_answers_now_count_as_incomplete_and_stay_visible(self):
        cases = fixture_cases(self.tmp.path)
        texts = {1: {"evidence": "a b", "period": "...", "action": "none"},
                 2: {"evidence": "none", "period": "None.", "action": "n/a"}}
        report = f.analyze(self.tmp.csv("r.csv", [explained("Short Answers", "att-s",
                                                            texts=texts)]), cases_dir=cases)
        a = report["initial"][0]
        self.assertFalse(a["completed"])
        self.assertEqual(report["n_attempts_completed"], 0)
        self.assertEqual([(g["line"], g["part"], g["text"], g["problem"])
                          for g in a["explanation_gaps"]],
                         [(1, "evidence", "a b", "short"), (1, "period", "...", "no words"),
                          (1, "action", "none", "stock"), (2, "evidence", "none", "stock"),
                          (2, "period", "None.", "stock"), (2, "action", "n/a", "stock")])
        # both lines carry text, so both reach the sheet with the parts named
        items = {i["line"]: i for i in report["explanation_items"]}
        self.assertEqual(sorted(items), [1, 2, 3, 4, 5])
        self.assertEqual(items[2]["parts"], {"evidence": "none", "period": "None.", "action": "n/a"})
        sheet = os.path.join(self.tmp.path, "sheet.csv")
        f.write_scoring_sheet(report, sheet, os.path.join(self.tmp.path, "key.csv"))
        with open(sheet, encoding="utf-8", newline="") as handle:
            rows = {r["line"]: r for r in csv.DictReader(handle)}
        self.assertEqual(rows["1"]["below_minimum"],
                         "decisive evidence: under two words and eight letters or digits; why it "
                         "matters for this period: punctuation or symbols only; action or source "
                         "request: a stock non-answer")
        self.assertEqual(rows["2"]["why_it_matters_for_this_period"], "None.")
        self.assertEqual(rows["3"]["below_minimum"], "")
        e = report["sets"][0]["explain"]
        self.assertEqual((e["first_attempts_with_gaps"], e["parts_below_minimum"],
                          e["below_minimum_items"]), (1, 6, 2))
        text = f.build_markdown(report, "r.csv")
        self.assertIn("**Written answers below the minimum.**", text)
        self.assertIn('| Short Answers | att-s | 1 | Why it matters for this period | "..." | '
                      'punctuation or symbols only |', text)
        fields = dict(f.readout_fields(report, "r.csv")["sets"][0][1])
        self.assertEqual(fields["explain.first_attempts_below_minimum"], 1)
        self.assertEqual(fields["explain.parts_below_minimum"], 6)

    def test_the_audits_v6_records_missing_explanations_are_incomplete(self):
        missing = f.analyze(audit_input(self, "v6-missing-explanation.csv"), cases_dir=CASES)
        a = missing["initial"][0]
        self.assertFalse(a["completed"])
        self.assertEqual([(g["line"], g["part"]) for g in a["explanation_gaps"]],
                         [(3, "evidence"), (3, "period"), (3, "action")])
        none = f.analyze(audit_input(self, "v6-no-explanations-at-all.csv"), cases_dir=CASES)
        b = none["initial"][0]
        self.assertFalse(b["completed"])
        self.assertEqual(len(b["explanation_gaps"]), 15)
        self.assertEqual({g["problem"] for g in b["explanation_gaps"]}, {"not posted"})
        self.assertIn("which asks for one on every call", f.build_markdown(none, "x.csv"))
        # a brightwater-v5 record was never asked, so it completes without any
        old = f.analyze(audit_input(self, "v5-record-carrying-explanations.csv"), cases_dir=CASES)
        self.assertTrue(old["initial"][0]["completed"])
        self.assertEqual(old["initial"][0]["explanation_gaps"], [])
        # and a complete v6 record completes
        good = f.analyze(audit_input(self, "version-mixing.csv"), cases_dir=CASES)
        six = [x for x in good["initial"] if x["set"].endswith("brightwater-v6")][0]
        self.assertTrue(six["completed"])


class ConflictTest(unittest.TestCase):
    """Item 3: one attempt identifier on rows that differ is a conflict, never a resend."""

    def setUp(self):
        self.tmp = Folder()

    def tearDown(self):
        self.tmp.close()

    def run_rows(self, rows, **kw):
        kw.setdefault("cases_dir", CASES)
        return f.analyze(self.tmp.csv("responses.csv", rows), **kw)

    def test_the_audits_reused_id_with_different_content_is_held_out(self):
        path = audit_input(self, "duplicate-attempt-id-different-content.csv")
        report = f.analyze(path, cases_dir=CASES)
        self.assertEqual(report["duplicate_sends"], [])
        self.assertEqual(len(report["conflicts"]), 1)
        c = report["conflicts"][0]
        self.assertEqual(c["attempt_id"], "dup-1")
        self.assertEqual([r["sheet_row"] for r in c["records"]], [2, 3])
        self.assertEqual([r["score"] for r in c["records"]], [13, 14])
        columns = [d["column"] for d in c["differences"]]
        self.assertIn("Call C1", columns)
        self.assertIn("Question C (round two string)", columns)
        self.assertNotIn("Timestamp", columns)
        # held out of every count and rate until resolved
        self.assertEqual((report["n_attempts_received"], len(report["initial"]), report["sets"]),
                         (0, 0, []))
        run = dict(f.readout_fields(report, "x.csv")["run"])
        self.assertEqual((run["run.attempt_conflicts_unresolved"],
                          run["run.attempt_conflict_rows_held_out"]), (1, 2))
        text = f.build_markdown(report, "x.csv")
        self.assertIn("**Unresolved: attempt dup-1**", text)
        self.assertIn("| 2 | Twin Lark | 2026/09/15 9:40:00 |", text)
        self.assertIn("| 3 | Twin Lark | 2026/09/15 9:02:11 |", text)
        # the facilitator keeps one row, and it is scored
        kept = f.analyze(path, cases_dir=CASES, resolutions={"dup-1": 3})
        self.assertEqual(kept["conflicts"], [])
        self.assertEqual(kept["conflicts_resolved"][0]["kept_row"], 3)
        self.assertEqual(kept["initial"][0]["score"], 14)
        self.assertIn("**Resolved by the facilitator: attempt dup-1**, sheet row 3 kept",
                      f.build_markdown(kept, "x.csv"))

    def test_identical_rows_are_one_attempt_sent_twice_at_the_earliest_time(self):
        first = response("Retry Sender", "att-r", "halyard-v4", ts="2026-09-15 10:05:00")
        again = dict(first, **{f.TIMESTAMP_TITLE: "2026-09-15 10:00:00"})
        report = self.run_rows([first, again])
        self.assertEqual(report["conflicts"], [])
        self.assertEqual(report["n_attempts_received"], 1)
        self.assertEqual(report["initial"][0]["timestamp"], "2026-09-15 10:00:00")
        self.assertEqual(report["duplicate_sends"],
                         ["Retry Sender (attempt att-r sent again: sheet row 2 repeats sheet row 3)"])

    def test_three_rows_two_alike_and_one_different_is_a_conflict_of_all_three(self):
        one = response("Triple", "att-3", "halyard-v4")
        two = dict(one)
        three = response("Triple", "att-3", "halyard-v4", calls=keyed_calls("halyard-v4", (0,)))
        report = self.run_rows([one, two, three])
        self.assertEqual(len(report["conflicts"]), 1)
        self.assertEqual(len(report["conflicts"][0]["records"]), 3)
        self.assertEqual(report["n_attempts_received"], 0)

    def test_a_later_attempt_is_not_promoted_over_an_unresolved_conflict(self):
        a = response("Same Name", "att-c", "halyard-v4", ts="2026-09-15 09:00:00")
        b = response("Same Name", "att-c", "halyard-v4", ts="2026-09-15 09:01:00",
                     calls=keyed_calls("halyard-v4", (2,)))
        later = response("SAME NAME", "att-d", "halyard-v4", ts="2026-09-15 11:00:00")
        report = self.run_rows([a, b, later])
        self.assertEqual(report["initial"], [])
        self.assertEqual(report["reattempts"][0]["attempt_number"], 2)
        self.assertEqual(report["reattempts"][0]["after_conflict"], ["att-c"])
        self.assertIn("after attempt att-c", f.build_markdown(report, "x.csv"))

    def test_a_resolution_that_names_the_wrong_row_or_no_conflict_is_refused(self):
        a = response("Same Name", "att-c", "halyard-v4")
        b = response("Same Name", "att-c", "halyard-v4", calls=keyed_calls("halyard-v4", (2,)))
        with self.assertRaises(f.InputError):
            self.run_rows([a, b], resolutions={"att-c": 9})
        with self.assertRaises(f.InputError):
            self.run_rows([a, b], resolutions={"att-zz": 2})
        self.assertEqual(f.main([self.tmp.csv("r.csv", [a, b]), "--cases", CASES,
                                 "--out", os.path.join(self.tmp.path, "o.md"),
                                 "--resolve-conflict", "att-c"]), 2)


class CodenameAndExclusionTest(unittest.TestCase):
    """Items 5 and 6: codenames folded before counting, and exclusions that only a marker earns."""

    def setUp(self):
        self.tmp = Folder()

    def tearDown(self):
        self.tmp.close()

    def run_rows(self, rows, **kw):
        kw.setdefault("cases_dir", CASES)
        return f.analyze(self.tmp.csv("responses.csv", rows), **kw)

    def test_composed_and_decomposed_zoe_are_one_codename_spelled_as_typed(self):
        path = audit_input(self, "non-ascii-codenames.csv")
        report = f.analyze(path, cases_dir=CASES)
        self.assertEqual(report["n_excluded"], 0)
        self.assertEqual(report["n_attempts_received"], 6)
        self.assertEqual(report["n_codenames"], 5)
        zoe = [a for a in report["attempts"] if f.codename_key(a["codename"]) == "zo" + chr(0xeb)]
        self.assertEqual([a["codename"] for a in zoe], ["Zo" + chr(0xeb), "Zoe" + chr(0x308)])
        self.assertEqual(sorted(a["attempt_number"] for a in zoe), [1, 2])
        self.assertEqual(report["reattempts"][0]["codename"], "Zoe" + chr(0x308))

    def test_case_folding_joins_codenames_and_the_roster(self):
        rows = [response("Stra" + chr(0xdf) + "e", "att-1", "halyard-v4", ts="2026-09-15 09:00:00"),
                response("STRASSE", "att-2", "halyard-v4", ts="2026-09-15 10:00:00")]
        roster = self.tmp.csv("roster.csv", [{"participant": "P1", "codename": "strasse",
                                              "consent": "yes"}])
        report = self.run_rows(rows, roster_path=roster)
        self.assertEqual(report["n_codenames"], 1)
        self.assertEqual(report["n_participants_confirmed"], 1)

    def test_real_codenames_that_contain_test_or_mention_synthetic_stay_in(self):
        rows = [response("Test Pilot", "att-1", "halyard-v4"),
                response("Contest Winner", "att-2", "halyard-v4"),
                response("Taste Tester", "att-3", "halyard-v4"),
                response("Blue Jay", "audit-7f3k", "halyard-v4"),
                response("Green Heron", "att-5", "halyard-v4",
                         marker="The memo reads like a synthetic test only")]
        report = self.run_rows(rows)
        self.assertEqual(report["n_excluded"], 0)
        self.assertEqual(report["n_attempts_received"], 5)
        for name in ("participant-text-says-synthetic.csv", "attempt-id-starting-audit.csv"):
            got = f.analyze(audit_input(self, name), cases_dir=CASES)
            self.assertEqual((got["n_excluded"], got["n_attempts_received"]), (0, 1), name)

    def test_test_words_and_markers_still_exclude_and_say_which_rule(self):
        rows = [response("Test Play", "att-1", "halyard-v4"),
                response(chr(0xff34) + chr(0xff45) + chr(0xff53) + chr(0xff54) + " Play", "att-2",
                         "halyard-v4"),
                response("walk test 2", "att-3", "halyard-v4"),
                response("rebuild-test-delete", "att-4", "halyard-v4"),
                response("DELETE ME", "att-5", "halyard-v4"),
                response("Synthetic Heron", "att-6", "halyard-v4"),
                response("Words Marker", "att-7", "halyard-v4", marker="Synthetic test only")]
        report = self.run_rows(rows)
        self.assertEqual(report["n_attempts_received"], 0)
        self.assertEqual(report["excluded"]["test_codename"], [
            "Test Play (sheet row 2, rule: a known test codename)",
            chr(0xff34) + chr(0xff45) + chr(0xff53) + chr(0xff54) +
            " Play (sheet row 3, rule: a known test codename)",
            "walk test 2 (sheet row 4, rule: a codename made only of test words)",
            "rebuild-test-delete (sheet row 5, rule: a known test codename)",
            "DELETE ME (sheet row 6, rule: a codename made only of test words)"])
        self.assertEqual(report["excluded"]["synthetic_by_rule"], [
            "Synthetic Heron (sheet row 7, rule: the codename begins with Synthetic)",
            "Words Marker (sheet row 8, rule: a cell or a Words line reads Synthetic test only)"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
