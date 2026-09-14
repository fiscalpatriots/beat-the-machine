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

No live drafting run produced the case memo. The build log shows both `ANTHROPIC_API_KEY` and `OPENAI_API_KEY`
absent at build time with the AI layer running deterministic, and every challenge in every session
log carries `"source": "deterministic"`, so the fourteen challenges came from the case file's own
key rather than from a model.

The build itself was carried out by an AI coding agent under Khaled Alkurd's direction, in a
session that began with `second-pass/` empty. The sentences were written with AI assistance, and
what they are is authored defects rather than generated prose that happened to be wrong.

## The drafting runs are separate, and they are not the case

`evidence/` holds six real drafting runs of 13 September 2026, one model drafting commentary from
the Halyard, Brightwater and Kestrel ledgers, once under a plain request and once under Prompt 1.
None of that output went into a case file. The two Halyard drafts are the retained
development-session run, written inside the session that was building the exercise, and the
Brightwater and Kestrel drafts are fresh-context runs, so the three are not a controlled
comparison. `evidence/EVIDENCE-NOTE.md` records the setup and the checker revision behind every
count, and `evidence/UNSUPPORTED-CLAIMS.md` classifies every unsupported claim with its exact text.
The checker those runs went through reads only the inputs `CHECKER.md` lists under "What goes in".

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
| 13 September 2026 | `halyard-v4` and `brightwater-v5` issued: every card gained a basis key, and every Brightwater fact on file quotes a named, dated document. Six drafting runs recorded in `evidence/`. |

The live call key dates from 12 September 2026 and the basis key from 13 September 2026. Rows
scored against different case versions are never pooled, and rows filed before the live versions
are not comparable with rows filed after them.
