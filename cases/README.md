# The shared case definitions

Two files hold the cases the public drill runs on.

| File | Version | Company | Lines |
| --- | --- | --- | --- |
| `halyard-v3.json` | halyard-v3, 13 September 2026 | Halyard Provisioning Group, Inc. | 14 |
| `brightwater-v2.json` | brightwater-v2, 13 September 2026 | Brightwater Dental Partners, PLLC | 5 |

Each file carries the company and period, the threshold policy and a sentence on its scope, a
note on what On file means, the ledger rows, the statement groups, and one entry per line with
the memo sentence, the on-file facts, the key, the error type, the reveal reason, the tell, and
the over-flag note where there is one.

## How the page reads them

`index.html` fetches both files at load. When the fetch fails, which is what happens when the
file is opened from a folder rather than served, the page falls back to a copy of the same JSON
written into the file between the `BUILD:CASES-START` and `BUILD:CASES-END` markers.

The JSON files are the source of truth. After editing either one, run:

```
node build-cases.cjs
```

That rewrites the inline copy and refuses to write if a card points at an account that is not in
the ledger, if a card's figures do not tie to the ledger row, or if a card is missing its key,
its reason or its tell. Never hand-edit the generated block.

`window.__BTM_CASES` on the live page reports which of the two paths won, and the version and
date ride into the response record on question A and into the local copy.

## For the checker lane

`checker.html` ships a Halyard sample. It must be regenerated from `halyard-v3.json` by the
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
   8, 12 and 14 in halyard-v3 now turn on exactly that distinction.
5. **No separate case-fact summary.** The game supplies On file facts per line as verified case
   assumptions. The checker supplies none, so a clean verdict in the game does not transfer to
   the checker sample without the matching evidence.

Until the sample is regenerated, label it in `CHECKER.md` as a different memo version with
unresolved issues rather than as the same case. Do not port a clean verdict from the game to the
checker sample without the evidence the game card rests on.

## What changed in halyard-v3 and brightwater-v2

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
