/* Screenshots to look at, and the measurements beside them, at 320, 375, 768, 1024, 1280 and 1600.
   node shots.cjs <root> <outdir>

   One headless Chrome, test mode, nothing posted. Each state is set up once and captured at every
   width:
     author-grid-<w>      the case settings on author.html (the period box, the two-way choices)
     author-card-<w>      a keyed card after the Kestrel sample is read (boxes fitted to their text)
     read-<w>             the drill's read screen, top of the viewport (its edges against the header)
     codename-<w>         the masthead with the codename at the start of the track
     chart-<w>            Halyard line 1's two-bar picture (the month labels)
     explain-empty-<w>    fresh line 1 with a call and a chip, the three boxes empty
     explain-refused-<w>  the same after Lock it in was pressed (errors, status, focus)
     explain-refused-view-<w>  the viewport at that moment, where the focused box sits
     explain-ready-<w>    the boxes filled with good answers after the refusal
     end-counts-<w>       the end screen's counts, with one false flag
   Writes <outdir>/*.png and <outdir>/measure.json. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../author-repair-2026-09-13/cdp.cjs");
const [ROOT, OUTDIR] = [process.argv[2], process.argv[3] || path.join(__dirname, "shots")];
const WIDTHS = [320, 375, 768, 1024, 1280, 1600];
const GOOD = ["The June invoice from the lab is on file.", "It dates the charge to June, the month the memo covers.",
  "Ask for the June case log to confirm the volume."];

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const { srv, port } = await serve(ROOT);
  const B = await launch("f2shots");
  const ev = B.ev;
  const base = `http://127.0.0.1:${port}/`;
  const measure = { ran: new Date().toString(), widths: WIDTHS, states: {} };
  const setWidth = async (w) => {
    await B.send("Emulation.setDeviceMetricsOverride", { width: w, height: w < 700 ? 800 : 900, deviceScaleFactor: 1, mobile: w < 700 });
    await sleep(260);
  };
  /* a clip around an element in document coordinates, padded, and kept inside the page */
  const clipShot = async (file, selector, pad, extraBelow) => {
    const r = await ev(`(function(){var e=document.querySelector(${JSON.stringify(selector)});if(!e) return null;
      var b=e.getBoundingClientRect();return {x:b.left+scrollX,y:b.top+scrollY,w:b.width,h:b.height,dw:document.documentElement.scrollWidth,dh:document.documentElement.scrollHeight};})()`);
    if (!r) return false;
    const p = pad || 12;
    const x = Math.max(0, r.x - p), y = Math.max(0, r.y - p);
    const width = Math.min(r.dw - x, r.w + 2 * p), height = Math.min(r.dh - y, r.h + 2 * p + (extraBelow || 0));
    const shot = await B.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
      clip: { x, y, width, height, scale: 1 } });
    fs.writeFileSync(path.join(OUTDIR, file), Buffer.from(shot.data, "base64"));
    return true;
  };
  const viewShot = async (file) => {
    const shot = await B.send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(path.join(OUTDIR, file), Buffer.from(shot.data, "base64"));
  };
  const record = (state, w, data) => { (measure.states[state] = measure.states[state] || {})[w] = data; };
  try {
    /* ---------------- author.html ---------------- */
    const AREADY = "!!(window.__SPA&&window.SecondPassCore)";
    await setWidth(1280);
    await B.nav(base + "author.html", AREADY);
    await ev("localStorage.clear();sessionStorage.clear();true");
    await B.nav(base + "author.html", AREADY);
    for (const w of WIDTHS) {
      await setWidth(w);
      await ev("window.scrollTo(0,0);true");
      await clipShot("author-grid-" + w + ".png", ".setgrid", 16);
      record("author-grid", w, await ev(`(function(){
        var p=document.getElementById('cperiod'), cs=getComputedStyle(p), c=document.createElement('canvas').getContext('2d');
        c.font=cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;
        var inner=p.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
        var seg=function(id){return [].map.call(document.querySelectorAll('#'+id+' button'),function(b){return {text:b.textContent,h:b.getBoundingClientRect().height,lines:Math.round(b.scrollHeight/parseFloat(getComputedStyle(b).lineHeight||20))};});};
        return {periodPlaceholderFits:c.measureText(p.placeholder).width<=inner, placeholderPx:Math.round(c.measureText(p.placeholder).width), innerPx:Math.round(inner),
          rule:seg('ruleseg'), zero:seg('zeroseg'), overflow:${OVERFLOW}};})()`));
    }
    await setWidth(1280);
    await ev("document.getElementById('loadsample').click();true"); await sleep(120);
    await ev("document.getElementById('read').click();true"); await sleep(600);
    for (const w of WIDTHS) {
      await setWidth(w);
      await sleep(200);
      const pick = await ev(`(function(){var best=null,score=-1;[].forEach.call(document.querySelectorAll('#cards .kcard'),function(k,ix){
        var s=0;[].forEach.call(k.querySelectorAll('textarea'),function(t){s+=t.value.length;});if(s>score){score=s;best=ix;}});
        [].forEach.call(document.querySelectorAll('#cards .kcard'),function(k,ix){k.id=k.id||('shotcard'+ix);});
        return best;})()`);
      await clipShot("author-card-" + w + ".png", "#cards .kcard:nth-child(" + (pick + 1) + ")", 10);
      record("author-card", w, await ev(`(function(){var bad=[];[].forEach.call(document.querySelectorAll('.kcard textarea'),function(t){
        if(t.offsetParent&&t.scrollHeight>t.clientHeight+2) bad.push(t.id+' '+t.scrollHeight+'>'+t.clientHeight);});
        return {textareasCut:bad, overflow:${OVERFLOW}};})()`));
    }
    /* the sample's provenance: replace the ledger, and the made-up answer is taken back */
    await setWidth(1280);
    measure.sampleOrigin = {
      afterSample: await ev("(function(){var b=document.querySelector('#originseg [aria-pressed=\"true\"]');return b?b.getAttribute('data-v'):null;})()"),
    };
    await ev(`(function(){var e=document.getElementById('ledger');e.value='6100\\tRent expense\\t100000\\t130000';e.dispatchEvent(new Event('input',{bubbles:true}));return true;})()`);
    measure.sampleOrigin.afterReplacingLedger = await ev("(function(){var b=document.querySelector('#originseg [aria-pressed=\"true\"]');return b?b.getAttribute('data-v'):null;})()");
    measure.sampleOrigin.message = await ev("document.getElementById('msg').textContent");

    /* ---------------- the drill ---------------- */
    const url = base + "index.html?test=1&case=halyard";
    const READY = "!!(window.__BTM_CASES&&window.__BTM&&document.getElementById('screen')&&document.getElementById('screen').children.length)";
    await B.nav(url, READY);
    await ev("sessionStorage.clear();localStorage.removeItem('btm.owncase.v1');true");
    await B.nav(url, READY);
    const st = await ev("__BTM_STEPS()");
    await ev("document.getElementById('go').click();true"); await sleep(120);
    await ev("document.getElementById('noticego').click();true"); await sleep(120);
    await ev("var i=document.getElementById('cn');i.value='Silver Ledger';i.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#orgs .chip').click();document.getElementById('next').click();true");
    await sleep(200);
    for (const w of WIDTHS) {
      await setWidth(w);
      await ev("window.scrollTo(0,0);true"); await sleep(120);
      await viewShot("read-" + w + ".png");
      record("read", w, await ev(`(function(){var m=document.querySelector('#sp-nav .mark'), band=document.querySelector('#mason b'), h=document.getElementById('orienthead'), st=document.querySelector('.stmt'), bandBox=document.getElementById('mason');
        var L=function(e){return e?Math.round(e.getBoundingClientRect().left):null;}, R=function(e){return e?Math.round(e.getBoundingClientRect().right):null;};
        return {wordmark:L(m), bandText:L(band), bandEdge:L(bandBox), heading:L(h), ledgerCard:L(st), navRight:R(document.querySelector('#sp-nav nav')), bandRight:R(bandBox), overflow:${OVERFLOW}};})()`));
    }
    await ev(`(function(){var a=String(__BTM_CARDS[0].acct);var c=Array.prototype.filter.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.textContent.split(' ')[0]===a;})[0];if(c) c.click();
      var go=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){var r=b.getBoundingClientRect();return r.width>0&&r.height>0;})[0];if(go) go.click();return true;})()`);
    await sleep(250);
    for (const w of WIDTHS) {
      await setWidth(w);
      await ev("window.scrollTo(0,0);true"); await sleep(420);
      await clipShot("codename-" + w + ".png", "#mason", 0, 0);
      await clipShot("chart-" + w + ".png", "#screen .chart", 14);
      record("codename-chart", w, await ev(`(function(){var tag=document.getElementById('codetag'), b=document.querySelector('#mason b'), labs=[].map.call(document.querySelectorAll('#screen .chartlab'),function(x){return {text:x.textContent, px:parseFloat(getComputedStyle(x).fontSize), w:Math.round(x.getBoundingClientRect().width)};});
        return {codetagLeft:Math.round(tag.getBoundingClientRect().left), bandTextLeft:Math.round(b.getBoundingClientRect().left), chartLabels:labs, overflow:${OVERFLOW}};})()`));
    }
    /* the fourteen practice lines, one clean line flagged */
    await setWidth(1280);
    const falseFlagAt = await ev("__BTM_CARDS.findIndex(function(c){return c.key==='stand';})");
    let guard = 0;
    while (guard++ < 200) {
      const s = await ev("__BTM.step");
      if (s === st.bridge) break;
      if (await ev("!!document.getElementById('next')")) { await ev("document.getElementById('next').click();true"); await sleep(50); continue; }
      const i = s - 3;
      await ev(`(function(){var c=__BTM_CARDS[${i}];var want=${i}===${falseFlagAt}?'flag':c.key;document.getElementById(want).click();
        var chips=[].slice.call(document.querySelectorAll('#commit .chip'));var chip=want==='flag'&&c.key==='stand'?'no source on file':(c.basisKey||[])[0];
        var hit=chips.filter(function(x){return x.textContent.trim()===chip;})[0]||chips[0];if(hit) hit.click();document.getElementById('lockin').click();return true;})()`);
      await sleep(60);
    }
    await ev("document.getElementById('r2go').click();true"); await sleep(200);
    await ev(`(function(){var c=__BTM_CARDS2[0];document.getElementById(c.key).click();return true;})()`); await sleep(80);
    await ev(`(function(){var chips=[].slice.call(document.querySelectorAll('#commit .chip'));var want=(__BTM_CARDS2[0].basisKey||[])[0];
      var hit=chips.filter(function(x){return x.textContent.trim()===want;})[0]||chips[0];hit.click();return true;})()`);
    await sleep(80);
    const explainMeasure = `(function(){var boxes=[].map.call(document.querySelectorAll('#screen textarea.explain'),function(t){
        var err=document.getElementById(t.id+'-err');return {id:t.id, h:Math.round(t.getBoundingClientRect().height), cut:t.scrollHeight>t.clientHeight+2,
        invalid:t.getAttribute('aria-invalid'), error:err&&!err.hidden?err.textContent:null};});
      var st=document.getElementById('lockstat'), a=document.activeElement, r=a?a.getBoundingClientRect():null;
      var bars=[].filter.call(document.querySelectorAll('body *'),function(e){var p=getComputedStyle(e).position;return (p==='fixed'||p==='sticky')&&e.getBoundingClientRect().height>0;}).map(function(e){var b=e.getBoundingClientRect();return {el:e.id||e.className,top:Math.round(b.top),bottom:Math.round(b.bottom)};});
      return {boxes:boxes, status:st?st.textContent:null, lockAria:(document.getElementById('lockin')||{}).getAttribute?document.getElementById('lockin').getAttribute('aria-disabled'):null,
        active:a?(a.id||a.className):null, activeTop:r?Math.round(r.top):null, activeBottom:r?Math.round(r.bottom):null, viewport:innerHeight, bars:bars, overflow:${OVERFLOW}};})()`;
    for (const w of WIDTHS) {
      await setWidth(w);
      await clipShot("explain-empty-" + w + ".png", "#commit", 12);
      record("explain-empty", w, await ev(explainMeasure));
    }
    await setWidth(1280);
    await ev("document.getElementById('lockin').click();true"); await sleep(200);
    for (const w of WIDTHS) {
      await setWidth(w);
      /* the refusal again at this width, so focus and the scroll land where a player at this width sees them */
      await ev("document.getElementById('lockin').click();true"); await sleep(350);
      await viewShot("explain-refused-view-" + w + ".png");
      record("explain-refused", w, await ev(explainMeasure));
      await clipShot("explain-refused-" + w + ".png", "#commit", 12);
    }
    await setWidth(1280);
    for (const [k, id] of [[0, "ex-decisiveEvidence"], [1, "ex-periodRelevance"], [2, "ex-actionOrRequest"]]) {
      await ev(`(function(){var t=document.getElementById('${id}');t.focus();t.setSelectionRange(0,t.value.length);return true;})()`);
      await B.send("Input.insertText", { text: GOOD[k] });
      await sleep(60);
    }
    for (const w of WIDTHS) {
      await setWidth(w);
      await clipShot("explain-ready-" + w + ".png", "#commit", 12);
      record("explain-ready", w, await ev(explainMeasure));
    }
    /* finish round two and look at the end screen's counts */
    await setWidth(1280);
    for (let i = 0; i < 5; i++) {
      if (i > 0) {
        await ev(`(function(){var c=__BTM_CARDS2[${i}];document.getElementById(c.key).click();return true;})()`); await sleep(60);
        await ev(`(function(){var chips=[].slice.call(document.querySelectorAll('#commit .chip'));var want=(__BTM_CARDS2[${i}].basisKey||[])[0];
          var hit=chips.filter(function(x){return x.textContent.trim()===want;})[0]||chips[0];hit.click();return true;})()`);
        for (const [k, id] of [[0, "ex-decisiveEvidence"], [1, "ex-periodRelevance"], [2, "ex-actionOrRequest"]]) {
          await ev(`(function(){var t=document.getElementById('${id}');t.focus();t.setSelectionRange(0,t.value.length);return true;})()`);
          await B.send("Input.insertText", { text: GOOD[k] });
        }
      }
      await ev("document.getElementById('lockin').click();true"); await sleep(150);
    }
    await ev("document.getElementById('r2done').click();true"); await sleep(250);
    for (const w of WIDTHS) {
      await setWidth(w);
      await clipShot("end-counts-" + w + ".png", ".final .counts", 40, 40);
      record("end-counts", w, await ev(`({counts:[].map.call(document.querySelectorAll('.final .counts span'),function(s){return s.textContent;}), overflow:${OVERFLOW}})`));
    }
    measure.errors = B.errors;
  } catch (e) {
    measure.failure = e.stack || e.message;
    measure.errors = B.errors;
    console.log("FAILURE " + measure.failure);
  } finally {
    B.close();
    srv.close();
  }
  fs.writeFileSync(path.join(OUTDIR, "measure.json"), JSON.stringify(measure, null, 1));
  console.log("wrote " + fs.readdirSync(OUTDIR).filter((f) => f.endsWith(".png")).length + " screenshots to " + OUTDIR);
})();
