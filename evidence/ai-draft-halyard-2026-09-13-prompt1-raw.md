# Raw AI draft, Halyard Provisioning Group, Prompt 1 run

Model: Claude Opus, via Claude Code, 13 September 2026.

Prompt given, verbatim (Prompt 1 as checker.html assembles it, with the Halyard ledger, a $25,000 floor, a 10 percent floor and the both-legs rule):

> Draft the month-end flux commentary for this close. Write the memo only; do not comment on the task.
>
> Close period: June 2026 against May 2026. Company: Halyard Provisioning Group, Inc..
> Commentary rule: a movement owes an explanation when it clears $25,000 and 10 percent of the prior balance (both legs, not either).
>
> LEDGER
> [the fourteen Halyard account lines with prior and current balances, as printed in the exercise]
>
> Write one numbered line for every account that clears the rule, and nothing else. Each line takes exactly this shape:
>
> <n>. <account number> <account name>: prior <prior balance>, current <current balance>, <rose or fell or flat> <change>, <percent> percent, because <one reason> (source: <the document, system or person the reason came from>).
>
> Rules for every line:
> - Write the account number first, exactly as the ledger prints it.
> - Write every figure in full dollars as the ledger prints them. No k, no M, no rounding to the nearest thousand, no restating in another unit.
> - Recompute the change and the percent from the two balances; do not copy a change column.
> - Use one direction word only, rose, fell or flat, and put it immediately before the change figure, so "rose $42,400" or "flat $0". The direction is read against the figure standing beside it.
> - Give one reason, and name its source. Where nothing on file supports a reason, write "no source on file" rather than inventing one.
> - Do not write a second line about an account you have already covered.
>
> Then stop, except for one closing sentence naming how many lines fell below the rule and stating that they carry no commentary. No summary paragraph, no recommendations, no headings.
>
> A deterministic checker reads this memo next and ties every figure back to the ledger, so the shape above is not a preference. A line that drops the account number, abbreviates a figure or carries two accounts at once will come back unmatched and go to a human by hand.

Inputs the model was given: the same Halyard ledger block only. The model had not read the exercise memo, the challenge list, or the answer key when it wrote what follows.

Nothing below this line was edited. No line was added, removed, reordered or corrected.

---

1. 4100 Service revenue, equipment maintenance: prior $812,000, current $1,041,000, rose $229,000, 28.2 percent, because no source on file (source: no source on file).
2. 4200 Freight billed to customers: prior $186,000, current $121,000, fell $65,000, 34.9 percent, because no source on file (source: no source on file).
3. 5100 Inbound freight: prior $214,000, current $287,800, rose $73,800, 34.5 percent, because no source on file (source: no source on file).
4. 6000 Warehouse wages: prior $630,000, current $702,500, rose $72,500, 11.5 percent, because no source on file (source: no source on file).
5. 6200 Repairs and maintenance, depots: prior $41,000, current $118,600, rose $77,600, 189.3 percent, because no source on file (source: no source on file).
6. 6400 Bad debt expense: prior $15,000, current $62,000, rose $47,000, 313.3 percent, because no source on file (source: no source on file).
7. 7100 Interest expense: prior $61,200, current $92,400, rose $31,200, 51.0 percent, because no source on file (source: no source on file).

Seven lines fell below the rule and carry no commentary.
