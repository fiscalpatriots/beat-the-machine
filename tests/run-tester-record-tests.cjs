#!/usr/bin/env node
/* The tester record and the feedback form link it rides in (release 1.9.2).
 *
 *   node tests/run-tester-record-tests.cjs
 *
 * Every test boots index.html in the harness (tests/index-harness.cjs) and plays the tester link
 * by pressing the page's own buttons: Play, Let it stand or Flag it, Lock it in, Keep going, Back,
 * Play again and the footer line. The basis chips are set in the run state, because the stub
 * draws no chip elements. Every way the page could reach the network is a spy, and the last tests
 * walk the whole tester link, the footer taps and the send guard to prove test mode posts nothing.
 *
 * Characters outside ASCII are built with String.fromCharCode, so this file stays ASCII.
 */
"use strict";
const { boot } = require("./index-harness.cjs");

const BARE = "https://forms.cloud.microsoft/r/Q2gRni88vR";
/* the shape of a real pre-filled link, with an id and a question name as long as Microsoft's */
const PREFILL = {
  base: "https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAN__TESTONLYUMkpXSE9GRkJaWkFHMVBTNkJBTVVDQi4u",
  param: "r0123456789abcdef0123456789abcdef",
};
const HEAD_LEN = (PREFILL.base + "&" + PREFILL.param + "=").length;
const BUDGET = 1800 - 1 - HEAD_LEN;
const CHIP = {
  hold: "the figure and reason hold", tie: "figure does not tie", dir: "direction wrong",
  src: "no source on file", period: "wrong period", acct: "wrong account", owed: "nothing written where owed",
};
const ch = (n) => String.fromCharCode(n);
const ARABIC = ch(0x0645);
const EMOJI = String.fromCodePoint(0x1F4CA);
const EM_DASH = ch(0x2014);

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
/* every round one line from where the run stands, Keep going pressed at the stop */
function playAll(t, line) {
  const S = t.S();
  while (S.step - 3 >= 0 && S.step - 3 < t.steps().lines && !S.calls[S.step - 3]) {
    const i = S.step - 3;
    play(t, ...line(i));
    if (i < t.steps().lines - 1) { if (t.el("next")) t.click("next"); else if (t.el("keepgoing")) t.click("keepgoing"); }
  }
}
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
/* five flagged lines with the same words on each, ending on the line 5 stop */
async function fiveWith(words) {
  const t = await testerRun({ prefill: PREFILL });
  for (let k = 0; k < 5; k++) { play(t, "flag", [CHIP.src, CHIP.tie], words, 5); if (k < 4) next(t); }
  return t;
}
function valueOf(href) {
  const head = PREFILL.base + "&" + PREFILL.param + "=";
  if (!href || href.indexOf(head) !== 0) return null;
  return decodeURIComponent(href.slice(head.length));
}
const TAIL_RE = /^(truncated after line|words cut to|words left off after line) \d+$/;
function split(record) {
  const parts = record.split("||");
  return {
    head: parts[0].split("|"),
    lines: parts.slice(1).filter((p) => !TAIL_RE.test(p)).map((p) => p.split("|")),
    trunc: parts.find((p) => /^truncated after line \d+$/.test(p)) || null,
    cut: parts.find((p) => /^words cut to \d+$/.test(p)) || null,
    off: parts.find((p) => /^words left off after line \d+$/.test(p)) || null,
  };
}
/* the record a word limit would give with words kept on the first keep lines, built from the
   full one the way the drill cuts */
function capRecord(full, cap, keep) {
  const parts = full.split("||");
  const segs = parts.slice(1);
  if (keep === undefined) keep = segs.length;
  let cut = false, off = false;
  const body = segs.map((p, idx) => {
    const f = p.split("|");
    if (f.length < 9) return p;
    const w = (cap && idx < keep) ? Array.from(f[8]).slice(0, cap).join("").trim() : "";
    if (w !== f[8]) { if (idx < keep) cut = true; else off = true; }
    return w ? f.slice(0, 8).concat([w]).join("|") : f.slice(0, 8).join("|");
  });
  if (cut) body.push("words cut to " + cap);
  if (off) body.push("words left off after line " + (keep ? segs[keep - 1].split("|")[0].slice(1) : 0));
  return [parts[0]].concat(body).join("||");
}
function netNonGet(t) {
  return t.net.filter((n) => !(n.kind === "fetch" && n.method === "GET" && /^cases\/[a-z0-9-]+\.json$/.test(n.url)));
}
function tap(t, times) { for (let k = 0; k < times; k++) t.click("masonfoot"); }
/* round two and the tester end screen, from wherever round one finished */
function finish(t) {
  const S = t.S();
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
}
const BAND_OFF = "Tester link<span>Nothing you do here is sent.</span>";
const BAND_ON = "Tester link<span>Nothing is sent from this page. The feedback form opens with your answers filled in, and Khaled sees them only if you submit it.</span>";

(async () => {
  /* ---------- T01-T04: the bare link when either constant is empty ---------- */
  {
    const t = await fiveLines();
    const html = t.screenHtml();
    eq("T01", "no prefill: the line 5 stop links to the bare form exactly as 1.9.1 did", t.feedbackHref(), BARE);
    check("T02", "no prefill: the stop keeps its 1.9.1 sentence and adds no note about the form",
      html.indexOf("That's five lines, which is all the feedback needs.") > -1 && html.indexOf("stopnote") === -1 && !!t.el("keepgoing"));
    eq("T03", "no prefill: the band still says nothing is sent", t.el("testband").innerHTML, BAND_OFF);
    eq("T03b", "no prefill: the version prints as 1.9.2 on the footer", t.el("verline").textContent, "second-pass-drill 1.9.2, test mode");
  }
  for (const [id, pf] of [["T04a", { base: PREFILL.base, param: "" }], ["T04b", { base: "", param: PREFILL.param }]]) {
    const t = await fiveLines({ prefill: pf });
    eq(id, "one constant empty (" + (pf.base ? "param" : "base") + "): the bare form, and the 1.9.1 band", [t.feedbackHref(), t.el("testband").innerHTML], [BARE, BAND_OFF]);
  }

  /* ---------- T05-T19: the record at the line 5 stop ---------- */
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
    eq("T07", "header: stamp, codename, attempt id, case, answered, right, points, run, case file",
      r.head, ["second-pass-drill 1.9.2", S.codename, S.attemptId, "case halyard", "answered 5", "right 3", "points " + S.points, "run 1", "case file halyard-v4"]);
    check("T07b", "header: points are the run's own total and above zero", S.points > 0 && r.head[6] === "points " + S.points);
    check("T07c", "the delimiters carry no spaces", rec.indexOf(" | ") === -1 && rec.indexOf(" || ") === -1 && /\|\|L1\|/.test(rec), rec);
    eq("T08", "five line segments, one per locked line, in order", r.lines.map((l) => l[0]), ["L1", "L2", "L3", "L4", "L5"]);
    eq("T09", "line 1: account, call, chips, key, caught, basis agrees, seconds, words with delimiters removed",
      r.lines[0], ["L1", "4200", "flag", "tie+owed", "key flag", "caught", "basis agrees", "34s", "Totals do not tie at all in June"]);
    eq("T10", "line 2: a stand on a keyed flag is missed, and holds differs from the key", r.lines[1], ["L2", "6200", "stand", "holds", "key flag", "missed", "basis differs", "12s"]);
    eq("T11", "line 3: caught with an extra chip is caught with a basis that differs", r.lines[2], ["L3", "5100", "flag", "direction+account", "key flag", "caught", "basis differs", "21s", "direction looks off"]);
    eq("T12", "line 4: a flag on a clean line is a false flag, words capped at 80", r.lines[3], ["L4", "4100", "flag", "source", "key stand", "false flag", "basis differs", "40s", "x".repeat(80)]);
    eq("T13", "line 5: cleared, basis agrees, no words field when nothing was written", r.lines[4], ["L5", "6500", "stand", "holds", "key stand", "cleared", "basis agrees", "9s"]);
    check("T14", "no truncation note and no word cut when every line fits", !/truncated|words cut/.test(rec) && t.window.__BTM_TESTER.prefill().wordsCap === 80);
    check("T15", "the link is under 1,800 characters", href.length < 1800, String(href.length));
    check("T16", "nothing identifying rides in it beyond the codename: no chapters, no notice, no clock",
      !/Beta Alpha|ACFE|NABA|notice|20\d\d-\d\d-\d\d|\d{10,}/.test(rec), rec);
    eq("T17", "prefill: the band says nothing leaves the page and the form opens with the answers in it", t.el("testband").innerHTML, BAND_ON);
    check("T18", "prefill: the stop says the five answers are filled in when the form opens and Khaled sees them only on submit",
      t.screenHtml().indexOf('<p class="stopnote">Your five answers are filled in when the feedback form opens, and Khaled sees them only if you submit it.</p>') > -1, t.screenHtml());
    const html = t.screenHtml();
    check("T19", "the href is written HTML-escaped, so the & between id and question survives", html.indexOf('href="' + PREFILL.base + "&amp;" + PREFILL.param + "=") > -1);
    check("T19b", "the copy carries no em dash", (html + t.el("testband").innerHTML).indexOf(EM_DASH) === -1);
  }

  /* ---------- T20-T24: escaping and the 80 character cap ---------- */
  {
    const t = await testerRun({ prefill: PREFILL });
    const S = t.S();
    S.codename = "Amber | Owl";
    play(t, "flag", [CHIP.tie], "a || b | c\r\nd" + ch(0x2028) + "e  \t f", 5); next(t);
    play(t, "flag", [CHIP.period, CHIP.src], EMOJI.repeat(100), 5); next(t);
    play(t, "flag", [CHIP.dir], "lone " + ch(0xD800) + " high and " + ch(0xDC00) + " low", 5);
    const rec = t.window.__BTM_TESTER.record();
    const r = split(rec);
    eq("T20", "a codename with a pipe loses it, and the header keeps nine fields", [r.head.length, r.head[1]], [9, "Amber Owl"]);
    eq("T21", "words lose pipes, line breaks, tabs and the line separators, and collapse their spaces", r.lines[0][8], "a b c d e f");
    eq("T22", "every line keeps its nine fields, so the delimiters only ever delimit", r.lines.map((l) => l.length), [9, 9, 9]);
    eq("T23", "the 80 character cap counts characters, so an emoji is never split", Array.from(r.lines[1][8]).length + ":" + r.lines[1][8].length, "80:160");
    eq("T24", "half of a surrogate pair is dropped, so the record always encodes", r.lines[2][8], "lone high and low");
    let threw = false; try { encodeURIComponent(rec); } catch (e) { threw = true; }
    check("T24b", "the record encodes without throwing", !threw);
    eq("T24c", "testerClean on its own: trims, removes pipes, caps", t.window.__BTM_TESTER.clean("  a|b  ", 2), "a");
  }

  /* ---------- T25-T29: Keep going, the 1,800 character cap, and words cut before lines ---------- */
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
    check("T26", "fourteen lines with long words all fit under 1,800 characters, because the words are cut and no line is",
      pf.href.length < 1800 && pf.included === 14 && pf.wordsCap === 20, pf.href.length + " chars, " + pf.included + " lines, words " + pf.wordsCap);
    eq("T27", "the record keeps every line in order, says how far the words were cut, and carries no truncation note",
      [r.lines.map((l) => l[0]), r.cut, r.trunc], [Array.from({ length: 14 }, (_, k) => "L" + (k + 1)), "words cut to 20", null]);
    check("T28", "every line's words are within the cut, and the calls are untouched",
      r.lines.every((l) => l.length < 9 || Array.from(l[8]).length <= 20) && r.lines.slice(5).every((l) => l[2] === "flag" && l[3] === "source+tie+period"));
    eq("T29", "the header still counts every locked line", r.head[4], "answered 14");
    const full = t.window.__BTM_TESTER.record();
    const keep = pf.wordsOffAfter === null ? 14 : pf.wordsOffAfter;
    const looser = keep < 14 ? capRecord(full, 20, keep + 1) : capRecord(full, 40);
    check("T29b", "the cut is the gentlest that fits: the step before it would not, and the record is that step exactly",
      encodeURIComponent(full).length > BUDGET && encodeURIComponent(looser).length > BUDGET && capRecord(full, 20, keep) === rec,
      "full " + encodeURIComponent(full).length + ", one step looser " + encodeURIComponent(looser).length + ", budget " + BUDGET + ", kept through " + keep);
    check("T29h", "when words must go from some lines, the newest lines lose theirs and the early notes stay",
      pf.wordsOffAfter === null || (r.off === "words left off after line " + pf.wordsOffAfter &&
        r.lines.slice(0, 5).filter((l) => l.length === 9).length === 3 && r.lines.slice(pf.wordsOffAfter).every((l) => l.length === 8)),
      rec);
    const wide = await testerRun({ prefill: PREFILL });
    for (let i = 0; i < 6; i++) { play(wide, "flag", [CHIP.src], ARABIC.repeat(80), 5); if (i < 4) next(wide); else if (i === 4) wide.click("keepgoing"); }
    const wp = wide.window.__BTM_TESTER.prefill();
    check("T29c", "eighty letters a line in a script that encodes long keeps all six calls under the cap",
      wp.href.length < 1800 && wp.included === 6 && !/truncated after line/.test(valueOf(wp.href)), wp.href.length + " chars, " + wp.included + " lines");
    /* the old cut dropped lines first; lines only go now when the calls alone do not fit */
    const tight = t.window.__BTM_TESTER.parts(600);
    const tr = split(tight.text);
    check("T29d", "a budget too small for the calls drops lines from the newest, words left out, and says where it stopped",
      tight.included < 14 && tight.included > 0 && tr.trunc === "truncated after line " + tight.included &&
      tr.lines.every((l) => l.length === 8) && encodeURIComponent(tight.text).length <= 600, tight.text);

    /* the end screen: round two, then the tester's own end screen */
    finish(t);
    eq("T30", "the tester end screen draws with the form link and no Send my results", [S.step === t.steps().done, !!t.el("feedbackform"), !!t.el("sendres")], [true, true, false]);
    const end = valueOf(t.feedbackHref());
    eq("T31", "the end screen's link carries the run as it stands, cut to fit", [end, t.feedbackHref().length < 1800], [t.window.__BTM_TESTER.record(BUDGET), true]);
    const endPf = t.window.__BTM_TESTER.prefill();
    const notes = endPf.wordsOffAfter === null
      ? " Your own words are cut to their first " + endPf.wordsCap + " characters so the link fits."
      : " Your own words are cut to their first " + endPf.wordsCap + " characters, and the ones after line " + endPf.wordsOffAfter + " are left out, so the link fits.";
    const want = '<p class="stopnote">Your ' + (endPf.included === 14 ? "fourteen" : "?") +
      " answers are filled in when the feedback form opens, and Khaled sees them only if you submit it." + notes +
      " If you already sent the form at line 5, send it again from here and the lines since go with it.</p>";
    check("T31b", "the end screen says what the link carries, its count matches prefill().included, and a tester who sent at line 5 is told to send again",
      endPf.included === 14 && t.screenHtml().indexOf(want) > -1, t.screenHtml().match(/<p class="stopnote">[^<]*<\/p>/) + "");
    check("T32", "the whole tester link, round two and the end screen included, made no request but the three case files",
      netNonGet(t).length === 0 && t.net.length === 3, JSON.stringify(t.net));
  }

  /* ---------- T29e-T29g: five lines of words that encode long keep all five calls ---------- */
  for (const [id, label, words] of [["T29e", "80 Arabic letters", ARABIC.repeat(80)], ["T29f", "80 emoji", EMOJI.repeat(80)],
                                    ["T29g", "80 accented letters", ch(0xE9).repeat(80)]]) {
    const t = await fiveWith(words);
    const pf = t.window.__BTM_TESTER.prefill();
    const r = split(valueOf(pf.href));
    const note = (t.screenHtml().match(/<p class="stopnote">[^<]*<\/p>/) || [""])[0];
    check(id, "five lines with " + label + " each keep all five calls, and the stop says the notes were cut",
      pf.on && pf.included === 5 && r.lines.length === 5 && r.lines.every((l) => l[2] === "flag") && pf.href.length < 1800 &&
      note.indexOf("Your five answers are filled in") > -1 && /Your own words (are cut to their first \d+ characters(, and the ones after line \d+ are left out,)?|are left out|after line \d+ are left out) so the link fits\./.test(note),
      pf.href.length + " chars, " + pf.included + " lines, words " + pf.wordsCap + ", " + note);
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

  /* ---------- T42-T43: three taps on the footer turn test mode on, and never off ---------- */
  {
    const t = await testerRun({ prefill: PREFILL });
    const S = t.S();
    tap(t, 3);
    eq("T42", "on the tester link, three taps on the footer leave test mode on: band shown, test attempt, footer says test mode",
      [t.el("testband").hidden, S.testAttempt, t.el("verline").textContent, t.el("testband").innerHTML], [false, true, "second-pass-drill 1.9.2, test mode", BAND_ON]);
    tap(t, 3);
    FIVE.forEach((l, k) => { play(t, l[0], l[1], l[2], l[3]); if (k < FIVE.length - 1) next(t); });
    check("T42b", "after six taps the line 5 stop still draws with the feedback form and Keep going",
      !!t.el("keepgoing") && !!t.el("feedbackform") && t.screenHtml().indexOf("stopnote") > -1);
    t.click("keepgoing");
    playAll(t, () => ["stand", [CHIP.hold], undefined, 4]);
    finish(t);
    eq("T42c", "the end screen after the taps has the feedback form and no Send my results", [S.step === t.steps().done, !!t.el("feedbackform"), !!t.el("sendres"), S.testAttempt], [true, true, false, true]);
    check("T42d", "and nothing was posted on the way", netNonGet(t).length === 0, JSON.stringify(t.net));

    const p = boot({ search: "" });
    await p.ready();
    tap(p, 3);
    const on = [p.el("testband").hidden, p.S().testAttempt];
    tap(p, 3);
    eq("T43", "on the public link three taps turn test mode on, and three more do not turn it off",
      [on, p.el("testband").hidden, p.S().testAttempt, p.el("verline").textContent], [[false, true], false, true, "second-pass-drill 1.9.2, test mode"]);
  }

  /* ---------- T44: Play again marks the record as a later run ---------- */
  {
    const t = await fiveLines({ prefill: PREFILL });
    const S = t.S();
    const first = { id: S.attemptId, code: S.codename, head: split(t.window.__BTM_TESTER.record()).head };
    t.click("keepgoing");
    playAll(t, () => ["stand", [CHIP.hold], undefined, 4]);
    t.go(t.steps().done);
    t.click("playagain");
    eq("T44", "Play again on the tester link goes straight to line 1 as run 2", [S.step, S.runIndex], [3, 2]);
    FIVE.forEach((l, k) => { play(t, l[0], l[1], l[2], l[3]); if (k < FIVE.length - 1) next(t); });
    const h = split(valueOf(t.feedbackHref())).head;
    eq("T44b", "the first run's header says run 1, the second's run 2, same codename, a new attempt id",
      [first.head[7], h[7], h[1] === first.code, h[2] !== first.id, h[4]], ["run 1", "run 2", true, true, "answered 5"]);
  }

  /* ---------- T45: a public run left in the tab is not picked up by the tester link ---------- */
  {
    const p = boot({ search: "" });
    await p.ready();
    p.S().codename = "Jane Q Student";
    p.go(1);
    const saved = p.store["btm.run.v1"];
    check("T45", "the public run was saved with its typed codename and as no test attempt",
      !!saved && JSON.parse(saved).codename === "Jane Q Student" && JSON.parse(saved).testAttempt === false);
    const t = boot({ search: "?test=1", session: { "btm.run.v1": saved } });
    await t.ready();
    t.S().tourSeen = true;
    t.click("go");
    play(t, "flag", [CHIP.tie], "", 5);
    const h = split(t.window.__BTM_TESTER.record()).head;
    check("T45b", "the tester link starts its own run under a random codename, not the saved one",
      h[1] !== "Jane Q Student" && h[2] !== JSON.parse(saved).attemptId && t.S().testAttempt === true, h.join("|"));
    /* a tester run itself still survives a reload */
    const mine = five.store["btm.run.v1"];
    const r = boot({ search: "?test=1", session: { "btm.run.v1": mine } });
    await r.ready();
    eq("T45c", "a tester run reloaded on the tester link keeps its codename and its five calls",
      [r.S().codename, r.S().calls.filter((c) => c).length], [JSON.parse(mine).codename, 5]);
  }

  /* ---------- T46: seconds are active seconds ---------- */
  {
    const t = await testerRun({ prefill: PREFILL });
    const S = t.S();
    t.click("flag");
    S.basis[0] = [CHIP.tie];
    S.itemStart = Date.now() - 50000;
    S.hiddenTotal = (S.itemHiddenBase || 0) + 30000;
    t.click("lockin");
    eq("T46", "a line that sat 30 of its 50 seconds in a hidden tab records 20 seconds",
      [S.secs[0], S.asecs[0], split(t.window.__BTM_TESTER.record()).lines[0][7]], [50, 20, "20s"]);
  }

  /* ---------- T47: the usual slips in pasting the two constants ---------- */
  {
    const clean = PREFILL.base + "&" + PREFILL.param + "=";
    for (const [id, label, pf] of [
      ["T47a", "a base pasted with a trailing &", { base: PREFILL.base + "&", param: PREFILL.param }],
      ["T47b", "a base pasted with the probe answer still on it", { base: PREFILL.base + "&" + PREFILL.param + "=probe", param: PREFILL.param }],
      ["T47c", "a name pasted with its & and =", { base: PREFILL.base, param: "&" + PREFILL.param + "=" }],
      ["T47d", "a base pasted with a trailing ?", { base: PREFILL.base + "?", param: PREFILL.param }],
    ]) {
      const t = await fiveLines({ prefill: pf });
      const href = t.feedbackHref();
      check(id, label + ": the link still carries question 9 once, after the clean base",
        href.indexOf(clean) === 0 && href.split(PREFILL.param + "=").length === 2 && valueOf(href) === t.window.__BTM_TESTER.record(), href.slice(0, 260));
    }
    const t = await fiveLines({ prefill: { base: BARE, param: PREFILL.param } });
    eq("T47e", "a base with no ResponsePage.aspx?id= counts as empty: the bare form and the 1.9.1 band",
      [t.feedbackHref(), t.el("testband").innerHTML, t.screenHtml().indexOf("stopnote")], [BARE, BAND_OFF, -1]);
  }

  console.log("\n" + passed + " passed, " + failed + " failed, " + (passed + failed) + " run");
  if (failed) { console.log("failed: " + fails.join(", ")); process.exit(1); }
})().catch((e) => { console.error(e.stack || e); process.exit(2); });
