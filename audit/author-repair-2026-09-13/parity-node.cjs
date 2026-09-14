/* Author sentence statuses against checker.html's own run(), with the author fold driven by the
   reader functions checker.html carries right now rather than by assets/second-pass-core.js.
   That separates two questions: is the author's fold the checker's fold (this script), and has
   the shared reader file caught up with the checker (the browser parity run).
   node parity-node.cjs <repo root> */
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const ROOT = process.argv[2];

class Element {
  constructor(tag) { this.tag = tag || "div"; this.value = ""; this.style = {}; this.children = []; this._html = "";
    this.textContent = ""; this.className = ""; this.classList = { add() {}, remove() {}, toggle() {} }; }
  set innerHTML(v) { this._html = String(v); if (v === "") this.children = []; }
  get innerHTML() { return this._html; }
  appendChild(e) { this.children.push(e); return e; }
  removeChild(e) { const i = this.children.indexOf(e); if (i > -1) this.children.splice(i, 1); }
  get firstChild() { return this.children[0] || null; }
  setAttribute() {} addEventListener() {} scrollIntoView() {} focus() {} select() {}
}

const html = fs.readFileSync(path.join(ROOT, "checker.html"), "utf8");
let SCRIPT = html.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/)[1];
/* lift the IIFE so the reader's functions are reachable by name */
SCRIPT = SCRIPT.replace(/^\s*\(function\(\)\{/, "").replace(/\}\)\(\);\s*$/, "");

const author = fs.readFileSync(path.join(ROOT, "author.html"), "utf8");
const a0 = author.indexOf("function foldSentence("), a1 = author.indexOf("function readSet(");
const a2 = author.indexOf("/* =============================================================================\n   One card per sentence");
if (a0 < 0 || a1 < 0 || a2 < 0) throw new Error("author fold not found");
const FOLD = author.slice(a0, a2);

const NAMES = ["parseLedger", "tieTotals", "legs", "clears", "pctCell", "splitSentences", "figures", "bindSentence",
  "clauseBind", "checkDollar", "checkPercent", "policyClaims", "directionOn", "spansOf", "negationIn", "claimIn",
  "worse", "zeroPolicyText", "acctId", "srcVersion", "RE_COARSE"];

const RENT = "6100\tRent expense\t100000\t130000";
const RENT2 = RENT + "\n6200\tInsurance expense\t50000\t95000";
const PROBES = [
  ["review", RENT2, "1. Rent expense did not increase by $30,000.\n2. The bank covenant ratio was 7.2%."],
  ["P05", RENT, "1. Rent expense increased by $30,000 and doubled."],
  ["P13", RENT, "1. Rent expense remained at $130,000."],
  ["P23", RENT, "1. Rent expense rose $30,000, or one and a half percent."],
  ["P25", RENT, "1. Rent expense rose $30,000 and increased by ٣٠٠٠٠."],
  ["P30", RENT, "1. Rent expense increased by $30,000 from $100,000 to $130,000."],
  ["P31", RENT, "1. Rent expense declined by $30,000 from $100,000 to $130,000."],
  ["wrong figure", RENT2, "1. Rent expense rose $35,000 to $130,000.\n2. Insurance expense rose $45,000, or 90 percent."],
  ["two accounts", RENT2, "1. Rent expense and insurance expense rose $30,000 and $45,000."],
  ["policy claim", RENT2 + "\n6300\tPostage\t1000\t1200", "1. Postage rose $200, which fails the dollar leg of the threshold, so this line carries no driver."],
  ["duplicate number", RENT + "\n6100\tRent expense annex\t5000\t9000", "1. 6100 rose $30,000."],
  ["three columns, no header", "6100\tRent expense\t100000\t130000\t30000", "1. Rent expense rose $30,000."],
  ["Prompt 1 roles", RENT, "1. Rent expense: prior $100,000, current $130,000, change $30,000 (30.0%)."],
];

const tests = JSON.parse(fs.readFileSync(path.join(ROOT, "tests", "checker-fixtures.json"), "utf8"));
const fixtures = (Array.isArray(tests) ? tests : tests.fixtures || []).filter((f) => f.inputs && f.inputs.ledger && f.inputs.memo &&
  !f.cols && !(f.inputs.ratios || "").trim() && (f.inputs.dollar || "25000") === "25000" && (f.inputs.pct || "10") === "10" &&
  (f.inputs.rule || "both") === "both" && (f.inputs.zerobase || "owing") === "owing")
  .map((f) => [f.id || f.name, f.inputs.ledger, f.inputs.memo]);

let fail = 0;
const rows = [];
PROBES.concat(fixtures).forEach(([id, led, memo]) => {
  const nodes = {};
  const get = (k) => nodes[k] || (nodes[k] = new Element(k));
  const document = { getElementById: get, createElement: (t) => new Element(t), createTextNode: (t) => ({ textContent: t }),
    body: new Element("body"), execCommand: () => true };
  const window = { location: { search: "" }, scrollTo() {}, print() {} };
  const ctx = vm.createContext({ document, window, navigator: {}, setTimeout() {}, clearTimeout() {},
    console: { log() {}, warn() {}, error() {} },
    Date, JSON, Math, RegExp, String, Number, Array, Object, isFinite, isNaN, parseInt, parseFloat, Error });
  vm.runInContext(SCRIPT, ctx);
  const inputs = { ledger: led, memo, ratios: "", dollar: "25000", pct: "10", rule: "both", zerobase: "owing",
    period: "parity", memover: "parity", company: "", reviewer: "" };
  Object.keys(inputs).forEach((k) => { get(k).value = inputs[k]; });
  get("run").onclick();
  const S = window.__secondPass();
  const chk = S ? S.sents.map((s) => s.label + " " + s.st) : [];
  vm.runInContext("var __CORE={};" + NAMES.map((n) => "__CORE." + n + "=" + n + ";").join("") +
    "function core(){return __CORE;}function money(v){return '$'+Math.round(Math.abs(v)).toLocaleString('en-US');}" +
    "function cap(t){t=String(t);return t.charAt(0).toUpperCase()+t.slice(1);}" +
    "function dot(t){t=cap(t);return /[.!?]$/.test(t)?t:t+'.';}" + FOLD.replace(/function readSet\(/, "function __authorReadSet("), ctx);
  ctx.__led = led; ctx.__memo = memo;
  const R = vm.runInContext("__authorReadSet(__led,__memo,25000,10,'both','owing')", ctx);
  const aut = R.error ? ["error " + R.error] : R.sents.map((s) => s.label + " " + s.st);
  const match = (!S && !!R.error) || !!S && aut.length === chk.length && aut.every((x, i) => x === chk[i]);
  if (!match) fail++;
  rows.push({ id, match, author: aut.join(" | "), checker: chk.join(" | ") });
});
rows.forEach((r) => console.log((r.match ? "MATCH " : "DIFF  ") + r.id + (r.match ? "" : "\n   author:  " + r.author + "\n   checker: " + r.checker)));
console.log(rows.length + " inputs, " + (rows.length - fail) + " match, " + fail + " differ");
process.exit(fail ? 1 : 0);
