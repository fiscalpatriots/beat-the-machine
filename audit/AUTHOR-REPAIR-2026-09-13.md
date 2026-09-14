# Author page and custom-case repair, 13 September 2026

Lane R3, written at 8:58 PM EDT. The source is section 5 of the third independent review, run
against public product 1.6.1 at `b6ba468`. The later director items (the codename wording, the
two form switches, the ledger-only picks and the written explanations) are in sections 7 to 10.

**How it was verified.** Every result below came from running the pages, not from reading them.
Headless Chrome 152 ran over the DevTools protocol with its own throwaway profile, against a local
static server. The "before" runs used an untouched export of `b6ba468`, and the "after" runs used
the working tree. The drill ran in test mode the whole way, so nothing was posted. Downloads were
captured through `Browser.setDownloadBehavior`, so a saved file here is the real download. The
scripts are in `audit/author-repair-2026-09-13/`, and each one takes the tree to test as its first
argument:

| Script | What it proves |
| --- | --- |
| `review-steps.cjs <root> <label> <out.json>` | The review's README steps 1 to 9 on the author page, then a reread, a reconcile and a clean save |
| `parity-widths.cjs <root> <out.json>` | Author statuses against `checker.html` on the same inputs in the browser, the permitted-origin path, and overflow at 320, 375, 768 and 1280 |
| `parity-node.cjs <root>` | The author page's sentence fold run on the reader functions inside `checker.html`, compared with the checker's own `run()` on every plain fixture and on 13 probes |
| `walk-drill.cjs <root> <case> <width> <out.json>` | A clicked walk of the drill from intro to end, the explanation lock, the form payload and the record |

## 1. Repair A: the author page holds what the checker holds

**Before (`b6ba468`).** The review's case was the rent ledger at 100,000 to 130,000, insurance at
50,000 to 95,000, and the memo "1. Rent expense did not increase by $30,000." followed by
"2. The bank covenant ratio was 7.2%." The readout printed "Every figure recomputes." and "Every
direction word agrees with the sign." The rent card suggested **stand**, **clean line** and "the
figure and reason hold", and gave "Every figure in this sentence ties, and every direction word
agrees with the sign." as its finding.

**After.** `foldSentence()` in `author.html` now carries a sentence through the checker's own
sequence: binding conflicts, duplicate account numbers, unconfirmed columns, unread spans, each
figure with its multi-account and negation holds, direction (bad, negated, not tied to a line),
threshold claims, and finally the rule that a sentence with nothing tested is not checked. A call
is suggested only when a sentence is checked within scope (stand) or failed (flag). A sentence that
needs review or was not checked gets no suggestion: the call, type and basis all start empty and the
card reads "suggested: none, the call is yours". Each of the two praise lines prints only when every
sentence is checked within scope.

The same case now reads:

- "2 memo sentences read: 0 checked within scope, 2 need review, 0 not checked, 0 failed."
- "Figures: 0 are checked within scope, 2 are held for review, 0 do not recompute."
- The rent card is **needs review** with no suggestion. It gives the checker's negation reason for `$30,000` and for the direction.
- The silent insurance line is **failed** and suggests flag, no explanation, which matches the checker's silence result.

**Parity.** The browser runs `author.html` and `checker.html` on the same inputs with the current
shared reader, `assets/second-pass-core.js`, as of R1's commit `d081409`:

| Input | Author | Checker |
| --- | --- | --- |
| Review case, two sentences | needs review, needs review | same |
| P05 "increased by $30,000 and doubled." | not checked | same |
| P13 "remained at $130,000." | failed | same |
| P23 "rose $30,000, or one and a half percent." | not checked | same |
| P25 Arabic-Indic digits | not checked | same |
| P30 control | checked within scope | same |
| P31 "declined" | failed | same |
| Wrong figure, two sentences | failed, checked within scope | same |
| Two accounts in one clause | failed | same |
| Threshold claim sentence | checked within scope | same |
| The Kestrel sample, six sentences | 1 checked, 2 not checked, 3 failed, 4 checked, 5 failed, 6 checked | same |

On all 11 inputs neither praise line printed unless every sentence was checked within scope, and no
card suggested a stand on an unsettled sentence. `parity-node.cjs` matched **220 of 220** inputs.
Before R1's last commit it found two differences (STILL12, STILL26), because R1 had added a
"direction word not tied to a line" hold. Commit `1fcedbd` mirrors that hold.

**Promise text.** The old line was "read it the way the checker does". It now says the page "reads
both with the checker's own reader and gives every sentence one of the checker's four statuses",
and that a sentence the checker would hold is held here too. **This stays true only while the fold
tracks `run()` in `checker.html`.** Whoever changes the checker's status rules next should rerun
`parity-node.cjs`.

## 2. Repair B: stale saves are impossible

**Before.** README step 6 changed rent to 230000 without pressing Read it, and step 7 pressed Save.
Save stayed enabled, the page said "Saved. 2 lines.", and `excluded-review-test-v1.json` downloaded
with `130000` and the stand key. That is the same defect as the review's retained file.

**After.**

- A read is stamped with the ledger, the memo, the dollar floor, the percent floor, the rule and the zero-prior policy.
- Once any of them changes after Read it, both **Save** and **Preview** are disabled. Two notices appear: "Changed since the last read." under Read it, and the reason beside Save.
- In the review's step 7, clicking Save did nothing and downloaded nothing. Calling the page's own `__SPA.save()` directly was also refused ("The ledger, the memo or the threshold changed after Read it."), again with no download.
- Pressing Read it again carries the author's own work forward. A line whose figures, checker status or threshold moved is marked: "Changed on this read: 6100 read $100,000 to $130,000 before and reads $100,000 to $230,000 now". That line holds the save until "The key holds on this read" is clicked.
- After confirming, the save downloaded a file whose ledger reads `100000, 230000`, with `case.source.version` `src-hwdwet-201`. That equals the stamp of the inputs on screen at that moment.
- A saved file now carries `sourceVersion`, and each case carries `source`. `source` holds `version`, `readAt`, `policy`, `ledgerText`, `memoText`, `ledger` (the figures read), `silent` and `sentences`. Each sentence records its checker status, account, card number, suggestion, `confirmedAfterChange` and any `excluded` reason.

## 3. Repair C: every sentence is accounted for

**Before.** The covenant sentence got no card, and the page said only "1 memo sentence binds to no
ledger line and gets no card." The save went through with two cards anyway.

**After.**

- The covenant sentence comes back as an open item under Key each line, with the checker's status (**needs review**) and its reasons.
- The item offers **Still open** or **Leave it out of the drill**. While it is open the save lists: "Main set, sentence 2 ... binds to no ledger line and is still open."
- Leaving it out with no reason written is refused by `itemProblems()`. That one path was read in the code but not driven by the scripts.
- With a reason written, the save goes through, and `source.sentences[1].excluded` carries that reason.
- The memo hint no longer promises one card per sentence. It says every sentence comes back as a card, or as an open item that is left out with a reason or rewritten and read again.

## 4. Repair D: the origin is recorded and the drill repeats it

**Before.** The drill intro for `?case=own` read "Excluded review test is a made-up company." no
matter where the figures came from.

**After.** The case section asks "Where the figures come from" and offers **Made up for this
drill** or **A real close, used with permission**. Neither is preselected. A real close also needs
the line "Who gave permission, and for what use".

- Save is refused without a choice, and refused for a real close without the permission line.
- The choice is saved as `origin` in the file and as `case.origin` in each case.
- The Kestrel sample button sets the made-up choice.

The drill intro for an own case now follows the choice:

- **Made up:** "Excluded review test is a made-up company, written for this drill. The memo is the commentary drafted about its ledger, and the person who built the case keyed each line."
- **Real close:** "Permitted origin test is a real close, used here with permission. ..."
- **No origin, a file saved before this build:** "... a case saved from the author page, which did not record whether its figures are made up or real."

The round two bridge follows the same choice. Halyard, Kestrel and Brightwater keep their original
text word for word.

## 5. Repair E: not done

"Open a saved case" was not built. The token cap went to A to D and the two director items that
were ranked ahead of it. The saved file does now carry `ledgerText`, `memoText`, the policy, the
origin and every key, so the control only has to read them back.

## 6. Widths

`parity-widths.cjs` loaded the author page with every new element showing at once:

- the origin control, with the permission field open
- the stale notice and the save gate
- a reconcile block
- an open item with its reason box
- the fresh set, opened

It also loaded the drill intro on the own case. **At 320, 375, 768 and 1280 the document width
equaled the viewport, and no element overflowed on either page.** The 320 screenshot was checked by
eye: the origin labels and the item control wrap inside their halves.

`walk-drill.cjs` walked Halyard at 320 with Brightwater as the fresh case. Every screen stayed clean,
including all five assessment cards with the three explanation boxes open.

## 7. Director item: the codename screen

The screen promised a leaderboard, and the site has none. It now reads "A codename labels your run
in the results without putting your name on it." and "A codename for your run record, and the
chapters you belong to." Commit `052fd1f`.

`FACILITATOR-GUIDE.md` line 60 still says "A rule makes the leaderboard readable". That belongs to
the materials lane.

## 8. Director item: the two switches, left as they are

| Setting | What it does today | The one-line change, and what it waits on |
| --- | --- | --- |
| `RECEIPT_ENDPOINT = ""` (index.html) | Empty, so a send posts only to the Google Form, which confirms nothing to the page. The record says "No receipt endpoint is set in this build", and no receipt is shown. | `var RECEIPT_ENDPOINT = "https://script.google.com/macros/s/<deployment id>/exec";`. It waits on Khaled deploying `receipts/Code.gs` and pasting its `/exec` URL. The record then goes to the endpoint first and the form post still follows. |
| `PLACEHOLDER_MODE = "numeric"` (index.html) | The four form questions the drill does not ask (expected quality, confidence before, close experience, final confidence) post the fixed values 3, 5, "Once or twice" and 5. The form marks them required, so they have to post something. The findings script must exclude them. | `var PLACEHOLDER_MODE = "empty";`. It waits on Khaled making those four questions optional in the form editor. After that the four fields post nothing. |

## 9. Director item: the ledger-only picks, removed and then restored

**What happened.** The picks were removed in `cc29007`. The director's gate arrived after that
commit, and the removal was reverted in `ea639f1`. Neither commit was pushed. The drill carries the
picks exactly as at `b6ba468`. The walk confirmed 14 chips on the orientation screen, and the form's
round one field posting `Prepicks: skipped.`.

**Why they came back.** The picks are the only point where a player decides before reading any
AI-drafted text.

- `roundOne()` builds the orientation screen from the ledger alone.
- `prepickBlock()` and `wirePrepicks()` record up to three accounts before a memo sentence appears.
- Every call is made in `callCard()`, which puts the memo sentence (the AI's claim) on the same screen as Let it stand and Flag it.
- The two-step lock (`select()`, a basis chip, then `lock()`) commits the call before `reveal()` shows the key. Brightwater holds all five reveals until the last call.
- The drill never shows a machine recommendation of stand or flag. The checker does not appear in it.
- So without the picks, every call is still committed before the key is revealed, but none is committed before the AI's text is read. The director has the three-line summary and the ruling is open.

**Requirement 4 of the build handoff** reads "Reuse commitment and response handling, with a
ledger-only judgment before the narrative". It is recorded as Done in
`audit/RELEASE-QA-2026-09-13.md`, row 4 of section 4.1 and the matching row near line 248, and the
evidence given there is the picks.

- **With the picks:** the requirement is met as written.
- **If a ruling removes them:** only the commitment half still holds, through the lock. The ledger-only judgment would go. The orientation screen would still show the full ledger before the first memo line, but that is reading, not a recorded judgment. The row would need to say so rather than stay Done.

**If the ruling removes the picks, these strings belong to other lanes:**

| File | Owner |
| --- | --- |
| `README.md` lines 200 to 206 ("The ledger-only picks") and line 758 | R4 |
| `audit/RELEASE-QA-2026-09-13.md` lines 90, 171 and 248 | QA record |
| `tools/findings.py` (`PREPICK_RE`, `parse_prepicks`, the `r1` column title "Round one free text (prepicks)", `r1.prepicks_given`), `tools/make-sample-csv.py`, `tools/findings-sample.csv`, `tools/FINDINGS-sample.md`, `tools/readout-fields-sample.json` | R2 |
| `drafts-2026-09-05-aina/CHATGPT-REVIEW-PACKET-2026-09-13.md` lines 26 and 43, `TRACTION-PUSH-rev1.md` lines 17 and 125 to 132, and the copy of `findings.py` there | Traction lane |

No mention was found in `FACILITATOR-GUIDE.md`, `FACILITATOR-ONE-PAGE.md` or `PROTOCOL.md`. If
the picks go, the form's round one field should post the note it carried before them: "Not
collected. The ledger screen is orientation only in this version."

## 10. Director item: written explanations on the Brightwater assessment

**What the player sees.** On every line of a fresh case run as an assessment, three short
answers are required before **Lock it in** becomes active, beside the chips:

1. **The decisive evidence**
2. **Why it matters for this period**
3. **The action or source request that follows**

On those lines the three boxes replace the optional "In your words" line. Each answer needs at least
three characters. Enter inside a box does not lock the call. The bridge screen names the three
prompts before the first line.

- The page does not score the answers. Points, rank and badges are unchanged: the walk scored 5 of 5 calls and 5 of 5 reasons as before.
- Halyard and Kestrel practice lines never ask. The walk's first Halyard record carries `writtenExplanationRequired: false`.
- An author-made fresh set saved as "All at the end" is also an assessment, so it asks as well.

Walked at 320: on all five items the lock was disabled with the boxes empty and enabled once they
were filled.

**Field names, for R2.**

| Where | Name and shape |
| --- | --- |
| Attempt record, each `responses[]` item (also the receipt body) | `writtenExplanationRequired` (boolean), and `writtenExplanation`: `{decisiveEvidence, periodRelevance, actionOrRequest}` on round two assessment items, `null` elsewhere. `caseVersion` on the same item reads `brightwater-v6`. |
| Attempt record, top level | `writtenExplanationPrompts`: `{version: "explain-2026-09-13", asked, decisiveEvidence, periodRelevance, actionOrRequest, scoring}`, where the last four hold the exact prompt wording |
| Form, question C (`entry.756559246`) | Already carries round two line by line, separated by ` \|\| `. Each line now reads `N: Basis: … \| Evidence: … \| Period: … \| Action: … \| Reason: … \| Key basis: …`, with `\|` and line breaks stripped from the player's text. The case version follows as before, as `case version brightwater-v6`. |
| Notice version | `notice-2026-09-13b`, because the collected-data sentence now names the written answers |

**Form question for Khaled's hands.** None is required, because question C carries the answers and
the form was not touched. If he wants them in a column of their own, the paragraph question to add
would read: "Round two written explanations (filled by the page, not by the player)". Its entry id
would then have to be added to `E` in `index.html`.

**`cases/brightwater-v6.json`** keeps v5's calls, error types, basis keys, memo sentences and figures.
The script that wrote it checked each of these against v5 and stops if any moved. The evidence now shows what each
document says and what is missing, and the reading of each document moved into that line's `why`:

| Line | Evidence change |
| --- | --- |
| 1 | Drops "Nothing on file states how many cases the surgical suite took in June or what those cases cost." |
| 2 | "The June payroll register is on file." and "The May payroll register and the June rate change report are on file." The excerpts still show $27,600 and $27,300, but the page no longer adds them up or says they are the whole movement. |
| 3 | Keeps the 31 May schedule excerpt and the missing June documents. Drops "It lists no plan that started in June." and "The 31 May schedule is the only plan document in the file, and it stops before the movement." |
| 4 | The missing production report keeps its fact and loses "so nothing states how much of the movement the two associates account for". The coaching line about the percentage leg goes; the policy excerpt stays. |
| 5 | The invoice and the subledger are named with their excerpts. The reconciliation and the dollar-leg coaching line moved to the reveal. |

The drill's `FRESH_FILE`, `build-cases.cjs` and the inline fallback now load v6, and
`node build-cases.cjs` passed its own checks.

**Still naming brightwater-v5 or the optional line, for the owning lanes.**

| Owner | Files |
| --- | --- |
| R1 | `checker.html`, `CHECKER.md`, `tests/checker-fixtures.json`, `build-checker-cases.cjs` |
| R2 | `tools/findings.py`, `tools/make-sample-csv.py`, `tools/tests/test_findings.py`, the samples, and the "Nobody used the optional line" sentence |
| R4 | `README.md` (lines 185 and 795 describe the optional line as the only free text), `cases/README.md`, `PROVENANCE.md`, `review.html` |
| Materials lane | `FACILITATOR-GUIDE.md` (line 136, and the case version), `FACILITATOR-ONE-PAGE.md` |
| No lane named | `RELEASE-NOTES.md`, `receipts/Code.gs` (sample `caseVersions`), `audit/PROMPT1-RERUN-2026-09-13.md`, `audit/RELEASE-QA-2026-09-13.md` |

## 11. Commits, local, not pushed

| Hash | Line |
| --- | --- |
| `052fd1f` | The author page holds what the checker holds, refuses stale saves, and records where a case comes from |
| `cc29007` | The ledger-only picks are gone from the drill |
| `ea639f1` | The ledger-only picks come back until the decide-first question is settled |
| `6447d97` | Every Brightwater call now needs a three-part written explanation, and the evidence stops pre-solving the line |
| `1fcedbd` | The author page holds a direction word the checker cannot tie to a line, as the checker now does |

## 12. For the freeze pass, by eye in a real browser

1. On `author.html`, run the review's README steps by hand. Watch Save and Preview grey out the moment rent changes. Then read the reconcile block and the open covenant item on a phone.
2. The origin control's two labels wrap inside their halves at 320. Check that they still read as two choices.
3. Play one Brightwater line on a phone with the keyboard up. The three boxes, the lock button and the sticky bars were measured, but never seen with an on-screen keyboard.
4. Open a case saved before this build in the drill. The intro should say its origin was not recorded.
5. Rerun `parity-node.cjs` after any later checker commit, because the author's promise depends on it.
