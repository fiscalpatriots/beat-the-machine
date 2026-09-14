// A1 independent audit: sizing probes for the classes the first batch found open.
// Writes inputs/a1-sizing-probes.json. Same fields and conventions as make-new-probes.cjs.
const fs = require("fs"), path = require("path");
const RENT = "6100\tRent expense\t100000\t130000";
const L2 = "4300\tConsulting revenue\t240000\t180000\n6700\tTravel expense\t12000\t12000\n6800\tUtilities expense\t50000\t50150";
const NC = "not checked", NR = "needs review", F = "failed", C = "checked within scope";
const P = [];
let n = 0;
function p(cls, memo, req, basis, ledger) { n++; P.push({ id: "B" + String(n).padStart(3, "0"), cls, inputs: { ledger: ledger || RENT, memo, ratios: "" }, req, basis }); }
// currency written as a word or a prefixed dollar
p("currency", "Rent expense rose 30,000 euros.", [NC], "1b a currency that is not the dollar");
p("currency", "Rent expense rose 30,000 pounds.", [NC], "1b");
p("currency", "Rent expense rose 30,000 yen.", [NC], "1b");
p("currency", "Rent expense rose 30,000 rupees.", [NC], "1b");
p("currency", "Rent expense rose 30,000 Canadian dollars.", [NC], "1b a currency that is not the dollar, named with the word dollars");
p("currency", "Rent expense rose 30,000 Australian dollars.", [NC], "1b");
p("currency", "Rent expense rose HK$30,000.", [NC], "1b (US$30,000 listed)");
p("currency", "Rent expense rose R$30,000.", [NC], "1b");
p("currency", "Rent expense rose 30,000 francs.", [NC], "1b");
p("currency", "Rent expense rose $30,000 in Canadian currency.", [NC], "1b");
// sign written in a form other than a leading minus or parentheses
p("sign", "Rent expense changed by $-30,000, or -30 percent.", [F], "1 minus sign; 5 sign clash");
p("sign", "Rent expense changed by +$30,000.", [C, F], "a plus sign that agrees");
p("sign", "Consulting revenue changed by +$60,000.", [F, NC, NR], "5 a figure written with its own sign is compared as written", L2);
p("sign", "Consulting revenue changed by $+60,000.", [F, NC, NR], "5", L2);
p("sign", "Consulting revenue changed by +25 percent.", [F, NC, NR], "5", L2);
p("sign", "Rent expense changed by minus $30,000.", [F, NC, NR], "silent: the word minus is a sign the words gave");
p("sign", "Rent expense changed by negative $30,000.", [F, NC, NR], "silent: the word negative is a sign");
p("sign", "Rent expense changed by 30,000 Cr.", [F, NC, NR], "silent: Cr indicator");
p("sign", "Rent expense changed by $30,000 credit.", [F, NC, NR], "silent: credit indicator");
// no-change words outside the enumerated list
p("nochange", "Rent expense was stable at $130,000.", [F, NC, NR], "silent: stable");
p("nochange", "Rent expense was steady at $130,000.", [F], "steady listed");
p("nochange", "Rent expense was constant at $130,000.", [F, NC, NR], "silent: 'remained constant' listed, 'was constant' not");
p("nochange", "Rent expense was the same as May at $130,000.", [F, NC, NR], "silent: 'stayed the same' listed");
p("nochange", "Rent expense did not move and closed at $130,000.", [NR, F], "negation");
p("nochange", "Rent expense was static at $130,000.", [F, NC, NR], "silent: static");
p("nochange", "Rent expense was unmoved at $130,000.", [F, NC, NR], "silent: unmoved");
p("nochange", "Rent expense was on par with May at $130,000.", [F, NC, NR], "silent: on par");
p("nochange", "Rent expense was equal to May at $130,000.", [F, NC, NR], "silent: equal to May");
p("nochange", "Rent expense matched May at $130,000.", [F, NC, NR], "silent: matched May");
p("nochange", "Rent expense was unchanged month over month at $130,000.", [F], "unchanged listed");
// period words
p("period", "Rent expense rose $30,000 versus the prior year.", [NR, NC], "silent: the prior year is not the prior column");
p("period", "Rent expense rose $30,000 on a trailing twelve month basis.", [NR, NC], "silent");
p("period", "Rent expense rose $30,000 since December.", [NR, NC], "silent: a month other than the prior column");
p("period", "Rent expense rose $30,000 compared with last June.", [NR, NC], "silent: T48 class without a figure");
p("period", "Rent expense rose $30,000, or 30 percent, over two years.", [NR, NC], "silent: count accounted for, period mismatch");
p("period", "Rent expense rose $30,000 in the first half.", [NR, NC], "silent");
fs.writeFileSync(path.join(__dirname, "..", "inputs", "a1-sizing-probes.json"), JSON.stringify(P, null, 1));
console.log("wrote", P.length, "probes");
