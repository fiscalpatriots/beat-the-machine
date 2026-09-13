#!/usr/bin/env python3
"""Builds findings-sample.csv: the form's real headers and fourteen fake responses.

The cells are written the way index.html writes them on 13 September 2026: the ledger
picks in the round one question, a basis, the page's own reason verdict and the card's
basis key in every Why field, the attempt identifier and the reason score in question B,
and the Round2 string with its per line basis at the tail of question C. Two rows are
left in older shapes on purpose, so the script can be seen handling them, and one row is
an authored case run so the own: identifier is exercised.

Only for testing findings.py. Delete it or leave it, it touches nothing else.
"""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from findings import CARDS, CARDS2, CALL_TITLES, WHY_TITLES  # noqa

HEADERS = ["Timestamp", "Codename",
           "Round one, question 1. Looking only at the numbers, which movements would "
           "you want explained, and what would you challenge?",
           "Question 2. Before you read it, how sound do you expect the machine's "
           "explanation to be?",
           "Question 3. How confident are you that you will catch what is wrong in it?",
           "Question 4. Have you reviewed or prepared a month-end close before?"]
for i in range(14):
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
VERSION_LINE = ("Product: %s. Notice: %s. Mode: round one practice, round two "
                "assessment." % (PRODUCT, NOTICE))
CASE_LINE = ("Case: halyard, version halyard-v4 (practice, 14 lines) and brightwater-v4 "
             "(assessment, 5 lines), dated 2026-09-13, loaded from cases/ files.")
OWN_CASE_LINE = ("Case: own:Ridgeline:2, version ridgeline-own-2 (practice, 14 lines) "
                 "and brightwater-v4 (assessment, 5 lines), dated 2026-09-13, loaded "
                 "from this browser, written by author.html.")
OLD_CASE_LINE = ("Cases: halyard-v3 and brightwater-v2, dated 2026-09-12, loaded from "
                 "cases/ files.")
KEY = [c[3] for c in CARDS]
TYPE = [c[4] for c in CARDS]
BASIS_KEY = [c[6] for c in CARDS]
HOLD = "the figure and reason hold"
FRESH_LETTERS = "".join("F" if c[3] == "flag" else "S" for c in CARDS2)


def reason_agrees(chips, key):
    return bool(chips) and all(c in key for c in chips)

# The chip a player reaches for when the reading is right, by error type. A stand on a
# clean line holds; a flag picks the chip that names what the player thinks is wrong.
RIGHT_CHIP = {
    "arithmetic": ["figure does not tie"],
    "timing": ["wrong period"],
    "wrong direction": ["direction wrong"],
    "unsupported driver": ["no source on file"],
    "unsupported attribution": ["wrong account", "no source on file"],
    "no explanation": ["nothing written where owed"],
    "clean line": [HOLD],
}
# What a player reaches for when the call is wrong: a flag on a clean line, or a stand
# on a planted problem.
WRONG_CHIP = {
    "flagged a clean line": ["no source on file"],
    "stood on a problem": [HOLD],
}

# Verbatim lines of a player's own words, offered on a flag only, by error type.
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
    "no explanation": ["nothing written on a line that clears both legs",
                       "silence on 72,500",
                       "no sentence at all here"],
    "clean line": ["the percentage pulled me in",
                   "big percentage, small dollars",
                   "I wanted a document that was already on file"],
}


def post(i, call):
    flag_value = CARDS[i][5]
    return flag_value if call == "flag" else ("Accept" if flag_value == "Reject" else "Reject")


def chips_for(i, call, style):
    """The chips a player taps on line i, given the call and how they play."""
    etype = TYPE[i]
    if style == "everything is unsourced":
        return ["no source on file"] if call == "flag" else [HOLD]
    if call == KEY[i]:
        chips = list(RIGHT_CHIP[etype]) if call == "flag" else [HOLD]
    elif call == "flag":
        chips = list(WRONG_CHIP["flagged a clean line"])
    else:
        chips = list(WRONG_CHIP["stood on a problem"])
    if style == "two chips" and call == "flag":
        extra = "no source on file"
        if extra not in chips:
            chips.append(extra)
    return chips


def basis_text(chips, words):
    out = "Basis: " + ("; ".join(chips) if chips else "none recorded")
    if words:
        out += " | Words: " + words
    return out


def why(i, call, chips, words):
    """A Why cell exactly as index.html builds it in payload()."""
    c = CARDS[i]
    return (basis_text(chips, words) +
            " || Line %d, account %s. Called: %s. Key: %s. Type: %s. %s"
            " Reason: %s Key basis: %s."
            % (c[0], c[1], call, c[3], c[4],
               "Correct." if call == c[3] else "Missed.",
               "agrees." if reason_agrees(chips, c[6]) else "does not agree.",
               "; ".join(c[6])))


def why_old(i, call):
    """The shape a row filed before 13 September 2026 carries: metadata only."""
    c = CARDS[i]
    return ("Line %d, account %s. Called: %s. Key: %s. Type: %s."
            % (c[0], c[1], call, c[3], c[4]))


def points_and_rank(calls, chips_by_line):
    """The page's own points and ladder, read off the same rules index.html uses."""
    pt_call, pt_reason, pt_streak, pt_cover, streak_from = 100, 50, 25, 75, 3
    cover = {"unsupported driver", "unsupported attribution"}
    points, run = 0, 0
    for i in range(14):
        if calls[i] != KEY[i]:
            run = 0
            continue
        points += pt_call
        if reason_agrees(chips_by_line[i], BASIS_KEY[i]):
            points += pt_reason
        run += 1
        if run >= streak_from:
            points += pt_streak
        if KEY[i] == "flag" and TYPE[i] in cover:
            points += pt_cover
    top, run = 0, 0
    for i in range(14):
        top += pt_call + pt_reason
        run += 1
        if run >= streak_from:
            top += pt_streak
        if KEY[i] == "flag" and TYPE[i] in cover:
            top += pt_cover
    ladder = [("Trainee", 0), ("Staff", round(top * 0.34)), ("Senior", round(top * 0.57)),
              ("Manager", round(top * 0.76)), ("Partner", round(top * 0.95))]
    rank = ladder[0][0]
    for name, at in ladder:
        if points >= at:
            rank = name
    return points, rank


def summary_b(calls, streak, chips_by_line, attempt_id, run_index, r2_reason):
    missed = [i for i in range(14) if calls[i] != KEY[i]]
    caught = sum(1 for i in range(14) if KEY[i] == "flag" and calls[i] == "flag")
    cleared = sum(1 for i in range(14) if KEY[i] == "stand" and calls[i] == "stand")
    false_flags = sum(1 for i in range(14) if KEY[i] == "stand" and calls[i] == "flag")
    score = caught + cleared
    reason_right = sum(1 for i in range(14)
                       if reason_agrees(chips_by_line[i], BASIS_KEY[i]))
    points, rank = points_and_rank(calls, chips_by_line)
    lines = ("Lines missed: " + "; ".join("%d %s (%s)" % (CARDS[i][0], CARDS[i][1], CARDS[i][4])
                                          for i in missed) + "."
             if missed else "No lines missed.")
    head = ("Attempt id: %s, run %d in this tab. Reason score: %d of 14 in round one and "
            "%d of 5 on the fresh case. A reason counts as right when every chip tapped "
            "is in the card's basis key and at least one was tapped. It is scored apart "
            "from the call and it does not move the rank."
            % (attempt_id, run_index, reason_right, r2_reason))
    return (head + " " + lines + " Pattern: mixed. Result: right call %d of 14, right "
            "reason %d of 14, %d caught, %d let stand correctly, %d false flag%s, "
            "%s points, rank %s. Four questions on the form (expected quality, "
            "confidence before, confidence after, close experience) are not asked in "
            "this version. They carry a placeholder value the question accepts and are "
            "not participant answers. Longest run of correct calls: %d."
            % (score, reason_right, caught, cleared, false_flags,
               "" if false_flags == 1 else "s", "{:,}".format(points), rank, streak))


FRESH_TAIL = ("Fresh case: Brightwater Dental Partners, PLLC, case version "
              "brightwater-v4, 5 lines, run as an assessment with no feedback between "
              "lines. A company the player had not seen. Not a player answer to "
              "question C.")


def r2_cell(right, calls, seconds, style="right"):
    """Question C as r2Line() builds it: the round two string, then the basis by line."""
    bas, reason_right = [], 0
    for j, letter in enumerate(calls):
        call = "flag" if letter == "F" else "stand"
        key, etype, bkey = CARDS2[j][3], CARDS2[j][4], CARDS2[j][5]
        if style == "everything is unsourced":
            chips = ["no source on file"] if call == "flag" else [HOLD]
        elif call == key:
            chips = list(RIGHT_CHIP[etype]) if call == "flag" else [HOLD]
        elif call == "flag":
            chips = list(WRONG_CHIP["flagged a clean line"])
        else:
            chips = list(WRONG_CHIP["stood on a problem"])
        words = WORDS[etype][j % len(WORDS[etype])] if (call == "flag" and j % 2 == 0) else ""
        agrees = reason_agrees(chips, bkey)
        if agrees:
            reason_right += 1
        bas.append("%d: %s | Reason: %s | Key basis: %s"
                   % (j + 1, basis_text(chips, words),
                      "agrees" if agrees else "does not agree", "; ".join(bkey)))
    cell = ("Round2: right call %d/5, right reason %d/5; calls %s; key %s; seconds %d. "
            "Round2 basis, by line: %s. %s"
            % (right, reason_right, calls, FRESH_LETTERS, seconds,
               " || ".join(bas), FRESH_TAIL))
    return cell, reason_right


def row(ts, codename, calls, orgs, minutes, streak, round2=None, style="plain",
        words_on=(), old_shape=False, stale_column=None, prepicks=("4000", "5000", "6000"),
        attempt=None, run_index=1, authored=False):
    """One response. stale_column forces the Accept or Reject cell on that line to
    contradict the call in the Why field, which is the cross-check the script reports."""
    r2_cellstr, r2_reason = (round2 if round2 else (None, 0))
    picks = ("Prepicks: " + "; ".join(prepicks) + "." if prepicks else "Prepicks: skipped.")
    if old_shape:
        out = [ts, codename, NOTE, PLACEHOLDERS[0], PLACEHOLDERS[1], PLACEHOLDERS[2]]
    else:
        out = [ts, codename, picks, NOT_ASKED, NOT_ASKED, NOT_ASKED]
    chips_by_line = []
    for i in range(14):
        call = calls[i]
        posted = post(i, call)
        if stale_column == i:
            posted = post(i, "flag" if call == "stand" else "stand")
        out.append(posted)
        chips = chips_for(i, call, style)
        chips_by_line.append(chips)
        if old_shape:
            out.append(why_old(i, call))
            continue
        words = ""
        if call == "flag" and i in words_on:
            pool = WORDS[TYPE[i]]
            words = pool[i % len(pool)]
        out.append(why(i, call, chips, words))
    case_line = OLD_CASE_LINE if old_shape else (OWN_CASE_LINE if authored else CASE_LINE)
    out += [PLACEHOLDERS[3] if old_shape else NOT_ASKED,
            "Organizations: " + "; ".join(orgs) + ". " + VERSION_LINE + " " + case_line,
            summary_b(calls, streak, chips_by_line,
                      attempt or ("att-" + codename.lower().replace(" ", "")[:10]),
                      run_index, r2_reason),
            r2_cellstr or ("Round2: no fresh case on this run. " + NOTE),
            str(minutes)]
    return out


def calls_with_misses(miss_indexes):
    calls = list(KEY)
    for i in miss_indexes:
        calls[i] = "flag" if KEY[i] == "stand" else "stand"
    return calls


ROWS = [
    # perfect run, a clean sweep of the fresh case, words on four of the flags
    dict(ts="2026/09/15 9:02:11", codename="REDLINE", calls=calls_with_misses([]),
         orgs=["ACFE"], minutes=7, streak=14, round2=r2_cell(5, "FSFFS", 61),
         words_on=(0, 1, 6, 10)),
    # misses the two unsupported lines, taps two chips on every flag
    dict(ts="2026/09/15 9:14:40", codename="BLUEBOOK", calls=calls_with_misses([11, 13]),
         orgs=["Beta Alpha Psi", "ACFE"], minutes=11, streak=8, style="two chips",
         words_on=(2, 7)),
    # misses timing and no explanation, one false flag on a clean line
    dict(ts="2026/09/15 9:31:05", codename="TIEOUT", calls=calls_with_misses([1, 10, 8]),
         orgs=["NABA"], minutes=13, streak=6, words_on=(8,), attempt="att-tieout-01"),
    # a test row that must be dropped
    dict(ts="2026/09/15 9:33:00", codename="TEST-AGENT-DELETE",
         calls=calls_with_misses([0, 1, 2]), orgs=["ACFE"], minutes=2, streak=3),
    # misses arithmetic on card 8, false flags two clean lines
    dict(ts="2026/09/15 9:48:22", codename="FOOTNOTE", calls=calls_with_misses([7, 3, 5]),
         orgs=["AAA", "GMU Student"], minutes=9, streak=7, words_on=(3, 5, 11)),
    # the professor, and a fresh case run that drops two lines
    dict(ts="2026/09/15 10:02:13", codename="MARGINCALL", calls=calls_with_misses([12]),
         orgs=["Professor", "ACFE"], minutes=6, streak=11,
         round2=r2_cell(3, "FSSFF", 97), words_on=(12, 13)),
    # flags all fourteen and reaches for the same chip every time
    dict(ts="2026/09/15 10:15:47", codename="SHOTGUN", calls=["flag"] * 14,
         orgs=["GMU Student"], minutes=4, streak=3, style="everything is unsourced"),
    # second test row
    dict(ts="2026/09/15 10:16:02", codename="Test Play", calls=calls_with_misses([2, 4]),
         orgs=["ASM"], minutes=3, streak=4),
    # the same attempt sent twice: one attempt identifier, two rows
    dict(ts="2026/09/15 10:29:31", codename="TIEOUT", calls=calls_with_misses([1, 10, 8]),
         orgs=["NABA"], minutes=13, streak=6, attempt="att-tieout-01", run_index=2,
         words_on=(8,)),
    # a row filed before 13 September 2026: fixed intake values, no basis, no case line
    dict(ts="2026/09/11 10:44:09", codename="CARRYOVER",
         calls=calls_with_misses([0, 2, 6, 9, 12]), orgs=["Beta Alpha Psi"], minutes=15,
         streak=4, old_shape=True),
    # the round two player, and one Accept or Reject cell that contradicts its Why field
    dict(ts="2026/09/15 11:01:55", codename="HARDCLOSE", calls=calls_with_misses([4, 10]),
         orgs=["ACFE", "Beta Alpha Psi"], minutes=10, streak=9,
         round2=r2_cell(4, "FSFFS", 84, style="everything is unsourced"),
         words_on=(1, 2), stale_column=6),
    # middling run
    dict(ts="2026/09/15 11:20:18", codename="DEPOTNINE",
         calls=calls_with_misses([3, 11, 13]), orgs=["ASM", "ACFE"], minutes=12,
         streak=5, words_on=(0, 10), prepicks=()),
    # a run on a case the player authored in their own browser
    dict(ts="2026/09/15 11:38:44", codename="RIDGEWAY",
         calls=calls_with_misses([6, 9]), orgs=["Outside Mason"], minutes=9, streak=8,
         words_on=(1, 7), authored=True, round2=r2_cell(4, "FSFFS", 73)),
    # the two new test codenames
    dict(ts="2026/09/15 11:44:02", codename="Test Harness",
         calls=calls_with_misses([1]), orgs=["ACFE"], minutes=1, streak=2),
    dict(ts="2026/09/15 11:45:30", codename="PLACEHOLDER-CHECK-DELETE",
         calls=calls_with_misses([]), orgs=["ACFE"], minutes=1, streak=14,
         old_shape=True),
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "findings-sample.csv")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(HEADERS)
        for spec in ROWS:
            writer.writerow(row(**spec))
    print("Wrote %s with %d responses." % (path, len(ROWS)))


if __name__ == "__main__":
    main()
