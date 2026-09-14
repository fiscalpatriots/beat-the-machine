/* The third review's author reproduction, README steps 1 to 8, run against one tree.
   node review-steps.cjs <root> <label> <out.json> */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep } = require("./cdp.cjs");
const ROOT = process.argv[2], LABEL = process.argv[3] || "run", OUT = process.argv[4];

const LEDGER = "6100\tRent expense\t100000\t130000\n6200\tInsurance expense\t50000\t95000";
const MEMO = "1. Rent expense did not increase by $30,000.\n2. The bank covenant ratio was 7.2%.";
const H = `
window.__set=function(id,v){var e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));return true;};
window.__click=function(sel){var e=document.querySelector(sel);if(!e)return 'missing '+sel;e.click();return true;};
window.__txt=function(sel){return Array.prototype.map.call(document.querySelectorAll(sel),function(e){return e.textContent.replace(/\\s+/g,' ').trim();});};
true`;

(async () => {
  const { srv, port } = await serve(ROOT);
  const B = await launch(LABEL);
  const base = `http://127.0.0.1:${port}/`;
  const out = { label: LABEL, root: ROOT, steps: {} };
  try {
    await B.width(1280);
    await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
    await B.ev("localStorage.clear();sessionStorage.clear();true");
    await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
    await B.ev(H);
    /* 1 to 3 */
    await B.ev(`__set('cname','Excluded review test');__set('cver','v1');__set('ccolA','May');__set('ccolB','June');
      __set('ledger',${JSON.stringify(LEDGER)});__set('memo',${JSON.stringify(MEMO)});true`);
    out.promise = await B.ev("document.querySelector('.band .promise').textContent.replace(/\\s+/g,' ').trim()");
    out.memoHint = await B.ev("document.querySelectorAll('.pane .hint')[1].textContent.replace(/\\s+/g,' ').trim()");
    /* 4 */
    await B.ev("__click('#read')");
    await sleep(200);
    out.steps.read = await B.ev(`({
      msg: __txt('#msg')[0]||'',
      facts: __txt('#facts li'),
      cards: __SPA.cards().map(function(c){return {n:c.n,acct:c.acct,memo:c.memo,status:c.status||null,key:c.key,type:c.type,basis:c.basis.slice(),found:c.found.slice(),why:c.why};}),
      items: (__SPA.items?__SPA.items():null),
      cardHeads: __txt('#cards .kcard .khead'),
      itemHeads: __txt('#items .kcard .khead')
    })`);
    /* 5: the two tell fields, and in the repaired page whatever else the save now requires,
       so the only thing left between the case and a save is the stale input */
    const hasItems = await B.ev("!!document.getElementById('items')");
    await B.ev(`Array.prototype.forEach.call(document.querySelectorAll('#cards textarea[id$="-tell"]'),function(t){
        t.value='Excluded audit test. This intentionally retains the suggested key.';t.dispatchEvent(new Event('input',{bubbles:true}));});true`);
    if (hasItems) {
      await B.ev(`__click('#originseg button[data-v="synthetic"]');
        Array.prototype.forEach.call(document.querySelectorAll('#cards .kcard'),function(k){
          var c=k.querySelector('[id$="-call"] button[data-v="flag"]');
          var st=k.querySelector('[id$="-call"] [aria-pressed="true"]');
          if(!st){ c.click(); var s=k.querySelector('select'); s.value='wrong direction'; s.dispatchEvent(new Event('change',{bubbles:true}));
            k.querySelector('.chip[data-b="2"]').click();
            var w=k.querySelector('textarea[id$="-why"]'); w.value='The sentence denies a movement the ledger shows.'; w.dispatchEvent(new Event('input',{bubbles:true})); }
        });
        Array.prototype.forEach.call(document.querySelectorAll('#items .kcard'),function(k){
          k.querySelector('button[data-v="exclude"]').click();
          var r=k.querySelector('textarea'); r.value='The covenant ratio is not on this ledger, so the drill leaves it out.'; r.dispatchEvent(new Event('input',{bubbles:true}));
        });true`);
      out.steps.problemsBeforeEdit = await B.ev("__SPA.problems()");
    }
    /* 6 */
    const before = await B.ev("document.getElementById('ledger').value");
    await B.ev(`__set('ledger',document.getElementById('ledger').value.replace('130000','230000'))`);
    out.steps.edit = await B.ev(`({ledgerChanged:${JSON.stringify(before)}!==document.getElementById('ledger').value,
      saveDisabled:document.getElementById('save').disabled, previewDisabled:document.getElementById('preview').disabled,
      notice:(__txt('#stale')[0]||__txt('#savegate')[0]||'')})`);
    /* 7: a real click, then the page's own save function called directly */
    B.clearDownloads();
    await B.ev("__click('#save')");
    await sleep(900);
    out.steps.saveClick = { downloads: B.downloadsNow(), saybox: await B.ev("__txt('#saybox')[0]||''") };
    if (!out.steps.saveClick.downloads.length) {
      await B.ev("__SPA.save();true");
      await sleep(900);
      out.steps.saveDirect = { downloads: B.downloadsNow(), saybox: await B.ev("__txt('#saybox')[0]||''") };
    }
    const got = B.downloadsNow();
    if (got.length) {
      const j = JSON.parse(fs.readFileSync(path.join(B.downloads, got[0]), "utf8"));
      out.steps.savedFile = { name: got[0], ledger: j.case.ledger, rentCard: j.case.cards[0],
        cards: j.case.cards.length, source: j.case.source || null, origin: j.origin || null };
    }
    /* repaired page only: read again, reconcile, save, and prove the file matches the screen */
    if (hasItems) {
      await B.ev("__click('#read')"); await sleep(200);
      out.steps.reread = await B.ev(`({msg:__txt('#msg')[0]||'', problems:__SPA.problems(),
        saveDisabled:document.getElementById('save').disabled,
        cards:__SPA.cards().map(function(c){return {acct:c.acct,current:c.current,status:c.status,key:c.key,reconcile:c.reconcile,confirmed:c.confirmed};})})`);
      await B.ev(`Array.prototype.forEach.call(document.querySelectorAll('#cards button[id$="-confirm"]'),function(b){b.click();});true`);
      out.steps.afterConfirm = await B.ev("__SPA.problems()");
      B.clearDownloads();
      await B.ev("__click('#save')"); await sleep(900);
      const f2 = B.downloadsNow();
      if (f2.length) {
        const j = JSON.parse(fs.readFileSync(path.join(B.downloads, f2[0]), "utf8"));
        const sigNow = await B.ev("__SPA.version()");
        out.steps.resaved = { ledger: j.case.ledger, sourceVersion: j.case.source.version, pageVersionNow: sigNow,
          sourceLedger: j.case.source.ledger, sentences: j.case.source.sentences, origin: j.origin, caseOrigin: j.case.origin,
          saybox: await B.ev("__txt('#saybox')[0]||''") };
      }
    }
    /* 8 */
    await B.nav(base + "index.html?case=own&test=1", "!!(window.__BTM_CASES&&document.getElementById('go'))");
    out.steps.drill = await B.ev(`({pick:__BTM_CASES.pick, source:__BTM_CASES.source,
      intro:Array.prototype.map.call(document.querySelectorAll('#screen p'),function(p){return p.textContent.replace(/\\s+/g,' ').trim();}).slice(0,3)})`);
    /* a permitted real case, repaired page only */
    if (hasItems) {
      await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
      await B.ev(H);
      out.steps.reopenedAuthor = await B.ev("__txt('#saybox')[0]||''");
    }
    /* 9 */
    await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
    await B.ev(H);
    await B.ev("document.getElementById('forget').hidden?false:(__click('#forget'),true)");
    out.steps.forget = await B.ev("({stored:localStorage.getItem(__SPA.key)})");
    out.errors = B.errors;
  } catch (e) {
    out.failure = e.message;
    out.errors = B.errors;
  } finally {
    B.close(); srv.close();
  }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2).slice(0, 6000));
})();
