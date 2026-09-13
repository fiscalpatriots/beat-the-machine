# How the checker's export fills the evidence log

`CHECKER.md` does not exist in this repository yet. The checker stopped at the design stage on
12 September 2026 and `CHECKER-STATUS.md` holds that design, so this note is written against it
and moves into `CHECKER.md` when the page is built. The control it feeds is `PROTOCOL.md`, and the
file it fills is `EVIDENCE-LOG-TEMPLATE.csv`.

The checker writes one row per memo sentence and one row per account that owes commentary and
never got a sentence. Those rows carry six of the log's fourteen columns and nothing else, which
is the point: the machine fills what it can recompute and a person fills the rest.

| Checker export column | Evidence log column | What carries across |
| --- | --- | --- |
| Account number | line | The ledger line the check ran against, matched by number, by name or by an exact figure |
| Account name | account | The name as the ledger prints it, not as the memo paraphrases it |
| Sentence | sentence | The memo sentence identifier, or `none` on a silence row |
| Check | check | One of arithmetic, direction, threshold, silence |
| Result | result | `pass`, `fail`, or `information` on a threshold row that only reports what the line owes |
| Detail | finding | The recomputed figure beside the memo's figure, in the checker's own words |

Nothing else in the export belongs in the log. The run header, which carries the close period and
the memo version the visitor pasted in, is typed into the first two columns of every row for that
run rather than exported per row.

The eight remaining columns are the reviewer's, and they are never machine filled.

- `ask to the controller` opens on any `fail` row that the preparer cannot clear, and on any
  reviewer row where the document is not on file.
- `reviewer answer` is written on the rows the reviewer works, which are the fails that came back
  and the queue. A `pass` row with no ask stays blank.
- `resolved` is `yes` only when the ask has an answer on file, or when the corrected sentence has
  been rechecked.
- `reviewer name`, `date` and `controller sign-off` are entered at step 5 of the protocol.

Two rows exist that the checker never produces. Every sentence that passes all four checks enters
the reviewer queue and is written into the log twice, once with `check` set to `driver` and once
with `check` set to `timing`, both with `result` set to `reviewer`. Those are the two judgment
questions, and a close with no such rows is a close where the second pass was not run.

The three example rows in the template come from the Halyard Provisioning Group case in
`index.html` and in `drafts-2026-09-05-aina/EXERCISE-case-01-form-rev4.md`. Halyard does not exist
and no figure in it came from any real company or engagement.
