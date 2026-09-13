#!/usr/bin/env python3
"""Findings for "Second Pass: Beat the Machine".

Reads the Google Form responses CSV (Responses tab, File, Download, CSV) and writes
FINDINGS-<date>.md plus a printed summary.

Usage:
    python findings.py responses.csv
    python findings.py responses.csv --out FINDINGS-sample.md

Columns are matched by the form's question titles, never by position. Any title the
script cannot find is printed under "Columns not found" and the measure that needed it
is skipped rather than guessed.

Since the 13 September 2026 build of the game each Why cell carries the basis the player
gave and the page's own reason verdict ahead of the metadata it computed, question A
carries the case id and both case versions, question B carries the attempt identifier and
the reason score, question C carries the Round2 string and the fresh case basis, and the
four questions the game never asks carry a placeholder. Rows filed before that build carry
the older shapes and are read as well; the four unasked questions are excluded from every
measure in every shape.

The field names printed under "Readout fields" are the names READOUT-TEMPLATE.md prints in
its cells, so a facilitator can copy a value across without translating it. --fields writes
the same set as JSON.

Run it from the repository root:

    python tools/findings.py responses.csv
"""

import argparse
import datetime
import os
import re
import statistics
import sys

# ---------------------------------------------------------------- the answer key
# Source: cases/halyard-v4.json in beat-the-machine, which the page loads at start and
# mirrors in the inline fallback. Key rebalanced 12 Sep 2026 to eight problem lines and
# six clean ones; error types renamed 13 Sep 2026 ("unsupported driver" replaced
# "invented driver", cards 12 and 14 are no longer both "wrong account"). post maps the
# player's call to the value the form receives. Card 1 is inverted on purpose: its
# question asks whether the player agrees nothing is owed on 4200, so flagging that line
# posts Reject. The last column is the card's basis key: a reason counts as right when at
# least one chip was tapped and every chip tapped is in that list.
CARDS = [
    # n, account, name, key, error type, post-value that means "flag", basis key
(1,  "4200", "Freight billed to customers",            "flag",  "arithmetic",       "Reject",
     ["figure does not tie", "nothing written where owed"]),
    (2,  "6200", "Repairs and maintenance, depots",        "flag",  "timing",           "Accept",
     ["wrong period", "no source on file"]),
    (3,  "5100", "Inbound freight",                        "flag",  "wrong direction",  "Accept",
     ["direction wrong", "no source on file"]),
    (4,  "4100", "Service revenue, equipment maintenance", "stand", "clean line",       "Accept",
     ["the figure and reason hold"]),
    (5,  "6500", "Professional fees",                      "stand", "clean line",       "Accept",
     ["the figure and reason hold"]),
    (6,  "7400", "Inventory shrink adjustment",            "stand", "clean line",       "Accept",
     ["the figure and reason hold"]),
    (7,  "4000", "Product revenue, distribution",          "flag",  "unsupported driver", "Accept",
     ["no source on file"]),
    (8,  "6400", "Bad debt expense",                       "flag",  "arithmetic",       "Accept",
     ["figure does not tie", "no source on file"]),
    (9,  "6100", "Fleet fuel",                             "stand", "clean line",       "Accept",
     ["the figure and reason hold"]),
    (10, "6300", "Software subscriptions",                 "stand", "clean line",       "Accept",
     ["the figure and reason hold"]),
    (11, "6000", "Warehouse wages",                        "flag",  "no explanation",   "Accept",
     ["nothing written where owed", "no source on file"]),
    (12, "4000", "Product revenue, distribution",          "flag",  "unsupported attribution", "Accept",
     ["no source on file"]),
    (13, "5000", "Cost of product sold",                   "stand", "clean line",       "Accept",
     ["the figure and reason hold"]),
    (14, "7100", "Interest expense",                       "flag",  "unsupported driver", "Accept",
     ["no source on file"]),
]

# The fresh case, cases/brightwater-v4.json. Five lines, run as an assessment with no
# feedback between them, and no Why field of their own: the basis for these rides at the
# end of question C. Reordered 13 September 2026 with the v4 key.
CARDS2 = [
    (1, "5210", "Dental supplies and lab fees",   "flag",  "unsupported driver",
     ["no source on file"]),
    (2, "6110", "Hygienist wages",                "stand", "clean line",
     ["the figure and reason hold"]),
    (3, "4220", "Orthodontic plan revenue",       "flag",  "unsupported driver",
     ["wrong period", "no source on file"]),
    (4, "4010", "Patient service revenue, net",   "flag",  "unsupported driver",
     ["no source on file"]),
    (5, "6610", "Marketing and patient outreach", "stand", "clean line",
     ["the figure and reason hold"]),
]

# The full question titles as the form builds them. The CSV header is the title.
CALL_TITLES = [
    "C1. Account 4200 Freight billed to customers, movement $6,500, tag amount",
    "C2. Account 6200 Repairs and maintenance, depots, movement $77,600, sentence S1, tag contradiction",
    "C3. Account 5100 Inbound freight, movement $73,800, sentence S6, tag direction",
    "C4. Account 4100 Service revenue, equipment maintenance, movement $229,000, sentence S9, tag period",
    "C5. Account 6500 Professional fees, movement $7,500, sentence S12, tag driver",
    "C6. Account 7400 Inventory shrink adjustment, movement $2,500, tag threshold",
    "C7. Account 4000 Product revenue, distribution, movement $372,000, sentence S5, tag driver",
    "C8. Account 6400 Bad debt expense, movement $47,000, sentence S2, tag amount",
    "C9. Account 6100 Fleet fuel, movement $5,200, sentence S8, tag period",
    "C10. Account 6300 Software subscriptions, movement $1,600, sentence S3, tag threshold",
    "C11. Account 6000 Warehouse wages, movement $72,500, tag driver",
    "C12. Account 4000 Product revenue, distribution, movement $372,000, sentence S4, tag transfer",
    "C13. Account 5000 Cost of product sold, movement $348,000, sentence S11, tag amount",
    "C14. Account 7100 Interest expense, movement $31,200, sentence S7, tag classification",
]
WHY_TITLES = ["C%d. Why? (optional, one line)" % n for n in range(1, 15)]

CODENAME_TITLE = "Codename"
QA_TITLE = ("Question A. Which of your own calls from round one did the machine's "
            "list also raise?")
QB_TITLE = ("Question B. What did the list catch that you had missed, and why do you "
            "think you missed it?")
QC_TITLE = ("Question C. One thing you will do differently the next time you review an "
            "explanation a machine drafted.")
QD_TITLE = "Question D. About how many minutes did this take? Par is ten."
TIMESTAMP_TITLE = "Timestamp"

# The four questions the form marks required and the three screen path never asks. Until
# 13 September 2026 they carried fixed values (3, 5, 5 and "Once or twice") that landed in
# the sheet looking like answers; since then they carry the literal "not asked". Neither
# form is a player answer, so both are excluded from every measure below.
INTAKE_TITLES = [
    ("Expected quality of the commentary",
     "Question 2. Before you read it, how sound do you expect the machine's explanation "
     "to be?", ["question 2.", "expect"]),
    ("Confidence before the round",
     "Question 3. How confident are you that you will catch what is wrong in it?",
     ["question 3.", "confident"]),
    ("Month end close experience",
     "Question 4. Have you reviewed or prepared a month-end close before?",
     ["question 4.", "close"]),
    ("Confidence after the round",
     "After the list. Now that you have seen the challenges, how confident are you that "
     "you caught what was wrong?", ["after the list", "confident"]),
]
NOT_ASKED = "not asked"

TEST_CODENAMES = {
    "test-agent-delete", "probe-two", "audit-test-delete",
    "rebuild-test-delete", "pages-check-delete", "test play",
    "test harness", "placeholder-check-delete",
}

CHIPS = ["Beta Alpha Psi", "ACFE", "ASM", "NABA", "AAA", "GMU Student", "Professor"]

# The basis chips, from BASIS_FLAG and BASIS_HOLD in index.html. The hold chip is offered
# only on a let it stand, and it sits first in that row.
BASIS_HOLD = "the figure and reason hold"
BASIS_FLAG_CHIPS = ["figure does not tie", "direction wrong", "no source on file",
                    "wrong period", "wrong account", "nothing written where owed"]
BASIS_CHIPS = [BASIS_HOLD] + BASIS_FLAG_CHIPS

PROBLEM = [c for c in CARDS if c[3] == "flag"]
CLEAN = [c for c in CARDS if c[3] == "stand"]


def rank_of(score):
    if score >= 14:
        return "Partner"
    if score == 13:
        return "Manager"
    if score >= 11:
        return "Senior"
    if score >= 9:
        return "Staff"
    return "Trainee"


RANK_ORDER = ["Partner", "Manager", "Senior", "Staff", "Trainee"]


# ---------------------------------------------------------------- reading the CSV
def read_rows(path):
    """Return (list of dicts, list of header strings). Uses pandas if it is installed."""
    try:
        import pandas as pd  # noqa
        frame = pd.read_csv(path, dtype=str, keep_default_na=False)
        headers = [str(h) for h in frame.columns]
        rows = [{str(k): ("" if v is None else str(v)) for k, v in rec.items()}
                for rec in frame.to_dict(orient="records")]
        return rows, headers
    except ImportError:
        pass
    except Exception as exc:  # a malformed frame should not lose the run
        print("pandas could not read the file (%s); falling back to the csv module." % exc)
    import csv
    with open(path, "r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = list(reader.fieldnames or [])
        rows = [{k: (v if v is not None else "") for k, v in row.items() if k is not None}
                for row in reader]
    return rows, headers


def norm(text):
    """Lowercase, straighten quotes, collapse whitespace, drop trailing punctuation."""
    text = (text or "")
    for curly, plain in (("’", "'"), ("‘", "'"), ("“", '"'),
                         ("”", '"'), ("–", "-"), ("—", "-"),
                         (" ", " ")):
        text = text.replace(curly, plain)
    return re.sub(r"\s+", " ", text).strip().lower()


class Columns(object):
    """Matches question titles to CSV headers and remembers what it could not find."""

    def __init__(self, headers):
        self.headers = headers
        self.by_norm = {}
        for head in headers:
            self.by_norm.setdefault(norm(head), head)
        self.missing = []
        self.matched = {}

    def find(self, title, label=None, contains=None):
        label = label or title
        want = norm(title)
        if want in self.by_norm:
            found = self.by_norm[want]
            self.matched[label] = found
            return found
        # Sheets sometimes trims or re-wraps a long title. Fall back to a prefix
        # match, then to a distinctive substring, before giving up.
        for head in self.headers:
            nh = norm(head)
            if len(nh) < 6:  # never let a stub header swallow a long title
                continue
            if nh.startswith(want[:60]) or want.startswith(nh[:60]):
                self.matched[label] = head
                return head
        if contains:
            needles = [norm(x) for x in contains]
            for head in self.headers:
                nh = norm(head)
                if all(n in nh for n in needles):
                    self.matched[label] = head
                    return head
        self.missing.append(label)
        return None


def pct(part, whole):
    if not whole:
        return None
    return 100.0 * part / whole


def fmt_pct(value, digits=0):
    if value is None:
        return "n/a"
    return ("%." + str(digits) + "f%%") % value


# ---------------------------------------------------------------- parsing a row
# Round two rides in question C. index.html builds the cell as
#   Round2: 4/5; calls FSFSF; key FSFSF; seconds 61.
# F is a flag and S is let it stand, in fresh card order. The seconds clause is read
# in either spelling in case the game ever shortens it.
ROUND2_RE = re.compile(
    r"round\s*2\s*:\s*(?:right\s+call\s*)?(?:(\d+)\s*/\s*(\d+))?"
    r"(?:\s*,\s*right\s+reason\s*(\d+)\s*/\s*(\d+))?"
    r"\s*;?\s*calls\s+([A-Za-z]+)\s*;?\s*key\s+([A-Za-z]+)",
    re.I)
R2_SECONDS_RE = re.compile(r"seconds\s+(\d+)|;\s*(\d+)\s*s\b", re.I)

# The fresh case key, from the CARDS2 array above: five lines of Brightwater Dental
# Partners, flag on three and stand on two. Reordered with brightwater-v4.
FRESH_KEY = "".join("F" if c[3] == "flag" else "S" for c in CARDS2)
STREAK_RE = re.compile(r"longest run of correct calls:\s*(\d+)", re.I)
ORG_RE = re.compile(r"organi[sz]ations?\s*:\s*(.*?)(?:\.|$)", re.I)

# --- the per line Why cell, since 13 September 2026 -------------------------------
# index.html builds it as
#   Basis: no source on file; wrong period | Words: the freight moved || Line 12,
#   account 4000. Called: flag. Key: flag. Type: unsupported attribution. Correct.
# " || " separates what the player said from what the page computed. The last token is
# "Correct." or "Missed." in the source; the write-up brief calls it Correct|Incorrect,
# so all three spellings are read and anything that is not Correct counts as a miss.
BASIS_RE = re.compile(r"basis\s*:\s*(.*?)(?:\s*\|\s*words\s*:\s*(.*?))?\s*$", re.I | re.S)
WHY_META_RE = re.compile(
    r"line\s+(\d+)\s*,\s*account\s+(\w+)\s*\.\s*called\s*:\s*(flag|stand)\s*\.\s*"
    r"key\s*:\s*(flag|stand)\s*\.\s*type\s*:\s*(.*?)\s*\.\s*"
    r"(correct|incorrect|missed)\s*\.?", re.I)
# Since 13 September 2026 the page writes its own verdict on the basis, and the card's
# basis key beside it, so the reason score is read rather than recomputed. A cell without
# it is scored here against the basis key in CARDS.
REASON_RE = re.compile(r"reason\s*:\s*(agrees|does not agree)", re.I)
KEYBASIS_RE = re.compile(r"key\s+basis\s*:\s*(.*?)\s*\.?\s*$", re.I | re.S)
NO_CHIPS = "none recorded"


def reason_agrees(chips, basis_key):
    """The page's rule: at least one chip tapped and every chip tapped is in the key."""
    if not chips:
        return False
    keyset = {norm(k) for k in basis_key}
    return all(norm(c) in keyset for c in chips)

# The fresh case basis rides at the end of question C, after the Round2 string:
#   Round2 basis, by line: 1: Basis: direction wrong || 2: Basis: the figure and reason
#   hold | Words: it ties.
R2_BASIS_RE = re.compile(
    r"round2\s+basis,\s*by\s+line\s*:\s*(.*?)(?:\s*fresh case\s*:|\s*$)", re.I | re.S)
# The case id, both versions and the key date, from caseLine() in question A. Today:
#   Case: halyard, version halyard-v4 (practice, 14 lines) and brightwater-v4
#   (assessment, 5 lines), dated 2026-09-13, loaded from cases/ files.
# An authored case posts an id that begins "own:", and it may carry no fresh set:
#   Case: own:Kestrel:3, version kestrel-own-3 (practice, 12 lines), no fresh case,
#   dated 2026-09-13, loaded from this browser, written by author.html.
CASES_RE = re.compile(
    r"case\s*:\s*([^,]+?)\s*,\s*version\s+([\w.:-]+)\s*(?:\([^)]*\))?"
    r"(?:\s*and\s+([\w.:-]+)\s*(?:\([^)]*\))?)?"
    r"(?:\s*,\s*no fresh case)?"
    r"\s*,\s*dated\s+([\d-]+)"
    r"(?:\s*,\s*loaded from\s+(.*?))?\s*\.", re.I)
# The shape the script read before 13 September 2026, kept so an older sheet still parses:
#   Cases: halyard-v3 and brightwater-v2, dated 2026-09-13, loaded from cases/ files.
CASES_RE_OLD = re.compile(
    r"cases\s*:\s*([\w.-]+)\s+and\s+([\w.-]+)\s*,\s*dated\s+([\d-]+)"
    r"(?:\s*,\s*loaded from\s+(.*?))?\s*\.", re.I)
# The product stamp, from versionLine() in question A: "Product: second-pass-drill 1.6.0."
PRODUCT_RE = re.compile(r"product\s*:\s*(.+?)\s*\.(?=\s+[A-Z]|$)", re.I)
TEST_ROW_RE = re.compile(r"test attempt,\s*exclude from reports", re.I)
# Question B: the attempt identifier, which every retry of one run repeats, and the
# reason score the page computed.
ATTEMPT_RE = re.compile(r"attempt\s+id\s*:\s*([\w:.-]+?)\s*,\s*run\s+(\d+)", re.I)
REASON_SCORE_RE = re.compile(
    r"reason\s+score\s*:\s*(\d+)\s+of\s+(\d+)\s+in\s+round\s+one"
    r"(?:\s+and\s+(\d+)\s+of\s+(\d+)\s+on\s+the\s+fresh\s+case)?", re.I)
# Question B again: the closing Result sentence, which carries the points and the rank.
RESULT_RE = re.compile(
    r"result\s*:\s*right\s+call\s+(\d+)\s+of\s+(\d+)\s*,\s*right\s+reason\s+(\d+)"
    r"\s+of\s+(\d+)\s*,\s*(\d+)\s+caught\s*,\s*(\d+)\s+let\s+stand\s+correctly\s*,\s*"
    r"(\d+)\s+false\s+flags?\s*,\s*([\d,]+)\s+points\s*,\s*rank\s+(\w+)", re.I)
# Round one, the free text question, which carries the ledger-only picks:
#   Prepicks: 4000; 5000; 6000.   or   Prepicks: skipped.
PREPICK_RE = re.compile(r"prepicks\s*:\s*(.*?)\s*\.?\s*$", re.I | re.S)
ROUND1_TITLE = ("Round one, question 1. Looking only at the numbers, which movements "
                "would you want explained, and what would you challenge?")


def split_chips(text):
    """'a; b' into ['a', 'b']. 'none recorded' and an empty cell give []."""
    text = (text or "").strip().strip(".")
    if not text or norm(text) == NO_CHIPS:
        return []
    out = []
    for piece in text.split(";"):
        piece = piece.strip().strip(".")
        if not piece:
            continue
        hit = next((c for c in BASIS_CHIPS if norm(c) == norm(piece)), piece)
        if hit not in out:
            out.append(hit)
    return out


def parse_basis(text):
    """'Basis: a; b | Words: one line' into (chips, words)."""
    match = BASIS_RE.search((text or "").strip())
    if not match:
        return [], ""
    chips = split_chips(match.group(1))
    words = (match.group(2) or "").strip().strip(".").strip()
    return chips, words


def parse_why(cell):
    """One Why cell into a dict, or None when the cell carries nothing readable.

    Keys: chips, words, called, key, type, correct, line, acct. The Called and Key values
    the page wrote are the authoritative ones; the caller cross checks them against the
    Accept or Reject column and against the answer key above.
    """
    cell = (cell or "").strip()
    if not cell:
        return None
    left, _, right = cell.partition("||")
    if not right:
        # A cell filed before 13 September 2026 carries only the metadata half.
        left, right = "", cell
    chips, words = parse_basis(left) if left.strip() else ([], "")
    meta = WHY_META_RE.search(right)
    said = REASON_RE.search(right)
    keyb = KEYBASIS_RE.search(right)
    out = {"chips": chips, "words": words, "called": None, "key": None,
           "type": None, "correct": None, "line": None, "acct": None,
           "has_basis": bool(left.strip()),
           "reason_right": (norm(said.group(1)) == "agrees") if said else None,
           "reason_source": "posted" if said else None,
           "key_basis": split_chips(keyb.group(1)) if keyb else []}
    if meta:
        out["line"] = int(meta.group(1))
        out["acct"] = meta.group(2)
        out["called"] = meta.group(3).lower()
        out["key"] = meta.group(4).lower()
        out["type"] = meta.group(5).strip()
        out["correct"] = norm(meta.group(6)) == "correct"
    return out


def parse_r2_basis(cell):
    """The fresh case basis at the tail of question C, as a list of (n, chips, words)."""
    match = R2_BASIS_RE.search(cell or "")
    if not match:
        return []
    out = []
    for piece in match.group(1).split("||"):
        piece = piece.strip().strip(".")
        if not piece:
            continue
        num = re.match(r"^\s*(\d+)\s*:\s*(.*)$", piece, re.S)
        n = int(num.group(1)) if num else len(out) + 1
        body = num.group(2) if num else piece
        said = REASON_RE.search(body)
        # the basis half stops at the first " | Reason:" the page writes after it
        head = re.split(r"\s*\|\s*reason\s*:", body, 1, flags=re.I)[0]
        chips, words = parse_basis(head)
        reason = (norm(said.group(1)) == "agrees") if said else None
        if reason is None and 1 <= n <= len(CARDS2):
            reason = reason_agrees(chips, CARDS2[n - 1][5])
        out.append((n, chips, words, reason))
    return out


def parse_cases(cell):
    """The case line out of question A, in either shape, or None.

    Returns the run id, both case versions, the key date and where the page loaded them
    from. An authored run posts an id beginning "own:" and may carry no fresh case, so
    "two" is None there rather than a guessed version.
    """
    match = CASES_RE.search(cell or "")
    if match:
        run_id = match.group(1).strip()
        return {"id": run_id, "one": match.group(2), "two": match.group(3),
                "date": match.group(4), "source": (match.group(5) or "").strip() or None,
                "authored": run_id.lower().startswith("own:")}
    match = CASES_RE_OLD.search(cell or "")
    if not match:
        return None
    return {"id": match.group(1).split("-")[0], "one": match.group(1),
            "two": match.group(2), "date": match.group(3),
            "source": (match.group(4) or "").strip() or None, "authored": False}


def parse_prepicks(cell):
    """The ledger-only picks out of the round one free text, as a list of accounts."""
    match = PREPICK_RE.search((cell or "").strip())
    if not match:
        return None
    body = match.group(1).strip().strip(".")
    if not body or norm(body) == "skipped":
        return []
    return [piece.strip() for piece in body.split(";") if piece.strip()]


def parse_attempt(cell):
    """The attempt identifier and the run number out of question B, or (None, None)."""
    match = ATTEMPT_RE.search(cell or "")
    if not match:
        return None, None
    return match.group(1), int(match.group(2))


PLACEHOLDER_VALUES = {"3", "5", "once or twice"}


def intake_kind(value):
    """What an intake cell carries: 'not asked', 'placeholder', 'value' or 'blank'."""
    text = (value or "").strip()
    if not text:
        return "blank"
    if norm(text) == NOT_ASKED:
        return "not asked"
    if norm(text) in PLACEHOLDER_VALUES:
        return "placeholder"
    return "value"


def parse_orgs(cell):
    match = ORG_RE.search(cell or "")
    chips = []
    if match:
        for piece in re.split(r"[;,]", match.group(1)):
            piece = piece.strip().strip(".")
            if piece:
                chips.append(piece)
    if not chips:
        # No prefix on the cell. Fall back to testing for the chip names, which is
        # what the older Organisations rows need too.
        low = norm(cell)
        chips = [chip for chip in CHIPS if norm(chip) in low]
    # Normalize each chip against the seven known names where it matches one.
    tidy = []
    for chip in chips:
        hit = next((c for c in CHIPS if norm(c) == norm(chip)), chip)
        if hit not in tidy:
            tidy.append(hit)
    return tidy


def parse_round2(cells):
    """Read the round two string. Question C first, then any other free text.

    Returns (right, total, seconds, calls, key) or None. The posted fraction is
    trusted where it is present, and the two letter strings are compared position by
    position as a check, so a disagreement is visible rather than silent.
    """
    for cell in cells:
        match = ROUND2_RE.search(cell or "")
        if not match:
            continue
        right, total, r_right, r_total, calls, key = match.groups()
        calls, key = calls.upper(), (key or FRESH_KEY).upper()
        pairs = min(len(calls), len(key))
        by_char = sum(1 for i in range(pairs) if calls[i] == key[i])
        sec_m = R2_SECONDS_RE.search(cell)
        seconds = None
        if sec_m:
            seconds = int(sec_m.group(1) or sec_m.group(2))
        reason = (int(r_right), int(r_total)) if (r_right is not None) else None
        if right is not None and total is not None:
            return int(right), int(total), seconds, calls, key, reason
        if pairs:
            return by_char, pairs, seconds, calls, key, reason
    return None


def parse_minutes(cell):
    match = re.search(r"\d+(?:\.\d+)?", cell or "")
    if not match:
        return None
    value = float(match.group(0))
    return value if value > 0 else None


# ---------------------------------------------------------------- the analysis
def analyze(path):
    rows, headers = read_rows(path)
    cols = Columns(headers)

    col_code = cols.find(CODENAME_TITLE, "Codename")
    col_qa = cols.find(QA_TITLE, "Question A (organizations)", contains=["question a"])
    col_qb = cols.find(QB_TITLE, "Question B (summary)", contains=["question b"])
    col_qc = cols.find(QC_TITLE, "Question C (round two string)", contains=["question c"])
    col_qd = cols.find(QD_TITLE, "Question D (minutes)", contains=["question d"])
    col_ts = cols.find(TIMESTAMP_TITLE, "Timestamp")
    col_r1 = cols.find(ROUND1_TITLE, "Round one free text (prepicks)",
                       contains=["round one", "question 1"])

    intake_cols = []
    for label, title, needles in INTAKE_TITLES:
        intake_cols.append((label, cols.find(title, "Intake placeholder: %s" % label,
                                             contains=needles)))

    call_cols, why_cols = [], []
    for i in range(14):
        call_cols.append(cols.find(CALL_TITLES[i], "Call C%d" % (i + 1),
                                   contains=["c%d." % (i + 1), "account"]))
        why_cols.append(cols.find(WHY_TITLES[i], "Why C%d" % (i + 1),
                                  contains=["c%d." % (i + 1), "why?"]))

    report = {"missing": cols.missing, "matched": cols.matched,
              "n_rows_raw": len(rows), "source": os.path.abspath(path)}

    # --- drop test rows, then repeat runs -------------------------------------
    kept, dropped_test, repeats = [], [], []
    seen_attempts, seen_codes = set(), set()
    for row in rows:
        code = (row.get(col_code, "") if col_code else "").strip()
        qb_raw = (row.get(col_qb, "") if col_qb else "")
        qa_raw = (row.get(col_qa, "") if col_qa else "")
        attempt, _run = parse_attempt(qb_raw)
        if norm(code) in TEST_CODENAMES:
            dropped_test.append(code)
            continue
        if TEST_ROW_RE.search(qa_raw):
            dropped_test.append("%s (marked TEST ATTEMPT by the page)" % (code or "(blank)"))
            continue
        if not code:
            dropped_test.append("(blank codename)")
            continue
        # A retry of one run posts the same attempt identifier, so the identifier decides
        # a repeat where the page wrote one and the codename decides where it did not.
        if attempt:
            if attempt in seen_attempts:
                repeats.append("%s (attempt %s sent again)" % (code, attempt))
                continue
            seen_attempts.add(attempt)
        elif norm(code) in seen_codes:
            repeats.append(code)
            continue
        seen_codes.add(norm(code))
        kept.append(row)

    report["dropped_test"] = dropped_test
    report["repeat_runs"] = repeats

    players = []
    disagreements = []
    for row in kept:
        code = row.get(col_code, "").strip()
        posted = []   # what the Accept or Reject column says
        for i, col in enumerate(call_cols):
            raw = (row.get(col, "") if col else "").strip()
            if not raw:
                posted.append(None)
                continue
            flag_value = CARDS[i][5]
            posted.append("flag" if norm(raw) == norm(flag_value) else "stand")

        # The Why cell is the authoritative record of the call and of the key it was
        # scored against, because it is the half the page wrote after the basis step.
        whys, calls, keys = [], [], []
        for i, col in enumerate(why_cols):
            parsed = parse_why(row.get(col, "") if col else "")
            whys.append(parsed)
            call = parsed["called"] if (parsed and parsed["called"]) else posted[i]
            key = (parsed["key"] if (parsed and parsed["key"]) else CARDS[i][3])
            calls.append(call)
            keys.append(key)
            if parsed and parsed["called"] and posted[i] and parsed["called"] != posted[i]:
                disagreements.append(
                    "%s line %d: Why says %s, the Accept or Reject column says %s"
                    % (code, i + 1, parsed["called"], posted[i]))
            if parsed and parsed["key"] and parsed["key"] != CARDS[i][3]:
                disagreements.append(
                    "%s line %d: Why says the key is %s, this script carries %s"
                    % (code, i + 1, parsed["key"], CARDS[i][3]))
            if parsed and parsed["type"] and norm(parsed["type"]) != norm(CARDS[i][4]):
                disagreements.append(
                    "%s line %d: Why says the type is %s, this script carries %s"
                    % (code, i + 1, parsed["type"], CARDS[i][4]))
        answered = [i for i, c in enumerate(calls) if c is not None]
        correct = [i for i in answered if calls[i] == CARDS[i][3]]
        # The reason score: the page's own verdict where the cell carries it, this
        # script's reading of the basis key where it does not.
        reasons = []
        for i, parsed in enumerate(whys):
            if parsed and parsed["reason_right"] is not None:
                reasons.append(parsed["reason_right"])
            elif parsed and parsed["has_basis"]:
                reasons.append(reason_agrees(parsed["chips"], CARDS[i][6]))
            else:
                reasons.append(None)
        qa_cell = row.get(col_qa, "") if col_qa else ""
        orgs = parse_orgs(qa_cell)
        qb = row.get(col_qb, "") if col_qb else ""
        streak_m = STREAK_RE.search(qb)
        # Question C is where the fresh case posts. The other free text is scanned
        # only as a fallback, in case the sheet is ever reordered or a column is
        # renamed out from under the title match.
        qc_cell = row.get(col_qc, "") if col_qc else ""
        free_text = [qc_cell]
        free_text += [row.get(c, "") for c in why_cols if c]
        free_text += [qb, qa_cell]
        intake = {label: intake_kind(row.get(col, "") if col else "")
                  for label, col in intake_cols}
        attempt_id, run_index = parse_attempt(qb)
        result_m = RESULT_RE.search(qb)
        reason_m = REASON_SCORE_RE.search(qb)
        players.append({
            "codename": code,
            "attempt_id": attempt_id,
            "run_index": run_index,
            "prepicks": parse_prepicks(row.get(col_r1, "") if col_r1 else ""),
            "reasons": reasons,
            "reason_right": sum(1 for v in reasons if v),
            "reason_scored": sum(1 for v in reasons if v is not None),
            "reason_posted_r1": (int(reason_m.group(1)), int(reason_m.group(2))) if reason_m else None,
            "reason_posted_r2": ((int(reason_m.group(3)), int(reason_m.group(4)))
                                 if (reason_m and reason_m.group(3)) else None),
            "points": int(result_m.group(8).replace(",", "")) if result_m else None,
            "posted_rank": result_m.group(9) if result_m else None,
            "product": (PRODUCT_RE.search(qa_cell).group(1).strip()
                        if PRODUCT_RE.search(qa_cell) else None),
            "timestamp": row.get(col_ts, "") if col_ts else "",
            "calls": calls,
            "posted": posted,
            "keys": keys,
            "whys": whys,
            "answered": answered,
            "score": len(correct),
            "orgs": orgs,
            "minutes": parse_minutes(row.get(col_qd, "") if col_qd else ""),
            "best_streak": int(streak_m.group(1)) if streak_m else None,
            "round2": parse_round2(free_text),
            "r2_basis": parse_r2_basis(qc_cell),
            "cases": parse_cases(qa_cell),
            "intake": intake,
            "flags": sum(1 for c in calls if c == "flag"),
            "coverage": sum(1 for w in whys if w and w["chips"]),
        })

    report["players"] = players
    report["n_players"] = len(players)
    report["disagreements"] = disagreements

    # --- the four intake placeholders -----------------------------------------
    # None of these is a player answer. They are counted here only so the export can be
    # seen for what it carries, and they enter no rate anywhere in this report.
    intake_report = []
    for label, col in intake_cols:
        kinds = {"not asked": 0, "placeholder": 0, "value": 0, "blank": 0}
        for p in players:
            kinds[p["intake"][label]] += 1
        intake_report.append({"label": label, "column": col, "kinds": kinds})
    report["intake"] = intake_report

    # --- case versions ---------------------------------------------------------
    versions = {}
    for p in players:
        if p["cases"]:
            tag = "%s and %s, dated %s" % (p["cases"]["one"],
                                           p["cases"]["two"] or "no fresh case",
                                           p["cases"]["date"])
            versions[tag] = versions.get(tag, 0) + 1
    report["case_versions"] = dict(sorted(versions.items(), key=lambda kv: -kv[1]))
    report["n_without_case"] = sum(1 for p in players if not p["cases"])

    # --- organizations ---------------------------------------------------------
    org_counts = {}
    for p in players:
        for chip in p["orgs"]:
            org_counts[chip] = org_counts.get(chip, 0) + 1
    report["org_counts"] = dict(sorted(org_counts.items(), key=lambda kv: -kv[1]))
    report["n_with_org"] = sum(1 for p in players if p["orgs"])

    # --- per card --------------------------------------------------------------
    per_card = []
    for i, card in enumerate(CARDS):
        n, acct, name, key, etype, _post, _basis = card
        seen_n = sum(1 for p in players if p["calls"][i] is not None)
        right = sum(1 for p in players if p["calls"][i] == key)
        flagged = sum(1 for p in players if p["calls"][i] == "flag")
        per_card.append({
            "n": n, "acct": acct, "name": name, "key": key, "type": etype,
            "seen": seen_n, "right": right, "flagged": flagged,
            "rate": pct(right, seen_n),
        })
    report["per_card"] = per_card

    problem_seen = sum(c["seen"] for c in per_card if c["key"] == "flag")
    problem_caught = sum(c["right"] for c in per_card if c["key"] == "flag")
    clean_seen = sum(c["seen"] for c in per_card if c["key"] == "stand")
    clean_right = sum(c["right"] for c in per_card if c["key"] == "stand")
    clean_flagged = sum(c["flagged"] for c in per_card if c["key"] == "stand")
    report["catch_rate"] = pct(problem_caught, problem_seen)
    report["catch_counts"] = (problem_caught, problem_seen)
    report["let_stand_rate"] = pct(clean_right, clean_seen)
    report["let_stand_counts"] = (clean_right, clean_seen)
    report["false_flag_rate"] = pct(clean_flagged, clean_seen)
    report["false_flag_counts"] = (clean_flagged, clean_seen)

    # --- by error type ---------------------------------------------------------
    by_type = {}
    for i, card in enumerate(CARDS):
        etype = card[4]
        bucket = by_type.setdefault(etype, {"seen": 0, "right": 0, "lines": []})
        bucket["seen"] += per_card[i]["seen"]
        bucket["right"] += per_card[i]["right"]
        bucket["lines"].append(card[0])
    for etype, bucket in by_type.items():
        bucket["rate"] = pct(bucket["right"], bucket["seen"])
    report["by_type"] = by_type

    # --- the basis a player gave ----------------------------------------------
    # Chip counts are grouped on the error type of the card, so a line keyed "no source
    # on file" can be read against how often the players reached for that chip on it.
    chips_by_type, calls_by_type, basis_by_type = {}, {}, {}
    chips_overall = {}
    examples = {}
    flags_total = flags_with_words = 0
    calls_total = calls_with_basis = calls_with_words = 0
    for p in players:
        for i, why in enumerate(p["whys"]):
            etype = CARDS[i][4]
            calls_by_type[etype] = calls_by_type.get(etype, 0) + 1
            if p["calls"][i] == "flag":
                flags_total += 1
            calls_total += 1
            if not why:
                continue
            if why["chips"]:
                calls_with_basis += 1
                basis_by_type[etype] = basis_by_type.get(etype, 0) + 1
                bucket = chips_by_type.setdefault(etype, {})
                for chip in why["chips"]:
                    bucket[chip] = bucket.get(chip, 0) + 1
                    chips_overall[chip] = chips_overall.get(chip, 0) + 1
            if why["words"]:
                calls_with_words += 1
                if p["calls"][i] == "flag":
                    flags_with_words += 1
                examples.setdefault(etype, []).append(
                    {"codename": p["codename"], "line": CARDS[i][0],
                     "acct": CARDS[i][1], "call": p["calls"][i], "words": why["words"]})

    report["basis"] = {
        "calls_total": calls_total,
        "calls_with_basis": calls_with_basis,
        "basis_rate": pct(calls_with_basis, calls_total),
        "calls_with_words": calls_with_words,
        "words_rate": pct(calls_with_words, calls_total),
        "flags_total": flags_total,
        "flags_with_words": flags_with_words,
        "flag_words_rate": pct(flags_with_words, flags_total),
        "chips_overall": dict(sorted(chips_overall.items(), key=lambda kv: -kv[1])),
        "by_type": {t: {"chips": dict(sorted(chips_by_type.get(t, {}).items(),
                                             key=lambda kv: -kv[1])),
                        "with_basis": basis_by_type.get(t, 0),
                        "calls": calls_by_type.get(t, 0)}
                    for t in calls_by_type},
        # three lines per type, verbatim, in the order they were filed
        "examples": {t: v[:3] for t, v in examples.items()},
        "examples_all": examples,
    }

    # The fresh case has no Why fields, so its basis is read off question C.
    r2_chips, r2_calls_with_basis, r2_lines = {}, 0, 0
    for p in players:
        for n, chips, words, _reason in p["r2_basis"]:
            if not 1 <= n <= len(CARDS2):
                continue
            etype = CARDS2[n - 1][4]
            r2_lines += 1
            if chips:
                r2_calls_with_basis += 1
                bucket = r2_chips.setdefault(etype, {})
                for chip in chips:
                    bucket[chip] = bucket.get(chip, 0) + 1
    report["r2_basis"] = {
        "lines": r2_lines,
        "with_basis": r2_calls_with_basis,
        "by_type": {t: dict(sorted(v.items(), key=lambda kv: -kv[1]))
                    for t, v in r2_chips.items()},
        "players": sum(1 for p in players if p["r2_basis"]),
    }

    # --- per player ------------------------------------------------------------
    ranks = {r: 0 for r in RANK_ORDER}
    for p in players:
        # the page computes the rank off its own points ladder, which is a share of what
        # the case can give; this script's banding is only the fallback for an older row
        p["rank"] = p["posted_rank"] or rank_of(p["score"])
        p["rank_source"] = "posted by the page" if p["posted_rank"] else "this script"
        if p["rank"] not in ranks:
            ranks[p["rank"]] = 0
        ranks[p["rank"]] += 1
    report["ranks"] = ranks
    scores = [p["score"] for p in players]
    report["mean_score"] = statistics.mean(scores) if scores else None
    report["median_score"] = statistics.median(scores) if scores else None

    covers = [p["coverage"] for p in players]
    report["coverage_mean"] = statistics.mean(covers) if covers else None
    report["coverage_full"] = sum(1 for c in covers if c == 14)
    report["coverage_none"] = sum(1 for c in covers if c == 0)

    minutes = [p["minutes"] for p in players if p["minutes"]]
    report["minutes_n"] = len(minutes)
    report["minutes_mean"] = statistics.mean(minutes) if minutes else None
    report["minutes_median"] = statistics.median(minutes) if minutes else None

    streaks = [p["best_streak"] for p in players if p["best_streak"] is not None]
    report["streak_n"] = len(streaks)
    report["streak_mean"] = statistics.mean(streaks) if streaks else None
    report["streak_best"] = max(streaks) if streaks else None

    flag_everything = [p["codename"] for p in players if p["flags"] == 14]
    report["flag_everything"] = flag_everything

    # --- round two transfer ----------------------------------------------------
    r2 = [p for p in players if p["round2"]]
    if r2:
        fresh_rates = [100.0 * p["round2"][0] / p["round2"][1] for p in r2 if p["round2"][1]]
        trained = [100.0 * p["score"] / max(1, len(p["answered"])) for p in r2]
        secs = [p["round2"][2] for p in r2 if p["round2"][2]]
        odd_key = sorted({p["round2"][4] for p in r2} - {FRESH_KEY})
        fresh_mean = statistics.mean(fresh_rates) if fresh_rates else None
        trained_mean = statistics.mean(trained) if trained else None
        report["round2"] = {
            "n": len(r2),
            "fresh_rate": fresh_mean,
            "trained_rate": trained_mean,
            "gap": (fresh_mean - trained_mean)
                   if (fresh_mean is not None and trained_mean is not None) else None,
            "right": sum(p["round2"][0] for p in r2),
            "total": sum(p["round2"][1] for p in r2),
            "seconds_median": statistics.median(secs) if secs else None,
            "odd_key": odd_key,
        }
    else:
        report["round2"] = None

    # --- professor subset ------------------------------------------------------
    profs = [p for p in players if any("professor" in norm(c) for c in p["orgs"])]
    if profs:
        p_seen = sum(1 for p in profs for i in range(14)
                     if p["calls"][i] is not None and CARDS[i][3] == "flag")
        p_caught = sum(1 for p in profs for i in range(14)
                       if p["calls"][i] == "flag" and CARDS[i][3] == "flag")
        report["professors"] = {
            "n": len(profs),
            "codenames": [p["codename"] for p in profs],
            "mean_score": statistics.mean([p["score"] for p in profs]),
            "catch_rate": pct(p_caught, p_seen),
        }
    else:
        report["professors"] = None

    return report


# ------------------------------------------------- the readout's field contract
# READOUT-TEMPLATE.md prints a field name in every cell it wants filled. These are those
# names, computed here so a facilitator copies a value across rather than translating one.
# A field the responses cannot support is written as None and printed as "not available",
# never as an estimate.
ORG_ORDER = ["Beta Alpha Psi", "ACFE", "ASM", "NABA", "AAA", "GMU Student", "Professor",
             "Outside Mason"]
TYPE_ORDER = ["arithmetic", "wrong direction", "timing", "unsupported driver",
              "unsupported attribution", "no explanation", "clean line"]
TYPE_LABEL = {"arithmetic": "Arithmetic", "wrong direction": "Wrong direction",
              "timing": "Timing", "unsupported driver": "Unsupported driver",
              "unsupported attribution": "Unsupported attribution",
              "no explanation": "No explanation",
              "clean line": "Clean line, the control"}


def _mean(values):
    values = [v for v in values if v is not None]
    return statistics.mean(values) if values else None


def _median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def readout_fields(report, csv_path):
    """Every field READOUT-TEMPLATE.md names, as an ordered list of (name, value)."""
    players = report["players"]
    out = []

    def add(name, value):
        out.append((name, value))

    versions = sorted(report.get("case_versions", {}).items(), key=lambda kv: -kv[1])
    one = two = date = None
    for p in players:
        if p["cases"]:
            one = one or p["cases"]["one"]
            two = two or p["cases"]["two"]
            date = date or p["cases"]["date"]
    product = next((p["product"] for p in players if p.get("product")), None)

    add("run.generated", datetime.date.today().isoformat())
    add("run.source_file", os.path.basename(csv_path))
    add("run.case_round1", one)
    add("run.case_round2", two)
    add("run.key_date", date)
    add("run.product_version", product)
    add("run.responses_total", report["n_rows_raw"])
    add("run.players", report["n_players"])
    add("run.test_rows_dropped", len(report["dropped_test"]))
    add("run.replays_dropped", len(report["repeat_runs"]))
    if len(versions) > 1:
        add("run.case_versions_mixed", "; ".join("%s (%d)" % (k, v) for k, v in versions))

    # 1. players by organization
    for name in ORG_ORDER:
        members = [p for p in players if any(norm(c) == norm(name) for c in p["orgs"])]
        key = "org." + name.lower().replace(" ", "-")
        add(key + ".name", name)
        add(key + ".players", len(members))
        add(key + ".call_mean_r1",
            _mean([100.0 * p["score"] / len(p["answered"])
                   for p in members if p["answered"]]))
        add(key + ".reason_mean_r1",
            _mean([100.0 * p["reason_right"] / p["reason_scored"]
                   for p in members if p["reason_scored"]]))

    # 2. right call and right reason by error type
    for etype in TYPE_ORDER:
        idx = [i for i, c in enumerate(CARDS) if c[4] == etype]
        if not idx:
            continue
        key = "type." + etype.replace(" ", "-")
        seen = sum(1 for p in players for i in idx if p["calls"][i] is not None)
        right = sum(1 for p in players for i in idx if p["calls"][i] == CARDS[i][3])
        r_scored = sum(1 for p in players for i in idx if p["reasons"][i] is not None)
        r_right = sum(1 for p in players for i in idx if p["reasons"][i])
        add(key + ".name", TYPE_LABEL[etype])
        add(key + ".lines", ", ".join(str(CARDS[i][0]) for i in idx))
        add(key + ".calls_seen", seen)
        add(key + ".right_call_rate", pct(right, seen))
        add(key + ".right_reason_rate", pct(r_right, r_scored))

    # 3. false flags on the clean lines
    clean_idx = [i for i, c in enumerate(CARDS) if c[3] == "stand"]
    flags_all = seen_all = 0
    for i in clean_idx:
        seen = sum(1 for p in players if p["calls"][i] is not None)
        flags = sum(1 for p in players if p["calls"][i] == "flag")
        flags_all += flags
        seen_all += seen
        key = "falseflag.line%d" % CARDS[i][0]
        add(key + ".flags", flags)
        add(key + ".rate", pct(flags, seen))
    add("falseflag.flags", flags_all)
    add("falseflag.overall_rate", pct(flags_all, seen_all))
    add("falseflag.players_with_none",
        sum(1 for p in players if not any(p["calls"][i] == "flag" for i in clean_idx)))

    # 4. the fresh case
    r2 = [p for p in players if p["round2"]]
    for n, card in enumerate(CARDS2, start=1):
        key = "fresh.line%d" % n
        add(key + ".name", card[2])
        add(key + ".key", card[3].capitalize())
        seen = right = 0
        for p in r2:
            calls = p["round2"][3]
            if len(calls) < n:
                continue
            seen += 1
            if calls[n - 1] == ("F" if card[3] == "flag" else "S"):
                right += 1
        add(key + ".calls_seen", seen)
        add(key + ".right_call_rate", pct(right, seen))
        rows = [row for p in players for row in p["r2_basis"]
                if row[0] == n and row[3] is not None]
        add(key + ".right_reason_rate",
            pct(sum(1 for row in rows if row[3]), len(rows)))
    add("fresh.players", len(r2))
    add("fresh.call_mean",
        _mean([100.0 * p["round2"][0] / p["round2"][1] for p in r2 if p["round2"][1]]))
    reason_means = []
    for p in players:
        scored = [row for row in p["r2_basis"] if row[3] is not None]
        if scored:
            reason_means.append(100.0 * sum(1 for row in scored if row[3]) / len(scored))
    add("fresh.reason_mean", _mean(reason_means))
    add("fresh.seconds_median", _median([p["round2"][2] for p in r2]))  # seconds

    # the trained fourteen, against which the fresh five are read
    add("r1.call_mean",
        _mean([100.0 * p["score"] / len(p["answered"]) for p in players if p["answered"]]))
    add("r1.reason_mean",
        _mean([100.0 * p["reason_right"] / p["reason_scored"]
               for p in players if p["reason_scored"]]))
    add("r1.lap_median", _median([p["minutes"] for p in players]))
    add("r1.prepicks_given", sum(1 for p in players if p["prepicks"]))

    # 5. best reason lines: a line in the player's own words where the basis agreed
    quotes = []
    for p in players:
        for i, why in enumerate(p["whys"]):
            if why and why["words"] and p["reasons"][i]:
                quotes.append({"words.codename": p["codename"],
                               "words.line": CARDS[i][0],
                               "words.type": TYPE_LABEL.get(CARDS[i][4], CARDS[i][4]),
                               "words.text": why["words"]})
    add("words.rows", quotes)
    return out


PERCENT_FIELDS = ("_rate", "call_mean", "reason_mean")


def fmt_field(value, name=""):
    """A percentage only where the field is one. Seconds and minutes are not rates."""
    if value is None:
        return "not available"
    if isinstance(value, float):
        if any(name.endswith(tail) or tail in name for tail in PERCENT_FIELDS):
            return "%.1f%%" % value
        return ("%.1f" % value).rstrip("0").rstrip(".")
    if isinstance(value, list):
        return "%d row%s" % (len(value), "" if len(value) == 1 else "s")
    return str(value)


def fields_block(fields, missing):
    lines = ["## Readout fields", "",
             "Every name READOUT-TEMPLATE.md prints in a cell, with the value to copy "
             "into it. A field reading *not available* stays blank on the readout rather "
             "than being estimated.", "",
             "| Field | Value |", "| --- | --- |"]
    for name, value in fields:
        if name == "words.rows":
            continue
        lines.append("| `%s` | %s |" % (name, fmt_field(value, name)))
    quotes = dict(fields).get("words.rows") or []
    lines += ["", "### `words.` rows, the reasons that agreed with the key", "",
              "| `words.codename` | `words.line` | `words.type` | `words.text` |",
              "| --- | --- | --- | --- |"]
    if quotes:
        for q in quotes[:12]:
            lines.append("| %s | %d | %s | %s |"
                         % (q["words.codename"], q["words.line"], q["words.type"],
                            q["words.text"]))
    else:
        lines.append("| none | | | |")
    if missing:
        lines += ["", "### Columns not found", ""]
        lines += ["- " + m for m in missing]
        lines += ["", "Every cell that needed one of these stays blank on the readout."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- the sentences
WORDS = ["zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
         "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
         "Sixteen", "Seventeen", "Eighteen", "Nineteen", "Twenty"]


def spell(n):
    """Numbers open a sentence as words, which is how he writes."""
    return WORDS[n] if 0 < n <= 20 else str(n)


def as_percent(value):
    if value is None:
        return "an unknown share"
    return "%d percent" % round(value)


def write_sentences(r):
    """Three sentences for the write-up, under sixty words together. No em dashes."""
    n = r["n_players"]
    player_word = "reviewer" if n == 1 else "reviewers"
    catch = as_percent(r["catch_rate"])
    false_flag = as_percent(r["false_flag_rate"])
    minutes = r["minutes_median"]

    # Best and worst caught among the eight problem lines. Ties break on the type
    # name so the same export always produces the same sentence.
    bad = [(t, b) for t, b in r["by_type"].items() if t != "clean line" and b["seen"]]
    bad.sort(key=lambda kv: (kv[1]["rate"], kv[0]))
    worst = bad[0] if bad else None
    best = bad[-1] if bad else None

    if minutes:
        s1 = ("%s %s ran the case and caught %s of the eight planted problems, in a "
              "median of %g minutes." % (spell(n), player_word, catch, round(minutes)))
    else:
        s1 = ("%s %s ran the case and caught %s of the eight planted problems."
              % (spell(n), player_word, catch))
    if worst and best and worst[0] != best[0]:
        s2 = ("They caught the %s line %s of the time and the %s line only %s."
              % (best[0], as_percent(best[1]["rate"]),
                 worst[0], as_percent(worst[1]["rate"])))
    elif worst:
        s2 = ("The %s line was caught %s of the time."
              % (worst[0], as_percent(worst[1]["rate"])))
    else:
        s2 = "No rate by error type could be computed from this export."
    s3 = ("False flags on the six clean lines ran %s, so over flagging cost real "
          "time." % false_flag)

    sentences = [s1, s2, s3]

    r2 = r["round2"]
    if r2 and r2["fresh_rate"] is not None:
        sentences.append(
            "On five lines of a company nobody had seen the rate held at %s (n=%d)."
            % (as_percent(r2["fresh_rate"]), r2["n"]))
        # Four sentences have to fit the same sixty word placeholder, so the two
        # longest clauses come out in order until they do.
        if sum(len(s.split()) for s in sentences) > 60:
            sentences[2] = "False flags on the six clean lines ran %s." % false_flag
        if sum(len(s.split()) for s in sentences) > 60 and minutes:
            sentences[0] = ("%s %s caught %s of the eight planted problems in a median "
                            "of %g minutes." % (spell(n), player_word, catch, round(minutes)))
        if sum(len(s.split()) for s in sentences) > 60 and worst and best and worst[0] != best[0]:
            sentences[1] = ("The %s line was caught %s, the %s line only %s."
                            % (best[0], as_percent(best[1]["rate"]),
                               worst[0], as_percent(worst[1]["rate"])))

    video = ("%s %s took the case, caught %s of the planted problems, and false "
             "flagged clean lines %s of the time."
             % (spell(n), player_word, catch, false_flag))
    if r2 and r2["fresh_rate"] is not None:
        video = ("%s %s took the case, caught %s of the planted problems, and held %s "
                 "on a fresh company they had never seen."
                 % (spell(n), player_word, catch, as_percent(r2["fresh_rate"])))

    words = sum(len(s.split()) for s in sentences)
    return sentences, words, video


def basis_sentence(r):
    """One more sentence, on the reason the player held. Empty when no basis was filed."""
    b = r["basis"]
    if not b["calls_with_basis"]:
        return ""
    parts = ["Players gave a basis on %s of their calls" % as_percent(b["basis_rate"])]
    if b["flags_total"]:
        parts.append("and added a line of their own on %s of the flags"
                     % as_percent(b["flag_words_rate"]))
    lead = ", ".join(parts) + "."
    # The chip players reached for most on the lines that were keyed silent, which is the
    # one comparison the chip names make directly.
    silent = b["by_type"].get("no explanation")
    if silent and silent["chips"] and silent["with_basis"]:
        chip, count = next(iter(silent["chips"].items()))
        lead += (" On the line the memo says nothing about, %s of them reached for \"%s\"."
                 % (as_percent(pct(count, silent["with_basis"])), chip))
    return lead


# ---------------------------------------------------------------- output
def build_markdown(r, sentences, words, video, csv_path):
    out = []
    today = datetime.date.today().isoformat()
    out.append("# Second Pass: Beat the Machine, findings")
    out.append("")
    out.append("Built %s from `%s`." % (today, os.path.basename(csv_path)))
    out.append("")
    out.append("## Paste into the write-up")
    out.append("")
    for s in sentences:
        out.append(s)
    out.append("")
    out.append("(%d words)" % words)
    out.append("")
    bas = basis_sentence(r)
    if bas:
        out.append("One more sentence, on the reason behind the call, if the write-up "
                   "has room for it:")
        out.append("")
        out.append(bas)
        out.append("")
    out.append("## Paste into the video script")
    out.append("")
    out.append(video)
    out.append("")

    out.append("## What came out of the sheet")
    out.append("")
    out.append("| Measure | Value |")
    out.append("| --- | --- |")
    out.append("| Rows in the export | %d |" % r["n_rows_raw"])
    out.append("| Test rows dropped | %d |" % len(r["dropped_test"]))
    out.append("| Repeat runs set aside | %d |" % len(r["repeat_runs"]))
    out.append("| Distinct players counted | %d |" % r["n_players"])
    out.append("| Mean score out of 14 | %s |"
               % ("%.1f" % r["mean_score"] if r["mean_score"] is not None else "n/a"))
    out.append("| Median score out of 14 | %s |"
               % ("%g" % r["median_score"] if r["median_score"] is not None else "n/a"))
    out.append("| Catch rate, eight problem lines | %s (%d of %d) |"
               % (fmt_pct(r["catch_rate"], 1), r["catch_counts"][0], r["catch_counts"][1]))
    out.append("| Correct let stand rate, six clean lines | %s (%d of %d) |"
               % (fmt_pct(r["let_stand_rate"], 1), r["let_stand_counts"][0],
                  r["let_stand_counts"][1]))
    out.append("| False flag rate | %s (%d of %d) |"
               % (fmt_pct(r["false_flag_rate"], 1), r["false_flag_counts"][0],
                  r["false_flag_counts"][1]))
    out.append("| Lap time, median minutes | %s |"
               % ("%g" % r["minutes_median"] if r["minutes_median"] is not None else "n/a"))
    out.append("| Lap time, mean minutes | %s |"
               % ("%.1f" % r["minutes_mean"] if r["minutes_mean"] is not None else "n/a"))
    out.append("| Best streak posted | %s |"
               % (r["streak_best"] if r["streak_best"] is not None else "n/a"))
    out.append("| Players who flagged all fourteen | %d |" % len(r["flag_everything"]))
    out.append("| Calls carrying a basis | %s (%d of %d) |"
               % (fmt_pct(r["basis"]["basis_rate"], 1), r["basis"]["calls_with_basis"],
                  r["basis"]["calls_total"]))
    out.append("| Flags carrying a line of the player's own words | %s (%d of %d) |"
               % (fmt_pct(r["basis"]["flag_words_rate"], 1),
                  r["basis"]["flags_with_words"], r["basis"]["flags_total"]))
    out.append("| Reasoning coverage, mean cards with a chip | %s of 14 |"
               % ("%.1f" % r["coverage_mean"] if r["coverage_mean"] is not None else "n/a"))
    out.append("| Players who gave a basis on all fourteen | %d |" % r["coverage_full"])
    out.append("")

    out.append("## By organization")
    out.append("")
    out.append("A player who tapped two chips counts in both, so these sum above the "
               "player count.")
    out.append("")
    out.append("| Chapter | Players |")
    out.append("| --- | --- |")
    for chip, count in r["org_counts"].items():
        out.append("| %s | %d |" % (chip, count))
    out.append("| Distinct players | %d |" % r["n_players"])
    out.append("")

    out.append("## By error type")
    out.append("")
    out.append("| Error type | Lines | Calls seen | Correct | Rate |")
    out.append("| --- | --- | --- | --- | --- |")
    order = sorted(r["by_type"].items(),
                   key=lambda kv: (kv[0] == "clean line", -(kv[1]["rate"] or 0)))
    for etype, b in order:
        out.append("| %s | %s | %d | %d | %s |"
                   % (etype, ", ".join(str(x) for x in b["lines"]),
                      b["seen"], b["right"], fmt_pct(b["rate"], 1)))
    out.append("")

    out.append("## The basis a player gave, by error type")
    out.append("")
    out.append("Read down a row to see which chips the players reached for on the lines "
               "of that type. The share is of the calls on those lines that carried a "
               "basis at all, and a player may tap more than one chip, so a row can sum "
               "above 100 percent.")
    out.append("")
    out.append("| Error type | Calls with a basis | Chips tapped |")
    out.append("| --- | --- | --- |")
    for etype, b in sorted(r["basis"]["by_type"].items(),
                           key=lambda kv: (kv[0] == "clean line", kv[0])):
        if not b["chips"]:
            out.append("| %s | 0 of %d | none recorded |" % (etype, b["calls"]))
            continue
        chips = "; ".join("%s %d (%s)" % (chip, count,
                                          fmt_pct(pct(count, b["with_basis"])))
                          for chip, count in b["chips"].items())
        out.append("| %s | %d of %d | %s |"
                   % (etype, b["with_basis"], b["calls"], chips))
    out.append("")
    if r["basis"]["chips_overall"]:
        out.append("| Chip | Times tapped |")
        out.append("| --- | --- |")
        for chip, count in r["basis"]["chips_overall"].items():
            out.append("| %s | %d |" % (chip, count))
        out.append("")

    out.append("## In their own words")
    out.append("")
    if r["basis"]["examples"]:
        out.append("Verbatim, up to three per error type, for the write-up.")
        out.append("")
        for etype in sorted(r["basis"]["examples"],
                            key=lambda t: (t == "clean line", t)):
            out.append("**%s**" % etype)
            out.append("")
            for ex in r["basis"]["examples"][etype]:
                out.append("- \"%s\" (%s, line %d, account %s, called %s)"
                           % (ex["words"], ex["codename"], ex["line"], ex["acct"],
                              ex["call"]))
            out.append("")
    else:
        out.append("Nobody used the optional line of their own words in this export.")
        out.append("")

    out.append("## By card")
    out.append("")
    out.append("| Line | Account | Key | Error type | Seen | Correct | Rate | Flagged |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in r["per_card"]:
        out.append("| %d | %s %s | %s | %s | %d | %d | %s | %d |"
                   % (c["n"], c["acct"], c["name"], c["key"], c["type"],
                      c["seen"], c["right"], fmt_pct(c["rate"], 1), c["flagged"]))
    out.append("")

    out.append("## By player")
    out.append("")
    out.append("| Codename | Right of 14 | Rank | Minutes | Best streak | Flags | "
               "Cards with a basis | Chapters |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for p in sorted(r["players"], key=lambda x: -x["score"]):
        out.append("| %s | %d | %s | %s | %s | %d | %d of 14 | %s |"
                   % (p["codename"], p["score"], p["rank"],
                      ("%g" % p["minutes"]) if p["minutes"] else "n/a",
                      p["best_streak"] if p["best_streak"] is not None else "n/a",
                      p["flags"], p["coverage"], ", ".join(p["orgs"]) or "none"))
    out.append("")
    out.append("| Rank | Players |")
    out.append("| --- | --- |")
    for rk in RANK_ORDER:
        out.append("| %s | %d |" % (rk, r["ranks"][rk]))
    out.append("")

    if r["flag_everything"]:
        out.append("Flagged all fourteen: %s. Those runs score eight and land on "
                   "Trainee, which is what the rebalanced key is for."
                   % ", ".join(r["flag_everything"]))
        out.append("")

    if r["round2"]:
        r2 = r["round2"]
        out.append("## Round two, fresh cases")
        out.append("")
        out.append("Read out of question C, which carries the whole fresh case as "
                   "`Round2: 4/5; calls FSFSF; key FSFSF; seconds 61. Round2 basis, by "
                   "line: 1: Basis: direction wrong || 2: ...`")
        out.append("")
        out.append("| Measure | Value |")
        out.append("| --- | --- |")
        out.append("| Players who ran round two | %d of %d |" % (r2["n"], r["n_players"]))
        out.append("| Fresh case correct rate | %s (%d of %d calls) |"
                   % (fmt_pct(r2["fresh_rate"], 1), r2["right"], r2["total"]))
        out.append("| Trained case rate, same people | %s |"
                   % fmt_pct(r2["trained_rate"], 1))
        out.append("| Transfer gap | %s |"
                   % ("%+.1f points" % r2["gap"] if r2["gap"] is not None else "n/a"))
        out.append("| Round two clock, median seconds | %s |"
                   % ("%g" % r2["seconds_median"] if r2["seconds_median"] else "n/a"))
        out.append("")
        if r2["gap"] is not None:
            out.append("The fresh case is five lines of Brightwater Dental Partners, a "
                       "company the player had not seen. A gap near zero says the reading "
                       "carried over rather than the answers.")
            out.append("")
        if r2["odd_key"]:
            out.append("Warning: a posted key string did not match the %s in the source "
                       "(%s). Check whether the fresh case was rekeyed after those rows "
                       "were filed." % (FRESH_KEY, ", ".join(r2["odd_key"])))
            out.append("")
        rb = r["r2_basis"]
        out.append("The fresh lines have no Why field of their own, so their basis rides "
                   "at the end of question C behind `Round2 basis, by line:`.")
        out.append("")
        if rb["lines"]:
            out.append("| Fresh line error type | Chips tapped |")
            out.append("| --- | --- |")
            for etype, chips in sorted(rb["by_type"].items(),
                                       key=lambda kv: (kv[0] == "clean line", kv[0])):
                out.append("| %s | %s |"
                           % (etype, "; ".join("%s %d" % (c, n)
                                               for c, n in chips.items())))
            out.append("")
            out.append("Read off %d fresh lines from %d player%s, %d of them carrying a "
                       "chip." % (rb["lines"], rb["players"],
                                  "" if rb["players"] == 1 else "s", rb["with_basis"]))
            out.append("")
        else:
            out.append("No fresh case basis in this export, which is what rows filed "
                       "before 13 September 2026 look like.")
            out.append("")
    else:
        out.append("## Round two, fresh cases")
        out.append("")
        out.append("No round two strings in this export, so no transfer rate.")
        out.append("")

    if r["professors"]:
        p = r["professors"]
        out.append("## Professors")
        out.append("")
        out.append("%d %s tapped the Professor chip (%s). Mean score %.1f of 14, "
                   "catch rate %s on the eight problem lines."
                   % (p["n"], "person" if p["n"] == 1 else "people",
                      ", ".join(p["codenames"]), p["mean_score"],
                      fmt_pct(p["catch_rate"], 1)))
        out.append("")

    out.append("## The four questions that are not asked")
    out.append("")
    out.append("Expected quality, confidence before the round, month end close "
               "experience and confidence after the round are never put to the player. "
               "Rows filed before 13 September 2026 carry fixed values that read like "
               "answers, and later rows carry the literal `not asked`. Neither is a "
               "player answer, so **none of these four columns enters any measure in "
               "this report**. They are counted here only so the export can be seen for "
               "what it holds.")
    out.append("")
    out.append("| Question | Sent as `not asked` | Fixed placeholder value | Something "
               "else | Blank |")
    out.append("| --- | --- | --- | --- | --- |")
    for item in r["intake"]:
        k = item["kinds"]
        out.append("| %s | %d | %d | %d | %d |"
                   % (item["label"], k["not asked"], k["placeholder"], k["value"],
                      k["blank"]))
    out.append("")
    stray = sum(i["kinds"]["value"] for i in r["intake"])
    if stray:
        out.append("%d cell%s carries something that is neither the literal nor a known "
                   "fixed value. Read those rows before you decide what they are; they "
                   "are excluded all the same." % (stray, "" if stray == 1 else "s"))
        out.append("")

    out.append("## Case version")
    out.append("")
    if r["case_versions"]:
        out.append("Question A carries the version and date of both cases, so a response "
                   "can be tied to the key it was scored against. Responses scored "
                   "against different case versions are never pooled.")
        out.append("")
        out.append("| Cases | Players |")
        out.append("| --- | --- |")
        for tag, count in r["case_versions"].items():
            out.append("| %s | %d |" % (tag, count))
        out.append("")
        if len(r["case_versions"]) > 1:
            out.append("Warning: more than one case version in this export. Split the "
                       "rows by version before any rate above is read.")
            out.append("")
    else:
        out.append("No case version in question A, which is what rows filed before 13 "
                   "September 2026 look like.")
        out.append("")
    if r["n_without_case"] and r["case_versions"]:
        one = r["n_without_case"] == 1
        out.append("%d row%s carr%s no case version at all."
                   % (r["n_without_case"], "" if one else "s", "ies" if one else "y"))
        out.append("")

    out.append("## Where the record disagrees with itself")
    out.append("")
    if r["disagreements"]:
        out.append("The call and the key in the Why field are the ones used above, "
                   "because the page writes that half after the basis step. Each line "
                   "below is a place where the Accept or Reject column, or this "
                   "script's own key, says something different.")
        out.append("")
        for item in r["disagreements"]:
            out.append("- %s" % item)
        out.append("")
    else:
        out.append("The Why field, the Accept or Reject column and the key in this "
                   "script agree on every call in this export.")
        out.append("")

    out.append("## Rows set aside")
    out.append("")
    out.append("Test codenames dropped: %s."
               % (", ".join(r["dropped_test"]) if r["dropped_test"] else "none"))
    out.append("")
    out.append("Repeat runs under a codename already counted: %s. The first run per "
               "codename is the one kept."
               % (", ".join(r["repeat_runs"]) if r["repeat_runs"] else "none"))
    out.append("")

    out.append("## Columns")
    out.append("")
    if r["missing"]:
        out.append("Not found in the export, so anything that needed them is missing "
                   "from the tables above:")
        out.append("")
        for label in r["missing"]:
            out.append("- %s" % label)
    else:
        out.append("Every question title matched a column in the export.")
    out.append("")
    return "\n".join(out) + "\n"


def print_summary(r, sentences, words, video, out_path):
    line = "-" * 62
    print(line)
    print("Second Pass findings")
    print(line)
    print("Rows in export        %d" % r["n_rows_raw"])
    print("Test rows dropped     %d" % len(r["dropped_test"]))
    print("Repeat runs           %d" % len(r["repeat_runs"]))
    print("Players counted       %d" % r["n_players"])
    print("Mean score of 14      %s"
          % ("%.1f" % r["mean_score"] if r["mean_score"] is not None else "n/a"))
    print("Catch rate            %s (%d of %d)"
          % (fmt_pct(r["catch_rate"], 1), r["catch_counts"][0], r["catch_counts"][1]))
    print("Let stand correctly   %s (%d of %d)"
          % (fmt_pct(r["let_stand_rate"], 1), r["let_stand_counts"][0],
             r["let_stand_counts"][1]))
    print("False flag rate       %s (%d of %d)"
          % (fmt_pct(r["false_flag_rate"], 1), r["false_flag_counts"][0],
             r["false_flag_counts"][1]))
    print("Lap time median/mean  %s / %s minutes"
          % ("%g" % r["minutes_median"] if r["minutes_median"] is not None else "n/a",
             "%.1f" % r["minutes_mean"] if r["minutes_mean"] is not None else "n/a"))
    print("Best streak posted    %s"
          % (r["streak_best"] if r["streak_best"] is not None else "n/a"))
    print("Flagged all fourteen  %d %s"
          % (len(r["flag_everything"]),
             "(" + ", ".join(r["flag_everything"]) + ")" if r["flag_everything"] else ""))
    print("Ranks                 " + ", ".join("%s %d" % (k, r["ranks"][k])
                                               for k in RANK_ORDER))
    print("Organizations         " + (", ".join("%s %d" % (k, v)
                                                for k, v in r["org_counts"].items())
                                      or "none found"))
    if r["professors"]:
        print("Professors            %d, mean %.1f of 14, catch %s"
              % (r["professors"]["n"], r["professors"]["mean_score"],
                 fmt_pct(r["professors"]["catch_rate"], 1)))
    if r["round2"]:
        r2 = r["round2"]
        print("Round two transfer    fresh %s (%d of %d) vs trained %s, gap %s, n=%d"
              % (fmt_pct(r2["fresh_rate"], 1), r2["right"], r2["total"],
                 fmt_pct(r2["trained_rate"], 1),
                 "%+.1f pts" % r2["gap"] if r2["gap"] is not None else "n/a", r2["n"]))
        if r2["seconds_median"]:
            print("Round two clock       %g seconds median" % r2["seconds_median"])
        if r2["odd_key"]:
            print("Round two KEY WARNING posted key not %s: %s"
                  % (FRESH_KEY, ", ".join(r2["odd_key"])))
    else:
        print("Round two transfer    no round two strings in question C")
    b = r["basis"]
    print("Calls with a basis    %s (%d of %d)"
          % (fmt_pct(b["basis_rate"], 1), b["calls_with_basis"], b["calls_total"]))
    print("Flags with words      %s (%d of %d)"
          % (fmt_pct(b["flag_words_rate"], 1), b["flags_with_words"], b["flags_total"]))
    print("Reasoning coverage    mean %s of 14 cards, %d gave a basis on all fourteen"
          % ("%.1f" % r["coverage_mean"] if r["coverage_mean"] is not None else "n/a",
             r["coverage_full"]))
    print("Case versions         "
          + (", ".join("%s (%d)" % (k, v) for k, v in r["case_versions"].items())
             or "none in question A"))
    print("Intake placeholders   EXCLUDED from every measure: "
          + ", ".join("%s (not asked %d, fixed %d, other %d)"
                      % (i["label"], i["kinds"]["not asked"], i["kinds"]["placeholder"],
                         i["kinds"]["value"]) for i in r["intake"]))
    if r["disagreements"]:
        print("CALL OR KEY DISAGREEMENTS %d, listed in the markdown"
              % len(r["disagreements"]))
    print(line)
    print("Basis chips by error type")
    for etype, bt in sorted(b["by_type"].items(),
                            key=lambda kv: (kv[0] == "clean line", kv[0])):
        chips = ", ".join("%s %d" % (c, n) for c, n in bt["chips"].items()) or "none"
        print("  %-24s %d of %d calls: %s" % (etype, bt["with_basis"], bt["calls"], chips))
    print(line)
    print("Catch rate by error type")
    for etype, b in sorted(r["by_type"].items(),
                           key=lambda kv: (kv[0] == "clean line", -(kv[1]["rate"] or 0))):
        print("  %-17s %s (%d of %d)"
              % (etype, fmt_pct(b["rate"], 1), b["right"], b["seen"]))
    print(line)
    print("For the write-up (%d words)" % words)
    for s in sentences:
        print("  " + s)
    bas = basis_sentence(r)
    if bas:
        print("")
        print("One more, on the reason behind the call")
        print("  " + bas)
    print("")
    print("For the video")
    print("  " + video)
    print(line)
    if r["missing"]:
        print("COLUMNS NOT FOUND (%d). Check the header row in the export:"
              % len(r["missing"]))
        for label in r["missing"]:
            print("  - %s" % label)
    else:
        print("All question titles matched a column.")
    print("Written to %s" % out_path)
    print(line)


def main():
    ap = argparse.ArgumentParser(
        description="Findings from the Second Pass: Beat the Machine responses CSV.")
    ap.add_argument("csv", help="path to the responses CSV")
    ap.add_argument("--out", help="markdown output path "
                                  "(default FINDINGS-<today>.md beside this script)")
    ap.add_argument("--fields", nargs="?", const="-", default=None,
                    help="also write the readout field contract as JSON; pass a path, "
                         "or leave it bare to print it")
    args = ap.parse_args()

    if not os.path.exists(args.csv):
        print("No file at %s" % args.csv)
        return 2

    r = analyze(args.csv)
    sentences, words, video = write_sentences(r)
    out_path = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "FINDINGS-%s.md" % datetime.date.today().isoformat())
    fields = readout_fields(r, args.csv)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(build_markdown(r, sentences, words, video, args.csv))
        handle.write("\n" + fields_block(fields, r["missing"]))
    if args.fields:
        import json
        blob = json.dumps(dict(fields), indent=2, ensure_ascii=False)
        if args.fields == "-":
            print(blob)
        else:
            with open(args.fields, "w", encoding="utf-8") as handle:
                handle.write(blob + "\n")
            print("Readout fields written to %s" % args.fields)
    print_summary(r, sentences, words, video, out_path)
    print("")
    print("Readout fields, for READOUT-TEMPLATE.md:")
    for name, value in fields:
        print("  %-34s %s" % (name, fmt_field(value, name)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
