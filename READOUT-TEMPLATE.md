# Second Pass: Results Readout

One page a facilitator fills after a session. Run `findings.py` against the downloaded responses and copy its output in. The name in each cell is the field the script writes for it, and a field printed under **Columns not found** leaves its cell blank rather than estimated. Players are distinct codenames, and one who tapped two chapters counts in both. Session `run.generated`, file `run.source_file`, cases `run.case_round1` and `run.case_round2`, key dated `run.key_date`, product `run.product_version`, responses `run.responses_total`, players `run.players`, test rows dropped `run.test_rows_dropped`, replays dropped `run.replays_dropped`.

## 1. Players by organization, fields carrying the prefix `org.`

| Chapter `name` | Count `players` | Call `call_mean_r1` | Reason `reason_mean_r1` |
| --- | --- | --- | --- |
| Beta Alpha Psi | | | |
| ACFE | | | |
| ASM | | | |
| NABA | | | |
| AAA | | | |
| GMU Student | | | |
| Professor | | | |
| Outside Mason | | | |

## 2. Right call and right reason by error type, fields carrying the prefix `type.`

| Error type `name` | Cards `lines` | Seen `calls_seen` | Call `right_call_rate` | Reason `right_reason_rate` |
| --- | --- | --- | --- | --- |
| Arithmetic | 1, 8 | | | |
| Wrong direction | 3 | | | |
| Timing | 2 | | | |
| Unsupported driver | 7, 14 | | | |
| Unsupported attribution | 12 | | | |
| No explanation | 11 | | | |
| Clean line, the control | 4, 5, 6, 9, 10, 13 | | | |

## 3. False flags on the six clean lines, fields carrying the prefix `falseflag.`

| Clean line | 4 | 5 | 6 | 9 | 10 | 13 | All six |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Count `flags` | | | | | | | |
| Share `rate` | | | | | | | `overall_rate` |

## 4. The fresh case, five lines nobody had seen, fields carrying the prefix `fresh.`

| Fresh line | Keyed call `key` | Call `right_call_rate` | Reason `right_reason_rate` |
| --- | --- | --- | --- |
| 1 Dental supplies | Flag | | |
| 2 Hygienist wages | Stand | | |
| 3 Orthodontic revenue | Flag | | |
| 4 Patient revenue | Flag | | |
| 5 Marketing | Stand | | |

Fresh five `fresh.call_mean` and `fresh.reason_mean` against the trained fourteen `r1.call_mean` and `r1.reason_mean`. Median lap `r1.lap_median`, round two clock `fresh.seconds_median`, no false flags `falseflag.players_with_none`.

## 5. Best reason lines, quoted where the reason agreed with the key

| Codename `words.codename` | Line, type `words.line`, `words.type` | Quote `words.text` |
| --- | --- | --- |
| | | |

## Reading these honestly

Every figure here is descriptive accuracy against a key on one sitting, so report it as what this group called on nineteen written lines and nothing more. The fresh five are a second unseen set scored the same way rather than a post-test, so the gap between those pairs separates two item sets rather than measuring learning, transfer or time saved. Write the case version and key date beside any number leaving this page, because a row scored against an earlier key is not comparable.
