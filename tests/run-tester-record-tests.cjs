#!/usr/bin/env node
/* The tester record and the feedback form link it rides in (release 1.9.2).
 *
 *   node tests/run-tester-record-tests.cjs
 *
 * Every test boots index.html in the harness (tests/index-harness.cjs) and plays the tester link
 * by pressing the page's own buttons: Play, Let it stand or Flag it, Lock it in, Keep going and
 * Back. The basis chips are set in the run state, because the stub draws no chip elements.
 * Every way the page could reach the network is a spy, and the last tests walk the whole tester
 * link and the send guard to prove test mode posts nothing.
 */
"use strict";
const { boot } = require("./index-harness.cjs");

const BARE = "https://forms.cloud.microsoft/r/Q2gRni88vR";
/* the shape of a real pre-filled link, with an id and a question name as long as Microsoft's */
const PREFILL = {
  base: "https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAN__TESTONLYUMkpXSE9GRkJaWkFHMVBTNkJBTVVDQi4u",
  param: "r0123456789abcdef0123456789abcdef",
};
const CHIP = {
  hold: "the figure and reason hold", tie: "figure does not tie", dir: "direction wrong",
  src: "no source on file", period: "wrong period", acct: "wrong account", owed: "nothing written where owed",
};

let passed = 0, failed = 0;
const fails = [];
function check(id, name, ok, detail) {
  if (ok) { passed++; console.log("pass " + id + " " + name); }
  else { failed++; fails.push(id); console.log("FAIL " + id + " " + name + (detail ? "\n     " + detail : "")); }
}
function eq(id, name, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  check(id, name, ok, ok ? "" : "got  " + JSON.stringify(got) + "\n     want " + JSON.stringify(want));
}

/* a run on the tester link, from the intro to line 1 */
async function testerRun(opts) {
  const t = boot(Object.assign({ search: "?test=1" }, opts || {}));
  await t.ready();
  t.S().tourSeen = true;
  t.click("go");
  return t;
}
/* one line: the call, the chips, the words (a flag only offers the words box) and the seconds */
function play(t, call, chips, words, secs) {
  const S = t.S();
  const i = S.step - 3;
  t.click(call);
  S.basis[i] = chips.slice();
  const box = t.el("basiswords");
  if (box && words !== undefined) box.value = words;
  S.itemStart = Date.now() - (secs || 0) * 1000;
  t.click("lockin");
  return i;
}
/* Next line, when the reveal carries one (the line 5 stop carries Keep going instead) */
function next(t) { if (t.el("next")) t.click("next"); }
/* the five lines the stop asks for, one of every outcome and both basis results */
const FIVE = [
  ["flag", [CHIP.tie, CHIP.owed], "Totals | do not || tie\nat all\tin June", 34],
  ["stand", [CHIP.hold], undefined, 12],
  ["flag", [CHIP.dir, CHIP.acct], "direction looks off", 21],
  ["flag", [CHIP.src], "x".repeat(200), 40],
  ["stand", [CHIP.hold], undefined, 9],
];
async function fiveLines(opts) {
  const t = await testerRun(opts);
  FIVE.forEach((l, k) => { play(t, l[0], l[1], l[2], l[3]); if (k < FIVE.length - 1) next(t); });
  return t;
}
function valueOf(href) {
  const head = PREFILL.base + "&" + PREFILL.param + "=";
  if (!href || href.indexOf(head) !== 0) return null;
  return decodeURIComponent(href.slice(head.length));
}
function split(record) {
  const parts = record.split(" || ");
  return { head: parts[0].split(" | "), lines: parts.slice(1).filter((p) => !/^truncated after line \d+$/.test(p)).map((p) => p.split(" | ")), tail: parts[parts.length - 1] };
}
function netNonGet(t) {
  return t.net.filter((n) => !(n.kind === "fetch" && n.method === "GET" && /^cases\/[a-z0-9-]+\.json$/.test(n.url)));
}

(async () => {
  /* ---------- T01-T04: the bare link when either constant is empty ---------- */
  {
    const t = await fiveLines();
    const html = t.screenHtml();
    eq("T01", "no prefill: the line 5 stop links to the bare form exactly as 1.9.1 did", t.feedbackHref(), BARE);
    check("T02", "no prefill: the stop keeps its 1.9.1 sentence and adds no note about the form",
      html.indexOf("That's five lines, which is all the feedback needs.") > -1 && html.indexOf("stopnote") === -1 && !!t.el("keepgoing"));
    eq("T03", "no prefill: the band still says nothing is sent", t.el("testband").innerHTML, "Tester link<span>Nothing you do here is sent.</span>");
    eq("T03b", "no prefill: the version prints as 1.9.2 on the footer", t.el("verline").textContent, "second-pass-drill 1.9.2, test mode");
  }
  for (const [id, pf] of [["T04a", { base: PREFILL.base, param: "" }], ["T04b", { base: "", param: PREFILL.param }]]) {
    const t = await fiveLines({ prefill: pf });
    eq(id, "one constant empty (" + (pf.base ? "param" : "base") + "): the bare form, and the 1.9.1 band", [t.feedbackHref(), t.el("testband").innerHTML], [BARE, "Tester link<span>Nothing you do here is sent.</span>"]);
  }

  /* ---------- T05-T16: the record at the line 5 stop ---------- */
  let five;
  {
    const t = await fiveLines({ prefill: PREFILL });
    five = t;
    const S = t.S();
    const href = t.feedbackHref();
    const rec = valueOf(href);
    check("T05", "prefill: the link is BASE & PARAM = the encoded record", rec !== null && href === PREFILL.base + "&" + PREFILL.param + "=" + encodeURIComponent(rec), href);
    eq("T06", "prefill: the link carries the record the page builds now", rec, t.window.__BTM_TESTER.record());
    const r = split(rec);
    eq("T07", "header: stamp, codename, attempt id, case, answered, right, points",
      r.head, ["second-pass-drill 1.9.2", S.codename, S.attemptId, "case halyard", "answered 5", "right 3", "points " + S.points]);
    check("T07b", "header: points are the run's own total and above zero", S.points > 0 && r.head[6] === "points " + S.points);
    eq("T08", "five line segments, one per locked line, in order", r.lines.map((l) => l[0]), ["L1", "L2", "L3", "L4", "L5"]);
    eq("T09", "line 1: account, call, chips, key, caught, basis agrees, seconds, words with delimiters removed",
      r.lines[0], ["L1", "4200", "flag", "tie+owed", "key flag", "caught", "basis agrees", "34s", "Totals do not tie at all in June"]);
    eq("T10", "line 2: a stand on a keyed flag is missed, and holds differs from the key", r.lines[1], ["L2", "6200", "stand", "holds", "key flag", "missed", "basis differs", "12s"]);
    eq("T11", "line 3: caught with an extra chip is caught with a basis that differs", r.lines[2], ["L3", "5100", "flag", "direction+account", "key flag", "caught", "basis differs", "21s", "direction looks off"]);
    eq("T12", "line 4: a flag on a clean line is a false flag, words capped at 80", r.lines[3], ["L4", "4100", "flag", "source", "key stand", "false flag", "basis differs", "40s", "x".repeat(80)]);
    eq("T13", "line 5: cleared, basis agrees, no words field when nothing was written", r.lines[4], ["L5", "6500", "stand", "holds", "key stand", "cleared", "basis agrees", "9s"]);
    check("T14", "no truncation note when every line fits", !/truncated/.test(rec));
    check("T15", "the link is under 1,800 characters", href.length < 1800, String(href.length));
    check("T16", "nothing identifying rides in it beyond the codename: no chapters, no notice, no clock",
      !/Beta Alpha|ACFE|NABA|notice|20\d\d-\d\d-\d\d|\d{10,}/.test(rec), rec);
    eq("T17", "prefill: the band says where the answers go",
      t.el("testband").innerHTML, "Tester link<span>Nothing is sent from this page. Your answers go along in the feedback form, where you see them before you submit.</span>");
    check("T18", "prefill: the stop says the five answers are in the form and the form is the only way Khaled sees them",
      t.screenHtml().indexOf('<p class="stopnote">Your five answers are already filled into the feedback form, and submitting that form is the only way Khaled sees them.</p>') > -1);
    const html = t.screenHtml();
    check("T19", "the href is written HTML-escaped, so the & between id and question survives", html.indexOf('href="' + PREFILL.base + "&amp;" + PREFILL.param + "=") > -1);
    check("T19b", "the copy carries no em dash", !/\u2014/.test(html + t.el("testband").innerHTML));
  }

  /* ---------- T20-T24: escaping and the 80 character cap ---------- */
  {
    const t = await testerRun({ prefill: PREFILL });
    const S = t.S();
    S.codename = "Amber | Owl";
    play(t, "flag", [CHIP.tie], "a || b | c\r\nd\u2028e  \t f", 5); next(t);
    const emoji = "\ud83d\udcca".repeat(100);
    play(t, "flag", [CHIP.period, CHIP.src], emoji, 5); next(t);
    play(t, "flag", [CHIP.dir], "lone \ud800 high and \udc00 low", 5);
    const rec = t.window.__BTM_TESTER.record();
    const r = split(rec);
    eq("T20", "a codename with a pipe loses it, and the header keeps seven fields", [r.head.length, r.head[1]], [7, "Amber Owl"]);
    eq("T21", "words lose pipes, line breaks, tabs and the line separators, and collapse their spaces", r.lines[0][8], "a b c d e f");
    eq("T22", "every line keeps its nine fields, so the delimiters only ever delimit", r.lines.map((l) => l.length), [9, 9, 9]);
    eq("T23", "the 80 character cap counts characters, so an emoji is never split", Array.from(r.lines[1][8]).length + ":" + r.lines[1][8].length, "80:160");
    eq("T24", "half of a surrogate pair is dropped, so the record always encodes", r.lines[2][8], "lone high and low");
    let threw = false; try { encodeURIComponent(rec); } catch (e) { threw = true; }
    check("T24b", "the record encodes without throwing", !threw);
    eq("T24c", "testerClean on its own: trims, removes pipes, caps", t.window.__BTM_TESTER.clean("  a|b  ", 2), "a");
  }

  /* ---------- T25-T29: Keep going, the 1,800 character cap and truncation ---------- */
  {
    const t = await fiveLines({ prefill: PREFILL });
    t.click("keepgoing");
    const S = t.S();
    const words = "We tied the June balance to the ledger and the memo figure is still off by a lot";
    for (let i = 5; i < t.steps().lines; i++) {
      play(t, "flag", [CHIP.src, CHIP.tie, CHIP.period], words, 300 + i);
      if (i < t.steps().lines - 1) next(t);
    }
    eq("T25", "all fourteen lines locked", S.calls.filter((c) => c).length, 14);
    const pf = t.window.__BTM_TESTER.prefill();
    const rec = valueOf(pf.href);
    const r = split(rec);
    check("T26", "fourteen long lines are cut to fit under 1,800 characters", pf.href.length < 1800 && pf.included < 14, pf.href.length + " chars, " + pf.included + " lines");
    eq("T27", "the cut keeps the earliest lines in order, newest last, and says where it stopped",
      [r.lines.map((l) => l[0]), r.tail], [Array.from({ length: pf.included }, (_, k) => "L" + (k + 1)), "truncated after line " + pf.included]);
    check("T28", "the five lines the stop asks for always make it in", pf.included >= 5, String(pf.included));
    eq("T29", "the header still counts every locked line", r.head[4], "answered 14");
    const one = t.window.__BTM_TESTER.record(pf.href.length - (PREFILL.base.length + PREFILL.param.length + 2) + 1);
    check("T29b", "one more line does not fit, so the cut is the most that fits",
      encodeURIComponent(t.window.__BTM_TESTER.parts(1e9).text).length > 1800 - (PREFILL.base.length + PREFILL.param.length + 2) && one === rec);
    const wide = await testerRun({ prefill: PREFILL });
    const ws = wide.S();
    for (let i = 0; i < 6; i++) { play(wide, "flag", [CHIP.src], "\u0645".repeat(80), 5); if (i < 4) next(wide); else if (i === 4) wide.click("keepgoing"); }
    const wp = wide.window.__BTM_TESTER.prefill();
    check("T29c", "eighty letters a line in a script that encodes long still stays under the cap", wp.href.length < 1800 && /truncated after line \d+$/.test(valueOf(wp.href)), wp.href.length + " chars");

    /* the end screen: round two, then the tester's own end screen */
    next(t);
    if (t.el("r2go")) t.click("r2go");
    while (S.step >= t.steps().l2 && S.step <= t.steps().l2last) {
      const j = S.step - t.steps().l2;
      t.click("stand");
      S.r2basis[j] = [CHIP.hold];
      S.r2explain[j] = { decisiveEvidence: "The invoice on file matches", periodRelevance: "It is dated inside June", actionOrRequest: "No request needed here" };
      S.itemStart = Date.now() - 5000;
      t.click("lockin");
    }
    if (t.el("r2see")) t.click("r2see");
    if (S.step === 92 && t.el("r2next")) t.click("r2next");
    if (S.step !== t.steps().done) t.go(t.steps().done);
    eq("T30", "the tester end screen draws with the form link and no Send my results", [S.step === t.steps().done, !!t.el("feedbackform"), !!t.el("sendres")], [true, true, false]);
    const end = valueOf(t.feedbackHref());
    eq("T31", "the end screen's link carries the run as it stands, cut to fit", [end, t.feedbackHref().length < 1800], [t.window.__BTM_TESTER.record(1800 - 1 - (PREFILL.base.length + PREFILL.param.length + 2)), true]);
    check("T32", "the whole tester link, round two and the end screen included, made no request but the three case files",
      netNonGet(t).length === 0 && t.net.length === 3, JSON.stringify(t.net));
  }

  /* ---------- T33-T37: Back and a changed answer ---------- */
  {
    const t = await fiveLines({ prefill: PREFILL });
    const S = t.S();
    const before = valueOf(t.feedbackHref());
    t.click("keepgoing");
    eq("T33", "Keep going opens line 6 with its Back button", [S.step - 3, !!t.el("backline")], [5, true]);
    t.click("backline");
    eq("T34", "Back reopens line 5 with its call taken off", [S.step - 3, S.calls[4]], [4, null]);
    eq("T34b", "while line 5 is open the record holds four lines", split(t.window.__BTM_TESTER.record()).lines.length, 4);
    play(t, "flag", [CHIP.src], "changed my mind", 15);
    const after = valueOf(t.feedbackHref());
    check("T35", "the stop draws again with a link that carries the changed answer", before !== after && !!t.el("keepgoing"));
    eq("T36", "line 5 now reads as the new call", split(after).lines[4], ["L5", "6500", "flag", "source", "key stand", "false flag", "basis differs", "15s", "changed my mind"]);
    eq("T36b", "the other four lines are untouched", split(after).lines.slice(0, 4), split(before).lines.slice(0, 4));
    /* pressing the button reads the record again, so a link drawn earlier never goes out stale */
    S.words[0] = "edited after the draw";
    const a = t.el("feedbackform");
    t.click("feedbackform");
    check("T37", "pressing the button rewrites its href from the run as it is at that moment",
      valueOf(a.getAttribute("href")).indexOf("edited after the draw") > -1);
  }

  /* ---------- T38-T41: test mode makes no POST ---------- */
  {
    check("T38", "the line 5 stop made no request but the three case files", netNonGet(five).length === 0, JSON.stringify(five.net));
    const t = await fiveLines({ prefill: PREFILL });
    t.click("feedbackform");
    check("T39", "pressing the feedback button is a link, not a request", netNonGet(t).length === 0 && t.net.length === 3, JSON.stringify(t.net));
    /* the send guard itself: a run marked as a test attempt, at the public end screen, presses
       Send my results and nothing is posted */
    const p = boot({ search: "" });
    await p.ready();
    const S = p.S();
    S.prepicks = ["4200"]; S.prepickAt = Date.now(); S.prepickSkipped = false;
    S.codename = "Harness Run";
    for (let i = 0; i < p.steps().lines; i++) { S.calls[i] = p.cards()[i].key; S.sel[i] = S.calls[i]; S.first[i] = S.calls[i]; S.basis[i] = p.window.__BTM_REASON.key(p.cards()[i]).slice(0, 1); }
    S.testAttempt = true;
    p.window.__BTM_POINTS.rescore();
    p.go(p.steps().done);
    check("T40", "the public end screen offers Send my results", !!p.el("sendres"));
    p.click("sendres");
    eq("T41", "a test attempt presses Send and posts nothing: no form submit, no fetch POST, no beacon",
      [netNonGet(p), S.sendState], [[], "not sent, test mode"]);
  }

  console.log("\n" + passed + " passed, " + failed + " failed, " + (passed + failed) + " run");
  if (failed) { console.log("failed: " + fails.join(", ")); process.exit(1); }
})().catch((e) => { console.error(e.stack || e); process.exit(2); });
