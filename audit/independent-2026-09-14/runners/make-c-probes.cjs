// A1 independent audit, 14 September 2026: new probes in the neighbours of every class closed
// on the night of 13/14 September. Writes inputs/c-probes.json.
// req   = the statuses CHECKER.md at the tested head permits for the sentence named in `label`.
// basis = the clause it rests on. "silent:" marks a requirement the contract does not state, which
//         then rests on the clearance grammar's own rule (nothing risky left once every claim is
//         read) or on the third review's principle that ambiguous quantitative language is held.
const fs = require("fs"), path = require("path");
const RENT = "6100\tRent expense\t100000\t130000";
const TWO = RENT + "\n6200\tInsurance expense\t50000\t95000";
const MON = "Account\tMay 2026\tJune 2026\n6100\tRent expense\t100000\t130000";
const MON2 = "Account\tMay 2026\tJune 2026\n6100\tRent expense\t100000\t130000\n6200\tInsurance expense\t50000\t95000";
const QTR = "Account\tQ1 2026\tQ2 2026\n6100\tRent expense\t100000\t130000";
const HALF = "Account\tH1 2026\tH2 2026\n6100\tRent expense\t100000\t130000";
const PCUR = "Account\tPrior month\tThis month\n6100\tRent expense\t100000\t130000";
const LEVEL = "6100\tRent expense, level 3\t100000\t130000";
const NC = "not checked", NR = "needs review", F = "failed", C = "checked within scope";
const P = [];
let n = 0;
function p(cls, memo, req, basis, ledger, ratios) {
  n++;
  P.push({ id: "C" + String(n).padStart(3, "0"), cls, inputs: { ledger: ledger || RENT, memo, ratios: ratios || "" }, req, basis });
}
// ---- 1. the claim-and-reason boundary: a direction word smuggled into a reason
p("reason", "Rent expense rose $30,000 (it fell).", [F, NR], "direction: a reason that points back with 'it' is tested");
p("reason", "Rent expense rose $30,000 (the balance declined).", [F, NR], "direction: 'as the balance' points back");
p("reason", "Rent expense rose $30,000 because it fell.", [F, NR], "direction: 'because it' points back");
p("reason", "Rent expense rose $30,000 as the balance declined.", [F, NR], "the contract's own example of a reason pointing back");
p("reason", "Rent expense rose $30,000 since the account dropped.", [F, NR], "silent: 'the account' points back at the line");
p("reason", "Rent expense rose $30,000, after it declined.", [F, NR], "direction: 'after' opens a reason, 'it' points back");
p("reason", "Rent expense rose $30,000 on the fall in Rent expense.", [F, NR], "direction: the reason names the bound line");
p("reason", "Rent expense rose $30,000, so it fell.", [F, NR], "direction: 'so' opens a reason, 'it' points back");
p("reason", "Rent expense rose $30,000 though it dropped.", [F, NR], "direction: 'though' opens a contrast, 'it' points back");
p("reason", "Rent expense rose $30,000; it fell.", [F, NR], "direction: a clause of its own naming the line by 'it'");
p("reason", "Rent expense rose $30,000, which fell in June.", [F, NR], "silent: a relative clause about the line, plus an unbound month");
p("reason", "Because vacancy decreased, rent expense rose $30,000.", [C, NR], "a reason in front of the claim");
p("reason", "Due to a decrease in vacancy, rent expense rose $30,000.", [C, NR], "the same, with 'due to'");
p("reason", "Rent expense rose $30,000 on a decrease in vacancy and an increase in rates.", [C], "two reason nouns, neither naming a line");
p("reason", "Rent expense rose $30,000 per the “decline in vacancy” memo.", [C, NR], "silent: a direction noun inside a quoted title");
p("reason", "Rent expense rose $30,000 on the increase in Insurance expense.", [C, NR, F], "direction: the reason names one bound line and Insurance expense did rise; the structural rule wants a claim for it", TWO);
p("reason", "Rent expense rose $30,000 because Insurance expense fell.", [F, NR], "direction: the reason names Insurance expense, which rose", TWO);
p("reason", "Rent expense rose $30,000 on the lease; Insurance expense rose $45,000 on premiums.", [C], "two clauses, each with its own claim", TWO);
p("reason", "Rent expense rose $30,000 on a decrease in vacancy. Insurance expense fell $45,000 on premiums.", [F], "two sentences, the second false", TWO);
// ---- 2. size and share words, one step to the side of SIZE and HEDGE
p("size", "Rent expense rose $30,000, a meaningful increase.", [NR], "size: an adjective standing on the movement noun");
p("size", "Rent expense rose $30,000, a hefty increase.", [NR], "size: the same");
p("size", "Rent expense rose $30,000, an enormous increase.", [NR], "size: the same");
p("size", "Rent expense rose $30,000, a healthy step up.", [NR, C], "silent: a size adjective on a movement written as 'step up'");
p("size", "Rent expense rose $30,000, a steep climb.", [NR, C], "silent: a size noun the list does not carry");
p("size", "Rent expense rose $30,000, notably higher than May.", [NR], "size: a degree word on a comparative, and 'than'");
p("size", "Rent expense rose $30,000, appreciably above May.", [NR], "size: a degree word on a comparative");
p("size", "Rent expense rose $30,000; the increase was manageable.", [NR, C], "silent: a size adjective after the movement noun");
p("size", "Rent expense rose $30,000; the change was not small.", [NR], "size: an adjective on the movement, under a negation");
p("size", "Rent expense rose $30,000 on a tad more space.", [NR, C], "silent: a degree word on a comparative inside a reason");
p("size", "Rent expense rose $30,000 on outsized demand for space.", [C, NR], "size weak: it sizes the demand, not the movement");
p("size", "Rent expense rose $30,000 on a massive new lease.", [C, NR], "size weak: it sizes the lease");
p("share", "Rent expense rose $30,000, the lion's share of it on the new lease.", [NR], "share of the movement");
p("share", "Rent expense rose $30,000, a good chunk of it on the new lease.", [NR, C], "silent: a share phrase the list does not carry");
p("share", "Rent expense rose $30,000, nearly all of it on the new lease.", [NR], "share of the movement");
p("share", "Rent expense rose $30,000, the remainder on the new lease.", [NR, C], "silent: a share phrase");
p("share", "Rent expense rose $30,000, the balance of it on the new lease.", [NR, C], "silent: a share phrase");
p("share", "Rent expense rose $30,000, two-thirds of it on the new lease.", [NC], "1b fraction");
// ---- 3. hedges on a figure that is true
p("hedge", "Rent expense rose about $30,000.", [NR, C], "silent: an approximation word on a true figure; the third review asked for ambiguous quantitative language to be held");
p("hedge", "Rent expense rose approximately $30,000.", [NR, C], "silent: the same");
p("hedge", "Rent expense rose roughly $30,000.", [NR, C], "silent: the same");
p("hedge", "Rent expense rose circa $30,000.", [NR, C, NC], "silent: the same");
p("hedge", "Rent expense rose ~$30,000.", [NR, C, NC], "silent: a tilde in front of the figure");
p("hedge", "Rent expense rose $30,000 or so.", [NR, C], "silent: a hedge after the figure");
p("hedge", "Rent expense rose $30,000, give or take.", [NR, C], "silent: the same");
p("hedge", "Rent expense rose some $30,000.", [NR, C], "silent: 'some' in front of a figure");
p("hedge", "Rent expense rose close to $30,000.", [NR, C], "silent: a hedge that also bounds");
p("hedge", "Rent expense rose in the region of $30,000.", [NR, C], "silent: the same");
p("hedge", "Rent expense rose north of $30,000.", [NR, C], "silent: a bound written as a hedge");
p("hedge", "Rent expense rose upwards of $30,000.", [NR, C], "silent: the same");
p("hedge", "Rent expense rose on the order of $30,000.", [NR, C], "silent: the same");
p("hedge", "Rent expense rose about 30 percent.", [NR, C], "silent: a hedge on a true percent");
// ---- 4. currencies in unusual positions
p("currency", "Rent expense, in euros, rose 30,000.", [NC, NR], "1b a currency named in words");
p("currency", "In euro terms, rent expense rose $30,000.", [NR, NC], "lexicon currency: a qualifier away from the figure");
p("currency", "Rent expense rose $30,000 (USD).", [NC, NR], "1b USD beside the figure");
p("currency", "Rent expense rose $30,000 USD.", [NC, NR], "1b the same");
p("currency", "Rent expense rose $30,000 on the euro lease.", [NR, NC], "lexicon currency, strong, inside a reason");
p("currency", "Rent expense rose $30,000 per the FX table.", [NR], "lexicon currency: FX");
p("currency", "Rent expense rose $30,000, translated at the June rate.", [NR], "lexicon currency and an unbound month");
p("currency", "Rent expense rose 30,000 quid.", [NC], "1b a currency name");
p("currency", "Rent expense rose $30,000, or €27,000.", [NC], "1b a euro figure");
p("currency", "Rent expense rose $30,000 at the current exchange rate.", [NR], "the contract's own example");
p("currency", "Rent expense rose $30,000 on a dollar basis.", [NR], "lexicon basis: 'basis'");
// ---- 5. signs in unusual positions
p("sign", "Rent expense changed by 30,000 (F).", [NR, NC], "lexicon sign: (F)");
p("sign", "Rent expense changed by 30,000 (U).", [NR, NC], "lexicon sign: (U)");
p("sign", "Rent expense changed by +/- 30,000.", [NR, NC], "lexicon sign: a sign apart from its figure");
p("sign", "Rent expense changed by ±30,000.", [NR, NC], "lexicon sign: plus-minus");
p("sign", "Rent expense changed by - $30,000.", [NR, NC, F], "lexicon sign: a minus standing apart from its figure");
p("sign", "Rent expense rose $30,000+.", [NR, NC, C], "silent: a plus written after the figure");
p("sign", "Rent expense changed by ＋30,000.", [NR, NC, F], "silent: a fullwidth plus in front of a figure");
p("sign", "Rent expense rose $30,000, favourable to plan.", [NR], "lexicon sign: favourable, and basis: plan");
p("sign", "Rent expense rose $30,000, an adverse variance.", [NR], "lexicon sign: adverse");
p("sign", "A credit balance of $30,000 sits in Rent expense.", [NR, NC], "lexicon sign: credit balance");
p("sign", "Rent expense changed by −30,000.", [F], "1 a Unicode minus reads as a minus, and the ledger rose");
p("sign", "Rent expense rose $30,000 net of credits.", [NR], "lexicon quantity: net of");
// ---- 6. quarters and halves
p("quarter", "Rent expense rose $30,000 in Q2 2026.", [C], "a quarter the column labels name", QTR);
p("quarter", "Rent expense rose $30,000 in 2Q26.", [C, NR], "silent: the 2Q26 spelling against a Q2 2026 label", QTR);
p("quarter", "Rent expense rose $30,000 in April.", [NR], "a column covering a quarter names no single month", QTR);
p("quarter", "Rent expense rose $30,000 in the first half.", [NR], "halves are held whatever the labels say", QTR);
p("quarter", "Rent expense rose $30,000 quarter to date.", [NR], "QTD is part of a quarter and always held", QTR);
p("quarter", "Rent expense rose $30,000 year to date.", [NR], "period strong: YTD", QTR);
p("quarter", "Rent expense rose $30,000 in H2.", [NR], "halves are held whatever the labels say", HALF);
p("quarter", "Rent expense rose $30,000 in the second half of the year.", [NR], "the same", HALF);
p("quarter", "Rent expense rose $30,000 in Q2.", [NR], "labels that name halves do not name a quarter", HALF);
p("quarter", "Rent expense rose $30,000 in Q3.", [NR], "a quarter the labels contradict", QTR);
p("quarter", "Rent expense rose $30,000 in the June quarter.", [NR], "silent: a quarter named by its month, on a monthly ledger", MON);
p("quarter", "Rent expense rose $30,000 in the quarter ended 30 June.", [NR], "a quarter on a monthly ledger", MON);
p("quarter", "Rent expense rose $30,000 in Q2.", [NR], "labels read as months, not quarters", PCUR);
// ---- 7. periods bound, or not, by the column labels
p("period", "Rent expense rose $30,000 in June.", [C], "a month either column names", MON);
p("period", "Rent expense rose $30,000 in May.", [C], "the prior column's month", MON);
p("period", "Rent expense rose $30,000 in July.", [NR], "a month neither column names", MON);
p("period", "Rent expense rose $30,000 in June 2025.", [NR], "a year the labels contradict", MON);
p("period", "Rent expense rose $30,000 as of 30 June.", [C, NR], "a date the current column's month binds", MON);
p("period", "Rent expense rose $30,000 on 30 July.", [NR], "a date neither column binds", MON);
p("period", "Rent expense rose $30,000 over May.", [C, NR], "the prior column's label as the frame", MON);
p("period", "Rent expense rose $30,000 over June.", [NR], "measured from the wrong column", MON);
p("period", "Rent expense rose $30,000 compared with May.", [C, NR], "comparison introducing the ledger's own prior column", MON);
p("period", "Rent expense rose $30,000 versus May.", [C, NR], "the same", MON);
p("period", "Rent expense rose $30,000 vs. May 2026.", [C, NR], "the same, abbreviated, and never split after vs.", MON);
p("period", "Rent expense rose $30,000 from May to June.", [C, NR], "both column labels", MON);
p("period", "Rent expense rose $30,000 month over month.", [C], "labels two months in a row", MON);
p("period", "Rent expense rose $30,000 month over month.", [C], "labels read as months", PCUR);
p("period", "Rent expense rose $30,000 in June.", [NR], "labels name no month", PCUR);
p("period", "Rent expense rose $30,000 for the month.", [NR], "labels name no period", RENT);
p("period", "Rent expense rose $30,000 on an annual insurance premium.", [NR, C], "period strong: annual, where it gives the length of a premium");
p("period", "Rent expense rose $30,000 on a yearly cleaning contract.", [NR, C], "the length-of-contract exception, one word to the side");
p("period", "Rent expense rose $30,000 as the one-year lease began.", [C], "the contract's own example of the exception");
// ---- 8. one account, one claim, and names that bind late
p("binding", "Rent expense rose $30,000, unlike Insurance expense.", [NR], "comparison strong, and Insurance expense carries no claim", TWO);
p("binding", "Rent expense rose $30,000 on Insurance expense's renewal.", [NR], "a name binds wherever it stands, and carries no claim of its own", TWO);
p("binding", "Rent expense rose $30,000 per the “Insurance expense” schedule.", [NR], "a name inside quotes still binds", TWO);
p("binding", "Rent expense rose $30,000, while Insurance expense rose $45,000.", [C], "each account with its own claim", TWO);
p("binding", "Rent expense and Insurance expense both rose.", [NC], "no figures", TWO);
p("binding", "Rent expense rose $30,000 and Insurance expense followed.", [NR], "the contract's own structural example", TWO);
p("binding", "Rent expense, level 3, rose $30,000.", [C, NR], "silent: 'level' inside the bound account's own name", LEVEL);
p("binding", "Rent expense rose $30,000 at the Stable Yard depot.", [C, NR], "silent: 'Stable' inside a proper name");
p("binding", "Rent expense rose $30,000 on the Constant Contact subscription.", [C, NR], "silent: 'Constant' inside a product name");
p("binding", "Rent expense rose $30,000 at the Level 3 data centre.", [C, NR], "silent: 'Level' inside a place name");
// ---- 9. mixed sentences, one claim wrong among several
p("mixed", "Rent expense rose $30,000, or 30 percent, in June on the U.S. Treasury lease.", [C], "every claim true, the month bound, the stop inside a name", MON);
p("mixed", "Rent expense rose $30,000, or 31 percent, in June on the U.S. Treasury lease.", [F], "5 the percent is false", MON);
p("mixed", "Rent expense rose $30,000, or 30 percent, in June, and Insurance expense rose $45,000, or 90 percent, in June.", [C], "two true claims on two lines", MON2);
p("mixed", "Rent expense rose $30,000, or 30 percent, in June, and Insurance expense rose $45,000, or 91 percent, in June.", [F], "the second percent is false", MON2);
p("mixed", "Rent expense rose $30,000, or 30 percent, sharply, in June.", [NR], "a size word beside true figures", MON);
p("mixed", "Rent expense rose $30,000, or 31 percent, sharply, in June.", [F], "a failed figure keeps its status and gets no wording row", MON);
p("mixed", "Rent expense rose $30,000, or 30 percent, and clears both legs, roughly.", [NR, C], "silent: a threshold claim with a hedge on it");
p("mixed", "Rent expense rose $30,000, or 30 percent, and fails the dollar leg.", [F], "the threshold claim is false: $30,000 clears a $25,000 floor");
p("mixed", "Rent expense rose $30,000 in June; Insurance expense was stable at $95,000.", [NR], "one clear sentence and one sameness word", MON2);
p("mixed", "Rent expense rose $30,000 in June. Insurance expense rose $45,000 in June.", [C], "two sentences, both true and bound", MON2);
// ---- 10. a ratio the pane supplies, with and without a risk word
p("ratio", "The rent to insurance ratio was 136.8 percent.", [C, NR, NC], "2 a percent settled against a supplied ratio", TWO, "rent to insurance = (6100) / (6200)");
p("ratio", "The rent to insurance ratio was 136.8 percent, broadly.", [NR, NC], "a sameness weak word inside the claim", TWO, "rent to insurance = (6100) / (6200)");
p("ratio", "The rent to insurance ratio was 200.0 percent.", [F, NR, NC], "5 the ratio is 136.8 percent", TWO, "rent to insurance = (6100) / (6200)");
// ---- 11. sameness and no-change neighbours
p("sameness", "Rent expense was steady at $130,000.", [F, NR], "flat words are tested; 'steady' is in the flat list");
p("sameness", "Rent expense did not budge from $130,000.", [NR], "negation");
p("sameness", "Rent expense moved sideways at $130,000.", [NR], "sameness strong: sideways");
p("sameness", "Rent expense was rangebound at $130,000.", [NR, C], "silent: a sameness word the list does not carry");
p("sameness", "Rent expense was unremarkable at $130,000.", [NR, C], "silent: the same");
p("sameness", "Rent expense barely moved, rising $30,000.", [NR], "sameness strong: barely");
p("sameness", "Rent expense was flattish at $130,000.", [NR], "sameness strong: flattish");
p("sameness", "Rent expense held at $130,000.", [F], "a tested no-change phrase on a line that moved");
// ---- 12. one long sentence, for the reader under load
const filler = Array.from({ length: 40 }, (_, i) => "the schedule item " + (i % 2 ? "was reviewed" : "was noted")).join(", ");
p("long", "Rent expense rose $30,000, " + filler + ", in June on the U.S. Treasury lease.", [C], "a true sentence 400 words long, with the month bound", MON);
p("long", "Rent expense rose $30,000, " + filler + ", sharply in June.", [NR], "a size word at the end of a long sentence", MON);
fs.writeFileSync(path.join(__dirname, "..", "inputs", "c-probes.json"), JSON.stringify(P, null, 1));
console.log("wrote", P.length, "probes");
