# What an AI assistant produced from three ledgers

Six drafting runs, 13 September 2026, Claude Opus through Claude Code. Every company was drafted twice. The blind draft saw the company header, the threshold rule and the account lines and nothing else, under one plain request: write the month-end variance commentary for the accounts that need explaining, one line per account, with the amount, the percent and the reason. The second used Prompt 1, copied from checker.html. No draft was edited. All six were then run through checker.html as it stood when this note was first committed, at 8db3106; the exports and the raw drafts sit beside this note.

Every unsupported claim in the six drafts is classified in [UNSUPPORTED-CLAIMS.md](UNSUPPORTED-CLAIMS.md), with the exact text behind every count.

## How the runs were set up, and why they are not a controlled comparison

The Halyard pair is the retained development-session run: both drafts were written inside the session that was building the exercise. Brightwater and Kestrel are fresh-context runs, drafted in contexts holding only the ledger, because the building session had read the sample memo printed beside the Kestrel ledger in checker.html and could no longer draft it blind. The raw Halyard files record that the model had not read the exercise memo, the challenge list or the key, and that statement cannot establish everything the session history held. The Halyard blind draft says "all four regional depots", which matches a case fact the ledger block did not contain. A difference between Halyard and the other two is therefore a difference between setups as much as between ledgers.

Two earlier passes at the fresh-context prompts were discarded, because each told the model it could not look anything up, which is the restraint Prompt 1 is meant to supply. They are not in this folder.

## The blind drafts

Claims are counted in four classes: a cause asserted with nothing on file behind it, a cause ruled out that the ledger cannot rule out, a forecast of a later period, and a request that names the source that would settle the driver. Figure fails are counted at figure level; review and not-checked are rows in the export.

| Run | Setup | Lines explained | Causes asserted | Causes ruled out | Forecasts | Requests naming a source | Figure fails | Direction fails | Review | Not checked | Rows |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Halyard | development session | 14 | 26 | 1 | 1 | 0 | 6 | 1 | 98 | 34 | 199 |
| Brightwater | fresh context | 3 | 0 | 1 | 0 | 3 | 0 | 0 | 9 | 4 | 39 |
| Kestrel | fresh context | 4 | 0 | 0 | 1 | 4 | 0 | 0 | 17 | 7 | 60 |

In the Halyard blind draft that is 26 causes, 1 cause ruled out, 1 forecast, and none of them has a source on file. The first version of this table counted 2 "fabricated facts" in that draft, the Southeast depot and three additional payroll days. Neither is a document, both sit inside causes counted above, and the column did not describe a defined unit, so the four classes replace it here and on the review page.

## The same three under Prompt 1

| Run | Setup | Lines explained | Causes asserted | Causes ruled out | Forecasts | Requests naming a source | "No source on file" | Figure fails | Direction fails | Review | Not checked | Rows |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Halyard | development session | 7 | 0 | 0 | 0 | 0 | 7 | 0 | 0 | 37 | 2 | 81 |
| Brightwater | fresh context | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 17 | 2 | 36 |
| Kestrel | fresh context | 4 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 22 | 5 | 52 |

## What changed under Prompt 1

Halyard changed most, and it is also the run whose setup differs. Its blind draft gave a reason for all fourteen accounts, wrote commentary on seven lines below the rule, and closed with a summary paragraph naming subtotals without naming an account. The seven checker failures all sit in that paragraph, and none of them is a numerical mistake. Total revenue rose $536,000, or 8.6 percent, total operating expenses rose $188,500, or 18.8 percent, and the net result fell $105,500, or 10.2 percent, and each of those recomputes from the ledger. The checker bound the subtotals to account 6400, whose name the paragraph mentions, compared them with that one account, and read "declined" against its rising balance. Under Prompt 1 the summary paragraph went, every reason became "no source on file", and the failures went with it.

Brightwater and Kestrel moved differently. Their blind drafts had no summary paragraph and already declined to assert a cause: each stated the movement and then named the document that would settle the driver, seven requests between them. They still carried one unsupported claim each. The Brightwater draft says "patient volume alone does not account for it", which rules out a cause the ledger cannot rule out, because the ledger carries revenue and not visits, procedure mix or realized prices. The Kestrel draft says "only the managed services base carries into August", a forecast nothing supplied supports. Under Prompt 1 both claims were gone, and so were the named documents, because every reason became "no source on file" with no record named.

Prompt 1 raised their review counts rather than lowering them. The checker at 8db3106 did not read "prior $96,000" or "current $138,400" as roles, so each of those figures came back unresolved and went to the queue. That is the prompt and the checker disagreeing, not the memo being wrong.

## Across the three

The arithmetic in the drafts held in all six runs. No draft stated a change or a percent the ledger does not produce, and the only failures anywhere came from the checker binding one summary paragraph's subtotals to a single account. The unsupported reasoning was not confined to the draft that asserted causes: the two drafts that asked for documents still ruled out one cause and forecast one month, so a memo that reads as cautious still needs its explanations checked against what is on file. Under Prompt 1 none of the three drafts carried an unsupported claim of any class, and every line read "no source on file", which leaves a queue of missing sources rather than claims to disprove but names no document for the reviewer to request.

## Coverage of each run

| Run | Sentences | Checked | Review | Not checked | Failed | Rows used | Queue |
|---|---|---|---|---|---|---|---|
| Halyard blind | 30 | 2 | 13 | 13 | 2 | 14 | 54 |
| Halyard Prompt 1 | 8 | 0 | 7 | 1 | 0 | 14 | 16 |
| Brightwater blind | 6 | 3 | 1 | 2 | 0 | 5 | 5 |
| Brightwater Prompt 1 | 4 | 0 | 3 | 1 | 0 | 5 | 8 |
| Kestrel blind | 7 | 3 | 2 | 2 | 0 | 6 | 10 |
| Kestrel Prompt 1 | 5 | 0 | 4 | 1 | 0 | 6 | 10 |

Every count above comes from checker.html at 8db3106, with the ledger text in `ledger-paste.txt` and the exports beside this note. The Halyard figures come from re-checking its two original drafts on that build, so all three sit on one scale; the earlier exports are kept and use the older columns. The third independent review reran all six drafts at b6ba468 and reproduced every sentence-status count here. Some queue counts changed with how the ledger was represented, so a queue count is comparable only with the same input text on the same revision. No run skipped a ledger row or left a qualifying line silent.

## What these runs do not establish

These are six single runs of one model under two setups, classified by one reader. They do not show how often a model invents causes, whether a reviewer could tell in advance which memo will, or how much Prompt 1 improves reliability. The rerun that would make the comparison fair has not been done: the three paired drafts repeated in clean contexts under fixed instructions, every output retained including the ones that abstain, and a second reader classifying the claims. Six more runs would still be an illustrative sample rather than a study of how reliably a model behaves.
