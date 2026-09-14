# Second Pass, release 1.6.1

13 September 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

---

## 1.7.0, what changed since 1.6.1 (draft, not released)

Draft written 13 September 2026. It is not released: the heading of this file stays at 1.6.1 until
the repaired release is frozen, and nothing below is pushed until then. Every change answers a
finding in the third independent review of 13 September 2026, which reviewed 1.6.1 at `b6ba468` and
the command line package at `130b6b7`. Commits in the second-pass repository are marked as such.

| Finding in the third review | What changed | Commits |
| --- | --- | --- |
| **1. The record counted attempts as players and scored a new case against the old key.** Two attempts under one codename came back as two players, and a Kestrel record was scored against Halyard | `tools/findings.py` scores every record against the case file for the version it names and refuses a version it has no file for. It reports received attempts, completed attempts, distinct codenames and facilitator-confirmed participants as four separate counts, reads only the first eligible attempt under each codename, and lists reattempts in their own table. `READOUT-TEMPLATE.md` defines each count once, and the facilitator guides never report codenames as people. The sample carries brightwater-v6 runs with written explanations | `c6f0088`, `3bdb3ff`, `a42d7af`, `19f4605`, `56b87a7` |
| **2. The reviewer page claimed more than the build shows.** "Reads better than a person writes", "every figure against the ledger", the universal input promise, and a counted unit named two ways | `review.html` claims only what the checker and the evidence show. The drill's scope note, the 404 page, the release notes and the facilitator guides no longer promise any ledger or every figure. The two earlier design variants, `review-a.html` and `review-b.html`, still served and still carrying the old claims, are retired to a noindex pointer at `review.html` | `b956423`, `8abea9e`, `19f4605`, `49767ad` |
| **3. The reason score and the rank.** The case guide said the reason score never moves the rank, and the executed points said it does. Chips measure agreement with accepted categories, not reasoning, and the Brightwater evidence pre-solved item 3 | The case guide, the governance note, both facilitator guides and five strings in the drill now say the reason's fifty points count toward the rank; the scoring code is unchanged. On `brightwater-v6` every assessment call needs a three-part written explanation (the decisive evidence, why it matters for the period, the action or source request) before it locks, the evidence shows document contents without saying what they establish, and `RUBRIC.md` with a blind scoring sheet puts the explanations in front of an educator | `8abea9e`, `f376b84`, `6447d97`, `1fcedbd`, `19f4605` |
| **4. The checker contract.** "Doubled", "remained at", a fraction and Arabic-Indic digits all cleared, Prompt 1's own labels were not read as roles, and the parity claim was byte for byte on files that differed | Multipliers, fractions, digits outside 0 to 9 and scale words are unparsed spans that leave a sentence not checked; "remained at" and other no-change claims no longer clear when the line moved; `prior` and `current` in front of a figure are read as roles. `CHECKER.md` says what the grammar reads and a sentence clears only when every quantitative expression in it is accounted for. The suite holds 212 fixtures, including the forty probes and 113 mutations across six classes, and the Prompt 1 rerun is recorded in `audit/PROMPT1-RERUN-2026-09-13.md`. The Python checker mirrors the contract, and one shared file of 212 inputs agrees on every compared field in both implementations | `d081409`, `71d457b`; second-pass `acdf580`, `fe8cd49`, `b523044` |
| **5. The author page.** An unresolved checker result became a clean suggestion, a save after an edit kept stale figures, and an unbound sentence vanished | The author page reads with the checker's own reader and holds what the checker holds, including a direction word it cannot tie to a line; save and preview are disabled until the inputs are read again; every sentence comes back as a card or an open item that must be settled; the case records whether it is synthetic or a permitted real case, and the drill's introduction follows it. A card checked within scope now names the numbers the checker read and left outside the check | `052fd1f`, `81f92dc`, `1fcedbd`, `5c6f9ab`, `742525a`, `50927f4` |
| **6. The three-ledger evidence.** The runs were not comparable, and unsupported exclusions and forecasts were not counted | Every unsupported claim in the six retained drafts is counted by class with its exact text, the development-session run is labeled apart from the fresh-context runs, and the prediction inference is gone | `a3ada19` |

**The read before the draft.** Not a review finding: Khaled ruled at about 9:40 PM on 13 September
2026 to keep the ledger-only step and make it count, because it is the one point where a player
decides before seeing anything the AI drafted. It is now required with no skip and no cap, locked
once the player goes on, and no later screen draws without it, whether reached by a button, a key,
the step hook or an edited saved run. The end screen says on how many round one lines the final
call moved off that read, and whether each change moved toward the key or away from it, with no
effect on points or rank. The round one question and the record carry the read per line with the
case version, the data notice names it (`notice-2026-09-13c`), and `findings.py` reports the
comparison for first attempts in each case set as descriptive agreement on a keyed exercise, with
six new tests. Walked in headless Chrome on Halyard, Kestrel and an authored case, 44 of 44
checks each, with viewport screenshots at six widths looked at by eye, in
`audit/PREPICKS-2026-09-13.md`. Commits `29df0aa`, `bce4a15`, `a4b1538`.

### What remains open

- **Receipt deployment.** `RECEIPT_ENDPOINT` is still empty in `index.html`. A synthetic receipt has
  to reach the real destination, and a retried attempt has to leave one stored record, before any
  collection is described as a verified store.
- **Observed practitioner sessions.** Two or three practitioners on a ledger and memo they did not
  build, uncoached, each ending in a saved review record. None has happened.
- **Educator review.** An independent educator's review of the keys, and blind scoring of the written
  explanations against `RUBRIC.md`, with a second scorer on a subset. Not yet done.
- **Clean-context evidence reruns.** The three paired drafts repeated in fresh contexts under fixed
  instructions, with every output kept and a second reader classifying the unsupported claims. Not
  yet run.
- **Opening a saved case in the author page.** The author page saves a case file but cannot open
  one. Ruled on 13 September 2026 to come after the freeze.

---

## 1.6.1, what changed since 1.6.0

1.6.1 closes the items the release QA of 13 September left open that did not need another person.

| What | Where | Evidence |
| --- | --- | --- |
| A quantity written out in words is read, or the sentence says it was not. Units through millions, hyphenated compounds included: a run becomes a figure where the parser resolves it and the words give it a unit, and otherwise it reaches the reviewer's queue and the sentence is not checked. A count in words beside no claim is left alone | `checker.html`, `CHECKER.md` rule 1c | fixtures `T49` to `T54`, and `T21` now fails a false percentage in words rather than leaving it unparsed. 59 fixtures, 59 pass. Mirrored in `second_pass/checker.py`, 138 pass |
| Three claims on the reviewer page corrected, and five more found reading the page against `CHECKER.md`, `PROTOCOL.md` and the evidence note | `review.html` | the page now says the protocol asks for four steps rather than that the site enforces them, that this checker leaves the driver and the period to a reviewer, and that the machine check is a figure that does not tie to the line it names |
| Two record fields renamed to what they hold, with the old names alongside for this version | `index.html`, `README.md` | `evidenceSupplied` with `evidenceSelected` beside it, `elapsedSecondsOnCard` and `activeSecondsOnCard`, `firstRunInThisTab`, and `renamedFields` on the record |
| The card clock now also reports time with the tab's hidden time taken out of it | `index.html` | `activeSecondsOnCard`, `activeSecondsOnCards` and `hiddenSecondsInRun`, measured on `visibilitychange` |
| Every on-file fact in the fresh case carries a one-line excerpt from a named, dated document, or says the document was requested and is not on file. The wrong-period item rests on a real quoted schedule dated 31 May 2026 | `cases/brightwater-v5.json` | the file's own change log; verified in the page in test mode at card 3 of 5 |
| The facilitator guide no longer decides the accrual from a contradiction, and every percentage in it is attributed or gone | `FACILITATOR-GUIDE.md`, `FACILITATOR-ONE-PAGE.md`, `Second-Pass-Facilitator-Guide.pdf` | the two sample-findings rates are out, because no room has run this yet |

---

## The problem

A month-end close now produces flux commentary faster than a person can read it. The sentences
come back fluent, the arithmetic usually holds, and the reason attached to each movement is the
part nobody checks. A reviewer under a close deadline reads for tone and reads for whether the
numbers look about right, and a sentence that names a cause no document supports goes into the
management report with everything else.

The failure is not that the machine cannot add. It is that a memo which adds up correctly and
explains itself confidently is the hardest thing in a close to argue with, and the accounting
judgment it displaces is exactly the judgment a student is supposed to be learning.

Second Pass is a training instrument and a working tool for the second reading. It teaches the
reviewer's move: recompute the figure, test the direction, find the line nobody wrote about, and
then ask what document would carry the cause the sentence names.

## What was built

Four pages, all static, all free, none behind a sign-in.

**A drill.** A player takes a fourteen-line ledger and a memo drafted against it, one account at a
time, and decides on each whether the sentence stands or gets flagged. Every call is followed by a
basis: which of seven things is wrong, or that the figure and the reason hold. The call and the
basis are scored separately, because agreeing with the answer key while naming the wrong defect is
not judgment. After the fourteen practice lines a second company appears, five lines nobody has
seen, run as an assessment with nothing revealed until all five are committed.

**A checker.** Paste a ledger in a layout it accepts and a memo, set the commentary threshold, and
the page recomputes each figure it can read against the ledger, tests the direction words it can tie
to a line against the sign, names every account that clears the threshold with no sentence written
about it, and returns one of four statuses per sentence: checked within scope, needs review, not
checked, failed. A sentence carrying anything the grammar cannot read is not checked, and what it
could not read goes to the reviewer. It runs entirely in the
visitor's browser. Nothing pasted into it is transmitted anywhere.

**An author page.** Paste your own trial balance and your own memo and the page reads them,
proposes a call and an error type per line, asks you to key each one, and writes a case the drill
will run. The case is a JSON file you keep.

**A reviewer page.** One page that sets out the problem, the governance, the evidence, the
outcomes plan, the scope and the replicability, and links everything else.

## Governance

The checker's headline behavior is abstention. A sentence is cleared only when every figure in it
carries a role the words gave it, a unit, and an unrounded comparison with the ledger that agreed.
A figure whose role the words do not give stops a clearance before any value is compared. A
sentence naming two accounts is held unless each figure binds inside its own clause. A negation, a
spelled-out percentage, a foreign currency, a bare number the grammar cannot place: each leaves
the sentence unresolved rather than passing it. No unresolved status is promoted to checked by a
later step, and the reviewer prompt the page generates opens by naming the mechanical work that
was **not** done.

The written protocol, `PROTOCOL.md` at version 1.1, states the control: no commentary drafted with
AI assistance is released until a second pass has tied every figure to the ledger and a named
reviewer, never the preparer, has signed the two judgment questions, whether the driver is
supported by a document on file and whether it belongs to the period.

Participant data is handled on the same principle. A data notice appears before a codename is
chosen and says plainly that a codename is a pseudonym and not anonymity. Completing the drill
does not require sharing anything: saving a local record and sending results are two separate
buttons. Four questions the collection form carries are not asked in this version, and the record
says so rather than posting a value that would read as an answer. A send is labeled sent and
unconfirmed, because a hidden frame loading does not prove a receiver stored anything. A test mode
posts nothing at all and stamps the record for exclusion.

`GOVERNANCE-NOTE.md` carries the decisions and who made them. `PROVENANCE.md` states, without
softening it, that the case company does not exist, that the fourteen planted defects were
authored rather than generated, and that the build was carried out by an AI coding agent under
direction.

## The outcomes plan, and what it can support

Nobody has run the drill yet. The release claims nothing about learning, time saved or real close
errors, and the plan is written so that it cannot drift into claiming them.

What a pilot can support is descriptive agreement with an author's key, on completed and eligible
attempts, at a frozen case version. The measures are: right call and right reason by error type;
false flags on the six clean control lines; the fresh five against the trained fourteen, reported
as two item sets rather than as a pre-test and a post-test; and the reasons participants actually
wrote, scored by a person against a three-point rubric the page does not attempt itself.

`tools/findings.py` computes exactly those, reads the responses export, drops test rows and
repeats on the attempt identifier, counts each organization separately, and writes every field
`READOUT-TEMPLATE.md` names, the run fields once and one block per case set. A field the
responses cannot support prints *not available* rather than an estimate.

What the record cannot support is written down too: confidence is null because it was not asked;
the evidence list is what the card supplied, not what the participant consulted; elapsed time does
not pause for an inactive tab; a codename is not a reliable way to count people. Those limits are
in the reviewer page and in this file because a measure that outruns its instrument is the failure
the whole project is about.

## Replicability

Everything needed to run this somewhere else is in the repository, and none of it needs the
author present.

A facilitator runs a session from the guide alone. A student authors a case from their own trial
balance in the browser and the drill runs it. An accounting department pastes its own memo into
the checker and gets a review log with evidence identifiers, a proposed conclusion, a human
conclusion, an unresolved issue, an owner and a review time. The answer keys are JSON files with
change logs that name who asked for each change and why. The checker's contract has 53 regression
tests, and the two shared cases the checker demonstrates are generated from the same files the
drill reads, so the two surfaces cannot drift apart.

## Honest scope

- **No participant has used it.** There are no results, and none are implied anywhere.
- **No practitioner has been observed** running a real memo through it without coaching.
- **No educator has independently reviewed the answer keys.** The keys are defensible under the
  supplied case facts and have survived one external review, which is not the same thing.
- **The checker checks figures, not causes.** Four of the five sentences in the assessment case
  come back checked within scope and still need a person, and the page says so.
- **The fresh case gives author-summarized facts,** not source excerpts. Judging evidence from a
  summary of the evidence is a weaker test than judging it from the document.
- **A spelled-out quantity with no unit word can still clear the checker.** Named in
  `audit/RELEASE-QA-2026-09-13.md` with its reproduction.
- **The case company does not exist.** No client data, no engagement, no real ledger.

---

## Every file in the release

### Pages

| File | What it is |
| --- | --- |
| `index.html` | The drill: fourteen practice lines, then five assessment lines on a company the player has not seen |
| `checker.html` | The checker: paste a ledger and a memo, get a per-sentence status, a reviewer queue, a CSV, a printable sheet and two prompts |
| `author.html` | Build a drill from your own trial balance and your own memo |
| `review.html` | The entry in one page: problem, governance, evidence, outcomes, scope, replicability |
| `404.html` | The custom not-found page, with the three ways back |
| `review-a.html`, `review-b.html` | Retired. Two earlier design variants of the reviewer page, now a short noindex page each that points to `review.html`, kept so old links do not end on a 404 |

### Shared assets

| File | What it is |
| --- | --- |
| `assets/second-pass.css` | Every rule two pages share: the tokens, the controls, the focus ring, the tables, the action bar |
| `assets/nav.js` | The header, the footer and the skip link, printed onto every page from one template |
| `assets/second-pass-core.js` | The ledger and memo reader the checker and the author page both run |
| `assets/favicon.svg`, `assets/favicon-32.png` | The tab icon in both formats |
| `assets/og-image.png`, `assets/og-image.svg` | The share card |
| `robots.txt`, `sitemap.xml` | Everything public, nothing disallowed, five URLs listed |

### Cases

| File | What it is |
| --- | --- |
| `cases/README.md` | How a case file is shaped, how to pick one, how to author one, and what changed in each version |
| `cases/halyard-v4.json` | Halyard Provisioning Group, fourteen accounts, eight problem lines and six clean ones. The practice case |
| `cases/brightwater-v5.json` | Brightwater Dental Partners, five accounts, three problem lines and two clean ones. The assessment case. Every on-file fact carries a dated document excerpt |
| `cases/kestrel-v1.json` | Kestrel IT Services, twelve accounts, seven problem lines and five clean ones. The second practice case |
| `cases/halyard-v3.json`, `cases/brightwater-v4.json`, `cases/brightwater-v3.json`, `cases/brightwater-v2.json` | Superseded versions, kept because a response scored against one of them is not comparable to a response scored against the current pair |
| `build-cases.cjs` | Validates a case file and refuses one whose reveal text is missing |
| `build-checker-cases.cjs` | Regenerates the checker's Halyard and Brightwater samples from the same case files the drill reads |

### The written record

| File | What it is |
| --- | --- |
| `README.md` | The whole build: every screen, every rule, every number and where it comes from |
| `CHECKER.md` | What the checker checks, what it refuses to check, and the expected output for all four samples |
| `PROTOCOL.md` | The one-page control, version 1.1 |
| `Second-Pass-Review-Protocol.pdf` | The same protocol, printable |
| `PROVENANCE.md` | Where the case came from, who wrote the memo, and what was authored rather than generated |
| `GOVERNANCE-NOTE.md` | The decisions taken during the build and who took them |
| `INTRO-CANDIDATES.md` | The intro lines considered on 12 September, kept as history; none of them is the live intro |
| `RELEASE-NOTES.md` | This file |

### Running a session

| File | What it is |
| --- | --- |
| `FACILITATOR-GUIDE.md`, `Second-Pass-Facilitator-Guide.docx`, `.pdf`, `-p1.png` | Run a session from the guide alone, in three formats |
| `FACILITATOR-ONE-PAGE.md` | The same, cut to one page |
| `EVIDENCE-LOG-TEMPLATE.csv` | The review log a practitioner fills, with two worked rows |
| `EXCEL-TEMPLATE.md`, `Second-Pass-Excel-Template.xlsx`, `build_excel_template.py` | The same log as a workbook, and the script that builds it |
| `READOUT-TEMPLATE.md`, `Second-Pass-Results-Readout.docx` | The readout a facilitator fills after a session, three pages: the counts, each defined once, then one block for each case set, naming the field for every cell |
| `build-facilitator-pdf.py` | Builds the guide's docx and pdf from the markdown |

### Evidence

| File | What it is |
| --- | --- |
| `evidence/EVIDENCE-NOTE.md` | What two real AI drafting runs got wrong, bounded to those runs and this case |
| `evidence/ai-draft-*-raw.md` | Six raw model drafts, three ledgers, blind and under Prompt 1, unedited |
| `evidence/*-run.csv`, `*-recheck.csv` | Each draft put through the checker, exported |
| `evidence/ledger-paste.txt` | The exact input the drafts were given |

### Tests and tools

| File | What it is |
| --- | --- |
| `tests/checker-fixtures.json` | 212 fixtures: the original defect set, the adversarial probe sets, the forty probes and 113 mutations from the third review, the boundary cases, and the sample cases end to end |
| `tests/run-checker-tests.cjs` | Runs them against `checker.html` itself, with no browser |
| `tools/findings.py` | Reads the responses export and writes the findings and every field the readout names |
| `tools/make-sample-csv.py`, `tools/findings-sample.csv` | A synthetic response set in the shapes the page posts, so the script can be proved without waiting for participants |

### Audit

| File | What it is |
| --- | --- |
| `audit/RELEASE-QA-2026-09-13.md` | This release's QA: 38 screens at six widths, both independent reviews item by item, and the consistency sweep |
| `audit/accessibility-2026-09-13.md` | The accessibility pass |
| `audit/performance-2026-09-13.md` | The performance pass |
| `screenshots/release/` | 76 screens at 375 and 1280, one per state walked |
| `screenshots/` | Earlier passes, kept as the record of what each revision looked like |
