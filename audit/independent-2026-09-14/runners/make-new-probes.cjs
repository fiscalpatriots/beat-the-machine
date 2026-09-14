// A1 independent audit, 13 September 2026: new checker probes. Writes inputs/a1-probes.json.
// req   = the statuses the published CHECKER.md contract (head 71d457b) permits for S1.
// basis = the clause the requirement rests on. "silent:" marks a requirement the contract does not
//         state in words; it rests on 1b's catch-all ("every other piece of quantitative language")
//         or on the status table ("every quantitative expression ... accounted for").
// Invisible and look-alike characters are written as \u escapes so the file reads plainly.
const fs = require("fs"), path = require("path");
const RENT = "6100\tRent expense\t100000\t130000";                       // the third review's ledger
const TWO = RENT + "\n6200\tInsurance expense\t50000\t95000";
const L2 = "4300\tConsulting revenue\t240000\t180000\n6700\tTravel expense\t12000\t12000\n6800\tUtilities expense\t50000\t50150"; // A1's own ledger
const NC = "not checked", NR = "needs review", F = "failed", C = "checked within scope";
const P = [];
let n = 0;
function p(cls, memo, req, basis, ledger) {
  n++;
  P.push({ id: "A" + String(n).padStart(3, "0"), cls, inputs: { ledger: ledger || RENT, memo, ratios: "" }, req, basis });
}
// ---- multipliers and fold words (rent moved +30,000, +30 percent)
p("multiplier", "Rent expense rose $30,000, or 1.3x the prior balance.", [NC, F], "1b multiplier (3x listed)");
p("multiplier", "Rent expense rose $30,000 and grew 1.3-fold.", [NC, F], "1b multiplier (two-fold listed)");
p("multiplier", "Rent expense rose $30,000 and grew twofold.", [NC, F], "1b multiplier (twofold listed)");
p("multiplier", "Rent expense rose $30,000 and grew by a third.", [NC, F], "1b fraction");
p("multiplier", "Rent expense rose $30,000 and was up by half.", [NC, F], "1b fraction");
p("multiplier", "Rent expense rose $30,000, a 1.3 times increase.", [NC, F], "1b multiplier (three times listed)");
p("multiplier", "Rent expense quadrupled to $130,000.", [NC, F], "1b multiplier");
p("multiplier", "Rent expense rose $30,000 and more than doubled.", [NC, F], "1b multiplier");
p("multiplier", "Rent expense rose $30,000, or x1.3 the prior month.", [NC, F], "1b number glued to letters");
p("multiplier", "Rent expense rose $30,000, roughly three tenths of the May balance.", [NC, F], "1b fraction");
p("multiplier", "Rent expense rose $30,000, a threefold jump.", [NC, F], "1b multiplier");
p("multiplier", "Consulting revenue fell $60,000 and was halved.", [NC, F], "1b multiplier (halved listed)", L2);
p("multiplier", "Consulting revenue fell $60,000, down by a quarter.", [NC, F], "1b fraction (a quarter of listed)", L2);
p("multiplier", "Consulting revenue fell $60,000, or 0.75x of May.", [NC, F], "1b multiplier", L2);
p("multiplier", "Rent expense rose $30,000, or 1.5 times.", [NC, F], "1b multiplier");
// ---- no-change and near-no-change
p("nochange", "Rent expense was flat at $130,000.", [F], "no-change: flat tested within half a percent");
p("nochange", "Rent expense held steady at $130,000.", [F], "no-change: steady listed");
p("nochange", "Rent expense was essentially flat at $130,000.", [F, NC], "no-change: flat listed");
p("nochange", "Rent expense was roughly unchanged at $130,000.", [F, NC], "no-change: unchanged listed");
p("nochange", "Rent expense was broadly stable at $130,000.", [F, NC, NR], "silent: 'stable' not listed; a green result clears a false no-change claim");
p("nochange", "Rent expense was level at $130,000.", [F, NC, NR], "silent: 'level with' listed, 'level at' not");
p("nochange", "Rent expense was consistent with May at $130,000.", [F, NC, NR], "silent: no-change claim outside the list");
p("nochange", "Rent expense was in line with May at $130,000.", [F, NC, NR], "silent: no-change claim outside the list");
p("nochange", "Rent expense showed no material change at $130,000.", [F, NR], "negation, or the 'no change' idiom");
p("nochange", "Rent expense was virtually unchanged from May at $130,000.", [F], "no-change: unchanged listed");
p("nochange", "Rent expense was flat.", [F, NC], "no figure: not checked; flat against a moved line may fail");
p("nochange", "Rent expense remained flat month over month.", [F, NC], "no figure; remained flat listed");
p("nochange", "Travel expense was unchanged at $12,000.", [C], "no-change passes on a line that did not move", L2);
p("nochange", "Travel expense rose $150.", [F], "a dollar figure against zero movement", L2);
p("nochange", "Utilities expense was flat at $50,150.", [C], "flat within half a percent (0.3 percent)", L2);
p("nochange", "Utilities expense was unchanged at $50,150.", [F], "unchanged is tested to the half cent", L2);
p("nochange", "Utilities expense held steady, up $150.", [C, NR], "steady within half a percent and up $150 ties", L2);
p("nochange", "Consulting revenue was stable at $180,000.", [F, NC, NR], "silent: 'stable' not listed", L2);
// ---- approximations
p("approx", "Rent expense rose about $32,000.", [F, NR, NC], "5 unrounded comparison; approximation words are not in the grammar");
p("approx", "Rent expense rose roughly $29,000.", [F, NR, NC], "5 unrounded");
p("approx", "Rent expense rose nearly $31,000.", [F, NR, NC], "5 unrounded");
p("approx", "Rent expense rose just over $30,000.", [NR, F, NC], "1d bound ('and the like'); P18 'more than' is needs review");
p("approx", "Rent expense rose by almost $30,000.", [NR, F, NC], "1d bound ('and the like')");
p("approx", "Rent expense rose by well over $30,000.", [NR, F, NC], "1d bound");
p("approx", "Rent expense rose by up to $30,000.", [NR, F, NC], "1d bound");
p("approx", "Rent expense rose approximately 30 percent.", [C], "a true percent");
p("approx", "Rent expense rose by about 25 percent.", [F, NR, NC], "5 unrounded");
p("approx", "Consulting revenue fell by about $55,000.", [F, NR, NC], "5 unrounded", L2);
p("approx", "Consulting revenue fell by a little under $60,000.", [NR, F, NC], "1d bound", L2);
// ---- ranges
p("range", "Rent expense rose between $25,000 and $35,000.", [NR, NC, F], "silent: a range is neither figure");
p("range", "Rent expense rose between 25 and 35 percent.", [NR, NC, F], "1b other run of digits");
p("range", "Rent expense rose $25,000-$35,000.", [NR, NC, F], "silent: a range");
p("range", "Rent expense rose 20-40%.", [NR, NC, F], "silent: a range");
p("range", "Rent expense rose in the range of $28,000 to $32,000.", [NR, NC, F], "silent: a range");
p("range", "Rent expense rose 29 to 31 percent.", [NR, NC, F], "1b other run of digits");
// ---- suffixes and scale
p("scale", "Rent expense rose $0.03 million.", [C, NC], "1 the $1.2M form; 1b scale word");
p("scale", "Rent expense rose 30 thousand dollars.", [NC], "1b '30 thousand' listed");
p("scale", "Rent expense rose $30 thousand.", [NC], "1b scale word ($30.0 thousand listed)");
p("scale", "Rent expense rose $0.03M.", [C], "1 the $1.2M form");
p("scale", "Rent expense rose $3M.", [F], "1 the $1.2M form, wrong value");
p("scale", "Rent expense rose $30 000.", [NC, F], "1 thousands commas only; space grouping");
p("scale", "Rent expense rose $30.000.", [NC, F], "1 decimals: $30.000 is thirty dollars");
p("scale", "Rent expense rose $30 grand.", [NC, F], "1b scale word");
p("scale", "Rent expense rose $30,000k.", [F, NC], "1 the k form: thirty million");
p("scale", "Rent expense rose 30,000 dollars.", [C], "1 a bare number with its unit");
p("scale", "Rent expense rose $30 thou.", [NC, F], "1b scale word");
p("scale", "Consulting revenue fell $0.06MM.", [NC, F, C], "1b scale (MM)", L2);
p("scale", "Consulting revenue fell $60 K.", [NC, F, C], "1 the k form with a space", L2);
// ---- parentheses negatives and accounting formats
p("sign", "Rent expense changed by (30,000).", [F], "1 parentheses negative; 5 sign clash");
p("sign", "Rent expense rose 30,000 CR.", [NC, NR, F], "silent: a CR indicator is a sign the words gave");
p("sign", "Rent expense moved $30,000 DR.", [NC, NR, C], "silent: DR indicator");
p("sign", "Rent expense changed by -$30,000.", [F], "1 minus sign; 5 sign clash");
p("sign", "Rent expense changed by $-30,000.", [F], "1 minus sign");
p("sign", "Rent expense changed by 30,000-.", [F, NC], "silent: a trailing minus is a sign");
p("sign", "Rent expense changed by $(30,000).", [F], "1 parentheses negative");
p("sign", "Consulting revenue changed by (60,000).", [C, NR], "1 parentheses negative agrees with -60,000", L2);
p("sign", "Consulting revenue changed by 60,000.", [C, NR], "5 a magnitude compared as a magnitude", L2);
p("sign", "Consulting revenue changed by +60,000.", [F, NC, NR], "5 a figure written with its own sign is compared as written", L2);
// ---- percent, percentage points and basis points
p("units", "Rent expense rose $30,000, or 30 percentage points.", [NR], "4 points against a dollar line");
p("units", "Rent expense rose $30,000, or 3,000 basis points.", [NC], "1b basis points");
p("units", "Rent expense rose $30,000, or 30 pts.", [NC, NR], "1b '3 points' listed");
p("units", "Rent expense rose $30,000, a 30 pct increase.", [C], "1 pct");
p("units", "Rent expense rose $30,000, or 30 p.p.", [NC, NR], "1 pp; 4 points against a dollar line");
p("units", "Rent expense rose $30,000, or 30 bps.", [NC], "1b basis points");
p("units", "Rent expense rose 0.3 percent.", [F], "5 unrounded");
p("units", "Rent expense rose $30,000, or 0.30 in percentage terms.", [NC, F], "1b other run of digits");
// ---- period mismatch
p("period", "Rent expense rose $30,000, or 30 percent, year over year.", [NR, NC], "silent: one pair of periods; a year-over-year claim is not that pair");
p("period", "Rent expense rose $30,000 compared with June 2025.", [NR, NC], "silent: a year is accounted for, but the comparison base is not the prior column");
p("period", "Rent expense rose $30,000 over the last twelve months.", [NR, NC], "silent: count accounted for; period mismatch");
p("period", "Year to date, rent expense rose $30,000.", [NR, NC], "silent: YTD is a current-column header word, not the pair");
p("period", "Rent expense rose $30,000 quarter over quarter.", [NR, NC], "silent: period mismatch");
p("period", "Rent expense rose $30,000 against budget.", [NR, NC], "silent: 'budget' names a prior column this ledger does not carry");
p("period", "Consulting revenue fell 25 percent from last year.", [NR, NC], "T48 class: a memo line quoting last year", L2);
// ---- two claims in one sentence, one wrong
p("two", "Rent expense rose $30,000 and Insurance expense rose $40,000.", [F], "2 clause binding; 5", TWO);
p("two", "Rent expense rose $30,000, or 30 percent, and ended at $140,000.", [F], "5");
p("two", "Rent expense rose $30,000 to $130,000, and Insurance expense fell to $95,000.", [F, NR], "direction inside a clause", TWO);
p("two", "Rent expense rose $30,000 while Insurance expense was unchanged.", [F, NR], "a no-change word in a clause naming a line", TWO);
p("two", "Rent expense and Insurance expense rose $30,000 and $45,000 respectively.", [NR], "2 a clause naming two accounts is a binding conflict", TWO);
p("two", "Rent expense rose $30,000; so did Insurance expense.", [NR, F, NC], "silent: 'so did' restates $30,000 for 6200, which moved $45,000", TWO);
p("two", "Rent expense rose $30,000 and Insurance expense rose too, by 30 percent.", [F, NR], "5 insurance moved 90 percent", TWO);
p("two", "Rent expense rose $30,000, the same increase as Insurance expense.", [NR, F, NC], "silent: a comparative claim false on 6200", TWO);
p("two", "Rent expense rose $30,000, or 30 percent, while Insurance expense rose 30 percent.", [F, NR], "5 insurance moved 90 percent", TWO);
// ---- negation scope
p("negation", "Rent expense not only increased by $30,000 but also ended at $130,000.", [NR], "negation voids the clause");
p("negation", "Rent expense did not decline; it rose $30,000.", [NR, C], "negation voids its own clause only");
p("negation", "Rent expense rose $45,000, not $30,000.", [F, NR], "negation attaches to 'not $30,000'; $45,000 stands in its own clause");
p("negation", "Rent expense rose $45,000 without any change in occupancy.", [F, NR], "negation (without)");
p("negation", "Rent expense rose $30,000 and Insurance expense didn’t rise.", [NR, F], "contracted negation with a curly apostrophe (flattened first)", TWO);
p("negation", "Rent expense rose $30,000, and it is untrue that it fell.", [NR, C], "silent: 'untrue' is not in the negation list");
p("negation", "Rent expense rose $30,000 and hardly moved.", [NR, F, NC], "silent: 'hardly moved' asserts near no change");
p("negation", "Rent expense rose $30,000, not a decline of $30,000 as reported earlier.", [NR], "negation");
p("negation", "Rent expense failed to fall, rising $30,000.", [NR, C], "'failed to' listed");
p("negation", "Rent expense rose $30,000; Insurance expense rose nowhere near $45,000.", [NR, F, NC], "silent: 'nowhere near' negates the figure", TWO);
// ---- other currencies and digit systems
p("currency", "Rent expense rose CAD 30,000.", [NC], "1b a currency that is not the dollar (USD 90000 listed)");
p("currency", "Rent expense rose C$30,000.", [NC], "1b a currency that is not the dollar (US$30,000 listed)");
p("currency", "Rent expense rose A$30,000.", [NC], "1b a currency that is not the dollar");
p("currency", "Rent expense rose ¥30,000.", [NC], "1b currency (yen sign)");
p("currency", "Rent expense rose 30,000 EUR.", [NC], "1b currency");
p("currency", "Rent expense rose ₹30,000.", [NC], "1b currency (rupee sign)");
p("currency", "Rent expense rose 30,000 pesos.", [NC], "1b currency");
p("currency", "Rent expense rose Rs. 30,000.", [NC], "1b currency");
p("currency", "Rent expense rose 3,00,000 on the lakh grouping.", [NC, F], "1 thousands commas; lakh grouping");
p("digits", "Rent expense rose ৩০,০০০.", [NC], "1b digits outside 0 to 9 (Bengali)");
p("digits", "Rent expense rose ３０,０００ dollars.", [NC], "1b fullwidth digits");
p("digits", "Rent expense rose $30,000, or 三十 percent.", [NC, F], "1b other quantitative language (CJK numerals)");
p("digits", "Rent expense rose $30,000, or trente pour cent.", [NC, F], "1b other quantitative language (French number words)");
p("digits", "Rent expense rose $30,000, or XXX percent.", [NC, F], "1b other quantitative language (Roman numerals)");
p("digits", "Rent expense rose $30,000, or ३० percent.", [NC], "1b Devanagari digits");
// ---- typography
p("typo", "Rent expense rose $ 30,000.", [C, NC], "a no-break space after the dollar sign");
p("typo", "Rent expense rose $30 000.", [NC, F], "a no-break space as the thousands separator");
p("typo", "Rent expense changed by −$30,000.", [F, NC], "U+2212 minus sign: a sign the words gave");
p("typo", "Rent expense changed by –$30,000.", [F, NC], "en dash flattened, then read as a minus sign");
p("typo", "Rent expense changed by —30,000.", [F, NC], "em dash as a minus sign");
p("typo", "Rent expense rose $30,000, or 90 percent.", [F, NC], "a no-break space between number and unit");
p("typo", "Rent expense rose $30,000, or 90 %.", [F, NC], "a thin space before the percent sign");
p("typo", "Rent expense rose $30,​000.", [NC, F, C], "a zero-width space inside the figure");
p("typo", "Rent expense rose $30,000, or 90％.", [F, NC], "fullwidth percent sign");
p("typo", "Rent expense rose ＄30,000, or 90 percent.", [F, NC], "fullwidth dollar sign, false percent");
p("typo", "Rent expense rose $30,000 – or 90 percent.", [F], "en dash then a false percent");
p("typo", "Rent expense rose $30,000, or 90 per­cent.", [F, NC], "a soft hyphen inside the unit word");
p("typo", "Rent expense rose $30,000, or 90 percent.", [F, NC], "no-break spaces between every word");
// ---- very long sentences
const filler = Array.from({ length: 60 }, (_, i) => "the landlord's schedule item " + (i % 2 ? "was reviewed" : "was noted")).join(", ");
p("long", "Rent expense rose $30,000, " + filler + ", and the balance fell by $45,000 by the end of June.", [F, NR], "5 a false second figure and a false 'fell'");
p("long", "Rent expense rose $30,000, " + filler + ", or 90 percent.", [F], "5 a false percent 600 words later");
p("long", "Rent expense rose $30,000, " + filler + ", and it doubled.", [NC, F], "1b a multiplier far from the figure");
p("long", "Rent expense rose $30,000, " + filler.repeat(20) + ", or 90 percent.", [F], "5 a false percent at the end of a 60,000-character sentence");
fs.mkdirSync(path.join(__dirname, "..", "inputs"), { recursive: true });
fs.writeFileSync(path.join(__dirname, "..", "inputs", "a1-probes.json"), JSON.stringify(P, null, 1));
console.log("wrote", P.length, "probes");
