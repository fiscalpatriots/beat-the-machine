#!/usr/bin/env node
/* Plays scripted tester runs through index.html in the harness and prints, as JSON, the record
 * each run puts into question 9 beside the facts the drill itself holds for every line. The
 * parser test (tests/test_tester_record_parse.py) reads this, so tools/tester_record_parse.py and
 * testerRecord() in index.html cannot drift apart without a test saying so.
 *
 *   node tests/tester-record-emit.cjs            the built-in runs
 *   node tests/tester-record-emit.cjs runs.json  runs of your own, in the same shape as RUNS
 *
 * A run is a list of lines, each [call, chips, words, seconds], played from line 1. A run longer
 * than five lines presses Keep going at the stop. budget cuts the record the way the form link
 * does, in encoded characters, so a truncated record can be produced on purpose.
 */
"use strict";
const fs = require("fs");
const { boot } = require("./index-harness.cjs");

const H = "the figure and reason hold", TIE = "figure does not tie", DIR = "direction wrong",
  SRC = "no source on file", PER = "wrong period", ACC = "wrong account", OWE = "nothing written where owed";

const RUNS = [
  { codename: "Amber Owl", lines: [
    ["flag", [TIE, OWE], "June total does not tie to the ledger", 41],
    ["flag", [PER], "this belongs in May", 33],
    ["stand", [H], "", 18],
    ["stand", [H], "", 12],
    ["stand", [H], "", 9]] },
  { codename: "Slate Heron", lines: [
    ["stand", [H], "", 25],
    ["flag", [PER, SRC], "accrual, \"not\" June's", 52],
    ["flag", [DIR, SRC], "it fell, the memo says rose", 38],
    ["flag", [ACC], "looks like the wrong account", 27],
    ["stand", [H], "", 14]] },
  { codename: "Teal Wren", lines: [
    ["flag", [TIE], "", 30], ["flag", [PER, SRC], "", 31], ["flag", [DIR], "", 22],
    ["stand", [H], "", 11], ["stand", [H], "", 10], ["stand", [H], "", 9],
    ["stand", [H], "", 15], ["flag", [TIE, SRC], "", 28], ["stand", [H], "", 8],
    ["stand", [H], "", 7], ["flag", [OWE, SRC], "", 26], ["flag", [SRC], "", 19],
    ["stand", [H], "", 6], ["flag", [SRC], "", 24]], budget: 900 },
];

(async () => {
  const runs = process.argv[2] ? JSON.parse(fs.readFileSync(process.argv[2], "utf8")) : RUNS;
  const out = [];
  for (const run of runs) {
    const t = boot({ search: "?test=1" });
    await t.ready();
    const S = t.S();
    S.tourSeen = true;
    t.click("go");
    if (run.codename) S.codename = run.codename;
    run.lines.forEach((l, k) => {
      const i = S.step - 3;
      t.click(l[0]);
      S.basis[i] = l[1].slice();
      const box = t.el("basiswords");
      if (box) box.value = l[2] || "";
      S.itemStart = Date.now() - (l[3] || 0) * 1000;
      t.click("lockin");
      if (k < run.lines.length - 1) {
        if (t.el("next")) t.click("next");
        else if (t.el("keepgoing")) t.click("keepgoing");
      }
    });
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
        basis_agrees: reason.right(i, 1), seconds: S.secs[i], words: S.words[i] || "",
      });
    }
    const parts = t.window.__BTM_TESTER.parts(run.budget === undefined ? undefined : run.budget);
    out.push({
      record: parts.text, included: parts.included,
      header: { version: "1.9.2", codename: S.codename, attempt_id: S.attemptId, case: "halyard",
                answered: facts.length, right: facts.filter((f) => f.outcome === "caught" || f.outcome === "cleared").length,
                points: S.points },
      lines: facts.slice(0, parts.included),
    });
  }
  process.stdout.write(JSON.stringify(out, null, 1));
})().catch((e) => { console.error(e.stack || e); process.exit(2); });
