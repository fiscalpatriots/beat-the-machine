/* Lane F4: the author page against the checker on every class input, including this lane's
   four classes, then the checker at 375 and 1,024 on a sample run and on a quarterly ledger.
   node pages.cjs <game-root> <out.json> <screenshot-dir>
   Headless Chrome in a throwaway profile, through the independent audit's driver. Nothing is
   posted and nothing is saved from the page. Every input is synthetic. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../../../independent-2026-09-13/runners/cdp.cjs");
const [ROOT, OUT, SHOTS] = process.argv.slice(2);
fs.mkdirSync(SHOTS, { recursive: true });

let src = fs.readFileSync(path.join(ROOT, "tests/run-checker-tests.cjs"), "utf8").replace(/^#![^\n]*\n/, "").split("const only =")[0];
const execute = new Function("require", "__dirname", src + "\nreturn execute;")(require, path.join(ROOT, "tests"));

const FIX = JSON.parse(fs.readFileSync(path.join(ROOT, "tests/checker-fixtures.json"), "utf8"));
const PLAIN = (f) => f.inputs && f.inputs.ledger && f.inputs.memo && !f.cols && !(f.inputs.ratios || "").trim() &&
  !f.inputs.dollar && !f.inputs.pct && !f.inputs.rule && !f.inputs.zerobase;
const INPUTS = FIX.filter((f) => /^(?:[AB][0-9]{3}|CUR|SIGN|SAME|PER|ANA|RESP|QTY|SPLIT|SIZE|PLAB|BIND|LEX|REAS|NAME|QTR|HEDGE)/.test(f.id) && PLAIN(f))
  .map((f) => ({ id: f.id, ledger: f.inputs.ledger, memo: f.inputs.memo }));
const QUARTER = { ledger: "Account\tQ1 2026\tQ2 2026\n6100\tRent expense\t100000\t130000\n6200\tInsurance expense\t50000\t95000",
  memo: "1. Rent expense rose $30,000 in Q2 on a decrease in vacancy at the U.S. Treasury lease.\n2. Insurance expense rose $45,000 in June." };

(async () => {
  const { srv, port } = await serve(ROOT);
  const B = await launch("f4");
  const base = `http://127.0.0.1:${port}/`;
  const out = { root: ROOT, author: [], widths: [], errors: [] };
  const set = `window.__set=function(id,v){var e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));return true;};true`;
  const clip = async (file, y, w, h) => {
    const r = await B.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
      clip: { x: 0, y: Math.max(0, y), width: w, height: h, scale: 1 } });
    fs.writeFileSync(file, Buffer.from(r.data, "base64"));
    return path.basename(file);
  };
  try {
    /* ---- 1. the author page on every audit probe and every class mutation */
    await B.width(1280);
    const ready = "!!(window.__SPA&&window.SecondPassCore)";
    await B.nav(base + "author.html", ready);
    await B.ev("localStorage.clear();sessionStorage.clear();true");
    await B.nav(base + "author.html", ready);
    await B.ev(set);
    for (const t of INPUTS) {
      const chk = execute({ inputs: { ledger: t.ledger, memo: t.memo } });
      await B.ev(`__set('ledger',${JSON.stringify(t.ledger)});__set('memo',${JSON.stringify(t.memo)});true`);
      await B.ev("document.getElementById('read').click();true");
      await sleep(40);
      const a = await B.ev(`({sents:__SPA.sentences(),cards:__SPA.cards().map(function(c){return {label:c.label,status:c.status,key:c.key};})})`);
      const rows = a.sents.map((s) => {
        const card = a.cards.find((c) => c.label === s.label) || null;
        return { label: s.label, text: s.text, author: s.status, checker: chk.status[s.label], key: card ? card.key : null };
      });
      const sameSplit = Object.keys(chk.status).length === a.sents.length;
      const bad = rows.filter((r) => r.author !== r.checker || (r.checker !== "checked within scope" && r.key === "stand"));
      out.author.push({ id: t.id, rows, sameSplit, ok: !bad.length && sameSplit });
    }
    /* ---- 2. the checker at the two widths this lane reads: a sample run, and a quarterly ledger */
    for (const w of [375, 1024]) {
      const row = { width: w };
      await B.width(w);
      await B.nav(base + "checker.html?sample=halyard", "!!(window.__secondPass&&window.__secondPass())");
      await sleep(400);
      row.halyardOverflow = await B.ev(OVERFLOW);
      const cov = await B.ev(`(function(){var e=document.querySelector('#out .summary')||document.getElementById('out');var r=e.getBoundingClientRect();return {y:r.top+window.scrollY-24};})()`);
      row.halyardShot = await clip(path.join(SHOTS, "checker-halyard-" + w + ".png"), cov.y, w, w < 700 ? 1100 : 900);
      await B.nav(base + "checker.html", "!!window.__secondPass");
      await B.ev(set);
      await B.ev(`__set('ledger',${JSON.stringify(QUARTER.ledger)});__set('memo',${JSON.stringify(QUARTER.memo)});true`);
      await B.ev("document.getElementById('run').click();true");
      await sleep(400);
      row.quarterOverflow = await B.ev(OVERFLOW);
      row.quarterStatuses = await B.ev(`(function(){var S=window.__secondPass();return S.sents.map(function(s){return s.label+' '+s.st;});})()`);
      const open = await B.ev(`(function(){[].slice.call(document.querySelectorAll('#out details.sent')).forEach(function(d){d.open=true;});
        var e=document.querySelector('#out .summary')||document.getElementById('out');var r=e.getBoundingClientRect();return {y:r.top+window.scrollY-24};})()`);
      await sleep(200);
      row.quarterShot = await clip(path.join(SHOTS, "checker-quarters-" + w + ".png"), open.y, w, w < 700 ? 1500 : 1100);
      row.quarterOverflowOpen = await B.ev(OVERFLOW);
      out.widths.push(row);
    }
    out.errors = B.errors.slice();
  } catch (e) {
    out.errors.push(String(e && e.stack || e));
  } finally {
    B.close(); srv.close();
  }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  const bad = out.author.filter((r) => !r.ok);
  const sentences = out.author.reduce((n, r) => n + r.rows.length, 0);
  const held = out.author.reduce((n, r) => n + r.rows.filter((x) => x.checker !== "checked within scope").length, 0);
  console.log("author inputs " + out.author.length + ", sentences " + sentences + ", held by the checker " + held +
    ", where the author page splits, rates or suggests differently " + bad.length);
  bad.slice(0, 10).forEach((r) => console.log("BAD " + r.id + " " + JSON.stringify(r.rows)));
  out.widths.forEach((x) => console.log(x.width, "halyard overflow", JSON.stringify(x.halyardOverflow),
    "quarters overflow", JSON.stringify(x.quarterOverflow), JSON.stringify(x.quarterOverflowOpen),
    "|", JSON.stringify(x.quarterStatuses)));
  if (out.errors.length) console.log("errors", out.errors);
})();
