"""A1 independent audit: findings script probes against tools/findings.py at a given tree.

usage: python findings-probes.py <game-root> <audit-dir>

Part 1 replays the third review's probe-findings.py exactly (same rows, analyze() with its
defaults), then again with synthetic_check=True, which is the switch the head now asks a
reviewer to use for review probes.
Part 2 builds new synthetic inputs from the head's own findings-sample.csv row shape and
records what analyze() and write_scoring_sheet() return. Every row here is synthetic.
"""
import csv, importlib.util, json, os, sys, copy

game, audit = sys.argv[1], sys.argv[2]
inputs = os.path.join(audit, "inputs", "findings")
outputs = os.path.join(audit, "outputs", "findings")
os.makedirs(inputs, exist_ok=True)
os.makedirs(outputs, exist_ok=True)
spec = importlib.util.spec_from_file_location("findings", os.path.join(game, "tools", "findings.py"))
f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(f)
CASES = os.path.join(game, "cases")


def write(name, rows, heads=None):
    path = os.path.join(inputs, name + ".csv")
    heads = heads or list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=heads)
        w.writeheader()
        w.writerows(rows)
    return path


def summary(rep):
    return {
        "n_rows_raw": rep["n_rows_raw"], "n_excluded": rep["n_excluded"],
        "excluded": rep["excluded"], "duplicate_sends": rep["duplicate_sends"],
        "n_attempts_received": rep["n_attempts_received"],
        "n_attempts_completed": rep["n_attempts_completed"], "n_codenames": rep["n_codenames"],
        "n_participants_confirmed": rep["n_participants_confirmed"],
        "roster": ({k: v for k, v in rep["roster"].items() if k != "confirmed"} if rep["roster"] else None),
        "refusal_counts": rep["refusal_counts"],
        "initial": [{"code": a["codename"], "attempt": a["attempt_id"], "set": a["set"], "score": a["score"],
                     "answered": len(a["answered"]), "fresh": a["fresh"], "completed": a["completed"],
                     "explanations": a["explanations"]} for a in rep["initial"]],
        "reattempts": [{"code": a["codename"], "attempt": a["attempt_id"], "n": a["attempt_number"]}
                       for a in rep["reattempts"]],
        "sets": [{"label": s["label"], "n_attempts": s["n_attempts"]} for s in rep["sets"]],
        "case_versions": rep["case_versions"], "disagreements": rep["disagreements"],
        "n_explanation_items": len(rep["explanation_items"]),
    }


results = {}

# ---------------------------------------------------------------- part 1: exact replay
def review_row(code, attempt, casefile):
    c = json.load(open(os.path.join(CASES, casefile), encoding="utf-8"))
    r = {f.CODENAME_TITLE: code,
         f.QA_TITLE: 'Case: %s, version %s (practice, %d lines), no fresh case, dated 2026-09-13, loaded from cases/ files. Product: second-pass-drill 1.6.1.'
         % (casefile.split("-")[0], casefile[:-5], len(c["cards"])),
         f.QB_TITLE: 'Attempt id: %s, run 1' % attempt, f.TIMESTAMP_TITLE: '2026-09-13 20:00:00'}
    for i, card in enumerate(c["cards"]):
        r[f.WHY_TITLES[i]] = ('Basis: %s | Words: Synthetic test only || Line %d, account %s. Called: %s. Key: %s. Type: %s. Correct. Reason: agrees. Key basis: %s.'
                              % (card["basisKey"][0], i + 1, card["acct"], card["key"], card["key"], card["type"], card["basisKey"][0]))
    return r


review_cases = {"same-person-two-attempts": [review_row("Synthetic same participant", "audit-a", "halyard-v4.json"),
                                             review_row("Synthetic same participant", "audit-b", "halyard-v4.json")],
                "kestrel-perfect": [review_row("Synthetic Kestrel participant", "audit-c", "kestrel-v1.json")]}
for name, rows in review_cases.items():
    p = write("review-" + name, rows)
    for check in (False, True):
        rep = f.analyze(p, synthetic_check=check)
        results["replay:%s:synthetic_check=%s" % (name, check)] = {
            "review_script_fields": {"players": rep["n_players"],
                                     "scores": [{"score": x["score"], "answered": len(x["answered"]), "case": x["cases"]} for x in rep["players"]],
                                     "repeatRuns": rep["repeat_runs"], "versions": rep["case_versions"],
                                     "disagreements": rep["disagreements"]},
            "summary": summary(rep)}

# ---------------------------------------------------------------- part 2: new probes
base_rows = list(csv.DictReader(open(os.path.join(game, "tools", "findings-sample.csv"), encoding="utf-8")))
HEADS = list(base_rows[0].keys())
T = copy.deepcopy(base_rows[0])  # REDLINE: halyard-v4 with brightwater-v5, 14 of 14


def row(code, attempt, fresh="brightwater-v5", ts="2026/09/15 9:02:11", explain=None, qa_extra=""):
    r = copy.deepcopy(T)
    r["Codename"] = code
    r["Timestamp"] = ts
    r[f.QA_TITLE] = r[f.QA_TITLE].replace("brightwater-v5", fresh) + qa_extra
    r[f.QB_TITLE] = r[f.QB_TITLE].replace("att-redline", attempt)
    qc = r[f.QC_TITLE]
    if explain is not None:
        # rebuild the Round2 basis in the explain-2026-09-13 shape the head posts
        keys = json.load(open(os.path.join(CASES, "brightwater-v6.json"), encoding="utf-8"))["cards"]
        parts = []
        for i, card in enumerate(keys):
            e = explain[i] if i < len(explain) else ("none", "none", "none")
            parts.append("%d: Basis: %s | Evidence: %s | Period: %s | Action: %s | Reason: agrees | Key basis: %s"
                         % (i + 1, card["basisKey"][0], e[0], e[1], e[2], "; ".join(card["basisKey"])))
        head, _, tail = qc.partition("Round2 basis, by line:")
        fresh_tail = tail[tail.find(" Fresh case:"):] if " Fresh case:" in tail else ""
        qc = head + "Round2 basis, by line: " + " || ".join(parts) + "." + fresh_tail
    r[f.QC_TITLE] = qc
    return r


GOOD = [("The invoice is on file", "It is dated June", "Ask for the schedule")] * 5
probes = {}
probes["version-mixing"] = [row("Quiet Heron", "mix-1", "brightwater-v5"), row("Amber Fox", "mix-2", "brightwater-v6", explain=GOOD)]
probes["unknown-version"] = [row("Slate Owl", "unk-1", "brightwater-v9")]
probes["unknown-practice-version"] = [dict(row("Slate Owl", "unk-2"), **{f.QA_TITLE: row("x", "y")[f.QA_TITLE].replace("halyard-v4", "halyard-v7")})]
probes["v6-missing-explanation"] = [row("Iron Wren", "miss-1", "brightwater-v6",
                                        explain=GOOD[:2] + [("none", "none", "none")] + GOOD[3:])]
probes["v6-no-explanations-at-all"] = [row("Iron Wren", "miss-2", "brightwater-v6")]
probes["v5-record-carrying-explanations"] = [row("Old Crow", "v5-1", "brightwater-v5", explain=GOOD)]
dup_a = row("Twin Lark", "dup-1", "brightwater-v6", ts="2026/09/15 9:02:11", explain=GOOD)
dup_b = row("Twin Lark", "dup-1", "brightwater-v6", ts="2026/09/15 9:40:00",
            explain=[("A different answer entirely", "different", "different")] * 5)
dup_b[f.WHY_TITLES[0]] = dup_b[f.WHY_TITLES[0]].replace("Called: flag", "Called: stand")
dup_b[f.CALL_TITLES[0]] = "Accept"
probes["duplicate-attempt-id-different-content"] = [dup_b, dup_a]  # the later, different row first in file order
inj = [("=HYPERLINK(\"http://example.invalid\",\"click\")", "+1+1", "-2+3"), ("@SUM(1,1)", "=1+1", "\t=cmd"),
       ("=1+1", "+cmd|' /C calc'!A0", "-1"), ("ok answer", "@x", "=x"), ("=A1", "+A1", "-A1")]
probes["csv-injection-in-explanations"] = [row("Red Kite", "inj-1", "brightwater-v6", explain=inj)]
probes["non-ascii-codenames"] = [row("Zoë", "na-1", "brightwater-v6", explain=GOOD, ts="2026/09/15 9:00:00"),
                                 row("Zoë", "na-2", "brightwater-v6", explain=GOOD, ts="2026/09/15 9:05:00"),
                                 row("李明", "na-3", "brightwater-v6", explain=GOOD, ts="2026/09/15 9:10:00"),
                                 row("Ｔｅｓｔ Pilot", "na-4", "brightwater-v6", explain=GOOD, ts="2026/09/15 9:15:00"),
                                 row("Contest Winner", "na-5", "brightwater-v6", explain=GOOD, ts="2026/09/15 9:20:00"),
                                 row("Test Pilot", "na-6", "brightwater-v6", explain=GOOD, ts="2026/09/15 9:25:00")]
probes["participant-text-says-synthetic"] = [row("Green Heron", "real-1", "brightwater-v6",
                                                explain=[("The memo reads like a synthetic test only", "May", "Ask")] + GOOD[1:])]
probes["attempt-id-starting-audit"] = [row("Blue Jay", "audit-7f3k", "brightwater-v6", explain=GOOD)]

roster_path = os.path.join(inputs, "roster-with-ghost.csv")
with open(roster_path, "w", encoding="utf-8", newline="") as h:
    w = csv.writer(h)
    w.writerow(["participant", "codename", "consent", "role"])
    w.writerow(["P1", "Quiet Heron", "yes", "student"])
    w.writerow(["P2", "Amber Fox", "yes", "practitioner"])
    w.writerow(["P3", "Never Played", "yes", "student"])
    w.writerow(["P4", "quiet heron", "yes", "student"])

for name, rows in probes.items():
    p = write(name, rows, HEADS)
    try:
        rep = f.analyze(p, cases_dir=CASES)
        out = summary(rep)
        if name == "csv-injection-in-explanations":
            sheet = os.path.join(outputs, "scoring-sheet-injection.csv")
            key = os.path.join(outputs, "scoring-sheet-injection-key.csv")
            f.write_scoring_sheet(rep, sheet, key)
            cells = [c for r in csv.reader(open(sheet, encoding="utf-8")) for c in r]
            out["scoring_sheet_cells_starting_with_formula_char"] = [c for c in cells if c[:1] in "=+-@\t"]
        results["probe:" + name] = out
    except Exception as exc:
        results["probe:" + name] = {"exception": "%s: %s" % (type(exc).__name__, exc)}

rep = f.analyze(write("version-mixing-with-roster", probes["version-mixing"], HEADS), roster_path=roster_path, cases_dir=CASES)
results["probe:roster-with-ghost-and-case-conflict"] = summary(rep)
json.dump(results, open(os.path.join(outputs, "findings-probes.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for k, v in results.items():
    print("==", k)
    print(json.dumps(v, ensure_ascii=False)[:1400])
