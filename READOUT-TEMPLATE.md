# Second Pass: Results Readout

One page a facilitator fills after a session, and one page for each case set the session played. Run `findings.py` against the downloaded responses, add `--roster` when you kept a consented roster, and copy its output in. The name in each cell is the field the script writes for it. The `run.` fields come from the Run block and every other field comes from the block headed by this page's case set, so a page is never filled from two case sets. A field the script prints as *not available*, or one listed under **Columns not found**, leaves its cell blank rather than estimated.

Session `run.generated`, file `run.source_file`, product `run.product_version`, evidence status `run.evidence_status`. Practice case `set.case_round1`, fresh case `set.case_round2`, key dated `set.key_date`.

## Counts, each defined once

| Count | Field | What it counts |
| --- | --- | --- |
| Rows in the export | `run.rows_in_export` | Every data row in the downloaded file. |
| Rows excluded | `run.rows_excluded` | Test codenames, rows the page marked as a test attempt, blank codenames and synthetic rows, each reason with its own `run.rows_excluded.` field. |
| Duplicate sends | `run.duplicate_sends_set_aside` | Rows that repeat an attempt identifier already read, so one attempt sent twice counts once. |
| Received attempts | `run.attempts_received` | The rows left after exclusions and duplicate sends, each one run of the drill. |
| Completed attempts | `run.attempts_completed` | Received attempts with a call on every practice line and, where a fresh case is named, on every fresh line. |
| Distinct codenames | `run.codenames_distinct` | Different codenames among received attempts. A codename is a pseudonym, so this count is never reported as a number of people. |
| Facilitator-confirmed participants | `run.participants_confirmed`, this case set `set.participants_confirmed` | Distinct participants on the consented roster with at least one received attempt. It stays blank when no roster was kept, and it is the only count on this page that may be called people. |
| First attempts | `run.first_attempts`, this case set `set.first_attempts` | The first eligible attempt by each codename, which is the only attempt any rate on this page reads. |
| Reattempts | `run.reattempts`, this case set `set.reattempts` | Later eligible attempts by a codename already counted. The findings list them in their own table and no rate here includes them. |
| Refused attempts | `run.attempts_refused` | Received attempts on a case version with no case file, or on an authored case, which are scored against nothing. |

Every rate is scored against the case file for the version the record names. A record on a version the script cannot read is refused rather than scored against another case's key.

## 1. First attempts by organization, fields carrying the prefix `org.`

A chip is what the player tapped about themselves, so one attempt can count under two chapters and a chip never confirms a role.

| Chapter `name` | First attempts `first_attempts` | Call agreement `call_agreement_mean` | Reason chip agreement `reason_agreement_mean` |
| --- | --- | --- | --- |
| Beta Alpha Psi | | | |
| ACFE | | | |
| ASM | | | |
| NABA | | | |
| AAA | | | |
| GMU Student | | | |
| Professor | | | |
| Outside Mason | | | |

## 2. Call agreement and reason chip agreement by error type, fields carrying the prefix `type.`

The lines come from the case set's own file, so copy `lines` rather than assuming Halyard's. A type this case set does not carry has no field and its row stays blank.

| Error type `name` | Lines `lines` | Seen `calls_seen` | Call agreement `call_agreement_rate` | Reason chip agreement `reason_agreement_rate` |
| --- | --- | --- | --- | --- |
| Arithmetic | | | | |
| Wrong direction | | | | |
| Timing | | | | |
| Unsupported driver | | | | |
| Unsupported attribution | | | | |
| Wrong account | | | | |
| No explanation | | | | |
| Clean line, the control | | | | |

## 3. False flags on the clean lines, fields carrying the prefix `falseflag.`

Clean lines on this case set `falseflag.lines`. One row per clean line, from `falseflag.line<N>.flags` and `falseflag.line<N>.rate`.

| Clean line | Flags | Share |
| --- | --- | --- |
| | | |
| All clean lines | `falseflag.flags` | `falseflag.overall_rate` |

First attempts with no false flag `falseflag.first_attempts_with_none`.

## 4. The fresh case, lines nobody had seen, fields carrying the prefix `fresh.`

| Fresh line `line<N>.name` | Keyed call `line<N>.key` | Call agreement `line<N>.call_agreement_rate` | Reason chip agreement `line<N>.reason_agreement_rate` |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

Fresh case `fresh.call_agreement_mean` and `fresh.reason_agreement_mean`, practice case `r1.call_agreement_mean` and `r1.reason_agreement_mean`. Median elapsed minutes on the page `r1.lap_median`, fresh case clock `fresh.seconds_median`.

## 5. Reason chip agreement, reported on its own

A reason agrees when at least one chip was tapped and every chip tapped sits inside the line's basis key. This is agreement with the accepted reason categories, and it is never reported as reasoning quality or as learning gain. The limit on this case set, as the script states it: `reason.limitation`.

## 6. Lines in the player's own words, quoted where the reason chips agreed with the key

| Codename `words.codename` | Line, type `words.line`, `words.type` | Quote `words.text` |
| --- | --- | --- |
| | | |

## The roster, when you keep one

A roster confirms people without adding accounts to the product. Write it after the session as a CSV with the columns `participant,codename,consent,role`, one row per codename a person used. `participant` is your own label, such as P01, and two codenames under one label count as one participant. `consent` must read yes for the row to be read at all. `role` is what you observed, such as student, practitioner or educator, and it is your record rather than anything the page asked. Keep names out of the file and keep the key from label to person with you.

## Reading these honestly

Every figure here is descriptive agreement with a key on one sitting, so report it as what this group called on these written lines and nothing more. The fresh lines are a second unseen item set scored the same way rather than a post-test, and with five items and no comparable baseline the gap between the two pairs separates two item sets rather than measuring learning, transfer or time saved. The findings print the page's rank beside each attempt, and a rank that leaves this page is a game rank, never a credential. A findings file stamped as a synthetic verification run never feeds this page. Write the case version and key date beside any number leaving this page, because a row scored against another version is not comparable.
