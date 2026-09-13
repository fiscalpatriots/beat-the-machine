# Provenance

How the Halyard case and its machine-drafted memo came to be.

## The case is constructed

Halyard Provisioning Group, Inc. does not exist. The company, the four depots, the fourteen
accounts and every June 2026 balance were invented for training, and
`cases/case-01-june.json` at github.com/fiscalpatriots/second-pass says so in its own `notice`
field. Nothing came from a real company, engagement or dataset, and the figures were designed so
that every planted defect is recomputable from the table alone.

## How the memo was produced

The twelve memo sentences were written during the build of 5 September 2026, each engineered to
carry a specific defect. Eleven defects sit in the case file's `answer_key`, keyed by type, tag,
sentence, account line and amount, alongside three deliberately weak challenges in `distractors`.
That is planting, not the output of a drafting run.

The file labels the commentary's author as "Assistant controller, drafted with the close assistant
and lightly edited". That line is part of the fiction. It says who is supposed to have written the
memo inside the case, and it is not a record of a model being called.

No live drafting run happened. The build log shows both `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`
absent at build time with the AI layer running deterministic, and every challenge in every session
log carries `"source": "deterministic"`, so the fourteen challenges came from the case file's own
key rather than from a model.

The build itself was carried out by an AI coding agent under Khaled Alkurd's direction, in a
session that began with `second-pass/` empty. The sentences were written with AI assistance, and
what they are is authored defects rather than generated prose that happened to be wrong.

## The dates

| Date | What happened |
| --- | --- |
| 5 September 2026 | Repository built from empty. Three cases, Halyard June among them, eleven keyed defects. Two pilots run by simulated reviewers, not by people. |
| 6 September 2026 | First public commit. |
| 8 September 2026 | Sanitized for publication: paths neutralized and one name removed, with no number, result or logic altered. The case laid out as a three page form. |
| 9 September 2026 | The same case, twelve sentences and fourteen challenges wrapped as a scored game. The Google Form went live. |
| 12 September 2026 | The key rebalanced. Four sentences were rewritten to be sound, moving the split from twelve problem lines and two clean to eight and six, so flagging everything now ranks last. Revision 4 put the deciding document behind four calls. |
| 12 September 2026 | The audit. A ChatGPT critique of a flat copy of the case was reconciled against the live build: five points confirmed the key, two were already fixed and seven were real wording defects. Cards 2, 4, 7, 9, 11, 12 and 14 were corrected. |
| 13 September 2026 | Round two added, five fresh lines of Brightwater Dental Partners, a four office dental group, carrying three of the same error types on a different industry. |

The live key dates from 12 September 2026, so earlier rows are not comparable.
