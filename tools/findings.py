#!/usr/bin/env python3
"""Findings for "Second Pass: Beat the Machine".

Reads the Google Form responses CSV (Responses tab, File, Download, CSV) and writes
FINDINGS-<date>.md plus a printed summary.

Usage, from the repository root:

    python tools/findings.py responses.csv
    python tools/findings.py responses.csv --out FINDINGS-session.md --fields fields.json
    python tools/findings.py responses.csv --roster roster.csv
    python tools/findings.py responses.csv --cases path/to/beat-the-machine/cases
    python tools/findings.py responses.csv --scoring-sheet scoring-sheet.csv
    python tools/findings.py responses.csv --scores first.csv --second-scores second.csv
    python tools/findings.py probe.csv --synthetic-check
    python tools/findings.py responses.csv --resolve-conflict att-k3x=14

Columns are matched by the form's question titles, never by position. Any title the
script cannot find is printed under "Columns not found" and the measure that needed it
is skipped rather than guessed.

Scoring by recorded case version
--------------------------------
Question A of every record names the practice case version and the fresh case version it
was played on. The key, the error type, the Accept or Reject mapping and the basis key of
every line are read from cases/<version>.json for that version and from nowhere else. A
record is refused from scoring, with its reason printed, when it names no version, when it
names an authored case (an id beginning "own:", whose key lives in one browser rather than
in cases/), or when the version it names has no readable case file. A refused record is
never scored against another case's key. Records on different case sets (a practice
version paired with a fresh version) are reported in separate blocks and never pooled.

The cases directory is --cases when given, otherwise ../cases beside this script, otherwise
./cases under the working directory.

Attempts and people
-------------------
A row is one transmission. The counts are kept apart, and each is defined where it prints:
received attempts, completed attempts, distinct codenames and facilitator-confirmed
participants. A codename is a pseudonym a player typed, so a count of codenames is not a
count of people; only a consented roster the facilitator supplies can confirm people. Two
codenames count as one when they match after Unicode NFC normalization and case folding, so
"Zoë" typed composed and decomposed is one codename; the spelling as typed is what prints. The
first eligible attempt per codename (eligible means received, not excluded, and on a case
set this script can score) enters the first-attempt tables; every later attempt by that
codename goes to the reattempt table and enters no first-attempt rate.

A retry of one run posts the same attempt identifier with the same content, so rows that
share an identifier and match in every cell but the timestamp are one attempt sent twice, kept
once at the earliest timestamp. Rows that share an identifier and differ anywhere else are a
conflict: every record is printed with the columns where they differ, none of them enters a
count or a rate, and a later attempt under the same codename does not become a first attempt
over it. --resolve-conflict ID=ROW keeps the named sheet row (the header is row 1) once the
facilitator has read them.

Rows excluded from participant evidence
---------------------------------------
Test codenames, rows the page itself marked as a test attempt, blank codenames and
synthetic rows are excluded by rule, counted by reason, and listed with the sheet row and the
rule that excluded each one. A test codename is on the list of known test codenames, or is
made only of test words with "test" or "delete" among them, so "Test Pilot" stays in. A
synthetic row has a codename that begins with "Synthetic", or a cell or a basis Words line that
reads exactly "Synthetic test only", which is how the third independent review marked its
records. Participant text that merely mentions a synthetic test, and an attempt identifier on
its own, exclude nothing. Codenames are matched after NFKC normalization and case folding.
--synthetic-check scores those synthetic rows instead, for reproducing a review probe, and
stamps every output as not participant evidence.

Reason chip agreement
---------------------
A reason agrees when at least one chip was tapped and every chip tapped is in the line's
basis key. That is agreement with the accepted reason categories and is reported as its
own result, never as reasoning quality or learning gain. Where a case's flag lines accept
"no source on file" and its stand lines accept only "the figure and reason hold", those two
chips earn agreement without stating why, and the limitation prints beside the result.

Written explanations (from brightwater-v6)
-----------------------------------------
Every fresh case call on brightwater-v6 carries a three-part written explanation. The script
never scores one, and no educator has scored one yet. --scoring-sheet writes a sheet for an
independent educator to fill against RUBRIC.md, blind to the machine: no codename, key, call
result or chips, which ride in a separate facilitator key joined on response_id, with the
second scorer's rows drawn by hash. --scores and --second-scores read the filled sheets back,
and the findings then report the educator's scores and the two scorers' agreement apart from
reason chip agreement. The explanation is read from the Evidence, Period and Action segments
question C carries on each line, named in one block, EXPLANATION_PARTS.

Each part is held to the minimum the page applies before a call locks: at least two words and
eight letters or digits, and not a stock non-answer such as none, n/a or same as above
(explanation_problem(), the same rule as explainProblem() in index.html). A record on a fresh
case that asks for explanations is complete only when all three parts meet it on every line.
A part that falls short is never dropped: it stays on the scoring sheet as posted, named in
the below_minimum column, and the findings list it with its codename, line and reason.

Both CSV files are written safe to open in a spreadsheet: a text cell that begins with =, +,
-, @, a tab or a line break, or a full-width form of those signs, is prefixed with an
apostrophe, and the numeric columns keep their numbers.

The read before the draft
-------------------------
Before a single sentence of the AI draft is shown, the page asks every player to tap, from the
ledger alone, the accounts they would give a second look. It is required, it has no skip, and
it posts into the round one question with the case version, the read and the final call on each
line as letters, and three counts. A tapped account reads as a flag on each of its lines and an
untapped one as let it stand. For first attempts only, and inside each case set, the script
sets that read beside the final call on every practice line against the key from the case file:
held, changed toward the key, or changed away from it. The accounts tapped are the data, so the
read is rebuilt from them against the recorded version, and the letters and counts the page
posted are only checked against that. A read locked in after a call was made, and every row
filed before the read was required (the optional picks of up to three accounts, or "skipped"),
enter no count and are counted apart. This is descriptive agreement on a keyed exercise. Each
final call was made after reading the draft, the file on the card and, in practice mode, the
reveals of the lines before it, so a change toward the key is not attributed to the draft alone,
and it is never a learning gain.

Roster file (optional, --roster)
--------------------------------
A CSV the facilitator writes after a session, one row per codename, no accounts involved:

    participant,codename,consent,role
    P01,REDLINE,yes,student
    P01,REDLINE-2,yes,student
    P02,TIEOUT,yes,practitioner

codename and consent are required. participant is the facilitator's own label and defaults
to the codename, so two codenames one person used count once. consent must read yes for
the row to count. role is optional and is the facilitator's record, not a field the page
asks. Keep names out of this file; the key from label to person stays with the facilitator.

The field names printed under "Readout fields" are the names READOUT-TEMPLATE.md prints in
its cells. --fields writes the same set as JSON, run fields first and one block per case set.

Two attempt-record fields were renamed in product 1.6.1 (evidenceReferences became
evidenceSupplied, elapsedActiveSeconds became elapsedSecondsOnCard). This script reads the
form export rather than the saved record, so the rename does not move a number here. The
minutes reported come from question D, which the page fills from a clock that does not pause
in a background tab, so r1.lap_median is elapsed time on the page and never active review time.
"""

import argparse
import datetime
import json
import os
import re
import statistics
import sys
import unicodedata

# ---------------------------------------------------------------- the form
# The full question titles as the form builds them. The CSV header is the title. The call
# titles name Halyard's accounts because the form was built for Halyard; every case posts
# its line n into slot Cn, and the case file for the recorded version says what the slot
# holds. The titles are column names only and never a key.
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
SLOTS = len(CALL_TITLES)
WHY_TITLES = ["C%d. Why? (optional, one line)" % n for n in range(1, SLOTS + 1)]

CODENAME_TITLE = "Codename"
QA_TITLE = ("Question A. Which of your own calls from round one did the machine's "
            "list also raise?")
QB_TITLE = ("Question B. What did the list catch that you had missed, and why do you "
            "think you missed it?")
QC_TITLE = ("Question C. One thing you will do differently the next time you review an "
            "explanation a machine drafted.")
QD_TITLE = "Question D. About how many minutes did this take? Par is ten."
TIMESTAMP_TITLE = "Timestamp"
ROUND1_TITLE = ("Round one, question 1. Looking only at the numbers, which movements "
                "would you want explained, and what would you challenge?")

# The four questions the form marks required and the screen path never asks. Until 13
# September 2026 they carried fixed values (3, 5, 5 and "Once or twice") that landed in the
# sheet looking like answers; since then they carry the literal "not asked". Neither form is
# a player answer, so both are excluded from every measure below.
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
PLACEHOLDER_VALUES = {"3", "5", "once or twice"}

# ---------------------------------------------------------------- written explanations
# The one place the explanation payload is named. From brightwater-v6 every fresh case call on
# an assessment run carries a required three-part written explanation (index.html at commit
# 6447d97, EXPLAIN_VERSION explain-2026-09-13). The form posts it in question C, on each line of
# the Round2 basis, between the basis and the reason verdict:
#   3: Basis: wrong period | Evidence: ... | Period: ... | Action: ... | Reason: agrees | Key basis: ...
# The attempt record and the receipt carry the same answers as writtenExplanation
# {decisiveEvidence, periodRelevance, actionOrRequest} on each round two item. The page strips
# "|" from the answers and writes "none" for an empty one. If the page renames a label, change it
# here and nothing else in the script moves. The script never scores an explanation.
EXPLANATION_PARTS = [
    # part key, label posted in question C, key in the attempt record, rubric criterion
    ("evidence", "Evidence", "decisiveEvidence", "Decisive evidence"),
    ("period", "Period", "periodRelevance", "Why it matters for this period"),
    ("action", "Action", "actionOrRequest", "Action or source request"),
]
EXPLANATION_EMPTY = "none"
EXPLANATION_LABELS = "|".join(re.escape(part[1]) for part in EXPLANATION_PARTS)
# The fresh case versions filed before the page asked for a written explanation. Every other
# fresh case run as an assessment asks, so its records need all three parts on every line.
EXPLANATION_NOT_ASKED = frozenset(["brightwater-v2", "brightwater-v3", "brightwater-v4",
                                   "brightwater-v5"])

# ---------------------------------------------------------------- the minimum answer
# The rule the page applies before Lock it in, explainProblem() in index.html between the
# explain-minimum markers, written the same way here so a record the page could not have locked
# is still caught. tools/tests/explanation-minimum.json holds the cases both are tested on, and
# the parity test runs the page's own function on them. Change the two together.
#
# A part is answered when its text, cleaned the way the page posts it, holds at least two words
# and at least eight letters or digits between them, and is not a stock non-answer. A word is a
# run of letters or digits after NFKC normalization and lowercasing, with apostrophes dropped; a
# character from a script written without spaces (Chinese, Japanese kana, Thai, Lao, Khmer,
# Myanmar) counts as a word by itself. A stock non-answer is a phrase on the list below, or a text
# whose every word is on the word list ("none", "n/a", "test test", "same as above").
EXPLAIN_RULE = ("at least two words and eight letters or digits, and not a stock non-answer "
                "such as none, n/a or same as above")
EXPLAIN_MIN_WORDS = 2
EXPLAIN_MIN_CHARS = 8
EXPLAIN_STOCK_WORDS = frozenset("""
    none nothing nil null na nan no nope nah yes yep ok okay idk dunno unknown unsure same ditto
    tbd tba todo pass skip skipped test testing asdf asdfg qwerty x xx xxx blah etc whatever
""".split())
EXPLAIN_STOCK_PHRASES = frozenset([
    "n a", "not applicable", "not relevant", "no answer", "no comment", "no idea", "not sure",
    "i dont know", "i do not know", "dont know", "do not know", "im not sure", "i am not sure",
    "same as above", "same as before", "same as previous", "see above", "as above",
    "see previous", "see before", "nothing to add", "nothing else", "does not apply",
    "doesnt apply", "no reason", "just because", "i guess", "to do", "to be done",
    "to be determined", "fill in later",
])
# JavaScript's \s, spelled out, so the cleaning matches explainClean() character for character
EXPLAIN_SPACE_RE = re.compile("[\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f"
                              "\u205f\u3000\ufeff]+")
EXPLAIN_NO_SPACE_RANGES = ((0x0E00, 0x0EFF), (0x1000, 0x109F), (0x1780, 0x17FF),
                           (0x3040, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF),
                           (0xF900, 0xFAFF), (0x20000, 0x3134F))
EXPLAIN_APOSTROPHES = "'\u2018\u2019\u02bc"
# what each problem is called in the findings and on the scoring sheet
EXPLAIN_PROBLEM_LABEL = {
    "not posted": "not posted",
    "empty": "empty",
    "no words": "punctuation or symbols only",
    "stock": "a stock non-answer",
    "short": "under two words and eight letters or digits",
}

# ---------------------------------------------------------------- exclusion rules
# Each rule is narrow on purpose: a codename a real player might type ("Test Pilot", "Contest
# Winner") stays in. Codenames are compared after NFKC normalization and case folding, so a
# full-width spelling is read the same way as the plain one.
TEST_CODENAMES = {
    "test-agent-delete", "probe-two", "audit-test-delete",
    "rebuild-test-delete", "pages-check-delete", "test play",
    "test harness", "placeholder-check-delete",
}
# a codename made only of these words, with at least one marker, is a test codename
TEST_MARKER_WORDS = frozenset(["test", "testing", "delete"])
TEST_FILLER_WORDS = frozenset("""
    agent attempt audit check demo dummy facilitator fake harness me only pages placeholder play
    please probe qa rebuild row run sample temp tmp trial walk walkthrough
""".split())
TEST_ROW_RE = re.compile(r"test attempt,\s*exclude from reports", re.I)
# the codename opens with the word synthetic, as the third review's records do
SYNTHETIC_CODENAME_RE = re.compile(r"^\s*synthetic(?:$|[^\w])", re.I)
# the marker "Synthetic test only" as the whole of a cell, or as the whole Words line of a basis
SYNTHETIC_CELL_RE = re.compile(r"^\s*synthetic\s+test\s+only\.?\s*$", re.I)
SYNTHETIC_WORDS_RE = re.compile(r"\|\s*words\s*:\s*synthetic\s+test\s+only\.?\s*(?:\|\||$)", re.I)

EXCLUSION_LABELS = [
    ("test_codename", "Test codename"),
    ("marked_test_by_page", "Marked TEST ATTEMPT by the page"),
    ("blank_codename", "Blank codename"),
    ("synthetic_by_rule", "Synthetic row, excluded by rule"),
]

CHIPS = ["Beta Alpha Psi", "ACFE", "ASM", "NABA", "AAA", "GMU Student", "Professor",
         "Outside Mason"]
ORG_ORDER = list(CHIPS)

# The basis chips, from BASIS_FLAG and BASIS_HOLD in index.html.
BASIS_HOLD = "the figure and reason hold"
BASIS_NO_SOURCE = "no source on file"
BASIS_FLAG_CHIPS = ["figure does not tie", "direction wrong", "no source on file",
                    "wrong period", "wrong account", "nothing written where owed"]
BASIS_CHIPS = [BASIS_HOLD] + BASIS_FLAG_CHIPS

TYPE_ORDER = ["arithmetic", "wrong direction", "timing", "unsupported driver",
              "unsupported attribution", "wrong account", "no explanation", "clean line"]
TYPE_LABEL = {"arithmetic": "Arithmetic", "wrong direction": "Wrong direction",
              "timing": "Timing", "unsupported driver": "Unsupported driver",
              "unsupported attribution": "Unsupported attribution",
              "wrong account": "Wrong account",
              "no explanation": "No explanation",
              "clean line": "Clean line, the control"}

WORDS_LOWER = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
               "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
               "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def say(n):
    """A count inside a sentence, in words to twenty."""
    return WORDS_LOWER[n] if 0 <= n <= 20 else str(n)


# ---------------------------------------------------------------- reading files
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
    """Lowercase, straighten quotes, collapse whitespace."""
    text = (text or "")
    for curly, plain in (("’", "'"), ("‘", "'"), ("“", '"'),
                         ("”", '"'), ("–", "-"), ("—", "-"),
                         (" ", " ")):
        text = text.replace(curly, plain)
    return re.sub(r"\s+", " ", text).strip().lower()


def codename_key(code):
    """The key two codenames are counted as one under: NFC, the norm() tidy, then case folding.

    "Zoë" typed as one composed letter and as an e with a combining diaeresis is one codename,
    and so are "Heron" and "HERON". The codename as typed is kept for display."""
    return norm(unicodedata.normalize("NFC", code or "")).casefold()


def exclusion_key(code):
    """A codename as the exclusion rules read it: NFKC, so a full-width spelling reads as plain."""
    return norm(unicodedata.normalize("NFKC", code or "")).casefold()


# ---------------------------------------------------------------- the minimum answer
def explain_clean(text):
    """explainClean() in index.html: no bars or line breaks, whitespace collapsed and trimmed."""
    text = re.sub(r"[\r\n|]+", " ", "" if text is None else str(text))
    return EXPLAIN_SPACE_RE.sub(" ", text).strip(" ")


def explanation_words(text):
    """The words the minimum counts, as explainWords() in index.html finds them."""
    s = unicodedata.normalize("NFKC", explain_clean(text)).lower()
    for mark in EXPLAIN_APOSTROPHES:
        s = s.replace(mark, "")
    words, cur = [], []
    for ch in s:
        if unicodedata.category(ch)[0] in ("L", "N"):
            cp = ord(ch)
            if any(lo <= cp <= hi for lo, hi in EXPLAIN_NO_SPACE_RANGES):
                if cur:
                    words.append("".join(cur))
                    cur = []
                words.append(ch)
            else:
                cur.append(ch)
        elif cur:
            words.append("".join(cur))
            cur = []
    if cur:
        words.append("".join(cur))
    return words


def explanation_problem(text):
    """None when one written part meets the minimum, else "empty", "no words", "stock" or "short"."""
    if not explain_clean(text):
        return "empty"
    words = explanation_words(text)
    if not words:
        return "no words"
    if " ".join(words) in EXPLAIN_STOCK_PHRASES or all(w in EXPLAIN_STOCK_WORDS for w in words):
        return "stock"
    if len(words) < EXPLAIN_MIN_WORDS or sum(len(w) for w in words) < EXPLAIN_MIN_CHARS:
        return "short"
    return None


def explanation_blank(text):
    """True for a part with nothing written: not posted, empty, or the page's "none" for empty."""
    clean = explain_clean(text)
    return not clean or re.match(r"^none\.?$", clean, re.I) is not None


# ---------------------------------------------------------------- spreadsheet safety
# A cell a spreadsheet would read as a formula: OWASP's list (=, +, -, @, tab, carriage return),
# the line feed, and the full-width and small-form spellings of the four signs, which some
# spreadsheet programs fold to the plain ones.
FORMULA_LEADS = "=+-@\t\r\n\uff1d\uff0b\uff0d\uff20\ufe66\ufe62\ufe63\ufe6b"
NUMBER_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")


def sheet_cell(value, numeric=False):
    """A value made safe to open in a spreadsheet.

    A text cell that begins with a formula lead gets a leading apostrophe, which spreadsheet
    programs read as "this is text" and do not display. A numeric column keeps a real number as
    it is, a negative one included, and neutralizes anything else written into it."""
    if value is None:
        return ""
    if isinstance(value, bool):
        value = "yes" if value else "no"
    if numeric and isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if numeric and NUMBER_RE.match(text):
        return text
    if text and text[0] in FORMULA_LEADS:
        return "'" + text
    return text


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
        # Sheets sometimes trims or re-wraps a long title. Fall back to a prefix match,
        # then to a distinctive substring, before giving up.
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


def cell(row, col):
    return (row.get(col, "") if col else "") or ""


def pct(part, whole):
    if not whole:
        return None
    return 100.0 * part / whole


def fmt_pct(value, digits=0):
    if value is None:
        return "n/a"
    return ("%." + str(digits) + "f%%") % value


def _mean(values):
    values = [v for v in values if v is not None]
    return statistics.mean(values) if values else None


def _median(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


# ---------------------------------------------------------------- the case library
VERSION_SAFE_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$", re.I)


def find_cases_dir(explicit=None):
    """The cases directory: --cases, then ../cases beside this script, then ./cases."""
    if explicit:
        return explicit if os.path.isdir(explicit) else None
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (os.path.normpath(os.path.join(here, os.pardir, "cases")),
                      os.path.join(os.getcwd(), "cases")):
        if os.path.isdir(candidate):
            return candidate
    return None


class CaseLibrary(object):
    """Reads cases/<version>.json on demand. lookup() never substitutes another version."""

    def __init__(self, cases_dir):
        self.dir = cases_dir
        self._cache = {}

    def lookup(self, version):
        """(case, None) for a version this script can score, or (None, reason)."""
        if version in self._cache:
            return self._cache[version]
        result = self._load(version)
        self._cache[version] = result
        return result

    def _load(self, version):
        if not version:
            return None, "no case version recorded"
        if not VERSION_SAFE_RE.match(version):
            return None, "case version %r is not a version name" % version
        if not self.dir:
            return None, ("no cases directory found, so %s cannot be read; pass --cases "
                          "with the path to beat-the-machine/cases" % version)
        path = os.path.join(self.dir, version + ".json")
        if not os.path.isfile(path):
            return None, ("unsupported case version %s: there is no cases/%s.json, so no "
                          "key exists to score it against" % (version, version))
        try:
            with open(path, "r", encoding="utf-8") as handle:
                raw = json.load(handle)
        except (OSError, ValueError) as exc:
            return None, "cases/%s.json could not be read (%s)" % (version, exc)
        if raw.get("version") != version:
            return None, ("cases/%s.json carries version %r inside it, so it is not the "
                          "definition of %s" % (version, raw.get("version"), version))
        cards_raw = raw.get("cards")
        if not isinstance(cards_raw, list) or not cards_raw:
            return None, "cases/%s.json carries no cards" % version
        cards = []
        for i, c in enumerate(cards_raw):
            post = c.get("post") or {}
            key = (c.get("key") or "").lower()
            if key not in ("flag", "stand") or not c.get("type") or \
                    not post.get("flag") or not post.get("stand") or c.get("n") != i + 1:
                return None, ("cases/%s.json line %d lacks a key, a type, a post mapping "
                              "or its line number" % (version, i + 1))
            basis = c.get("basisKey")
            cards.append({
                "n": i + 1, "acct": str(c.get("acct", "")), "name": c.get("name", ""),
                "memo": c.get("memo") or "",
                "key": key, "type": c.get("type"),
                "post_flag": post["flag"], "post_stand": post["stand"],
                "basis_key": list(basis) if isinstance(basis, list) and basis else None,
            })
        case = {"version": version, "date": raw.get("date"), "company": raw.get("company"),
                "mode": raw.get("mode") or "practice", "cards": cards,
                "path": "cases/%s.json" % version,
                "has_basis_key": all(c["basis_key"] for c in cards)}
        return case, None


def key_letters(case):
    return "".join("F" if c["key"] == "flag" else "S" for c in case["cards"])


def reason_limitation(case):
    """The construct limit on reason chip agreement for one case, or None."""
    if not case or not case["has_basis_key"]:
        return None
    flags = [c for c in case["cards"] if c["key"] == "flag"]
    stands = [c for c in case["cards"] if c["key"] == "stand"]
    flag_ns = [c for c in flags
               if BASIS_NO_SOURCE in [norm(b) for b in c["basis_key"]]]
    stand_hold = [c for c in stands
                  if [norm(b) for b in c["basis_key"]] == [BASIS_HOLD]]
    if not flag_ns and not stand_hold:
        return None
    total = len(flags) + len(stands)
    free = len(flag_ns) + len(stand_hold)
    return {
        "version": case["version"], "flags": len(flags), "flags_no_source": len(flag_ns),
        "stands": len(stands), "stands_hold_only": len(stand_hold),
        "lines": total, "lines_without_why": free,
        "text": ("On %s, %s of the %s flag lines accept \"no source on file\" and %s of the "
                 "%s stand lines accept only \"the figure and reason hold\". A player who "
                 "taps those two chips after correct calls agrees on %s of %s lines without "
                 "stating why the evidence fails or holds, and the stand chip largely "
                 "restates the decision. Read this result as agreement with accepted reason "
                 "categories, not as reasoning quality."
                 % (case["version"], say(len(flag_ns)), say(len(flags)),
                    say(len(stand_hold)), say(len(stands)), say(free), say(total))),
    }


# ---------------------------------------------------------------- parsing a row
# Round two rides in question C. index.html builds the cell as
#   Round2: right call 4/5, right reason 3/5; calls FSFFS; key FSFFS; seconds 61.
ROUND2_RE = re.compile(
    r"round\s*2\s*:\s*(?:right\s+call\s*)?(?:(\d+)\s*/\s*(\d+))?"
    r"(?:\s*,\s*right\s+reason\s*(\d+)\s*/\s*(\d+))?"
    r"\s*;?\s*calls\s+([A-Za-z]+)\s*;?\s*key\s+([A-Za-z]+)",
    re.I)
R2_SECONDS_RE = re.compile(r"seconds\s+(\d+)|;\s*(\d+)\s*s\b", re.I)
STREAK_RE = re.compile(r"longest run of correct calls:\s*(\d+)", re.I)
ORG_RE = re.compile(r"organi[sz]ations?\s*:\s*(.*?)(?:\.|$)", re.I)

# The per line Why cell, since 13 September 2026:
#   Basis: no source on file; wrong period | Words: the freight moved || Line 12,
#   account 4000. Called: flag. Key: flag. Type: unsupported attribution. Correct.
#   Reason: agrees. Key basis: no source on file.
BASIS_RE = re.compile(r"basis\s*:\s*(.*?)(?:\s*\|\s*words\s*:\s*(.*?))?\s*$", re.I | re.S)
WHY_META_RE = re.compile(
    r"line\s+(\d+)\s*,\s*account\s+(\w+)\s*\.\s*called\s*:\s*(flag|stand)\s*\.\s*"
    r"key\s*:\s*(flag|stand)\s*\.\s*type\s*:\s*(.*?)\s*\.\s*"
    r"(correct|incorrect|missed)\s*\.?", re.I)
CALLED_RE = re.compile(r"called\s*:\s*(flag|stand)", re.I)
REASON_RE = re.compile(r"reason\s*:\s*(agrees|does not agree)", re.I)
KEYBASIS_RE = re.compile(r"key\s+basis\s*:\s*(.*?)\s*\.?\s*$", re.I | re.S)
NO_CHIPS = "none recorded"

R2_BASIS_RE = re.compile(
    r"round2\s+basis,\s*by\s+line\s*:\s*(.*?)(?:\s*fresh case\s*:|\s*$)", re.I | re.S)
EXPLANATION_SEGMENT_RE = re.compile(
    r"\|\s*(%s)\s*:\s*(.*?)(?=\s*\|\s*(?:%s|reason|key\s+basis)\s*:|$)"
    % (EXPLANATION_LABELS, EXPLANATION_LABELS), re.I | re.S)
# The case line from caseLine() in question A:
#   Case: halyard, version halyard-v4 (practice, 14 lines) and brightwater-v5
#   (assessment, 5 lines), dated 2026-09-13, loaded from cases/ files.
#   Case: own:Kestrel:3, version kestrel-own-3 (practice, 12 lines), no fresh case,
#   dated 2026-09-13, loaded from this browser, written by author.html.
CASES_RE = re.compile(
    r"case\s*:\s*([^,]+?)\s*,\s*version\s+([\w.:-]+)\s*(?:\(\s*\w+\s*,\s*(\d+)\s*lines?\s*\))?"
    r"(?:\s*and\s+([\w.:-]+)\s*(?:\(\s*\w+\s*,\s*(\d+)\s*lines?\s*\))?)?"
    r"(?:\s*,\s*no fresh case)?"
    r"\s*,\s*dated\s+([\d-]+)"
    r"(?:\s*,\s*loaded from\s+(.*?))?\s*\.", re.I)
# The shape filed before 13 September 2026:
#   Cases: halyard-v3 and brightwater-v2, dated 2026-09-12, loaded from cases/ files.
CASES_RE_OLD = re.compile(
    r"cases\s*:\s*([\w.-]+)\s+and\s+([\w.-]+)\s*,\s*dated\s+([\d-]+)"
    r"(?:\s*,\s*loaded from\s+(.*?))?\s*\.", re.I)
PRODUCT_RE = re.compile(r"product\s*:\s*(.+?)\s*\.(?=\s+[A-Z]|$)", re.I)
ATTEMPT_RE = re.compile(r"attempt\s+id\s*:\s*([\w:.-]+?)\s*,\s*run\s+(\d+)", re.I)
REASON_SCORE_RE = re.compile(
    r"reason\s+score\s*:\s*(\d+)\s+of\s+(\d+)\s+in\s+round\s+one"
    r"(?:\s+and\s+(\d+)\s+of\s+(\d+)\s+on\s+the\s+fresh\s+case)?", re.I)
RESULT_RE = re.compile(
    r"result\s*:\s*right\s+call\s+(\d+)\s+of\s+(\d+)\s*,\s*right\s+reason\s+(\d+)"
    r"\s+of\s+(\d+)\s*,\s*(\d+)\s+caught\s*,\s*(\d+)\s+let\s+stand\s+correctly\s*,\s*"
    r"(\d+)\s+false\s+flags?\s*,\s*([\d,]+)\s+points\s*,\s*rank\s+(\w+)", re.I)
# The round one question, from prepickLine() in index.html. The required read since the
# evening of 13 September 2026:
#   Prepicks: 4200; 5100; 6000. Required read before the AI draft, case halyard-v4, by line,
#   F tapped for a second look and S left untapped: FSFSSSSSSSFSSS. Final calls after the
#   draft: FFFSSSFFSSFFSF. Against the key: 5 changed toward it, 0 changed away from it, 9 held.
# with " Taken after a call was locked, so not a read before the draft." when it was. Earlier
# that day the step was optional and capped at three: "Prepicks: 4200; 6000; 6400." or
# "Prepicks: skipped."
PREPICK_RE = re.compile(r"prepicks\s*:\s*(.*?)\s*(?:\.\s*required read before|\.?\s*$)", re.I | re.S)
PREPICK_READ_RE = re.compile(
    r"required read before the ai draft\s*,\s*case\s+([\w.:+-]+?)\s*,\s*by line[^:]*:\s*"
    r"([FS]+)\s*\.\s*final calls after the draft\s*:\s*([FS-]+)\s*\.\s*"
    r"against the key\s*:\s*(\d+)\s+changed toward it\s*,\s*(\d+)\s+changed away from it\s*,"
    r"\s*(\d+)\s+held", re.I)
PREPICK_LATE_RE = re.compile(r"taken after a call was locked", re.I)
PREPICK_NOTE = ("Descriptive agreement on a keyed exercise, first attempts only. The read is "
                "taken from the ledger alone before the AI draft is shown, and a tapped account "
                "reads as a flag on its lines. Each final call came after reading the draft, "
                "the file on the card and, in practice mode, the reveals of the lines before "
                "it, so a change toward the key is not credited to the draft alone. It is not "
                "a pre-test and post-test, and it is not a learning gain.")


def reason_agrees(chips, basis_key):
    """The page's rule: at least one chip tapped and every chip tapped is in the key."""
    if not chips:
        return False
    keyset = {norm(k) for k in basis_key}
    return all(norm(c) in keyset for c in chips)


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


def parse_why(text):
    """One Why cell into a dict, or None when the cell carries nothing readable."""
    text = (text or "").strip()
    if not text:
        return None
    left, _, right = text.partition("||")
    if not right:
        # A cell filed before 13 September 2026 carries only the metadata half.
        left, right = "", text
    chips, words = parse_basis(left) if left.strip() else ([], "")
    meta = WHY_META_RE.search(right)
    said = REASON_RE.search(right)
    keyb = KEYBASIS_RE.search(right)
    out = {"chips": chips, "words": words, "called": None, "key": None,
           "type": None, "correct": None, "line": None, "acct": None,
           "has_basis": bool(left.strip()),
           "reason_right": (norm(said.group(1)) == "agrees") if said else None,
           "key_basis": split_chips(keyb.group(1)) if keyb else []}
    if meta:
        out["line"] = int(meta.group(1))
        out["acct"] = meta.group(2)
        out["called"] = meta.group(3).lower()
        out["key"] = meta.group(4).lower()
        out["type"] = meta.group(5).strip()
        out["correct"] = norm(meta.group(6)) == "correct"
    else:
        called = CALLED_RE.search(right)
        if called:
            out["called"] = called.group(1).lower()
    return out


def parse_r2_basis(text, case2):
    """The fresh case basis at the tail of question C, as a list of (n, chips, words, reason)."""
    match = R2_BASIS_RE.search(text or "")
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
        # the basis half stops at the first explanation label or " | Reason:" after it
        head = re.split(r"\s*\|\s*(?:%s|reason)\s*:" % EXPLANATION_LABELS, body, 1,
                        flags=re.I)[0]
        chips, words = parse_basis(head)
        reason = (norm(said.group(1)) == "agrees") if said else None
        if reason is None and case2 and 1 <= n <= len(case2["cards"]):
            bkey = case2["cards"][n - 1]["basis_key"]
            reason = reason_agrees(chips, bkey) if bkey else None
        out.append((n, chips, words, reason))
    return out


def parse_explanations(qc_text, lines):
    """{line: {part: text as posted}} from the Round2 basis in question C.

    Every segment the page posted is kept as written, "none" and a non-answer included, so a part
    that falls short stays visible. explanation_gaps() says which parts fall short and why."""
    match = R2_BASIS_RE.search(qc_text or "")
    if not match:
        return {}
    out = {}
    for piece in match.group(1).split("||"):
        num = re.match(r"^\s*(\d+)\s*:\s*(.*)$", piece.strip(), re.S)
        if not num or not 1 <= int(num.group(1)) <= lines:
            continue
        parts = {}
        body = re.split(r"\s*\|\s*reason\s*:", num.group(2), 1, flags=re.I)[0]
        for seg in EXPLANATION_SEGMENT_RE.finditer(body):
            key = next(p[0] for p in EXPLANATION_PARTS if norm(p[1]) == norm(seg.group(1)))
            parts[key] = seg.group(2).strip()
        if parts:
            out[int(num.group(1))] = parts
    return out


def explanation_required(case2):
    """True when the fresh case asks every call for the three written parts."""
    return bool(case2) and case2.get("mode") == "assessment" and \
        case2["version"] not in EXPLANATION_NOT_ASKED


def part_problems(parts):
    """[(part key, problem)] for one fresh line's posted parts, in EXPLANATION_PARTS order."""
    out = []
    for key, _label, _record, _criterion in EXPLANATION_PARTS:
        if key not in (parts or {}):
            out.append((key, "not posted"))
            continue
        problem = explanation_problem(parts[key])
        if problem:
            out.append((key, problem))
    return out


def explanation_gaps(a):
    """Every required part, on every fresh line, that falls below the minimum, in line order."""
    case2 = a["case2"]
    if not explanation_required(case2):
        return []
    gaps = []
    for n in range(1, len(case2["cards"]) + 1):
        parts = a["explanations"].get(n) or {}
        for key, problem in part_problems(parts):
            gaps.append({"line": n, "part": key, "text": parts.get(key), "problem": problem})
    return gaps


def parse_cases(text):
    """The case line out of question A, in either shape, or None."""
    match = CASES_RE.search(text or "")
    if match:
        run_id = match.group(1).strip()
        return {"id": run_id, "one": match.group(2),
                "one_lines": int(match.group(3)) if match.group(3) else None,
                "two": match.group(4),
                "two_lines": int(match.group(5)) if match.group(5) else None,
                "date": match.group(6),
                "source": (match.group(7) or "").strip() or None,
                "authored": run_id.lower().startswith("own:")}
    match = CASES_RE_OLD.search(text or "")
    if not match:
        return None
    return {"id": match.group(1).split("-")[0], "one": match.group(1), "one_lines": None,
            "two": match.group(2), "two_lines": None, "date": match.group(3),
            "source": (match.group(4) or "").strip() or None, "authored": False}


def parse_prepicks(text):
    """The round one cell, or None when it carries no Prepicks sentence at all.

    required is True only for the required read, which alone carries a version, the letters
    and the counts. picks is the accounts tapped, empty for an old skip or "not recorded"."""
    raw = (text or "").strip()
    match = PREPICK_RE.search(raw)
    if not match:
        return None
    body = match.group(1).strip().strip(".")
    read = PREPICK_READ_RE.search(raw)
    out = {"picks": [], "required": bool(read), "skipped": False, "not_recorded": False,
           "version": None, "read": None, "final": None, "posted": None,
           "late": bool(PREPICK_LATE_RE.search(raw))}
    if norm(body) == "skipped":
        out["skipped"] = True
    elif norm(body) == "not recorded":
        out["not_recorded"] = True
    elif body:
        out["picks"] = [piece.strip() for piece in body.split(";") if piece.strip()]
    if read:
        out.update({"version": read.group(1), "read": read.group(2).upper(),
                    "final": read.group(3).upper(),
                    "posted": (int(read.group(4)), int(read.group(5)), int(read.group(6)))})
    return out


def score_prepick(a, case):
    """The required read against the final calls, line by line, on the recorded version.

    a["read"] stays None for a row with no required read. The read is rebuilt from the
    accounts tapped, and the letters and counts the page posted are checked against it."""
    p = a["prepicks"]
    a["read"] = None
    if not p or not p["required"]:
        return
    code, version, cards = a["codename"], case["version"], case["cards"]
    dis = a["disagreements"]
    if p["version"] and p["version"] != version:
        dis.append("%s: the read before the draft names case %s, question A names %s"
                   % (code, p["version"], version))
    tapped = {norm(x) for x in p["picks"]}
    read = ["flag" if norm(c["acct"]) in tapped else "stand" for c in cards]
    letters = "".join("F" if r == "flag" else "S" for r in read)
    if not p["picks"]:
        dis.append("%s: the read before the draft carries no account, which the page does not "
                   "allow" % code)
    if p["read"] and p["read"] != letters:
        dis.append("%s: the page posted the read %s, the accounts tapped read %s on %s"
                   % (code, p["read"], letters, version))
    if p["late"]:
        a["read"] = {"late": True}
        return
    moves = []
    for i, card in enumerate(cards):
        final = a["calls"][i] if i < len(a["calls"]) else None
        if final is None:
            moves.append(None)
        elif final == read[i]:
            moves.append("held")
        elif final == card["key"]:
            moves.append("toward")
        else:
            moves.append("away")
    counts = (moves.count("toward"), moves.count("away"), moves.count("held"))
    if p["posted"] and p["posted"] != counts:
        dis.append("%s: the page posted %d toward, %d away and %d held after the draft, %s "
                   "reads %d, %d and %d" % ((code,) + p["posted"] + (version,) + counts))
    a["read"] = {"late": False, "read": read, "moves": moves, "toward": counts[0],
                 "away": counts[1], "held": counts[2],
                 "compared": sum(1 for m in moves if m is not None)}


def parse_attempt(text):
    match = ATTEMPT_RE.search(text or "")
    if not match:
        return None, None
    return match.group(1), int(match.group(2))


def intake_kind(value):
    text = (value or "").strip()
    if not text:
        return "blank"
    if norm(text) == NOT_ASKED:
        return "not asked"
    if norm(text) in PLACEHOLDER_VALUES:
        return "placeholder"
    return "value"


def parse_orgs(text):
    match = ORG_RE.search(text or "")
    chips = []
    if match:
        for piece in re.split(r"[;,]", match.group(1)):
            piece = piece.strip().strip(".")
            if piece:
                chips.append(piece)
    if not chips:
        low = norm(text)
        chips = [chip for chip in CHIPS if norm(chip) in low]
    tidy = []
    for chip in chips:
        hit = next((c for c in CHIPS if norm(c) == norm(chip)), chip)
        if hit not in tidy:
            tidy.append(hit)
    return tidy


def parse_round2(cells):
    """The Round2 string, read from question C first and any other free text after."""
    for text in cells:
        match = ROUND2_RE.search(text or "")
        if not match:
            continue
        right, total, r_right, r_total, calls, key = match.groups()
        sec_m = R2_SECONDS_RE.search(text)
        return {"posted_right": int(right) if right is not None else None,
                "posted_total": int(total) if total is not None else None,
                "posted_reason": (int(r_right), int(r_total)) if r_right is not None else None,
                "calls": calls.upper(), "key": (key or "").upper(),
                "seconds": int(sec_m.group(1) or sec_m.group(2)) if sec_m else None}
    return None


def parse_minutes(text):
    match = re.search(r"\d+(?:\.\d+)?", text or "")
    if not match:
        return None
    value = float(match.group(0))
    return value if value > 0 else None


TS_FORMATS = ["%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
              "%m/%d/%Y %H:%M:%S", "%Y/%m/%d %I:%M:%S %p", "%m/%d/%Y %I:%M:%S %p",
              "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%m/%d/%Y %H:%M", "%Y-%m-%d"]


def parse_timestamp(text):
    t = (text or "").strip()
    if not t:
        return None
    t = re.sub(r"(?:\s*(?:z|utc|gmt)?\s*[+-]\d\d:?\d\d|\s*z|\s+(?:utc|gmt|[ecmp][sd]t))$",
               "", t, flags=re.I)
    t = re.sub(r"\.\d+$", "", t)
    for f in TS_FORMATS:
        try:
            return datetime.datetime.strptime(t, f)
        except ValueError:
            pass
    return None


# ---------------------------------------------------------------- the roster
class InputError(Exception):
    """A roster or a scored sheet this script cannot read, reported instead of guessed."""


RosterError = InputError


CONSENT_YES = {"yes", "y", "true", "1", "consented"}


def read_roster(path):
    """The facilitator's consented roster as a list of dicts with the four fields."""
    if not os.path.isfile(path):
        raise RosterError("No roster file at %s" % path)
    rows, headers = read_rows(path)
    lookup = {norm(h): h for h in headers}
    if "codename" not in lookup or "consent" not in lookup:
        raise RosterError("The roster at %s needs a codename column and a consent column; "
                          "it has %s" % (path, ", ".join(headers) or "no header"))
    out = []
    for r in rows:
        code = cell(r, lookup["codename"]).strip()
        label = cell(r, lookup.get("participant")).strip() or code
        out.append({"participant": label, "codename": code,
                    "consent": norm(cell(r, lookup["consent"])) in CONSENT_YES,
                    "role": cell(r, lookup.get("role")).strip() or None})
    return out


def confirm_roster(roster, attempts):
    """Match a roster against received attempts. Only consented rows are read."""
    received_codes = {a["code_key"] for a in attempts}
    consented = [r for r in roster if r["consent"] and r["codename"]]
    claims = {}
    for r in consented:
        claims.setdefault(codename_key(r["codename"]), set()).add(r["participant"])
    conflicts = sorted(code for code, who in claims.items() if len(who) > 1)
    confirmed, roles = {}, {}
    for r in consented:
        code = codename_key(r["codename"])
        if code in conflicts or code not in received_codes:
            continue
        confirmed.setdefault(r["participant"], set()).add(code)
        if r["role"]:
            roles.setdefault(r["participant"], r["role"])
    role_counts = {}
    for label in confirmed:
        role = roles.get(label, "role not recorded")
        role_counts[role] = role_counts.get(role, 0) + 1
    roster_codes = set(claims)
    return {
        "rows": len(roster),
        "consented_rows": len(consented),
        "rows_without_consent": sum(1 for r in roster if not r["consent"]),
        "confirmed": confirmed,
        "n_confirmed": len(confirmed),
        "code_to_participant": {code: next(iter(who)) for code, who in claims.items()
                                if len(who) == 1},
        "roster_codenames_without_attempt": len(roster_codes - received_codes),
        "attempt_codenames_not_on_roster": len(received_codes - roster_codes),
        "codename_conflicts": conflicts,
        "roles": dict(sorted(role_counts.items(), key=lambda kv: (-kv[1], kv[0]))),
    }


# ---------------------------------------------------------------- one attempt
def test_codename_rule(code):
    """The rule that makes a codename a test codename, in words, or None."""
    key = exclusion_key(code)
    if key in TEST_CODENAMES:
        return "a known test codename"
    words = [w for w in re.split(r"[^\w]+|_", key) if w]
    if words and any(w in TEST_MARKER_WORDS for w in words) and \
            all(w in TEST_MARKER_WORDS or w in TEST_FILLER_WORDS or w.isdigit() for w in words):
        return "a codename made only of test words"
    return None


def synthetic_rule(code, row):
    """The synthetic marker a row carries, in words, or None. The attempt id alone is no marker."""
    if SYNTHETIC_CODENAME_RE.search(unicodedata.normalize("NFKC", code or "")):
        return "the codename begins with Synthetic"
    for value in row.values():
        text = unicodedata.normalize("NFKC", value or "")
        if SYNTHETIC_CELL_RE.search(text) or SYNTHETIC_WORDS_RE.search(text):
            return "a cell or a Words line reads Synthetic test only"
    return None


def exclusion_of(code, qa, qb, row, synthetic_check, sheet_row=None):
    """(reason key, detail) when a row is excluded from participant evidence, else None.

    The detail names the codename as typed, the sheet row and the rule that excluded it."""
    def detail(text, rule):
        where = ("sheet row %d, " % sheet_row) if sheet_row else ""
        return "%s (%srule: %s)" % (text, where, rule)
    if not code:
        return "blank_codename", detail("(blank codename)", "no codename")
    rule = test_codename_rule(code)
    if rule:
        return "test_codename", detail(code, rule)
    if TEST_ROW_RE.search(qa):
        return "marked_test_by_page", detail(code, "the page marked it TEST ATTEMPT")
    rule = synthetic_rule(code, row)
    if rule and not synthetic_check:
        return "synthetic_by_rule", detail(code, rule)
    return None


def set_label(one, two):
    return "%s with %s" % (one, two or "no fresh case")


def score_practice(a, row, cols, case):
    """Round one against the case file for the recorded version, and nothing else."""
    cards = case["cards"]
    code, version = a["codename"], case["version"]
    dis = a["disagreements"]
    posted, whys, calls, reasons = [], [], [], []
    for i, card in enumerate(cards):
        raw = cell(row, cols["call"][i]).strip()
        if not raw:
            p = None
        elif norm(raw) == norm(card["post_flag"]):
            p = "flag"
        elif norm(raw) == norm(card["post_stand"]):
            p = "stand"
        else:
            p = None
            dis.append("%s line %d: the Accept or Reject column reads %r, which %s does "
                       "not post on this line" % (code, i + 1, raw, version))
        posted.append(p)
        parsed = parse_why(cell(row, cols["why"][i]))
        whys.append(parsed)
        call = parsed["called"] if (parsed and parsed["called"]) else p
        calls.append(call)
        if parsed and parsed["called"] and p and parsed["called"] != p:
            dis.append("%s line %d: Why says %s, the Accept or Reject column says %s"
                       % (code, i + 1, parsed["called"], p))
        if parsed and parsed["line"] is not None and parsed["line"] != card["n"]:
            dis.append("%s slot %d: Why names line %d, %s puts line %d here"
                       % (code, i + 1, parsed["line"], version, card["n"]))
        if parsed and parsed["acct"] and parsed["acct"] != card["acct"]:
            dis.append("%s line %d: Why names account %s, %s carries account %s"
                       % (code, i + 1, parsed["acct"], version, card["acct"]))
        if parsed and parsed["key"] and parsed["key"] != card["key"]:
            dis.append("%s line %d: Why says the key is %s, %s carries %s"
                       % (code, i + 1, parsed["key"], version, card["key"]))
        if parsed and parsed["type"] and norm(parsed["type"]) != norm(card["type"]):
            dis.append("%s line %d: Why says the type is %s, %s carries %s"
                       % (code, i + 1, parsed["type"], version, card["type"]))
        if parsed and parsed["key_basis"] and card["basis_key"] and \
                not {norm(x) for x in parsed["key_basis"]} <= {norm(x) for x in card["basis_key"]}:
            dis.append("%s line %d: Why carries key basis %s, which reaches outside the %s "
                       "basis key %s"
                       % (code, i + 1, "; ".join(parsed["key_basis"]), version,
                          "; ".join(card["basis_key"])))
        # The reason: the page's own verdict where the cell carries it, the case file's
        # basis key where it does not, and unscored where neither exists.
        if parsed and parsed["reason_right"] is not None:
            reason = parsed["reason_right"]
            if parsed["has_basis"] and card["basis_key"] and \
                    reason_agrees(parsed["chips"], card["basis_key"]) != reason:
                dis.append("%s line %d: the page posted Reason %s, the chips against the "
                           "%s basis key read %s"
                           % (code, i + 1, "agrees" if reason else "does not agree",
                              version, "agrees" if not reason else "does not agree"))
        elif parsed and parsed["has_basis"] and card["basis_key"]:
            reason = reason_agrees(parsed["chips"], card["basis_key"])
        else:
            reason = None
        reasons.append(reason)
    for j in range(len(cards), SLOTS):
        extra = cell(row, cols["call"][j]).strip()
        parsed = parse_why(cell(row, cols["why"][j]))
        if extra or (parsed and parsed["called"]):
            dis.append("%s slot %d: a call is recorded past the %d lines of %s"
                       % (code, j + 1, len(cards), version))
    answered = [i for i, c in enumerate(calls) if c is not None]
    correct = [i for i in answered if calls[i] == cards[i]["key"]]
    a.update({
        "posted": posted, "whys": whys, "calls": calls, "reasons": reasons,
        "answered": answered, "score": len(correct),
        "reason_right": sum(1 for v in reasons if v),
        "reason_scored": sum(1 for v in reasons if v is not None),
        "flags": sum(1 for c in calls if c == "flag"),
        "coverage": sum(1 for w in whys if w and w["chips"]),
    })
    if a["posted_result"]:
        pr = a["posted_result"]
        if pr["calls_total"] != len(cards) or pr["right"] != len(correct):
            dis.append("%s: the page posted right call %d of %d, %s scores %d of %d"
                       % (code, pr["right"], pr["calls_total"], version, len(correct),
                          len(cards)))


def score_fresh(a, qc, other_text, case2):
    """Round two against the case file for the recorded fresh version."""
    r2 = parse_round2([qc] + other_text)
    a["r2_basis"] = parse_r2_basis(qc, case2)
    if not r2:
        a["fresh"] = None
        return
    letters = key_letters(case2)
    calls = r2["calls"]
    seen = min(len(calls), len(letters))
    right = sum(1 for i in range(seen) if calls[i] == letters[i])
    code, version = a["codename"], case2["version"]
    if r2["key"] and r2["key"] != letters:
        a["disagreements"].append("%s fresh case: the page posted key %s, %s carries %s"
                                  % (code, r2["key"], version, letters))
    if r2["posted_right"] is not None and (r2["posted_right"] != right or
                                           r2["posted_total"] != len(letters)):
        a["disagreements"].append("%s fresh case: the page posted %d/%d, %s scores %d/%d"
                                  % (code, r2["posted_right"], r2["posted_total"] or 0,
                                     version, right, len(letters)))
    a["fresh"] = {"right": right, "total": len(letters), "seen": seen, "calls": calls,
                  "seconds": r2["seconds"]}


def completion_of(a, row, cols):
    """True when every practice line and every named fresh line carries a call, and, on a fresh
    case that asks for written explanations, every part on every fresh line meets the minimum."""
    case1, case2 = a["case1"], a["case2"]
    if case1:
        practice_ok = len(a["answered"]) == len(case1["cards"])
    else:
        lines = a["cases"]["one_lines"] if a["cases"] else None
        if not lines or lines > SLOTS:
            return False
        got = 0
        for i in range(lines):
            parsed = parse_why(cell(row, cols["why"][i]))
            if cell(row, cols["call"][i]).strip() or (parsed and parsed["called"]):
                got += 1
        practice_ok = got == lines
    if not practice_ok:
        return False
    two = a["cases"]["two"] if a["cases"] else None
    if not two:
        return True
    if case2:
        if not (a["fresh"] and a["fresh"]["seen"] == len(case2["cards"])):
            return False
        return not a["explanation_gaps"]
    r2 = parse_round2([cell(row, cols["qc"])])
    lines = a["cases"]["two_lines"]
    return bool(r2 and lines and len(r2["calls"]) == lines)


def read_attempt(index, row, cols, library):
    code = cell(row, cols["code"]).strip()
    qa, qb, qc = cell(row, cols["qa"]), cell(row, cols["qb"]), cell(row, cols["qc"])
    attempt_id, run_index = parse_attempt(qb)
    result_m = RESULT_RE.search(qb)
    reason_m = REASON_SCORE_RE.search(qb)
    product_m = PRODUCT_RE.search(qa)
    streak_m = STREAK_RE.search(qb)
    cases = parse_cases(qa)
    a = {
        "row_index": index, "sheet_row": index + 1, "codename": code,
        "code_key": codename_key(code),
        "timestamp": cell(row, cols["ts"]), "ts_value": parse_timestamp(cell(row, cols["ts"])),
        "attempt_id": attempt_id, "run_index": run_index,
        "product": product_m.group(1).strip() if product_m else None,
        "orgs": parse_orgs(qa), "cases": cases,
        "prepicks": parse_prepicks(cell(row, cols["r1"])),
        "minutes": parse_minutes(cell(row, cols["qd"])),
        "best_streak": int(streak_m.group(1)) if streak_m else None,
        "points": int(result_m.group(8).replace(",", "")) if result_m else None,
        "posted_rank": result_m.group(9) if result_m else None,
        "posted_result": ({"right": int(result_m.group(1)), "calls_total": int(result_m.group(2))}
                          if result_m else None),
        "reason_posted_r1": (int(reason_m.group(1)), int(reason_m.group(2))) if reason_m else None,
        "intake": {label: intake_kind(cell(row, col)) for label, col in cols["intake"]},
        "disagreements": [], "supported": False, "refusal": None,
        "case1": None, "case2": None, "set": None,
        "calls": [], "posted": [], "whys": [], "reasons": [], "answered": [], "score": 0,
        "reason_right": 0, "reason_scored": 0, "flags": 0, "coverage": 0,
        "fresh": None, "r2_basis": [], "explanations": {}, "explanation_gaps": [], "read": None,
        "after_conflict": None,
    }
    if not cases:
        a["refusal"] = "no case version recorded in question A"
    elif cases["authored"]:
        a["refusal"] = ("authored case %s (%s): its key lives in the author's browser, not in "
                        "cases/, so it is not scored" % (cases["id"], cases["one"]))
    else:
        case1, why1 = library.lookup(cases["one"])
        case2, why2 = (library.lookup(cases["two"]) if cases["two"] else (None, None))
        if not case1:
            a["refusal"] = why1
        elif cases["two"] and not case2:
            a["refusal"] = "fresh case: " + why2
        elif len(case1["cards"]) > SLOTS:
            a["refusal"] = ("%s has %d lines and the form has %d slots"
                            % (case1["version"], len(case1["cards"]), SLOTS))
        else:
            a["case1"], a["case2"] = case1, case2
    if a["case1"]:
        a["supported"] = True
        a["set"] = set_label(a["case1"]["version"], a["case2"]["version"] if a["case2"] else None)
        if cases["one_lines"] and cases["one_lines"] != len(a["case1"]["cards"]):
            a["disagreements"].append("%s: question A says %d practice lines, %s has %d"
                                      % (code, cases["one_lines"], a["case1"]["version"],
                                         len(a["case1"]["cards"])))
        score_practice(a, row, cols, a["case1"])
        score_prepick(a, a["case1"])
        if a["case2"]:
            others = [cell(row, c) for c in cols["why"] if c] + [qb, qa]
            score_fresh(a, qc, others, a["case2"])
            a["explanations"] = parse_explanations(qc, len(a["case2"]["cards"]))
            a["explanation_gaps"] = explanation_gaps(a)
    a["completed"] = completion_of(a, row, cols)
    return a


# ---------------------------------------------------------------- the analysis
def match_columns(headers):
    cols = Columns(headers)
    found = {
        "code": cols.find(CODENAME_TITLE, "Codename"),
        "qa": cols.find(QA_TITLE, "Question A (case line and organizations)",
                        contains=["question a"]),
        "qb": cols.find(QB_TITLE, "Question B (attempt id and result)", contains=["question b"]),
        "qc": cols.find(QC_TITLE, "Question C (round two string)", contains=["question c"]),
        "qd": cols.find(QD_TITLE, "Question D (minutes)", contains=["question d"]),
        "ts": cols.find(TIMESTAMP_TITLE, "Timestamp"),
        "r1": cols.find(ROUND1_TITLE, "Round one free text (prepicks)",
                        contains=["round one", "question 1"]),
        "intake": [], "call": [], "why": [],
    }
    for label, title, needles in INTAKE_TITLES:
        found["intake"].append((label, cols.find(title, "Intake placeholder: %s" % label,
                                                 contains=needles)))
    for i in range(SLOTS):
        found["call"].append(cols.find(CALL_TITLES[i], "Call C%d" % (i + 1),
                                       contains=["c%d." % (i + 1), "account"]))
        found["why"].append(cols.find(WHY_TITLES[i], "Why C%d" % (i + 1),
                                      contains=["c%d." % (i + 1), "why?"]))
    return cols, found


def tidy_cell(value):
    return re.sub(r"\s+", " ", value or "").strip()


def excerpt(text, other, width=90):
    """The stretch of text around the first place it differs from other."""
    i = 0
    while i < min(len(text), len(other)) and text[i] == other[i]:
        i += 1
    start = max(0, i - 30)
    piece = text[start:start + width]
    return ("..." if start else "") + piece + ("..." if start + width < len(text) else "")


def conflict_differences(members, labels, skip):
    """[{column, values}] for every column the records of one attempt identifier disagree on."""
    heads = list(dict.fromkeys(k for _i, row in members for k in row if k not in skip))
    out = []
    for head in heads:
        values = [tidy_cell(row.get(head)) for _i, row in members]
        if len(set(values)) > 1:
            other = next(v for v in values if v != values[0])
            out.append({"column": labels.get(head, head[:60]),
                        "values": [excerpt(v, other if k == 0 else values[0])
                                   for k, v in enumerate(values)]})
    return out


def analyze(path, roster_path=None, cases_dir=None, synthetic_check=False,
            scores_path=None, second_scores_path=None, resolutions=None):
    rows, headers = read_rows(path)
    cols, found = match_columns(headers)
    resolved_dir = find_cases_dir(cases_dir)
    library = CaseLibrary(resolved_dir)

    report = {"missing": cols.missing, "matched": cols.matched, "n_rows_raw": len(rows),
              "source": os.path.abspath(path), "cases_dir": resolved_dir,
              "synthetic_check": bool(synthetic_check)}

    # --- exclusions ------------------------------------------------------------
    excluded = {key: [] for key, _ in EXCLUSION_LABELS}
    kept = []
    for index, row in enumerate(rows, start=1):
        code = cell(row, found["code"]).strip()
        qa, qb = cell(row, found["qa"]), cell(row, found["qb"])
        why = exclusion_of(code, qa, qb, row, synthetic_check, sheet_row=index + 1)
        if why:
            excluded[why[0]].append(why[1])
            continue
        kept.append((index, row, parse_attempt(qb)[0]))

    # --- one attempt identifier on more than one row ----------------------------
    # A retry of one run posts the same attempt identifier and the same content, so rows that
    # match in every cell but the timestamp are one attempt sent twice, and the earliest is kept.
    # Rows that share an identifier and differ anywhere else are a conflict: every record is
    # reported, none enters a count or a rate, and the facilitator resolves it by naming the
    # sheet row to keep with --resolve-conflict. A row with no identifier is its own attempt.
    groups, order = {}, []
    for index, row, attempt_id in kept:
        if attempt_id:
            if attempt_id not in groups:
                groups[attempt_id] = []
                order.append(attempt_id)
            groups[attempt_id].append((index, row))
    skip = {found["ts"]} if found["ts"] else set()
    labels = {head: label for label, head in cols.matched.items()}
    pending = dict(resolutions or {})
    duplicates, conflicts, resolved, chosen = [], [], [], set()
    for attempt_id in order:
        members = groups[attempt_id]
        if len(members) == 1:
            chosen.add(members[0][0])
            continue
        contents = []
        for _index, row in members:
            content = tuple((k, tidy_cell(v)) for k, v in row.items() if k not in skip)
            if content not in contents:
                contents.append(content)
        if len(contents) == 1:
            keep = min(members, key=lambda m: (parse_timestamp(cell(m[1], found["ts"])) or
                                               datetime.datetime.max, m[0]))
            chosen.add(keep[0])
            for index, row in members:
                if index != keep[0]:
                    duplicates.append("%s (attempt %s sent again: sheet row %d repeats sheet "
                                      "row %d)" % (cell(row, found["code"]).strip(), attempt_id,
                                                   index + 1, keep[0] + 1))
            continue
        records = []
        for index, row in members:
            probe = read_attempt(index, row, found, library)
            records.append({
                "sheet_row": index + 1, "row_index": index, "codename": probe["codename"],
                "code_key": probe["code_key"], "timestamp": probe["timestamp"],
                "ts_value": probe["ts_value"], "supported": probe["supported"],
                "set": probe["set"], "refusal": probe["refusal"], "score": probe["score"],
                "lines": len(probe["case1"]["cards"]) if probe["case1"] else None,
                "fresh_calls": probe["fresh"]["calls"] if probe["fresh"] else None,
                "completed": probe["completed"],
            })
        entry = {"attempt_id": attempt_id, "records": records,
                 "differences": conflict_differences(members, labels, skip)}
        want = pending.pop(attempt_id, None)
        if want is None:
            conflicts.append(entry)
            continue
        rows_here = [r["sheet_row"] for r in records]
        if want not in rows_here:
            raise InputError("--resolve-conflict %s=%s names a sheet row that does not carry "
                             "attempt %s; its rows are %s"
                             % (attempt_id, want, attempt_id,
                                ", ".join(str(r) for r in rows_here)))
        chosen.add(want - 1)
        entry["kept_row"] = want
        resolved.append(entry)
    if pending:
        raise InputError("--resolve-conflict names %s, which %s not a conflict in this export"
                         % (", ".join(sorted(pending)), "is" if len(pending) == 1 else "are"))
    attempts = [read_attempt(index, row, found, library) for index, row, attempt_id in kept
                if not attempt_id or index in chosen]

    report["excluded"] = excluded
    report["n_excluded"] = sum(len(v) for v in excluded.values())
    report["duplicate_sends"] = duplicates
    report["conflicts"] = conflicts
    report["conflicts_resolved"] = resolved
    report["n_conflict_rows_held"] = sum(len(c["records"]) for c in conflicts)
    report["n_conflict_rows_set_aside"] = sum(len(c["records"]) - 1 for c in resolved)
    report["attempts"] = attempts
    report["n_attempts_received"] = len(attempts)
    report["n_attempts_completed"] = sum(1 for a in attempts if a["completed"])
    report["n_codenames"] = len({a["code_key"] for a in attempts})

    refused = [a for a in attempts if not a["supported"]]
    refusal_counts = {}
    for a in refused:
        refusal_counts[a["refusal"]] = refusal_counts.get(a["refusal"], 0) + 1
    report["refused"] = refused
    report["refusal_counts"] = dict(sorted(refusal_counts.items(), key=lambda kv: -kv[1]))

    # --- first attempts and reattempts ----------------------------------------
    eligible = [a for a in attempts if a["supported"]]
    if eligible and all(a["ts_value"] for a in eligible):
        eligible.sort(key=lambda a: (a["ts_value"], a["row_index"]))
        report["order_basis"] = "timestamp"
    else:
        report["order_basis"] = "file order"
    # A conflict held out of the counts still happened. A later attempt under the same codename is
    # not promoted to a first attempt over it: it counts the conflict as the earlier attempt.
    held = {}
    for c in conflicts:
        for rec in c["records"]:
            if rec["supported"]:
                held.setdefault(rec["code_key"], []).append((rec, c["attempt_id"]))

    def held_before(rec, a):
        if report["order_basis"] == "timestamp":
            if not rec["ts_value"]:
                return True
            return (rec["ts_value"], rec["row_index"]) < (a["ts_value"], a["row_index"])
        return rec["row_index"] < a["row_index"]

    counts = {}
    for a in eligible:
        counts[a["code_key"]] = counts.get(a["code_key"], 0) + 1
        prior = sorted({aid for rec, aid in held.get(a["code_key"], []) if held_before(rec, a)})
        a["after_conflict"] = prior or None
        a["attempt_number"] = counts[a["code_key"]] + len(prior)
        a["initial"] = a["attempt_number"] == 1
    initial = [a for a in eligible if a["initial"]]
    later = [a for a in eligible if not a["initial"]]
    report["initial"] = initial
    report["reattempts"] = later

    # --- roster ----------------------------------------------------------------
    if roster_path:
        roster = confirm_roster(read_roster(roster_path), attempts)
        roster["path"] = os.path.basename(roster_path)
        report["roster"] = roster
        report["n_participants_confirmed"] = roster["n_confirmed"]
    else:
        report["roster"] = None
        report["n_participants_confirmed"] = None

    # --- written explanations and the educator's scores ------------------------
    report["explanation_items"] = explanation_items(initial + later)
    report["scores"] = merge_scores(report["explanation_items"], scores_path, second_scores_path)

    # --- case sets -------------------------------------------------------------
    labels = []
    for a in initial + later:
        if a["set"] not in labels:
            labels.append(a["set"])
    sets = []
    for label in labels:
        first = [a for a in initial if a["set"] == label]
        again = [a for a in later if a["set"] == label]
        probe = (first or again)[0]
        sets.append(analyze_set(label, probe["case1"], probe["case2"], first, again, report))
    sets.sort(key=lambda s: (-s["n_attempts"], s["label"]))
    report["sets"] = sets

    # --- versions as recorded, for every received attempt ---------------------
    versions = {}
    for a in attempts:
        if a["cases"]:
            tag = "%s, dated %s" % (set_label(a["cases"]["one"], a["cases"]["two"]),
                                    a["cases"]["date"])
        else:
            tag = "no case version recorded"
        versions[tag] = versions.get(tag, 0) + 1
    report["case_versions"] = dict(sorted(versions.items(), key=lambda kv: -kv[1]))

    # --- the four intake placeholders -----------------------------------------
    intake_report = []
    for label, col in found["intake"]:
        kinds = {"not asked": 0, "placeholder": 0, "value": 0, "blank": 0}
        for a in attempts:
            kinds[a["intake"][label]] += 1
        intake_report.append({"label": label, "column": col, "kinds": kinds})
    report["intake"] = intake_report

    report["disagreements"] = [d for a in attempts for d in a["disagreements"]]

    # Names the third independent review's probe script reads. "players" is the list of
    # first attempts and "n_players" is the count of distinct codenames. Neither is a count
    # of people, and neither name is printed anywhere in the findings.
    report["players"] = initial
    report["n_players"] = report["n_codenames"]
    report["repeat_runs"] = ["%s (attempt %d, %s)" % (a["codename"], a["attempt_number"],
                                                     a["attempt_id"] or "no attempt id")
                             for a in later]
    report["dropped_test"] = [d for key, _ in EXCLUSION_LABELS for d in excluded[key]]
    return report


def read_results(cards, first):
    """The read before the draft against the final calls, for the first attempts of one set."""
    with_read = [a for a in first if a.get("read") and not a["read"]["late"]]
    per_line = []
    for i, card in enumerate(cards):
        moves = [a["read"]["moves"][i] for a in with_read if a["read"]["moves"][i] is not None]
        tapped = sum(1 for a in with_read if a["read"]["read"][i] == "flag")
        per_line.append({"n": card["n"], "acct": card["acct"], "name": card["name"],
                         "key": card["key"], "type": card["type"], "compared": len(moves),
                         "tapped": tapped, "held": moves.count("held"),
                         "toward": moves.count("toward"), "away": moves.count("away")})
    compared = sum(a["read"]["compared"] for a in with_read)
    toward = sum(a["read"]["toward"] for a in with_read)
    away = sum(a["read"]["away"] for a in with_read)
    held = sum(a["read"]["held"] for a in with_read)
    changed = toward + away
    changed_any = sum(1 for a in with_read if a["read"]["toward"] + a["read"]["away"])
    return {
        "n": len(with_read),
        "n_late": sum(1 for a in first if a.get("read") and a["read"]["late"]),
        "n_before_required": sum(1 for a in first if a["prepicks"] and
                                 not a["prepicks"]["required"]),
        "n_missing": sum(1 for a in first if not a["prepicks"]),
        "changed_any": changed_any, "changed_any_rate": pct(changed_any, len(with_read)),
        "compared": compared, "changed": changed, "changed_rate": pct(changed, compared),
        "toward": toward, "toward_rate": pct(toward, changed),
        "away": away, "away_rate": pct(away, changed), "held": held,
        "per_line": per_line,
    }


def analyze_set(label, case1, case2, first, again, report):
    """Every first-attempt rate for one case set. Reattempts are carried, never pooled."""
    cards = case1["cards"]
    n_lines = len(cards)
    s = {"label": label, "case1": case1, "case2": case2, "attempts": first,
         "reattempts": again, "n_attempts": len(first), "n_reattempts": len(again),
         "n_completed": sum(1 for a in first if a["completed"]),
         "n_lines": n_lines}
    s["dates"] = sorted({a["cases"]["date"] for a in first + again
                         if a["cases"] and a["cases"]["date"]})
    s["products"] = sorted({a["product"] for a in first + again if a["product"]})
    roster = report.get("roster")
    if roster:
        people = set()
        for a in first:
            who = roster["code_to_participant"].get(a["code_key"])
            if who and who in roster["confirmed"]:
                people.add(who)
        s["participants_confirmed"] = len(people)
    else:
        s["participants_confirmed"] = None

    per_card = []
    for i, card in enumerate(cards):
        seen = sum(1 for a in first if a["calls"][i] is not None)
        right = sum(1 for a in first if a["calls"][i] == card["key"])
        flagged = sum(1 for a in first if a["calls"][i] == "flag")
        r_scored = sum(1 for a in first if a["reasons"][i] is not None)
        r_right = sum(1 for a in first if a["reasons"][i])
        per_card.append({"n": card["n"], "acct": card["acct"], "name": card["name"],
                         "key": card["key"], "type": card["type"], "seen": seen,
                         "right": right, "flagged": flagged, "rate": pct(right, seen),
                         "reason_scored": r_scored, "reason_right": r_right,
                         "reason_rate": pct(r_right, r_scored)})
    s["per_card"] = per_card
    problem = [c for c in per_card if c["key"] == "flag"]
    clean = [c for c in per_card if c["key"] == "stand"]
    s["n_problem"], s["n_clean"] = len(problem), len(clean)
    s["catch_counts"] = (sum(c["right"] for c in problem), sum(c["seen"] for c in problem))
    s["catch_rate"] = pct(*s["catch_counts"])
    s["let_stand_counts"] = (sum(c["right"] for c in clean), sum(c["seen"] for c in clean))
    s["let_stand_rate"] = pct(*s["let_stand_counts"])
    s["false_flag_counts"] = (sum(c["flagged"] for c in clean), sum(c["seen"] for c in clean))
    s["false_flag_rate"] = pct(*s["false_flag_counts"])

    by_type = {}
    for c in per_card:
        b = by_type.setdefault(c["type"], {"seen": 0, "right": 0, "lines": [],
                                           "reason_scored": 0, "reason_right": 0})
        b["seen"] += c["seen"]
        b["right"] += c["right"]
        b["reason_scored"] += c["reason_scored"]
        b["reason_right"] += c["reason_right"]
        b["lines"].append(c["n"])
    for b in by_type.values():
        b["rate"] = pct(b["right"], b["seen"])
        b["reason_rate"] = pct(b["reason_right"], b["reason_scored"])
    s["by_type"] = by_type
    s["type_order"] = ([t for t in TYPE_ORDER if t in by_type] +
                       sorted(t for t in by_type if t not in TYPE_ORDER))

    reason_scored = sum(a["reason_scored"] for a in first)
    reason_right = sum(a["reason_right"] for a in first)
    s["reason_counts"] = (reason_right, reason_scored)
    s["reason_rate"] = pct(reason_right, reason_scored)
    s["limitations"] = [x for x in (reason_limitation(case1), reason_limitation(case2)) if x]

    # --- the basis given -------------------------------------------------------
    chips_by_type, calls_by_type, basis_by_type, chips_overall, examples = {}, {}, {}, {}, {}
    flags_total = flags_with_words = calls_total = calls_with_basis = calls_with_words = 0
    for a in first:
        for i, why in enumerate(a["whys"]):
            etype = cards[i]["type"]
            calls_by_type[etype] = calls_by_type.get(etype, 0) + 1
            calls_total += 1
            if a["calls"][i] == "flag":
                flags_total += 1
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
                if a["calls"][i] == "flag":
                    flags_with_words += 1
                examples.setdefault(etype, []).append(
                    {"codename": a["codename"], "line": cards[i]["n"], "acct": cards[i]["acct"],
                     "call": a["calls"][i], "words": why["words"]})
    s["basis"] = {
        "calls_total": calls_total, "calls_with_basis": calls_with_basis,
        "basis_rate": pct(calls_with_basis, calls_total),
        "calls_with_words": calls_with_words, "words_rate": pct(calls_with_words, calls_total),
        "flags_total": flags_total, "flags_with_words": flags_with_words,
        "flag_words_rate": pct(flags_with_words, flags_total),
        "chips_overall": dict(sorted(chips_overall.items(), key=lambda kv: -kv[1])),
        "by_type": {t: {"chips": dict(sorted(chips_by_type.get(t, {}).items(),
                                             key=lambda kv: -kv[1])),
                        "with_basis": basis_by_type.get(t, 0), "calls": calls_by_type.get(t, 0)}
                    for t in calls_by_type},
        "examples": {t: v[:3] for t, v in examples.items()},
    }

    # --- per attempt -----------------------------------------------------------
    scores = [a["score"] for a in first]
    s["mean_score"] = _mean(scores)
    s["median_score"] = _median(scores)
    covers = [a["coverage"] for a in first]
    s["coverage_mean"] = _mean(covers)
    s["coverage_full"] = sum(1 for c in covers if c == n_lines)
    minutes = [a["minutes"] for a in first if a["minutes"]]
    s["minutes_n"] = len(minutes)
    s["minutes_mean"] = _mean(minutes)
    s["minutes_median"] = _median(minutes)
    streaks = [a["best_streak"] for a in first if a["best_streak"] is not None]
    s["streak_best"] = max(streaks) if streaks else None
    s["flag_everything"] = [a["codename"] for a in first if a["flags"] == n_lines]
    ranks = {}
    for a in first:
        rank = a["posted_rank"] or "not posted"
        ranks[rank] = ranks.get(rank, 0) + 1
    s["ranks"] = ranks

    s["read"] = read_results(cards, first)

    # --- orgs ------------------------------------------------------------------
    org_counts = {}
    for a in first:
        for chip in a["orgs"]:
            org_counts[chip] = org_counts.get(chip, 0) + 1
    s["org_counts"] = dict(sorted(org_counts.items(), key=lambda kv: -kv[1]))

    # --- the fresh case --------------------------------------------------------
    if case2:
        withr2 = [a for a in first if a["fresh"]]
        fresh_rates = [100.0 * a["fresh"]["right"] / a["fresh"]["total"]
                       for a in withr2 if a["fresh"]["total"]]
        practice_rates = [100.0 * a["score"] / max(1, len(a["answered"])) for a in withr2]
        fresh_mean, practice_mean = _mean(fresh_rates), _mean(practice_rates)
        per_line = []
        letters = key_letters(case2)
        for n, card in enumerate(case2["cards"], start=1):
            seen = sum(1 for a in withr2 if len(a["fresh"]["calls"]) >= n)
            right = sum(1 for a in withr2 if len(a["fresh"]["calls"]) >= n and
                        a["fresh"]["calls"][n - 1] == letters[n - 1])
            rows = [r for a in first for r in a["r2_basis"] if r[0] == n and r[3] is not None]
            per_line.append({"n": n, "name": card["name"], "key": card["key"],
                             "type": card["type"], "seen": seen, "right": right,
                             "rate": pct(right, seen), "reason_scored": len(rows),
                             "reason_right": sum(1 for r in rows if r[3]),
                             "reason_rate": pct(sum(1 for r in rows if r[3]), len(rows))})
        reason_means = []
        for a in first:
            scored = [r for r in a["r2_basis"] if r[3] is not None]
            if scored:
                reason_means.append(100.0 * sum(1 for r in scored if r[3]) / len(scored))
        r2_chips, r2_with_basis, r2_lines = {}, 0, 0
        for a in first:
            for n, chips, _words, _reason in a["r2_basis"]:
                if not 1 <= n <= len(case2["cards"]):
                    continue
                etype = case2["cards"][n - 1]["type"]
                r2_lines += 1
                if chips:
                    r2_with_basis += 1
                    bucket = r2_chips.setdefault(etype, {})
                    for chip in chips:
                        bucket[chip] = bucket.get(chip, 0) + 1
        s["fresh"] = {
            "n": len(withr2), "lines": len(case2["cards"]),
            "call_mean": fresh_mean, "practice_mean": practice_mean,
            "difference": (fresh_mean - practice_mean)
                          if (fresh_mean is not None and practice_mean is not None) else None,
            "right": sum(a["fresh"]["right"] for a in withr2),
            "total": sum(a["fresh"]["total"] for a in withr2),
            "seconds_median": _median([a["fresh"]["seconds"] for a in withr2]),
            "reason_mean": _mean(reason_means), "per_line": per_line,
            "basis_by_type": {t: dict(sorted(v.items(), key=lambda kv: -kv[1]))
                              for t, v in r2_chips.items()},
            "basis_lines": r2_lines, "basis_with_chips": r2_with_basis,
        }
    else:
        s["fresh"] = None

    profs = [a for a in first if any("professor" in norm(c) for c in a["orgs"])]
    if profs:
        p_seen = sum(1 for a in profs for i in range(n_lines)
                     if a["calls"][i] is not None and cards[i]["key"] == "flag")
        p_caught = sum(1 for a in profs for i in range(n_lines)
                       if a["calls"][i] == "flag" and cards[i]["key"] == "flag")
        s["professors"] = {"n": len(profs), "codenames": [a["codename"] for a in profs],
                           "mean_score": _mean([a["score"] for a in profs]),
                           "catch_rate": pct(p_caught, p_seen)}
    else:
        s["professors"] = None
    s["explain"] = explanation_results(case2, first, report) if case2 else None
    s["disagreements"] = [d for a in first + again for d in a["disagreements"]]
    return s


# ------------------------------------------------- the explanation scoring sheet
# The sheet an educator fills is blind to the machine: it carries the memo sentence, the
# participant's own call and the three written parts, and never the key, the call result, the
# chips, the chip agreement or the codename. Those ride in a separate facilitator key joined on
# response_id. Rows are ordered by fresh line, so one item is scored across every response
# before the next, and by a hash of response_id inside a line, so one attempt's answers are
# not read in a row. RUBRIC.md is the scoring guide and describes the second scorer's draw.
SHEET_COLUMNS = ["response_id", "case_version", "line", "account", "memo_sentence",
                 "participant_call", "decisive_evidence", "why_it_matters_for_this_period",
                 "action_or_source_request", "below_minimum", "second_scorer", "score_evidence",
                 "score_period", "score_action", "scorer", "key_disagreement", "notes"]
# the columns that hold numbers, written as numbers; every other cell is text and is neutralized
SHEET_NUMERIC = frozenset(["line", "score_evidence", "score_period", "score_action"])
KEY_NUMERIC = frozenset(["line"])
SHEET_TEXT = {"evidence": "decisive_evidence", "period": "why_it_matters_for_this_period",
              "action": "action_or_source_request"}
SHEET_SCORE = {"evidence": "score_evidence", "period": "score_period",
               "action": "score_action"}
KEY_COLUMNS = ["response_id", "codename", "attempt_id", "attempt", "timestamp", "case_set",
               "case_version", "line", "participant_call", "keyed_call", "call_result",
               "reason_chips", "reason_chip_agreement", "second_scorer"]
SECOND_SCORER_SEED = "second-pass-rubric-v1"
SECOND_SCORER_MODULUS = 5          # one response in five, by hash
SECOND_SCORER_MIN_PER_LINE = 2     # topped up by lowest hash on every fresh line


def _hash(text):
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def explanation_items(attempts):
    """One item per fresh line of every eligible attempt that carries any written text.

    A line whose parts are all blank (not posted, empty, or the page's "none") has nothing to
    score and is listed with the explanation gaps instead. A line with any text goes on the sheet
    with every part as posted, and below_minimum names each part that falls short, so an answer
    the minimum refuses is scored and seen rather than dropped."""
    items = []
    for a in attempts:
        if not a["case2"] or not a["explanations"]:
            continue
        case2 = a["case2"]
        identity = a["attempt_id"] or "%s|%s|row %d" % (a["codename"], a["timestamp"],
                                                        a["row_index"])
        for n, parts in sorted(a["explanations"].items()):
            if all(explanation_blank(parts.get(key)) for key, _l, _r, _c in EXPLANATION_PARTS):
                continue
            card = case2["cards"][n - 1]
            call = a["fresh"]["calls"][n - 1] if (a["fresh"] and len(a["fresh"]["calls"]) >= n) \
                else None
            call = {"F": "flag", "S": "stand"}.get(call)
            basis = [r for r in a["r2_basis"] if r[0] == n]
            rid = "R" + _hash("%s|%s|%d" % (identity, case2["version"], n))[:10].upper()
            items.append({
                "response_id": rid, "attempt": a, "line": n, "card": card,
                "case_version": case2["version"], "parts": parts, "call": call,
                "below_minimum": part_problems(parts),
                "call_result": (None if call is None else
                                "agrees with key" if call == card["key"] else
                                "does not agree with key"),
                "chips": basis[0][1] if basis else [],
                "chip_agreement": basis[0][3] if basis else None,
                "draw": int(_hash(SECOND_SCORER_SEED + "|" + rid), 16),
                "second": False, "first_scores": None, "second_scores": None,
            })
    by_line = {}
    for item in items:
        item["second"] = item["draw"] % SECOND_SCORER_MODULUS == 0
        by_line.setdefault((item["case_version"], item["line"]), []).append(item)
    for group in by_line.values():
        chosen = sum(1 for i in group if i["second"])
        for item in sorted(group, key=lambda i: i["draw"]):
            if chosen >= min(SECOND_SCORER_MIN_PER_LINE, len(group)):
                break
            if not item["second"]:
                item["second"] = True
                chosen += 1
    items.sort(key=lambda i: (i["case_version"], i["line"], i["draw"]))
    return items


def below_minimum_text(problems):
    """"period: a stock non-answer; action: not posted", or "" when every part meets it."""
    names = {key: SHEET_TEXT[key].replace("_", " ") for key in SHEET_TEXT}
    return "; ".join("%s: %s" % (names[key], EXPLAIN_PROBLEM_LABEL[problem])
                     for key, problem in problems)


def write_scoring_sheet(report, sheet_path, key_path):
    """The blind sheet and the facilitator key, as CSV that is safe to open in a spreadsheet.

    Every cell passes through sheet_cell(): text that a spreadsheet would run as a formula (a
    participant answer or a codename beginning =, +, -, @, a tab or a line break, or their
    full-width forms) is written with a leading apostrophe, and the numeric columns keep their
    numbers as numbers."""
    import csv
    items = report["explanation_items"]
    with open(sheet_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(SHEET_COLUMNS)
        for i in items:
            card = i["card"]
            row = {"response_id": i["response_id"], "case_version": i["case_version"],
                   "line": i["line"], "account": "%s %s" % (card["acct"], card["name"]),
                   "memo_sentence": card.get("memo", ""),
                   "participant_call": {"flag": "flag", "stand": "let it stand"}.get(i["call"],
                                                                                    "not recorded"),
                   "below_minimum": below_minimum_text(i["below_minimum"]),
                   "second_scorer": "yes" if i["second"] else ""}
            for key, column in SHEET_TEXT.items():
                row[column] = i["parts"].get(key, "")
            writer.writerow([sheet_cell(row.get(c, ""), numeric=c in SHEET_NUMERIC)
                             for c in SHEET_COLUMNS])
    with open(key_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(KEY_COLUMNS)
        for i in items:
            a = i["attempt"]
            values = [i["response_id"], a["codename"], a["attempt_id"] or "",
                      "first" if a["initial"] else "reattempt %d" % a["attempt_number"],
                      a["timestamp"], a["set"], i["case_version"], i["line"],
                      i["call"] or "not recorded", i["card"]["key"],
                      i["call_result"] or "not recorded", "; ".join(i["chips"]),
                      {True: "agrees", False: "does not agree"}.get(i["chip_agreement"],
                                                                    "not scored"),
                      "yes" if i["second"] else ""]
            writer.writerow([sheet_cell(v, numeric=c in KEY_NUMERIC)
                             for c, v in zip(KEY_COLUMNS, values)])
    return len(items)


def read_score_sheet(path):
    """{response_id: {"scores": {part: 0|1|2} or None, "scorer", "key_disagreement", ...}}."""
    rows, headers = read_rows(path)
    lookup = {norm(h): h for h in headers}
    needed = ["response_id"] + list(SHEET_SCORE.values())
    absent = [c for c in needed if c not in lookup]
    if absent:
        raise InputError("The scored sheet at %s lacks %s" % (path, ", ".join(absent)))
    out = {}
    for r in rows:
        rid = cell(r, lookup["response_id"]).strip()
        if not rid:
            continue
        scores, invalid = {}, False
        for key, column in SHEET_SCORE.items():
            # a spreadsheet can hand a typed score back with the apostrophe that marks it as text
            raw = cell(r, lookup[column]).strip().lstrip("'").strip()
            if raw in ("0", "1", "2"):
                scores[key] = int(raw)
            elif raw:
                invalid = True
        out[rid] = {"scores": scores if (len(scores) == len(SHEET_SCORE) and not invalid) else None,
                    "invalid": invalid,
                    "scorer": cell(r, lookup.get("scorer")).strip(),
                    "key_disagreement": cell(r, lookup.get("key_disagreement")).strip(),
                    "notes": cell(r, lookup.get("notes")).strip()}
    return out


def merge_scores(items, first_path, second_path):
    """Attach the first and second scorer's rows to the exported items by response_id."""
    status = {"first_path": os.path.basename(first_path) if first_path else None,
              "second_path": os.path.basename(second_path) if second_path else None,
              "unknown_ids": 0, "invalid_rows": 0, "key_disagreements": []}
    by_id = {i["response_id"]: i for i in items}
    for which, path in (("first_scores", first_path), ("second_scores", second_path)):
        if not path:
            continue
        for rid, got in read_score_sheet(path).items():
            item = by_id.get(rid)
            if not item:
                status["unknown_ids"] += 1
                continue
            if got["invalid"]:
                status["invalid_rows"] += 1
            item[which] = got
            if got["key_disagreement"]:
                status["key_disagreements"].append(
                    {"item": item, "scorer": got["scorer"] or which.split("_")[0] + " scorer",
                     "text": got["key_disagreement"]})
    return status


def explanation_results(case2, first, report):
    """Educator-scored explanation results for one case set's first attempts."""
    ids = {id(a) for a in first}
    items = [i for i in report["explanation_items"] if id(i["attempt"]) in ids]
    fresh_calls = sum(len(a["fresh"]["calls"]) for a in first if a["fresh"])
    scored = [i for i in items if i["first_scores"] and i["first_scores"]["scores"]]
    res = {"version": case2["version"], "items": len(items),
           "fresh_calls": fresh_calls, "without_text": max(0, fresh_calls - len(items)),
           "second_drawn": sum(1 for i in items if i["second"]),
           "scored": len(scored), "sheet_supplied": bool(report["scores"]["first_path"])}
    for key, _label, _record, _criterion in EXPLANATION_PARTS:
        res[key + "_avg"] = _mean([float(i["first_scores"]["scores"][key]) for i in scored])
    res["total_avg"] = _mean([float(sum(i["first_scores"]["scores"].values())) for i in scored])
    res["distribution"] = {key: {v: sum(1 for i in scored
                                         if i["first_scores"]["scores"][key] == v)
                                 for v in (0, 1, 2)}
                           for key, _l, _r, _c in EXPLANATION_PARTS}
    per_line = []
    for n, card in enumerate(case2["cards"], start=1):
        line_items = [i for i in scored if i["line"] == n]
        per_line.append({"n": n, "name": card["name"], "scored": len(line_items),
                         "total_avg": _mean([float(sum(i["first_scores"]["scores"].values()))
                                             for i in line_items])})
    res["per_line"] = per_line
    double = [i for i in scored if i["second_scores"] and i["second_scores"]["scores"]]
    res["double_scored"] = len(double)
    pairs = [(i["first_scores"]["scores"][k], i["second_scores"]["scores"][k])
             for i in double for k, _l, _r, _c in EXPLANATION_PARTS]
    res["exact_rate"] = pct(sum(1 for x, y in pairs if x == y), len(pairs))
    res["within_one_rate"] = pct(sum(1 for x, y in pairs if abs(x - y) <= 1), len(pairs))
    res["key_disagreements"] = [d for d in report["scores"]["key_disagreements"]
                                if id(d["item"]["attempt"]) in ids]
    # the parts that fall short of the minimum, kept visible and counted as incomplete
    res["required"] = explanation_required(case2)
    res["below_minimum_items"] = sum(1 for i in items if i["below_minimum"])
    res["gaps"] = [dict(g, codename=a["codename"], attempt_id=a["attempt_id"])
                   for a in first for g in a["explanation_gaps"]]
    res["first_attempts_with_gaps"] = sum(1 for a in first if a["explanation_gaps"])
    res["parts_below_minimum"] = len(res["gaps"])
    return res


# ------------------------------------------------- the readout's field contract
def run_fields(report, csv_path):
    out = []

    def add(name, value):
        out.append((name, value))

    products = sorted({a["product"] for a in report["attempts"] if a["product"]})
    add("run.generated", datetime.date.today().isoformat())
    add("run.source_file", os.path.basename(csv_path))
    add("run.evidence_status", "synthetic verification run, not participant evidence"
        if report["synthetic_check"] else "participant export")
    add("run.product_version", "; ".join(products) if products else None)
    add("run.rows_in_export", report["n_rows_raw"])
    add("run.rows_excluded", report["n_excluded"])
    for key, _label in EXCLUSION_LABELS:
        add("run.rows_excluded.%s" % key, len(report["excluded"][key]))
    add("run.duplicate_sends_set_aside", len(report["duplicate_sends"]))
    add("run.attempt_conflicts_unresolved", len(report["conflicts"]))
    add("run.attempt_conflict_rows_held_out", report["n_conflict_rows_held"])
    add("run.attempt_conflicts_resolved", len(report["conflicts_resolved"]))
    add("run.attempts_received", report["n_attempts_received"])
    add("run.attempts_completed", report["n_attempts_completed"])
    add("run.attempts_refused", len(report["refused"]))
    add("run.codenames_distinct", report["n_codenames"])
    add("run.participants_confirmed", report["n_participants_confirmed"])
    add("run.first_attempts", len(report["initial"]))
    add("run.reattempts", len(report["reattempts"]))
    add("run.case_sets", "; ".join("%s (%d first, %d later)"
                                   % (s["label"], s["n_attempts"], s["n_reattempts"])
                                   for s in report["sets"]) or None)
    return out


def set_fields(s):
    """Every per case set field READOUT-TEMPLATE.md names, as an ordered list."""
    out = []
    first = s["attempts"]
    cards = s["case1"]["cards"]

    def add(name, value):
        out.append((name, value))

    add("set.case_round1", s["case1"]["version"])
    add("set.case_round2", s["case2"]["version"] if s["case2"] else None)
    add("set.key_date", "; ".join(s["dates"]) if s["dates"] else s["case1"]["date"])
    add("set.first_attempts", s["n_attempts"])
    add("set.first_attempts_completed", s["n_completed"])
    add("set.codenames", len({a["code_key"] for a in first}))
    add("set.participants_confirmed", s["participants_confirmed"])
    add("set.reattempts", s["n_reattempts"])

    for name in ORG_ORDER:
        members = [a for a in first if any(norm(c) == norm(name) for c in a["orgs"])]
        key = "org." + name.lower().replace(" ", "-")
        add(key + ".name", name)
        add(key + ".first_attempts", len(members))
        add(key + ".call_agreement_mean",
            _mean([100.0 * a["score"] / len(a["answered"]) for a in members if a["answered"]]))
        add(key + ".reason_agreement_mean",
            _mean([100.0 * a["reason_right"] / a["reason_scored"]
                   for a in members if a["reason_scored"]]))

    for etype in s["type_order"]:
        b = s["by_type"][etype]
        key = "type." + etype.replace(" ", "-")
        add(key + ".name", TYPE_LABEL.get(etype, etype.capitalize()))
        add(key + ".lines", ", ".join(str(x) for x in b["lines"]))
        add(key + ".calls_seen", b["seen"])
        add(key + ".call_agreement_rate", b["rate"])
        add(key + ".reason_agreement_rate", b["reason_rate"])

    clean = [c for c in s["per_card"] if c["key"] == "stand"]
    add("falseflag.lines", ", ".join(str(c["n"]) for c in clean))
    for c in clean:
        add("falseflag.line%d.flags" % c["n"], c["flagged"])
        add("falseflag.line%d.rate" % c["n"], pct(c["flagged"], c["seen"]))
    add("falseflag.flags", s["false_flag_counts"][0])
    add("falseflag.overall_rate", s["false_flag_rate"])
    clean_idx = [i for i, c in enumerate(cards) if c["key"] == "stand"]
    add("falseflag.first_attempts_with_none",
        sum(1 for a in first if not any(a["calls"][i] == "flag" for i in clean_idx)))

    f = s["fresh"]
    if f:
        for line in f["per_line"]:
            key = "fresh.line%d" % line["n"]
            add(key + ".name", line["name"])
            add(key + ".key", line["key"].capitalize())
            add(key + ".calls_seen", line["seen"])
            add(key + ".call_agreement_rate", line["rate"])
            add(key + ".reason_agreement_rate", line["reason_rate"])
        add("fresh.first_attempts", f["n"])
        add("fresh.call_agreement_mean", f["call_mean"])
        add("fresh.reason_agreement_mean", f["reason_mean"])
        add("fresh.seconds_median", f["seconds_median"])

    add("r1.call_agreement_mean",
        _mean([100.0 * a["score"] / len(a["answered"]) for a in first if a["answered"]]))
    add("r1.reason_agreement_mean",
        _mean([100.0 * a["reason_right"] / a["reason_scored"] for a in first
               if a["reason_scored"]]))
    add("r1.lap_median", _median([a["minutes"] for a in first]))
    add("reason.limitation", " ".join(x["text"] for x in s["limitations"]) or None)

    r = s["read"]
    add("prepick.first_attempts_with_read", r["n"])
    add("prepick.first_attempts_changed_any", r["changed_any"] if r["n"] else None)
    add("prepick.first_attempts_changed_any_rate", r["changed_any_rate"])
    add("prepick.lines_compared", r["compared"] if r["n"] else None)
    add("prepick.lines_changed", r["changed"] if r["n"] else None)
    add("prepick.lines_changed_rate", r["changed_rate"])
    add("prepick.changed_toward_key", r["toward"] if r["n"] else None)
    add("prepick.changed_toward_key_rate", r["toward_rate"])
    add("prepick.changed_away_from_key", r["away"] if r["n"] else None)
    add("prepick.changed_away_from_key_rate", r["away_rate"])
    add("prepick.lines_held", r["held"] if r["n"] else None)
    add("prepick.first_attempts_before_required", r["n_before_required"])
    add("prepick.first_attempts_read_after_a_call", r["n_late"])

    e = s.get("explain")
    if e:
        add("explain.case_version", e["version"])
        add("explain.items_with_text", e["items"])
        add("explain.fresh_calls_without_text", e["without_text"])
        add("explain.items_below_minimum", e["below_minimum_items"])
        add("explain.first_attempts_below_minimum", e["first_attempts_with_gaps"])
        add("explain.parts_below_minimum", e["parts_below_minimum"])
        add("explain.items_scored", e["scored"])
        for key, _label, _record, _criterion in EXPLANATION_PARTS:
            add("explain.%s_avg_of_2" % key, e[key + "_avg"])
        add("explain.total_avg_of_6", e["total_avg"])
        add("explain.second_scorer_drawn", e["second_drawn"])
        add("explain.double_scored", e["double_scored"])
        add("explain.second_exact_agreement_rate", e["exact_rate"])
        add("explain.second_within_one_rate", e["within_one_rate"])
        add("explain.key_disagreements_recorded", len(e["key_disagreements"]))

    quotes = []
    for a in first:
        for i, why in enumerate(a["whys"]):
            if why and why["words"] and a["reasons"][i]:
                quotes.append({"words.codename": a["codename"], "words.line": cards[i]["n"],
                               "words.type": TYPE_LABEL.get(cards[i]["type"], cards[i]["type"]),
                               "words.text": why["words"]})
    add("words.rows", quotes)
    return out


def readout_fields(report, csv_path):
    """{"run": [(name, value)], "sets": [(label, [(name, value)])]}."""
    return {"run": run_fields(report, csv_path),
            "sets": [(s["label"], set_fields(s)) for s in report["sets"]]}


def fields_json(fields):
    return {"run": dict(fields["run"]),
            "case_sets": {label: dict(values) for label, values in fields["sets"]}}


PERCENT_FIELDS = ("_rate", ".rate", "_mean")


def fmt_field(value, name=""):
    """A percentage only where the field is one. Seconds and minutes are not rates."""
    if value is None:
        return "not available"
    if isinstance(value, float):
        if any(name.endswith(tail) for tail in PERCENT_FIELDS):
            return "%.1f%%" % value
        return ("%.1f" % value).rstrip("0").rstrip(".")
    if isinstance(value, list):
        return "%d row%s" % (len(value), "" if len(value) == 1 else "s")
    return str(value)


def fields_block(fields, missing):
    lines = ["## Readout fields", "",
             "Every name READOUT-TEMPLATE.md prints in a cell, with the value to copy into it. "
             "The `run.` fields fill the header once. Every other field belongs to one case "
             "set, so a readout is filled from one block below and never from two. A field "
             "reading *not available* stays blank on the readout rather than being estimated.",
             "", "### Run", "", "| Field | Value |", "| --- | --- |"]
    for name, value in fields["run"]:
        lines.append("| `%s` | %s |" % (name, fmt_field(value, name)))
    for label, values in fields["sets"]:
        lines += ["", "### Case set %s" % label, "", "| Field | Value |", "| --- | --- |"]
        for name, value in values:
            if name == "words.rows":
                continue
            lines.append("| `%s` | %s |" % (name, fmt_field(value, name)))
        quotes = dict(values).get("words.rows") or []
        lines += ["", "`words.` rows for %s, lines in the player's own words where the "
                      "reason chips agreed with the key" % label, "",
                  "| `words.codename` | `words.line` | `words.type` | `words.text` |",
                  "| --- | --- | --- | --- |"]
        if quotes:
            for q in quotes[:12]:
                lines.append("| %s | %d | %s | %s |" % (q["words.codename"], q["words.line"],
                                                        q["words.type"], q["words.text"]))
        else:
            lines.append("| none | | | |")
    if missing:
        lines += ["", "### Columns not found", ""]
        lines += ["- " + m for m in missing]
        lines += ["", "Every cell that needed one of these stays blank on the readout."]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- the sentences
def as_percent(value):
    if value is None:
        return "an unknown share"
    return "%d percent" % round(value)


def write_sentences(s, report):
    """Paste sentences for one case set, under sixty words together. No em dashes."""
    n = s["n_attempts"]
    version = s["case1"]["version"]
    confirmed = s["participants_confirmed"]
    who = "%s first attempt%s on %s" % (say(n), "" if n == 1 else "s", version)
    if confirmed:
        who += (", one by a confirmed participant" if confirmed == 1 else
                ", %s by confirmed participants" % say(confirmed))
    catch = as_percent(s["catch_rate"])
    minutes = s["minutes_median"]
    bad = [(t, b) for t, b in s["by_type"].items() if t != "clean line" and b["seen"]]
    bad.sort(key=lambda kv: (kv[1]["rate"], kv[0]))
    worst = bad[0] if bad else None
    best = bad[-1] if bad else None

    if minutes:
        s1 = ("Across %s, reviewers caught %s of the %s planted problems, in a median of %g "
              "minutes elapsed on the page." % (who, catch, say(s["n_problem"]), round(minutes)))
    else:
        s1 = ("Across %s, reviewers caught %s of the %s planted problems."
              % (who, catch, say(s["n_problem"])))
    if worst and best and worst[0] != best[0]:
        s2 = ("They caught the %s line %s of the time and the %s line only %s."
              % (best[0], as_percent(best[1]["rate"]), worst[0], as_percent(worst[1]["rate"])))
    elif worst:
        s2 = "The %s line was caught %s of the time." % (worst[0], as_percent(worst[1]["rate"]))
    else:
        s2 = "No rate by error type could be computed from this export."
    s3 = ("False flags on the %s clean lines ran %s."
          % (say(s["n_clean"]), as_percent(s["false_flag_rate"])))
    sentences = [s1, s2, s3]
    f = s["fresh"]
    if f and f["call_mean"] is not None:
        sentences.append("On %s lines of a company nobody had seen, calls agreed with the key "
                         "%s of the time (n=%d)."
                         % (say(f["lines"]), as_percent(f["call_mean"]), f["n"]))
        if sum(len(x.split()) for x in sentences) > 60 and minutes:
            sentences[0] = ("Across %s, reviewers caught %s of the %s planted problems."
                            % (who, catch, say(s["n_problem"])))
        if sum(len(x.split()) for x in sentences) > 60 and worst and best and worst[0] != best[0]:
            sentences[1] = ("The %s line was caught %s, the %s line only %s."
                            % (best[0], as_percent(best[1]["rate"]), worst[0],
                               as_percent(worst[1]["rate"])))
        if sum(len(x.split()) for x in sentences) > 60:
            sentences[3] = ("On a company nobody had seen, calls agreed with the key %s of the "
                            "time (n=%d)." % (as_percent(f["call_mean"]), f["n"]))
        if sum(len(x.split()) for x in sentences) > 60:
            sentences[0] = ("Across %s first attempt%s on %s, reviewers caught %s of the %s "
                            "planted problems." % (say(n), "" if n == 1 else "s", version,
                                                   catch, say(s["n_problem"])))
    video = ("Across %s, reviewers caught %s of the planted problems and false flagged clean "
             "lines %s of the time." % (who, catch, as_percent(s["false_flag_rate"])))
    if f and f["call_mean"] is not None:
        video = ("Across %s, reviewers caught %s of the planted problems, and on a company they "
                 "had never seen their calls agreed with the key %s of the time."
                 % (who, catch, as_percent(f["call_mean"])))
    words = sum(len(x.split()) for x in sentences)
    return sentences, words, video


def reason_sentence(s):
    """The reason chip result, stated as agreement and nothing more."""
    b = s["basis"]
    if not b["calls_with_basis"] or s["reason_rate"] is None:
        return ""
    return ("A basis chip was tapped on %s of the calls, and the chips agreed with the key's "
            "accepted reason categories on %s of the lines scored, which is agreement with "
            "those categories rather than a measure of reasoning."
            % (as_percent(b["basis_rate"]), as_percent(s["reason_rate"])))


# ---------------------------------------------------------------- output
def count_rows(report):
    """The run level counts, each with the definition READOUT-TEMPLATE.md uses."""
    roster = report["roster"]
    confirmed = (str(report["n_participants_confirmed"]) if roster else
                 "not available, no roster supplied")
    return [
        ("Rows in the export", str(report["n_rows_raw"]),
         "Every data row in the file."),
        ("Rows excluded from participant evidence", str(report["n_excluded"]),
         "Test codenames, rows the page marked as a test attempt, blank codenames and "
         "synthetic rows, itemized below."),
        ("Duplicate sends set aside", str(len(report["duplicate_sends"])),
         "A row repeating another row's attempt identifier and every cell but the timestamp. "
         "One attempt sent twice counts once, at its earliest timestamp."),
        ("Attempt conflicts held out", "%d (%d rows)" % (len(report["conflicts"]),
                                                         report["n_conflict_rows_held"]),
         "Attempt identifiers carried by rows that differ in content. Every record is listed "
         "below, and none enters a count or a rate until the facilitator keeps one with "
         "--resolve-conflict."),
        ("Received attempts", str(report["n_attempts_received"]),
         "Rows left after those steps. Each is one run of the drill."),
        ("Completed attempts", str(report["n_attempts_completed"]),
         "Received attempts with a call on every practice line and, where a fresh case is "
         "named, on every fresh line. On a fresh case that asks for written explanations "
         "(brightwater-v6 on), all three parts on every fresh line must also meet the minimum: "
         "%s." % EXPLAIN_RULE),
        ("Distinct codenames", str(report["n_codenames"]),
         "Different codenames among received attempts. A codename is a pseudonym, so this is "
         "not a count of people: one person can type two, and two people can type one."),
        ("Facilitator-confirmed participants", confirmed,
         "Distinct participants on the consented roster the facilitator supplied, each with at "
         "least one received attempt."),
        ("First attempts scored", str(len(report["initial"])),
         "The first eligible attempt per codename, by %s. Every rate in a case set block "
         "reads these." % report["order_basis"]),
        ("Reattempts", str(len(report["reattempts"])),
         "Later eligible attempts by a codename already counted. Listed in the reattempt "
         "table and in no rate."),
        ("Attempts refused from scoring", str(len(report["refused"])),
         "Received attempts on a case version this script cannot score, itemized below."),
    ]


def build_gap_markdown(e, out):
    """The written parts below the minimum, as posted, so none is dropped without a trace."""
    if not e["gaps"]:
        if e["required"] and e["items"]:
            out.append("Every written part on these first attempts meets the minimum the page "
                       "applies before a call locks: %s." % EXPLAIN_RULE)
            out.append("")
        return
    out.append("**Written answers below the minimum.** %s first attempt%s on %s carr%s %s "
               "written part%s that fall%s short of the minimum the page applies before a call "
               "locks: %s. %s A line with any text stays on the scoring sheet with the part "
               "named in `below_minimum`, and every part is listed here as posted."
               % (say(e["first_attempts_with_gaps"]).capitalize(),
                  "" if e["first_attempts_with_gaps"] == 1 else "s", e["version"],
                  "ies" if e["first_attempts_with_gaps"] == 1 else "y",
                  say(e["parts_below_minimum"]), "" if e["parts_below_minimum"] == 1 else "s",
                  "s" if e["parts_below_minimum"] == 1 else "", EXPLAIN_RULE,
                  "That attempt counts as incomplete." if e["first_attempts_with_gaps"] == 1
                  else "Each of those attempts counts as incomplete."))
    out.append("")
    out.append("| Codename | Attempt | Fresh line | Part | As posted | What falls short |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    names = {key: criterion for key, _l, _r, criterion in EXPLANATION_PARTS}
    for g in e["gaps"]:
        posted = "(not posted)" if g["text"] is None else \
            ('"%s"' % md_cell(g["text"]) if g["text"] else '""')
        out.append("| %s | %s | %d | %s | %s | %s |"
                   % (md_cell(g["codename"]), g["attempt_id"] or "no attempt id", g["line"],
                      names[g["part"]], posted, EXPLAIN_PROBLEM_LABEL[g["problem"]]))
    out.append("")


def md_cell(text):
    """Text safe inside a markdown table cell."""
    return str(text).replace("|", "/").replace("\n", " ")


def build_explanation_markdown(e, s, report, out):
    out.append("### Educator-scored explanations")
    out.append("")
    out.append("A separate result from reason chip agreement. Each written explanation on a "
               "fresh line is for an independent educator to score against RUBRIC.md, three "
               "criteria at 0 to 2 each, and never this script. No score appears below until a "
               "filled sheet is read back with --scores. The machine's call result and the chips "
               "are kept off the sheet the educator scores.")
    out.append("")
    if not e["items"]:
        if e["required"]:
            out.append("No written explanation text was found on the %s fresh calls of these "
                       "first attempts on %s, which asks for one on every call."
                       % (e["fresh_calls"], e["version"]))
        else:
            out.append("No written explanation was found on the %s fresh calls of these first "
                       "attempts on %s. Fresh cases before brightwater-v6 did not ask for one."
                       % (e["fresh_calls"], e["version"]))
        out.append("")
        build_gap_markdown(e, out)
        return
    out.append("| Measure | Value |")
    out.append("| --- | --- |")
    out.append("| Fresh lines carrying a written explanation | %d |" % e["items"])
    out.append("| Fresh calls with no explanation text | %d |" % e["without_text"])
    out.append("| Lines on the sheet with a part below the minimum | %d |" % e["below_minimum_items"])
    out.append("| First attempts with a part below the minimum, counted incomplete | %d |"
               % e["first_attempts_with_gaps"])
    out.append("| Drawn for the second scorer | %d |" % e["second_drawn"])
    if not e["sheet_supplied"]:
        out.append("")
        out.append("Not scored yet. Write the sheet with --scoring-sheet, have the educator fill "
                   "it, and run again with --scores.")
        out.append("")
        build_gap_markdown(e, out)
        return
    out.append("| Scored by the first scorer | %d |" % e["scored"])
    for key, _label, _record, criterion in EXPLANATION_PARTS:
        avg = e[key + "_avg"]
        dist = e["distribution"][key]
        out.append("| %s, mean of 2 | %s (0: %d, 1: %d, 2: %d) |"
                   % (criterion, "%.2f" % avg if avg is not None else "n/a",
                      dist[0], dist[1], dist[2]))
    out.append("| Total, mean of 6 | %s |"
               % ("%.2f" % e["total_avg"] if e["total_avg"] is not None else "n/a"))
    out.append("| Scored by both scorers | %d |" % e["double_scored"])
    out.append("| Criterion scores the two scorers gave identically | %s |"
               % fmt_pct(e["exact_rate"], 1))
    out.append("| Criterion scores within one point | %s |" % fmt_pct(e["within_one_rate"], 1))
    out.append("| Key disagreements the scorers recorded | %d |" % len(e["key_disagreements"]))
    out.append("")
    out.append("| Fresh line | Scored | Total, mean of 6 |")
    out.append("| --- | --- | --- |")
    for line in e["per_line"]:
        out.append("| %d %s | %d | %s |" % (line["n"], line["name"], line["scored"],
                                          "%.2f" % line["total_avg"]
                                          if line["total_avg"] is not None else "n/a"))
    out.append("")
    if e["key_disagreements"]:
        out.append("Recorded key disagreements, kept as written. The key was not changed to fit "
                   "them; RUBRIC.md says how they are reviewed.")
        out.append("")
        for d in e["key_disagreements"]:
            out.append("- Line %d, %s, %s: %s" % (d["item"]["line"], d["item"]["response_id"],
                                                  d["scorer"], d["text"]))
        out.append("")
    status = report["scores"]
    if status["unknown_ids"] or status["invalid_rows"]:
        out.append("The scored sheets carried %d response id%s this export does not hold and %d "
                   "row%s with a score outside 0, 1 or 2, which are left unscored."
                   % (status["unknown_ids"], "" if status["unknown_ids"] == 1 else "s",
                      status["invalid_rows"], "" if status["invalid_rows"] == 1 else "s"))
        out.append("")
    out.append("With %s items and no comparable baseline, these scores describe the "
               "explanations written on one unseen set and do not establish learning gain."
               % say(len(s["case2"]["cards"])))
    out.append("")
    build_gap_markdown(e, out)


def build_read_markdown(s, out):
    r = s["read"]
    out.append("### The read before the draft, against the final calls")
    out.append("")
    out.append(PREPICK_NOTE)
    out.append("")
    apart = []
    if r["n_before_required"]:
        apart.append("%s posted before the read was required" % say(r["n_before_required"]))
    if r["n_late"]:
        apart.append("%s locked in after a call" % say(r["n_late"]))
    if r["n_missing"]:
        apart.append("%s with no read in the round one question" % say(r["n_missing"]))
    if not r["n"]:
        out.append("No first attempt on this case set carries the required read, so nothing is "
                   "compared%s." % ((". First attempts left out: " + "; ".join(apart)) if apart
                                    else ""))
        out.append("")
        return
    out.append("| Measure | Value |")
    out.append("| --- | --- |")
    out.append("| First attempts with the required read | %d of %d |" % (r["n"], s["n_attempts"]))
    out.append("| First attempts whose final calls moved off the read on at least one line | "
               "%s (%d of %d) |" % (fmt_pct(r["changed_any_rate"], 1), r["changed_any"], r["n"]))
    out.append("| Lines where the final call moved off the read | %s (%d of %d lines compared) |"
               % (fmt_pct(r["changed_rate"], 1), r["changed"], r["compared"]))
    out.append("| Of those, changed toward the key | %s (%d of %d) |"
               % (fmt_pct(r["toward_rate"], 1), r["toward"], r["changed"]))
    out.append("| Of those, changed away from the key | %s (%d of %d) |"
               % (fmt_pct(r["away_rate"], 1), r["away"], r["changed"]))
    out.append("| Lines where the final call held the read | %d |" % r["held"])
    out.append("")
    if apart:
        out.append("First attempts left out of this table: %s." % "; ".join(apart))
        out.append("")
    out.append("| Line | Account | Key | Error type | Compared | Tapped before the draft | Held | "
               "Toward the key | Away from the key |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in r["per_line"]:
        out.append("| %d | %s %s | %s | %s | %d | %d | %d | %d | %d |"
                   % (c["n"], c["acct"], c["name"], c["key"], c["type"], c["compared"],
                      c["tapped"], c["held"], c["toward"], c["away"]))
    out.append("")


def build_set_markdown(s, report, out):
    case1, case2 = s["case1"], s["case2"]
    out.append("## Case set %s" % s["label"])
    out.append("")
    if not s["n_attempts"]:
        out.append("No first attempt was made on this case set. Its %s attempt%s came from "
                   "codenames that had already played another case set, so %s listed in the "
                   "reattempt table and no rate is computed here."
                   % (say(s["n_reattempts"]), "" if s["n_reattempts"] == 1 else "s",
                      "it is" if s["n_reattempts"] == 1 else "they are"))
        out.append("")
        return
    out.append("Scored against `%s`%s and no other key. Every rate in this block reads the "
               "first attempt by each codename on this case set, and reattempts stay in their "
               "own table." % (case1["path"], (" and `%s`" % case2["path"]) if case2 else ""))
    out.append("")
    if len(s["dates"]) > 1:
        out.append("Warning: these records carry more than one key date (%s) for the same "
                   "version. Read the case file's change log before reporting."
                   % ", ".join(s["dates"]))
        out.append("")

    sentences, words, video = write_sentences(s, report)
    out.append("### Paste into the write-up")
    out.append("")
    out.extend(sentences)
    out.append("")
    out.append("(%d words)" % words)
    out.append("")
    rs = reason_sentence(s)
    if rs:
        out.append("One more sentence, on the reason chips, if the write-up has room for it:")
        out.append("")
        out.append(rs)
        out.append("")
    out.append("### Paste into the video script")
    out.append("")
    out.append(video)
    out.append("")

    out.append("### First attempts")
    out.append("")
    out.append("| Measure | Value |")
    out.append("| --- | --- |")
    out.append("| First attempts on this case set | %d |" % s["n_attempts"])
    out.append("| Completed | %d |" % s["n_completed"])
    out.append("| Facilitator-confirmed participants | %s |"
               % (s["participants_confirmed"] if s["participants_confirmed"] is not None
                  else "not available, no roster supplied"))
    out.append("| Reattempts on this case set, not in any rate | %d |" % s["n_reattempts"])
    out.append("| Mean call agreement, lines of %d | %s |"
               % (s["n_lines"], "%.1f" % s["mean_score"] if s["mean_score"] is not None else "n/a"))
    out.append("| Median call agreement, lines of %d | %s |"
               % (s["n_lines"], "%g" % s["median_score"] if s["median_score"] is not None else "n/a"))
    out.append("| Catch rate, %d problem lines | %s (%d of %d) |"
               % (s["n_problem"], fmt_pct(s["catch_rate"], 1), s["catch_counts"][0],
                  s["catch_counts"][1]))
    out.append("| Correct let stand rate, %d clean lines | %s (%d of %d) |"
               % (s["n_clean"], fmt_pct(s["let_stand_rate"], 1), s["let_stand_counts"][0],
                  s["let_stand_counts"][1]))
    out.append("| False flag rate | %s (%d of %d) |"
               % (fmt_pct(s["false_flag_rate"], 1), s["false_flag_counts"][0],
                  s["false_flag_counts"][1]))
    out.append("| Reason chip agreement, practice lines | %s (%d of %d scored) |"
               % (fmt_pct(s["reason_rate"], 1), s["reason_counts"][0], s["reason_counts"][1]))
    out.append("| Elapsed minutes on the page, median | %s |"
               % ("%g" % s["minutes_median"] if s["minutes_median"] is not None else "n/a"))
    out.append("| Elapsed minutes on the page, mean | %s |"
               % ("%.1f" % s["minutes_mean"] if s["minutes_mean"] is not None else "n/a"))
    out.append("| Best streak posted | %s |"
               % (s["streak_best"] if s["streak_best"] is not None else "n/a"))
    out.append("| First attempts that flagged every line | %d |" % len(s["flag_everything"]))
    out.append("| Calls carrying a basis chip | %s (%d of %d) |"
               % (fmt_pct(s["basis"]["basis_rate"], 1), s["basis"]["calls_with_basis"],
                  s["basis"]["calls_total"]))
    out.append("| Flags carrying a line of the player's own words | %s (%d of %d) |"
               % (fmt_pct(s["basis"]["flag_words_rate"], 1), s["basis"]["flags_with_words"],
                  s["basis"]["flags_total"]))
    out.append("| First attempts with a basis chip on every line | %d |" % s["coverage_full"])
    out.append("")

    out.append("### By organization")
    out.append("")
    out.append("The chapter chips a player tapped. One attempt can carry two, so these sum "
               "above the first attempt count, and a chip is a self-description rather than a "
               "confirmed role.")
    out.append("")
    out.append("| Chapter | First attempts |")
    out.append("| --- | --- |")
    for chip, count in s["org_counts"].items():
        out.append("| %s | %d |" % (chip, count))
    out.append("")

    out.append("### Call agreement and reason chip agreement by error type")
    out.append("")
    out.append("Two separate results. Call agreement is the flag or stand decision against "
               "the key. Reason chip agreement is whether the chips tapped fall inside the "
               "line's accepted reason categories.")
    out.append("")
    out.append("| Error type | Lines | Calls seen | Call agreement | Reasons scored | "
               "Reason chip agreement |")
    out.append("| --- | --- | --- | --- | --- | --- |")
    for etype in s["type_order"]:
        b = s["by_type"][etype]
        out.append("| %s | %s | %d | %s (%d) | %d | %s (%d) |"
                   % (etype, ", ".join(str(x) for x in b["lines"]), b["seen"],
                      fmt_pct(b["rate"], 1), b["right"], b["reason_scored"],
                      fmt_pct(b["reason_rate"], 1), b["reason_right"]))
    out.append("")

    out.append("### What reason chip agreement measures")
    out.append("")
    out.append("A reason agrees when at least one chip was tapped and every chip tapped is in "
               "the line's basis key. It is agreement with accepted reason categories. It is "
               "not a measure of reasoning quality, and it is not evidence of learning gain.")
    out.append("")
    for lim in s["limitations"]:
        out.append(lim["text"])
        out.append("")

    out.append("### The basis given, by error type")
    out.append("")
    out.append("The share is of the calls on those lines that carried a chip at all, and a "
               "player may tap more than one chip, so a row can sum above 100 percent.")
    out.append("")
    out.append("| Error type | Calls with a basis | Chips tapped |")
    out.append("| --- | --- | --- |")
    for etype, b in sorted(s["basis"]["by_type"].items(),
                           key=lambda kv: (kv[0] == "clean line", kv[0])):
        if not b["chips"]:
            out.append("| %s | 0 of %d | none recorded |" % (etype, b["calls"]))
            continue
        chips = "; ".join("%s %d (%s)" % (chip, count, fmt_pct(pct(count, b["with_basis"])))
                          for chip, count in b["chips"].items())
        out.append("| %s | %d of %d | %s |" % (etype, b["with_basis"], b["calls"], chips))
    out.append("")

    out.append("### In their own words")
    out.append("")
    if s["basis"]["examples"]:
        out.append("Verbatim, up to three per error type.")
        out.append("")
        for etype in sorted(s["basis"]["examples"], key=lambda t: (t == "clean line", t)):
            out.append("**%s**" % etype)
            out.append("")
            for ex in s["basis"]["examples"][etype]:
                out.append("- \"%s\" (%s, line %d, account %s, called %s)"
                           % (ex["words"], ex["codename"], ex["line"], ex["acct"], ex["call"]))
            out.append("")
    else:
        out.append("Nobody used the optional line of their own words on this case set.")
        out.append("")

    out.append("### By card")
    out.append("")
    out.append("| Line | Account | Key | Error type | Seen | Call agreement | Flagged | "
               "Reason chip agreement |")
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in s["per_card"]:
        out.append("| %d | %s %s | %s | %s | %d | %s (%d) | %d | %s |"
                   % (c["n"], c["acct"], c["name"], c["key"], c["type"], c["seen"],
                      fmt_pct(c["rate"], 1), c["right"], c["flagged"],
                      fmt_pct(c["reason_rate"], 1)))
    out.append("")

    build_read_markdown(s, out)

    out.append("### By first attempt")
    out.append("")
    out.append("The game rank is the page's own label for its points, which include a bonus "
               "for agreeing reason chips. It is a game rank, not a credential or a measure of "
               "professional skill, and a row filed before the page posted it reads not posted.")
    out.append("")
    out.append("| Codename | Call agreement of %d | Reason chip agreement | Game rank | Minutes "
               "| Best streak | Flags | Cards with a chip | Chapters |" % s["n_lines"])
    out.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for a in sorted(s["attempts"], key=lambda x: (-x["score"], x["row_index"])):
        out.append("| %s | %d | %s | %s | %s | %s | %d | %d of %d | %s |"
                   % (a["codename"], a["score"],
                      ("%d of %d" % (a["reason_right"], a["reason_scored"]))
                      if a["reason_scored"] else "not scored",
                      a["posted_rank"] or "not posted",
                      ("%g" % a["minutes"]) if a["minutes"] else "n/a",
                      a["best_streak"] if a["best_streak"] is not None else "n/a",
                      a["flags"], a["coverage"], s["n_lines"], ", ".join(a["orgs"]) or "none"))
    out.append("")
    if s["flag_everything"]:
        out.append("Flagged every line: %s." % ", ".join(s["flag_everything"]))
        out.append("")

    f = s["fresh"]
    out.append("### The fresh case")
    out.append("")
    if not case2:
        out.append("This case set has no fresh case.")
        out.append("")
    elif not f["n"]:
        out.append("No Round2 string in question C on these first attempts.")
        out.append("")
    else:
        out.append("Scored against `%s`, read out of question C." % case2["path"])
        out.append("")
        out.append("| Measure | Value |")
        out.append("| --- | --- |")
        out.append("| First attempts with a fresh case result | %d of %d |" % (f["n"], s["n_attempts"]))
        out.append("| Fresh case call agreement | %s (%d of %d calls) |"
                   % (fmt_pct(f["call_mean"], 1), f["right"], f["total"]))
        out.append("| Fresh case reason chip agreement, mean | %s |" % fmt_pct(f["reason_mean"], 1))
        out.append("| Practice case call agreement, same attempts | %s |"
                   % fmt_pct(f["practice_mean"], 1))
        out.append("| Difference between the two item sets | %s |"
                   % ("%+.1f points" % f["difference"] if f["difference"] is not None else "n/a"))
        out.append("| Fresh case clock, median seconds | %s |"
                   % ("%g" % f["seconds_median"] if f["seconds_median"] else "n/a"))
        out.append("")
        out.append("| Fresh line | Keyed call | Seen | Call agreement | Reason chip agreement |")
        out.append("| --- | --- | --- | --- | --- |")
        for line in f["per_line"]:
            out.append("| %d %s | %s | %d | %s | %s |"
                       % (line["n"], line["name"], line["key"], line["seen"],
                          fmt_pct(line["rate"], 1), fmt_pct(line["reason_rate"], 1)))
        out.append("")
        out.append("The fresh lines are a second unseen item set scored the same way, not a "
                   "post-test. With %s items and no comparable baseline, the difference above "
                   "separates two item sets and does not establish learning gain, transfer or "
                   "time saved." % say(f["lines"]))
        out.append("")
        if f["basis_lines"]:
            out.append("| Fresh line error type | Chips tapped |")
            out.append("| --- | --- |")
            for etype, chips in sorted(f["basis_by_type"].items(),
                                       key=lambda kv: (kv[0] == "clean line", kv[0])):
                out.append("| %s | %s |" % (etype, "; ".join("%s %d" % (c, n)
                                                             for c, n in chips.items())))
            out.append("")

    e = s.get("explain")
    if e:
        build_explanation_markdown(e, s, report, out)

    if s["professors"]:
        p = s["professors"]
        out.append("### The Professor chip")
        out.append("")
        out.append("First attempts carrying the Professor chip, a self-selected chip rather "
                   "than a confirmed role: %d (%s). Mean call agreement %.1f of %d, catch rate "
                   "%s on the %d problem lines."
                   % (p["n"], ", ".join(p["codenames"]),
                      p["mean_score"], s["n_lines"], fmt_pct(p["catch_rate"], 1), s["n_problem"]))
        out.append("")

    out.append("### Where the record disagrees with itself")
    out.append("")
    if s["disagreements"]:
        out.append("Every rate above uses the key in `%s`. Each line below is a place where "
                   "the record the page wrote says something different, which is worth reading "
                   "before any number leaves this page." % case1["path"])
        out.append("")
        for item in s["disagreements"]:
            out.append("- %s" % item)
        out.append("")
    else:
        out.append("The Why fields, the Accept or Reject columns and the case files agree on "
                   "every call on this case set.")
        out.append("")


def build_markdown(report, csv_path):
    out = []
    today = datetime.date.today().isoformat()
    out.append("# Second Pass: Beat the Machine, findings")
    out.append("")
    out.append("Built %s from `%s`." % (today, os.path.basename(csv_path)))
    out.append("")
    if report["synthetic_check"]:
        out.append("**Synthetic verification run. Not participant evidence.** Rows matching "
                   "the synthetic rule were scored so a review probe can be reproduced. Nothing "
                   "in this file may be copied into a readout or an application.")
        out.append("")

    out.append("## Attempts and people")
    out.append("")
    out.append("| Count | Value | What it counts |")
    out.append("| --- | --- | --- |")
    for label, value, meaning in count_rows(report):
        out.append("| %s | %s | %s |" % (label, value, meaning))
    out.append("")

    out.append("## Rows excluded from participant evidence")
    out.append("")
    for key, label in EXCLUSION_LABELS:
        items = report["excluded"][key]
        out.append("- %s: %d%s" % (label, len(items),
                                   (", " + "; ".join(items)) if items else ""))
    out.append("- Duplicate sends set aside: %d%s"
               % (len(report["duplicate_sends"]),
                  (", " + "; ".join(report["duplicate_sends"])) if report["duplicate_sends"] else ""))
    out.append("")
    out.append("Every exclusion names the rule that made it. A test codename is one on the list of "
               "known test codenames, or one made only of test words with test or delete among "
               "them (\"Test Play\", \"walk test 2\"), so a real codename that merely contains "
               "test (\"Test Pilot\", \"Contest Winner\") stays in. A synthetic row is one whose "
               "codename begins with Synthetic, or one with a cell or a basis Words line that "
               "reads exactly \"Synthetic test only\". The third independent review's synthetic "
               "records match it, so they cannot enter participant evidence from this script. "
               "Codenames are read after NFKC normalization and case folding, so a full-width "
               "spelling is treated as the plain one.")
    out.append("")

    out.append("## Attempt conflicts")
    out.append("")
    if report["conflicts"] or report["conflicts_resolved"]:
        out.append("One attempt identifier on rows whose content differs is not a resend, and "
                   "the script does not guess which row is the attempt. An unresolved conflict "
                   "holds every one of its rows out of every count and rate, and a later attempt "
                   "under the same codename counts it as the earlier attempt rather than becoming "
                   "a first attempt. To resolve one, read the rows in the export and run again "
                   "with `--resolve-conflict <attempt id>=<sheet row to keep>`. Sheet rows count "
                   "the header as row 1.")
        out.append("")
    else:
        out.append("No attempt identifier appears on rows whose content differs.")
        out.append("")
    for label, entries in (("Unresolved", report["conflicts"]),
                           ("Resolved by the facilitator", report["conflicts_resolved"])):
        for c in entries:
            kept = c.get("kept_row")
            out.append("**%s: attempt %s**%s" % (label, c["attempt_id"],
                                                 (", sheet row %d kept" % kept) if kept else ""))
            out.append("")
            out.append("| Sheet row | Codename | Timestamp | Case set | Call agreement | Fresh "
                       "calls | Completed |")
            out.append("| --- | --- | --- | --- | --- | --- | --- |")
            for r in c["records"]:
                out.append("| %d | %s | %s | %s | %s | %s | %s |"
                           % (r["sheet_row"], md_cell(r["codename"]), r["timestamp"] or "n/a",
                              r["set"] or ("refused: " + md_cell(r["refusal"] or "")),
                              ("%d of %d" % (r["score"], r["lines"])) if r["lines"] else "n/a",
                              r["fresh_calls"] or "n/a", "yes" if r["completed"] else "no"))
            out.append("")
            if c["differences"]:
                out.append("Where the records differ, by column, each value in sheet row order:")
                out.append("")
                for d in c["differences"]:
                    out.append("- %s: %s" % (d["column"], " / ".join(
                        '"%s"' % md_cell(v) for v in d["values"])))
                out.append("")

    out.append("## Case versions")
    out.append("")
    out.append("Every received attempt as its record names its cases. Each case set below is "
               "scored against its own case files, and a refused attempt is scored against "
               "nothing.")
    out.append("")
    out.append("| Cases as recorded | Received attempts |")
    out.append("| --- | --- |")
    for tag, count in report["case_versions"].items():
        out.append("| %s | %d |" % (tag, count))
    out.append("")
    if report["refusal_counts"]:
        out.append("### Attempts refused from scoring")
        out.append("")
        out.append("| Reason | Attempts |")
        out.append("| --- | --- |")
        for reason, count in report["refusal_counts"].items():
            out.append("| %s | %d |" % (reason, count))
        out.append("")
        out.append("Refused: %s." % ", ".join(a["codename"] for a in report["refused"]))
        out.append("")
    if not report["cases_dir"]:
        out.append("No cases directory was found, so every attempt is refused. Pass --cases "
                   "with the path to beat-the-machine/cases.")
        out.append("")
    if len(report["sets"]) > 1:
        out.append("This export holds %s case sets. They are reported in separate blocks and "
                   "no rate pools them." % say(len(report["sets"])))
        out.append("")

    if report["roster"]:
        r = report["roster"]
        out.append("## Roster")
        out.append("")
        out.append("Read from `%s`, the consented roster the facilitator supplied." % r["path"])
        out.append("")
        out.append("| Measure | Value |")
        out.append("| --- | --- |")
        out.append("| Roster rows | %d |" % r["rows"])
        out.append("| Rows without consent, not read | %d |" % r["rows_without_consent"])
        out.append("| Facilitator-confirmed participants with a received attempt | %d |"
                   % r["n_confirmed"])
        out.append("| Roster codenames with no received attempt | %d |"
                   % r["roster_codenames_without_attempt"])
        out.append("| Received codenames not on the roster | %d |"
                   % r["attempt_codenames_not_on_roster"])
        out.append("| Codenames claimed by two participants, not confirmed | %d |"
                   % len(r["codename_conflicts"]))
        out.append("")
        if r["roles"]:
            out.append("| Role, as the facilitator recorded it | Confirmed participants |")
            out.append("| --- | --- |")
            for role, count in r["roles"].items():
                out.append("| %s | %d |" % (role, count))
            out.append("")

    for s in report["sets"]:
        build_set_markdown(s, report, out)

    out.append("## Reattempts")
    out.append("")
    if report["reattempts"]:
        out.append("Later attempts by a codename that already has a first attempt counted. "
                   "They enter no rate above, because a player who has seen the reveal once "
                   "answers with something the first attempt did not have.")
        out.append("")
        out.append("| Codename | Attempt number | Case set | Timestamp | Call agreement | Reason "
                   "chip agreement | Fresh case calls agreeing |")
        out.append("| --- | --- | --- | --- | --- | --- | --- |")
        for a in report["reattempts"]:
            out.append("| %s | %d | %s | %s | %d of %d | %s | %s |"
                       % (a["codename"], a["attempt_number"], a["set"], a["timestamp"] or "n/a",
                          a["score"], len(a["case1"]["cards"]),
                          ("%d of %d" % (a["reason_right"], a["reason_scored"]))
                          if a["reason_scored"] else "not scored",
                          ("%d of %d" % (a["fresh"]["right"], a["fresh"]["total"]))
                          if a["fresh"] else "n/a"))
        out.append("")
        after = [a for a in report["reattempts"] if a.get("after_conflict")]
        if after:
            out.append("Counted after an unresolved attempt conflict under the same codename, "
                       "which holds the first-attempt place until it is resolved: %s."
                       % "; ".join("%s (after attempt %s)" % (a["codename"],
                                                           ", ".join(a["after_conflict"]))
                                   for a in after))
            out.append("")
    else:
        out.append("No codename has a second eligible attempt in this export.")
        out.append("")

    out.append("## The four questions that are not asked")
    out.append("")
    out.append("Expected quality, confidence before the round, month end close experience and "
               "confidence after the round are never put to the player. Rows filed before 13 "
               "September 2026 carry fixed values that read like answers, and later rows carry "
               "the literal `not asked`. Neither is a player answer, so **none of these four "
               "columns enters any measure in this report**.")
    out.append("")
    out.append("| Question | Sent as `not asked` | Fixed placeholder value | Something else | Blank |")
    out.append("| --- | --- | --- | --- | --- |")
    for item in report["intake"]:
        k = item["kinds"]
        out.append("| %s | %d | %d | %d | %d |"
                   % (item["label"], k["not asked"], k["placeholder"], k["value"], k["blank"]))
    out.append("")

    out.append("## Columns")
    out.append("")
    if report["missing"]:
        out.append("Not found in the export, so anything that needed them is missing from the "
                   "tables above:")
        out.append("")
        for label in report["missing"]:
            out.append("- %s" % label)
    else:
        out.append("Every question title matched a column in the export.")
    out.append("")
    return "\n".join(out) + "\n"


def print_summary(report, out_path):
    line = "-" * 66
    print(line)
    print("Second Pass findings")
    if report["synthetic_check"]:
        print("SYNTHETIC VERIFICATION RUN. NOT PARTICIPANT EVIDENCE.")
    print(line)
    for label, value, _meaning in count_rows(report):
        print("%-40s %s" % (label, value))
    for key, label in EXCLUSION_LABELS:
        if report["excluded"][key]:
            print("  excluded, %-29s %d" % (label.lower(), len(report["excluded"][key])))
    for reason, count in report["refusal_counts"].items():
        print("  REFUSED %d: %s" % (count, reason))
    for c in report["conflicts"]:
        print("  CONFLICT, held out: attempt %s on sheet rows %s"
              % (c["attempt_id"], ", ".join(str(r["sheet_row"]) for r in c["records"])))
    for s in report["sets"]:
        print(line)
        print("Case set %s" % s["label"])
        print("  First attempts %d, completed %d, reattempts %d"
              % (s["n_attempts"], s["n_completed"], s["n_reattempts"]))
        print("  Catch rate            %s (%d of %d)"
              % (fmt_pct(s["catch_rate"], 1), s["catch_counts"][0], s["catch_counts"][1]))
        print("  False flag rate       %s (%d of %d)"
              % (fmt_pct(s["false_flag_rate"], 1), s["false_flag_counts"][0],
                 s["false_flag_counts"][1]))
        print("  Mean call agreement   %s of %d"
              % ("%.1f" % s["mean_score"] if s["mean_score"] is not None else "n/a", s["n_lines"]))
        print("  Reason chip agreement %s (%d of %d scored), agreement with accepted categories"
              % (fmt_pct(s["reason_rate"], 1), s["reason_counts"][0], s["reason_counts"][1]))
        if s["read"]["n"]:
            r = s["read"]
            print("  Read before the draft %d of %d lines moved, %d toward the key, %d away, "
                  "first attempts, descriptive" % (r["changed"], r["compared"], r["toward"],
                                                   r["away"]))
        if s["fresh"] and s["fresh"]["n"]:
            f = s["fresh"]
            print("  Fresh case            call agreement %s (%d of %d), n=%d, %s"
                  % (fmt_pct(f["call_mean"], 1), f["right"], f["total"], f["n"],
                     s["case2"]["version"]))
        if s.get("explain") and s["explain"]["items"]:
            e = s["explain"]
            print("  Explanations          %d written, %d scored, total mean of 6 %s, %d double scored"
                  % (e["items"], e["scored"],
                     "%.2f" % e["total_avg"] if e["total_avg"] is not None else "n/a",
                     e["double_scored"]))
        if s.get("explain") and s["explain"]["gaps"]:
            e = s["explain"]
            print("  BELOW THE MINIMUM     %d written part%s on %d first attempt%s, counted "
                  "incomplete, listed in the markdown"
                  % (e["parts_below_minimum"], "" if e["parts_below_minimum"] == 1 else "s",
                     e["first_attempts_with_gaps"], "" if e["first_attempts_with_gaps"] == 1 else "s"))
        if s["disagreements"]:
            print("  RECORD DISAGREEMENTS  %d, listed in the markdown" % len(s["disagreements"]))
    print(line)
    if report["missing"]:
        print("COLUMNS NOT FOUND (%d). Check the header row in the export." % len(report["missing"]))
    else:
        print("All question titles matched a column.")
    print("Written to %s" % out_path)
    print(line)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Findings from the Second Pass: Beat the Machine responses CSV.")
    ap.add_argument("csv", help="path to the responses CSV")
    ap.add_argument("--out", help="markdown output path (default FINDINGS-<today>.md beside "
                                  "this script)")
    ap.add_argument("--fields", nargs="?", const="-", default=None,
                    help="also write the readout field contract as JSON; pass a path, or leave "
                         "it bare to print it")
    ap.add_argument("--roster", help="the facilitator's consented roster CSV "
                                     "(participant, codename, consent, role)")
    ap.add_argument("--cases", help="the cases directory (default ../cases beside this script, "
                                    "then ./cases)")
    ap.add_argument("--scoring-sheet",
                    help="write the blind explanation scoring sheet (CSV) for the educator here")
    ap.add_argument("--scoring-key",
                    help="write the facilitator key for that sheet here (default: beside the "
                         "sheet, ending -facilitator-key.csv)")
    ap.add_argument("--scores", help="the scoring sheet as the first scorer filled it")
    ap.add_argument("--second-scores", help="the scoring sheet as the second scorer filled it")
    ap.add_argument("--synthetic-check", action="store_true",
                    help="score rows the synthetic rule excludes, to reproduce a review probe; "
                         "every output is stamped as not participant evidence")
    ap.add_argument("--resolve-conflict", action="append", default=[], metavar="ID=ROW",
                    help="keep sheet row ROW (the header is row 1) for attempt identifier ID "
                         "when rows carrying it differ; repeat for each conflict")
    args = ap.parse_args(argv)

    if not os.path.exists(args.csv):
        print("No file at %s" % args.csv)
        return 2
    if args.cases and not os.path.isdir(args.cases):
        print("No cases directory at %s" % args.cases)
        return 2
    resolutions = {}
    for spec in args.resolve_conflict:
        attempt_id, _, row = spec.partition("=")
        if not attempt_id.strip() or not row.strip().isdigit():
            print("--resolve-conflict takes ID=ROW, for example att-k3x=14; got %r" % spec)
            return 2
        resolutions[attempt_id.strip()] = int(row)
    try:
        report = analyze(args.csv, roster_path=args.roster, cases_dir=args.cases,
                         synthetic_check=args.synthetic_check, scores_path=args.scores,
                         second_scores_path=args.second_scores, resolutions=resolutions)
    except InputError as exc:
        print(str(exc))
        return 2
    out_path = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "FINDINGS-%s.md" % datetime.date.today().isoformat())
    fields = readout_fields(report, args.csv)
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(build_markdown(report, args.csv))
        handle.write("\n" + fields_block(fields, report["missing"]))
    if args.fields:
        blob = json.dumps(fields_json(fields), indent=2, ensure_ascii=False)
        if args.fields == "-":
            print(blob)
        else:
            with open(args.fields, "w", encoding="utf-8") as handle:
                handle.write(blob + "\n")
            print("Readout fields written to %s" % args.fields)
    if args.scoring_sheet:
        key_path = args.scoring_key or (os.path.splitext(args.scoring_sheet)[0] +
                                        "-facilitator-key.csv")
        count = write_scoring_sheet(report, args.scoring_sheet, key_path)
        print("Scoring sheet with %d explanation%s written to %s, facilitator key to %s"
              % (count, "" if count == 1 else "s", args.scoring_sheet, key_path))
    print_summary(report, out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
