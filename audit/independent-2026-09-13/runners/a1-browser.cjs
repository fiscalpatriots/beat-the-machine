/* A1 independent audit: author page and drill in a disposable headless Chrome profile.
   node a1-browser.cjs <game-root> <out.json>
   Test mode throughout; nothing is posted. Every participant string is synthetic. */
const fs = require("fs");
const { serve, launch, sleep, OVERFLOW } = require("./cdp.cjs");
const [ROOT, OUT] = process.argv.slice(2);
const TWO = "6100\tRent expense\t100000\t130000\n6200\tInsurance expense\t50000\t95000";
const MEMO = "1. Rent expense did not increase by $30,000.\n2. The bank covenant ratio was 7.2%.";
const H = `window.__set=function(id,v){var e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));return true;};
window.__gate=function(){return {save:document.getElementById('save').disabled, preview:document.getElementById('preview').disabled,
  stale:document.getElementById('stale').textContent.trim().slice(0,120), savegate:document.getElementById('savegate').textContent.trim().slice(0,160),
  staleFlag:__SPA.stale(), problems:__SPA.problems()};};true`;

(async () => {
  const { srv, port } = await serve(ROOT);
  const B = await launch("a1");
  const base = `http://127.0.0.1:${port}/`;
  const out = { root: ROOT, author: {}, drill: {} };
  const ev = B.ev, A = out.author;
  const key = async (k, code, vk, mods, commands) => {
    await B.send("Input.dispatchKeyEvent", { type: "keyDown", key: k, code, windowsVirtualKeyCode: vk, modifiers: mods || 0, commands: commands || [] });
    await B.send("Input.dispatchKeyEvent", { type: "keyUp", key: k, code, windowsVirtualKeyCode: vk, modifiers: mods || 0 });
  };
  try {
    await B.width(1280);
    const ready = "!!(window.__SPA&&window.SecondPassCore)";
    await B.nav(base + "author.html", ready);
    await ev("localStorage.clear();sessionStorage.clear();true");
    await B.nav(base + "author.html", ready);
    await ev(H);
    // ---- 1. the review's case, read
    await ev(`__set('cname','A1 audit case');__set('cver','v1');__set('ccolA','May');__set('ccolB','June');__set('ledger',${JSON.stringify(TWO)});__set('memo',${JSON.stringify(MEMO)});true`);
    await ev("document.getElementById('read').click();true"); await sleep(250);
    A.read = await ev(`({sentences:__SPA.sentences(), facts:Array.prototype.map.call(document.querySelectorAll('#facts li'),function(e){return e.textContent.trim();}),
      cards:__SPA.cards().map(function(c){return {acct:c.acct,status:c.status||null,key:c.key,type:c.type,basis:(c.basis||[]).slice()};}),
      items:__SPA.items().map(function(i){return {label:i.label,res:i.res,status:i.status||i.st||null};})})`);
    // ---- 2. settle everything the save asks for, so the only thing left is staleness
    await ev(`document.querySelector('#originseg button[data-v="synthetic"]').click();
      Array.prototype.forEach.call(document.querySelectorAll('#cards .kcard'),function(k){
        var t=k.querySelector('textarea[id$="-tell"]'); if(t){t.value='A1 audit: synthetic tell.';t.dispatchEvent(new Event('input',{bubbles:true}));}
        var st=k.querySelector('[id$="-call"] [aria-pressed="true"]');
        if(!st){ k.querySelector('[id$="-call"] button[data-v="flag"]').click(); var s=k.querySelector('select'); if(s){s.value=s.options[1].value; s.dispatchEvent(new Event('change',{bubbles:true}));}
          var ch=[].slice.call(k.querySelectorAll('.chip')).filter(function(x){return !/figure and reason hold/.test(x.textContent);})[0]; if(ch) ch.click(); var w=k.querySelector('textarea[id$="-why"]'); if(w){w.value='A1 audit: synthetic why.'; w.dispatchEvent(new Event('input',{bubbles:true}));} }
      });
      Array.prototype.forEach.call(document.querySelectorAll('#items .kcard'),function(k){
        k.querySelector('button[data-v="exclude"]').click(); var r=k.querySelector('textarea'); r.value='A1 audit: not on this ledger.'; r.dispatchEvent(new Event('input',{bubbles:true}));
      });true`);
    A.settled = await ev("__gate()");
    // ---- 3. stale-save paths. Each: change, gate, call save directly, count downloads, revert, gate.
    const trySave = async () => { B.clearDownloads(); await ev("__SPA.save();true"); await sleep(400); return B.downloadsNow(); };
    const selectIn = (id, needle) => ev(`(function(){var e=document.getElementById('${id}');e.focus();var i=e.value.indexOf(${JSON.stringify(needle)});e.setSelectionRange(i,i+${needle.length});return i;})()`);
    A.paths = {};
    // a. typing, real key input through CDP
    await selectIn("ledger", "130000");
    await B.send("Input.insertText", { text: "230000" }); await sleep(100);
    A.paths.typing = { value: await ev("document.getElementById('ledger').value.split('\\n')[0]"), gate: await ev("__gate()"), downloads: await trySave() };
    // b. undo with Ctrl+Z, then redo with Ctrl+Y
    await ev("document.getElementById('ledger').focus();true");
    await key("z", "KeyZ", 90, 2, ["undo"]); await sleep(150);
    A.paths.undo = { value: await ev("document.getElementById('ledger').value.split('\\n')[0]"), gate: await ev("__gate()") };
    await key("y", "KeyY", 89, 2, ["redo"]); await sleep(150);
    A.paths.redo = { value: await ev("document.getElementById('ledger').value.split('\\n')[0]"), gate: await ev("__gate()"), downloads: await trySave() };
    await ev(`__set('ledger',${JSON.stringify(TWO)});true`);
    A.paths.revertedByHand = { gate: await ev("__gate()") };
    // c. paste-shaped insert (execCommand insertText, the path a paste takes into a textarea)
    await selectIn("memo", "7.2%");
    await ev("document.execCommand('insertText',false,'9.9%');true"); await sleep(100);
    A.paths.pasteInsert = { value: await ev("document.getElementById('memo').value"), gate: await ev("__gate()"), downloads: await trySave() };
    await ev(`__set('memo',${JSON.stringify(MEMO)});true`);
    // d. policy: the rule control, then the dollar floor typed
    await ev("document.querySelector('#ruleseg button[data-v=\"either\"]').click();true"); await sleep(80);
    A.paths.ruleChange = { gate: await ev("__gate()"), downloads: await trySave() };
    await ev("document.querySelector('#ruleseg button[data-v=\"both\"]').click();true"); await sleep(80);
    await ev("document.getElementById('dollar').focus();true"); await key("a", "KeyA", 65, 2, ["selectAll"]); await B.send("Input.insertText", { text: "5000" }); await sleep(80);
    A.paths.dollarFloorTyped = { gate: await ev("__gate()"), downloads: await trySave() };
    await ev("__set('dollar','25000');true");
    // e. a value set with no event at all (not a user path): does the save itself still refuse?
    await ev(`document.getElementById('ledger').value=${JSON.stringify(TWO.replace("130000", "230000"))};true`);
    A.paths.silentValueChange = { gate: await ev("({save:document.getElementById('save').disabled, problems:__SPA.problems()})"), downloads: await trySave() };
    await ev(`__set('ledger',${JSON.stringify(TWO)});true`);
    A.paths.columnMapping = "author.html carries no column-mapping control (no colprior/colcur elements); the reader's own guess is the only mapping";
    A.paths.finalCleanSave = { gate: await ev("__gate()"), downloads: await trySave() };
    const dl = B.downloadsNow();
    if (dl.length) A.paths.finalCleanSaveFile = JSON.parse(fs.readFileSync(require("path").join(B.downloads, dl[0]), "utf8")).case.source.ledgerText;
    // ---- 4. the author page on A1 false-clearance memos: does a clean suggestion follow?
    await ev(`__set('memo',${JSON.stringify("1. Rent expense rose 30,000 euros.\n2. Insurance expense changed by $-45,000.\n3. Rent expense was stable at $130,000.\n4. Insurance expense rose $45,000, or 90 percent, year over year.")});true`);
    await ev("document.getElementById('read').click();true"); await sleep(250);
    A.falseClearanceMemo = await ev(`({sentences:__SPA.sentences(), facts:Array.prototype.map.call(document.querySelectorAll('#facts li'),function(e){return e.textContent.trim();}),
      cards:__SPA.cards().map(function(c){return {acct:c.acct,memo:c.memo,status:c.status||null,key:c.key,type:c.type,basis:(c.basis||[]).slice()};})})`);
    // ---- 5. accessibility: labels on every field, live regions for the messages
    A.a11y = await ev(`(function(){var bad=[];Array.prototype.forEach.call(document.querySelectorAll('textarea,input,select'),function(e){
        if(e.type==='hidden')return; var l=(e.id&&document.querySelector('label[for="'+e.id+'"]'))||e.closest('label')||e.getAttribute('aria-label')||e.getAttribute('aria-labelledby');
        if(!l) bad.push((e.id||e.tagName)+' '+(e.placeholder||''));});
      var roles={}; ['msg','stale','savegate','saybox'].forEach(function(id){var e=document.getElementById(id); roles[id]=e?{role:e.getAttribute('role'),live:e.getAttribute('aria-live')}:null;});
      return {unlabeled:bad, roles:roles};})()`);
    // ---- 6. 320 width with a long unbroken token in the memo
    await B.width(320);
    await ev(`__set('memo',${JSON.stringify("1. Rent expense rose $30,000 per https://example.invalid/" + "a".repeat(180) + "\n2. Insurance expense rose $45,000.")});true`);
    await ev("document.getElementById('read').click();true"); await sleep(300);
    A.overflow320LongToken = await ev(OVERFLOW);
    await B.width(1280);
    // ---- 7. provenance: load the sample, then replace both panes with other figures
    await ev("localStorage.clear();true");
    await B.nav(base + "author.html", ready); await ev(H);
    const before = await ev("document.querySelector('#originseg [aria-pressed=\"true\"]')?document.querySelector('#originseg [aria-pressed=\"true\"]').getAttribute('data-v'):null");
    await ev("document.getElementById('loadsample').click();true"); await sleep(100);
    await ev(`__set('ledger',${JSON.stringify(TWO)});__set('memo',"1. Rent expense rose $30,000.\\n2. Insurance expense rose $45,000.");true`);
    A.sampleThenReplace = { originBeforeSample: before, originAfterReplacingBothPanes: await ev("document.querySelector('#originseg [aria-pressed=\"true\"]').getAttribute('data-v')") };

    // ================= the drill
    const D = out.drill;
    const dready = "!!(window.__BTM_CASES&&document.getElementById('go'))";
    await B.nav(base + "index.html?test=1&case=halyard", dready);
    await ev("sessionStorage.clear();localStorage.removeItem('btm.owncase.v1');true");
    await B.nav(base + "index.html?test=1&case=halyard", dready);
    await ev("document.getElementById('go').click();true"); await sleep(100);
    await ev("document.getElementById('noticego').click();true"); await sleep(100);
    await ev("var i=document.getElementById('cn');i.value='A1 Audit Walk';i.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#orgs .chip').click();document.getElementById('next').click();true");
    await sleep(150);
    await ev("(function(){var b=document.querySelector('[data-go3]');if(b)b.click();return true;})()"); await sleep(150);
    const st = await ev("__BTM_STEPS()");
    let guard = 0, probed = false;
    D.lock = [];
    while (guard++ < 400) {
      const s = await ev("__BTM.step");
      if (s === 92) { await ev("document.getElementById('r2done').click();true"); await sleep(80); continue; }
      if (s >= st.done) break;
      if (s === st.bridge) { await ev("document.getElementById('r2go').click();true"); await sleep(80); continue; }
      if (await ev("!!document.getElementById('next')")) { await ev("document.getElementById('next').click();true"); await sleep(60); continue; }
      const round = s >= st.l2 ? 2 : 1, i = round === 2 ? s - st.l2 : s - 3;
      const r = await ev(`(function(){var c=${round}===2?__BTM_CARDS2[${i}]:__BTM_CARDS[${i}];var b=document.getElementById(c.key);if(!b)return {err:1};b.click();return {key:c.key,basis:(c.basisKey||[])[0]};})()`);
      if (r.err) { D.failure = "no call button at step " + s; break; }
      await sleep(60);
      await ev(`(function(){var chips=[].slice.call(document.querySelectorAll('#commit .chip'));var h=chips.filter(function(x){return x.textContent.trim()===${JSON.stringify(r.basis)};})[0]||chips[0];if(h)h.click();return true;})()`);
      const boxes = await ev("document.querySelectorAll('#screen textarea.explain').length");
      const lockState = () => ev("(function(){var l=document.getElementById('lockin');return {disabled:l?l.disabled:null, calls:JSON.stringify(__BTM.r2calls||null)};})()");
      const fill = (vals) => ev(`(function(){var v=${JSON.stringify(vals)};[].forEach.call(document.querySelectorAll('#screen textarea.explain'),function(t,k){t.value=v[k];t.dispatchEvent(new Event('input',{bubbles:true}));});return true;})()`);
      if (boxes && !probed) {
        probed = true;
        const rec = { item: i + 1 };
        rec.empty = await lockState();
        // keyboard: Enter with focus on the body, then on the lock button itself
        await ev("document.activeElement&&document.activeElement.blur();true");
        await key("Enter", "Enter", 13); await sleep(120);
        rec.enterOnBodyWhileEmpty = { step: await ev("__BTM.step"), same: (await ev("__BTM.step")) === s };
        await ev("(function(){var l=document.getElementById('lockin');l.disabled=false;l.click();return true;})()"); await sleep(120);
        rec.forcedClickOnDisabledButton = { stepUnchanged: (await ev("__BTM.step")) === s };
        await fill(["   ", "\t\t", "\n\n"]); rec.whitespace = await lockState();
        await fill(["a b", "a b", "a b"]); rec.threeCharsWithSpace = await lockState();
        await fill(["...", "...", "..."]); rec.dots = await lockState();
        await fill(["none", "None.", "n/a"]); rec.noneWords = await lockState();
        await fill(["=HYPERLINK(\"http://example.invalid\",\"x\")", "+1+1", "@SUM(1,1)"]);
        // the label, focus order and any announcement tied to the boxes
        rec.a11y = await ev(`(function(){var t=[].slice.call(document.querySelectorAll('#screen textarea.explain'));
          return t.map(function(x){var l=document.querySelector('label[for="'+x.id+'"]');return {id:x.id,label:l?l.textContent:null,describedby:x.getAttribute('aria-describedby'),required:x.required||x.getAttribute('aria-required')};})
            .concat([{lockDescribedby:document.getElementById('lockin').getAttribute('aria-describedby'), liveRegions:document.querySelectorAll('#screen [aria-live],#screen [role=alert],#screen [role=status]').length}]);})()`);
        // reload before locking: does the typed explanation survive?
        await B.nav(base + "index.html?test=1&case=halyard", "!!window.__BTM");
        await sleep(300);
        rec.afterReload = await ev("({step:__BTM.step, boxes:[].map.call(document.querySelectorAll('#screen textarea.explain'),function(t){return t.value;}), stored:(function(){try{var s=JSON.parse(sessionStorage.getItem(Object.keys(sessionStorage).filter(function(k){return /btm|run/i.test(k);})[0]));return s&&s.r2explain?s.r2explain["+i+"]:null;}catch(e){return String(e);}})()})");
        D.lock.push(rec);
        if (rec.afterReload.step !== s) { D.reloadNote = "the reload did not return to the same item; the walk continues from step " + rec.afterReload.step; }
        continue;
      }
      if (boxes) await fill(["The invoice is on file.", "It is dated June.", "Ask for the June schedule."]);
      await ev("(function(){var l=document.getElementById('lockin');if(l)l.click();return true;})()"); await sleep(80);
    }
    D.endStep = await ev("__BTM.step");
    await ev("(function(){var b=document.getElementById('sendres');if(b)b.click();return true;})()"); await sleep(300);
    D.qc = await ev("(function(){var p=window.__BTM_LAST_POST||{};return p['entry.756559246']||null;})()");
    D.record = await ev("(function(){var r=__BTM_RECORD(null);return r.responses.filter(function(x){return x.round===2;}).map(function(x){return {item:x.item,v:x.caseVersion,req:x.writtenExplanationRequired,ex:x.writtenExplanation};});})()");
    out.errors = B.errors;
  } catch (e) { out.failure = e.message; out.errors = B.errors; }
  finally { B.close(); srv.close(); }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out, null, 1).slice(0, 9000));
})();
