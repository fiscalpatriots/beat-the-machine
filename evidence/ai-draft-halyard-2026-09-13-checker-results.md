# Checker results, both Halyard runs, 13 September 2026

Two runs of the same ledger through checker.html: the blind draft written from the ledger alone, and the Prompt 1 draft. Source exports kept beside this file as blind-run.csv and prompt1-run.csv.

---

# Checker results, blind draft (no prompt engineering)

Checker: checker.html from this repository, served locally at http://127.0.0.1:8765/checker.html and run in the Browser pane on 13 September 2026.

Settings used: close period June 2026 against May 2026, company Halyard Provisioning Group, Inc., dollar floor $25,000, percent floor 10 percent, both legs required.

Headline strip as the checker printed it: 14 lines checked, 2 arithmetic fails, 1 direction fail, 0 silent lines, 17 sentences for the reviewer.

Result counts across every row: below 7, clears 7, fail 3, info 8, pass 53, review 34.

Export method: the checker's Download CSV button, which writes the same rows as the Copy results as table button. Clipboard reads are blocked inside the Browser pane, so the CSV was used and reformatted as the table below with no change to any value.

| Line | Account | Sentence | Check | Result | Finding | Ask the controller |
| --- | --- | --- | --- | --- | --- | --- |
| 4000 | Product revenue, distribution | none | recompute | below | Change $372,000, 7.1% of the prior balance, no commentary owed |  |
| 4100 | Service revenue, equipment maintenance | none | recompute | clears | Change $229,000, 28.2% of the prior balance |  |
| 4200 | Freight billed to customers | none | recompute | clears | Change -$65,000, -34.9% of the prior balance |  |
| 5000 | Cost of product sold | none | recompute | below | Change $348,000, 8.9% of the prior balance, no commentary owed |  |
| 5100 | Inbound freight | none | recompute | clears | Change $73,800, 34.5% of the prior balance |  |
| 6000 | Warehouse wages | none | recompute | clears | Change $72,500, 11.5% of the prior balance |  |
| 6100 | Fleet fuel | none | recompute | below | Change -$5,200, -5.4% of the prior balance, no commentary owed |  |
| 6200 | Repairs and maintenance, depots | none | recompute | clears | Change $77,600, 189.3% of the prior balance |  |
| 6300 | Software subscriptions | none | recompute | below | Change $1,600, 5.6% of the prior balance, no commentary owed |  |
| 6400 | Bad debt expense | none | recompute | clears | Change $47,000, 313.3% of the prior balance |  |
| 6500 | Professional fees | none | recompute | below | Change -$7,500, -13.6% of the prior balance, no commentary owed |  |
| 7000 | Depreciation | none | recompute | below | Change $0, 0.0% of the prior balance, no commentary owed |  |
| 7100 | Interest expense | none | recompute | clears | Change $31,200, 51.0% of the prior balance |  |
| 7400 | Inventory shrink adjustment | none | recompute | below | Change $2,500, 39.1% of the prior balance, no commentary owed |  |
| none | none | S1 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| none | none | S2 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| none | none | S3 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 4000, 4100 | Product revenue, distribution; Service revenue, equipment maintenance | S4 | match | pass | 4000 Product revenue, distribution; 4100 Service revenue, equipment maintenance (by a word in the account name) |  |
| 4000 | Product revenue, distribution | S5 | match | pass | 4000 Product revenue, distribution (by account number) |  |
| 4100 | Service revenue, equipment maintenance | S6 | match | pass | 4100 Service revenue, equipment maintenance (by account number) |  |
| 4200 | Freight billed to customers | S7 | match | pass | 4200 Freight billed to customers (by account number) |  |
| 5000 | Cost of product sold | S8 | match | pass | 5000 Cost of product sold (by account name) |  |
| 5000 | Cost of product sold | S9 | match | pass | 5000 Cost of product sold (by account number) |  |
| 4000, 4200, 5000 | Product revenue, distribution; Freight billed to customers; Cost of product sold | S10 | match | pass | 4000 Product revenue, distribution; 4200 Freight billed to customers; 5000 Cost of product sold (by a word in the account name) |  |
| 5100 | Inbound freight | S11 | match | pass | 5100 Inbound freight (by account number) |  |
| none | none | S12 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 6000 | Warehouse wages | S13 | match | pass | 6000 Warehouse wages (by account number) |  |
| none | none | S14 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 6100 | Fleet fuel | S15 | match | pass | 6100 Fleet fuel (by account number) |  |
| none | none | S16 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 6200 | Repairs and maintenance, depots | S17 | match | pass | 6200 Repairs and maintenance, depots (by account number) |  |
| 6300 | Software subscriptions | S18 | match | pass | 6300 Software subscriptions (by account number) |  |
| none | none | S19 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 6400 | Bad debt expense | S20 | match | pass | 6400 Bad debt expense (by account number) |  |
| 6500 | Professional fees | S21 | match | pass | 6500 Professional fees (by account number) |  |
| 7000 | Depreciation | S22 | match | pass | 7000 Depreciation (by account number) |  |
| 7400 | Inventory shrink adjustment | S23 | match | pass | 7400 Inventory shrink adjustment (by account number) |  |
| none | none | S24 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| none | none | S25 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 7100 | Interest expense | S26 | match | pass | 7100 Interest expense (by account number) |  |
| none | none | S27 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 6400 | Bad debt expense | S28 | match | pass | 6400 Bad debt expense (by account name) |  |
| 6400 | Bad debt expense | S29 | match | pass | 6400 Bad debt expense (by account name) |  |
| none | none | S30 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 4000, 4100 | Product revenue, distribution; Service revenue, equipment maintenance | S4 | arithmetic | pass | This sentence carries no dollar figure and no percent, so there is nothing to recompute. |  |
| 4000 | Product revenue, distribution | S5 | arithmetic | pass | $372,000 is the change on 4000 Product revenue, distribution. 7.1 percent ties to 4000 Product revenue, distribution moved 7.1%. |  |
| 4100 | Service revenue, equipment maintenance | S6 | arithmetic | pass | $229,000 is the change on 4100 Service revenue, equipment maintenance. 28.2 percent ties to 4100 Service revenue, equipment maintenance moved 28.2%. |  |
| 4200 | Freight billed to customers | S7 | arithmetic | pass | ($65,000) is the change on 4200 Freight billed to customers. -34.9 percent ties to 4200 Freight billed to customers moved -34.9%. |  |
| 5000 | Cost of product sold | S8 | arithmetic | pass | This sentence carries no dollar figure and no percent, so there is nothing to recompute. |  |
| 5000 | Cost of product sold | S9 | arithmetic | pass | $348,000 is the change on 5000 Cost of product sold. 8.9 percent ties to 5000 Cost of product sold moved 8.9%. |  |
| 4000, 4200, 5000 | Product revenue, distribution; Freight billed to customers; Cost of product sold | S10 | arithmetic | review | 25.0 percent is not a line percent; nearest values: 4200 Freight billed to customers percent change -34.9%; 5000 Cost of product sold percent change 8.9%; 4000 Product revenue, distribution percent change 7.1%. 23.8 percent is not a line percent; nearest values: 4200 Freight billed to customers percent change -34.9%; 5000 Cost of product sold percent change 8.9%; 4000 Product revenue, distribution percent change 7.1%. | Confirm what this percent is measuring, since it is not the movement on the line. |
| 5100 | Inbound freight | S11 | arithmetic | pass | $73,800 is the change on 5100 Inbound freight. 34.5 percent ties to 5100 Inbound freight moved 34.5%. |  |
| 6000 | Warehouse wages | S13 | arithmetic | pass | $72,500 is the change on 6000 Warehouse wages. 11.5 percent ties to 6000 Warehouse wages moved 11.5%. |  |
| 6100 | Fleet fuel | S15 | arithmetic | pass | ($5,200) is the change on 6100 Fleet fuel. -5.4 percent ties to 6100 Fleet fuel moved -5.4%. |  |
| 6200 | Repairs and maintenance, depots | S17 | arithmetic | pass | $77,600 is the change on 6200 Repairs and maintenance, depots. 189.3 percent ties to 6200 Repairs and maintenance, depots moved 189.3%. |  |
| 6300 | Software subscriptions | S18 | arithmetic | pass | $1,600 is the change on 6300 Software subscriptions. 5.6 percent ties to 6300 Software subscriptions moved 5.6%. |  |
| 6400 | Bad debt expense | S20 | arithmetic | pass | $47,000 is the change on 6400 Bad debt expense. 313.3 percent ties to 6400 Bad debt expense moved 313.3%. |  |
| 6500 | Professional fees | S21 | arithmetic | pass | ($7,500) is the change on 6500 Professional fees. -13.6 percent ties to 6500 Professional fees moved -13.6%. |  |
| 7000 | Depreciation | S22 | arithmetic | pass | $0 is the change on 7000 Depreciation. |  |
| 7400 | Inventory shrink adjustment | S23 | arithmetic | pass | $2,500 is the change on 7400 Inventory shrink adjustment. 39.1 percent ties to 7400 Inventory shrink adjustment moved 39.1%. |  |
| 7100 | Interest expense | S26 | arithmetic | pass | $31,200 is the change on 7100 Interest expense. 51.0 percent ties to 7100 Interest expense moved 51.0%. |  |
| 6400 | Bad debt expense | S28 | arithmetic | fail | memo says $536,000; ledger current balance is $62,000. memo says $188,500; ledger current balance is $62,000. 8.6 percent is not a line percent; nearest values: 6400 Bad debt expense percent change 313.3%. 18.8 percent is not a line percent; nearest values: 6400 Bad debt expense percent change 313.3%. | Which figure is right, the memo or the ledger, and where did the memo's number come from? |
| 6400 | Bad debt expense | S29 | arithmetic | fail | memo says $105,500; ledger current balance is $62,000. -10.2 percent is not a line percent; nearest values: 6400 Bad debt expense percent change 313.3%. | Which figure is right, the memo or the ledger, and where did the memo's number come from? |
| 4000, 4100 | Product revenue, distribution; Service revenue, equipment maintenance | S4 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 4000 | Product revenue, distribution | S5 | direction | pass | "higher" agrees with 4000 Product revenue, distribution. |  |
| 4100 | Service revenue, equipment maintenance | S6 | direction | pass | "growth" agrees with 4100 Service revenue, equipment maintenance. |  |
| 4200 | Freight billed to customers | S7 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 5000 | Cost of product sold | S8 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 5000 | Cost of product sold | S9 | direction | pass | "increase" agrees with 5000 Cost of product sold. |  |
| 4000, 4200, 5000 | Product revenue, distribution; Freight billed to customers; Cost of product sold | S10 | direction | pass | "increases" agrees with the matched line. |  |
| 5100 | Inbound freight | S11 | direction | pass | "increases" agrees with 5100 Inbound freight. |  |
| 6000 | Warehouse wages | S13 | direction | pass | "higher" agrees with 6000 Warehouse wages. |  |
| 6100 | Fleet fuel | S15 | direction | pass | "lower" agrees with 6100 Fleet fuel. |  |
| 6200 | Repairs and maintenance, depots | S17 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 6300 | Software subscriptions | S18 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 6400 | Bad debt expense | S20 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 6500 | Professional fees | S21 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 7000 | Depreciation | S22 | direction | pass | This sentence makes no claim about which way the account moved. |  |
| 7400 | Inventory shrink adjustment | S23 | direction | pass | "higher" agrees with 7400 Inventory shrink adjustment. |  |
| 7100 | Interest expense | S26 | direction | pass | "higher" agrees with 7100 Interest expense. |  |
| 6400 | Bad debt expense | S28 | direction | pass | "increased" agrees with the matched line; "growth" agrees with the matched line. |  |
| 6400 | Bad debt expense | S29 | direction | fail | the memo says "declined" but 6400 Bad debt expense rose. | Which way did this account actually move, and does the driver still hold once the sign is right? |
| 4000 | Product revenue, distribution | S5 | threshold | info | No commentary owed; fine if correct. 4000 Product revenue, distribution moved $372,000, 7.1%, which does not clear the rule. |  |
| 5000 | Cost of product sold | S8 | threshold | info | No commentary owed; fine if correct. 5000 Cost of product sold moved $348,000, 8.9%, which does not clear the rule. |  |
| 5000 | Cost of product sold | S9 | threshold | info | No commentary owed; fine if correct. 5000 Cost of product sold moved $348,000, 8.9%, which does not clear the rule. |  |
| 6100 | Fleet fuel | S15 | threshold | info | No commentary owed; fine if correct. 6100 Fleet fuel moved -$5,200, -5.4%, which does not clear the rule. |  |
| 6300 | Software subscriptions | S18 | threshold | info | No commentary owed; fine if correct. 6300 Software subscriptions moved $1,600, 5.6%, which does not clear the rule. |  |
| 6500 | Professional fees | S21 | threshold | info | No commentary owed; fine if correct. 6500 Professional fees moved -$7,500, -13.6%, which does not clear the rule. |  |
| 7000 | Depreciation | S22 | threshold | info | No commentary owed; fine if correct. 7000 Depreciation moved $0, 0.0%, which does not clear the rule. |  |
| 7400 | Inventory shrink adjustment | S23 | threshold | info | No commentary owed; fine if correct. 7400 Inventory shrink adjustment moved $2,500, 39.1%, which does not clear the rule. |  |
| 4000, 4100 | Product revenue, distribution; Service revenue, equipment maintenance | S4 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 4000 | Product revenue, distribution | S5 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 4100 | Service revenue, equipment maintenance | S6 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 4200 | Freight billed to customers | S7 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 5000 | Cost of product sold | S8 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 5000 | Cost of product sold | S9 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 4000, 4200, 5000 | Product revenue, distribution; Freight billed to customers; Cost of product sold | S10 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 5100 | Inbound freight | S11 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6000 | Warehouse wages | S13 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6100 | Fleet fuel | S15 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6200 | Repairs and maintenance, depots | S17 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6300 | Software subscriptions | S18 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6400 | Bad debt expense | S20 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6500 | Professional fees | S21 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 7000 | Depreciation | S22 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 7400 | Inventory shrink adjustment | S23 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 7100 | Interest expense | S26 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 4000 | Product revenue, distribution | none | read together | review | Read together: 3 sentences on this account (S4, S5, S10). The checker does not test them against each other. | Do these sentences agree with one another, and if not, which one holds? |
| 4100 | Service revenue, equipment maintenance | none | read together | review | Read together: 2 sentences on this account (S4, S6). The checker does not test them against each other. | Do these sentences agree with one another, and if not, which one holds? |
| 4200 | Freight billed to customers | none | read together | review | Read together: 2 sentences on this account (S7, S10). The checker does not test them against each other. | Do these sentences agree with one another, and if not, which one holds? |
| 5000 | Cost of product sold | none | read together | review | Read together: 3 sentences on this account (S8, S9, S10). The checker does not test them against each other. | Do these sentences agree with one another, and if not, which one holds? |
| 6400 | Bad debt expense | none | read together | review | Read together: 3 sentences on this account (S20, S28, S29). The checker does not test them against each other. | Do these sentences agree with one another, and if not, which one holds? |


---

# Checker results, Prompt 1 draft

Checker: checker.html from this repository, served locally at http://127.0.0.1:8765/checker.html and run in the Browser pane on 13 September 2026.

Settings used: close period June 2026 against May 2026, company Halyard Provisioning Group, Inc., dollar floor $25,000, percent floor 10 percent, both legs required.

Headline strip as the checker printed it: 14 lines checked, 0 arithmetic fails, 0 direction fails, 0 silent lines, 7 sentences for the reviewer.

Result counts across every row: below 7, clears 7, pass 21, review 8.

Export method: the checker's Download CSV button, which writes the same rows as the Copy results as table button. Clipboard reads are blocked inside the Browser pane, so the CSV was used and reformatted as the table below with no change to any value.

| Line | Account | Sentence | Check | Result | Finding | Ask the controller |
| --- | --- | --- | --- | --- | --- | --- |
| 4000 | Product revenue, distribution | none | recompute | below | Change $372,000, 7.1% of the prior balance, no commentary owed |  |
| 4100 | Service revenue, equipment maintenance | none | recompute | clears | Change $229,000, 28.2% of the prior balance |  |
| 4200 | Freight billed to customers | none | recompute | clears | Change -$65,000, -34.9% of the prior balance |  |
| 5000 | Cost of product sold | none | recompute | below | Change $348,000, 8.9% of the prior balance, no commentary owed |  |
| 5100 | Inbound freight | none | recompute | clears | Change $73,800, 34.5% of the prior balance |  |
| 6000 | Warehouse wages | none | recompute | clears | Change $72,500, 11.5% of the prior balance |  |
| 6100 | Fleet fuel | none | recompute | below | Change -$5,200, -5.4% of the prior balance, no commentary owed |  |
| 6200 | Repairs and maintenance, depots | none | recompute | clears | Change $77,600, 189.3% of the prior balance |  |
| 6300 | Software subscriptions | none | recompute | below | Change $1,600, 5.6% of the prior balance, no commentary owed |  |
| 6400 | Bad debt expense | none | recompute | clears | Change $47,000, 313.3% of the prior balance |  |
| 6500 | Professional fees | none | recompute | below | Change -$7,500, -13.6% of the prior balance, no commentary owed |  |
| 7000 | Depreciation | none | recompute | below | Change $0, 0.0% of the prior balance, no commentary owed |  |
| 7100 | Interest expense | none | recompute | clears | Change $31,200, 51.0% of the prior balance |  |
| 7400 | Inventory shrink adjustment | none | recompute | below | Change $2,500, 39.1% of the prior balance, no commentary owed |  |
| 4100 | Service revenue, equipment maintenance | 1 | match | pass | 4100 Service revenue, equipment maintenance (by account number) |  |
| 4200 | Freight billed to customers | 2 | match | pass | 4200 Freight billed to customers (by account number) |  |
| 5100 | Inbound freight | 3 | match | pass | 5100 Inbound freight (by account number) |  |
| 6000 | Warehouse wages | 4 | match | pass | 6000 Warehouse wages (by account number) |  |
| 6200 | Repairs and maintenance, depots | 5 | match | pass | 6200 Repairs and maintenance, depots (by account number) |  |
| 6400 | Bad debt expense | 6 | match | pass | 6400 Bad debt expense (by account number) |  |
| 7100 | Interest expense | 7 | match | pass | 7100 Interest expense (by account number) |  |
| none | none | S8 | match | review | No account number, no name and no amount in this sentence ties to a ledger line. | Which account is this sentence about, and what amount does it rest on? |
| 4100 | Service revenue, equipment maintenance | 1 | arithmetic | pass | $812,000 is the prior balance on 4100 Service revenue, equipment maintenance. $1,041,000 is the current balance on 4100 Service revenue, equipment maintenance. $229,000 is the change on 4100 Service revenue, equipment maintenance. 28.2 percent ties to 4100 Service revenue, equipment maintenance moved 28.2%. |  |
| 4200 | Freight billed to customers | 2 | arithmetic | pass | $186,000 is the prior balance on 4200 Freight billed to customers. $121,000 is the current balance on 4200 Freight billed to customers. $65,000 is the change on 4200 Freight billed to customers. 34.9 percent ties to 4200 Freight billed to customers moved -34.9%. |  |
| 5100 | Inbound freight | 3 | arithmetic | pass | $214,000 is the prior balance on 5100 Inbound freight. $287,800 is the current balance on 5100 Inbound freight. $73,800 is the change on 5100 Inbound freight. 34.5 percent ties to 5100 Inbound freight moved 34.5%. |  |
| 6000 | Warehouse wages | 4 | arithmetic | pass | $630,000 is the prior balance on 6000 Warehouse wages. $702,500 is the current balance on 6000 Warehouse wages. $72,500 is the change on 6000 Warehouse wages. 11.5 percent ties to 6000 Warehouse wages moved 11.5%. |  |
| 6200 | Repairs and maintenance, depots | 5 | arithmetic | pass | $41,000 is the prior balance on 6200 Repairs and maintenance, depots. $118,600 is the current balance on 6200 Repairs and maintenance, depots. $77,600 is the change on 6200 Repairs and maintenance, depots. 189.3 percent ties to 6200 Repairs and maintenance, depots moved 189.3%. |  |
| 6400 | Bad debt expense | 6 | arithmetic | pass | $15,000 is the prior balance on 6400 Bad debt expense. $62,000 is the current balance on 6400 Bad debt expense. $47,000 is the change on 6400 Bad debt expense. 313.3 percent ties to 6400 Bad debt expense moved 313.3%. |  |
| 7100 | Interest expense | 7 | arithmetic | pass | $61,200 is the prior balance on 7100 Interest expense. $92,400 is the current balance on 7100 Interest expense. $31,200 is the change on 7100 Interest expense. 51.0 percent ties to 7100 Interest expense moved 51.0%. |  |
| 4100 | Service revenue, equipment maintenance | 1 | direction | pass | "rose" agrees with 4100 Service revenue, equipment maintenance. |  |
| 4200 | Freight billed to customers | 2 | direction | pass | "fell" agrees with 4200 Freight billed to customers. |  |
| 5100 | Inbound freight | 3 | direction | pass | "rose" agrees with 5100 Inbound freight. |  |
| 6000 | Warehouse wages | 4 | direction | pass | "rose" agrees with 6000 Warehouse wages. |  |
| 6200 | Repairs and maintenance, depots | 5 | direction | pass | "rose" agrees with 6200 Repairs and maintenance, depots. |  |
| 6400 | Bad debt expense | 6 | direction | pass | "rose" agrees with 6400 Bad debt expense. |  |
| 7100 | Interest expense | 7 | direction | pass | "rose" agrees with 7100 Interest expense. |  |
| 4100 | Service revenue, equipment maintenance | 1 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 4200 | Freight billed to customers | 2 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 5100 | Inbound freight | 3 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6000 | Warehouse wages | 4 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6200 | Repairs and maintenance, depots | 5 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 6400 | Bad debt expense | 6 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |
| 7100 | Interest expense | 7 | reviewer | review | The arithmetic and the direction hold. What is left is judgment, and the checker does not make it. | Is the driver named here supported by anything on file? Is the period right (nothing pulled forward or deferred)? |

