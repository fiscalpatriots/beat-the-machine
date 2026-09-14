/* Viewport screenshots of the read before the draft and of the end screen's comparison, at six
   widths, for a person to open and look at. Full-page captures misplace the fixed bars, so every
   image here is exactly what the window shows.
   node shots-prepicks.cjs <root> <outdir>
   Writes read-top-<w>.png, read-chips-<w>.png (two lines tapped) and end-<w>.png (the comparison
   with its disclosure open) for 320, 375, 768, 1024, 1280 and 1600, and shots.json with the
   overflow audit and the bounding boxes of the parts that must not clip. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../author-repair-2026-09-13/cdp.cjs");
const [ROOT, OUTDIR] = [process.argv[2], process.argv[3] || path.join(__dirname, "shots")];
const WIDTHS = [320, 375, 768, 1024, 1280, 1600];

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const { srv, port } = await serve(ROOT);
  const B = await launch("prepick-shots");
  const ev = B.ev;
  const url = `http://127.0.0.1:${port}/index.html?test=1&case=halyard`;
  const READY = "!!(window.__BTM_CASES&&window.__BTM&&document.getElementById('screen')&&document.getElementById('screen').children.length)";
  const out = { ran: new Date().toString(), widths: {} };
  const viewShot = async (file) => {
    const r = await B.send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(path.join(OUTDIR, file), Buffer.from(r.data, "base64"));
  };
  const setWidth = (w) => B.send("Emulation.setDeviceMetricsOverride",
    { width: w, height: w < 700 ? 760 : (w < 1100 ? 820 : 1000), deviceScaleFactor: 1, mobile: w < 700 });
  const BOXES = `(function(){function box(sel){var e=document.querySelector(sel);if(!e) return null;var r=e.getBoundingClientRect();
      return {l:Math.round(r.left),r:Math.round(r.right),w:Math.round(r.width),h:Math.round(r.height)};}
    var vw=document.documentElement.clientWidth;
    var chips=Array.prototype.map.call(document.querySelectorAll('#prepicks .chip'),function(b){var r=b.getBoundingClientRect();
      return {r:Math.round(r.right),w:Math.round(r.width),h:Math.round(r.height),font:parseFloat(getComputedStyle(b).fontSize)};});
    return {vw:vw, section:box('#prepicksection'), stat:box('#prepickstat'), readshift:box('.readshift'),
      chipsPastEdge:chips.filter(function(c){return c.r>vw;}).length, chipMinHeight:Math.min.apply(null,chips.map(function(c){return c.h;}).concat([999])),
      chipFont:chips.length?chips[0].font:null,
      goes:Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){return b.getBoundingClientRect().width>0;}).map(function(b){
        var r=b.getBoundingClientRect();return {l:Math.round(r.left),r:Math.round(r.right),t:Math.round(r.top),b:Math.round(r.bottom),w:Math.round(r.width),text:b.textContent};})};})()`;
  try {
    for (const w of WIDTHS) {
      await setWidth(w);
      await B.nav(url, READY);
      await ev("sessionStorage.clear();true");
      await B.nav(url, READY);
      await ev("document.getElementById('go').click();true"); await sleep(120);
      await ev("document.getElementById('noticego').click();true"); await sleep(120);
      await ev("var i=document.getElementById('cn');i.value='Shots';i.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#orgs .chip').click();document.getElementById('next').click();true");
      await sleep(350);
      const rec = { overflow: await ev(OVERFLOW), top: await ev(BOXES) };
      await viewShot("read-top-" + w + ".png");
      /* the page's own scroll: press the onward button with nothing tapped, then tap two lines */
      await ev("(function(){var b=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){return b.getBoundingClientRect().width>0;})[0];b.click();return true;})()");
      await sleep(300);
      rec.headingAfterEmptyPress = await ev("(function(){var h=document.getElementById('prepickhead').getBoundingClientRect(),b=document.getElementById('bar').getBoundingClientRect();return {headingTop:Math.round(h.top),barBottom:Math.round(b.bottom),clear:h.top>=b.bottom};})()");
      for (const p of ["1", "10"]) await ev(`document.querySelector('#prepicks .chip[data-p="${p}"]').click();true`);
      await sleep(150);
      rec.chips = await ev(BOXES);
      rec.chipsOverflow = await ev(OVERFLOW);
      await viewShot("read-chips-" + w + ".png");
      out.widths[w] = rec;
    }

    /* one run to the end at 375, then the comparison at every width */
    await setWidth(375); await sleep(200);
    await ev("(function(){var b=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){return b.getBoundingClientRect().width>0;})[0];b.click();return true;})()");
    await sleep(250);
    const st = await ev("__BTM_STEPS()");
    const off = [0, 3, 6];
    let guard = 0;
    while (guard++ < 400) {
      const s = await ev("__BTM.step");
      if (s === 92) { await ev("document.getElementById('r2done').click();true"); await sleep(100); continue; }
      if (s >= st.done) break;
      if (s === st.bridge) { await ev("document.getElementById('r2go').click();true"); await sleep(100); continue; }
      if (await ev("!!document.getElementById('next')")) { await ev("document.getElementById('next').click();true"); await sleep(60); continue; }
      const round = s >= st.l2 ? 2 : 1, i = round === 2 ? s - st.l2 : s - 3;
      await ev(`(function(){var c=(${round}===2?__BTM_CARDS2:__BTM_CARDS)[${i}];var want=c.key;
        if(${round}===1 && ${JSON.stringify(off)}.indexOf(${i})>-1) want=(want==='flag'?'stand':'flag');
        document.getElementById(want).click();return true;})()`);
      await sleep(50);
      await ev(`(function(){var chips=document.querySelectorAll('#commit .chip');if(chips[0]) chips[0].click();
        Array.prototype.forEach.call(document.querySelectorAll('#screen textarea.explain'),function(t){t.value='A written answer for the shot.';t.dispatchEvent(new Event('input',{bubbles:true}));});
        var l=document.getElementById('lockin');if(l) l.click();return true;})()`);
      await sleep(80);
    }
    await ev("(function(){var d=document.querySelector('.readshift details');if(d) d.open=true;return true;})()");
    for (const w of WIDTHS) {
      await setWidth(w); await sleep(300);
      await ev("(function(){var s=document.querySelector('.readshift');var y=s.getBoundingClientRect().top+window.scrollY-document.getElementById('bar').offsetHeight-12;window.scrollTo(0,y);return true;})()");
      await sleep(250);
      out.widths[w].end = { overflow: await ev(OVERFLOW), boxes: await ev(BOXES), text: await ev("document.querySelector('.readshift').innerText.slice(0,400)") };
      await viewShot("end-" + w + ".png");
    }
    out.errors = B.errors;
  } catch (e) {
    out.failure = e.message; out.errors = B.errors;
  } finally { B.close(); srv.close(); }
  fs.writeFileSync(path.join(OUTDIR, "shots.json"), JSON.stringify(out, null, 2));
  const summary = {};
  for (const w of WIDTHS) {
    const r = out.widths[w] || {};
    summary[w] = { overflowTop: r.overflow && r.overflow.clean, overflowChips: r.chipsOverflow && r.chipsOverflow.clean,
      overflowEnd: r.end && r.end.overflow.clean, chipsPastEdge: r.chips && r.chips.chipsPastEdge, chipFont: r.chips && r.chips.chipFont,
      chipMinHeight: r.chips && r.chips.chipMinHeight, goes: r.chips && r.chips.goes.map((g) => g.text + " " + g.l + "-" + g.r),
      headingAfterEmptyPress: r.headingAfterEmptyPress };
  }
  console.log(JSON.stringify({ failure: out.failure || null, errors: out.errors, summary }, null, 1));
})();
