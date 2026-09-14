// Runs checker inputs through checker.html at a given tree, using that tree's own
// suite harness (tests/run-checker-tests.cjs, execute()). Independent audit A1.
// usage: node run-browser.cjs <game-root> <inputs.json> <out.json>
// inputs.json: [{id, inputs:{ledger,memo,...}, cols?, sample?}]
const fs = require("fs"), path = require("path");
const [game, inFile, outFile] = process.argv.slice(2);
let src = fs.readFileSync(path.join(game, "tests/run-checker-tests.cjs"), "utf8")
  .replace(/^#![^\n]*\n/, "").split("const only =")[0];
const execute = new Function("require", "__dirname", src + "\nreturn execute;")(require, path.join(game, "tests"));
const items = JSON.parse(fs.readFileSync(inFile, "utf8"));
const out = [];
for (const it of items) {
  let p, err = null;
  try { p = execute(it); } catch (e) { err = String(e && e.message); }
  out.push(err ? { id: it.id, error: err } : {
    id: it.id, ran: p.ran, status: p.status, role: p.role, stats: p.stats, queueKinds: p.queueKinds,
    finding: p.finding, survivors: p.survivors, queue: p.queue, csv: p.csv, tsv: p.tsv, json: p.json,
    prompt: p.prompt, consoleErrors: p.consoleErrors, pageText: p.pageText, accounts: p.accounts, flags: p.flags
  });
}
fs.writeFileSync(outFile, JSON.stringify(out, null, 1));
console.log("browser ran", out.length, "inputs,", out.filter(o => o.error).length, "threw");
