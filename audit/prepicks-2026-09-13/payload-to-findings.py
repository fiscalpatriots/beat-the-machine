#!/usr/bin/env python3
"""Feed the payloads the walk captured from the running page to tools/findings.py.

    python audit/prepicks-2026-09-13/payload-to-findings.py <walk outdir>

Each <case>-payload-run1.json holds the exact form payload the page built in test mode. This
turns every one into a response row under the form's question titles, using the entry ids read
out of index.html the way receipts/receipts-to-form-csv.py does, and runs the findings on them.
The page stamps a test attempt as one to exclude, so the codename is made synthetic and the
script is run with --synthetic-check, which scores synthetic rows and says so. It prints, per
case, what the page posted for the read and what findings.py rebuilt from the case file, and
exits 1 if they differ or the findings record any disagreement.
"""
import csv
import glob
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


def main(outdir):
    ids = convert.entry_ids(os.path.join(ROOT, "index.html"))
    titles = convert.titles_for(ids)
    rows, posted = [], {}
    for n, path in enumerate(sorted(glob.glob(os.path.join(outdir, "*-payload-run1.json")))):
        blob = json.load(open(path, encoding="utf-8"))
        case = os.path.basename(path).split("-payload")[0]
        row = {findings.TIMESTAMP_TITLE: "2026-09-13 22:%02d:00" % n,
               findings.CODENAME_TITLE: "Synthetic prepick walk %s" % case}
        for key, value in blob["payload"].items():
            title = titles.get(key.split(".", 1)[1] if key.startswith("entry.") else key)
            if title and title != findings.CODENAME_TITLE:
                row[title] = value.replace("TEST ATTEMPT, exclude from reports.", "") \
                    if title == findings.QA_TITLE else value
        rows.append(row)
        posted[row[findings.CODENAME_TITLE]] = blob["prepicks"]["afterDraft"]
    if not rows:
        print("no payload files in %s" % outdir)
        return 1
    heads = list(dict.fromkeys(k for r in rows for k in r))
    tmp = os.path.join(tempfile.mkdtemp(prefix="prepick-parity-"), "responses.csv")
    with open(tmp, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=heads)
        writer.writeheader()
        writer.writerows(rows)
    report = findings.analyze(tmp, cases_dir=os.path.join(ROOT, "cases"), synthetic_check=True)
    ok = True
    for a in report["attempts"]:
        page = posted[a["codename"]]
        got = a["read"]
        same = bool(got) and not got["late"] and (got["toward"], got["away"], got["held"]) == (
            page["changedTowardKey"], page["changedAwayFromKey"], page["held"])
        ok = ok and same and not a["disagreements"]
        print("%s on %s: page posted %d toward, %d away, %d held; findings rebuilt %s; "
              "call agreement %d of %d; disagreements %d; %s"
              % (a["codename"], a["case1"]["version"] if a["case1"] else a["refusal"],
                 page["changedTowardKey"], page["changedAwayFromKey"], page["held"],
                 ("%d, %d, %d" % (got["toward"], got["away"], got["held"])) if got else "nothing",
                 a["score"], len(a["answered"]), len(a["disagreements"]),
                 "MATCH" if same else "DIFFERENT"))
        for d in a["disagreements"]:
            print("  disagreement: %s" % d)
    for s in report["sets"]:
        r = s["read"]
        print("set %s: first attempts with the read %d, lines compared %d, changed %d, toward %d, "
              "away %d, held %d" % (s["label"], r["n"], r["compared"], r["changed"], r["toward"],
                                    r["away"], r["held"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else HERE))
