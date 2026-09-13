# Second Pass, release 1.6.1

13 September 2026. Khaled Alkurd, George Mason University.
Live at https://fiscalpatriots.github.io/beat-the-machine/

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

**A checker.** Paste a ledger and a memo, set the commentary threshold, and the page recomputes
every figure against the ledger, tests every direction word against the sign, names every account
that clears the threshold with no sentence written about it, and returns one of four statuses per
sentence: checked within scope, needs review, not checked, failed. It runs entirely in the
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
`READOUT-TEMPLATE.md` names, 127 of them. A field the responses cannot support prints *not
available* rather than an estimate.

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
| `review-a.html`, `review-b.html` | Two earlier design variants of the reviewer page, kept for the record and linked from nothing |

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
| `INTRO-CANDIDATES.md` | The intro lines considered and the one chosen |
| `RELEASE-NOTES.md` | This file |

### Running a session

| File | What it is |
| --- | --- |
| `FACILITATOR-GUIDE.md`, `Second-Pass-Facilitator-Guide.docx`, `.pdf`, `-p1.png` | Run a session from the guide alone, in three formats |
| `FACILITATOR-ONE-PAGE.md` | The same, cut to one page |
| `EVIDENCE-LOG-TEMPLATE.csv` | The review log a practitioner fills, with two worked rows |
| `EXCEL-TEMPLATE.md`, `Second-Pass-Excel-Template.xlsx`, `build_excel_template.py` | The same log as a workbook, and the script that builds it |
| `READOUT-TEMPLATE.md`, `Second-Pass-Results-Readout.docx` | One page a facilitator fills after a session, naming the field for every cell |
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
| `tests/checker-fixtures.json` | 59 fixtures: the original defect set, the adversarial probe set, the boundary cases, and both sample cases end to end |
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
