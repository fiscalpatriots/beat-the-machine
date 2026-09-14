/* Clearance grammar, lane F1: the author page against the checker on every input the checker
   holds, then both pages read at four widths.
   node author-and-widths.cjs <game-root> <out.json> <screenshot-dir>
   Headless Chrome in a throwaway profile, through the audit's own driver. Nothing is posted
   and nothing is saved from the page. Every input is synthetic. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../../independent-2026-09-13/runners/cdp.cjs");
const [ROOT, OUT, SHOTS] = process.argv.slice(2);

/* the checker's own statuses, from the suite harness, for the same inputs */
let src = fs.readFileSync(path.join(ROOT, "tests/run-checker-tests.cjs"), "utf8").replace(/^#![^\n]*\n/, "").split("const only =")[0];
const execute = new Function("require", "__dirname", src + "\nreturn execute;")(require, path.join(ROOT, "tests"));

const FIX = JSON.parse(fs.readFileSync(path.join(ROOT, "tests/checker-fixtures.json"), "utf8"));
const PLAIN = (f) => f.inputs && f.inputs.ledger && f.inputs.memo && !f.cols && !(f.inputs.ratios || "").trim() &&
  !f.inputs.dollar && !f.inputs.pct && !f.inputs.rule && !f.inputs.zerobase;
const INPUTS = FIX.filter((f) => /^(?:[AB][0-9]{3}|CUR|SIGN|SAME|PER|ANA|RESP|QTY)/.test(f.id) && PLAIN(f))
  .map((f) => ({ id: f.id, ledger: f.inputs.ledger, memo: f.inputs.memo }));
const TWO = "6100\tRent expense\t100000\t130000\n6200\tInsurance expense\t50000\t95000";
const D6 = "1. Rent expense rose 30,000 euros.\n2. Insurance expense changed by $-45,000.\n3. Rent expense was stable at $130,000.\n" +
  "4. Insurance expense rose $45,000, or 90 percent, year over year.";
INPUTS.unshift({ id: "D6 memo", ledger: TWO, memo: D6 });
const SHOWCASE = "1. Rent expense rose $30,000, or 30 percent, on the new Suite 200 lease.\n" +
  "2. Rent expense was stable at $130,000.\n3. Insurance expense rose $45,000, or 90 percent, year over year.\n" +
  "4. Rent expense rose $30,000; so did Insurance expense.";

(async () => {
  const { srv, port } = await serve(ROOT);
  const B = await launch("f1");
  const base = `http://127.0.0.1:${port}/`;
  const out = { root: ROOT, author: [], widths: [], errors: [] };
  const set = `window.__set=function(id,v){var e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));return true;};true`;
  try {
    /* ---- 1. the author page on every audit probe and mutation */
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
      await sleep(60);
      const a = await B.ev(`({sents:__SPA.sentences(),cards:__SPA.cards().map(function(c){return {label:c.label,status:c.status,key:c.key,type:c.type,found:(c.found||[]).join(' ')};})})`);
      const rows = a.sents.map((s) => {
        const card = a.cards.find((c) => c.label === s.label) || null;
        const cst = chk.status[s.label];
        return { label: s.label, author: s.status, checker: cst, key: card ? card.key : null,
          namesWord: card && cst === "needs review" ? /held for a person to read/.test(card.found) : null };
      });
      const bad = rows.filter((r) => r.author !== r.checker || (r.checker !== "checked within scope" && r.key === "stand"));
      out.author.push({ id: t.id, rows, ok: !bad.length });
    }
    /* ---- 2. both pages at four widths, with the held sentences on screen */
    for (const w of [320, 375, 1024, 1600]) {
      await B.width(w);
      await B.nav(base + "checker.html", "!!document.getElementById('run')");
      await B.ev(`document.getElementById('ledger').value=${JSON.stringify(TWO)};document.getElementById('memo').value=${JSON.stringify(SHOWCASE)};document.getElementById('run').click();true`);
      await sleep(300);
      const cOver = await B.ev(OVERFLOW);
      const cBox = await B.ev(`(function(){var rows=[].slice.call(document.querySelectorAll('#out tr,#out li')).filter(function(e){return /OUTSIDE THE GRAMMAR|Unread wording/i.test(e.textContent);});
        if(!rows.length)return null; var r=rows[0].getBoundingClientRect(); return {y:Math.max(0,r.top+window.scrollY-40),n:rows.length};})()`);
      const cFile = path.join(SHOTS, "checker-" + w + ".png");
      if (cBox) {
        const r = await B.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
          clip: { x: 0, y: cBox.y, width: w, height: w < 700 ? 1100 : 900, scale: 1 } });
        fs.writeFileSync(cFile, Buffer.from(r.data, "base64"));
      }
      await B.nav(base + "author.html", ready);
      await B.ev(set);
      await B.ev(`__set('ledger',${JSON.stringify(TWO)});__set('memo',${JSON.stringify(SHOWCASE)});true`);
      await B.ev("document.getElementById('read').click();true");
      await sleep(300);
      const aOver = await B.ev(OVERFLOW);
      const aBox = await B.ev(`(function(){var k=[].slice.call(document.querySelectorAll('#cards .kcard')).filter(function(e){return /held for a person to read/.test(e.textContent);});
        if(!k.length)return null; var r=k[0].getBoundingClientRect(); return {y:Math.max(0,r.top+window.scrollY-20),h:r.height,n:k.length};})()`);
      const aFile = path.join(SHOTS, "author-" + w + ".png");
      if (aBox) {
        const r = await B.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
          clip: { x: 0, y: aBox.y, width: w, height: Math.min(1400, Math.max(700, aBox.h + 40)), scale: 1 } });
        fs.writeFileSync(aFile, Buffer.from(r.data, "base64"));
      }
      out.widths.push({ width: w, checker: { overflow: cOver, heldRows: cBox && cBox.n, shot: cBox ? path.basename(cFile) : null },
        author: { overflow: aOver, heldCards: aBox && aBox.n, shot: aBox ? path.basename(aFile) : null } });
    }
    out.errors = B.errors.slice();
  } catch (e) {
    out.errors.push(String(e && e.stack || e));
  } finally {
    B.close(); srv.close();
  }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  const bad = out.author.filter((r) => !r.ok);
  const held = out.author.reduce((n, r) => n + r.rows.filter((x) => x.checker !== "checked within scope").length, 0);
  const named = out.author.reduce((n, r) => n + r.rows.filter((x) => x.namesWord).length, 0);
  console.log("author inputs " + out.author.length + ", sentences held by the checker " + held +
    ", author disagrees or suggests a stand on " + bad.length + ", needs-review cards naming the word " + named);
  bad.slice(0, 10).forEach((r) => console.log("BAD " + r.id + " " + JSON.stringify(r.rows)));
  out.widths.forEach((x) => console.log(x.width, "checker", JSON.stringify(x.checker), "author", JSON.stringify(x.author)));
  if (out.errors.length) console.log("errors", out.errors);
})();
