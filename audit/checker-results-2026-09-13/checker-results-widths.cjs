/* The checker's results at six widths: page and results height, overflow, and screenshots of the
   parts a reviewer reads first. Headless Chrome in a throwaway profile, through the audit's driver.
   node checker-results-widths.cjs <game-root> <out.json> <screenshot-dir> [sample] [label]
   Nothing is posted and nothing is saved from the page. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../independent-2026-09-13/runners/cdp.cjs");
const [ROOT, OUT, SHOTS, SAMPLE, LABEL] = process.argv.slice(2);
const sample = SAMPLE || "halyard", label = LABEL || "after";
const WIDTHS = [320, 375, 768, 1024, 1280, 1600];

(async () => {
  const { srv, port } = await serve(ROOT);
  const B = await launch("f1res");
  const base = `http://127.0.0.1:${port}/`;
  const out = { sample, label, widths: [], errors: [] };
  fs.mkdirSync(SHOTS, { recursive: true });
  try {
    for (const w of WIDTHS) {
      await B.width(w);
      await B.nav(base + "checker.html?sample=" + sample, "!!(window.__secondPass&&window.__secondPass())");
      await sleep(400);
      const m = await B.ev(`(function(){
        var o=document.getElementById('out'),r=o.getBoundingClientRect();
        var small=[];[].slice.call(document.querySelectorAll('#out *')).forEach(function(e){
          if(!e.childNodes.length||!e.getClientRects().length)return;
          var own=[].slice.call(e.childNodes).some(function(n){return n.nodeType===3&&n.textContent.trim();});
          if(own&&parseFloat(getComputedStyle(e).fontSize)<12)small.push(e.tagName+'.'+e.className+' '+getComputedStyle(e).fontSize);});
        return {doc:document.documentElement.scrollHeight,out:Math.round(r.height),outTop:Math.round(r.top+window.scrollY),
          details:document.querySelectorAll('#out details').length,open:document.querySelectorAll('#out details[open]').length,
          small:small.slice(0,6)};})()`);
      const over = await B.ev(OVERFLOW);
      const shot = async (name, y, h) => {
        const r = await B.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
          clip: { x: 0, y: Math.max(0, y), width: w, height: h, scale: 1 } });
        const f = path.join(SHOTS, `checker-${label}-${sample}-${w}-${name}.png`);
        fs.writeFileSync(f, Buffer.from(r.data, "base64"));
        return path.basename(f);
      };
      const H = w < 700 ? 1400 : 1000;
      const shots = [await shot("results-top", m.outTop - 20, H)];
      const q = await B.ev(`(function(){var e=document.getElementById('res-queue')||[].slice.call(document.querySelectorAll('#out h2')).filter(function(h){return /queue/i.test(h.textContent);})[0];
        return e?Math.round(e.getBoundingClientRect().top+window.scrollY):null;})()`);
      if (q !== null) shots.push(await shot("queue", q - 20, H));
      const sl = await B.ev(`(function(){var e=document.getElementById('res-silent');return e?Math.round(e.getBoundingClientRect().top+window.scrollY):null;})()`);
      if (sl !== null) shots.push(await shot("silent", sl - 20, w < 700 ? 900 : 600));
      const hero = await B.ev(`(function(){var e=document.querySelector('figure.shot');return e?Math.round(e.getBoundingClientRect().top+window.scrollY):null;})()`);
      if (hero !== null) shots.push(await shot("hero", hero - 10, w < 700 ? 900 : 800));
      /* opened: the first sentence and the ledger fold, and every anchor the jumps point at */
      const opened = await B.ev(`(function(){
        var d=document.querySelector('#out details.sent'),l=document.getElementById('res-ledger');
        if(!d)return null; d.open=true; if(l)l.open=true;
        var anchors=[].slice.call(document.querySelectorAll('#out a[href^="#"]')).map(function(a){return a.getAttribute('href');});
        var missing=anchors.filter(function(h){return !document.getElementById(h.slice(1));});
        return {y:Math.round(d.getBoundingClientRect().top+window.scrollY), ly:l?Math.round(l.getBoundingClientRect().top+window.scrollY):null,
          anchors:anchors.length, missing:missing};})()`);
      if (opened) {
        await sleep(150);
        shots.push(await shot("sentence-open", opened.y - 10, w < 700 ? 1500 : 1000));
        if (opened.ly !== null) shots.push(await shot("ledger-open", opened.ly - 10, w < 700 ? 1500 : 1000));
        m.anchors = opened.anchors; m.missingAnchors = opened.missing;
        m.overflowOpened = await B.ev(OVERFLOW);
      }
      out.widths.push({ width: w, heights: m, overflow: over, shots });
    }
    out.errors = B.errors.slice();
  } catch (e) {
    out.errors.push(String(e && e.stack || e));
  } finally {
    B.close(); srv.close();
  }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  out.widths.forEach((x) => console.log(x.width, "doc", x.heights.doc, "results", x.heights.out, "anchors", x.heights.anchors, "missing", JSON.stringify(x.heights.missingAnchors), "opened overflow clean", x.heights.overflowOpened && x.heights.overflowOpened.clean, "details", x.heights.details,
    "open", x.heights.open, "overflow clean", x.overflow.clean, x.overflow.bad.join(";"), "small", x.heights.small.join("; ")));
  if (out.errors.length) console.log("errors", out.errors);
})();
