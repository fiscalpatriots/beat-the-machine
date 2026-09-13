#!/usr/bin/env node
/* Regression suite for checker.html.
 *
 *   node tests/run-checker-tests.cjs            run every fixture
 *   node tests/run-checker-tests.cjs T02        run one, and print its probe
 *   node tests/run-checker-tests.cjs --dump T02 print the whole probe as JSON
 *
 * The page is a single HTML file with no build step, so the suite lifts the
 * script out of it and runs it against a document stub. The stub is the audit
 * harness's stub from Second-Pass-Verification/work/checker-audit.cjs, widened
 * for the elements the current page carries.
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");
const HTML = fs.readFileSync(path.join(ROOT, "checker.html"), "utf8");
const SCRIPT = HTML.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/)[1];
const FIXTURES = JSON.parse(fs.readFileSync(path.join(__dirname, "checker-fixtures.json"), "utf8"));

class Element {
  constructor(tag) {
    this.tag = tag || "div";
    this.value = "";
    this.style = {};
    this.children = [];
    this._html = "";
    this.textContent = "";
    this.className = "";
    this.classList = { add() {}, remove() {} };
  }
  set innerHTML(v) { this._html = String(v); if (v === "") this.children = []; }
  get innerHTML() { return this._html; }
  appendChild(e) { this.children.push(e); return e; }
  removeChild(e) { const i = this.children.indexOf(e); if (i > -1) this.children.splice(i, 1); }
  get firstChild() { return this.children[0] || null; }
  setAttribute() {}
  addEventListener() {}
  scrollIntoView() {}
  focus() {}
  select() {}
  text() {
    let s = String(this._html || "").replace(/<[^>]+>/g, " ") + " " + (this.textContent || "");
    this.children.forEach((c) => { s += " " + (c.text ? c.text() : String(c.textContent || "")); });
    return s;
  }
}

function execute(fx) {
  const nodes = {};
  const get = (id) => nodes[id] || (nodes[id] = new Element(id));
  const document = {
    getElementById: get,
    createElement: (t) => new Element(t),
    createTextNode: (t) => ({ textContent: t, text: () => String(t) }),
    body: new Element("body"),
    execCommand: () => true,
  };
  const window = { location: { search: "" }, scrollTo() {}, print() {} };
  const errors = [];
  const ctx = vm.createContext({
    document, window, navigator: {}, setTimeout() {}, clearTimeout() {},
    console: { log() {}, warn(...a) { errors.push(a.join(" ")); }, error(...a) { errors.push(a.join(" ")); } },
    Date, JSON, Math, RegExp, String, Number, Array, Object, isFinite, isNaN, parseInt, parseFloat, Error,
  });
  vm.runInContext(SCRIPT, ctx);

  const inputs = Object.assign(
    { ledger: "", memo: "", ratios: "", dollar: "25000", pct: "10", rule: "both",
      zerobase: "owing", period: "Regression fixture", memover: "fixture", company: "", reviewer: "" },
    fx.inputs || {}
  );
  Object.keys(inputs).forEach((k) => { get(k).value = inputs[k]; });
  if (fx.cols) { get("colprior").value = String(fx.cols.p); get("colcur").value = String(fx.cols.c); get("colprior").onchange(); }

  if (fx.sample) {
    const sp = get("samplepick");
    sp.value = fx.sample;
    sp.onchange.call(sp);
  } else {
    get("run").onclick();
  }
  const S = window.__secondPass();
  const probe = {
    ran: !!S,
    pageText: (get("msg").text() + " " + get("out").text() + " " + get("pvfacts").text() + " " + get("pvbody").text())
      .replace(/\s+/g, " "),
    consoleErrors: errors,
  };
  if (!S) {
    probe.stats = {};
    probe.status = {};
    probe.finding = {};
    probe.account = {};
    probe.accounts = [];
    probe.flags = {};
    probe.queue = "";
    probe.csv = "";
    probe.prompt = "";
    probe.json = "";
    probe.tsv = "";
    return probe;
  }
  probe.stats = S.stats;
  probe.runId = S.runId;
  probe.status = {};
  probe.role = {};
  probe.finding = {};
  S.sents.forEach((s) => {
    probe.status[s.label] = s.st;
    probe.role[s.label] = s.figs.map((f) => f.raw + "=" + f.unit + "/" + f.role).join(" | ");
    probe.finding[s.label] = S.rows
      .filter((r) => r.label === s.label)
      .map((r) => r.check + ": " + r.result + " " + r.det + " " + (Array.isArray(r.ask) ? r.ask.join(" ") : r.ask))
      .join(" || ");
  });
  probe.accounts = S.accounts.map((a) => ({
    num: a.num, name: a.name, prior: a.prior, cur: a.cur, change: a.change, pct: a.pct,
    clears: a.clears, legD: a.legs.d, legP: a.legs.p, sentences: a.sent.length,
  }));
  probe.account = {};
  probe.accounts.forEach((a) => { if (!(a.num in probe.account)) probe.account[a.num] = a; });
  probe.accountCount = probe.accounts.length;
  probe.survivors = S.survivors.map((s) => s.label).join(",");
  probe.flags = {
    colsUnconfirmed: !!S.ledger.colsUnconfirmed,
    ambig: S.ledger.ambig.length,
    discarded: S.ledger.discarded.length,
    dups: S.ledger.dups.length,
    skipped: S.stats.rowsSkipped,
  };
  probe.queue = JSON.stringify(S.queue);
  probe.queueKinds = S.queue.map((q) => q.kind).join(",");
  probe.csv = window.__secondPass("csv");
  probe.prompt = window.__secondPass("prompt");
  probe.json = window.__secondPass("json");
  probe.tsv = window.__secondPass("table");
  return probe;
}

function dig(probe, p) {
  return p.split(".").reduce((o, k) => (o == null ? o : o[k]), probe);
}
const OPS = {
  eq: (a, b) => a === b,
  ne: (a, b) => a !== b,
  gte: (a, b) => Number(a) >= Number(b),
  lte: (a, b) => Number(a) <= Number(b),
  approx: (a, b) => Math.abs(Number(a) - Number(b)) < 0.0005,
  includes: (a, b) => String(a).indexOf(b) > -1,
  notIncludes: (a, b) => String(a).indexOf(b) < 0,
  oneOf: (a, b) => b.indexOf(a) > -1,
  isNull: (a) => a === null,
};

const only = process.argv.slice(2).filter((a) => a !== "--dump");
const dump = process.argv.indexOf("--dump") > -1;
let pass = 0, fail = 0;
const failed = [];

FIXTURES.forEach((fx) => {
  if (only.length && !only.some((o) => fx.id === o || fx.name.indexOf(o) > -1)) return;
  let probe;
  try {
    probe = execute(fx);
  } catch (e) {
    fail++;
    failed.push(fx.id + " threw: " + e.message + "\n" + (e.stack || "").split("\n").slice(0, 4).join("\n"));
    console.log("FAIL " + fx.id + " " + fx.name + " — threw " + e.message);
    return;
  }
  if (dump) console.log(JSON.stringify(probe, null, 2));
  const bad = [];
  (fx.expect || []).forEach((c) => {
    const got = dig(probe, c.get);
    const ok = OPS[c.op](got, c.value);
    if (!ok) bad.push("  " + c.desc + "\n    " + c.get + " " + c.op + " " + JSON.stringify(c.value) +
      "\n    got: " + JSON.stringify(typeof got === "string" && got.length > 400 ? got.slice(0, 400) + "…" : got));
  });
  if (probe.consoleErrors && probe.consoleErrors.length) bad.push("  console error: " + probe.consoleErrors.join("; "));
  if (bad.length) {
    fail++;
    failed.push(fx.id + " " + fx.name + "\n" + bad.join("\n"));
    console.log("FAIL " + fx.id + " " + fx.name);
  } else {
    pass++;
    console.log("pass " + fx.id + " " + fx.name);
  }
});

console.log("\n" + pass + " passed, " + fail + " failed, " + (pass + fail) + " run");
if (failed.length) {
  console.log("\n--- failures ---");
  failed.forEach((f) => console.log(f + "\n"));
}
process.exit(fail ? 1 : 0);
