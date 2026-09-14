/* Walk the drill in test mode from intro to the end screen by clicking, on one case, at one width.
   Records the orientation screen, the payload's round one field, the record's keys, and for the
   fresh assessment items whether the lock waits on the written explanation.
   node walk-drill.cjs <root> <case> <width> <out.json> */
const fs = require("fs");
const { serve, launch, sleep, OVERFLOW } = require("./cdp.cjs");
const [ROOT, CASE, WIDTH, OUT] = [process.argv[2], process.argv[3] || "halyard", Number(process.argv[4] || 1280), process.argv[5]];

(async () => {
  const { srv, port } = await serve(ROOT);
  const B = await launch("walk");
  const base = `http://127.0.0.1:${port}/`;
  const out = { case: CASE, width: WIDTH, screens: [], widths: [] };
  const ev = B.ev;
  try {
    await B.width(WIDTH);
    await B.nav(base + "index.html?test=1&case=" + CASE, "!!(window.__BTM_CASES&&document.getElementById('go'))");
    await ev("sessionStorage.clear();localStorage.removeItem('btm.owncase.v1');true");
    await B.nav(base + "index.html?test=1&case=" + CASE, "!!(window.__BTM_CASES&&document.getElementById('go'))");
    out.cases = await ev("({one:__BTM_CASES.one,two:__BTM_CASES.two,assessment:__BTM_CASES.assessment,lines:__BTM_CASES.lines,lines2:__BTM_CASES.lines2})");
    const audit = async (tag) => { const o = await ev(OVERFLOW); out.widths.push({ tag, ...o }); };
    await audit("intro");
    await ev("document.getElementById('go').click();true"); await sleep(100);
    await ev("document.getElementById('noticego').click();true"); await sleep(100);
    await ev("var i=document.getElementById('cn');i.value='Walk Test';i.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#orgs .chip').click();document.getElementById('next').click();true");
    await sleep(150);
    /* Since 29df0aa the read before the draft is required: no skip, at least one line tapped.
       The walk presses the visible onward button once with nothing tapped (it must stay on the
       read), taps the first card's account, and goes on. */
    const visibleGo = "Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){var r=b.getBoundingClientRect();return r.width>0&&r.height>0;})";
    out.orientation = await ev(`({step:__BTM.step, prepickSection:!!document.querySelector('.prepick'), chips:document.querySelectorAll('#prepicks .chip').length,
      onward:${visibleGo}.map(function(b){return b.textContent;}),
      skipControls:Array.prototype.filter.call(document.querySelectorAll('#screen button'),function(b){return /skip/i.test(b.textContent);}).length,
      text:document.getElementById('screen').textContent.replace(/\\s+/g,' ').slice(0,300)})`);
    await audit("orientation");
    await ev(`(function(){var b=${visibleGo}[0];if(b) b.click();return true;})()`); await sleep(150);
    out.stepAfterEmptyPress = await ev("__BTM.step");
    await ev(`(function(){var a=String(__BTM_CARDS[0].acct);var c=Array.prototype.filter.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.textContent.split(' ')[0]===a;})[0];if(c) c.click();
      var b=${visibleGo}[0];if(b) b.click();return true;})()`); await sleep(150);
    out.afterOrientationStep = await ev("__BTM.step");
    const st = await ev("__BTM_STEPS()");
    let guard = 0, explainSeen = [];
    while (guard++ < 400) {
      const s = await ev("__BTM.step");
      if (s === 92) { await audit("fresh results"); await ev("document.getElementById('r2done').click();true"); await sleep(80); continue; }
      if (s >= st.done) break;
      if (s === st.bridge) { await audit("bridge"); await ev("document.getElementById('r2go').click();true"); await sleep(80); continue; }
      const hasNext = await ev("!!document.getElementById('next')");
      if (hasNext) { await ev("document.getElementById('next').click();true"); await sleep(60); continue; }
      const round = s >= st.l2 ? 2 : 1, i = round === 2 ? s - st.l2 : s - 3;
      /* take the key's call and its first key basis chip */
      const r = await ev(`(function(){
        var c=${round}===2?__BTM_CARDS2[${i}]:__BTM_CARDS[${i}];
        var b=document.getElementById(c.key);
        if(!b) return {err:'no call button', html:document.getElementById('screen').innerHTML.slice(0,400)};
        b.click(); return {key:c.key, basis:(c.basisKey||[])[0]||null};
      })()`);
      if (r.err) { out.failure = "step " + s + ": " + r.err + " " + r.html; break; }
      await sleep(60);
      const e = await ev(`(function(){
        var chips=Array.prototype.slice.call(document.querySelectorAll('#commit .chip'));
        var want=${JSON.stringify(r.basis)};
        var hit=chips.filter(function(x){return x.textContent.trim().toLowerCase()===String(want).toLowerCase();})[0]||chips[0];
        if(hit) hit.click();
        var box=document.querySelectorAll('#screen textarea.explain');
        var lock=document.getElementById('lockin');
        return {chips:chips.length, explainBoxes:box.length, lockDisabledBefore: lock?!!lock.disabled:null};
      })()`);
      if (e.explainBoxes) {
        await audit("assessment item " + (i + 1) + " explanation open");
        const blocked = await ev("(function(){var l=document.getElementById('lockin');return l?!!l.disabled:null;})()");
        await ev(`Array.prototype.forEach.call(document.querySelectorAll('#screen textarea.explain'),function(t,k){
          t.value=['The dated schedule lists no plan starting in June.','A June driver needs a June document.','Ask for the June enrollment report.'][k]||'x';
          t.dispatchEvent(new Event('input',{bubbles:true}));});true`);
        const after = await ev("(function(){var l=document.getElementById('lockin');return l?!!l.disabled:null;})()");
        explainSeen.push({ item: i + 1, boxes: e.explainBoxes, lockBlockedEmpty: blocked, lockOpenFilled: after === false });
      }
      await ev("(function(){var l=document.getElementById('lockin');if(l) l.click();return true;})()");
      await sleep(80);
    }
    out.explanations = explainSeen;
    out.endStep = await ev("__BTM.step");
    await audit("end");
    await ev("(function(){var b=document.getElementById('sendres');if(b) b.click();return true;})()"); await sleep(300);
    out.post = await ev("(function(){var p=window.__BTM_LAST_POST||{};return {round1:p['entry.1115022539']||null, qc:p['entry.756559246']||null};})()");
    out.record = await ev(`(function(){var r=__BTM_RECORD(null);return {keys:Object.keys(r), prepicks:('prepicks' in r),
      prompts:r.writtenExplanationPrompts||null, r2:r.responses.filter(function(x){return x.round===2;}).map(function(x){return {item:x.item,caseVersion:x.caseVersion,required:x.writtenExplanationRequired,explanation:x.writtenExplanation};}), r1sample:(function(x){return {item:x.item,required:x.writtenExplanationRequired,explanation:x.writtenExplanation};})(r.responses[0])};})()`);
    out.payloadRound1 = await ev("(function(){try{return (window.__BTM_PAYLOAD?__BTM_PAYLOAD():null);}catch(e){return String(e);}})()");
    out.text = await ev("(function(){try{return typeof asText==='function'?null:null;}catch(e){return null;}})()");
    out.errors = B.errors;
  } catch (e) { out.failure = (out.failure || "") + e.message; out.errors = B.errors; }
  finally { B.close(); srv.close(); }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ failure: out.failure, errors: out.errors, cases: out.cases, orientation: out.orientation,
    afterOrientationStep: out.afterOrientationStep, endStep: out.endStep, explanations: out.explanations,
    recordKeys: out.record && out.record.keys, prepicksInRecord: out.record && out.record.prepicks, post: out.post, prompts: out.record && out.record.prompts, r2: out.record && out.record.r2, r1sample: out.record && out.record.r1sample,
    widthsBad: out.widths.filter((w) => !w.clean) }, null, 1));
})();
