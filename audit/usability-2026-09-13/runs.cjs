/* The "How a review runs" section of review.html at each width: a clipped shot of the section,
   the card sizes, the smallest text inside it, and the page's sideways overflow.
   node runs.cjs <root> <outdir> <label> [widths] */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../author-repair-2026-09-13/cdp.cjs");
const { setWidth } = require("./shoot.cjs");
const [ROOT, OUTDIR, LABEL, WL] = process.argv.slice(2);
const WIDTHS = (WL || "320,375,768,1009,1024,1280,1600").split(",").map(Number);

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const { srv, port } = await serve(ROOT);
  const B = await launch("runs");
  const out = [];
  try {
    for (const w of WIDTHS) {
      await setWidth(B, w, 1);
      await B.nav(`http://127.0.0.1:${port}/review.html`);
      await B.ev("document.fonts.ready.then(function(){return true})");
      await B.ev("Array.prototype.forEach.call(document.querySelectorAll('img[loading=lazy]'),function(i){i.loading='eager';});Promise.all(Array.prototype.map.call(document.images,function(i){return i.complete?1:new Promise(function(r){i.onload=i.onerror=r;});})).then(function(){return true})");
      await sleep(300);
      const m = await B.ev(`(function(){
        var s=document.querySelector('.runs'), r=s.getBoundingClientRect();
        var cards=Array.prototype.map.call(document.querySelectorAll('.shot'),function(e){var b=e.getBoundingClientRect();
          var v=e.querySelector('.viz,img'), vb=v.getBoundingClientRect(), cap=e.querySelector('figcaption'), cb=cap.getBoundingClientRect();
          return {x:Math.round(b.left),y:Math.round(b.top-r.top),w:Math.round(b.width),h:Math.round(b.height),visual:[Math.round(vb.width),Math.round(vb.height)],capTop:Math.round(cb.top-r.top),capFont:getComputedStyle(cap.querySelector('p')).fontSize};});
        var min=99, minTxt='';
        Array.prototype.forEach.call(s.querySelectorAll('*'),function(e){var own=Array.prototype.some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim();});
          if(!own) return; var f=parseFloat(getComputedStyle(e).fontSize); if(f<min){min=f;minTxt=e.textContent.trim().slice(0,30);}});
        var clipped=[];Array.prototype.forEach.call(s.querySelectorAll('*'),function(e){if(e.scrollWidth>e.clientWidth+1&&e.clientWidth>0&&getComputedStyle(e).display!=='inline') clipped.push(e.className+' '+e.scrollWidth+'>'+e.clientWidth);});
        return {top:Math.round(r.top+scrollY),height:Math.round(r.height),width:Math.round(r.width),cards:cards,minFont:min,minTxt:minTxt,innerOverflow:clipped.slice(0,8)};})()`);
      const ov = await B.ev(OVERFLOW);
      const shot = await B.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
        clip: { x: 0, y: Math.max(0, m.top - 16), width: w, height: m.height + 32, scale: 1 } });
      const file = path.join(OUTDIR, `steps-${w}-${LABEL}.png`);
      fs.writeFileSync(file, Buffer.from(shot.data, "base64"));
      out.push({ width: w, file: path.basename(file), ...m, doc: ov.doc, clean: ov.clean, bad: ov.bad });
      console.log(w, JSON.stringify({ h: m.height, cards: m.cards.map((c) => c.w + "x" + c.h + " vis " + c.visual.join("x") + " cap@" + c.capTop), min: m.minFont + " " + m.minTxt, inner: m.innerOverflow, doc: ov.doc, clean: ov.clean }));
    }
  } catch (e) { console.log("ERR", e.message); }
  finally { B.close(); srv.close(); fs.writeFileSync(path.join(OUTDIR, `steps-${LABEL}.json`), JSON.stringify(out, null, 1)); process.exit(0); }
})();
