/* Author statuses against the checker's own run, the permitted-origin path, and widths.
   node parity-widths.cjs <root> <out.json> */
const fs = require("fs");
const { serve, launch, sleep, OVERFLOW } = require("./cdp.cjs");
const ROOT = process.argv[2], OUT = process.argv[3];

const RENT = "6100\tRent expense\t100000\t130000";
const RENT2 = RENT + "\n6200\tInsurance expense\t50000\t95000";
const PROBES = [
  { id: "review", ledger: RENT2, memo: "1. Rent expense did not increase by $30,000.\n2. The bank covenant ratio was 7.2%." },
  { id: "P05", ledger: RENT, memo: "1. Rent expense increased by $30,000 and doubled." },
  { id: "P13", ledger: RENT, memo: "1. Rent expense remained at $130,000." },
  { id: "P23", ledger: RENT, memo: "1. Rent expense rose $30,000, or one and a half percent." },
  { id: "P25", ledger: RENT, memo: "1. Rent expense rose $30,000 and increased by ٣٠٠٠٠." },
  { id: "P30", ledger: RENT, memo: "1. Rent expense increased by $30,000 from $100,000 to $130,000." },
  { id: "P31", ledger: RENT, memo: "1. Rent expense declined by $30,000 from $100,000 to $130,000." },
  { id: "wrong figure", ledger: RENT2, memo: "1. Rent expense rose $35,000 to $130,000.\n2. Insurance expense rose $45,000, or 90 percent." },
  { id: "two accounts", ledger: RENT2, memo: "1. Rent expense and insurance expense rose $30,000 and $45,000." },
  { id: "policy claim", ledger: RENT2 + "\n6300\tPostage\t1000\t1200", memo: "1. Postage rose $200, which fails the dollar leg of the threshold, so this line carries no driver." },
  { id: "kestrel sample", ledger: null, memo: null },
];

(async () => {
  const { srv, port } = await serve(ROOT);
  const B = await launch("parity");
  const base = `http://127.0.0.1:${port}/`;
  const out = { parity: [], origin: {}, widths: [] };
  const H = `window.__set=function(id,v){var e=document.getElementById(id);e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));return true;};true`;
  try {
    await B.width(1280);
    for (const p of PROBES) {
      await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
      await B.ev(H);
      if (p.ledger === null) { await B.ev("document.getElementById('loadsample').click();true"); }
      else await B.ev(`__set('ledger',${JSON.stringify(p.ledger)});__set('memo',${JSON.stringify(p.memo)});true`);
      const led = await B.ev("document.getElementById('ledger').value"), memo = await B.ev("document.getElementById('memo').value");
      await B.ev("document.getElementById('read').click();true");
      await sleep(150);
      const a = await B.ev(`({sents:__SPA.sentences(), facts:Array.prototype.map.call(document.querySelectorAll('#facts li'),function(l){return l.textContent;}),
        cards:__SPA.cards().map(function(c){return {acct:c.acct,status:c.status,key:c.key,sug:c.sug.call};}),
        items:__SPA.items().map(function(i){return {label:i.label,status:i.status};})})`);
      await B.nav(base + "checker.html", "!!(window.__secondPass&&document.getElementById('run'))");
      await B.ev(H);
      await B.ev(`__set('ledger',${JSON.stringify(led)});__set('memo',${JSON.stringify(memo)});document.getElementById('run').click();true`);
      await sleep(200);
      const c = await B.ev("(function(){var L=window.__secondPass();return L?L.sents.map(function(s){return {label:s.label,status:s.st};}):null;})()");
      const match = !!c && c.length === a.sents.length && c.every((s, i) => s.status === a.sents[i].status && s.label === a.sents[i].label);
      const praise = a.facts.filter((f) => /^Every (figure|direction)/.test(f));
      const allChecked = a.sents.length && a.sents.every((s) => s.status === "checked within scope");
      const standOnUnsettled = a.cards.filter((k) => k.status !== "checked within scope" && k.sug === "stand").length;
      out.parity.push({ id: p.id, match, author: a.sents.map((s) => s.label + " " + s.status), checker: c && c.map((s) => s.label + " " + s.status),
        praise, praiseOnlyWhenAllChecked: !praise.length || !!allChecked, standSuggestedOnUnsettled: standOnUnsettled,
        cards: a.cards, items: a.items });
    }

    /* a permitted real case: refused without the permission line, saved with it, and the drill says so */
    await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
    await B.ev("localStorage.clear();true");
    await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
    await B.ev(H);
    await B.ev(`__set('cname','Permitted origin test');__set('cver','v1');__set('ledger',${JSON.stringify(RENT2)});
      __set('memo','1. Rent expense rose $30,000 to $130,000.\\n2. Insurance expense rose $45,000 to $95,000.');
      document.getElementById('read').click();
      Array.prototype.forEach.call(document.querySelectorAll('#cards textarea[id$="-tell"]'),function(t){t.value='Origin test.';t.dispatchEvent(new Event('input',{bubbles:true}));});
      document.querySelector('#originseg [data-v="permitted"]').click();true`);
    out.origin.permissionFieldShown = await B.ev("!document.getElementById('permf').hidden");
    out.origin.problemsWithoutPermission = await B.ev("__SPA.problems()");
    await B.ev("__set('cperm','The controller, for classroom use with names removed');true");
    out.origin.problemsWithPermission = await B.ev("__SPA.problems()");
    await B.ev("document.getElementById('save').click();true");
    await sleep(700);
    out.origin.stored = await B.ev("(function(){var j=JSON.parse(localStorage.getItem('btm.owncase.v1')||'null');return j&&{origin:j.origin,caseOrigin:j.case.origin,sourceVersion:j.sourceVersion,cards:j.case.cards.map(function(c){return c.key+' '+c.current;})};})()");
    await B.nav(base + "index.html?case=own&test=1", "!!(window.__BTM_CASES&&document.getElementById('go'))");
    out.origin.intro = await B.ev("Array.prototype.map.call(document.querySelectorAll('#screen p'),function(p){return p.textContent.replace(/\\s+/g,' ').trim();})[1]");
    await B.nav(base + "index.html?test=1", "!!(window.__BTM_CASES&&document.getElementById('go'))");
    out.origin.halyardIntro = await B.ev("Array.prototype.map.call(document.querySelectorAll('#screen p'),function(p){return p.textContent.replace(/\\s+/g,' ').trim();})[1]");

    /* widths: the author page with every new element open, and the drill intro on the own case */
    for (const w of [320, 375, 768, 1280]) {
      await B.width(w);
      await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
      await B.ev(H);
      await B.ev(`__set('cname','Width test');__set('ledger',${JSON.stringify(RENT2)});
        __set('memo','1. Rent expense did not increase by $30,000.\\n2. The bank covenant ratio was 7.2%.');
        document.getElementById('read').click();
        document.querySelector('#originseg [data-v="permitted"]').click();
        Array.prototype.forEach.call(document.querySelectorAll('#items [data-v="exclude"]'),function(b){b.click();});
        document.getElementById('freshblock').open=true;
        Array.prototype.forEach.call(document.querySelectorAll('#cards textarea[id$="-tell"]'),function(t){t.value='x';t.dispatchEvent(new Event('input',{bubbles:true}));});
        __set('ledger',document.getElementById('ledger').value.replace('130000','230000'));
        document.getElementById('read').click();
        __set('memo',document.getElementById('memo').value+' ');
        document.getElementById('save').disabled;`);
      await sleep(250);
      const author = await B.ev(OVERFLOW);
      const vis = await B.ev(`({recon:!!document.querySelector('.recon:not([hidden])'), stale:!!document.querySelector('#stale .status'),
        gate:!!document.querySelector('#savegate .status'), reason:!!document.querySelector('#items [id$="-rf"]:not([hidden])'), perm:!document.getElementById('permf').hidden})`);
      if (w === 320) await B.shot(OUT.replace(/\.json$/, "-author-320.png"));
      await B.nav(base + "index.html?case=own&test=1", "!!(window.__BTM_CASES&&document.getElementById('go'))");
      await sleep(200);
      const drill = await B.ev(OVERFLOW);
      out.widths.push({ width: w, author, authorShowing: vis, drillIntro: drill });
    }
    out.errors = B.errors;
  } catch (e) {
    out.failure = e.message; out.errors = B.errors;
  } finally { B.close(); srv.close(); }
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2));
  console.log(JSON.stringify({ failure: out.failure, errors: out.errors,
    parity: out.parity.map((p) => [p.id, p.match, p.author.join(" | "), p.checker && p.checker.join(" | "), p.praise.join(" / "), p.praiseOnlyWhenAllChecked, p.standSuggestedOnUnsettled]),
    origin: out.origin, widths: out.widths }, null, 1));
})();
