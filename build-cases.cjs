/* build-cases.cjs
   Writes the two shared case definitions into index.html as an inline fallback.

   index.html fetches cases/halyard-v4.json and cases/brightwater-v6.json at load.
   On file:// and on any host that blocks the fetch, the fetch fails and the page
   falls back to the copy this script writes between the two BUILD markers, so the
   drill still runs from a folder on a laptop with no server.

   Run:  node build-cases.cjs
   The JSON files are the source of truth. Never hand-edit the generated block. */

var fs = require("fs");
var path = require("path");

var ROOT = __dirname;
var HTML = path.join(ROOT, "index.html");
var START = "/* BUILD:CASES-START";
var END = "/* BUILD:CASES-END */";

function load(name) {
  var p = path.join(ROOT, "cases", name);
  var raw = fs.readFileSync(p, "utf8");
  var obj = JSON.parse(raw);
  check(obj, name);
  return obj;
}

/* the checks that would otherwise only show up as a blank card in front of a player */
function check(c, name) {
  var need = ["version", "date", "company", "threshold", "ledger", "groups", "cards"];
  need.forEach(function (k) {
    if (!c[k]) throw new Error(name + ": missing " + k);
  });
  var byAcct = {};
  c.ledger.forEach(function (r) { byAcct[r[0]] = r; });
  c.cards.forEach(function (card) {
    var r = byAcct[card.acct];
    if (!r) throw new Error(name + ": card " + card.n + " points at account " + card.acct + ", which is not in the ledger");
    if (r[2] !== card.prior || r[3] !== card.current) {
      throw new Error(name + ": card " + card.n + " figures do not tie to the ledger for account " + card.acct);
    }
    if (card.key !== "flag" && card.key !== "stand") throw new Error(name + ": card " + card.n + " has key " + card.key);
    if (!card.why || !card.tell) throw new Error(name + ": card " + card.n + " is missing why or tell");
    /* the wrong face of the reveal reads truth and ask off the card, so a flag card without
       them would put an empty panel in front of a player who let that line through */
    if (card.key === "flag" && (!card.truth || !card.ask)) {
      throw new Error(name + ": card " + card.n + " is a flag card missing truth or ask");
    }
    /* the wrong face of a clean line reads over, which is what the player over-flagged against */
    if (card.key === "stand" && !card.over) {
      throw new Error(name + ": card " + card.n + " is a clean line missing over");
    }
    if (c.mode === "assessment") assessmentMemo(card, name);
  });
  checkBasis(c, name);
  if (c.mode === "assessment") {
    /* From brightwater-v4 onward every assessment line tests a named cause. A silent line has no cause
       to judge, so it belongs in the practice case and not in the scored one. */
    c.cards.forEach(function (card) {
      if (!card.memo) throw new Error(name + ": card " + card.n + " carries no memo sentence, and every assessment line has to name a cause");
      if (card.type === "no explanation") throw new Error(name + ": card " + card.n + " is a no-explanation line, which an assessment case no longer carries");
    });
  }
}

/* the basis key: the chips that are correct for a card. Anything outside it contradicts the key.
   A card the key lets stand carries the hold chip and nothing else, because a chip naming a
   defect contradicts a line that has none. */
var HOLD_CHIP = "the figure and reason hold";
var FLAG_CHIPS = ["figure does not tie", "direction wrong", "no source on file",
                  "wrong period", "wrong account", "nothing written where owed"];
function checkBasis(c, name) {
  c.cards.forEach(function (card) {
    var k = card.basisKey;
    if (!k || !k.length) throw new Error(name + ": card " + card.n + " has no basisKey");
    k.forEach(function (chip) {
      if (chip !== HOLD_CHIP && FLAG_CHIPS.indexOf(chip) === -1) {
        throw new Error(name + ": card " + card.n + " basisKey has \"" + chip + "\", which is not a chip the page offers");
      }
    });
    if (card.key === "stand") {
      if (k.length !== 1 || k[0] !== HOLD_CHIP) {
        throw new Error(name + ": card " + card.n + " is a stand and its basisKey has to be the hold chip alone");
      }
    } else if (k.indexOf(HOLD_CHIP) !== -1) {
      throw new Error(name + ": card " + card.n + " is a flag and its basisKey carries the hold chip");
    }
  });
}

/* An assessment memo is only allowed to state figures that tie, because the whole test is
   the cause. Every dollar amount and every percent in the sentence has to be one of the four
   figures the ledger row produces, and the direction word has to match the sign. */
function assessmentMemo(card, name) {
  if (!card.memo) return;
  var d = card.current - card.prior;
  var pct = (d / card.prior * 100).toFixed(1);
  var okMoney = [card.prior, card.current, Math.abs(d)].map(function (v) {
    return Math.round(v).toLocaleString("en-US");
  });
  (card.memo.match(/\$[\d,]+/g) || []).forEach(function (raw) {
    var m = raw.replace(/,+$/, "");
    if (okMoney.indexOf(m.slice(1)) === -1) {
      throw new Error(name + ": card " + card.n + " states " + m + ", which is not a figure account " + card.acct + " produces");
    }
  });
  (card.memo.match(/([\d.]+) percent/g) || []).forEach(function (m) {
    if (m.replace(" percent", "") !== pct) {
      throw new Error(name + ": card " + card.n + " states " + m + ", and the movement is " + pct + " percent");
    }
  });
  var up = /\b(rose|increased|grew|climbed)\b/i.test(card.memo);
  var down = /\b(fell|declined|eased|dropped|decreased)\b/i.test(card.memo);
  if (up && d < 0) throw new Error(name + ": card " + card.n + " reads as an increase and the account fell");
  if (down && d > 0) throw new Error(name + ": card " + card.n + " reads as a decrease and the account rose");
}

var one = load("halyard-v4.json");
var two = load("brightwater-v6.json");

var block =
  START + "  generated by build-cases.cjs, " + new Date().toISOString().slice(0, 10) + ".\n" +
  "   Source of truth: cases/" + one.version + ".json and cases/" + two.version + ".json.\n" +
  "   Used only when the fetch of those files fails, which is what happens on file://. */\n" +
  "var CASE1_FALLBACK = " + JSON.stringify(one) + ";\n" +
  "var CASE2_FALLBACK = " + JSON.stringify(two) + ";\n" +
  END;

var html = fs.readFileSync(HTML, "utf8");
var a = html.indexOf(START);
var b = html.indexOf(END);
if (a === -1 || b === -1) throw new Error("index.html is missing the BUILD:CASES markers");
html = html.slice(0, a) + block + html.slice(b + END.length);
fs.writeFileSync(HTML, html);

console.log("index.html fallback rewritten from " + one.version + " and " + two.version +
  " (" + one.cards.length + " + " + two.cards.length + " cards).");
