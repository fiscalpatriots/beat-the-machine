/* Before and after for lane F4's record.
   node summarize.cjs <A1 audit dir> <exports dir> <outputs dir> <archived game tree at the after commit> [<F3 dir>] */
const fs = require("fs"), path = require("path");
const [A1, X, OUT, G, F3IN] = process.argv.slice(2);
const F3 = F3IN || path.join(G, "audit", "clearance-grammar-2026-09-13", "residual");
const J = (f) => JSON.parse(fs.readFileSync(f, "utf8"));
const res = { classes: {}, totals: {}, sets: {}, parity: {}, sixDrafts: [], prompt1: {}, samples: {},
              neighbours: {}, classProbes: {}, fixtures: {} };

/* the audit's 175 probes, graded against what the audit accepts */
for (const g of ["a1-graded", "a1-sizing-graded"]) {
  const before = Object.fromEntries(J(path.join(X, g + "-before.json")).map((r) => [r.id, r]));
  for (const r of J(path.join(X, g + ".json"))) {
    const b = before[r.id];
    const c = (res.classes[r.cls] = res.classes[r.cls] || { probes: 0, fcBefore: 0, fcAfter: 0, missBefore: 0, missAfter: 0, moved: [] });
    c.probes++;
    if (b.falseClearance) c.fcBefore++;
    if (r.falseClearance) c.fcAfter++;
    if (!b.falseClearance && !(b.meetsContractBrowser && b.meetsContractPython)) c.missBefore++;
    if (!r.falseClearance && !(r.meetsContractBrowser && r.meetsContractPython)) c.missAfter++;
    if (b.browser !== r.browser) c.moved.push({ id: r.id, memo: r.memo, before: b.browser, after: r.browser, meets: r.meetsContractBrowser && r.meetsContractPython });
  }
}
res.totals = Object.values(res.classes).reduce((t, c) => { for (const k in c) if (k !== "moved") t[k] = (t[k] || 0) + c[k]; return t; }, {});

/* parity on every set, after */
for (const s of ["new-40", "prior-24", "six-drafts", "a1", "a1-sizing", "neighbour-probes", "samples", "class-probes"]) {
  const p = J(path.join(X, s + "-parity.json"));
  res.parity[s] = { inputs: p.length, allFieldsEqual: p.filter((r) => !r.differingFields.length).length,
    differing: p.filter((r) => r.differingFields.length).map((r) => [r.id, r.differingFields]) };
}
res.parity.total = { inputs: Object.values(res.parity).reduce((n, p) => n + p.inputs, 0),
  allFieldsEqual: Object.values(res.parity).reduce((n, p) => n + p.allFieldsEqual, 0) };

/* the review's 40 and 24 probes: against the audit's head statuses and against the lane's before */
for (const [set, summary] of [["new-40", "new-40-summary.json"], ["prior-24", "prior-24-summary.json"]]) {
  const head = Object.fromEntries(J(path.join(A1, "outputs", summary)).map((r) => [r.id, r]));
  const before = Object.fromEntries(J(path.join(X, set + "-browser-before.json")).map((r) => [r.id, r.status]));
  const now = J(path.join(X, set + "-browser.json"));
  res.sets[set] = {
    inputs: now.length,
    movedAgainstAuditHead: now.filter((r) => JSON.stringify(r.status) !== JSON.stringify(head[r.id].head))
      .map((r) => ({ id: r.id, memo: head[r.id].memo, auditHead: head[r.id].head, after: r.status })),
    movedAgainstBefore: now.filter((r) => JSON.stringify(r.status) !== JSON.stringify(before[r.id]))
      .map((r) => ({ id: r.id, memo: head[r.id].memo, before: before[r.id], after: r.status })),
  };
}

/* sentence statuses per draft, and every sentence whose text or status moved */
const tally = (rec) => {
  const t = { sentences: 0, checked: 0, review: 0, notChecked: 0, failed: 0, queue: 0 };
  const js = rec.json ? JSON.parse(rec.json) : { sentences: [] };
  js.sentences.forEach((s) => {
    t.sentences++;
    t[{ "checked within scope": "checked", "needs review": "review", "not checked": "notChecked", "failed": "failed" }[s.status]]++;
  });
  t.queue = rec.stats ? rec.stats.queue : 0;
  return { t, sents: js.sentences.map((s) => ({ label: s.id, status: s.status, text: s.text })) };
};
const sixBefore = Object.fromEntries(J(path.join(X, "six-drafts-browser-before.json")).map((r) => [r.id, r]));
for (const r of J(path.join(X, "six-drafts-browser.json"))) {
  const a = tally(r), b = tally(sixBefore[r.id]);
  const bt = Object.fromEntries(b.sents.map((s) => [s.text, s]));
  const at = Object.fromEntries(a.sents.map((s) => [s.text, s]));
  res.sixDrafts.push({ id: r.id, before: b.t, after: a.t,
    statusMoved: a.sents.filter((s) => bt[s.text] && bt[s.text].status !== s.status)
      .map((s) => ({ label: s.label, text: s.text, before: bt[s.text].status, after: s.status })),
    splitDiffers: { onlyBefore: b.sents.filter((s) => !at[s.text]), onlyAfter: a.sents.filter((s) => !bt[s.text]) } });
}
const p1 = res.sixDrafts.filter((d) => /prompt1/.test(d.id));
res.prompt1 = { sentences: p1.reduce((n, d) => n + d.after.sentences, 0),
  checkedBefore: p1.reduce((n, d) => n + d.before.checked, 0), checkedAfter: p1.reduce((n, d) => n + d.after.checked, 0) };

/* the four samples */
const sBefore = Object.fromEntries(J(path.join(X, "samples-browser-before.json")).map((r) => [r.id, r]));
for (const r of J(path.join(X, "samples-browser.json"))) {
  const a = tally(r), b = tally(sBefore[r.id]);
  res.samples[r.id] = { before: b.t, after: a.t,
    moved: a.sents.filter((s, i) => b.sents[i] && b.sents[i].status !== s.status).map((s) => ({ label: s.label, text: s.text, after: s.status })) };
}

/* lane F3's neighbour probes, which must not move, and this lane's own class probes */
const st = (s) => Object.values(s || {});
const nBefore = Object.fromEntries(J(path.join(X, "neighbour-probes-browser-before.json")).map((r) => [r.id, r.status]));
const nb = J(path.join(X, "neighbour-probes-browser.json"));
const nIn = Object.fromEntries(J(path.join(F3, "inputs", "neighbour-probes.json")).map((r) => [r.id, r]));
res.neighbours = { inputs: nb.length,
  clearedBefore: nb.filter((r) => st(nBefore[r.id]).includes("checked within scope")).length,
  clearedAfter: nb.filter((r) => st(r.status).includes("checked within scope")).length,
  moved: nb.filter((r) => JSON.stringify(nBefore[r.id]) !== JSON.stringify(r.status))
    .map((r) => ({ id: r.id, label: nIn[r.id] && nIn[r.id].label, memo: nIn[r.id] && nIn[r.id].inputs.memo,
                   before: nBefore[r.id], after: r.status })) };
const cBefore = Object.fromEntries(J(path.join(X, "class-probes-browser-before.json")).map((r) => [r.id, r.status]));
const cb = J(path.join(X, "class-probes-browser.json"));
res.classProbes = { inputs: cb.length,
  clearedBefore: cb.filter((r) => st(cBefore[r.id]).includes("checked within scope")).length,
  clearedAfter: cb.filter((r) => st(r.status).includes("checked within scope")).length,
  moved: cb.filter((r) => JSON.stringify(cBefore[r.id]) !== JSON.stringify(r.status))
    .map((r) => ({ id: r.id, before: cBefore[r.id], after: r.status })) };

/* the shared fixtures, by class, at the after commit */
const FX = J(path.join(G, "tests", "checker-fixtures.json"));
res.fixtures.total = FX.length;
for (const f of FX) {
  const c = f.id.replace(/[0-9]+[a-z]?$/, "");
  const k = /refusing/.test(f.name) ? "refusing" : /accepting/.test(f.name) ? "accepting" : /mixed/.test(f.name) ? "mixed" : "other";
  const e = (res.fixtures[c] = res.fixtures[c] || { n: 0 });
  e.n++; e[k] = (e[k] || 0) + 1;
}
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(res, null, 1));
console.log("audit probes", JSON.stringify(res.totals));
Object.entries(res.classes).forEach(([k, c]) => console.log("  " + k, c.probes, "fc", c.fcBefore + "->" + c.fcAfter, "miss", c.missBefore + "->" + c.missAfter, "moved", c.moved.length));
Object.entries(res.parity).forEach(([k, p]) => console.log("parity", k, p.allFieldsEqual + "/" + p.inputs, JSON.stringify(p.differing || [])));
console.log("new-40 moved vs audit head", res.sets["new-40"].movedAgainstAuditHead.map((m) => m.id), "vs before", res.sets["new-40"].movedAgainstBefore.map((m) => m.id));
console.log("prior-24 moved vs audit head", res.sets["prior-24"].movedAgainstAuditHead.map((m) => m.id), "vs before", res.sets["prior-24"].movedAgainstBefore.map((m) => m.id));
res.sixDrafts.forEach((d) => console.log(d.id, JSON.stringify(d.before), "->", JSON.stringify(d.after)));
console.log("prompt 1", JSON.stringify(res.prompt1));
Object.entries(res.samples).forEach(([k, s]) => console.log("sample", k, JSON.stringify(s.before), "->", JSON.stringify(s.after)));
console.log("F3 neighbours", res.neighbours.inputs, "cleared before", res.neighbours.clearedBefore, "after", res.neighbours.clearedAfter, "moved", res.neighbours.moved.length);
res.neighbours.moved.slice(0, 20).forEach((m) => console.log("  moved", m.id, m.label, JSON.stringify(m.before), "->", JSON.stringify(m.after)));
console.log("class probes", res.classProbes.inputs, "cleared before", res.classProbes.clearedBefore, "after", res.classProbes.clearedAfter, "moved", res.classProbes.moved.length);
console.log("fixtures", JSON.stringify(res.fixtures));
