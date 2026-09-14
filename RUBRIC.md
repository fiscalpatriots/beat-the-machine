# Second Pass: Explanation Rubric

Version 1.1, 13 September 2026, with the same three criteria as version 1 and a scoring sheet that now marks short answers and keeps every cell as text. It applies to the five assessment lines of the fresh case from `brightwater-v6` onward, where every call carries a written explanation in three parts: the decisive evidence, why that evidence matters for this period, and the action or source request that follows. An independent educator will score each part 0, 1 or 2 against this page. No explanation has been scored yet. The script never scores an explanation, and the result will be reported apart from reason chip agreement, which only says whether the chips a player tapped fall inside the key's accepted categories.

The page will not lock a call until each part holds at least two words and eight letters or digits and is not a stock non-answer such as none, n/a or same as above. That is a floor against empty and placeholder answers, not a judgment of quality, so an answer that clears it can still earn a 0.

Score what the player wrote against what the case file puts on the page. Whether the call agreed with the key is not a criterion, and the sheet you score does not show it. An explanation that misstates the file cannot earn a 2 on any criterion it misstates.

## 1. Decisive evidence

Does the explanation name the document, figure or missing record in the file that decides the call?

| Score | What earns it | Anchor, line 2, hygienist wages, keyed let it stand |
| --- | --- | --- |
| 2 | Names the specific item that decides the call, as the file states it. | "The June payroll register pays A. Rivas $27,600 and D. Okafor $27,300, both hired 1 June for the second chair, and the May register with the June rate change report shows no other hygienist pay moved." |
| 1 | Points to the right kind of evidence without naming what it says, or names it with a material gap. | "Payroll is on file for the new hygienists." |
| 0 | Gives no evidence, relies on plausibility instead of the file, or cites something the file does not contain. | "Opening a second chair would obviously raise wages." |

On a flag line the decisive evidence is often an absence, and naming it earns the same credit. Line 1, dental supplies, at a 2: "The only document is the 1 June completion certificate for the surgical suite. No lab invoice summary, case mix report or implant count was supplied for May or June."

## 2. Why it matters for this period

Does the explanation connect the evidence to the month the memo sentence is about?

| Score | What earns it | Anchor, line 3, orthodontic plan revenue, keyed flag |
| --- | --- | --- |
| 2 | States how the evidence bears on the period the sentence covers, and what it can or cannot establish for that period. | "The schedule is dated 31 May and says it does not cover plans starting after 31 May, so it cannot show the thirty-one plans the memo says started in June." |
| 1 | Notices the date or the period but does not connect it to what the sentence claims. | "The schedule is from May, so it is out of date." |
| 0 | Says nothing about the period, or treats a document from another period as support for this one. | "The plan schedule is on file, so the new plans are documented." |

On a stand line the same criterion asks why the support belongs to this month. Line 2 at a 2: "Both hires start 1 June and are paid in the June register, and no rate change took effect in June, so the $54,900 belongs to June."

## 3. Action or source request

Does the explanation say what the reviewer does next and, where the call is a flag, which record would settle it?

| Score | What earns it | Anchor, line 4, patient service revenue, keyed flag |
| --- | --- | --- |
| 2 | States the action and names the record that would settle the question. | "Hold the sentence and ask the practice for a production report by provider for May and June, which would show what the two associates billed." |
| 1 | States an action without the record that would settle it. | "Ask the practice for more information about the new dentists." |
| 0 | States no action, or an action that would not resolve the question. | "Nothing to do, since the line fails the percentage leg and no commentary was owed." |

On a stand line the action is the sign-off and the record it rests on. Line 5, marketing and patient outreach, at a 2: "Let it stand. Invoice 20614 for the $5,700 mailer and the unchanged $18,400 of recurring spend in the June subledger make up the whole $24,100, so the sentence can be signed without a request."

## How to score

1. Run `python tools/findings.py responses.csv --scoring-sheet scoring-sheet.csv`. It writes the sheet and, beside it, a facilitator key ending `-facilitator-key.csv`. The facilitator keeps the key; the educator receives only the sheet.
2. The sheet carries `response_id`, `case_version`, `line`, `account`, `memo_sentence`, `participant_call`, the three written parts, `below_minimum` and `second_scorer`. It never carries the codename, the key, the call result, the chips or the chip agreement. A text cell that begins with =, +, -, @ or a tab carries a leading apostrophe, so a spreadsheet shows the answer as text instead of running it as a formula; the apostrophe is not part of what the player wrote.
3. `below_minimum` names any part that fell short of the page's floor, for a record the page could not have locked (an older build or an edited run), such as "why it matters for this period: a stock non-answer". Score that part as written, like any other. The column is there so a short answer is seen rather than dropped, and it does not set the score.
4. Read the case file named in `case_version` before scoring, so the file on the page is the one you score against.
5. Fill `score_evidence`, `score_period` and `score_action` with 0, 1 or 2, and `scorer` with your label. `key_disagreement` and `notes` are for your own words. Leave every other column as it is. A score outside 0, 1 and 2 leaves that row unscored.
6. The sheet is ordered by line, so score every response to one line before moving to the next. Do not open the facilitator key or the findings until scoring is finished.
7. Run `python tools/findings.py responses.csv --scores first.csv --second-scores second.csv` to put the results in the findings.

## Disagreements are recorded, never resolved by changing the key

**With the key.** When you believe the file supports a different call or a different reason than the key, write that in `key_disagreement` in your own words and score the explanation against the file as you read it. The key is not changed to fit the responses. The findings print every recorded disagreement word for word. The case owner reads them once scoring is complete, and any change to a call, a type or a basis key becomes a new case version with its reason in the change log, while records already filed stay scored against the version they carry.

**Between scorers.** Both scorers' numbers are kept as filed. The means in the findings come from the first scorer, and the second scorer's rows measure agreement: the share of criterion scores the two gave identically and the share within one point, on every row both scored. Scores are not averaged together or re-scored to a consensus. If the two scorers talk a row through afterwards, write the outcome in `notes` and leave both filed scores unchanged. Report the agreement beside the means, because a low figure is a finding about how clearly this rubric reads.

## How the second scorer's rows are drawn

Nobody chooses them. `findings.py` marks a response `yes` in `second_scorer` when the SHA-256 hash of `second-pass-rubric-v1|<response_id>` is divisible by five, which draws about one response in five, and then tops up every fresh line to at least two drawn responses, taking the lowest hashes first. A `response_id` is itself a hash of the attempt identifier, the case version and the line, so a response keeps its id and its draw when the sheet is rebuilt with later rows. A top-up can shift as rows are added, so draw once, when scoring starts, and keep that sheet.

Give the second scorer a copy of the blank sheet filtered to the rows marked `yes`, never the first scorer's filled copy, and have them score those rows independently under the same instructions.

## What these scores can support

Once an educator has scored them, they will describe how well participants explained their calls on five unseen items, judged against this rubric. They will be a separate result from reason chip agreement, and neither stands in for the other. With five items and no comparable baseline, they will not establish learning gain, professional competence or transfer to real review work.
