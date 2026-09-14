# How the checker's export fills the evidence log, and how the drill scores a reason

Two exports leave this repository and neither one is a conclusion. The checker writes what it
recomputed; the drill writes what a player called and why. This note says which column each
piece lands in and which columns a person still has to fill.

The control the checker feeds is `PROTOCOL.md`, version 1.1. The file it fills is
`EVIDENCE-LOG-TEMPLATE.csv`. The page's own contract is `CHECKER.md`, which is in this
repository and is the authority on statuses and on the reviewer queue.

## The checker export

The checker writes one row per memo sentence, one row per check it ran, and one row per account
that owes commentary and never got a sentence. Its CSV carries eighteen columns. Six of them
carry across to the evidence log, four are the run header that is typed into the first two log
columns for every row of that run, and the rest exist so a reader can find the sentence again.

| Checker export column | Evidence log column | What carries across |
| --- | --- | --- |
| `account` | account | The name as the ledger prints it, not as the memo paraphrases it |
| `line` | line | The ledger line the check ran against, matched by number, by name or by an exact figure. `none` on a silence row |
| `sentence id` | sentence | The memo sentence identifier, or blank on a silence row |
| `check` | check | The check that produced the row: arithmetic, direction, threshold or silence |
| `status` | result | `checked within scope`, `needs review`, `not checked` or `failed`, in the checker's own words rather than translated into pass and fail |
| `finding` | finding | The recomputed figure beside the memo's figure, in the checker's own words |

`run id`, `run timestamp`, `close period` and `reviewed memo version` are the run header. The
close period and the memo version go into the first two log columns for every row of that run.
The run identifier and the timestamp are kept with the retained evidence so a log row can be
tied back to the run that produced it.

`evidence id`, `sentence text`, `proposed conclusion`, `unresolved issue` and `action owner`
stay in the export. `human conclusion` and `review time` are exported empty on purpose: the page
does not write them and does not time anybody.

`status` is the column that matters most, and it is never promoted on the way into the log.
`checked within scope` means every figure in the sentence carried a role the words gave it and
the comparison with the ledger agreed. It does not mean the sentence is true. `not checked`
means nothing in the sentence could be tied to the ledger and tested, which is not a pass.

## The eight columns the machine never fills

- `ask to the controller` opens on any `failed` row the preparer cannot clear, on any
  `needs review` row that is still unresolved, and on any reviewer row where the document is
  not on file.
- `reviewer answer` is written on the rows the reviewer works, which are the queue and the
  sentences returned as checked within scope. A row with no ask and no judgment question stays
  blank.
- `resolved` is `yes` only when the ask has an answer on file, or when the corrected sentence
  has been rechecked. A row where the arithmetic was corrected and the cause was not is `no`.
- `reviewer name`, `date` and `controller sign-off` are entered at step 5 of the protocol.

Two rows exist that the checker never produces. Every sentence returned as checked within scope
enters the reviewer queue's judgment step and is written into the log twice, once with `check`
set to `driver` and once with `check` set to `timing`, both with `result` set to `reviewer`.
Those are the two judgment questions, and a close with no such rows is a close where the second
pass was not run.

## The worked example in the template

The three example rows come from the Halyard Provisioning Group case in `cases/halyard-v4.json`
and in `drafts-2026-09-05-aina/EXERCISE-case-01-form-rev4.md`. Halyard does not exist and no
figure in it came from any real company or engagement.

The first row is the one to read before filling a log. The preparer corrected the figure, the
recomputation ties, and the row is still `resolved: no`, because what the $5,000 above the named
Coastal Grocers reserve is has not been established and no June reserve rollforward is on file.
A corrected number is not a supported cause. Until 13 September 2026 that row named a routine
monthly provision the ledger does not support and signed the line off, which taught the opposite
of the control.

## How the drill scores a reason

The drill exports the same distinction the log draws. It records the call a player made and the
basis they tapped, and it scores those separately.

Every card in `cases/` carries `basisKey`, the set of basis chips that are correct on that card.
A chip outside that set contradicts the key for that card. A reason counts as right when the
player tapped at least one chip in the key and no chip outside it. A card the key lets stand
carries `the figure and reason hold` and nothing else, so `wrong account` on a clean line is a
contradiction rather than a weak answer.

| Where it appears | What it says |
| --- | --- |
| The running pill | `Right 7 of 9`, the call score only, so the pill reads the same as it always did |
| The end screen | `Right call 12 of 14. Right reason 9 of 14.`, and the fresh case carries the same pair |
| The end screen, one line under the rank | That the points, the rank and the badges are read off the trained lines. The badges read the calls alone; an agreeing reason adds points, so it counts toward the rank |
| The coach section | A block naming every line where the call agreed with the key and the basis did not, with the chips the player tapped and the basis key beside them |
| Question B on the form | The reason score for both rounds, beside the attempt identifier |
| Question C on the form | The fresh case pair, and the reason verdict and basis key line by line |
| The downloadable record | `basisKey` and `reasonResult` on every one of the nineteen items, and `rightReason` beside `right` in both rounds |

The reason score is a compatibility check on the stated basis. It is not a rubric score, it does
not establish that a player reasoned, and it never moves the badges. Its points do count toward
the total the rank is read off, so the same calls with different reasons can land on different
ranks, and the rank is not a professional credential or a learning outcome. The
three-dimension reasoning rubric is scored by a person outside the page, and reviewer
disagreements with the key are retained rather than settled by it.

The reason score exists because a 13 September 2026 independent review completed the whole drill
while tapping `wrong account` on every one of the nineteen lines, and the page awarded 14 of 14
and 5 of 5. The same run now scores zero on reason, because no card in either case has an amount
booked in an account it does not belong in.

## What the two exports do not establish

Neither export is evidence of a learning gain, of time saved, or of an error prevented in real
work. The drill's numbers are answer-key agreement on a keyed exercise, and the checker's numbers
are coverage of a pasted memo. Published measures name which of the two files they came from,
and test attempts and incomplete attempts are excluded before anything is counted.
