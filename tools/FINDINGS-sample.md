# Second Pass: Beat the Machine, findings

Built 2026-09-13 from `findings-sample.csv`.

## Attempts and people

| Count | Value | What it counts |
| --- | --- | --- |
| Rows in the export | 23 | Every data row in the file. |
| Rows excluded from participant evidence | 6 | Test codenames, rows the page marked as a test attempt, blank codenames and synthetic rows, itemized below. |
| Duplicate sends set aside | 1 | A row repeating an attempt identifier already read. One attempt sent twice counts once. |
| Received attempts | 16 | Rows left after those two steps. Each is one run of the drill. |
| Completed attempts | 15 | Received attempts with a call on every practice line and, where a fresh case is named, on every fresh line. |
| Distinct codenames | 15 | Different codenames among received attempts. A codename is a pseudonym, so this is not a count of people: one person can type two, and two people can type one. |
| Facilitator-confirmed participants | 8 | Distinct participants on the consented roster the facilitator supplied, each with at least one received attempt. |
| First attempts scored | 13 | The first eligible attempt per codename, by timestamp. Every rate in a case set block reads these. |
| Reattempts | 1 | Later eligible attempts by a codename already counted. Listed in the reattempt table and in no rate. |
| Attempts refused from scoring | 2 | Received attempts on a case version this script cannot score, itemized below. |

## Rows excluded from participant evidence

- Test codename: 4, TEST-AGENT-DELETE; Test Play; Test Harness; PLACEHOLDER-CHECK-DELETE
- Marked TEST ATTEMPT by the page: 1, FIELDCHECK
- Blank codename: 0
- Synthetic row, excluded by rule: 1, Synthetic same participant (codename says synthetic)
- Duplicate sends set aside: 1, TIEOUT (attempt att-tieout-01 sent again)

The synthetic rule matches the word synthetic in a codename, the marker "Synthetic test only" in any cell, and an attempt identifier beginning "audit-". The third independent review's synthetic records match it, so they cannot enter participant evidence from this script.

## Case versions

Every received attempt as its record names its cases. Each case set below is scored against its own case files, and a refused attempt is scored against nothing.

| Cases as recorded | Received attempts |
| --- | --- |
| halyard-v4 with brightwater-v5, dated 2026-09-13 | 9 |
| kestrel-v1 with brightwater-v5, dated 2026-09-13 | 2 |
| halyard-v4 with brightwater-v6, dated 2026-09-13 | 2 |
| halyard-v3 with brightwater-v2, dated 2026-09-12 | 1 |
| ridgeline-own-2 with brightwater-v5, dated 2026-09-13 | 1 |
| halyard-v9 with brightwater-v5, dated 2026-09-13 | 1 |

### Attempts refused from scoring

| Reason | Attempts |
| --- | --- |
| authored case own:Ridgeline:2 (ridgeline-own-2): its key lives in the author's browser, not in cases/, so it is not scored | 1 |
| unsupported case version halyard-v9: there is no cases/halyard-v9.json, so no key exists to score it against | 1 |

Refused: RIDGEWAY, OLDKEY.

This export holds four case sets. They are reported in separate blocks and no rate pools them.

## Roster

Read from `findings-sample-roster.csv`, the consented roster the facilitator supplied.

| Measure | Value |
| --- | --- |
| Roster rows | 11 |
| Rows without consent, not read | 1 |
| Facilitator-confirmed participants with a received attempt | 8 |
| Roster codenames with no received attempt | 1 |
| Received codenames not on the roster | 6 |
| Codenames claimed by two participants, not confirmed | 0 |

| Role, as the facilitator recorded it | Confirmed participants |
| --- | --- |
| student | 4 |
| practitioner | 2 |
| educator | 1 |
| role not recorded | 1 |

## Case set halyard-v4 with brightwater-v5

Scored against `cases/halyard-v4.json` and `cases/brightwater-v5.json` and no other key. Every rate in this block reads the first attempt by each codename on this case set, and reattempts stay in their own table.

### Paste into the write-up

Across eight first attempts on halyard-v4, reviewers caught 88 percent of the eight planted problems.
The wrong direction line was caught 100 percent, the no explanation line only 75 percent.
False flags on the six clean lines ran 25 percent.
On a company nobody had seen, calls agreed with the key 85 percent of the time (n=8).

(57 words)

One more sentence, on the reason chips, if the write-up has room for it:

A basis chip was tapped on 100 percent of the calls, and the chips agreed with the key's accepted reason categories on 76 percent of the lines scored, which is agreement with those categories rather than a measure of reasoning.

### Paste into the video script

Across eight first attempts on halyard-v4, six by confirmed participants, reviewers caught 88 percent of the planted problems, and on a company they had never seen their calls agreed with the key 85 percent of the time.

### First attempts

| Measure | Value |
| --- | --- |
| First attempts on this case set | 8 |
| Completed | 8 |
| Facilitator-confirmed participants | 6 |
| Reattempts on this case set, not in any rate | 1 |
| Mean call agreement, lines of 14 | 11.5 |
| Median call agreement, lines of 14 | 11.5 |
| Catch rate, 8 problem lines | 87.5% (56 of 64) |
| Correct let stand rate, 6 clean lines | 75.0% (36 of 48) |
| False flag rate | 25.0% (12 of 48) |
| Reason chip agreement, practice lines | 75.9% (85 of 112 scored) |
| Elapsed minutes on the page, median | 9.5 |
| Elapsed minutes on the page, mean | 9.0 |
| Best streak posted | 14 |
| First attempts that flagged every line | 1 |
| Calls carrying a basis chip | 100.0% (112 of 112) |
| Flags carrying a line of the player's own words | 23.5% (16 of 68) |
| First attempts with a basis chip on every line | 8 |

### By organization

The chapter chips a player tapped. One attempt can carry two, so these sum above the first attempt count, and a chip is a self-description rather than a confirmed role.

| Chapter | First attempts |
| --- | --- |
| ACFE | 5 |
| Beta Alpha Psi | 2 |
| GMU Student | 2 |
| NABA | 1 |
| AAA | 1 |
| Professor | 1 |
| ASM | 1 |

### Call agreement and reason chip agreement by error type

Two separate results. Call agreement is the flag or stand decision against the key. Reason chip agreement is whether the chips tapped fall inside the line's accepted reason categories.

| Error type | Lines | Calls seen | Call agreement | Reasons scored | Reason chip agreement |
| --- | --- | --- | --- | --- | --- |
| arithmetic | 1, 8 | 16 | 93.8% (15) | 16 | 81.2% (13) |
| wrong direction | 3 | 8 | 100.0% (8) | 8 | 100.0% (8) |
| timing | 2 | 8 | 87.5% (7) | 8 | 87.5% (7) |
| unsupported driver | 7, 14 | 16 | 87.5% (14) | 16 | 87.5% (14) |
| unsupported attribution | 12 | 8 | 75.0% (6) | 8 | 12.5% (1) |
| no explanation | 11 | 8 | 75.0% (6) | 8 | 75.0% (6) |
| clean line | 4, 5, 6, 9, 10, 13 | 48 | 75.0% (36) | 48 | 75.0% (36) |

### What reason chip agreement measures

A reason agrees when at least one chip was tapped and every chip tapped is in the line's basis key. It is agreement with accepted reason categories. It is not a measure of reasoning quality, and it is not evidence of learning gain.

On halyard-v4, seven of the eight flag lines accept "no source on file" and six of the six stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on thirteen of fourteen lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality.

On brightwater-v5, three of the three flag lines accept "no source on file" and two of the two stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on five of five lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality.

### The basis given, by error type

The share is of the calls on those lines that carried a chip at all, and a player may tap more than one chip, so a row can sum above 100 percent.

| Error type | Calls with a basis | Chips tapped |
| --- | --- | --- |
| arithmetic | 16 of 16 | figure does not tie 13 (81%); no source on file 4 (25%); the figure and reason hold 1 (6%) |
| no explanation | 8 of 8 | nothing written where owed 5 (62%); no source on file 2 (25%); the figure and reason hold 2 (25%) |
| timing | 8 of 8 | wrong period 6 (75%); no source on file 2 (25%); the figure and reason hold 1 (12%) |
| unsupported attribution | 8 of 8 | no source on file 6 (75%); wrong account 5 (62%); the figure and reason hold 2 (25%) |
| unsupported driver | 16 of 16 | no source on file 14 (88%); the figure and reason hold 2 (12%) |
| wrong direction | 8 of 8 | direction wrong 7 (88%); no source on file 2 (25%) |
| clean line | 48 of 48 | the figure and reason hold 36 (75%); no source on file 12 (25%) |

### In their own words

Verbatim, up to three per error type.

**arithmetic**

- "the subtraction does not tie to the ledger" (REDLINE, line 1, account 4200, called flag)
- "186 less 121 is 65, not 6.5" (BLUEBOOK, line 8, account 6400, called flag)
- "the subtraction does not tie to the ledger" (DEPOTNINE, line 1, account 4200, called flag)

**no explanation**

- "silence on 72,500" (REDLINE, line 11, account 6000, called flag)
- "silence on 72,500" (DEPOTNINE, line 11, account 6000, called flag)

**timing**

- "one program, two end dates" (REDLINE, line 2, account 6200, called flag)
- "one program, two end dates" (HARDCLOSE, line 2, account 6200, called flag)

**unsupported attribution**

- "ask for the billing bridge by customer" (FOOTNOTE, line 12, account 4000, called flag)

**unsupported driver**

- "no bridge behind the depot story" (REDLINE, line 7, account 4000, called flag)
- "nothing on file ties the ramp to the 372" (MARGINCALL, line 14, account 7100, called flag)

**wrong direction**

- "the word and the column point opposite ways" (BLUEBOOK, line 3, account 5100, called flag)
- "the word and the column point opposite ways" (HARDCLOSE, line 3, account 5100, called flag)

**clean line**

- "I wanted a document that was already on file" (TIEOUT, line 9, account 6100, called flag)
- "the percentage pulled me in" (FOOTNOTE, line 4, account 4100, called flag)
- "I wanted a document that was already on file" (FOOTNOTE, line 6, account 7400, called flag)

### By card

| Line | Account | Key | Error type | Seen | Call agreement | Flagged | Reason chip agreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4200 Freight billed to customers | flag | arithmetic | 8 | 100.0% (8) | 8 | 75.0% |
| 2 | 6200 Repairs and maintenance, depots | flag | timing | 8 | 87.5% (7) | 7 | 87.5% |
| 3 | 5100 Inbound freight | flag | wrong direction | 8 | 100.0% (8) | 8 | 100.0% |
| 4 | 4100 Service revenue, equipment maintenance | stand | clean line | 8 | 62.5% (5) | 3 | 62.5% |
| 5 | 6500 Professional fees | stand | clean line | 8 | 75.0% (6) | 2 | 75.0% |
| 6 | 7400 Inventory shrink adjustment | stand | clean line | 8 | 75.0% (6) | 2 | 75.0% |
| 7 | 4000 Product revenue, distribution | flag | unsupported driver | 8 | 100.0% (8) | 8 | 100.0% |
| 8 | 6400 Bad debt expense | flag | arithmetic | 8 | 87.5% (7) | 7 | 87.5% |
| 9 | 6100 Fleet fuel | stand | clean line | 8 | 75.0% (6) | 2 | 75.0% |
| 10 | 6300 Software subscriptions | stand | clean line | 8 | 87.5% (7) | 1 | 87.5% |
| 11 | 6000 Warehouse wages | flag | no explanation | 8 | 75.0% (6) | 6 | 75.0% |
| 12 | 4000 Product revenue, distribution | flag | unsupported attribution | 8 | 75.0% (6) | 6 | 12.5% |
| 13 | 5000 Cost of product sold | stand | clean line | 8 | 75.0% (6) | 2 | 75.0% |
| 14 | 7100 Interest expense | flag | unsupported driver | 8 | 75.0% (6) | 6 | 75.0% |

### The read before the draft, against the final calls

Descriptive agreement on a keyed exercise, first attempts only. The read is taken from the ledger alone before the AI draft is shown, and a tapped account reads as a flag on its lines. Each final call came after reading the draft, the file on the card and, in practice mode, the reveals of the lines before it, so a change toward the key is not credited to the draft alone. It is not a pre-test and post-test, and it is not a learning gain.

No first attempt on this case set carries the required read, so nothing is compared. First attempts left out: eight posted before the read was required.

### By first attempt

The game rank is the page's own label for its points, which include a bonus for agreeing reason chips. It is a game rank, not a credential or a measure of professional skill, and a row filed before the page posted it reads not posted.

| Codename | Call agreement of 14 | Reason chip agreement | Game rank | Minutes | Best streak | Flags | Cards with a chip | Chapters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REDLINE | 14 | 13 of 14 | Partner | 7 | 14 | 8 | 14 of 14 | ACFE |
| MARGINCALL | 13 | 12 of 14 | Manager | 6 | 11 | 9 | 14 of 14 | Professor, ACFE |
| BLUEBOOK | 12 | 11 of 14 | Manager | 11 | 8 | 6 | 14 of 14 | Beta Alpha Psi, ACFE |
| HARDCLOSE | 12 | 11 of 14 | Manager | 10 | 9 | 8 | 14 of 14 | ACFE, Beta Alpha Psi |
| TIEOUT | 11 | 10 of 14 | Senior | 13 | 6 | 7 | 14 of 14 | NABA |
| FOOTNOTE | 11 | 10 of 14 | Senior | 9 | 7 | 9 | 14 of 14 | AAA, GMU Student |
| DEPOTNINE | 11 | 11 of 14 | Senior | 12 | 5 | 7 | 14 of 14 | ASM, ACFE |
| SHOTGUN | 8 | 7 of 14 | Staff | 4 | 3 | 14 | 14 of 14 | GMU Student |

Flagged every line: SHOTGUN.

### The fresh case

Scored against `cases/brightwater-v5.json`, read out of question C.

| Measure | Value |
| --- | --- |
| First attempts with a fresh case result | 8 of 8 |
| Fresh case call agreement | 85.0% (34 of 40 calls) |
| Fresh case reason chip agreement, mean | 85.0% |
| Practice case call agreement, same attempts | 82.1% |
| Difference between the two item sets | +2.9 points |
| Fresh case clock, median seconds | 72.5 |

| Fresh line | Keyed call | Seen | Call agreement | Reason chip agreement |
| --- | --- | --- | --- | --- |
| 1 Dental supplies and lab fees | flag | 8 | 100.0% | 100.0% |
| 2 Hygienist wages | stand | 8 | 87.5% | 87.5% |
| 3 Orthodontic plan revenue | flag | 8 | 87.5% | 87.5% |
| 4 Patient service revenue, net | flag | 8 | 87.5% | 87.5% |
| 5 Marketing and patient outreach | stand | 8 | 62.5% | 62.5% |

The fresh lines are a second unseen item set scored the same way, not a post-test. With five items and no comparable baseline, the difference above separates two item sets and does not establish learning gain, transfer or time saved.

| Fresh line error type | Chips tapped |
| --- | --- |
| unsupported driver | no source on file 22; the figure and reason hold 2 |
| clean line | the figure and reason hold 12; no source on file 4 |

### Educator-scored explanations

A separate result from reason chip agreement. Each written explanation on a fresh line is scored by an independent educator against RUBRIC.md, three criteria at 0 to 2 each, and never by this script. The machine's call result and the chips are kept off the sheet the educator scores.

No written explanation was found on the 40 fresh calls of these first attempts on brightwater-v5. Fresh cases before brightwater-v6 did not ask for one, and on brightwater-v6 or later an empty result means the export lacks the Evidence, Period and Action segments in question C.

### The Professor chip

First attempts carrying the Professor chip, a self-selected chip rather than a confirmed role: 1 (MARGINCALL). Mean call agreement 13.0 of 14, catch rate 100.0% on the 8 problem lines.

### Where the record disagrees with itself

Every rate above uses the key in `cases/halyard-v4.json`. Each line below is a place where the record the page wrote says something different, which is worth reading before any number leaves this page.

- HARDCLOSE line 7: Why says flag, the Accept or Reject column says stand

## Case set halyard-v4 with brightwater-v6

Scored against `cases/halyard-v4.json` and `cases/brightwater-v6.json` and no other key. Every rate in this block reads the first attempt by each codename on this case set, and reattempts stay in their own table.

### Paste into the write-up

Across two first attempts on halyard-v4, reviewers caught 81 percent of the eight planted problems.
The unsupported driver line was caught 100 percent, the no explanation line only 50 percent.
False flags on the six clean lines ran 0 percent.
On a company nobody had seen, calls agreed with the key 90 percent of the time (n=2).

(57 words)

One more sentence, on the reason chips, if the write-up has room for it:

A basis chip was tapped on 100 percent of the calls, and the chips agreed with the key's accepted reason categories on 86 percent of the lines scored, which is agreement with those categories rather than a measure of reasoning.

### Paste into the video script

Across two first attempts on halyard-v4, two by confirmed participants, reviewers caught 81 percent of the planted problems, and on a company they had never seen their calls agreed with the key 90 percent of the time.

### First attempts

| Measure | Value |
| --- | --- |
| First attempts on this case set | 2 |
| Completed | 2 |
| Facilitator-confirmed participants | 2 |
| Reattempts on this case set, not in any rate | 0 |
| Mean call agreement, lines of 14 | 12.5 |
| Median call agreement, lines of 14 | 12.5 |
| Catch rate, 8 problem lines | 81.2% (13 of 16) |
| Correct let stand rate, 6 clean lines | 100.0% (12 of 12) |
| False flag rate | 0.0% (0 of 12) |
| Reason chip agreement, practice lines | 85.7% (24 of 28 scored) |
| Elapsed minutes on the page, median | 17.5 |
| Elapsed minutes on the page, mean | 17.5 |
| Best streak posted | 10 |
| First attempts that flagged every line | 0 |
| Calls carrying a basis chip | 100.0% (28 of 28) |
| Flags carrying a line of the player's own words | 23.1% (3 of 13) |
| First attempts with a basis chip on every line | 2 |

### By organization

The chapter chips a player tapped. One attempt can carry two, so these sum above the first attempt count, and a chip is a self-description rather than a confirmed role.

| Chapter | First attempts |
| --- | --- |
| Beta Alpha Psi | 1 |
| Outside Mason | 1 |

### Call agreement and reason chip agreement by error type

Two separate results. Call agreement is the flag or stand decision against the key. Reason chip agreement is whether the chips tapped fall inside the line's accepted reason categories.

| Error type | Lines | Calls seen | Call agreement | Reasons scored | Reason chip agreement |
| --- | --- | --- | --- | --- | --- |
| arithmetic | 1, 8 | 4 | 100.0% (4) | 4 | 100.0% (4) |
| wrong direction | 3 | 2 | 50.0% (1) | 2 | 50.0% (1) |
| timing | 2 | 2 | 100.0% (2) | 2 | 100.0% (2) |
| unsupported driver | 7, 14 | 4 | 100.0% (4) | 4 | 100.0% (4) |
| unsupported attribution | 12 | 2 | 50.0% (1) | 2 | 0.0% (0) |
| no explanation | 11 | 2 | 50.0% (1) | 2 | 50.0% (1) |
| clean line | 4, 5, 6, 9, 10, 13 | 12 | 100.0% (12) | 12 | 100.0% (12) |

### What reason chip agreement measures

A reason agrees when at least one chip was tapped and every chip tapped is in the line's basis key. It is agreement with accepted reason categories. It is not a measure of reasoning quality, and it is not evidence of learning gain.

On halyard-v4, seven of the eight flag lines accept "no source on file" and six of the six stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on thirteen of fourteen lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality.

On brightwater-v6, three of the three flag lines accept "no source on file" and two of the two stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on five of five lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality.

### The basis given, by error type

The share is of the calls on those lines that carried a chip at all, and a player may tap more than one chip, so a row can sum above 100 percent.

| Error type | Calls with a basis | Chips tapped |
| --- | --- | --- |
| arithmetic | 4 of 4 | figure does not tie 4 (100%) |
| no explanation | 2 of 2 | nothing written where owed 1 (50%); the figure and reason hold 1 (50%) |
| timing | 2 of 2 | wrong period 2 (100%) |
| unsupported attribution | 2 of 2 | the figure and reason hold 1 (50%); wrong account 1 (50%); no source on file 1 (50%) |
| unsupported driver | 4 of 4 | no source on file 4 (100%) |
| wrong direction | 2 of 2 | direction wrong 1 (50%); the figure and reason hold 1 (50%) |
| clean line | 12 of 12 | the figure and reason hold 12 (100%) |

### In their own words

Verbatim, up to three per error type.

**arithmetic**

- "the subtraction does not tie to the ledger" (COLDREAD, line 1, account 4200, called flag)

**timing**

- "one program, two end dates" (SIGNOFF, line 2, account 6200, called flag)

**wrong direction**

- "the word and the column point opposite ways" (COLDREAD, line 3, account 5100, called flag)

### By card

| Line | Account | Key | Error type | Seen | Call agreement | Flagged | Reason chip agreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4200 Freight billed to customers | flag | arithmetic | 2 | 100.0% (2) | 2 | 100.0% |
| 2 | 6200 Repairs and maintenance, depots | flag | timing | 2 | 100.0% (2) | 2 | 100.0% |
| 3 | 5100 Inbound freight | flag | wrong direction | 2 | 50.0% (1) | 1 | 50.0% |
| 4 | 4100 Service revenue, equipment maintenance | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 5 | 6500 Professional fees | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 6 | 7400 Inventory shrink adjustment | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 7 | 4000 Product revenue, distribution | flag | unsupported driver | 2 | 100.0% (2) | 2 | 100.0% |
| 8 | 6400 Bad debt expense | flag | arithmetic | 2 | 100.0% (2) | 2 | 100.0% |
| 9 | 6100 Fleet fuel | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 10 | 6300 Software subscriptions | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 11 | 6000 Warehouse wages | flag | no explanation | 2 | 50.0% (1) | 1 | 50.0% |
| 12 | 4000 Product revenue, distribution | flag | unsupported attribution | 2 | 50.0% (1) | 1 | 0.0% |
| 13 | 5000 Cost of product sold | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 14 | 7100 Interest expense | flag | unsupported driver | 2 | 100.0% (2) | 2 | 100.0% |

### The read before the draft, against the final calls

Descriptive agreement on a keyed exercise, first attempts only. The read is taken from the ledger alone before the AI draft is shown, and a tapped account reads as a flag on its lines. Each final call came after reading the draft, the file on the card and, in practice mode, the reveals of the lines before it, so a change toward the key is not credited to the draft alone. It is not a pre-test and post-test, and it is not a learning gain.

| Measure | Value |
| --- | --- |
| First attempts with the required read | 2 of 2 |
| First attempts whose final calls moved off the read on at least one line | 100.0% (2 of 2) |
| Lines where the final call moved off the read | 28.6% (8 of 28 lines compared) |
| Of those, changed toward the key | 100.0% (8 of 8) |
| Of those, changed away from the key | 0.0% (0 of 8) |
| Lines where the final call held the read | 20 |

| Line | Account | Key | Error type | Compared | Tapped before the draft | Held | Toward the key | Away from the key |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4200 Freight billed to customers | flag | arithmetic | 2 | 1 | 1 | 1 | 0 |
| 2 | 6200 Repairs and maintenance, depots | flag | timing | 2 | 1 | 1 | 1 | 0 |
| 3 | 5100 Inbound freight | flag | wrong direction | 2 | 0 | 1 | 1 | 0 |
| 4 | 4100 Service revenue, equipment maintenance | stand | clean line | 2 | 0 | 2 | 0 | 0 |
| 5 | 6500 Professional fees | stand | clean line | 2 | 0 | 2 | 0 | 0 |
| 6 | 7400 Inventory shrink adjustment | stand | clean line | 2 | 0 | 2 | 0 | 0 |
| 7 | 4000 Product revenue, distribution | flag | unsupported driver | 2 | 1 | 1 | 1 | 0 |
| 8 | 6400 Bad debt expense | flag | arithmetic | 2 | 0 | 0 | 2 | 0 |
| 9 | 6100 Fleet fuel | stand | clean line | 2 | 0 | 2 | 0 | 0 |
| 10 | 6300 Software subscriptions | stand | clean line | 2 | 0 | 2 | 0 | 0 |
| 11 | 6000 Warehouse wages | flag | no explanation | 2 | 1 | 2 | 0 | 0 |
| 12 | 4000 Product revenue, distribution | flag | unsupported attribution | 2 | 1 | 2 | 0 | 0 |
| 13 | 5000 Cost of product sold | stand | clean line | 2 | 0 | 2 | 0 | 0 |
| 14 | 7100 Interest expense | flag | unsupported driver | 2 | 0 | 0 | 2 | 0 |

### By first attempt

The game rank is the page's own label for its points, which include a bonus for agreeing reason chips. It is a game rank, not a credential or a measure of professional skill, and a row filed before the page posted it reads not posted.

| Codename | Call agreement of 14 | Reason chip agreement | Game rank | Minutes | Best streak | Flags | Cards with a chip | Chapters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COLDREAD | 13 | 13 of 14 | Manager | 16 | 10 | 7 | 14 of 14 | Beta Alpha Psi |
| SIGNOFF | 12 | 11 of 14 | Manager | 19 | 7 | 6 | 14 of 14 | Outside Mason |

### The fresh case

Scored against `cases/brightwater-v6.json`, read out of question C.

| Measure | Value |
| --- | --- |
| First attempts with a fresh case result | 2 of 2 |
| Fresh case call agreement | 90.0% (9 of 10 calls) |
| Fresh case reason chip agreement, mean | 90.0% |
| Practice case call agreement, same attempts | 89.3% |
| Difference between the two item sets | +0.7 points |
| Fresh case clock, median seconds | 236 |

| Fresh line | Keyed call | Seen | Call agreement | Reason chip agreement |
| --- | --- | --- | --- | --- |
| 1 Dental supplies and lab fees | flag | 2 | 100.0% | 100.0% |
| 2 Hygienist wages | stand | 2 | 100.0% | 100.0% |
| 3 Orthodontic plan revenue | flag | 2 | 50.0% | 50.0% |
| 4 Patient service revenue, net | flag | 2 | 100.0% | 100.0% |
| 5 Marketing and patient outreach | stand | 2 | 100.0% | 100.0% |

The fresh lines are a second unseen item set scored the same way, not a post-test. With five items and no comparable baseline, the difference above separates two item sets and does not establish learning gain, transfer or time saved.

| Fresh line error type | Chips tapped |
| --- | --- |
| unsupported driver | no source on file 5; the figure and reason hold 1 |
| clean line | the figure and reason hold 4 |

### Educator-scored explanations

A separate result from reason chip agreement. Each written explanation on a fresh line is scored by an independent educator against RUBRIC.md, three criteria at 0 to 2 each, and never by this script. The machine's call result and the chips are kept off the sheet the educator scores.

| Measure | Value |
| --- | --- |
| Fresh lines carrying a written explanation | 10 |
| Fresh calls with no explanation text | 0 |
| Drawn for the second scorer | 10 |

Not scored yet. Write the sheet with --scoring-sheet, have the educator fill it, and run again with --scores.

### Where the record disagrees with itself

The Why fields, the Accept or Reject columns and the case files agree on every call on this case set.

## Case set kestrel-v1 with brightwater-v5

Scored against `cases/kestrel-v1.json` and `cases/brightwater-v5.json` and no other key. Every rate in this block reads the first attempt by each codename on this case set, and reattempts stay in their own table.

### Paste into the write-up

Across two first attempts on kestrel-v1, reviewers caught 86 percent of the seven planted problems.
The wrong direction line was caught 100 percent, the unsupported driver line only 50 percent.
False flags on the five clean lines ran 0 percent.
On a company nobody had seen, calls agreed with the key 90 percent of the time (n=2).

(57 words)

One more sentence, on the reason chips, if the write-up has room for it:

A basis chip was tapped on 100 percent of the calls, and the chips agreed with the key's accepted reason categories on 83 percent of the lines scored, which is agreement with those categories rather than a measure of reasoning.

### Paste into the video script

Across two first attempts on kestrel-v1, one by a confirmed participant, reviewers caught 86 percent of the planted problems, and on a company they had never seen their calls agreed with the key 90 percent of the time.

### First attempts

| Measure | Value |
| --- | --- |
| First attempts on this case set | 2 |
| Completed | 2 |
| Facilitator-confirmed participants | 1 |
| Reattempts on this case set, not in any rate | 0 |
| Mean call agreement, lines of 12 | 11.0 |
| Median call agreement, lines of 12 | 11 |
| Catch rate, 7 problem lines | 85.7% (12 of 14) |
| Correct let stand rate, 5 clean lines | 100.0% (10 of 10) |
| False flag rate | 0.0% (0 of 10) |
| Reason chip agreement, practice lines | 83.3% (20 of 24 scored) |
| Elapsed minutes on the page, median | 10 |
| Elapsed minutes on the page, mean | 10.0 |
| Best streak posted | 12 |
| First attempts that flagged every line | 0 |
| Calls carrying a basis chip | 100.0% (24 of 24) |
| Flags carrying a line of the player's own words | 33.3% (4 of 12) |
| First attempts with a basis chip on every line | 2 |

### By organization

The chapter chips a player tapped. One attempt can carry two, so these sum above the first attempt count, and a chip is a self-description rather than a confirmed role.

| Chapter | First attempts |
| --- | --- |
| Outside Mason | 1 |
| Beta Alpha Psi | 1 |

### Call agreement and reason chip agreement by error type

Two separate results. Call agreement is the flag or stand decision against the key. Reason chip agreement is whether the chips tapped fall inside the line's accepted reason categories.

| Error type | Lines | Calls seen | Call agreement | Reasons scored | Reason chip agreement |
| --- | --- | --- | --- | --- | --- |
| arithmetic | 1 | 2 | 100.0% (2) | 2 | 100.0% (2) |
| wrong direction | 2 | 2 | 100.0% (2) | 2 | 100.0% (2) |
| timing | 8 | 2 | 100.0% (2) | 2 | 100.0% (2) |
| unsupported driver | 4 | 2 | 50.0% (1) | 2 | 50.0% (1) |
| unsupported attribution | 6 | 2 | 100.0% (2) | 2 | 0.0% (0) |
| wrong account | 10 | 2 | 50.0% (1) | 2 | 50.0% (1) |
| no explanation | 12 | 2 | 100.0% (2) | 2 | 100.0% (2) |
| clean line | 3, 5, 7, 9, 11 | 10 | 100.0% (10) | 10 | 100.0% (10) |

### What reason chip agreement measures

A reason agrees when at least one chip was tapped and every chip tapped is in the line's basis key. It is agreement with accepted reason categories. It is not a measure of reasoning quality, and it is not evidence of learning gain.

On kestrel-v1, six of the seven flag lines accept "no source on file" and five of the five stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on eleven of twelve lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality.

On brightwater-v5, three of the three flag lines accept "no source on file" and two of the two stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on five of five lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality.

### The basis given, by error type

The share is of the calls on those lines that carried a chip at all, and a player may tap more than one chip, so a row can sum above 100 percent.

| Error type | Calls with a basis | Chips tapped |
| --- | --- | --- |
| arithmetic | 2 of 2 | figure does not tie 2 (100%) |
| no explanation | 2 of 2 | nothing written where owed 2 (100%) |
| timing | 2 of 2 | wrong period 2 (100%) |
| unsupported attribution | 2 of 2 | wrong account 2 (100%); no source on file 2 (100%) |
| unsupported driver | 2 of 2 | the figure and reason hold 1 (50%); no source on file 1 (50%) |
| wrong account | 2 of 2 | the figure and reason hold 1 (50%); wrong account 1 (50%) |
| wrong direction | 2 of 2 | direction wrong 2 (100%) |
| clean line | 10 of 10 | the figure and reason hold 10 (100%) |

### In their own words

Verbatim, up to three per error type.

**arithmetic**

- "the subtraction does not tie to the ledger" (LEDGERHAWK, line 1, account 6200, called flag)

**no explanation**

- "no sentence at all here" (LEDGERHAWK, line 12, account 4000, called flag)

**unsupported attribution**

- "ask for the billing bridge by customer" (QUICKTIE, line 6, account 4200, called flag)

**wrong direction**

- "it went up, not down" (LEDGERHAWK, line 2, account 5000, called flag)

### By card

| Line | Account | Key | Error type | Seen | Call agreement | Flagged | Reason chip agreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6200 Software licenses and hosting | flag | arithmetic | 2 | 100.0% (2) | 2 | 100.0% |
| 2 | 5000 Subcontracted engineering | flag | wrong direction | 2 | 100.0% (2) | 2 | 100.0% |
| 3 | 6400 Client acquisition costs | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 4 | 4100 Project and implementation revenue | flag | unsupported driver | 2 | 50.0% (1) | 1 | 50.0% |
| 5 | 6000 Salaries and wages | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 6 | 4200 Hardware and license resale | flag | unsupported attribution | 2 | 100.0% (2) | 2 | 0.0% |
| 7 | 5100 Hardware and license cost of resale | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 8 | 4100 Project and implementation revenue | flag | timing | 2 | 100.0% (2) | 2 | 100.0% |
| 9 | 6500 Insurance, cyber liability included | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 10 | 6300 Computer equipment | flag | wrong account | 2 | 50.0% (1) | 1 | 50.0% |
| 11 | 5200 Travel and onsite delivery | stand | clean line | 2 | 100.0% (2) | 0 | 100.0% |
| 12 | 4000 Recurring managed services | flag | no explanation | 2 | 100.0% (2) | 2 | 100.0% |

### The read before the draft, against the final calls

Descriptive agreement on a keyed exercise, first attempts only. The read is taken from the ledger alone before the AI draft is shown, and a tapped account reads as a flag on its lines. Each final call came after reading the draft, the file on the card and, in practice mode, the reveals of the lines before it, so a change toward the key is not credited to the draft alone. It is not a pre-test and post-test, and it is not a learning gain.

No first attempt on this case set carries the required read, so nothing is compared. First attempts left out: two posted before the read was required.

### By first attempt

The game rank is the page's own label for its points, which include a bonus for agreeing reason chips. It is a game rank, not a credential or a measure of professional skill, and a row filed before the page posted it reads not posted.

| Codename | Call agreement of 12 | Reason chip agreement | Game rank | Minutes | Best streak | Flags | Cards with a chip | Chapters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QUICKTIE | 12 | 11 of 12 | Partner | 9 | 12 | 7 | 12 of 12 | Beta Alpha Psi |
| LEDGERHAWK | 10 | 9 of 12 | Senior | 11 | 6 | 5 | 12 of 12 | Outside Mason |

### The fresh case

Scored against `cases/brightwater-v5.json`, read out of question C.

| Measure | Value |
| --- | --- |
| First attempts with a fresh case result | 2 of 2 |
| Fresh case call agreement | 90.0% (9 of 10 calls) |
| Fresh case reason chip agreement, mean | 90.0% |
| Practice case call agreement, same attempts | 91.7% |
| Difference between the two item sets | -1.7 points |
| Fresh case clock, median seconds | 75.5 |

| Fresh line | Keyed call | Seen | Call agreement | Reason chip agreement |
| --- | --- | --- | --- | --- |
| 1 Dental supplies and lab fees | flag | 2 | 100.0% | 100.0% |
| 2 Hygienist wages | stand | 2 | 100.0% | 100.0% |
| 3 Orthodontic plan revenue | flag | 2 | 50.0% | 50.0% |
| 4 Patient service revenue, net | flag | 2 | 100.0% | 100.0% |
| 5 Marketing and patient outreach | stand | 2 | 100.0% | 100.0% |

The fresh lines are a second unseen item set scored the same way, not a post-test. With five items and no comparable baseline, the difference above separates two item sets and does not establish learning gain, transfer or time saved.

| Fresh line error type | Chips tapped |
| --- | --- |
| unsupported driver | no source on file 5; the figure and reason hold 1 |
| clean line | the figure and reason hold 4 |

### Educator-scored explanations

A separate result from reason chip agreement. Each written explanation on a fresh line is scored by an independent educator against RUBRIC.md, three criteria at 0 to 2 each, and never by this script. The machine's call result and the chips are kept off the sheet the educator scores.

No written explanation was found on the 10 fresh calls of these first attempts on brightwater-v5. Fresh cases before brightwater-v6 did not ask for one, and on brightwater-v6 or later an empty result means the export lacks the Evidence, Period and Action segments in question C.

### Where the record disagrees with itself

The Why fields, the Accept or Reject columns and the case files agree on every call on this case set.

## Case set halyard-v3 with brightwater-v2

Scored against `cases/halyard-v3.json` and `cases/brightwater-v2.json` and no other key. Every rate in this block reads the first attempt by each codename on this case set, and reattempts stay in their own table.

### Paste into the write-up

Across one first attempt on halyard-v3, reviewers caught 62 percent of the eight planted problems, in a median of 15 minutes elapsed on the page.
They caught the unsupported attribution line 100 percent of the time and the wrong direction line only 0 percent.
False flags on the six clean lines ran 33 percent.

(54 words)

### Paste into the video script

Across one first attempt on halyard-v3, reviewers caught 62 percent of the planted problems and false flagged clean lines 33 percent of the time.

### First attempts

| Measure | Value |
| --- | --- |
| First attempts on this case set | 1 |
| Completed | 0 |
| Facilitator-confirmed participants | 0 |
| Reattempts on this case set, not in any rate | 0 |
| Mean call agreement, lines of 14 | 9.0 |
| Median call agreement, lines of 14 | 9 |
| Catch rate, 8 problem lines | 62.5% (5 of 8) |
| Correct let stand rate, 6 clean lines | 66.7% (4 of 6) |
| False flag rate | 33.3% (2 of 6) |
| Reason chip agreement, practice lines | n/a (0 of 0 scored) |
| Elapsed minutes on the page, median | 15 |
| Elapsed minutes on the page, mean | 15.0 |
| Best streak posted | 4 |
| First attempts that flagged every line | 0 |
| Calls carrying a basis chip | 0.0% (0 of 14) |
| Flags carrying a line of the player's own words | 0.0% (0 of 7) |
| First attempts with a basis chip on every line | 0 |

### By organization

The chapter chips a player tapped. One attempt can carry two, so these sum above the first attempt count, and a chip is a self-description rather than a confirmed role.

| Chapter | First attempts |
| --- | --- |
| Beta Alpha Psi | 1 |

### Call agreement and reason chip agreement by error type

Two separate results. Call agreement is the flag or stand decision against the key. Reason chip agreement is whether the chips tapped fall inside the line's accepted reason categories.

| Error type | Lines | Calls seen | Call agreement | Reasons scored | Reason chip agreement |
| --- | --- | --- | --- | --- | --- |
| arithmetic | 1, 8 | 2 | 50.0% (1) | 0 | n/a (0) |
| wrong direction | 3 | 1 | 0.0% (0) | 0 | n/a (0) |
| timing | 2 | 1 | 100.0% (1) | 0 | n/a (0) |
| unsupported driver | 7, 14 | 2 | 50.0% (1) | 0 | n/a (0) |
| unsupported attribution | 12 | 1 | 100.0% (1) | 0 | n/a (0) |
| no explanation | 11 | 1 | 100.0% (1) | 0 | n/a (0) |
| clean line | 4, 5, 6, 9, 10, 13 | 6 | 66.7% (4) | 0 | n/a (0) |

### What reason chip agreement measures

A reason agrees when at least one chip was tapped and every chip tapped is in the line's basis key. It is agreement with accepted reason categories. It is not a measure of reasoning quality, and it is not evidence of learning gain.

### The basis given, by error type

The share is of the calls on those lines that carried a chip at all, and a player may tap more than one chip, so a row can sum above 100 percent.

| Error type | Calls with a basis | Chips tapped |
| --- | --- | --- |
| arithmetic | 0 of 2 | none recorded |
| no explanation | 0 of 1 | none recorded |
| timing | 0 of 1 | none recorded |
| unsupported attribution | 0 of 1 | none recorded |
| unsupported driver | 0 of 2 | none recorded |
| wrong direction | 0 of 1 | none recorded |
| clean line | 0 of 6 | none recorded |

### In their own words

Nobody used the optional line of their own words on this case set.

### By card

| Line | Account | Key | Error type | Seen | Call agreement | Flagged | Reason chip agreement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4200 Freight billed to customers | flag | arithmetic | 1 | 0.0% (0) | 0 | n/a |
| 2 | 6200 Repairs and maintenance, depots | flag | timing | 1 | 100.0% (1) | 1 | n/a |
| 3 | 5100 Inbound freight | flag | wrong direction | 1 | 0.0% (0) | 0 | n/a |
| 4 | 4100 Service revenue, equipment maintenance | stand | clean line | 1 | 100.0% (1) | 0 | n/a |
| 5 | 6500 Professional fees | stand | clean line | 1 | 100.0% (1) | 0 | n/a |
| 6 | 7400 Inventory shrink adjustment | stand | clean line | 1 | 100.0% (1) | 0 | n/a |
| 7 | 4000 Product revenue, distribution | flag | unsupported driver | 1 | 0.0% (0) | 0 | n/a |
| 8 | 6400 Bad debt expense | flag | arithmetic | 1 | 100.0% (1) | 1 | n/a |
| 9 | 6100 Fleet fuel | stand | clean line | 1 | 100.0% (1) | 0 | n/a |
| 10 | 6300 Software subscriptions | stand | clean line | 1 | 0.0% (0) | 1 | n/a |
| 11 | 6000 Warehouse wages | flag | no explanation | 1 | 100.0% (1) | 1 | n/a |
| 12 | 4000 Product revenue, distribution | flag | unsupported attribution | 1 | 100.0% (1) | 1 | n/a |
| 13 | 5000 Cost of product sold | stand | clean line | 1 | 0.0% (0) | 1 | n/a |
| 14 | 7100 Interest expense | flag | unsupported driver | 1 | 100.0% (1) | 1 | n/a |

### The read before the draft, against the final calls

Descriptive agreement on a keyed exercise, first attempts only. The read is taken from the ledger alone before the AI draft is shown, and a tapped account reads as a flag on its lines. Each final call came after reading the draft, the file on the card and, in practice mode, the reveals of the lines before it, so a change toward the key is not credited to the draft alone. It is not a pre-test and post-test, and it is not a learning gain.

No first attempt on this case set carries the required read, so nothing is compared. First attempts left out: one with no read in the round one question.

### By first attempt

The game rank is the page's own label for its points, which include a bonus for agreeing reason chips. It is a game rank, not a credential or a measure of professional skill, and a row filed before the page posted it reads not posted.

| Codename | Call agreement of 14 | Reason chip agreement | Game rank | Minutes | Best streak | Flags | Cards with a chip | Chapters |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CARRYOVER | 9 | not scored | Staff | 15 | 4 | 7 | 0 of 14 | Beta Alpha Psi |

### The fresh case

No Round2 string in question C on these first attempts.

### Educator-scored explanations

A separate result from reason chip agreement. Each written explanation on a fresh line is scored by an independent educator against RUBRIC.md, three criteria at 0 to 2 each, and never by this script. The machine's call result and the chips are kept off the sheet the educator scores.

No written explanation was found on the 0 fresh calls of these first attempts on brightwater-v2. Fresh cases before brightwater-v6 did not ask for one, and on brightwater-v6 or later an empty result means the export lacks the Evidence, Period and Action segments in question C.

### Where the record disagrees with itself

The Why fields, the Accept or Reject columns and the case files agree on every call on this case set.

## Reattempts

Later attempts by a codename that already has a first attempt counted. They enter no rate above, because a player who has seen the reveal once answers with something the first attempt did not have.

| Codename | Attempt number | Case set | Timestamp | Call agreement | Reason chip agreement | Fresh case calls agreeing |
| --- | --- | --- | --- | --- | --- | --- |
| BLUEBOOK | 2 | halyard-v4 with brightwater-v5 | 2026/09/15 12:20:00 | 14 of 14 | 13 of 14 | 5 of 5 |

## The four questions that are not asked

Expected quality, confidence before the round, month end close experience and confidence after the round are never put to the player. Rows filed before 13 September 2026 carry fixed values that read like answers, and later rows carry the literal `not asked`. Neither is a player answer, so **none of these four columns enters any measure in this report**.

| Question | Sent as `not asked` | Fixed placeholder value | Something else | Blank |
| --- | --- | --- | --- | --- |
| Expected quality of the commentary | 15 | 1 | 0 | 0 |
| Confidence before the round | 15 | 1 | 0 | 0 |
| Month end close experience | 15 | 1 | 0 | 0 |
| Confidence after the round | 15 | 1 | 0 | 0 |

## Columns

Every question title matched a column in the export.


## Readout fields

Every name READOUT-TEMPLATE.md prints in a cell, with the value to copy into it. The `run.` fields fill the header once. Every other field belongs to one case set, so a readout is filled from one block below and never from two. A field reading *not available* stays blank on the readout rather than being estimated.

### Run

| Field | Value |
| --- | --- |
| `run.generated` | 2026-09-13 |
| `run.source_file` | findings-sample.csv |
| `run.evidence_status` | participant export |
| `run.product_version` | second-pass-drill 1.6.1 |
| `run.rows_in_export` | 23 |
| `run.rows_excluded` | 6 |
| `run.rows_excluded.test_codename` | 4 |
| `run.rows_excluded.marked_test_by_page` | 1 |
| `run.rows_excluded.blank_codename` | 0 |
| `run.rows_excluded.synthetic_by_rule` | 1 |
| `run.duplicate_sends_set_aside` | 1 |
| `run.attempts_received` | 16 |
| `run.attempts_completed` | 15 |
| `run.attempts_refused` | 2 |
| `run.codenames_distinct` | 15 |
| `run.participants_confirmed` | 8 |
| `run.first_attempts` | 13 |
| `run.reattempts` | 1 |
| `run.case_sets` | halyard-v4 with brightwater-v5 (8 first, 1 later); halyard-v4 with brightwater-v6 (2 first, 0 later); kestrel-v1 with brightwater-v5 (2 first, 0 later); halyard-v3 with brightwater-v2 (1 first, 0 later) |

### Case set halyard-v4 with brightwater-v5

| Field | Value |
| --- | --- |
| `set.case_round1` | halyard-v4 |
| `set.case_round2` | brightwater-v5 |
| `set.key_date` | 2026-09-13 |
| `set.first_attempts` | 8 |
| `set.first_attempts_completed` | 8 |
| `set.codenames` | 8 |
| `set.participants_confirmed` | 6 |
| `set.reattempts` | 1 |
| `org.beta-alpha-psi.name` | Beta Alpha Psi |
| `org.beta-alpha-psi.first_attempts` | 2 |
| `org.beta-alpha-psi.call_agreement_mean` | 85.7% |
| `org.beta-alpha-psi.reason_agreement_mean` | 78.6% |
| `org.acfe.name` | ACFE |
| `org.acfe.first_attempts` | 5 |
| `org.acfe.call_agreement_mean` | 88.6% |
| `org.acfe.reason_agreement_mean` | 82.9% |
| `org.asm.name` | ASM |
| `org.asm.first_attempts` | 1 |
| `org.asm.call_agreement_mean` | 78.6% |
| `org.asm.reason_agreement_mean` | 78.6% |
| `org.naba.name` | NABA |
| `org.naba.first_attempts` | 1 |
| `org.naba.call_agreement_mean` | 78.6% |
| `org.naba.reason_agreement_mean` | 71.4% |
| `org.aaa.name` | AAA |
| `org.aaa.first_attempts` | 1 |
| `org.aaa.call_agreement_mean` | 78.6% |
| `org.aaa.reason_agreement_mean` | 71.4% |
| `org.gmu-student.name` | GMU Student |
| `org.gmu-student.first_attempts` | 2 |
| `org.gmu-student.call_agreement_mean` | 67.9% |
| `org.gmu-student.reason_agreement_mean` | 60.7% |
| `org.professor.name` | Professor |
| `org.professor.first_attempts` | 1 |
| `org.professor.call_agreement_mean` | 92.9% |
| `org.professor.reason_agreement_mean` | 85.7% |
| `org.outside-mason.name` | Outside Mason |
| `org.outside-mason.first_attempts` | 0 |
| `org.outside-mason.call_agreement_mean` | not available |
| `org.outside-mason.reason_agreement_mean` | not available |
| `type.arithmetic.name` | Arithmetic |
| `type.arithmetic.lines` | 1, 8 |
| `type.arithmetic.calls_seen` | 16 |
| `type.arithmetic.call_agreement_rate` | 93.8% |
| `type.arithmetic.reason_agreement_rate` | 81.2% |
| `type.wrong-direction.name` | Wrong direction |
| `type.wrong-direction.lines` | 3 |
| `type.wrong-direction.calls_seen` | 8 |
| `type.wrong-direction.call_agreement_rate` | 100.0% |
| `type.wrong-direction.reason_agreement_rate` | 100.0% |
| `type.timing.name` | Timing |
| `type.timing.lines` | 2 |
| `type.timing.calls_seen` | 8 |
| `type.timing.call_agreement_rate` | 87.5% |
| `type.timing.reason_agreement_rate` | 87.5% |
| `type.unsupported-driver.name` | Unsupported driver |
| `type.unsupported-driver.lines` | 7, 14 |
| `type.unsupported-driver.calls_seen` | 16 |
| `type.unsupported-driver.call_agreement_rate` | 87.5% |
| `type.unsupported-driver.reason_agreement_rate` | 87.5% |
| `type.unsupported-attribution.name` | Unsupported attribution |
| `type.unsupported-attribution.lines` | 12 |
| `type.unsupported-attribution.calls_seen` | 8 |
| `type.unsupported-attribution.call_agreement_rate` | 75.0% |
| `type.unsupported-attribution.reason_agreement_rate` | 12.5% |
| `type.no-explanation.name` | No explanation |
| `type.no-explanation.lines` | 11 |
| `type.no-explanation.calls_seen` | 8 |
| `type.no-explanation.call_agreement_rate` | 75.0% |
| `type.no-explanation.reason_agreement_rate` | 75.0% |
| `type.clean-line.name` | Clean line, the control |
| `type.clean-line.lines` | 4, 5, 6, 9, 10, 13 |
| `type.clean-line.calls_seen` | 48 |
| `type.clean-line.call_agreement_rate` | 75.0% |
| `type.clean-line.reason_agreement_rate` | 75.0% |
| `falseflag.lines` | 4, 5, 6, 9, 10, 13 |
| `falseflag.line4.flags` | 3 |
| `falseflag.line4.rate` | 37.5% |
| `falseflag.line5.flags` | 2 |
| `falseflag.line5.rate` | 25.0% |
| `falseflag.line6.flags` | 2 |
| `falseflag.line6.rate` | 25.0% |
| `falseflag.line9.flags` | 2 |
| `falseflag.line9.rate` | 25.0% |
| `falseflag.line10.flags` | 1 |
| `falseflag.line10.rate` | 12.5% |
| `falseflag.line13.flags` | 2 |
| `falseflag.line13.rate` | 25.0% |
| `falseflag.flags` | 12 |
| `falseflag.overall_rate` | 25.0% |
| `falseflag.first_attempts_with_none` | 2 |
| `fresh.line1.name` | Dental supplies and lab fees |
| `fresh.line1.key` | Flag |
| `fresh.line1.calls_seen` | 8 |
| `fresh.line1.call_agreement_rate` | 100.0% |
| `fresh.line1.reason_agreement_rate` | 100.0% |
| `fresh.line2.name` | Hygienist wages |
| `fresh.line2.key` | Stand |
| `fresh.line2.calls_seen` | 8 |
| `fresh.line2.call_agreement_rate` | 87.5% |
| `fresh.line2.reason_agreement_rate` | 87.5% |
| `fresh.line3.name` | Orthodontic plan revenue |
| `fresh.line3.key` | Flag |
| `fresh.line3.calls_seen` | 8 |
| `fresh.line3.call_agreement_rate` | 87.5% |
| `fresh.line3.reason_agreement_rate` | 87.5% |
| `fresh.line4.name` | Patient service revenue, net |
| `fresh.line4.key` | Flag |
| `fresh.line4.calls_seen` | 8 |
| `fresh.line4.call_agreement_rate` | 87.5% |
| `fresh.line4.reason_agreement_rate` | 87.5% |
| `fresh.line5.name` | Marketing and patient outreach |
| `fresh.line5.key` | Stand |
| `fresh.line5.calls_seen` | 8 |
| `fresh.line5.call_agreement_rate` | 62.5% |
| `fresh.line5.reason_agreement_rate` | 62.5% |
| `fresh.first_attempts` | 8 |
| `fresh.call_agreement_mean` | 85.0% |
| `fresh.reason_agreement_mean` | 85.0% |
| `fresh.seconds_median` | 72.5 |
| `r1.call_agreement_mean` | 82.1% |
| `r1.reason_agreement_mean` | 75.9% |
| `r1.lap_median` | 9.5 |
| `reason.limitation` | On halyard-v4, seven of the eight flag lines accept "no source on file" and six of the six stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on thirteen of fourteen lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality. On brightwater-v5, three of the three flag lines accept "no source on file" and two of the two stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on five of five lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality. |
| `prepick.first_attempts_with_read` | 0 |
| `prepick.first_attempts_changed_any` | not available |
| `prepick.first_attempts_changed_any_rate` | not available |
| `prepick.lines_compared` | not available |
| `prepick.lines_changed` | not available |
| `prepick.lines_changed_rate` | not available |
| `prepick.changed_toward_key` | not available |
| `prepick.changed_toward_key_rate` | not available |
| `prepick.changed_away_from_key` | not available |
| `prepick.changed_away_from_key_rate` | not available |
| `prepick.lines_held` | not available |
| `prepick.first_attempts_before_required` | 8 |
| `prepick.first_attempts_read_after_a_call` | 0 |
| `explain.case_version` | brightwater-v5 |
| `explain.items_with_text` | 0 |
| `explain.fresh_calls_without_text` | 40 |
| `explain.items_scored` | 0 |
| `explain.evidence_avg_of_2` | not available |
| `explain.period_avg_of_2` | not available |
| `explain.action_avg_of_2` | not available |
| `explain.total_avg_of_6` | not available |
| `explain.second_scorer_drawn` | 0 |
| `explain.double_scored` | 0 |
| `explain.second_exact_agreement_rate` | not available |
| `explain.second_within_one_rate` | not available |
| `explain.key_disagreements_recorded` | 0 |

`words.` rows for halyard-v4 with brightwater-v5, lines in the player's own words where the reason chips agreed with the key

| `words.codename` | `words.line` | `words.type` | `words.text` |
| --- | --- | --- | --- |
| REDLINE | 1 | Arithmetic | the subtraction does not tie to the ledger |
| REDLINE | 2 | Timing | one program, two end dates |
| REDLINE | 7 | Unsupported driver | no bridge behind the depot story |
| REDLINE | 11 | No explanation | silence on 72,500 |
| BLUEBOOK | 3 | Wrong direction | the word and the column point opposite ways |
| BLUEBOOK | 8 | Arithmetic | 186 less 121 is 65, not 6.5 |
| MARGINCALL | 14 | Unsupported driver | nothing on file ties the ramp to the 372 |
| HARDCLOSE | 2 | Timing | one program, two end dates |
| HARDCLOSE | 3 | Wrong direction | the word and the column point opposite ways |
| DEPOTNINE | 1 | Arithmetic | the subtraction does not tie to the ledger |
| DEPOTNINE | 11 | No explanation | silence on 72,500 |

### Case set halyard-v4 with brightwater-v6

| Field | Value |
| --- | --- |
| `set.case_round1` | halyard-v4 |
| `set.case_round2` | brightwater-v6 |
| `set.key_date` | 2026-09-13 |
| `set.first_attempts` | 2 |
| `set.first_attempts_completed` | 2 |
| `set.codenames` | 2 |
| `set.participants_confirmed` | 2 |
| `set.reattempts` | 0 |
| `org.beta-alpha-psi.name` | Beta Alpha Psi |
| `org.beta-alpha-psi.first_attempts` | 1 |
| `org.beta-alpha-psi.call_agreement_mean` | 92.9% |
| `org.beta-alpha-psi.reason_agreement_mean` | 92.9% |
| `org.acfe.name` | ACFE |
| `org.acfe.first_attempts` | 0 |
| `org.acfe.call_agreement_mean` | not available |
| `org.acfe.reason_agreement_mean` | not available |
| `org.asm.name` | ASM |
| `org.asm.first_attempts` | 0 |
| `org.asm.call_agreement_mean` | not available |
| `org.asm.reason_agreement_mean` | not available |
| `org.naba.name` | NABA |
| `org.naba.first_attempts` | 0 |
| `org.naba.call_agreement_mean` | not available |
| `org.naba.reason_agreement_mean` | not available |
| `org.aaa.name` | AAA |
| `org.aaa.first_attempts` | 0 |
| `org.aaa.call_agreement_mean` | not available |
| `org.aaa.reason_agreement_mean` | not available |
| `org.gmu-student.name` | GMU Student |
| `org.gmu-student.first_attempts` | 0 |
| `org.gmu-student.call_agreement_mean` | not available |
| `org.gmu-student.reason_agreement_mean` | not available |
| `org.professor.name` | Professor |
| `org.professor.first_attempts` | 0 |
| `org.professor.call_agreement_mean` | not available |
| `org.professor.reason_agreement_mean` | not available |
| `org.outside-mason.name` | Outside Mason |
| `org.outside-mason.first_attempts` | 1 |
| `org.outside-mason.call_agreement_mean` | 85.7% |
| `org.outside-mason.reason_agreement_mean` | 78.6% |
| `type.arithmetic.name` | Arithmetic |
| `type.arithmetic.lines` | 1, 8 |
| `type.arithmetic.calls_seen` | 4 |
| `type.arithmetic.call_agreement_rate` | 100.0% |
| `type.arithmetic.reason_agreement_rate` | 100.0% |
| `type.wrong-direction.name` | Wrong direction |
| `type.wrong-direction.lines` | 3 |
| `type.wrong-direction.calls_seen` | 2 |
| `type.wrong-direction.call_agreement_rate` | 50.0% |
| `type.wrong-direction.reason_agreement_rate` | 50.0% |
| `type.timing.name` | Timing |
| `type.timing.lines` | 2 |
| `type.timing.calls_seen` | 2 |
| `type.timing.call_agreement_rate` | 100.0% |
| `type.timing.reason_agreement_rate` | 100.0% |
| `type.unsupported-driver.name` | Unsupported driver |
| `type.unsupported-driver.lines` | 7, 14 |
| `type.unsupported-driver.calls_seen` | 4 |
| `type.unsupported-driver.call_agreement_rate` | 100.0% |
| `type.unsupported-driver.reason_agreement_rate` | 100.0% |
| `type.unsupported-attribution.name` | Unsupported attribution |
| `type.unsupported-attribution.lines` | 12 |
| `type.unsupported-attribution.calls_seen` | 2 |
| `type.unsupported-attribution.call_agreement_rate` | 50.0% |
| `type.unsupported-attribution.reason_agreement_rate` | 0.0% |
| `type.no-explanation.name` | No explanation |
| `type.no-explanation.lines` | 11 |
| `type.no-explanation.calls_seen` | 2 |
| `type.no-explanation.call_agreement_rate` | 50.0% |
| `type.no-explanation.reason_agreement_rate` | 50.0% |
| `type.clean-line.name` | Clean line, the control |
| `type.clean-line.lines` | 4, 5, 6, 9, 10, 13 |
| `type.clean-line.calls_seen` | 12 |
| `type.clean-line.call_agreement_rate` | 100.0% |
| `type.clean-line.reason_agreement_rate` | 100.0% |
| `falseflag.lines` | 4, 5, 6, 9, 10, 13 |
| `falseflag.line4.flags` | 0 |
| `falseflag.line4.rate` | 0.0% |
| `falseflag.line5.flags` | 0 |
| `falseflag.line5.rate` | 0.0% |
| `falseflag.line6.flags` | 0 |
| `falseflag.line6.rate` | 0.0% |
| `falseflag.line9.flags` | 0 |
| `falseflag.line9.rate` | 0.0% |
| `falseflag.line10.flags` | 0 |
| `falseflag.line10.rate` | 0.0% |
| `falseflag.line13.flags` | 0 |
| `falseflag.line13.rate` | 0.0% |
| `falseflag.flags` | 0 |
| `falseflag.overall_rate` | 0.0% |
| `falseflag.first_attempts_with_none` | 2 |
| `fresh.line1.name` | Dental supplies and lab fees |
| `fresh.line1.key` | Flag |
| `fresh.line1.calls_seen` | 2 |
| `fresh.line1.call_agreement_rate` | 100.0% |
| `fresh.line1.reason_agreement_rate` | 100.0% |
| `fresh.line2.name` | Hygienist wages |
| `fresh.line2.key` | Stand |
| `fresh.line2.calls_seen` | 2 |
| `fresh.line2.call_agreement_rate` | 100.0% |
| `fresh.line2.reason_agreement_rate` | 100.0% |
| `fresh.line3.name` | Orthodontic plan revenue |
| `fresh.line3.key` | Flag |
| `fresh.line3.calls_seen` | 2 |
| `fresh.line3.call_agreement_rate` | 50.0% |
| `fresh.line3.reason_agreement_rate` | 50.0% |
| `fresh.line4.name` | Patient service revenue, net |
| `fresh.line4.key` | Flag |
| `fresh.line4.calls_seen` | 2 |
| `fresh.line4.call_agreement_rate` | 100.0% |
| `fresh.line4.reason_agreement_rate` | 100.0% |
| `fresh.line5.name` | Marketing and patient outreach |
| `fresh.line5.key` | Stand |
| `fresh.line5.calls_seen` | 2 |
| `fresh.line5.call_agreement_rate` | 100.0% |
| `fresh.line5.reason_agreement_rate` | 100.0% |
| `fresh.first_attempts` | 2 |
| `fresh.call_agreement_mean` | 90.0% |
| `fresh.reason_agreement_mean` | 90.0% |
| `fresh.seconds_median` | 236 |
| `r1.call_agreement_mean` | 89.3% |
| `r1.reason_agreement_mean` | 85.7% |
| `r1.lap_median` | 17.5 |
| `reason.limitation` | On halyard-v4, seven of the eight flag lines accept "no source on file" and six of the six stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on thirteen of fourteen lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality. On brightwater-v6, three of the three flag lines accept "no source on file" and two of the two stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on five of five lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality. |
| `prepick.first_attempts_with_read` | 2 |
| `prepick.first_attempts_changed_any` | 2 |
| `prepick.first_attempts_changed_any_rate` | 100.0% |
| `prepick.lines_compared` | 28 |
| `prepick.lines_changed` | 8 |
| `prepick.lines_changed_rate` | 28.6% |
| `prepick.changed_toward_key` | 8 |
| `prepick.changed_toward_key_rate` | 100.0% |
| `prepick.changed_away_from_key` | 0 |
| `prepick.changed_away_from_key_rate` | 0.0% |
| `prepick.lines_held` | 20 |
| `prepick.first_attempts_before_required` | 0 |
| `prepick.first_attempts_read_after_a_call` | 0 |
| `explain.case_version` | brightwater-v6 |
| `explain.items_with_text` | 10 |
| `explain.fresh_calls_without_text` | 0 |
| `explain.items_scored` | 0 |
| `explain.evidence_avg_of_2` | not available |
| `explain.period_avg_of_2` | not available |
| `explain.action_avg_of_2` | not available |
| `explain.total_avg_of_6` | not available |
| `explain.second_scorer_drawn` | 10 |
| `explain.double_scored` | 0 |
| `explain.second_exact_agreement_rate` | not available |
| `explain.second_within_one_rate` | not available |
| `explain.key_disagreements_recorded` | 0 |

`words.` rows for halyard-v4 with brightwater-v6, lines in the player's own words where the reason chips agreed with the key

| `words.codename` | `words.line` | `words.type` | `words.text` |
| --- | --- | --- | --- |
| COLDREAD | 1 | Arithmetic | the subtraction does not tie to the ledger |
| COLDREAD | 3 | Wrong direction | the word and the column point opposite ways |
| SIGNOFF | 2 | Timing | one program, two end dates |

### Case set kestrel-v1 with brightwater-v5

| Field | Value |
| --- | --- |
| `set.case_round1` | kestrel-v1 |
| `set.case_round2` | brightwater-v5 |
| `set.key_date` | 2026-09-13 |
| `set.first_attempts` | 2 |
| `set.first_attempts_completed` | 2 |
| `set.codenames` | 2 |
| `set.participants_confirmed` | 1 |
| `set.reattempts` | 0 |
| `org.beta-alpha-psi.name` | Beta Alpha Psi |
| `org.beta-alpha-psi.first_attempts` | 1 |
| `org.beta-alpha-psi.call_agreement_mean` | 100.0% |
| `org.beta-alpha-psi.reason_agreement_mean` | 91.7% |
| `org.acfe.name` | ACFE |
| `org.acfe.first_attempts` | 0 |
| `org.acfe.call_agreement_mean` | not available |
| `org.acfe.reason_agreement_mean` | not available |
| `org.asm.name` | ASM |
| `org.asm.first_attempts` | 0 |
| `org.asm.call_agreement_mean` | not available |
| `org.asm.reason_agreement_mean` | not available |
| `org.naba.name` | NABA |
| `org.naba.first_attempts` | 0 |
| `org.naba.call_agreement_mean` | not available |
| `org.naba.reason_agreement_mean` | not available |
| `org.aaa.name` | AAA |
| `org.aaa.first_attempts` | 0 |
| `org.aaa.call_agreement_mean` | not available |
| `org.aaa.reason_agreement_mean` | not available |
| `org.gmu-student.name` | GMU Student |
| `org.gmu-student.first_attempts` | 0 |
| `org.gmu-student.call_agreement_mean` | not available |
| `org.gmu-student.reason_agreement_mean` | not available |
| `org.professor.name` | Professor |
| `org.professor.first_attempts` | 0 |
| `org.professor.call_agreement_mean` | not available |
| `org.professor.reason_agreement_mean` | not available |
| `org.outside-mason.name` | Outside Mason |
| `org.outside-mason.first_attempts` | 1 |
| `org.outside-mason.call_agreement_mean` | 83.3% |
| `org.outside-mason.reason_agreement_mean` | 75.0% |
| `type.arithmetic.name` | Arithmetic |
| `type.arithmetic.lines` | 1 |
| `type.arithmetic.calls_seen` | 2 |
| `type.arithmetic.call_agreement_rate` | 100.0% |
| `type.arithmetic.reason_agreement_rate` | 100.0% |
| `type.wrong-direction.name` | Wrong direction |
| `type.wrong-direction.lines` | 2 |
| `type.wrong-direction.calls_seen` | 2 |
| `type.wrong-direction.call_agreement_rate` | 100.0% |
| `type.wrong-direction.reason_agreement_rate` | 100.0% |
| `type.timing.name` | Timing |
| `type.timing.lines` | 8 |
| `type.timing.calls_seen` | 2 |
| `type.timing.call_agreement_rate` | 100.0% |
| `type.timing.reason_agreement_rate` | 100.0% |
| `type.unsupported-driver.name` | Unsupported driver |
| `type.unsupported-driver.lines` | 4 |
| `type.unsupported-driver.calls_seen` | 2 |
| `type.unsupported-driver.call_agreement_rate` | 50.0% |
| `type.unsupported-driver.reason_agreement_rate` | 50.0% |
| `type.unsupported-attribution.name` | Unsupported attribution |
| `type.unsupported-attribution.lines` | 6 |
| `type.unsupported-attribution.calls_seen` | 2 |
| `type.unsupported-attribution.call_agreement_rate` | 100.0% |
| `type.unsupported-attribution.reason_agreement_rate` | 0.0% |
| `type.wrong-account.name` | Wrong account |
| `type.wrong-account.lines` | 10 |
| `type.wrong-account.calls_seen` | 2 |
| `type.wrong-account.call_agreement_rate` | 50.0% |
| `type.wrong-account.reason_agreement_rate` | 50.0% |
| `type.no-explanation.name` | No explanation |
| `type.no-explanation.lines` | 12 |
| `type.no-explanation.calls_seen` | 2 |
| `type.no-explanation.call_agreement_rate` | 100.0% |
| `type.no-explanation.reason_agreement_rate` | 100.0% |
| `type.clean-line.name` | Clean line, the control |
| `type.clean-line.lines` | 3, 5, 7, 9, 11 |
| `type.clean-line.calls_seen` | 10 |
| `type.clean-line.call_agreement_rate` | 100.0% |
| `type.clean-line.reason_agreement_rate` | 100.0% |
| `falseflag.lines` | 3, 5, 7, 9, 11 |
| `falseflag.line3.flags` | 0 |
| `falseflag.line3.rate` | 0.0% |
| `falseflag.line5.flags` | 0 |
| `falseflag.line5.rate` | 0.0% |
| `falseflag.line7.flags` | 0 |
| `falseflag.line7.rate` | 0.0% |
| `falseflag.line9.flags` | 0 |
| `falseflag.line9.rate` | 0.0% |
| `falseflag.line11.flags` | 0 |
| `falseflag.line11.rate` | 0.0% |
| `falseflag.flags` | 0 |
| `falseflag.overall_rate` | 0.0% |
| `falseflag.first_attempts_with_none` | 2 |
| `fresh.line1.name` | Dental supplies and lab fees |
| `fresh.line1.key` | Flag |
| `fresh.line1.calls_seen` | 2 |
| `fresh.line1.call_agreement_rate` | 100.0% |
| `fresh.line1.reason_agreement_rate` | 100.0% |
| `fresh.line2.name` | Hygienist wages |
| `fresh.line2.key` | Stand |
| `fresh.line2.calls_seen` | 2 |
| `fresh.line2.call_agreement_rate` | 100.0% |
| `fresh.line2.reason_agreement_rate` | 100.0% |
| `fresh.line3.name` | Orthodontic plan revenue |
| `fresh.line3.key` | Flag |
| `fresh.line3.calls_seen` | 2 |
| `fresh.line3.call_agreement_rate` | 50.0% |
| `fresh.line3.reason_agreement_rate` | 50.0% |
| `fresh.line4.name` | Patient service revenue, net |
| `fresh.line4.key` | Flag |
| `fresh.line4.calls_seen` | 2 |
| `fresh.line4.call_agreement_rate` | 100.0% |
| `fresh.line4.reason_agreement_rate` | 100.0% |
| `fresh.line5.name` | Marketing and patient outreach |
| `fresh.line5.key` | Stand |
| `fresh.line5.calls_seen` | 2 |
| `fresh.line5.call_agreement_rate` | 100.0% |
| `fresh.line5.reason_agreement_rate` | 100.0% |
| `fresh.first_attempts` | 2 |
| `fresh.call_agreement_mean` | 90.0% |
| `fresh.reason_agreement_mean` | 90.0% |
| `fresh.seconds_median` | 75.5 |
| `r1.call_agreement_mean` | 91.7% |
| `r1.reason_agreement_mean` | 83.3% |
| `r1.lap_median` | 10 |
| `reason.limitation` | On kestrel-v1, six of the seven flag lines accept "no source on file" and five of the five stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on eleven of twelve lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality. On brightwater-v5, three of the three flag lines accept "no source on file" and two of the two stand lines accept only "the figure and reason hold". A player who taps those two chips after correct calls agrees on five of five lines without stating why the evidence fails or holds, and the stand chip largely restates the decision. Read this result as agreement with accepted reason categories, not as reasoning quality. |
| `prepick.first_attempts_with_read` | 0 |
| `prepick.first_attempts_changed_any` | not available |
| `prepick.first_attempts_changed_any_rate` | not available |
| `prepick.lines_compared` | not available |
| `prepick.lines_changed` | not available |
| `prepick.lines_changed_rate` | not available |
| `prepick.changed_toward_key` | not available |
| `prepick.changed_toward_key_rate` | not available |
| `prepick.changed_away_from_key` | not available |
| `prepick.changed_away_from_key_rate` | not available |
| `prepick.lines_held` | not available |
| `prepick.first_attempts_before_required` | 2 |
| `prepick.first_attempts_read_after_a_call` | 0 |
| `explain.case_version` | brightwater-v5 |
| `explain.items_with_text` | 0 |
| `explain.fresh_calls_without_text` | 10 |
| `explain.items_scored` | 0 |
| `explain.evidence_avg_of_2` | not available |
| `explain.period_avg_of_2` | not available |
| `explain.action_avg_of_2` | not available |
| `explain.total_avg_of_6` | not available |
| `explain.second_scorer_drawn` | 0 |
| `explain.double_scored` | 0 |
| `explain.second_exact_agreement_rate` | not available |
| `explain.second_within_one_rate` | not available |
| `explain.key_disagreements_recorded` | 0 |

`words.` rows for kestrel-v1 with brightwater-v5, lines in the player's own words where the reason chips agreed with the key

| `words.codename` | `words.line` | `words.type` | `words.text` |
| --- | --- | --- | --- |
| LEDGERHAWK | 1 | Arithmetic | the subtraction does not tie to the ledger |
| LEDGERHAWK | 2 | Wrong direction | it went up, not down |
| LEDGERHAWK | 12 | No explanation | no sentence at all here |

### Case set halyard-v3 with brightwater-v2

| Field | Value |
| --- | --- |
| `set.case_round1` | halyard-v3 |
| `set.case_round2` | brightwater-v2 |
| `set.key_date` | 2026-09-12 |
| `set.first_attempts` | 1 |
| `set.first_attempts_completed` | 0 |
| `set.codenames` | 1 |
| `set.participants_confirmed` | 0 |
| `set.reattempts` | 0 |
| `org.beta-alpha-psi.name` | Beta Alpha Psi |
| `org.beta-alpha-psi.first_attempts` | 1 |
| `org.beta-alpha-psi.call_agreement_mean` | 64.3% |
| `org.beta-alpha-psi.reason_agreement_mean` | not available |
| `org.acfe.name` | ACFE |
| `org.acfe.first_attempts` | 0 |
| `org.acfe.call_agreement_mean` | not available |
| `org.acfe.reason_agreement_mean` | not available |
| `org.asm.name` | ASM |
| `org.asm.first_attempts` | 0 |
| `org.asm.call_agreement_mean` | not available |
| `org.asm.reason_agreement_mean` | not available |
| `org.naba.name` | NABA |
| `org.naba.first_attempts` | 0 |
| `org.naba.call_agreement_mean` | not available |
| `org.naba.reason_agreement_mean` | not available |
| `org.aaa.name` | AAA |
| `org.aaa.first_attempts` | 0 |
| `org.aaa.call_agreement_mean` | not available |
| `org.aaa.reason_agreement_mean` | not available |
| `org.gmu-student.name` | GMU Student |
| `org.gmu-student.first_attempts` | 0 |
| `org.gmu-student.call_agreement_mean` | not available |
| `org.gmu-student.reason_agreement_mean` | not available |
| `org.professor.name` | Professor |
| `org.professor.first_attempts` | 0 |
| `org.professor.call_agreement_mean` | not available |
| `org.professor.reason_agreement_mean` | not available |
| `org.outside-mason.name` | Outside Mason |
| `org.outside-mason.first_attempts` | 0 |
| `org.outside-mason.call_agreement_mean` | not available |
| `org.outside-mason.reason_agreement_mean` | not available |
| `type.arithmetic.name` | Arithmetic |
| `type.arithmetic.lines` | 1, 8 |
| `type.arithmetic.calls_seen` | 2 |
| `type.arithmetic.call_agreement_rate` | 50.0% |
| `type.arithmetic.reason_agreement_rate` | not available |
| `type.wrong-direction.name` | Wrong direction |
| `type.wrong-direction.lines` | 3 |
| `type.wrong-direction.calls_seen` | 1 |
| `type.wrong-direction.call_agreement_rate` | 0.0% |
| `type.wrong-direction.reason_agreement_rate` | not available |
| `type.timing.name` | Timing |
| `type.timing.lines` | 2 |
| `type.timing.calls_seen` | 1 |
| `type.timing.call_agreement_rate` | 100.0% |
| `type.timing.reason_agreement_rate` | not available |
| `type.unsupported-driver.name` | Unsupported driver |
| `type.unsupported-driver.lines` | 7, 14 |
| `type.unsupported-driver.calls_seen` | 2 |
| `type.unsupported-driver.call_agreement_rate` | 50.0% |
| `type.unsupported-driver.reason_agreement_rate` | not available |
| `type.unsupported-attribution.name` | Unsupported attribution |
| `type.unsupported-attribution.lines` | 12 |
| `type.unsupported-attribution.calls_seen` | 1 |
| `type.unsupported-attribution.call_agreement_rate` | 100.0% |
| `type.unsupported-attribution.reason_agreement_rate` | not available |
| `type.no-explanation.name` | No explanation |
| `type.no-explanation.lines` | 11 |
| `type.no-explanation.calls_seen` | 1 |
| `type.no-explanation.call_agreement_rate` | 100.0% |
| `type.no-explanation.reason_agreement_rate` | not available |
| `type.clean-line.name` | Clean line, the control |
| `type.clean-line.lines` | 4, 5, 6, 9, 10, 13 |
| `type.clean-line.calls_seen` | 6 |
| `type.clean-line.call_agreement_rate` | 66.7% |
| `type.clean-line.reason_agreement_rate` | not available |
| `falseflag.lines` | 4, 5, 6, 9, 10, 13 |
| `falseflag.line4.flags` | 0 |
| `falseflag.line4.rate` | 0.0% |
| `falseflag.line5.flags` | 0 |
| `falseflag.line5.rate` | 0.0% |
| `falseflag.line6.flags` | 0 |
| `falseflag.line6.rate` | 0.0% |
| `falseflag.line9.flags` | 0 |
| `falseflag.line9.rate` | 0.0% |
| `falseflag.line10.flags` | 1 |
| `falseflag.line10.rate` | 100.0% |
| `falseflag.line13.flags` | 1 |
| `falseflag.line13.rate` | 100.0% |
| `falseflag.flags` | 2 |
| `falseflag.overall_rate` | 33.3% |
| `falseflag.first_attempts_with_none` | 0 |
| `fresh.line1.name` | Dental supplies and lab fees |
| `fresh.line1.key` | Flag |
| `fresh.line1.calls_seen` | 0 |
| `fresh.line1.call_agreement_rate` | not available |
| `fresh.line1.reason_agreement_rate` | not available |
| `fresh.line2.name` | Patient service revenue, net |
| `fresh.line2.key` | Stand |
| `fresh.line2.calls_seen` | 0 |
| `fresh.line2.call_agreement_rate` | not available |
| `fresh.line2.reason_agreement_rate` | not available |
| `fresh.line3.name` | Orthodontic plan revenue |
| `fresh.line3.key` | Flag |
| `fresh.line3.calls_seen` | 0 |
| `fresh.line3.call_agreement_rate` | not available |
| `fresh.line3.reason_agreement_rate` | not available |
| `fresh.line4.name` | Marketing and patient outreach |
| `fresh.line4.key` | Stand |
| `fresh.line4.calls_seen` | 0 |
| `fresh.line4.call_agreement_rate` | not available |
| `fresh.line4.reason_agreement_rate` | not available |
| `fresh.line5.name` | Hygienist wages |
| `fresh.line5.key` | Flag |
| `fresh.line5.calls_seen` | 0 |
| `fresh.line5.call_agreement_rate` | not available |
| `fresh.line5.reason_agreement_rate` | not available |
| `fresh.first_attempts` | 0 |
| `fresh.call_agreement_mean` | not available |
| `fresh.reason_agreement_mean` | not available |
| `fresh.seconds_median` | not available |
| `r1.call_agreement_mean` | 64.3% |
| `r1.reason_agreement_mean` | not available |
| `r1.lap_median` | 15 |
| `reason.limitation` | not available |
| `prepick.first_attempts_with_read` | 0 |
| `prepick.first_attempts_changed_any` | not available |
| `prepick.first_attempts_changed_any_rate` | not available |
| `prepick.lines_compared` | not available |
| `prepick.lines_changed` | not available |
| `prepick.lines_changed_rate` | not available |
| `prepick.changed_toward_key` | not available |
| `prepick.changed_toward_key_rate` | not available |
| `prepick.changed_away_from_key` | not available |
| `prepick.changed_away_from_key_rate` | not available |
| `prepick.lines_held` | not available |
| `prepick.first_attempts_before_required` | 0 |
| `prepick.first_attempts_read_after_a_call` | 0 |
| `explain.case_version` | brightwater-v2 |
| `explain.items_with_text` | 0 |
| `explain.fresh_calls_without_text` | 0 |
| `explain.items_scored` | 0 |
| `explain.evidence_avg_of_2` | not available |
| `explain.period_avg_of_2` | not available |
| `explain.action_avg_of_2` | not available |
| `explain.total_avg_of_6` | not available |
| `explain.second_scorer_drawn` | 0 |
| `explain.double_scored` | 0 |
| `explain.second_exact_agreement_rate` | not available |
| `explain.second_within_one_rate` | not available |
| `explain.key_disagreements_recorded` | 0 |

`words.` rows for halyard-v3 with brightwater-v2, lines in the player's own words where the reason chips agreed with the key

| `words.codename` | `words.line` | `words.type` | `words.text` |
| --- | --- | --- | --- |
| none | | | |
