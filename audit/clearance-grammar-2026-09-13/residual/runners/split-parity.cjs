/* Lane F3: the sentence splitter against a person's reading, and against the Python splitter.
   node split-parity.cjs <game tree> <trainer tree> <split-readings.json> <out.json>
   Reads 44 sentences written to test a person's reading, every fixture memo and the six retained
   drafts; splits each with assets/second-pass-core.js and with second_pass.checker.split_sentences,
   and records any split that differs from the reading or between the two. */
const fs = require("fs"), path = require("path"), vm = require("vm"), { execFileSync } = require("child_process");
const [G, T, READINGS, OUT] = process.argv.slice(2);
const ctx = {}; ctx.window = ctx; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(G, "assets", "second-pass-core.js"), "utf8"), ctx);
const C = ctx.SecondPassCore;
const readings = JSON.parse(fs.readFileSync(READINGS, "utf8"));
const fixtures = JSON.parse(fs.readFileSync(path.join(G, "tests", "checker-fixtures.json"), "utf8"));
const drafts = JSON.parse(fs.readFileSync(path.join(G, "audit", "independent-2026-09-13", "inputs", "six-drafts-as-fixtures.json"), "utf8"));
const texts = readings.map((r) => r.text)
  .concat(fixtures.filter((f) => f.inputs && f.inputs.memo).map((f) => f.inputs.memo))
  .concat(drafts.map((d) => d.inputs.memo));
const js = texts.map((t) => C.splitSentences(t).map((s) => [s.label, s.text]));
const tmp = OUT + ".texts.json";
fs.writeFileSync(tmp, JSON.stringify(texts));
const py = JSON.parse(execFileSync("python", ["-c",
  "import json,sys; sys.path.insert(0, sys.argv[1]); from second_pass import checker; " +
  "t=json.load(open(sys.argv[2], encoding='utf-8')); " +
  "print(json.dumps([[[s['label'], s['text']] for s in checker.split_sentences(x)] for x in t]))", T, tmp],
  { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 }));
fs.unlinkSync(tmp);
const readingMisses = readings.map((r, i) => ({ text: r.text, want: r.sentences, got: js[i].map((s) => s[1]) }))
  .filter((r) => JSON.stringify(r.want) !== JSON.stringify(r.got));
const parityMisses = texts.map((t, i) => ({ text: t, browser: js[i], python: py[i] }))
  .filter((r) => JSON.stringify(r.browser) !== JSON.stringify(r.python));
const out = { readings: readings.length, memos: texts.length, readingMisses, parityMisses };
fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
console.log("split readings " + readings.length + ", as a person reads them " + (readings.length - readingMisses.length) +
  "; memos split in both " + texts.length + ", split the same way " + (texts.length - parityMisses.length));
