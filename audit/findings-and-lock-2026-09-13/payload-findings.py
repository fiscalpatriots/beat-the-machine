#!/usr/bin/env python3
"""Read the send the lock walk captured back through tools/findings.py, then the same send with
its written answers cut below the minimum the way an older build could have posted them.

    python audit/findings-and-lock-2026-09-13/payload-findings.py <runs dir>

The payload in <runs dir>/lock-payload.json is the exact form payload the page built in test mode.
It becomes one response row under the form's question titles (the entry ids are read out of
index.html by receipts/receipts-to-form-csv.py). The page stamps a test attempt to be excluded, so
the codename is made synthetic and the findings run with synthetic_check, which says so.

1. As sent: the brightwater-v6 attempt must be complete with no explanation gap.
2. The same row with fresh line 2's answers replaced by "a b", "..." and "none": it must be
   incomplete, the three parts listed, and the line kept on the scoring sheet with below_minimum.
3. The scoring sheet for both rows must hold no cell a spreadsheet would run as a formula.
Prints what it found and exits 1 on any difference.
"""
import csv
import importlib.util
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import findings  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "receipts_to_form", os.path.join(ROOT, "receipts", "receipts-to-form-csv.py"))
convert = importlib.util.module_from_spec(spec)
spec.loader.exec_module(convert)


def main(runs):
    blob = json.load(open(os.path.join(runs, "lock-payload.json"), encoding="utf-8"))
    titles = convert.titles_for(convert.entry_ids(os.path.join(ROOT, "index.html")))
    row = {findings.TIMESTAMP_TITLE: "2026-09-13 23:40:00",
           findings.CODENAME_TITLE: "Synthetic lock walk"}
    for key, value in blob["payload"].items():
        title = titles.get(key.split(".", 1)[1] if key.startswith("entry.") else key)
        if title and title != findings.CODENAME_TITLE:
            row[title] = value.replace("TEST ATTEMPT, exclude from reports.", "") \
                if title == findings.QA_TITLE else value
    cut = dict(row)
    cut[findings.CODENAME_TITLE] = "Synthetic lock walk cut short"
    qc = cut[findings.QC_TITLE]
    start = qc.index("2: Basis:")
    end = qc.index("|| 3: Basis:")
    line2 = qc[start:end]
    body = line2.split(" | Evidence: ")[0]
    tail = line2[line2.index(" | Reason:"):]
    cut[findings.QC_TITLE] = qc[:start] + body + " | Evidence: a b | Period: ... | Action: none" + \
        tail + qc[end:]
    cut[findings.QB_TITLE] = cut[findings.QB_TITLE].replace("Attempt id: ", "Attempt id: cut-")

    folder = tempfile.mkdtemp(prefix="lock-findings-")
    path = os.path.join(folder, "responses.csv")
    heads = list(dict.fromkeys(k for r in (row, cut) for k in r))
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=heads)
        writer.writeheader()
        writer.writerows([row, cut])
    report = findings.analyze(path, cases_dir=os.path.join(ROOT, "cases"), synthetic_check=True)
    ok = True
    by_code = {a["codename"]: a for a in report["attempts"]}
    sent, short = by_code.get("Synthetic lock walk"), by_code.get("Synthetic lock walk cut short")
    print("as sent: set %s, completed %s, explanation gaps %d, parts posted %s"
          % (sent["set"], sent["completed"], len(sent["explanation_gaps"]),
             sorted(sent["explanations"])))
    ok = ok and sent["completed"] and not sent["explanation_gaps"] and \
        sent["case2"]["version"] == "brightwater-v6" and len(sent["explanations"]) == 5
    gaps = [(g["line"], g["part"], g["text"], g["problem"]) for g in short["explanation_gaps"]]
    print("cut short: completed %s, gaps %s" % (short["completed"], gaps))
    ok = ok and not short["completed"] and gaps == [
        (2, "evidence", "a b", "short"), (2, "period", "...", "no words"),
        (2, "action", "none", "stock")]
    sheet = os.path.join(folder, "sheet.csv")
    count = findings.write_scoring_sheet(report, sheet, os.path.join(folder, "key.csv"))
    with open(sheet, encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    marked = [r for r in rows if r["below_minimum"]]
    print("scoring sheet: %d rows, %d marked below the minimum: %s"
          % (count, len(marked), [(r["line"], r["below_minimum"]) for r in marked]))
    ok = ok and count == 10 and len(marked) == 1 and marked[0]["line"] == "2"
    leads = set(findings.FORMULA_LEADS)
    unsafe = [c for name in ("sheet.csv", "key.csv")
              for r in csv.reader(open(os.path.join(folder, name), encoding="utf-8"))
              for c in r if c[:1] in leads]
    print("cells beginning with a formula lead: %d" % len(unsafe))
    ok = ok and not unsafe
    print("disagreements: %s" % (report["disagreements"] or "none"))
    print("RESULT: %s" % ("AS EXPECTED" if ok else "DIFFERENT"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "runs")))
