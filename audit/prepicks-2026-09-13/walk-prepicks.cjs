/* The required read before the draft, walked end to end in headless Chrome on one case.
   node walk-prepicks.cjs <root> <case> <outdir>
   <case> is halyard, kestrel, or own. "own" seeds this browser's saved case the way author.html
   saves one, from a copy of kestrel-v1 renamed walk-own-1 with no fresh set, and walks that.

   Test mode the whole way, so nothing is posted. It proves, by running the page:
   1. the read cannot be skipped by a click, a key, the step hook, an edited saved run or the address;
   2. tapping is keyboard reachable and survives a reload, and the read locks once the player goes on;
   3. the end screen states where the final calls moved off the read, and the counts are right;
   4. the form payload and the record carry the read per line with the case version;
   5. Play again starts with no read, and the second run reports its own read, never the first;
   6. no horizontal overflow on the read screen or the end screen at 320, 375, 768 and 1280.
   Writes <outdir>/<case>-walk.json, <outdir>/<case>-payload-run1.json and -run2.json. The screenshots to
   look at are the viewport captures shots-prepicks.cjs writes. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../author-repair-2026-09-13/cdp.cjs");
const [ROOT, CASE, OUTDIR] = [process.argv[2], process.argv[3] || "halyard", process.argv[4] || __dirname];

const NUMWORDS = ["zero","one","two","three","four","five","six","seven","eight","nine","ten","eleven",
  "twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty"];
const word = (n) => NUMWORDS[n] || String(n);
const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
/* the end screen's paragraph, from the counts, written out independently of the page */
function leadText(nPicks, e, lines) {
  const changed = e.toward + e.away;
  let t = "Before the memo you tapped " + word(nPicks) + " account" + (nPicks === 1 ? "" : "s") + " on the ledger for a second look. ";
  if (!changed) return t + "After reading the AI draft, all " + word(lines) + " of your final calls matched that read.";
  t += "After reading the AI draft, your final call moved off that read on " + word(changed) + " of the " + word(lines) + " lines. ";
  if (e.toward && e.away) t += cap(word(e.toward)) + " of those changes moved toward the answer key and " + word(e.away) + " moved away from it. ";
  else t += (changed === 1 ? "That change moved " : "Every one of those changes moved ") + (e.toward ? "toward the answer key. " : "away from the answer key. ");
  if (e.held) t += (e.held === 1 ? "On the one other line, " : "On the other " + word(e.held) + " lines, ") + "your final call matched your first read.";
  return t.trim();
}

/* the page's rule, restated here so the test does not read the answer off the page */
function expected(cards, picks, calls, version) {
  const read = cards.map((c) => (picks.includes(String(c.acct)) ? "flag" : "stand"));
  const moves = read.map((r, i) => (calls[i] === r ? "held" : (calls[i] === cards[i].key ? "toward" : "away")));
  const L = (list) => list.map((v) => (v === "flag" ? "F" : "S")).join("");
  const toward = moves.filter((m) => m === "toward").length;
  const away = moves.filter((m) => m === "away").length;
  const held = moves.filter((m) => m === "held").length;
  const cell = "Prepicks: " + picks.join("; ") + ". Required read before the AI draft, case " + version +
    ", by line, F tapped for a second look and S left untapped: " + L(read) + ". Final calls after the draft: " +
    L(calls) + ". Against the key: " + toward + " changed toward it, " + away + " changed away from it, " + held + " held.";
  return { read, moves, toward, away, held, cell, readLetters: L(read), finalLetters: L(calls) };
}

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const { srv, port } = await serve(ROOT);
  const B = await launch("prepick-" + CASE);
  const ev = B.ev;
  const base = `http://127.0.0.1:${port}/`;
  const url = base + "index.html?test=1&case=" + CASE;
  const READY = "!!(window.__BTM_CASES&&window.__BTM&&document.getElementById('screen')&&document.getElementById('screen').children.length)";
  const out = { case: CASE, ran: new Date().toString(), checks: [], widths: [], errors: [] };
  const check = (name, pass, detail) => {
    out.checks.push({ name, pass: !!pass, detail: detail === undefined ? null : detail });
    if (!pass) console.log("FAIL " + CASE + ": " + name + " " + JSON.stringify(detail));
  };
  const press = async (k) => {
    const map = { Enter: [13, "\r", "Enter"], Space: [32, " ", " "], Tab: [9, "", "Tab"] };
    const [vk, text, keyName] = map[k];
    await B.send("Input.dispatchKeyEvent", { type: "keyDown", key: keyName, code: k === "Space" ? "Space" : k,
      windowsVirtualKeyCode: vk, nativeVirtualKeyCode: vk, text: text || undefined });
    await B.send("Input.dispatchKeyEvent", { type: "keyUp", key: keyName, code: k === "Space" ? "Space" : k,
      windowsVirtualKeyCode: vk, nativeVirtualKeyCode: vk });
    await sleep(60);
  };
  const step = () => ev("__BTM.step");
  const VISIBLE_GO = `(function(){return Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){
      var r=b.getBoundingClientRect(),cs=getComputedStyle(b);return r.width>0&&r.height>0&&cs.visibility!=='hidden';
    }).map(function(b){return {where:b.closest('.stickygo')?'sticky bar':(b.closest('.prepickgo')?'under the lines':(b.closest('.orientside')?'rail':'other')),text:b.textContent.trim(),
      tag:b.tagName,type:b.getAttribute('type'),disabled:b.disabled};});})()`;
  const MEMO_SHOWN = `(function(){var t=document.getElementById('screen').innerText;
      return !!document.querySelector('#screen .quote') || __BTM_CARDS.some(function(c){return c.memo && t.indexOf(c.memo.slice(0,48))>-1;});})()`;
  const clickGo = (where) => ev(`(function(){var b=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){
      var r=b.getBoundingClientRect();return r.width>0&&r.height>0;})[0];if(!b) return false;b.click();return true;})()`);
  const audit = async (tag) => { const o = await ev(OVERFLOW); out.widths.push({ tag, ...o }); return o; };

  async function toReadScreen(fresh) {
    if (fresh) {
      await B.nav(url, READY);
      await ev("sessionStorage.clear();localStorage.removeItem('btm.owncase.v1');true");
      if (CASE === "own") await seedOwn();
      await B.nav(url, READY);
    }
    await ev("document.getElementById('go').click();true"); await sleep(120);
    await ev("document.getElementById('noticego').click();true"); await sleep(120);
    await ev("var i=document.getElementById('cn');i.value='Prepick Walk';i.dispatchEvent(new Event('input',{bubbles:true}));" +
      "if(!document.querySelector('#orgs .chip.on')) document.querySelector('#orgs .chip').click();document.getElementById('next').click();true");
    await sleep(200);
  }

  /* one full run, the calls chosen by callFor(round, index, card) */
  async function playRun(callFor) {
    const st = await ev("__BTM_STEPS()");
    let guard = 0;
    while (guard++ < 400) {
      const s = await step();
      if (s === 92) { await ev("document.getElementById('r2done').click();true"); await sleep(100); continue; }
      if (s >= st.done) break;
      if (s === st.bridge) { await ev("document.getElementById('r2go').click();true"); await sleep(100); continue; }
      if (await ev("!!document.getElementById('next')")) { await ev("document.getElementById('next').click();true"); await sleep(70); continue; }
      const round = s >= st.l2 ? 2 : 1, i = round === 2 ? s - st.l2 : s - 3;
      const card = await ev(`(${round}===2?__BTM_CARDS2:__BTM_CARDS)[${i}]`);
      const want = callFor(round, i, card);
      const r = await ev(`(function(){var b=document.getElementById(${JSON.stringify(want)});if(!b) return 'no call button at step ${s}';b.click();return 'ok';})()`);
      if (r !== "ok") throw new Error(r);
      await sleep(60);
      await ev(`(function(){var chips=Array.prototype.slice.call(document.querySelectorAll('#commit .chip'));
        var key=${JSON.stringify(card.basisKey || [])};
        var hit=chips.filter(function(x){return key.indexOf(x.textContent.trim())>-1;})[0]||chips[0];if(hit) hit.click();
        Array.prototype.forEach.call(document.querySelectorAll('#screen textarea.explain'),function(t,k){
          t.value=['The document on the card settles it.','It covers this month.','Ask for the schedule behind it.'][k];
          t.dispatchEvent(new Event('input',{bubbles:true}));});
        var l=document.getElementById('lockin');if(l) l.click();return true;})()`);
      await sleep(90);
    }
  }

  /* an authored case, saved where author.html saves one: kestrel-v1's lines under another name, no fresh set */
  async function seedOwn() {
    await ev(`(async function(){var c=await (await fetch('cases/kestrel-v1.json',{cache:'no-store'})).json();
      c.version='walk-own-1'; c.company='Walk Own Case LLC'; c.origin={kind:'synthetic'};
      localStorage.setItem('btm.owncase.v1', JSON.stringify({id:'own:WalkOwn:1', name:'WalkOwn', caseVersion:'1', 'case':c, fresh:null}));
      return true;})()`);
  }

  try {
    await B.width(375);
    const cases = await (async () => {
      await B.nav(url, READY);
      if (CASE === "own") { await seedOwn(); await B.nav(url, READY); }
      return ev("({one:__BTM_CASES.one,two:__BTM_CASES.two,lines:__BTM_CASES.lines,source:__BTM_CASES.source,id:__BTM_CASES.id})");
    })();
    out.cases = cases;
    if (CASE === "own") check("the authored case loaded from this browser, with no fresh set", cases.source === "this browser, written by author.html" && cases.one === "walk-own-1" && cases.two === null, cases);
    else check("case files loaded from cases/, not the inline fallback", cases.source === "cases/ files", cases);

    /* ---------- 1. no way past an empty read ---------- */
    await toReadScreen(true);
    const s2 = await ev(`({step:__BTM.step, section:!!document.getElementById('prepicksection'),
      chips:document.querySelectorAll('#prepicks .chip').length, rows:(function(){var n=0;try{n=__BTM_CASES.lines;}catch(e){}return n;})(),
      ledgerRows:document.querySelectorAll('#screen .stmt .srow:not(.sub):not(.net)').length,
      skipText:Array.prototype.filter.call(document.querySelectorAll('#screen button,#screen a,#screen [role=button]'),function(b){return /skip|later|not now|pass/i.test(b.textContent);}).map(function(b){return b.textContent;}),
      pageSkipLinks:Array.prototype.filter.call(document.querySelectorAll('a'),function(b){return /skip/i.test(b.textContent);}).map(function(b){return b.textContent+' -> '+b.getAttribute('href');}),
      focus:document.activeElement && document.activeElement.id,
      head:document.getElementById('prepickhead').textContent, whyline:document.querySelector('.whyline').textContent,
      stat:document.getElementById('prepickstat').textContent})`);
    out.readScreen = s2;
    check("the drill arrives on the read screen after the codename", s2.step === 2 && s2.section, s2);
    check("one chip per ledger account", s2.chips === s2.ledgerRows && s2.chips > 0, { chips: s2.chips, ledgerRows: s2.ledgerRows });
    check("no control on the drill screen offers a skip or a later (the header's skip-to-content link is the only skip on the page)", s2.skipText.length === 0 && s2.pageSkipLinks.every(function(x){return /main content/i.test(x);}), {screen:s2.skipText, page:s2.pageSkipLinks});
    check("focus lands on the screen heading", s2.focus === "orienthead", s2.focus);
    check("no memo sentence is on the read screen", !(await ev(MEMO_SHOWN)));
    const vis375 = await ev(VISIBLE_GO);
    check("exactly one onward button is visible at 375, in the sticky bar, and it is a labeled button", vis375.length === 1 && vis375[0].where === "sticky bar" && vis375[0].text.length > 0 && vis375[0].type === "button", vis375);

    await clickGo();
    await sleep(250);
    const afterEmpty = await ev("({step:__BTM.step, focus:document.activeElement&&document.activeElement.getAttribute('data-p'), stat:document.getElementById('prepickstat').textContent, memo:!!document.querySelector('#screen .quote')})");
    check("clicking on with nothing tapped stays on the read and moves focus to the first line", afterEmpty.step === 2 && afterEmpty.focus === "0" && !afterEmpty.memo, afterEmpty);

    await ev("(function(){var b=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){return b.getBoundingClientRect().width>0;})[0];b.focus();return true;})()");
    await press("Enter"); await sleep(150);
    const kEnter = await step();
    await ev("(function(){var b=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){return b.getBoundingClientRect().width>0;})[0];b.focus();return true;})()");
    await press("Space"); await sleep(150);
    const kSpace = await step();
    check("Enter and Space on the onward button with nothing tapped stay on the read", kEnter === 2 && kSpace === 2, { kEnter, kSpace });

    const st = await ev("__BTM_STEPS()");
    await ev("__BTM_GO(3);true"); await sleep(150);
    const hook3 = { step: await step(), memo: await ev(MEMO_SHOWN) };
    await ev(`__BTM_GO(${st.done});true`); await sleep(150);
    const hookDone = { step: await step(), memo: await ev(MEMO_SHOWN), trophy: await ev("!!document.querySelector('.trophywrap')") };
    await ev(`__BTM_GO(92);true`); await sleep(150);
    const hook92 = { step: await step(), memo: await ev(MEMO_SHOWN) };
    check("the step hook cannot open line one, the fresh results or the end screen without a read", hook3.step === 2 && !hook3.memo && hookDone.step === 2 && !hookDone.trophy && hook92.step === 2 && !hook92.memo, { hook3, hookDone, hook92 });

    /* an edited saved run: a finished round with every call made and no read */
    await ev(`(function(){var r=JSON.parse(sessionStorage.getItem('btm.run.v1'));r.step=${st.done};r.prepickAt=0;
      r.calls=__BTM_CARDS.map(function(c){return c.key;});r.r2calls=__BTM_CARDS2.map(function(c){return c.key;});
      sessionStorage.setItem('btm.run.v1',JSON.stringify(r));return true;})()`);
    await B.nav(url, READY); await sleep(200);
    const saved = { step: await step(), memo: await ev(MEMO_SHOWN), trophy: await ev("!!document.querySelector('.trophywrap')") };
    check("an edited saved run that jumps to the end comes back on the read screen", saved.step === 2 && !saved.memo && !saved.trophy, saved);

    /* a forged read naming an account that is not on this ledger */
    await ev(`(function(){var r=JSON.parse(sessionStorage.getItem('btm.run.v1'));r.step=5;r.prepicks=['99999'];r.prepickAt=Date.now();
      r.calls=__BTM_CARDS.map(function(){return null;});sessionStorage.setItem('btm.run.v1',JSON.stringify(r));return true;})()`);
    await B.nav(url, READY); await sleep(200);
    const forged = { step: await step(), memo: await ev(MEMO_SHOWN) };
    check("a saved read naming an account not on the ledger is not a read", forged.step === 2 && !forged.memo, forged);

    /* the address: there is no step parameter, and one added does nothing */
    await ev("sessionStorage.clear();true");
    await B.nav(url + "&step=5#step=5", READY); await sleep(200);
    const addr = { step: await step(), memo: await ev(MEMO_SHOWN) };
    check("a step in the address is ignored and the drill starts at the intro", addr.step === 0 && !addr.memo, addr);

    /* ---------- 2. keyboard, reload and lock ---------- */
    await toReadScreen(false);
    const tabs = [];
    for (let k = 0; k < 90; k++) {
      await press("Tab");
      const d = await ev("(function(){var a=document.activeElement;if(!a) return null;return a.getAttribute('data-p')!==null?'chip '+a.getAttribute('data-p'):(a.hasAttribute('data-precont')?'onward':(a.id||a.className||a.tagName));})()");
      tabs.push(d);
      if (d === "onward") break;
    }
    const nChips = s2.chips;
    const chipsReached = new Set(tabs.filter((t) => t && t.startsWith("chip ")));
    check("Tab reaches every line chip and then the onward button at 375", chipsReached.size === nChips && tabs[tabs.length - 1] === "onward", { reached: chipsReached.size, of: nChips, last: tabs[tabs.length - 1], presses: tabs.length });

    await ev("document.querySelector('#prepicks .chip[data-p=\"1\"]').focus();true");
    await press("Space");
    const sp = await ev("document.querySelector('#prepicks .chip[data-p=\"1\"]').getAttribute('aria-pressed')");
    await ev("document.querySelector('#prepicks .chip[data-p=\"2\"]').focus();true");
    await press("Enter");
    const en1 = await ev("document.querySelector('#prepicks .chip[data-p=\"2\"]').getAttribute('aria-pressed')");
    await press("Enter");
    const en2 = await ev("document.querySelector('#prepicks .chip[data-p=\"2\"]').getAttribute('aria-pressed')");
    await ev("document.querySelector('#prepicks .chip[data-p=\"1\"]').focus();true");
    await press("Space");
    const sp2 = await ev("document.querySelector('#prepicks .chip[data-p=\"1\"]').getAttribute('aria-pressed')");
    check("Space and Enter toggle a line chip on and off, and aria-pressed follows", sp === "true" && en1 === "true" && en2 === "false" && sp2 === "false", { sp, en1, en2, sp2 });

    /* the planned read: the first line's account, the first clean line's account, and a ledger account with no line where one exists */
    const plan = await ev(`(function(){var cards=__BTM_CARDS, codes=Array.prototype.map.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.textContent.split(' ')[0];});
      var stand=cards.filter(function(c){return c.key==='stand';})[0];
      var onCard=function(code){return cards.some(function(c){return String(c.acct)===code;});};
      var spare=codes.filter(function(c){return !onCard(c);})[0];
      var want=[String(cards[0].acct), String(stand.acct)]; if(spare) want.push(spare);
      return {codes:codes, want:want};})()`);
    for (const code of plan.want) {
      await ev(`(function(){var b=Array.prototype.filter.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.textContent.split(' ')[0]===${JSON.stringify(code)};})[0];b.click();return true;})()`);
      await sleep(40);
    }
    const picksLedgerOrder = plan.codes.filter((c) => plan.want.includes(c));
    const tappedState = await ev("({picks:__BTM.prepicks.slice(), at:__BTM.prepickAt, stat:document.getElementById('prepickstat').textContent, go:" + VISIBLE_GO + "})");
    check("tapping saves the read in ledger order without locking it", JSON.stringify(tappedState.picks) === JSON.stringify(picksLedgerOrder) && !tappedState.at, tappedState);
    check("the onward label and the status change once a line is tapped", tappedState.go[0].text === "Lock in my read and continue" && /You have tapped \d+ lines?\./.test(tappedState.stat), tappedState);

    await B.nav(url, READY); await sleep(200);
    const reloaded = await ev("({step:__BTM.step, pressed:Array.prototype.filter.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.getAttribute('aria-pressed')==='true';}).map(function(b){return b.textContent.split(' ')[0];})})");
    check("a reload on the read screen keeps what was tapped", reloaded.step === 2 && JSON.stringify(reloaded.pressed) === JSON.stringify(picksLedgerOrder), reloaded);

    await clickGo(); await sleep(250);
    const locked = await ev("({step:__BTM.step, picks:__BTM.prepicks.slice(), at:__BTM.prepickAt, before:__BTM.prepickCallsBefore, memo:!!document.querySelector('#screen .quote')})");
    check("going on locks the read and opens line one", locked.step === 3 && locked.at > 0 && locked.before === 0 && locked.memo, locked);

    await ev("__BTM_GO(2);true"); await sleep(150);
    const relook = await ev("({disabled:Array.prototype.every.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.disabled;}), go:" + VISIBLE_GO + ", stat:document.getElementById('prepickstat').textContent})");
    await ev("(function(){var b=document.querySelector('#prepicks .chip:not(.on)');if(b){b.disabled=false;b.click();}return true;})()");
    const afterForcedTap = await ev("__BTM.prepicks.slice()");
    check("a locked read cannot be changed, even with a chip re-enabled by hand", relook.disabled && relook.go[0].text === "Continue to the memo" && JSON.stringify(afterForcedTap) === JSON.stringify(picksLedgerOrder), { relook, afterForcedTap });
    await clickGo(); await sleep(200);

    /* ---------- 3 and 4. a run with two calls turned over, the end screen, the payload, the record ---------- */
    const cards1 = await ev("__BTM_CARDS");
    const off = [0, 3];
    const calls1 = cards1.map((c, i) => (off.includes(i) ? (c.key === "flag" ? "stand" : "flag") : c.key));
    await playRun((round, i, card) => (round === 1 ? calls1[i] : card.key));
    const exp1 = expected(cards1, picksLedgerOrder, calls1, cases.one);
    const end1 = await ev(`(function(){var s=document.querySelector('.readshift');var d=s&&s.querySelector('details.readlines');
      var closed=d?!d.open:null, summary=d?d.querySelector('summary').textContent:null; if(d) d.open=true;
      return {step:__BTM.step, has:!!s, closed:closed, summary:summary, text:s?s.innerText:'', items:s?s.querySelectorAll('li').length:0,
      points:__BTM.points, rank:document.querySelector('.rankbig')&&document.querySelector('.rankbig').textContent};})()`);
    out.endScreenRun1 = end1;
    const changed1 = exp1.toward + exp1.away;
    const wantLead = leadText(picksLedgerOrder.length, exp1, cards1.length);
    check("the changed lines sit behind one disclosure that names how many moved", end1.closed === true && end1.summary === "See the " + word(changed1) + " lines that moved", { closed: end1.closed, summary: end1.summary });
    check("the end screen states where the final calls moved off the read, with the right counts", end1.step === st.done && end1.has && end1.text.indexOf(wantLead) > -1 && end1.items === changed1,
      { want: wantLead, got: end1.text, items: end1.items, expected: { toward: exp1.toward, away: exp1.away, held: exp1.held } });

    await ev("document.getElementById('sendres').click();true"); await sleep(400);
    const post1 = await ev("window.__BTM_LAST_POST");
    const rec1 = await ev("__BTM_RECORD(window.__BTM_LAST_POST)");
    check("the form payload's round one question carries the read per line with the case version", post1["entry.1115022539"] === exp1.cell, { want: exp1.cell, got: post1["entry.1115022539"] });
    const r1 = rec1.responses.filter((x) => x.round === 1);
    const perLineOk = r1.every((x, i) => x.ledgerOnlyRead === exp1.read[i] && x.caseVersion === cases.one &&
      x.readVersusFinal === { held: "held", toward: "changed toward the key", away: "changed away from the key" }[exp1.moves[i]]);
    const r2none = rec1.responses.filter((x) => x.round === 2).every((x) => x.ledgerOnlyRead === null && x.readVersusFinal === null);
    check("the record carries the read on every round one response with its case version, and none on round two", perLineOk && r2none, r1.map((x) => [x.item, x.caseVersion, x.ledgerOnlyRead, x.readVersusFinal]));
    const pb = rec1.prepicks;
    check("the record's prepicks block carries the version, both letter strings and the counts", pb.required && pb.taken && pb.caseVersion === cases.one &&
      pb.readByLine === exp1.readLetters && pb.finalByLine === exp1.finalLetters && pb.beforeAnyCall === true &&
      pb.afterDraft.changedTowardKey === exp1.toward && pb.afterDraft.changedAwayFromKey === exp1.away && pb.afterDraft.held === exp1.held &&
      JSON.stringify(pb.picks) === JSON.stringify(picksLedgerOrder) && rec1.payload["entry.1115022539"] === exp1.cell, pb);
    check("the send stayed local in test mode", rec1.attempt.testAttempt === true && /test mode/.test(rec1.attempt.submissionState), rec1.attempt.submissionState);
    fs.writeFileSync(path.join(OUTDIR, CASE + "-payload-run1.json"), JSON.stringify({ payload: post1, prepicks: pb, expected: exp1 }, null, 2));

    for (const w of [320, 375, 768, 1280]) {
      await B.width(w); await sleep(250);
      await audit("end screen, run one, " + w);
    }
    await B.width(375); await sleep(200);

    /* ---------- 5. Play again carries nothing of the first read ---------- */
    await ev("window.scrollTo(0,0);document.getElementById('playagain').click();true"); await sleep(200);
    const again = await ev("({step:__BTM.step, picks:__BTM.prepicks.slice(), at:__BTM.prepickAt, before:__BTM.prepickCallsBefore, run:__BTM.runIndex})");
    check("Play again clears the read", again.step === 1 && again.picks.length === 0 && again.at === 0 && again.run === 2, again);
    await ev("document.getElementById('next').click();true"); await sleep(200);
    const again2 = await ev("({step:__BTM.step, pressed:document.querySelectorAll('#prepicks .chip[aria-pressed=\"true\"]').length, disabled:document.querySelectorAll('#prepicks .chip:disabled').length, go:" + VISIBLE_GO + ", cell:(function(){var p=null;try{p=__BTM_RECORD(null);}catch(e){return String(e);}return p.payload['entry.1115022539']+' | taken '+p.prepicks.taken;})()})");
    check("the second run opens on an empty, unlocked read and posts no stale one", again2.step === 2 && again2.pressed === 0 && again2.disabled === 0 && again2.go[0].text === "Tap at least one line" && again2.cell === "Prepicks: not recorded. | taken false", again2);
    await ev("__BTM_GO(3);true"); await sleep(150);
    check("the second run cannot skip the read either", (await step()) === 2 && !(await ev(MEMO_SHOWN)));

    for (const w of [320, 375, 768, 1024, 1280, 1600]) {
      await B.width(w); await sleep(300);
      const o = await audit("read screen, " + w);
      /* at a desk width the button sits under the lines; scrolled there, the legend rail must be
         wholly in view or wholly scrolled away, never half under the progress bar */
      let rail = null;
      if (w >= 900) {
        await ev("window.scrollTo(0,document.documentElement.scrollHeight);true"); await sleep(150);
        await ev("document.getElementById('prepickstat').scrollIntoView({block:'center'});true"); await sleep(150);
        rail = await ev("(function(){var s=document.querySelector('.orientside'),b=document.getElementById('bar');var r=s.getBoundingClientRect(),bb=b.getBoundingClientRect().bottom;return {railTop:Math.round(r.top),railBottom:Math.round(r.bottom),barBottom:Math.round(bb),straddles:r.top<bb&&r.bottom>bb,position:getComputedStyle(s).position};})()");
      }
      const vis = await ev(VISIBLE_GO);
      check("at " + w + " exactly one onward button is visible" + (w >= 900 ? " under the lines" : " in the sticky bar"),
        vis.length === 1 && vis[0].where === (w >= 900 ? "under the lines" : "sticky bar"), vis);
      if (w >= 900) check("at " + w + " the legend rail scrolls with the page and is never half under the progress bar at the lines", rail && rail.position !== "sticky" && !rail.straddles, rail);
    }
    await B.width(1280); await sleep(200);
    await ev("document.getElementById('orienthead').focus();true");
    const tabs2 = [];
    for (let k = 0; k < 90; k++) {
      await press("Tab");
      const d = await ev("(function(){var a=document.activeElement;if(!a) return null;return a.getAttribute('data-p')!==null?'chip '+a.getAttribute('data-p'):(a.hasAttribute('data-precont')?'onward':(a.id||a.className||a.tagName));})()");
      tabs2.push(d);
      if (d === "onward") break;
    }
    check("Tab reaches every line chip and then the onward button at 1280", new Set(tabs2.filter((t) => t && t.startsWith("chip "))).size === nChips && tabs2[tabs2.length - 1] === "onward", { presses: tabs2.length, last: tabs2[tabs2.length - 1] });
    const a11y = await ev("({unnamed:Array.prototype.filter.call(document.querySelectorAll('#prepicks .chip,[data-precont]'),function(b){return !b.textContent.trim();}).length, group:document.getElementById('prepicks').getAttribute('role'), labelledby:document.getElementById('prepicks').getAttribute('aria-labelledby'), live:document.getElementById('prepickstat').getAttribute('aria-live')})");
    check("every chip and onward button has a visible name, the chips sit in a labeled group, and the status is announced", a11y.unnamed === 0 && a11y.group === "group" && a11y.labelledby === "prepickhead" && a11y.live === "polite", a11y);

    await B.width(375); await sleep(200);
    const lastCard = cards1[cards1.length - 1];
    const picks2 = [String(lastCard.acct)];
    await ev(`(function(){var b=Array.prototype.filter.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.textContent.split(' ')[0]===${JSON.stringify(picks2[0])};})[0];b.click();return true;})()`);
    await clickGo(); await sleep(250);
    const calls2 = cards1.map(() => "stand");
    await playRun((round) => "stand");
    const exp2 = expected(cards1, picks2, calls2, cases.one);
    const end2 = await ev("(function(){var s=document.querySelector('.readshift');return {step:__BTM.step, text:s?s.innerText:'', items:s?s.querySelectorAll('li').length:0};})()");
    const changed2 = exp2.toward + exp2.away;
    const wantLead2 = leadText(1, exp2, cards1.length);
    check("the second run's end screen reports the second read, not the first", end2.step === st.done && end2.text.indexOf(wantLead2) > -1 && end2.items === changed2, { want: wantLead2, got: end2.text });
    await ev("document.getElementById('sendres').click();true"); await sleep(400);
    const post2 = await ev("window.__BTM_LAST_POST");
    const rec2 = await ev("__BTM_RECORD(window.__BTM_LAST_POST)");
    check("the second run's payload and record carry the second read", post2["entry.1115022539"] === exp2.cell && JSON.stringify(rec2.prepicks.picks) === JSON.stringify(picks2) && rec2.attempt.runIndex === 2,
      { want: exp2.cell, got: post2["entry.1115022539"], picks: rec2.prepicks.picks });
    fs.writeFileSync(path.join(OUTDIR, CASE + "-payload-run2.json"), JSON.stringify({ payload: post2, prepicks: rec2.prepicks, expected: exp2 }, null, 2));
    for (const w of [320, 768, 1280]) { await B.width(w); await sleep(250); await audit("end screen, run two, " + w); }
    out.endScreenRun2 = end2;
  } catch (e) {
    check("the walk ran to the end without throwing", false, e.message);
  } finally {
    out.errors = B.errors;
    B.close(); srv.close();
  }
  check("no console errors or uncaught exceptions", out.errors.length === 0, out.errors);
  const bad = out.widths.filter((w) => !w.clean);
  check("no horizontal overflow on any audited screen and width", bad.length === 0, bad);
  fs.writeFileSync(path.join(OUTDIR, CASE + "-walk.json"), JSON.stringify(out, null, 2));
  const passed = out.checks.filter((c) => c.pass).length;
  console.log(CASE + ": " + passed + " of " + out.checks.length + " checks passed");
  process.exitCode = passed === out.checks.length ? 0 : 1;
})();
