#!/usr/bin/env node
/* Plays scripted tester runs through index.html in the harness and prints, as JSON, the record
 * each run puts into question 9 beside the facts the drill itself holds for every line. The
 * parser test (tools/tests/test_tester_record_parse.py) reads this, so tools/tester_record_parse.py
 * and testerRecord() in index.html cannot drift apart without a test saying so.
 *
 *   node tests/tester-record-emit.cjs            the built-in runs
 *   node tests/tester-record-emit.cjs runs.json  runs of your own, in the same shape as RUNS
 *
 * A run is a list of lines, each [call, chips, words, seconds], played from line 1. A run longer
 * than five lines presses Keep going at the stop. budget cuts the record the way the form link
 * does, in encoded characters, so a truncated record can be produced on purpose. link: true sets
 * the two prefill constants to test values and takes the record out of the feedback link itself,
 * cut exactly as a tester would send it. again is a second list of lines, played after Play again
 * on the end screen, and gives a second record from the same tab marked run 2.
 */
"use strict";
const fs = require("fs");
const { boot } = require("./index-harness.cjs");

const H = "the figure and reason hold", TIE = "figure does not tie", DIR = "direction wrong",
  SRC = "no source on file", PER = "wrong period", ACC = "wrong account", OWE = "nothing written where owed";
/* the shape of a real pre-filled link, the same test values tests/run-tester-record-tests.cjs uses */
const PREFILL = {
  base: "https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAN__TESTONLYUMkpXSE9GRkJaWkFHMVBTNkJBTVVDQi4u",
  param: "r0123456789abcdef0123456789abcdef",
};

const RUNS = [
  { codename: "Amber Owl", lines: [
    ["flag", [TIE, OWE], "June total does not tie to the ledger", 41],
    ["flag", [PER], "this belongs in May", 33],
    ["stand", [H], "", 18],
    ["stand", [H], "", 12],
    ["stand", [H], "", 9]],
    again: [
    ["flag", [TIE, OWE], "", 14], ["flag", [PER, SRC], "", 12], ["flag", [DIR, SRC], "", 10],
    ["stand", [H], "", 8], ["stand", [H], "", 6]] },
  { codename: "Slate Heron", lines: [
    ["stand", [H], "", 25],
    ["flag", [PER, SRC], "accrual, \"not\" June's", 52],
    ["flag", [DIR, SRC], "it fell, the memo says rose", 38],
    ["flag", [ACC], "looks like the wrong account", 27],
    ["stand", [H], "", 14]] },
  { codename: "Teal Wren", link: true, lines: [
    ["flag", [TIE], "the subtraction is off by a zero, it fell 65,000 not 6,500 as written", 30],
    ["flag", [PER, SRC], "finished on June 30 and still running into August, both cannot be true", 31],
    ["flag", [DIR], "the memo says declined next to a June balance higher than May", 22],
    ["stand", [H], "", 11], ["stand", [H], "", 10], ["stand", [H], "", 9],
    ["stand", [H], "", 15], ["flag", [TIE, SRC], "the account moved 47,000 and the memo says 42,000 for the reserve", 28],
    ["stand", [H], "", 8], ["stand", [H], "", 7],
    ["flag", [OWE, SRC], "wages cleared both legs and the memo says nothing about them at all", 26],
    ["flag", [SRC], "the depot and the quarter forecast have nothing on file behind them", 19],
    ["stand", [H], "", 6], ["flag", [SRC], "no fixed asset additions and depreciation flat, so the story fails", 24]] },
  { codename: "Ivory Seal", budget: 900, lines: [
    ["flag", [TIE], "", 30], ["flag", [PER, SRC], "", 31], ["flag", [DIR], "", 22],
    ["stand", [H], "", 11], ["stand", [H], "", 10], ["stand", [H], "", 9],
    ["stand", [H], "", 15], ["flag", [TIE, SRC], "", 28], ["stand", [H], "", 8],
    ["stand", [H], "", 7], ["flag", [OWE, SRC], "", 26], ["flag", [SRC], "", 19],
    ["stand", [H], "", 6], ["flag", [SRC], "", 24]] },
];

function decodeLink(href) {
  const head = PREFILL.base + "&" + PREFILL.param + "=";
  if (!href || href.indexOf(head) !== 0) throw new Error("the feedback link does not carry the prefill: " + href);
  return decodeURIComponent(href.slice(head.length));
}

function playLines(t, lines) {
  const S = t.S();
  lines.forEach((l, k) => {
    const i = S.step - 3;
    t.click(l[0]);
    S.basis[i] = l[1].slice();
    const box = t.el("basiswords");
    if (box) box.value = l[2] || "";
    S.itemStart = Date.now() - (l[3] || 0) * 1000;
    t.click("lockin");
    if (k < lines.length - 1) {
      if (t.el("next")) t.click("next");
      else if (t.el("keepgoing")) t.click("keepgoing");
    }
  });
}

/* what the drill holds for the run as it stands, and the record it would send */
function snapshot(t, run) {
  const S = t.S();
  const cards = t.cards();
  const reason = t.window.__BTM_REASON;
  const facts = [];
  for (let i = 0; i < cards.length; i++) {
    const call = S.calls[i];
    if (call !== "stand" && call !== "flag") continue;
    const c = cards[i];
    const right = call === c.key;
    facts.push({
      line: i + 1, account: c.acct, call, chips: (S.basis[i] || []).slice(), key: c.key,
      outcome: right ? (c.key === "flag" ? "caught" : "cleared") : (c.key === "flag" ? "missed" : "false flag"),
      basis_agrees: reason.right(i, 1), seconds: S.asecs[i], words: S.words[i] || "",
    });
  }
  let record, included, wordsCap, wordsOffAfter;
  if (run.link) {
    const pf = t.window.__BTM_TESTER.prefill();
    record = decodeLink(pf.href); included = pf.included; wordsCap = pf.wordsCap; wordsOffAfter = pf.wordsOffAfter;
  } else {
    const parts = t.window.__BTM_TESTER.parts(run.budget === undefined ? undefined : run.budget);
    record = parts.text; included = parts.included; wordsCap = parts.wordsCap; wordsOffAfter = parts.wordsOffAfter;
  }
  return {
    record, included, words_cap: wordsCap, words_off_after: wordsOffAfter,
    header: { version: "1.9.2", codename: S.codename, attempt_id: S.attemptId, case: "halyard",
              answered: facts.length, right: facts.filter((f) => f.outcome === "caught" || f.outcome === "cleared").length,
              points: S.points, run: S.runIndex, case_file: "halyard-v4" },
    lines: facts.slice(0, included),
  };
}

(async () => {
  const runs = process.argv[2] ? JSON.parse(fs.readFileSync(process.argv[2], "utf8")) : RUNS;
  const out = [];
  for (const run of runs) {
    const t = boot(Object.assign({ search: "?test=1" }, run.link ? { prefill: PREFILL } : {}));
    await t.ready();
    const S = t.S();
    S.tourSeen = true;
    t.click("go");
    if (run.codename) S.codename = run.codename;
    playLines(t, run.lines);
    out.push(snapshot(t, run));
    if (run.again) {
      /* the rest of round one, then the end screen and Play again, which goes straight to line 1 */
      while (S.step - 3 >= 0 && S.step - 3 < t.steps().lines && !S.calls[S.step - 3]) {
        if (t.el("keepgoing")) { t.click("keepgoing"); continue; }
        playLines(t, [["stand", [H], "", 4]]);
        if (t.el("next")) t.click("next");
      }
      t.go(t.steps().done);
      t.click("playagain");
      playLines(t, run.again);
      out.push(snapshot(t, run));
    }
  }
  process.stdout.write(JSON.stringify(out, null, 1));
})().catch((e) => { console.error(e.stack || e); process.exit(2); });
