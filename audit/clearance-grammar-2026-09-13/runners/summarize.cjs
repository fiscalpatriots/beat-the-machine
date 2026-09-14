/* Before and after, for lane F1's record. node summarize.cjs <A1 audit dir> <outputs dir> */
const fs = require("fs"), path = require("path");
const [A1, OUT] = process.argv.slice(2);
const J = (f) => JSON.parse(fs.readFileSync(f, "utf8"));
const res = { classes: {}, totals: {}, sets: {} };
for (const g of ["a1-graded.json", "a1-sizing-graded.json"]) {
  const before = Object.fromEntries(J(path.join(A1, "outputs", g)).map((r) => [r.id, r]));
  for (const r of J(path.join(OUT, g))) {
    const b = before[r.id], c = (res.classes[r.cls] = res.classes[r.cls] || { probes: 0, fcBefore: 0, fcAfter: 0, missBefore: 0, missAfter: 0 });
    c.probes++;
    if (b.falseClearance) c.fcBefore++;
    if (r.falseClearance) c.fcAfter++;
    if (!b.falseClearance && !(b.meetsContractBrowser && b.meetsContractPython)) c.missBefore++;
    if (!r.falseClearance && !(r.meetsContractBrowser && r.meetsContractPython)) c.missAfter++;
  }
}
res.totals = Object.values(res.classes).reduce((t, c) => { for (const k in c) t[k] = (t[k] || 0) + c[k]; return t; }, {});
for (const [set, summary] of [["new-40", "new-40-summary.json"], ["prior-24", "prior-24-summary.json"]]) {
  const head = Object.fromEntries(J(path.join(A1, "outputs", summary)).map((r) => [r.id, r.head]));
  const now = J(path.join(OUT, set + "-browser.json"));
  const moved = now.filter((r) => JSON.stringify(r.status) !== JSON.stringify(head[r.id])).map((r) => ({ id: r.id, before: head[r.id], after: r.status }));
  res.sets[set] = { inputs: now.length, moved };
}
const sixBefore = Object.fromEntries(J(path.join(A1, "outputs", "six-drafts-browser.json")).map((r) => [r.id, r.status]));
const six = J(path.join(OUT, "six-drafts-browser.json"));
res.sets["six-drafts"] = six.map((r) => {
  const count = (st) => Object.values(st || {}).filter((x) => x === "checked within scope").length;
  const moved = Object.keys(r.status).filter((k) => r.status[k] !== (sixBefore[r.id] || {})[k]).map((k) => ({ label: k, before: sixBefore[r.id][k], after: r.status[k] }));
  return { id: r.id, sentences: Object.keys(r.status).length, checkedBefore: count(sixBefore[r.id]), checkedAfter: count(r.status), moved };
});
const p1 = res.sets["six-drafts"].filter((d) => /prompt1/.test(d.id));
res.prompt1 = { sentences: p1.reduce((n, d) => n + d.sentences, 0), checkedBefore: p1.reduce((n, d) => n + d.checkedBefore, 0), checkedAfter: p1.reduce((n, d) => n + d.checkedAfter, 0) };
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(res, null, 1));
console.log(JSON.stringify(res.totals), "prompt 1", JSON.stringify(res.prompt1));
Object.entries(res.classes).forEach(([k, c]) => console.log(k, JSON.stringify(c)));
console.log("new-40 moved", res.sets["new-40"].moved.length, "prior-24 moved", res.sets["prior-24"].moved.length);
res.sets["six-drafts"].forEach((d) => console.log(d.id, d.checkedBefore + "->" + d.checkedAfter, "of", d.sentences, JSON.stringify(d.moved)));
