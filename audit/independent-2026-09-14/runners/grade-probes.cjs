// Grades A1 probes: observed status in both implementations against the contract requirement.
// usage: node grade-probes.cjs <inputs/a1-probes.json> <browser.json> <python.json> <parity.json> <out.json>
const fs = require("fs");
const [inF, bF, pF, parF, outF] = process.argv.slice(2);
const inp = JSON.parse(fs.readFileSync(inF, "utf8"));
const br = Object.fromEntries(JSON.parse(fs.readFileSync(bF, "utf8")).map((x) => [x.id, x]));
const py = Object.fromEntries(JSON.parse(fs.readFileSync(pF, "utf8")).map((x) => [x.id, x]));
const par = Object.fromEntries(JSON.parse(fs.readFileSync(parF, "utf8")).map((x) => [x.id, x]));
const rows = inp.map((t) => {
  const b = br[t.id], y = py[t.id];
  const bs = b.error ? "ERROR " + b.error : (b.status || {}).S1 || (b.status || {})["1"] || JSON.stringify(b.status);
  const ys = y.error ? "ERROR " + y.error : (y.status || {}).S1 || (y.status || {})["1"] || JSON.stringify(y.status);
  const okB = t.req.includes(bs), okY = t.req.includes(ys);
  return {
    id: t.id, cls: t.cls, memo: t.inputs.memo.length > 200 ? t.inputs.memo.slice(0, 120) + " ... [" + t.inputs.memo.length + " chars] ... " + t.inputs.memo.slice(-60) : t.inputs.memo,
    ledger: t.inputs.ledger.split("\n")[0].split("\t").slice(0, 2).join(" ") + (t.inputs.ledger.includes("\n") ? " +" : ""),
    required: t.req, basis: t.basis, browser: bs, python: ys,
    browserRoles: b.role ? b.role.S1 || b.role["1"] : null, browserQueue: b.queueKinds,
    browserFinding: b.finding ? String(b.finding.S1 || "").slice(0, 400) : null,
    meetsContractBrowser: okB, meetsContractPython: okY,
    falseClearance: (bs === "checked within scope" && !okB) || (ys === "checked within scope" && !okY),
    parityStatus: bs === ys, parityAllFields: par[t.id] ? par[t.id].differingFields.length === 0 : null,
    parityDifferingFields: par[t.id] ? par[t.id].differingFields : null,
  };
});
fs.writeFileSync(outF, JSON.stringify(rows, null, 1));
const fc = rows.filter((r) => r.falseClearance), miss = rows.filter((r) => !r.falseClearance && (!r.meetsContractBrowser || !r.meetsContractPython));
const pd = rows.filter((r) => !r.parityStatus || r.parityAllFields === false);
console.log("probes", rows.length, "| false clearances", fc.length, "| other contract misses", miss.length, "| parity differences", pd.length);
for (const r of fc) console.log("FALSE CLEARANCE", r.id, r.cls, JSON.stringify(r.memo), "| browser:", r.browser, "| python:", r.python, "| roles:", r.browserRoles, "| req:", r.required.join("/"));
for (const r of miss) console.log("MISS", r.id, r.cls, JSON.stringify(r.memo), "| browser:", r.browser, "| python:", r.python, "| roles:", r.browserRoles, "| req:", r.required.join("/"));
for (const r of pd) console.log("PARITY", r.id, JSON.stringify(r.memo), r.browser, "vs", r.python, r.parityDifferingFields);
