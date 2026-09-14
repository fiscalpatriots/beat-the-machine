# Prompt 1 drafts, rerun through the repaired checker

Run on 13 September 2026 by the checker repair lane, after the third independent review of the same day.

The review found that all three retained Prompt 1 drafts came back with **no sentence checked within scope**, because the checker did not read "prior $96,000" or "current $138,400" as roles, and those are the labels Prompt 1 asks for. The repair reads "prior", "previous" and "current" standing in front of a figure as the prior and current balance, and turns "no source on file" into a question for the controller instead of leaving it silent.

## What was run

| | Revision | File |
| --- | --- | --- |
| Before | beat-the-machine `b6ba468` | `checker.html` at that commit, the revision the review examined |
| After | beat-the-machine `d081409` | `checker.html` at that commit |
| After, command line | second-pass `acdf580` | `second_pass/checker.py` at that commit |

Both browser runs use the suite harness in `tests/run-checker-tests.cjs` with the page defaults: a $25,000 floor, a 10 percent floor, both legs, zero prior balances owing commentary, no ratios. The Python run calls `checker.run_check` with the same defaults. The inputs are the ones the review retained in `drafts-rechecked.json`; each memo is the text under the last `---` of its raw file in `evidence/`, and it matches that file exactly once line endings are normalized.

## Sentence status counts

| Draft | Sentences | Checked within scope | Needs review | Not checked | Failed | Queue |
| --- | --- | --- | --- | --- | --- | --- |
| Halyard Provisioning Group, June 2026, before | 8 | 0 | 7 | 1 | 0 | 16 |
| Halyard Provisioning Group, June 2026, after | 8 | **7** | 0 | 1 | 0 | 9 |
| Brightwater Dental Partners, June 2026, before | 4 | 0 | 3 | 1 | 0 | 7 |
| Brightwater Dental Partners, June 2026, after | 4 | **3** | 0 | 1 | 0 | 4 |
| Kestrel IT Services, July 2026, before | 5 | 0 | 4 | 1 | 0 | 10 |
| Kestrel IT Services, July 2026, after | 5 | **4** | 0 | 1 | 0 | 6 |

Across the three drafts: **0 of 17** sentences checked within scope before, **14 of 17** after. The before counts reproduce the review's own `drafts-rechecked.json` exactly. The command line returns the same counts and the same status for every sentence after the repair.

The one sentence left **not checked** in each draft is the closing line, "Seven lines fell below the rule and carry no commentary" and its kin. It names no account, so nothing binds it, which is the right answer. Every numbered line now checks on its prior balance, current balance, change and percent, and its direction word agrees with the sign.

## What the queue now carries

The queue got shorter because the role questions are gone, and what is left is what a person has to answer:

- **Halyard Provisioning Group, June 2026**: 1 discarded column, 7 no source on file, 1 unmatched sentence.
- **Brightwater Dental Partners, June 2026**: 3 no source on file, 1 unmatched sentence.
- **Kestrel IT Services, July 2026**: 1 discarded column, 4 no source on file, 1 unmatched sentence.

Every numbered line in all three drafts says "because no source on file". Each one is now a **No source on file** item owned by the controller, asking what drove the line and which document supports it. A checked status on those lines says the figures tie. It does not say the driver is known, and the queue says so line by line.

## The exact inputs

### Halyard Provisioning Group, June 2026

Ledger, from `evidence/ledger-paste.txt`, as the review read it. SHA-256 `34a95a659daf44bd394e09c8c5c04e205665a95bdf2b77847bd40ed3a496f364`.

```
Line	Account	Prior	Current	Variance	Percent
4000	Product revenue, distribution	5,240,000	5,612,000	372,000	7.1%
4100	Service revenue, equipment maintenance	812,000	1,041,000	229,000	28.2%
4200	Freight billed to customers	186,000	121,000	(65,000)	-34.9%
5000	Cost of product sold	3,930,000	4,278,000	348,000	8.9%
5100	Inbound freight	214,000	287,800	73,800	34.5%
6000	Warehouse wages	630,000	702,500	72,500	11.5%
6100	Fleet fuel	96,400	91,200	(5,200)	-5.4%
6200	Repairs and maintenance, depots	41,000	118,600	77,600	189.3%
6300	Software subscriptions	28,500	30,100	1,600	5.6%
6400	Bad debt expense	15,000	62,000	47,000	313.3%
6500	Professional fees	55,000	47,500	(7,500)	-13.6%
7000	Depreciation	128,000	128,000	0	0.0%
7100	Interest expense	61,200	92,400	31,200	51.0%
7400	Inventory shrink adjustment	6,400	8,900	2,500	39.1%
```

Memo, from `evidence/ai-draft-halyard-2026-09-13-prompt1-raw.md`. SHA-256 `8b3031683506b3dfc14183037c6b8f7889241b3b557e98de060f7f7f24e16342`.

```
1. 4100 Service revenue, equipment maintenance: prior $812,000, current $1,041,000, rose $229,000, 28.2 percent, because no source on file (source: no source on file).
2. 4200 Freight billed to customers: prior $186,000, current $121,000, fell $65,000, 34.9 percent, because no source on file (source: no source on file).
3. 5100 Inbound freight: prior $214,000, current $287,800, rose $73,800, 34.5 percent, because no source on file (source: no source on file).
4. 6000 Warehouse wages: prior $630,000, current $702,500, rose $72,500, 11.5 percent, because no source on file (source: no source on file).
5. 6200 Repairs and maintenance, depots: prior $41,000, current $118,600, rose $77,600, 189.3 percent, because no source on file (source: no source on file).
6. 6400 Bad debt expense: prior $15,000, current $62,000, rose $47,000, 313.3 percent, because no source on file (source: no source on file).
7. 7100 Interest expense: prior $61,200, current $92,400, rose $31,200, 51.0 percent, because no source on file (source: no source on file).

Seven lines fell below the rule and carry no commentary.
```

### Brightwater Dental Partners, June 2026

Ledger, from the ledger rows of `cases/brightwater-v5.json`, account, name, prior and current joined by tabs. SHA-256 `d74f768c323ed3733d312882698897a8a8341fca7f7bf7b6e252e0f0e4e51097`.

```
4010	Patient service revenue, net	742000	803500
4220	Orthodontic plan revenue	96000	138400
5210	Dental supplies and lab fees	138500	191200
6110	Hygienist wages	214000	268900
6610	Marketing and patient outreach	18400	24100
```

Memo, from `evidence/ai-draft-brightwater-2026-09-13-prompt1-raw.md`. SHA-256 `28dbdd06f45add9201fc26ae01ed0b4f67a5198045f9d1b719cf50294bd324c3`.

```
1. 4220 Orthodontic plan revenue: prior $96,000, current $138,400, rose by $42,400, 44.2 percent, because no source on file (source: no source on file).
2. 5210 Dental supplies and lab fees: prior $138,500, current $191,200, rose by $52,700, 38.1 percent, because no source on file (source: no source on file).
3. 6110 Hygienist wages: prior $214,000, current $268,900, rose by $54,900, 25.7 percent, because no source on file (source: no source on file).

Two lines fell below the rule and carry no commentary.
```

### Kestrel IT Services, July 2026

Ledger, from the Kestrel ledger inline in `checker.html` (the QuickBooks Profit and Loss Comparison paste). SHA-256 `72025bf0dadc157e050d7a1079b0e49f7d524fb9ada0e80bb71096fbc94a17c9`.

```
Kestrel IT Services, LLC
Profit and Loss Comparison
July 2026 compared with June 2026

	Jul 2026	Jun 2026	$ Change	% Change
Income
   4000 Recurring managed services	198,400.00	161,500.00	36,900.00	22.85 %
   4100 Project and implementation revenue	96,400.00	38,900.00	57,500.00	147.81 %
Total Income	294,800.00	200,400.00	94,400.00	47.11 %
Cost of Goods Sold
   5000 Subcontracted engineering	88,300.00	41,800.00	46,500.00	111.24 %
Total Cost of Goods Sold	88,300.00	41,800.00	46,500.00	111.24 %
Gross Profit	206,500.00	158,600.00	47,900.00	30.20 %
Expenses
   6000 Salaries and wages	88,500.00	88,500.00	0.00	0.00 %
   6200 Software licenses and hosting	57,900.00	22,600.00	35,300.00	156.19 %
   6400 Client acquisition costs	14,200.00	4,900.00	9,300.00	189.80 %
Total Expenses	160,600.00	116,000.00	44,600.00	38.45 %
Net Operating Income	45,900.00	42,600.00	3,300.00	7.75 %
Net Income	45,900.00	42,600.00	3,300.00	7.75 %
```

Memo, from `evidence/ai-draft-kestrel-2026-09-13-prompt1-raw.md`. SHA-256 `3c94fe0dc37e04217b91d57ef31f555ee072c8065ada44d549d1abc9cb9c59be`.

```
1. 4000 Recurring managed services: prior $161,500.00, current $198,400.00, rose by $36,900.00, 22.85 percent, because no source on file (source: no source on file).
2. 4100 Project and implementation revenue: prior $38,900.00, current $96,400.00, rose by $57,500.00, 147.81 percent, because no source on file (source: no source on file).
3. 5000 Subcontracted engineering: prior $41,800.00, current $88,300.00, rose by $46,500.00, 111.24 percent, because no source on file (source: no source on file).
4. 6200 Software licences and hosting: prior $22,600.00, current $57,900.00, rose by $35,300.00, 156.19 percent, because no source on file (source: no source on file).

Two lines fell below the rule and carry no commentary.
```

## Reproduce

From beat-the-machine at `d081409`, with the review bundle beside it, load `execute` from `tests/run-checker-tests.cjs` the way the review's `recheck-drafts.cjs` does, and call it with `{inputs: {ledger, memo}}` for each block above. For the before column, point the harness at `git show b6ba468:checker.html`. From second-pass at `acdf580`, `checker.run_check(ledger, memo)` returns the after counts.
