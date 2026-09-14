/* The drill's own minimum for a written explanation, run outside the page.
   Reads the block between the explain-minimum markers in index.html, evaluates it on its own, and
   prints explainProblem() for each text it is handed as a JSON array on standard input.
   tools/tests/test_findings.py compares the output with findings.explanation_problem().

   node tools/tests/explain-minimum.cjs index.html < texts.json */
const fs = require("fs");
const vm = require("vm");

const page = fs.readFileSync(process.argv[2], "utf8");
const start = page.indexOf("/* explain-minimum:start */");
const end = page.indexOf("/* explain-minimum:end */");
if (start < 0 || end < start) {
  console.error("index.html carries no explain-minimum block");
  process.exit(2);
}
const block = page.slice(start, end);
const box = {};
vm.createContext(box);
vm.runInContext(block + "\nthis.explainProblem = explainProblem;", box);
const texts = JSON.parse(fs.readFileSync(0, "utf8"));
process.stdout.write(JSON.stringify(texts.map((t) => box.explainProblem(t) || null)));
