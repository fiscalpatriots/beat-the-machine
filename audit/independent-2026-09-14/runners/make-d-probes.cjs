// A1 independent audit, 14 September 2026: sizing probes for the four classes the C series found
// still open (sameness, size after the movement noun, share of the movement, hedges and a trailing
// sign). Writes inputs/d-probes.json. Same conventions as make-c-probes.cjs.
const fs = require("fs"), path = require("path");
const RENT = "6100\tRent expense\t100000\t130000";
const NC = "not checked", NR = "needs review", F = "failed", C = "checked within scope";
const P = [];
let n = 0;
function p(cls, memo, req, basis, ledger) {
  n++;
  P.push({ id: "D" + String(n).padStart(3, "0"), cls, inputs: { ledger: ledger || RENT, memo, ratios: "" }, req, basis });
}
// sameness: a no-change claim on a line that moved 30 percent
const same = [
  "Rent expense was rangebound at $130,000.",
  "Rent expense was unremarkable at $130,000.",
  "Rent expense went nowhere, ending at $130,000.",
  "Rent expense was quiet at $130,000.",
  "Rent expense was untouched at $130,000.",
  "Rent expense was as before, at $130,000.",
  "Rent expense was where it was in May, at $130,000.",
  "Rent expense held its ground at $130,000.",
  "Rent expense was at a standstill at $130,000.",
  "Rent expense was uniform with May at $130,000.",
  "Rent expense was unvaried at $130,000.",
  "Rent expense showed no real movement, ending at $130,000.",
];
same.forEach((m) => p("sameness", m, [NR, F, NC], "silent: a no-change claim outside the tested list and outside the sameness lexicon; the clearance grammar's own rule is that nothing risky is left"));
// size words after the movement noun
const size = [
  "Rent expense rose $30,000; the increase was manageable.",
  "Rent expense rose $30,000; the increase was tolerable.",
  "Rent expense rose $30,000; the rise was decent.",
  "Rent expense rose $30,000; the increase was noteworthy.",
  "Rent expense rose $30,000; the movement was chunky.",
  "Rent expense rose $30,000, a beefy increase.",
  "Rent expense rose $30,000, a sizeable increase.",
  "Rent expense rose $30,000, a whopping increase.",
  "Rent expense rose $30,000, a punchy increase.",
];
size.forEach((m) => p("size", m, [NR], "size: an adjective standing on the movement, in front of the movement noun or after it with 'was' between"));
// share of the movement
const share = [
  "Rent expense rose $30,000, a good chunk of it on the new lease.",
  "Rent expense rose $30,000, nearly all of it on the new lease.",
  "Rent expense rose $30,000, the remainder on the new lease.",
  "Rent expense rose $30,000, the balance of it on the new lease.",
  "Rent expense rose $30,000, a fair bit of it on the new lease.",
  "Rent expense rose $30,000, some of the increase on the new lease.",
  "Rent expense rose $30,000, a slice of the increase on the new lease.",
  "Rent expense rose $30,000, the rest of the increase on the new lease.",
];
share.forEach((m) => p("share", m, [NR], "share of the movement: a word that says how much of the movement the sentence explains"));
// hedges on a true figure
const hedge = [
  "Rent expense rose about $30,000.",
  "Rent expense rose approximately $30,000.",
  "Rent expense rose roughly $30,000.",
  "Rent expense rose ~$30,000.",
  "Rent expense rose some $30,000.",
  "Rent expense rose $30,000, give or take.",
  "Rent expense rose $30,000 or thereabouts.",
  "Rent expense rose a ballpark $30,000.",
  "Rent expense rose $30,000 in round numbers.",
  "Rent expense rose a touch over $30,000.",
  "Rent expense rose just shy of $30,000.",
  "Rent expense rose about 30 percent.",
];
hedge.forEach((m) => p("hedge", m, [NR, C], "silent: an approximation on a figure that ties; the third review asked for ambiguous quantitative language to be held, and CHECKER.md lists no hedge class"));
// a sign written after the figure
p("sign", "Rent expense rose $30,000+.", [NR, NC, C], "silent: a plus after the figure; a minus after it is read as a sign (contract 1)");
p("sign", "Rent expense rose $30,000 +.", [NR, NC, C], "silent: the same, spaced");
p("sign", "Rent expense rose $30,000-plus.", [NR, NC, C], "silent: the same, hyphenated");
p("sign", "Rent expense rose 30,000(+).", [NR, NC, C], "silent: a bracketed plus after the figure");
p("sign", "Rent expense rose $30,000 plus.", [NR, NC], "sign weak: plus");
p("sign", "Rent expense changed by 30,000-.", [F], "contract 1: a minus written straight after the figure is a sign, and the ledger rose");
fs.writeFileSync(path.join(__dirname, "..", "inputs", "d-probes.json"), JSON.stringify(P, null, 1));
console.log("wrote", P.length, "probes");
