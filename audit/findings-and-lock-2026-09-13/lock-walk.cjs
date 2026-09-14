/* The written-explanation lock on brightwater-v6, walked end to end in headless Chrome.
   node lock-walk.cjs <root> <outdir>

   Test mode the whole way, so nothing is posted. The walk plays Halyard's fourteen practice lines by
   clicking (one clean line flagged, so the end screen prints one false flag), then tries every way
   past the lock on fresh line 1 before answering it properly:
     no chip; empty boxes; whitespace; punctuation with the Enter key on the page; "a b" with Enter and
     Space on the lock button itself; stock non-answers with a forced click on a button stripped of
     aria-disabled; pasted text through execCommand and CDP; a reload in the middle of the item; and
     three direct state edits (the step hook, the saved run in sessionStorage, and a jump to the end).
   Each refusal is checked for: no call locked, no step taken, a status message naming what is missing,
   focus on the first missing part, aria-invalid on each failing box, and a visible error in words.
   Lines 2 to 5 are answered properly, line 2 through the Enter key. The send runs in test mode, and
   the payload and record are written for payload-findings.py.
   Writes <outdir>/lock-walk.json and <outdir>/lock-payload.json. Exits 1 on any failed check. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../author-repair-2026-09-13/cdp.cjs");
const [ROOT, OUTDIR] = [process.argv[2], process.argv[3] || __dirname];

const GOOD = ["The June invoice from the lab is on file.", "It dates the charge to June, the month the memo covers.",
  "Ask for the June case log to confirm the volume."];

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const { srv, port } = await serve(ROOT);
  const B = await launch("lockwalk");
  const ev = B.ev;
  const base = `http://127.0.0.1:${port}/`;
  const url = base + "index.html?test=1&case=halyard";
  const READY = "!!(window.__BTM_CASES&&window.__BTM&&document.getElementById('screen')&&document.getElementById('screen').children.length)";
  const out = { ran: new Date().toString(), root: ROOT, checks: [], refusals: {}, errors: [] };
  const check = (name, pass, detail) => {
    out.checks.push({ name, pass: !!pass, detail: detail === undefined ? null : detail });
    console.log((pass ? "PASS " : "FAIL ") + name);
  };
  const key = async (k, code, vk, text) => {
    await B.send("Input.dispatchKeyEvent", { type: "keyDown", key: k, code, windowsVirtualKeyCode: vk, text });
    await B.send("Input.dispatchKeyEvent", { type: "keyUp", key: k, code, windowsVirtualKeyCode: vk });
  };
  const state = () => ev(`(function(){
    var l=document.getElementById('lockin'), st=document.getElementById('lockstat');
    var boxes=[].map.call(document.querySelectorAll('#screen textarea.explain'),function(t){
      var err=document.getElementById(t.id+'-err');
      return {id:t.id, value:t.value, invalid:t.getAttribute('aria-invalid'), describedby:t.getAttribute('aria-describedby'),
        required:t.getAttribute('aria-required'), label:(document.querySelector('label[for="'+t.id+'"]')||{}).textContent||null,
        error:err&&!err.hidden?err.textContent:null, errorVisible:!!(err&&!err.hidden&&err.getBoundingClientRect().height>0),
        errorColor:err?getComputedStyle(err).color:null};});
    return {step:__BTM.step, calls:(__BTM.r2calls||[]).slice(), stored:(__BTM.r2explain||[]).slice(0,2),
      lockAria:l?l.getAttribute('aria-disabled'):null, lockDisabled:l?l.disabled:null, lockDescribedby:l?l.getAttribute('aria-describedby'):null,
      status:st?st.textContent:null, statusRole:st?st.getAttribute('role'):null, statusLive:st?st.getAttribute('aria-live'):null,
      statusVisible:!!(st&&st.getBoundingClientRect().height>0),
      active:document.activeElement?(document.activeElement.id||document.activeElement.className||document.activeElement.tagName):null,
      boxes:boxes};})()`);
  /* replace a box's text through the browser's own typing path */
  const typeInto = async (id, text) => {
    await ev(`(function(){var t=document.getElementById(${JSON.stringify(id)});t.focus();t.setSelectionRange(0,t.value.length);return true;})()`);
    if (text === "") {
      await key("Backspace", "Backspace", 8);
    } else {
      await B.send("Input.insertText", { text });
    }
    await sleep(40);
  };
  const fillAll = async (vals) => {
    const ids = ["ex-decisiveEvidence", "ex-periodRelevance", "ex-actionOrRequest"];
    for (let k = 0; k < 3; k++) await typeInto(ids[k], vals[k]);
  };
  const clickLock = () => ev("(function(){var l=document.getElementById('lockin');if(l) l.click();return true;})()");
  try {
    await B.width(1280);
    await B.nav(url, READY);
    await ev("sessionStorage.clear();localStorage.removeItem('btm.owncase.v1');true");
    await B.nav(url, READY);
    const st = await ev("__BTM_STEPS()");
    out.steps = st;
    await ev("document.getElementById('go').click();true"); await sleep(120);
    await ev("document.getElementById('noticego').click();true"); await sleep(120);
    await ev("var i=document.getElementById('cn');i.value='Lock Walk';i.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#orgs .chip').click();document.getElementById('next').click();true");
    await sleep(150);
    await ev(`(function(){var a=String(__BTM_CARDS[0].acct);var c=Array.prototype.filter.call(document.querySelectorAll('#prepicks .chip'),function(b){return b.textContent.split(' ')[0]===a;})[0];if(c) c.click();
      var go=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){var r=b.getBoundingClientRect();return r.width>0&&r.height>0;})[0];if(go) go.click();return true;})()`);
    await sleep(150);
    check("the required read is taken and the first practice line opens", (await ev("__BTM.step")) === 3);

    /* the fourteen practice lines, with the key's call except one clean line flagged */
    const falseFlagAt = await ev("__BTM_CARDS.findIndex(function(c){return c.key==='stand';})");
    let guard = 0;
    while (guard++ < 200) {
      const s = await ev("__BTM.step");
      if (s === st.bridge) break;
      if (await ev("!!document.getElementById('next')")) { await ev("document.getElementById('next').click();true"); await sleep(50); continue; }
      const i = s - 3;
      const call = await ev(`(function(){var c=__BTM_CARDS[${i}];var want=${i}===${falseFlagAt}?'flag':c.key;document.getElementById(want).click();return want;})()`);
      await sleep(40);
      await ev(`(function(){var c=__BTM_CARDS[${i}];var chips=[].slice.call(document.querySelectorAll('#commit .chip'));
        var want=${JSON.stringify(call)}==='flag'&&c.key==='stand'?'no source on file':(c.basisKey||[])[0];
        var hit=chips.filter(function(x){return x.textContent.trim()===want;})[0]||chips[0];if(hit) hit.click();
        document.getElementById('lockin').click();return true;})()`);
      await sleep(60);
    }
    check("the practice round reaches the bridge", (await ev("__BTM.step")) === st.bridge);
    check("the practice lines never ask for a written explanation", (await ev("document.querySelectorAll('textarea.explain').length")) === 0);
    await ev("document.getElementById('r2go').click();true"); await sleep(150);
    check("fresh line 1 opens after the bridge", (await ev("__BTM.step")) === st.l2);

    /* ---------------- fresh line 1: every way past the lock ---------------- */
    const L1 = st.l2;
    const refusedOk = (s, name, focusWant, statusWant) => {
      const locked = s.calls[0] !== null && s.calls[0] !== undefined;
      check(name + ": no call locked and no step taken", !locked && s.step === L1, { step: s.step, calls: s.calls });
      check(name + ": the status line says what is still needed", !!s.status && s.status.indexOf(statusWant || "Still needed") > -1 && s.statusVisible,
        { status: s.status });
      if (focusWant) check(name + ": focus moves to " + focusWant, s.active === focusWant || (focusWant === "chip" && /chip/.test(s.active || "")), { active: s.active });
      out.refusals[name] = s;
    };
    const k0 = await ev("__BTM_CARDS2[0].key");
    await ev(`document.getElementById(${JSON.stringify(k0)}).click();true`); await sleep(80);
    let s = await state();
    check("the three boxes carry their labels", s.boxes.map((b) => b.label).join(" | ") ===
      "The decisive evidence | Why it matters for this period | The action or source request that follows", s.boxes.map((b) => b.label));
    check("each box is required and described by a visible hint", s.boxes.every((b) => b.required === "true" && /ex-\w+-hint/.test(b.describedby || "")),
      s.boxes.map((b) => b.describedby));
    check("no placeholder text is left to be cut off", (await ev("[].every.call(document.querySelectorAll('#screen textarea.explain'),function(t){return !t.getAttribute('placeholder');})")));
    check("the lock is marked not ready for a screen reader and points at the status line", s.lockAria === "true" && s.lockDescribedby === "lockstat" && s.statusRole === "status" && s.statusLive === "polite", s);
    await clickLock(); await sleep(120);
    refusedOk(await state(), "no basis chip", "chip", "a basis chip");

    await ev(`(function(){var chips=[].slice.call(document.querySelectorAll('#commit .chip'));var want=(__BTM_CARDS2[0].basisKey||[])[0];
      var hit=chips.filter(function(x){return x.textContent.trim()===want;})[0]||chips[0];hit.click();return true;})()`);
    await sleep(60);
    await clickLock(); await sleep(120);
    s = await state();
    refusedOk(s, "empty boxes", "ex-decisiveEvidence");
    check("empty boxes: each box is aria-invalid with a visible error in words, tied by aria-describedby",
      s.boxes.every((b) => b.invalid === "true" && b.errorVisible && /^Needed: /.test(b.error) && (b.describedby || "").indexOf(b.id + "-err") === 0), s.boxes);

    await fillAll(["   ", "\t\t", "\n\n"]); await clickLock(); await sleep(120);
    refusedOk(await state(), "whitespace", "ex-decisiveEvidence");

    await fillAll(["...", "...", "..."]);
    await ev("document.activeElement.blur();true");
    await key("Enter", "Enter", 13, "\r"); await sleep(120);
    s = await state();
    refusedOk(s, "punctuation, Enter on the page", "ex-decisiveEvidence");
    check("punctuation: the error names punctuation", s.boxes[0].error === "Needed: words, not only punctuation or symbols.", s.boxes[0].error);

    await fillAll(["a b", "a b", "a b"]);
    await ev("document.getElementById('lockin').focus();true");
    await key("Enter", "Enter", 13, "\r"); await sleep(120);
    refusedOk(await state(), "two letters, Enter on the lock button", "ex-decisiveEvidence");
    await ev("document.getElementById('lockin').focus();true");
    await key(" ", "Space", 32, " "); await sleep(120);
    s = await state();
    refusedOk(s, "two letters, Space on the lock button", "ex-decisiveEvidence");
    check("two letters: the error names the minimum", s.boxes[0].error === "Needed: at least two words and eight letters or digits.", s.boxes[0].error);

    await fillAll(["none", "None.", "n/a"]);
    await ev("(function(){var l=document.getElementById('lockin');l.removeAttribute('aria-disabled');l.disabled=false;l.click();return true;})()");
    await sleep(120);
    s = await state();
    refusedOk(s, "stock non-answers, forced click", "ex-decisiveEvidence");
    check("stock non-answers: the error says they do not count", /do not count/.test(s.boxes[2].error || ""), s.boxes.map((b) => b.error));

    await ev(`(function(){var t=document.getElementById('ex-decisiveEvidence');t.focus();t.select();document.execCommand('insertText',false,'|||');return true;})()`);
    await typeInto("ex-periodRelevance", "...");
    await ev(`(function(){var t=document.getElementById('ex-actionOrRequest');t.focus();t.select();document.execCommand('insertText',false,'same as above');return true;})()`);
    await clickLock(); await sleep(120);
    refusedOk(await state(), "pasted text", "ex-decisiveEvidence");

    /* one good part and two short: focus lands on the first part that still falls short */
    await fillAll([GOOD[0], "June", GOOD[2]]); await clickLock(); await sleep(120);
    s = await state();
    refusedOk(s, "one short part in the middle", "ex-periodRelevance");
    check("one short part: only that box is marked", s.boxes.map((b) => b.invalid).join(",") === ",true," || JSON.stringify(s.boxes.map((b) => b.invalid)) === JSON.stringify([null, "true", null]), s.boxes.map((b) => b.invalid));

    /* reload in the middle of the item, with non-answers typed */
    await fillAll(["a b", "...", "none"]);
    await B.nav(url, READY); await sleep(250);
    s = await state();
    check("reload mid-item: the same item, with what was typed", s.step === L1 && s.boxes.map((b) => b.value).join("|") === "a b|...|none", { step: s.step, values: s.boxes.map((b) => b.value) });
    check("reload mid-item: the lock is still not ready", s.lockAria === "true", s.lockAria);
    await clickLock(); await sleep(120);
    refusedOk(await state(), "reload mid-item", "ex-decisiveEvidence");

    /* direct state edits */
    await ev(`(function(){__BTM.r2explain[0]={decisiveEvidence:'a b',periodRelevance:'...',actionOrRequest:'none'};__BTM.r2calls[0]=${JSON.stringify(k0)};__BTM_GO(${L1 + 1});return true;})()`);
    await sleep(200);
    s = await state();
    refusedOk(s, "state edit through the step hook", null, "This call was unlocked");
    check("state edit: the line reopens with the call unlocked and the errors showing", s.calls[0] === null && s.boxes.every((b) => b.invalid === "true"), s);

    await ev(`(function(){__BTM.r2explain[0]={decisiveEvidence:'none',periodRelevance:'none',actionOrRequest:'none'};__BTM.r2calls[0]=${JSON.stringify(k0)};__BTM_GO(__BTM_STEPS().done);return true;})()`);
    await sleep(200);
    s = await state();
    refusedOk(s, "state edit, jump to the end screen", null, "This call was unlocked");
    check("state edit, jump to the end: no end screen drawn", (await ev("!document.getElementById('sendres')")), null);

    await ev(`(function(){var k=Object.keys(sessionStorage).filter(function(x){return /btm\\.run/.test(x);})[0];var r=JSON.parse(sessionStorage.getItem(k));
      r.r2calls[0]=${JSON.stringify(k0)};r.r2explain[0]={decisiveEvidence:'ok',periodRelevance:'??',actionOrRequest:'test test'};r.step=92;sessionStorage.setItem(k,JSON.stringify(r));return true;})()`);
    await B.nav(url, READY); await sleep(250);
    s = await state();
    refusedOk(s, "state edit in the saved run, then reload", null, "This call was unlocked");

    /* answered properly, by typing */
    await fillAll(GOOD);
    s = await state();
    check("good answers: the lock is ready, the errors clear and the status says ready",
      s.lockAria === "false" && s.boxes.every((b) => !b.invalid && !b.errorVisible) && /^Ready\./.test(s.status || ""), s);
    out.acceptedState = s;
    await clickLock(); await sleep(200);
    s = await state();
    check("good answers: the call locks and the page moves to fresh line 2", s.step === L1 + 1 && s.calls[0] === k0, { step: s.step, calls: s.calls });
    const stored0 = await ev("__BTM.r2explain[0]");
    check("the stored answers are the cleaned text", JSON.stringify(stored0) === JSON.stringify({ decisiveEvidence: GOOD[0], periodRelevance: GOOD[1], actionOrRequest: GOOD[2] }), stored0);

    /* lines 2 to 5, line 2 through the Enter key */
    for (let i = 1; i < 5; i++) {
      const kk = await ev(`__BTM_CARDS2[${i}].key`);
      await ev(`document.getElementById(${JSON.stringify(kk)}).click();true`); await sleep(60);
      await ev(`(function(){var chips=[].slice.call(document.querySelectorAll('#commit .chip'));var want=(__BTM_CARDS2[${i}].basisKey||[])[0];
        var hit=chips.filter(function(x){return x.textContent.trim()===want;})[0]||chips[0];hit.click();return true;})()`);
      await fillAll(["Line " + (i + 1) + ": " + GOOD[0], GOOD[1], GOOD[2]]);
      if (i === 1) { await ev("document.activeElement.blur();true"); await key("Enter", "Enter", 13, "\r"); }
      else await clickLock();
      await sleep(150);
    }
    check("the fifth call opens the round two results", (await ev("__BTM.step")) === 92);
    await ev("document.getElementById('r2done').click();true"); await sleep(200);
    out.endCounts = await ev("(document.querySelector('.counts')||{}).textContent||null");
    /* the counts are three spans, a bold figure then its noun, so textContent runs them together */
    check("the end screen prints one false flag in the singular", /(^|\D)1false flag$/.test(out.endCounts || ""), out.endCounts);
    await ev("(function(){var b=document.getElementById('sendres');if(b) b.click();return true;})()"); await sleep(300);
    const payload = await ev("window.__BTM_LAST_POST||null");
    const record = await ev("__BTM_RECORD(null)");
    check("the send payload was built in test mode", !!payload);
    fs.writeFileSync(path.join(OUTDIR, "lock-payload.json"), JSON.stringify({ payload, record }, null, 1));
    const qc = payload ? payload["entry.756559246"] : "";
    check("question C carries the five explanations as written", [1, 2, 3, 4, 5].every((n) => qc.indexOf(n + ": Basis:") > -1) &&
      qc.indexOf("Evidence: " + GOOD[0]) > -1 && qc.indexOf("Evidence: Line 5: " + GOOD[0]) > -1 && qc.indexOf("Evidence: none") === -1, qc.slice(0, 400));
    check("the record names the minimum beside the prompts", record && record.writtenExplanationPrompts &&
      /two words and eight letters or digits/.test(record.writtenExplanationPrompts.minimum || "") && record.writtenExplanationPrompts.version === "explain-2026-09-13b",
      record && record.writtenExplanationPrompts);
    out.overflow1280 = await ev(OVERFLOW);
    out.errors = B.errors;
    check("no page error during the walk", !B.errors.length, B.errors);
  } catch (e) {
    out.failure = e.stack || e.message;
    out.errors = B.errors;
    console.log("FAILURE " + out.failure);
  } finally {
    B.close();
    srv.close();
  }
  out.passed = out.checks.filter((c) => c.pass).length;
  out.failed = out.checks.filter((c) => !c.pass).length;
  fs.writeFileSync(path.join(OUTDIR, "lock-walk.json"), JSON.stringify(out, null, 1));
  console.log(out.passed + " passed, " + out.failed + " failed" + (out.failure ? ", and the walk stopped early" : ""));
  process.exit(out.failed || out.failure ? 1 : 0);
})();
