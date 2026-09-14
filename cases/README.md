# The shared case definitions

Two files hold the cases the public drill runs on.

| File | Version | Company | Lines | Mode |
| --- | --- | --- | --- | --- |
| `halyard-v4.json` | halyard-v4, 13 September 2026 | Halyard Provisioning Group, Inc. | 14 | practice |
| `brightwater-v5.json` | brightwater-v5, 13 September 2026 | Brightwater Dental Partners, PLLC | 5 | assessment |
| `brightwater-v4.json` | brightwater-v4, 13 September 2026 | Brightwater Dental Partners, PLLC | 5 | assessment, retired |
| `halyard-v3.json` | halyard-v3, 13 September 2026 | Halyard Provisioning Group, Inc. | 14 | practice, retired |
| `brightwater-v3.json` | brightwater-v3, 13 September 2026 | Brightwater Dental Partners, PLLC | 5 | assessment, retired |
| `brightwater-v2.json` | brightwater-v2, 13 September 2026 | Brightwater Dental Partners, PLLC | 5 | practice, retired |

The retired files are kept because responses were scored against them and a superseded key has to
stay readable. The page loads `halyard-v4` and `brightwater-v5` only, and rows scored against one version are never
pooled with rows scored against another. Each v4 file carries a `changeLog` array recording what
moved from v3 and why.

## The basis key

Every card carries `basisKey`, the set of basis chips that are correct on that card. A chip
outside that set contradicts the key for that card, which is why `wrong account` on a clean line
is wrong rather than merely unhelpful. The page counts the reason as right when the player tapped
at least one chip in the key and no chip outside it, and it counts that apart from the call.

A card the key lets stand carries `the figure and reason hold` and nothing else, because a chip
naming a defect contradicts a line that has none. `build-cases.cjs` refuses to write if a stand
carries anything else, if a flag carries the hold chip, or if a key names a chip the page does
not offer.

No card in either case has an amount booked in an account it does not belong in, so
`wrong account` is in no key in this release. Tapping it on all nineteen lines scores zero on
reason. That is the point of counting the reason separately: the same run scored 14 of 14 and 5
of 5 on the call in the 13 September review.

The reason score is a compatibility check on the stated basis and not a rubric score: it measures
agreement with the accepted reason categories on each card. It does move the rank. `linePoints` in
`index.html` awards 50 points for an agreeing reason on top of the 100 for a correct call (and
nothing for the reason when the call is wrong), and the rank is read off total points, so the same
fourteen correct Halyard calls reach Partner at 2,625 points with every reason agreeing and stop at
Senior at 1,925 with none agreeing. The badges read the calls alone and never the reason. The rank
is a game device on one case, not a credential and not a learning outcome. A participant who taps
`no source on file` on every flag and the hold chip on every stand would score well on reason
without having reasoned, so the three-dimension reasoning rubric stays with a person outside the
page, and reviewer disagreements are retained rather than settled by the key.

Each file carries the company and period, the threshold policy and a sentence on its scope, a
note on what On file means, the ledger rows, the statement groups, and one entry per line with
the memo sentence, the on-file facts, the key, the error type, the reveal reason, the tell, and
the over-flag note where there is one. A file with `"mode": "assessment"` also carries
`assessmentNote`, the sentence the bridge screen prints to say what is already settled.

## The assessment case, brightwater-v5

Round two is an independent assessment rather than more practice, so the page suppresses every
signal that would leak correctness: no reveal between lines, no running score, no streak, and no
track. All five verdicts arrive together on a results screen once the fifth call is in.

Every entry under **On file** carries one line quoted out of a named, dated document, or says in the
same place that the document was asked for and never arrived. Line 3 is the one to read twice: the
orthodontic plan schedule is a real document, it is quoted, it ties to the ledger's May balance of
$96,000, and it is dated 31 May, so it cannot carry a cause that starts in June. A document on the
card is not the same as a document covering the period the sentence is about.

Every one of the five lines tests causal evidence. Every figure in every sentence ties to the
ledger, every direction word matches the sign of the movement, and every threshold reading in the
memo is correct. Every line carries a sentence naming a cause, so on all five the only question
is whether something on file carries that cause. The mix is three unsupported-cause flags, lines
1, 3 and 4, and two supported-cause stands, lines 2 and 5.

| Line | Account | May | June | Change | Percent | Owes commentary | Call | Type | Basis key |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5210 Dental supplies and lab fees | $138,500 | $191,200 | +$52,700 | 38.1% | yes | Flag | unsupported driver | no source on file |
| 2 | 6110 Hygienist wages | $214,000 | $268,900 | +$54,900 | 25.7% | yes | Let it stand | clean line | the figure and reason hold |
| 3 | 4220 Orthodontic plan revenue | $96,000 | $138,400 | +$42,400 | 44.2% | yes | Flag | unsupported driver | wrong period; no source on file |
| 4 | 4010 Patient service revenue, net | $742,000 | $803,500 | +$61,500 | 8.3% | no | Flag | unsupported driver | no source on file |
| 5 | 6610 Marketing and patient outreach | $18,400 | $24,100 | +$5,700 | 31.0% | no | Let it stand | clean line | the figure and reason hold |

The two stands are carried by a document. Line 2 has a June payroll register putting the whole
$54,900 on the two hygienists hired for the second chair, with no other hygienist pay moving.
Line 5 has the vendor invoice for the mailer and $18,400 of unchanged recurring spend, which
together reconcile the whole of June's $24,100.

The three flags name a cause nothing supplied establishes. Line 1 attributes $52,700 to a new
surgical suite with no case mix report, no lab invoice summary and no implant count on file.
Line 3 attributes $42,400 to thirty-one plans that started in June, and the only plan schedule on
file is dated 31 May and covers the plans running before June, so a genuine document is on file
and it relates to the wrong period. Line 4 attributes $61,500 to two associate dentists with no
production report by provider and no visit count on file.

Line 3 is the line that stops document presence from being an automatic answer. A participant who
reads "schedule on file" and lets the sentence stand has not checked what period the schedule
covers.

Lines 4 and 5 both say plainly on file that the threshold required no commentary and the memo
explained the line anyway, so the question on both is the explanation rather than whether one was
owed. That sentence appears on both, so it separates nothing except the evidence.

### What a shortcut scores

Stated rather than claimed away. Three lines clear both legs of the threshold and two clear one
leg each.

| Strategy | Calls | Right |
| --- | --- | --- |
| The key | flag, stand, flag, flag, stand | 5 of 5 |
| Flag every line over both legs | flag, flag, flag, stand, stand | 3 of 5 |
| Flag every line | flag, flag, flag, flag, flag | 3 of 5 |
| Let every line stand | stand, stand, stand, stand, stand | 2 of 5 |

Two shortcuts reach 3 of 5 on the call. Five items cannot separate judgment from a shortcut on
their own, which is why the fresh case is reported as five-item decision accuracy on a second
unseen set, scored the same way as round one, and never as proof of transfer or of a learning
gain. The reason chips are a second reading, of agreement with accepted reason categories, and a
chip shortcut reaches that too: `no source on file` on the three flags and the hold chip on the
two stands scores 5 of 5 on reason without saying why the 31 May schedule cannot carry June plan
starts. That is why the measurement adopted on 13 September 2026 for the next assessment version,
`brightwater-v6`, asks for a short written explanation on each of the five items, naming the
decisive evidence, why it matters for this period, and the action or source request that follows,
scored blind by an independent educator against a rubric, with the chips still reported
separately. Until that version is in this folder, `brightwater-v5` above is the assessment case.

`build-cases.cjs` enforces the assessment contract. It refuses to write if a memo states a dollar
figure the account does not produce, states a percent that is not the movement, uses a direction
word against the sign, if an assessment line carries no memo sentence, or if an assessment line
is a no-explanation line. A silent line has no cause to judge, so it belongs in the practice case
and not in the scored one.

## How the page reads them

`index.html` fetches both files at load. When the fetch fails, which is what happens when the
file is opened from a folder rather than served, the page falls back to a copy of the same JSON
written into the file between the `BUILD:CASES-START` and `BUILD:CASES-END` markers.

The JSON files are the source of truth. After editing either one, run:

```
node build-cases.cjs
```

That rewrites the inline copy and refuses to write if a card points at an account that is not in
the ledger, if a card's figures do not tie to the ledger row, if a card is missing its key, its
reason or its tell, or if a basis key breaks the rules above. Never hand-edit the generated
block.

`window.__BTM_CASES` on the live page reports which of the two paths won, and the version and
date ride into the response record on question A and into the local copy.

<!-- GAME LANE SECTION START: authored cases, the columns field, what the drill requires of a
     case file. Owned by the game lane, 13 September 2026. -->

## A case the drill can run

Nothing in the drill counts to fourteen any more. A case file of any length runs, and a case with
no fresh set beside it goes from its last line to the end screen. What a file has to carry:

| Field | What it is |
| --- | --- |
| `version`, `date`, `company`, `period` | the stamps that ride into the response and the record |
| `columns` | the two month names, as `["June", "July"]`. Optional; without it the drill prints May against June |
| `caption`, `threshold`, `policyScope`, `evidenceNote` | the sentences the orientation screen and the legend print |
| `ledger` | one row per account, `[number, name, prior, current, owesCommentary]` |
| `groups` | the statement sections, `{title, accts, total}` |
| `cards` | one per line, in the shape the table below sets out |
| `mode` | `"assessment"` on a case scored at the end rather than line by line, with `assessmentNote` beside it |

A card carries `n`, `icon`, `acct`, `name`, `prior`, `current`, `memo`, `file`, `key`, `type`,
`why`, `truth`, `ask`, `tell`, `post` and `basisKey`. `over` is the line a stand shows when it was
flagged anyway, and `stillOpen` is the line a stand shows when its reasoning is provisional.

`columns` was added on 13 September 2026 for `kestrel-v1`, which runs June against July.
`halyard-v4` and `brightwater-v5` do not carry it and are read as May against June, which is what
they have always printed.

## Cases authored from `author.html`

`author.html` writes a case file in exactly this format, plus two fields of its own, and that file
can be committed straight into this folder once it has been read.

| Field | What it is |
| --- | --- |
| `authoredBy` | the author page and its version, so a hand-written case and a generated one can be told apart |
| `savedAt`, `id`, `name`, `caseVersion` | the wrapper the browser stores, under `btm.owncase.v1` |

The wrapper is `{savedAt, authoredBy, name, caseVersion, id, case, fresh}`. The drill reads the
`case` object and, when it is not null, the `fresh` one. `id` is `own:<name>:<version>`, and it is
what the record and question A report for that run.

The author page will not save a case that breaks the basis-key contract above: a stand carries
`the figure and reason hold` and nothing else and its type is `clean line`, a flag carries no hold
chip and its type is not `clean line`, every card has at least one chip, a why and a tell, and
every card's figures reconcile to the ledger row it points at. It names what is missing instead of
refusing silently.

An authored case is generated rather than policed. `build-cases.cjs` is still the gate for
anything that goes into `index.html`'s inline fallback, and an authored file has to pass it before
it is treated as a published case rather than as one facilitator's own.

<!-- GAME LANE SECTION END -->

## For the checker lane

`checker.html` ships a Halyard sample. It must be regenerated from `halyard-v4.json` by the
checker lane; nothing in this folder changes the checker, and the game lane does not edit
`checker.html` or `CHECKER.md`.

The checker's ledger already matches all fourteen game accounts. Its sample memo does not. The
differences known on 13 September 2026:

1. **The sample is thirteen lines, the game is fourteen.** The two are different memo versions,
   not the same text at different lengths.
2. **"Both revenue lines."** The sample restores a sentence tying the two revenue lines together.
   The game's card 12 turns on the memo never making that connection, so the sample resolves the
   line the game asks the player to catch.
3. **Pump-price assertions.** The sample asserts lower pump prices as the fleet fuel driver. The
   game's card 9 stands on a narrow statement with no driver asserted, and on case facts that
   state June consumption and June invoices are the same population.
4. **Billing assertions placed inside the draft.** The sample has the draft assert its own
   support. A draft's assertion about its own support is not independent evidence, and cards 4,
   8, 12 and 14 in halyard-v4 now turn on exactly that distinction.
5. **No separate case-fact summary.** The game supplies On file facts per line as verified case
   assumptions. The checker supplies none, so a clean verdict in the game does not transfer to
   the checker sample without the matching evidence.

Until the sample is regenerated, label it in `CHECKER.md` as a different memo version with
unresolved issues rather than as the same case. Do not port a clean verdict from the game to the
checker sample without the evidence the game card rests on.

## What changed in brightwater-v5

Written on 13 September 2026, closing the two source-excerpt items the release review left open.

| Line | Call | Change |
| --- | --- | --- |
| All five | unchanged | Every on-file fact carries a one-line excerpt from a named, dated document, or states that the document was requested and is not on file. The author-summarized facts are gone. |
| Brightwater 3, orthodontic plan revenue | flag, unchanged | The wrong-period item now rests on a genuine dated document shown on the card: the orthodontic plan schedule of 31 May 2026, quoted as 96 active plans and $96,000 of monthly billing at that date, stating in its own words that it does not cover plans starting later. |

No call, key, basis key, figure or memo sentence moved. The evidence a player reads is what changed.

## What changed in halyard-v4 and brightwater-v4

Written on 13 September 2026 after an independent release review. Each file's own `changeLog`
carries the same entries in machine-readable form.

| Line | Call | Change |
| --- | --- | --- |
| Halyard 4, service revenue | stand, unchanged | The reveal no longer says billing in arrears puts each fee in the month it was earned. It says the service dates and the earned revenue bridge place the full $229,000 in June, and billing timing is background. The review's objection: billing does not determine when service revenue is earned. |
| Halyard 14, interest expense | flag, unchanged | The on-file fact that read "No draw dates, daily balances, rates or fee schedule were supplied" now reads "Other draw and repayment dates, daily balances, rates and fees were not supplied", because the file had already supplied the 3 June draw date. |
| Halyard 13, cost of product sold | stand, unchanged | The reveal, the over-flag note and a new `stillOpen` line say the stand is provisional: the calculation holds, and the mix cause is a hypothesis until the category sales and cost bridge is on file. |
| Brightwater 3, orthodontic plan revenue | flag, unchanged | No longer a silent line. It carries a memo sentence whose figures tie and whose named cause rests on a plan schedule dated 31 May, so the type moves from no explanation to unsupported driver. |
| All nineteen | unchanged | Every card gained a `basisKey`, and the page scores the call and the reason separately. |

## What changed in halyard-v3 and brightwater-v2

These are the 13 September revisions that produced halyard-v3 and the retired brightwater-v2.
brightwater-v3 replaced v2 the same day and is described above.

Substance changed on six lines. The rest kept their call and tightened the reasoning.

| Line | Call | Change |
| --- | --- | --- |
| Halyard 2, repairs | flag, unchanged | Dropped the inference that completion alone decides the accrual. Asks what June work was performed, recorded and unrecorded, and raises repair against improvement. |
| Halyard 4, service revenue | stand, unchanged | Gained service dates for the twelve contracts and an earned revenue bridge on file that reconciles $812,000 plus $229,000 to $1,041,000. |
| Halyard 8, bad debt | flag, unchanged | Dropped $42,000 as an established component and the routine $5,000 provision. Asks for a reserve rollforward. |
| Halyard 12, product revenue | flag, unchanged | Dropped the exact $65,000 transfer. Keeps the challenge to the demand attribution and asks for a billing bridge by customer. |
| Halyard 13, cost of product sold | stand, unchanged | Memo now separates gross profit dollars from the margin percentage and writes the mix claim as a hypothesis with a bridge requested. |
| Brightwater 5, hygienist wages | flag, unchanged | Dropped the merit increase residual. Asks for a payroll bridge. |

Everywhere else, "fabricated" became "not established from supplied evidence", and derived causes
became requests for a bridge: billing bridge, payroll bridge, reserve rollforward, depot revenue
bridge. A flag can be correct while its explanation is wrong, so a reveal credits the call and
corrects the reasoning separately.

<!-- BEGIN kestrel-v1 section, added 13 September 2026 by the case-authoring lane. Nothing above
     this line was changed. -->

## The second practice case, kestrel-v1

| File | Version | Company | Lines | Mode |
| --- | --- | --- | --- | --- |
| `kestrel-v1.json` | kestrel-v1, 13 September 2026 | Kestrel IT Services, LLC | 12 | practice, not yet loaded |

**`index.html` does not load this file.** The page fetches the v4 pair and nothing else, and the
inline fallback `build-cases.cjs` writes carries the v4 pair and nothing else. Wiring case selection
is a later lane's work, and until it lands, `kestrel-v1.json` is read by people rather than by the
page. It is written to the same schema as `halyard-v4.json` and passes every rule in
`build-cases.cjs`, including the basis key rules, so the wiring lane has nothing to fix in the data.

Two things that lane has to handle:

1. **The comparison months are June and July, not May and June.** `statement()` in `index.html`
   prints the column headers `May` and `June` as literals. `kestrel-v1.json` carries a `columns`
   field, `["June","July"]`, and the headers have to read from it once a third case is selectable.
   The months are June and July because the Kestrel sample already shipping in `checker.html` is
   titled "July 2026 compared with June 2026", and the two have to stay the same memo.
2. **The fifth element on each ledger row.** In this file it is 1 when the movement clears both legs
   of the threshold and 0 when it does not, which the file states in `ledgerNote`. Nothing in
   `index.html` reads it.

### What the case is

Twelve accounts for a managed IT services firm, twelve memo sentences, keyed as seven flags and five
stands. Six accounts and all six memo sentences come from the Kestrel sample in `checker.html`,
carried over with the same figures and the same calls, so a verdict reached in the checker holds in
the game. The six accounts added around them are 4200 hardware and license resale, 5100 hardware and
license cost of resale, 5200 travel and onsite delivery, 6300 computer equipment, 6500 insurance and
7000 depreciation. Revenue, cost of sales, operating expenses and the net line reconcile from the
twelve balances.

Account 7000 carries no card. It is on the statement because card 10 rests on depreciation not
moving, which is the same role account 7000 plays in `halyard-v4.json`. Account 4100 carries two
cards, as account 4000 does in Halyard.

| # | Account | June | July | Change | Percent | Owes commentary | Call | Type | Basis key |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 6200 Software licenses and hosting | $22,600 | $57,900 | +$35,300 | 156.2% | yes | Flag | arithmetic | figure does not tie; no source on file |
| 2 | 5000 Subcontracted engineering | $41,800 | $88,300 | +$46,500 | 111.2% | yes | Flag | wrong direction | direction wrong; no source on file |
| 3 | 6400 Client acquisition costs | $4,900 | $14,200 | +$9,300 | 189.8% | no | Let it stand | clean line | the figure and reason hold |
| 4 | 4100 Project and implementation revenue | $38,900 | $96,400 | +$57,500 | 147.8% | yes | Flag | unsupported driver | no source on file |
| 5 | 6000 Salaries and wages | $88,500 | $88,500 | $0 | 0.0% | no | Let it stand | clean line | the figure and reason hold |
| 6 | 4200 Hardware and license resale | $148,000 | $96,000 | -$52,000 | -35.1% | yes | Flag | unsupported attribution | no source on file |
| 7 | 5100 Hardware and license cost of resale | $100,700 | $65,300 | -$35,400 | -35.2% | yes | Let it stand | clean line | the figure and reason hold |
| 8 | 4100 Project and implementation revenue | $38,900 | $96,400 | +$57,500 | 147.8% | yes | Flag | timing | wrong period; no source on file |
| 9 | 6500 Insurance, cyber liability included | $6,900 | $9,600 | +$2,700 | 39.1% | no | Let it stand | clean line | the figure and reason hold |
| 10 | 6300 Computer equipment | $3,200 | $21,900 | +$18,700 | 584.4% | no | Flag | wrong account | wrong account |
| 11 | 5200 Travel and onsite delivery | $6,400 | $32,900 | +$26,500 | 414.1% | yes | Let it stand | clean line | the figure and reason hold |
| 12 | 4000 Recurring managed services | $161,500 | $198,400 | +$36,900 | 22.8% | yes | Flag | no explanation | nothing written where owed; no source on file |

All seven error types appear. Attribution appears twice, once as `unsupported attribution` on line 6
and once as `wrong account` on line 10, and every other flag type appears once.

**Line 10 is the first card in any case whose basis key is `wrong account`.** This document recorded
that no card in the v4 release had an amount booked in an account it does not belong in, so tapping
that chip scored zero on all nineteen lines. Kestrel gives the chip one line where it is right. The
invoice on file lists eight items, every one of them above the firm's $2,000 capitalisation policy,
and depreciation did not move.

**Four sentences cite a source inside the draft and only one of those documents was supplied.** The
payroll register on line 5 is genuinely on file and carries the stand. The billing schedule on line
4, the partner invoices on line 2 and the vendor invoice on line 1 were never handed over. A case
where every cited source was missing would teach a shortcut instead of the distinction, which is why
one of the four holds.

**Lines 6 and 7 are the same event with two different answers.** The resale billings fell and the
resale cost fell with them. The cost sentence recomputes clean at 32.0 percent in both months and
the vendor cost report ties the whole $65,300 to July invoices, so it stands. The revenue sentence
blames finished refresh cycles and never mentions that the two largest clients moved to a bundled
subscription on account 4000 from 1 July, so it is flagged.

### What a shortcut scores

Stated rather than claimed away. Seven of the twelve lines clear both legs of the threshold.

| Strategy | Right |
| --- | --- |
| The key | 12 of 12 |
| Flag every line over both legs, stand the rest | 9 of 12 |
| Flag every line | 7 of 12 |
| Let every line stand | 5 of 12 |

The threshold shortcut misses the three lines the case was built around: the equipment sitting in
the wrong account on a movement that owed no commentary, the cost line that recomputes clean, and
the travel line a document carries end to end.

### The human-readable copy

`EXERCISE-kestrel-rev1.md` in the Coach HQ repository holds the same case written for a facilitator,
with the setup, the ledger, the twelve sentences, the on-file facts and the key in a separate final
section.

<!-- END kestrel-v1 section -->

