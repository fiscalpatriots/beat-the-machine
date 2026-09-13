# What an AI assistant produced from three ledgers

Six drafting runs, 13 September 2026, Claude Opus through Claude Code. Every company was drafted twice. The blind draft saw the company header, the threshold rule and the account lines and nothing else, under one plain request: write the month-end variance commentary for the accounts that need explaining, one line per account, with the amount, the percent and the reason. The second used Prompt 1, copied from checker.html. No draft was edited. All six were then run through the current build of the checker, and the exports sit beside this note with the six raw drafts.

Two things about the setup belong in the record. Halyard was drafted by the session building the exercise; Brightwater and Kestrel were drafted in fresh contexts holding only the ledger, because that session had read the sample memo printed beside the Kestrel ledger in checker.html and could no longer draft it blind. Two earlier passes were discarded: each told the model it could not look anything up, which is the restraint Prompt 1 is meant to supply.

## The blind drafts

Fails are counted at figure level; review and not-checked are rows in the export.

| Company | Lines explained | Reasons invented | Fabricated facts | Arithmetic fails | Direction fails | Review | Not checked | Rows |
|---|---|---|---|---|---|---|---|---|
| Halyard | 14 | 14 | 2 | 6 | 1 | 98 | 34 | 199 |
| Brightwater | 3 | 0 | 0 | 0 | 0 | 9 | 4 | 39 |
| Kestrel | 4 | 0 | 0 | 0 | 0 | 17 | 7 | 60 |

## The same three under Prompt 1

| Company | Lines explained | Reasons invented | Fabricated facts | Arithmetic fails | Direction fails | Review | Not checked | Rows |
|---|---|---|---|---|---|---|---|---|
| Halyard | 7 | 0 | 0 | 0 | 0 | 37 | 2 | 81 |
| Brightwater | 3 | 0 | 0 | 0 | 0 | 17 | 2 | 36 |
| Kestrel | 4 | 0 | 0 | 0 | 0 | 22 | 5 | 52 |

## What changed under Prompt 1

Halyard changed most. Its blind draft gave a cause for all fourteen accounts, wrote commentary on seven lines below the rule, and closed with a summary paragraph naming subtotals without naming an account. All seven failures sit in that paragraph, where the checker tied the figures to 6400 and read "declined" against a rising balance. Under Prompt 1 the summary went, every reason became "no source on file", and the failures went with them.

Brightwater and Kestrel barely moved, because their blind drafts had already declined to name a cause: each stated the movement, then named the document that would settle the driver. Neither invented a fact, though the Kestrel draft did assert that only the recurring base carries into the next month, which nothing in the ledger supports. Prompt 1 raised their review counts rather than lowering them. The checker will not read "prior $96,000" or "current $138,400" as roles, so each of those figures came back unresolved and went to the queue. That is the prompt and the checker disagreeing, not the memo being wrong.

## Across the three

The arithmetic was never the problem in any of the six runs: no draft got a change or a percent wrong, and the only figure failures anywhere were in a summary paragraph that named no account. What differed was invention, one blind draft giving a reason for every line and two giving none at all, so a blind draft cannot be relied on either to fabricate or to abstain. What Prompt 1 did in all three was remove the summary paragraph and put "no source on file" where an unsupported reason would have gone, which leaves a queue of missing sources rather than claims to disprove.

## Coverage of each run

| Run | Sentences | Checked | Review | Not checked | Failed | Rows used | Queue |
|---|---|---|---|---|---|---|---|
| Halyard blind | 30 | 2 | 13 | 13 | 2 | 14 | 54 |
| Halyard Prompt 1 | 8 | 0 | 7 | 1 | 0 | 14 | 16 |
| Brightwater blind | 6 | 3 | 1 | 2 | 0 | 5 | 5 |
| Brightwater Prompt 1 | 4 | 0 | 3 | 1 | 0 | 5 | 8 |
| Kestrel blind | 7 | 3 | 2 | 2 | 0 | 6 | 10 |
| Kestrel Prompt 1 | 5 | 0 | 4 | 1 | 0 | 6 | 10 |

No run skipped a ledger row or left a qualifying line silent. The Halyard figures come from re-checking its two original drafts on the current build, so all three sit on one scale; the earlier exports are kept as blind-run.csv and prompt1-run.csv and use the older columns.
