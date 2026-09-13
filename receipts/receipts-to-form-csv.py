#!/usr/bin/env python3
"""Turn a "Second Pass receipts" sheet export into the shape tools/findings.py reads.

Why it exists. findings.py matches columns by the Google Form's question titles, because that
is what the form export gives it. The receipts sheet holds something better, the whole attempt
record as JSON, but under different column names. This script reads the receipts export, pulls
the posted payload out of each record, and writes a CSV whose headers are the form's question
titles, so findings.py runs against it unchanged:

    python receipts/receipts-to-form-csv.py receipts-export.csv --out responses-from-receipts.csv
    python tools/findings.py responses-from-receipts.csv

Nothing is invented. Every cell written here was posted by the page and stored by the endpoint;
the entry ids come out of index.html at run time, so a question that is renumbered there is
renumbered here without this file being touched. A row whose raw JSON will not parse is counted
and named rather than guessed at, and test attempts are dropped unless --keep-test is passed.
"""

import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import findings  # noqa: E402  the answer key and the question titles, one source of truth


def entry_ids(index_html):
    """The entry id map out of index.html: {"codename": "5327...", "call": [...], ...}."""
    with open(index_html, encoding="utf-8") as handle:
        text = handle.read()
    start = text.find("var E = {")
    if start < 0:
        raise SystemExit("no entry id block in %s" % index_html)
    end = text.find("};", start)
    block = text[start:end]
    out = {}
    for key, raw in re.findall(r'(\w+)\s*:\s*(\[[^\]]*\]|"[^"]*")', block):
        out[key] = json.loads(raw)
    missing = [k for k in ("codename", "round1", "call", "why") if k not in out]
    if missing:
        raise SystemExit("entry id block is missing %s" % ", ".join(missing))
    return out


def titles_for(ids):
    """entry id -> the form question title findings.py looks for."""
    m = {
        ids["codename"]: findings.CODENAME_TITLE,
        ids["round1"]: findings.ROUND1_TITLE,
        ids["expect"]: findings.INTAKE_TITLES[0][1],
        ids["confPre"]: findings.INTAKE_TITLES[1][1],
        ids["experience"]: findings.INTAKE_TITLES[2][1],
        ids["confPost"]: findings.INTAKE_TITLES[3][1],
        ids["qa"]: findings.QA_TITLE,
        ids["qb"]: findings.QB_TITLE,
        ids["qc"]: findings.QC_TITLE,
        ids["qd"]: findings.QD_TITLE,
    }
    for i, entry in enumerate(ids["call"]):
        m[entry] = findings.CALL_TITLES[i]
    for i, entry in enumerate(ids["why"]):
        m[entry] = findings.WHY_TITLES[i]
    return m


def raw_json(row):
    """The record, put back together from the cells it was written across."""
    parts = []
    for i in range(1, 9):
        cell = row.get("rawJson%d" % i, "")
        if cell:
            parts.append(cell)
    return "".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="the receipts sheet, downloaded as CSV")
    ap.add_argument("--out", default="responses-from-receipts.csv", help="where to write")
    ap.add_argument("--index", default=os.path.join(ROOT, "index.html"),
                    help="the page the entry ids are read from")
    ap.add_argument("--keep-test", action="store_true",
                    help="keep rows marked as test attempts, which are dropped by default")
    args = ap.parse_args()

    if not os.path.exists(args.csv):
        raise SystemExit("no file at %s" % args.csv)

    ids = entry_ids(args.index)
    titles = titles_for(ids)
    ordered = ([findings.TIMESTAMP_TITLE, findings.CODENAME_TITLE, findings.ROUND1_TITLE] +
               [findings.INTAKE_TITLES[i][1] for i in range(3)] +
               [t for pair in zip(findings.CALL_TITLES, findings.WHY_TITLES) for t in pair] +
               [findings.INTAKE_TITLES[3][1], findings.QA_TITLE, findings.QB_TITLE,
                findings.QC_TITLE, findings.QD_TITLE] +
               ["Receipt", "Attempt id", "Stored at"])

    kept, dropped_test, unparsed = [], 0, []
    with open(args.csv, encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            text = raw_json(row)
            if not text:
                unparsed.append(row.get("attemptId", "(no id)") + ": no raw JSON in the row")
                continue
            try:
                record = json.loads(text)
            except ValueError as exc:
                unparsed.append("%s: %s" % (row.get("attemptId", "(no id)"), exc))
                continue
            attempt = record.get("attempt", {})
            if attempt.get("testAttempt") and not args.keep_test:
                dropped_test += 1
                continue
            payload = record.get("payload") or {}
            out = {t: "" for t in ordered}
            out[findings.TIMESTAMP_TITLE] = row.get("receivedAt", "") or attempt.get("completed", "")
            out["Receipt"] = row.get("receipt", "")
            out["Attempt id"] = attempt.get("id", "")
            out["Stored at"] = row.get("receivedAt", "")
            for key, value in payload.items():
                entry = key.split(".", 1)[1] if key.startswith("entry.") else key
                title = titles.get(entry)
                if title:
                    out[title] = value
            kept.append(out)

    with open(args.out, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        for row in kept:
            writer.writerow(row)

    print("%d rows written to %s" % (len(kept), args.out))
    if dropped_test:
        print("%d test attempts dropped; pass --keep-test to keep them" % dropped_test)
    for line in unparsed:
        print("could not read: %s" % line)
    print("Now run: python tools/findings.py %s" % args.out)


if __name__ == "__main__":
    main()
