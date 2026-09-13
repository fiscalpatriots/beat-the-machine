# Raw AI draft, Kestrel IT Services, blind run

Model: Claude Opus, via Claude Code, 13 September 2026.

Prompt given, verbatim, with the input block that sat above it:

> A line owes commentary only when it clears both $25,000 and 10 percent.
>
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
> Write the month-end variance commentary for July against June for the accounts that need explaining, one line per account, with the amount, the percent and the reason.

Inputs the model was given: the ledger block as the checker's Kestrel sample prints it, in the shape of a QuickBooks Profit and Loss Comparison export, with the title block, six accounts, the subtotals, and the threshold rule above it. Nothing else.

Why this one was run in a fresh context. The checker file that holds the Kestrel ledger also holds a sample memo with drivers written into it, and the session running this work had read that file. A blind draft written from that session would have been borrowing those drivers rather than producing its own, so the drafting was handed to a context that held only the block above. It reported its tool calls: it searched two paths for any Kestrel material, found none, read no file for content, and wrote its answer.

Two earlier passes at this same prompt were discarded before this one and are not the record. The first told the model not to look anything up; the second told it to use no tool but Write. Both of those sentences tell a model that no source exists, which is the restraint the second prompt is supposed to supply, so neither was a fair blind run. The draft below carries no such sentence.

Nothing below this line was edited. No line was added, removed, reordered or corrected.

---

4000 Recurring managed services rose $36,900, or 22.85 percent, to $198,400. The statement does not carry the cause, so the driver has to come from the July billing register: confirm how much is new agreements that began in July, how much is contracted rate increases on existing clients, and whether any of it is June service billed late.

4100 Project and implementation revenue rose $57,500, or 147.81 percent, to $96,400, the largest movement on the statement. Confirm from the project billing detail which engagements hit the milestones invoiced in July, and flag how much of the increase is non-recurring, because only the managed services base carries into August.

5000 Subcontracted engineering rose $46,500, or 111.24 percent, to $88,300, moving with project revenue in the same month. Gross margin fell from 79.14 percent in June to 70.05 percent in July, so confirm from the subcontractor invoices how much of the July cost sits against the projects billed in July and whether any July cost belongs to work still unbilled at month end.

6200 Software licences and hosting rose $35,300, or 156.19 percent, to $57,900. Confirm whether an annual or multi-month renewal was paid inside July. If it was, the charge covers a term rather than the month, and it belongs in prepaid expense amortised across that term, which would change both this month and the months it covers.
