# Raw AI draft, Kestrel IT Services, Prompt 1 run

Model: Claude Opus, via Claude Code, 13 September 2026.

Prompt given, verbatim. This is Prompt 1 exactly as checker.html assembles it with the Kestrel ledger in the ledger pane, a $25,000 floor, a 10 percent floor, the both-legs rule and the default zero-balance policy:

> Draft the month-end flux commentary for this close. Write the memo only; do not comment on the task.
>
> Close period: July 2026. Company: Kestrel IT Services, LLC.
> Commentary rule: a movement owes an explanation when the change is more than $25,000 and the percent of the prior balance is at least 10 percent (both legs, not either), and a line with a zero prior balance is treated as owing commentary on any movement (the default).
>
> LEDGER
> Kestrel IT Services, LLC
> Profit and Loss Comparison
> July 2026 compared with June 2026
>
> (tab) Jul 2026 / Jun 2026 / $ Change / % Change
> Income
>    4000 Recurring managed services 198,400.00 161,500.00 36,900.00 22.85 %
>    4100 Project and implementation revenue 96,400.00 38,900.00 57,500.00 147.81 %
> Total Income 294,800.00 200,400.00 94,400.00 47.11 %
> Cost of Goods Sold
>    5000 Subcontracted engineering 88,300.00 41,800.00 46,500.00 111.24 %
> Total Cost of Goods Sold 88,300.00 41,800.00 46,500.00 111.24 %
> Gross Profit 206,500.00 158,600.00 47,900.00 30.20 %
> Expenses
>    6000 Salaries and wages 88,500.00 88,500.00 0.00 0.00 %
>    6200 Software licences and hosting 57,900.00 22,600.00 35,300.00 156.19 %
>    6400 Client acquisition costs 14,200.00 4,900.00 9,300.00 189.80 %
> Total Expenses 160,600.00 116,000.00 44,600.00 38.45 %
> Net Operating Income 45,900.00 42,600.00 3,300.00 7.75 %
> Net Income 45,900.00 42,600.00 3,300.00 7.75 %
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

Inputs the model was given: the same ledger block, inside the prompt above. It had not read the sample memo that sits beside this ledger in checker.html, and it reported writing this answer with no file read and no search run.

Nothing below this line was edited. No line was added, removed, reordered or corrected.

---

1. 4000 Recurring managed services: prior $161,500.00, current $198,400.00, rose by $36,900.00, 22.85 percent, because no source on file (source: no source on file).
2. 4100 Project and implementation revenue: prior $38,900.00, current $96,400.00, rose by $57,500.00, 147.81 percent, because no source on file (source: no source on file).
3. 5000 Subcontracted engineering: prior $41,800.00, current $88,300.00, rose by $46,500.00, 111.24 percent, because no source on file (source: no source on file).
4. 6200 Software licences and hosting: prior $22,600.00, current $57,900.00, rose by $35,300.00, 156.19 percent, because no source on file (source: no source on file).

Two lines fell below the rule and carry no commentary.
