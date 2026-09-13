# Raw AI draft, Brightwater Dental Partners, Prompt 1 run

Model: Claude Opus, via Claude Code, 13 September 2026.

Prompt given, verbatim. This is Prompt 1 exactly as checker.html assembles it with the Brightwater ledger in the ledger pane, a $25,000 floor, a 10 percent floor, the both-legs rule and the default zero-balance policy:

> Draft the month-end flux commentary for this close. Write the memo only; do not comment on the task.
>
> Close period: June 2026. Company: Brightwater Dental Partners, PLLC.
> Commentary rule: a movement owes an explanation when the change is more than $25,000 and the percent of the prior balance is at least 10 percent (both legs, not either), and a line with a zero prior balance is treated as owing commentary on any movement (the default).
>
> LEDGER
> Line / Account / Prior / Current / Variance / Percent
> 4010 Patient service revenue, net 742,000 803,500 61,500 8.3%
> 4220 Orthodontic plan revenue 96,000 138,400 42,400 44.2%
> 5210 Dental supplies and lab fees 138,500 191,200 52,700 38.1%
> 6110 Hygienist wages 214,000 268,900 54,900 25.7%
> 6610 Marketing and patient outreach 18,400 24,100 5,700 31.0%
>
> Write one numbered line for every account that clears the rule, and nothing else. Each line takes exactly this shape:
>
> <n>. <account number> <account name>: prior <prior balance>, current <current balance>, <rose or fell or flat> by <change>, <percent> percent, because <one reason> (source: <the document, system or person the reason came from>).
>
> Rules for every line:
> - Write the account number first, exactly as the ledger prints it.
> - Write every figure in full dollars as the ledger prints them. No k, no M, no rounding to the nearest thousand, no restating in another unit.
> - Say what each figure is in words: "prior", "current", "by" for the change, and "percent" for the percent. A figure with no such word beside it cannot be checked and comes back unresolved.
> - Recompute the change and the percent from the two balances; do not copy a change column.
> - Use one direction word only, rose, fell or flat, and put it immediately before the change figure.
> - Give one reason, and name its source. Where nothing on file supports a reason, write "no source on file" rather than inventing one.
> - Do not write a second line about an account you have already covered.
>
> Then stop, except for one closing sentence naming how many lines fell below the rule and stating that they carry no commentary. No summary paragraph, no recommendations, no headings.
>
> A deterministic checker reads this memo next. It ties each sentence to a ledger line, reads what each figure is meant to be from the words beside it, and recomputes it. A line that drops the account number, abbreviates a figure, leaves a figure's role unsaid or carries two accounts at once comes back unresolved and goes to a person by hand.

Inputs the model was given: the same five account lines, inside the prompt above. It had not read the exercise memo, the facts on file or the key. The context that wrote it held nothing else, and it reported writing this answer with no file read and no search run.

Nothing below this line was edited. No line was added, removed, reordered or corrected.

---

1. 4220 Orthodontic plan revenue: prior $96,000, current $138,400, rose by $42,400, 44.2 percent, because no source on file (source: no source on file).
2. 5210 Dental supplies and lab fees: prior $138,500, current $191,200, rose by $52,700, 38.1 percent, because no source on file (source: no source on file).
3. 6110 Hygienist wages: prior $214,000, current $268,900, rose by $54,900, 25.7 percent, because no source on file (source: no source on file).

Two lines fell below the rule and carry no commentary.
