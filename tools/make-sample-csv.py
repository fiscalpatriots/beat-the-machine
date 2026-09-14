#!/usr/bin/env python3
"""Builds findings-sample.csv and findings-sample-roster.csv for testing findings.py.

The response file carries the form's real headers and invented responses, written the way
index.html writes its cells in product 1.6.1: the ledger picks in the round one question, a
basis, the page's own reason verdict and the card's basis key in every Why field, the attempt
identifier and the reason score in question B, and the Round2 string with its per line basis
at the tail of question C. Every key comes from the case file for the version a row names.

The rows exercise every rule findings.py applies: three case sets (halyard-v4 and kestrel-v1
with brightwater-v5, and halyard-v4 with brightwater-v6, whose fresh lines carry the three-part
written explanation in question C the way r2Line() posts it) plus an older halyard-v3 row, a reattempt under a codename already
counted, one attempt sent twice, an authored case and an unknown version that must both be
refused, test codenames, a row the page marked as a test attempt, and a synthetic row in the
third review's shape that the synthetic rule must exclude. The roster file is a consented
roster in the documented format, with one participant under two codenames, one row without
consent and one codename that never played.

Only for testing findings.py. It touches nothing but the two sample files.

    python tools/make-sample-csv.py
    python tools/findings.py tools/findings-sample.csv --roster tools/findings-sample-roster.csv --out tools/FINDINGS-sample.md --fields tools/readout-fields-sample.json
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from findings import (CALL_TITLES, WHY_TITLES, SLOTS, CaseLibrary,  # noqa
                      find_cases_dir, reason_agrees, key_letters)

LIBRARY = CaseLibrary(find_cases_dir())


def case(version):
    found, why = LIBRARY.lookup(version)
    if not found:
        raise SystemExit("make-sample-csv.py needs %s: %s" % (version, why))
    return found


HALYARD = case("halyard-v4")
HALYARD_OLD = case("halyard-v3")
KESTREL = case("kestrel-v1")
FRESH = case("brightwater-v5")
FRESH6 = case("brightwater-v6")

HEADERS = ["Timestamp", "Codename",
           "Round one, question 1. Looking only at the numbers, which movements would "
           "you want explained, and what would you challenge?",
           "Question 2. Before you read it, how sound do you expect the machine's "
           "explanation to be?",
           "Question 3. How confident are you that you will catch what is wrong in it?",
           "Question 4. Have you reviewed or prepared a month-end close before?"]
for i in range(SLOTS):
    HEADERS.append(CALL_TITLES[i])
    HEADERS.append(WHY_TITLES[i])
HEADERS += ["After the list. Now that you have seen the challenges, how confident are "
            "you that you caught what was wrong?",
            "Question A. Which of your own calls from round one did the machine's list "
            "also raise?",
            "Question B. What did the list catch that you had missed, and why do you "
            "think you missed it?",
            "Question C. One thing you will do differently the next time you review an "
            "explanation a machine drafted.",
            "Question D. About how many minutes did this take? Par is ten."]

NOTE = "Not collected. The ledger screen is orientation only in this version."
NOT_ASKED = "not asked"
PLACEHOLDERS = ("3", "5", "Once or twice", "5")
PRODUCT = "second-pass-drill 1.6.1"
NOTICE = "notice-2026-09-13"
HOLD = "the figure and reason hold"


def version_line(test=False):
    return ("Product: %s. Notice: %s. Mode: round one practice, round two assessment%s"
            % (PRODUCT, NOTICE, ". TEST ATTEMPT, exclude from reports." if test else "."))


def case_line(run_id, one, lines, two="brightwater-v5"):
    return ("Case: %s, version %s (practice, %d lines) and %s (assessment, 5 lines), dated "
            "2026-09-13, loaded from cases/ files." % (run_id, one, lines, two))


OWN_CASE_LINE = ("Case: own:Ridgeline:2, version ridgeline-own-2 (practice, 14 lines) "
                 "and brightwater-v5 (assessment, 5 lines), dated 2026-09-13, loaded "
                 "from this browser, written by author.html.")
OLD_CASE_LINE = ("Cases: halyard-v3 and brightwater-v2, dated 2026-09-12, loaded from "
                 "cases/ files.")

RIGHT_CHIP = {
    "arithmetic": ["figure does not tie"],
    "timing": ["wrong period"],
    "wrong direction": ["direction wrong"],
    "unsupported driver": ["no source on file"],
    "unsupported attribution": ["wrong account", "no source on file"],
    "wrong account": ["wrong account"],
    "no explanation": ["nothing written where owed"],
    "clean line": [HOLD],
}
WORDS = {
    "arithmetic": ["the subtraction does not tie to the ledger",
                   "186 less 121 is 65, not 6.5",
                   "the number in the sentence is not the number in the column"],
    "timing": ["finished in June and still running in August cannot both hold",
               "one program, two end dates",
               "which June work was actually performed"],
    "wrong direction": ["declined next to a higher balance",
                        "it went up, not down",
                        "the word and the column point opposite ways"],
    "unsupported driver": ["no bridge behind the depot story",
                           "nothing on file ties the ramp to the 372",
                           "depreciation never moved, so the equipment story is thin"],
    "unsupported attribution": ["the freight moved into the price and nobody says so",
                                "two revenue lines and no link between them",
                                "ask for the billing bridge by customer"],
    "wrong account": ["a laptop order is not a subscription",
                      "that spend belongs in another account",
                      "the account and the sentence describe different things"],
    "no explanation": ["nothing written on a line that clears both legs",
                       "silence on 72,500",
                       "no sentence at all here"],
    "clean line": ["the percentage pulled me in",
                   "big percentage, small dollars",
                   "I wanted a document that was already on file"],
}


def post(card, call):
    return card["post_flag"] if call == "flag" else card["post_stand"]


def chips_for(card, call, style):
    if style == "everything is unsourced":
        return ["no source on file"] if call == "flag" else [HOLD]
    if call == card["key"]:
        chips = list(RIGHT_CHIP[card["type"]]) if call == "flag" else [HOLD]
    elif call == "flag":
        chips = ["no source on file"]
    else:
        chips = [HOLD]
    if style == "two chips" and call == "flag" and "no source on file" not in chips:
        chips.append("no source on file")
    return chips


def basis_text(chips, words):
    out = "Basis: " + ("; ".join(chips) if chips else "none recorded")
    if words:
        out += " | Words: " + words
    return out


def agrees(chips, card):
    return reason_agrees(chips, card["basis_key"]) if card["basis_key"] else False


def why(card, call, chips, words):
    """A Why cell exactly as index.html builds it in payload()."""
    return (basis_text(chips, words) +
            " || Line %d, account %s. Called: %s. Key: %s. Type: %s. %s"
            " Reason: %s Key basis: %s."
            % (card["n"], card["acct"], call, card["key"], card["type"],
               "Correct." if call == card["key"] else "Missed.",
               "agrees." if agrees(chips, card) else "does not agree.",
               "; ".join(card["basis_key"] or [])))


def why_old(card, call):
    """The shape a row filed before 13 September 2026 carries: metadata only."""
    return ("Line %d, account %s. Called: %s. Key: %s. Type: %s."
            % (card["n"], card["acct"], call, card["key"], card["type"]))


def points_and_rank(cards, calls, chips_by_line):
    """The page's points and ladder, as index.html computes them on any case."""
    pt_call, pt_reason, pt_streak, pt_cover, streak_from = 100, 50, 25, 75, 3
    cover = {"unsupported driver", "unsupported attribution"}
    points = top = run = top_run = 0
    for i, card in enumerate(cards):
        top += pt_call + pt_reason
        top_run += 1
        if top_run >= streak_from:
            top += pt_streak
        if card["key"] == "flag" and card["type"] in cover:
            top += pt_cover
        if calls[i] != card["key"]:
            run = 0
            continue
        points += pt_call
        if agrees(chips_by_line[i], card):
            points += pt_reason
        run += 1
        if run >= streak_from:
            points += pt_streak
        if card["key"] == "flag" and card["type"] in cover:
            points += pt_cover
    ladder = [("Trainee", 0), ("Staff", round(top * 0.34)), ("Senior", round(top * 0.57)),
              ("Manager", round(top * 0.76)), ("Partner", round(top * 0.95))]
    rank = ladder[0][0]
    for name, at in ladder:
        if points >= at:
            rank = name
    return points, rank


def summary_b(cards, calls, streak, chips_by_line, attempt_id, run_index, r2_reason):
    n = len(cards)
    missed = [i for i in range(n) if calls[i] != cards[i]["key"]]
    caught = sum(1 for i in range(n) if cards[i]["key"] == "flag" and calls[i] == "flag")
    cleared = sum(1 for i in range(n) if cards[i]["key"] == "stand" and calls[i] == "stand")
    false_flags = sum(1 for i in range(n) if cards[i]["key"] == "stand" and calls[i] == "flag")
    reason_right = sum(1 for i in range(n) if agrees(chips_by_line[i], cards[i]))
    points, rank = points_and_rank(cards, calls, chips_by_line)
    lines = ("Lines missed: " + "; ".join("%d %s (%s)" % (cards[i]["n"], cards[i]["acct"],
                                                         cards[i]["type"]) for i in missed) + "."
             if missed else "No lines missed.")
    head = ("Attempt id: %s, run %d in this tab. Reason score: %d of %d in round one and "
            "%d of 5 on the fresh case. A reason counts as right when every chip tapped "
            "is in the card's basis key and at least one was tapped. It is scored apart "
            "from the call." % (attempt_id, run_index, reason_right, n, r2_reason))
    return (head + " " + lines + " Pattern: mixed. Result: right call %d of %d, right "
            "reason %d of %d, %d caught, %d let stand correctly, %d false flag%s, "
            "%s points, rank %s. Four questions on the form (expected quality, "
            "confidence before, confidence after, close experience) are not asked in "
            "this version. They carry a placeholder value the question accepts and are "
            "not participant answers. Longest run of correct calls: %d."
            % (caught + cleared, n, reason_right, n, caught, cleared, false_flags,
               "" if false_flags == 1 else "s", "{:,}".format(points), rank, streak))


def fresh_tail(fresh):
    return ("Fresh case: %s, case version %s, %d lines, run as an assessment with no "
            "feedback between lines. A company the player had not seen. Not a player answer "
            "to question C." % (fresh["company"], fresh["version"], len(fresh["cards"])))


def clean_answer(text):
    """explainClean() in index.html: no bars or line breaks, and "none" for an empty answer."""
    out = " ".join(str(text or "").replace("|", " ").split())
    return out or "none"


def r2_cell(calls, seconds, style="right", fresh=FRESH, explain=None):
    """Question C as r2Line() builds it: the round two string, then the basis by line.

    explain, when given, is one (evidence, period, action) triple per fresh line, posted
    between the basis and the reason verdict as brightwater-v6 assessment runs post it."""
    bas, reason_right, right = [], 0, 0
    letters = key_letters(fresh)
    for j, letter in enumerate(calls):
        card = fresh["cards"][j]
        call = "flag" if letter == "F" else "stand"
        if letter == letters[j]:
            right += 1
        chips = chips_for(card, call, style)
        words = WORDS[card["type"]][j % 3] if (call == "flag" and j % 2 == 0) else ""
        ok = agrees(chips, card)
        reason_right += 1 if ok else 0
        written = ""
        if explain is not None:
            evidence, period, action = explain[j]
            written = " | Evidence: %s | Period: %s | Action: %s" % (
                clean_answer(evidence), clean_answer(period), clean_answer(action))
        bas.append("%d: %s%s | Reason: %s | Key basis: %s"
                   % (j + 1, basis_text(chips, words), written,
                      "agrees" if ok else "does not agree", "; ".join(card["basis_key"])))
    text = ("Round2: right call %d/5, right reason %d/5; calls %s; key %s; seconds %d. "
            "Round2 basis, by line: %s. %s"
            % (right, reason_right, calls, letters, seconds, " || ".join(bas),
               fresh_tail(fresh)))
    return text, reason_right


def row(ts, codename, calls, orgs, minutes, streak, cases=HALYARD, round2=None,
        style="plain", words_on=(), old_shape=False, stale_column=None,
        prepicks=("4000", "5000", "6000"), attempt=None, run_index=1, line=None,
        test=False, words_marker=None):
    cards = cases["cards"]
    r2_text, r2_reason = (round2 if round2 else (None, 0))
    picks = ("Prepicks: " + "; ".join(prepicks) + "." if prepicks else "Prepicks: skipped.")
    if old_shape:
        out = [ts, codename, NOTE, PLACEHOLDERS[0], PLACEHOLDERS[1], PLACEHOLDERS[2]]
    else:
        out = [ts, codename, picks, NOT_ASKED, NOT_ASKED, NOT_ASKED]
    chips_by_line = []
    for i in range(SLOTS):
        if i >= len(cards):
            out += ["", ""]
            continue
        card, call = cards[i], calls[i]
        posted = post(card, call)
        if stale_column == i:
            posted = post(card, "flag" if call == "stand" else "stand")
        out.append(posted)
        chips = chips_for(card, call, style)
        chips_by_line.append(chips)
        if old_shape:
            out.append(why_old(card, call))
            continue
        words = words_marker or ""
        if not words and call == "flag" and i in words_on:
            words = WORDS[card["type"]][i % 3]
        out.append(why(card, call, chips, words))
    out += [PLACEHOLDERS[3] if old_shape else NOT_ASKED,
            "Organizations: " + "; ".join(orgs) + ". " + version_line(test) + " " +
            (line or case_line(cases["version"].split("-")[0], cases["version"], len(cards))),
            summary_b(cards, calls, streak, chips_by_line,
                      attempt or ("att-" + codename.lower().replace(" ", "")[:10]),
                      run_index, r2_reason),
            r2_text or ("Round2: no fresh case on this run. " + NOTE),
            str(minutes)]
    return out


def misses(cases, miss_indexes):
    calls = [c["key"] for c in cases["cards"]]
    for i in miss_indexes:
        calls[i] = "flag" if calls[i] == "stand" else "stand"
    return calls


# Invented written explanations for the brightwater-v6 rows, one (evidence, period, action)
# triple per fresh line in card order. They are written to be scored, not to be right.
EXPLAIN_COLDREAD = [
    ("nothing on file shows implant cases or a surgical suite in June",
     "the supply spend has to belong to cases performed in June",
     "ask for the June implant case log and the supplier invoices"),
    ("the hiring record and the chair opening on 1 June are on file",
     "the wages follow a chair that opened inside the month",
     "no request, the line stands"),
    ("the plan schedule on file is dated May and lists no June starts",
     "June billing needs plans that started in June",
     "ask for the June plan start list"),
    ("nothing on file shows the associates' June patient schedules",
     "a May start only matters if June visits actually rose",
     "ask for the June appointment counts by dentist"),
    ("the mailer invoice dated the first week of June",
     "the spend and the delivery fall in the same month",
     "no request, the line stands"),
]
EXPLAIN_SIGNOFF = [
    ("no case log for the surgical suite", "June supplies", "request the case log"),
    ("the chair opened 1 June", "inside June", "none needed"),
    ("the plan schedule on file", "June", ""),
    ("no schedules for the two associates", "the full schedule is claimed for June",
     "ask for the June schedules"),
    ("the mailer invoice", "delivered in June", "stand"),
]


ROWS = [
    # perfect run, a clean sweep of the fresh case, words on four of the flags
    dict(ts="2026/09/15 9:02:11", codename="REDLINE", calls=misses(HALYARD, []),
         orgs=["ACFE"], minutes=7, streak=14, round2=r2_cell("FSFFS", 61),
         words_on=(0, 1, 6, 10)),
    # misses the two unsupported lines, taps two chips on every flag
    dict(ts="2026/09/15 9:14:40", codename="BLUEBOOK", calls=misses(HALYARD, [11, 13]),
         orgs=["Beta Alpha Psi", "ACFE"], minutes=11, streak=8, style="two chips",
         words_on=(2, 7), round2=r2_cell("FSFSS", 70)),
    # misses timing and no explanation, one false flag on a clean line
    dict(ts="2026/09/15 9:31:05", codename="TIEOUT", calls=misses(HALYARD, [1, 10, 8]),
         orgs=["NABA"], minutes=13, streak=6, words_on=(8,), attempt="att-tieout-01",
         round2=r2_cell("FSFFF", 90)),
    # a test row that must be dropped
    dict(ts="2026/09/15 9:33:00", codename="TEST-AGENT-DELETE",
         calls=misses(HALYARD, [0, 1, 2]), orgs=["ACFE"], minutes=2, streak=3),
    # misses arithmetic on card 8, false flags two clean lines
    dict(ts="2026/09/15 9:48:22", codename="FOOTNOTE", calls=misses(HALYARD, [7, 3, 5]),
         orgs=["AAA", "GMU Student"], minutes=9, streak=7, words_on=(3, 5, 11),
         round2=r2_cell("FSFFS", 75)),
    # the Professor chip, and a fresh case run that drops two lines
    dict(ts="2026/09/15 10:02:13", codename="MARGINCALL", calls=misses(HALYARD, [12]),
         orgs=["Professor", "ACFE"], minutes=6, streak=11,
         round2=r2_cell("FSSFF", 97), words_on=(12, 13)),
    # flags all fourteen and reaches for the same chip every time
    dict(ts="2026/09/15 10:15:47", codename="SHOTGUN", calls=["flag"] * 14,
         orgs=["GMU Student"], minutes=4, streak=3, style="everything is unsourced",
         round2=r2_cell("FFFFF", 40, style="everything is unsourced")),
    # second test row
    dict(ts="2026/09/15 10:16:02", codename="Test Play", calls=misses(HALYARD, [2, 4]),
         orgs=["ASM"], minutes=3, streak=4),
    # the same attempt sent twice: one attempt identifier, two rows
    dict(ts="2026/09/15 10:29:31", codename="TIEOUT", calls=misses(HALYARD, [1, 10, 8]),
         orgs=["NABA"], minutes=13, streak=6, attempt="att-tieout-01", run_index=1,
         words_on=(8,), round2=r2_cell("FSFFF", 90)),
    # a row filed before 13 September 2026 on halyard-v3: fixed intake values, no basis
    dict(ts="2026/09/11 10:44:09", codename="CARRYOVER", cases=HALYARD_OLD,
         calls=misses(HALYARD_OLD, [0, 2, 6, 9, 12]), orgs=["Beta Alpha Psi"], minutes=15,
         streak=4, old_shape=True, line=OLD_CASE_LINE),
    # a fresh case run, and one Accept or Reject cell that contradicts its Why field
    dict(ts="2026/09/15 11:01:55", codename="HARDCLOSE", calls=misses(HALYARD, [4, 10]),
         orgs=["ACFE", "Beta Alpha Psi"], minutes=10, streak=9,
         round2=r2_cell("FSFFS", 84, style="everything is unsourced"),
         words_on=(1, 2), stale_column=6),
    # middling run
    dict(ts="2026/09/15 11:20:18", codename="DEPOTNINE", calls=misses(HALYARD, [3, 11, 13]),
         orgs=["ASM", "ACFE"], minutes=12, streak=5, words_on=(0, 10), prepicks=(),
         round2=r2_cell("FSFFS", 66)),
    # a run on a case authored in the player's own browser: refused, its key is not in cases/
    dict(ts="2026/09/15 11:38:44", codename="RIDGEWAY", calls=misses(HALYARD, [6, 9]),
         orgs=["Outside Mason"], minutes=9, streak=8, words_on=(1, 7),
         line=OWN_CASE_LINE, round2=r2_cell("FSFFS", 73)),
    # the two newer test codenames
    dict(ts="2026/09/15 11:44:02", codename="Test Harness", calls=misses(HALYARD, [1]),
         orgs=["ACFE"], minutes=1, streak=2),
    dict(ts="2026/09/15 11:45:30", codename="PLACEHOLDER-CHECK-DELETE",
         cases=HALYARD_OLD, calls=misses(HALYARD_OLD, []), orgs=["ACFE"], minutes=1,
         streak=14, old_shape=True, line=OLD_CASE_LINE),
    # BLUEBOOK comes back an hour later with a new attempt identifier: a reattempt
    dict(ts="2026/09/15 12:20:00", codename="BLUEBOOK", calls=misses(HALYARD, []),
         orgs=["Beta Alpha Psi", "ACFE"], minutes=6, streak=14, attempt="att-bluebook-02",
         run_index=2, words_on=(0,), round2=r2_cell("FSFFS", 45)),
    # a Kestrel run, scored against kestrel-v1 and reported as its own case set
    dict(ts="2026/09/15 12:31:10", codename="LEDGERHAWK", cases=KESTREL,
         calls=misses(KESTREL, [9, 3]), orgs=["Outside Mason"], minutes=11, streak=6,
         words_on=(0, 1, 11), round2=r2_cell("FSFFS", 80)),
    # a second Kestrel run
    dict(ts="2026/09/15 12:40:44", codename="QUICKTIE", cases=KESTREL,
         calls=misses(KESTREL, []), orgs=["Beta Alpha Psi"], minutes=9, streak=12,
         words_on=(5,), round2=r2_cell("FSSFS", 71)),
    # a version with no case file: refused, never scored against another key
    dict(ts="2026/09/15 12:45:00", codename="OLDKEY", calls=misses(HALYARD, [0]),
         orgs=["ACFE"], minutes=8, streak=9,
         line=case_line("halyard", "halyard-v9", 14), round2=r2_cell("FSFFS", 60)),
    # the page marked this run as a test attempt
    dict(ts="2026/09/15 12:50:00", codename="FIELDCHECK", calls=misses(HALYARD, []),
         orgs=["ACFE"], minutes=5, streak=14, test=True),
    # brightwater-v6: every fresh call carries the three-part written explanation, and the
    # run is reported as its own case set rather than pooled with the brightwater-v5 runs
    dict(ts="2026/09/21 9:05:12", codename="COLDREAD", calls=misses(HALYARD, [11]),
         orgs=["Beta Alpha Psi"], minutes=16, streak=10, words_on=(0, 2),
         line=case_line("halyard", "halyard-v4", 14, two="brightwater-v6"),
         round2=r2_cell("FSFFS", 212, fresh=FRESH6, explain=EXPLAIN_COLDREAD)),
    # a second brightwater-v6 run: one wrong call, and one explanation that stops at the
    # document without saying what to request
    dict(ts="2026/09/21 9:40:37", codename="SIGNOFF", calls=misses(HALYARD, [2, 10]),
         orgs=["Outside Mason"], minutes=19, streak=7, words_on=(1,),
         line=case_line("halyard", "halyard-v4", 14, two="brightwater-v6"),
         round2=r2_cell("FSSFS", 260, fresh=FRESH6, explain=EXPLAIN_SIGNOFF)),
    # a row in the shape of the third review's synthetic records
    dict(ts="2026/09/15 12:55:00", codename="Synthetic same participant",
         calls=misses(HALYARD, []), orgs=["ACFE"], minutes=5, streak=14, attempt="audit-a",
         words_marker="Synthetic test only"),
]

ROSTER = [
    ("P09", "COLDREAD", "yes", "student"),
    ("P10", "SIGNOFF", "yes", "practitioner"),
    ("P01", "REDLINE", "yes", "student"),
    ("P02", "BLUEBOOK", "yes", "student"),
    ("P03", "TIEOUT", "yes", "practitioner"),
    ("P04", "FOOTNOTE", "no", "student"),
    ("P05", "MARGINCALL", "yes", "educator"),
    ("P06", "HARDCLOSE", "yes", "student"),
    ("P06", "LEDGERHAWK", "yes", "student"),
    ("P07", "DEPOTNINE", "yes", ""),
    ("P08", "NOSHOW", "yes", "student"),
]


def main():
    path = os.path.join(HERE, "findings-sample.csv")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        for spec in ROWS:
            writer.writerow(row(**spec))
    roster = os.path.join(HERE, "findings-sample-roster.csv")
    with open(roster, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["participant", "codename", "consent", "role"])
        writer.writerows(ROSTER)
    print("Wrote %s with %d responses and %s with %d roster rows."
          % (path, len(ROWS), roster, len(ROSTER)))


if __name__ == "__main__":
    main()
