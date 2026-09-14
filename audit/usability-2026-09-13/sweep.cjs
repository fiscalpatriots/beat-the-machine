/* Full-page screenshots of every page and state at six widths, with in-page checks.
   node sweep.cjs <root> <outdir> [widths comma list] [states comma list]
   States: review, landing, read, halyard, kestrel, explain, end, checker-empty, checker-run,
   author-empty, author-read, 404. Test mode throughout, so the drill posts nothing. */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep } = require("../author-repair-2026-09-13/cdp.cjs");
const { fullShot, setWidth } = require("./shoot.cjs");
const { tallShot } = require("./tall.cjs");
const D = require("./drive.cjs");
const CHECKS = fs.readFileSync(path.join(__dirname, "checks.js"), "utf8");

const [ROOT, OUTDIR, WL, SL] = process.argv.slice(2);
const WIDTHS = (WL || "320,375,768,1024,1280,1600").split(",").map(Number);
const ALL = ["review", "landing", "read", "halyard", "kestrel", "explain", "end", "checker-empty", "checker-run", "author-empty", "author-read", "404"];
const STATES = SL ? SL.split(",") : ALL;

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const { srv, port } = await serve(ROOT);
  const base = `http://127.0.0.1:${port}/`;
  const B = await launch("sweep");
  const dr = D.drill(B, base);
  const report = {};
  const snap = async (state, w) => {
    await B.ev("document.fonts.ready.then(function(){return true})");
    await sleep(250);
    const file = path.join(OUTDIR, `${state}-${w}.png`);
    const checks = await B.ev(CHECKS);
    /* lazy images: force them to load before the shot */
    await B.ev("Array.prototype.forEach.call(document.querySelectorAll('img[loading=lazy]'),function(i){i.loading='eager';});Promise.all(Array.prototype.map.call(document.images,function(i){return i.complete?1:new Promise(function(r){i.onload=i.onerror=r;});})).then(function(){return true})");
    const lm = await B.send("Page.getLayoutMetrics");
    const dims = lm.cssContentSize.height > 12000 ? await tallShot(B, file, w) : await fullShot(B, file);
    report[`${state}-${w}`] = { dims, checks };
    const flag = checks.overflow.length || checks.clipped.length || checks.small.length || checks.images.some((x) => /SQUASHED/.test(x));
    console.log(`${state}-${w}`, dims.w + "x" + dims.h, checks.doc, flag ? JSON.stringify({ o: checks.overflow, c: checks.clipped, s: checks.small, i: checks.images.filter((x) => /SQUASHED/.test(x)) }) : "clean");
  };
  try {
    for (const w of WIDTHS) {
      await setWidth(B, w, 1);
      for (const s of STATES) {
        try {
          if (s === "review") { await B.nav(base + "review.html"); await snap(s, w); }
          else if (s === "404") { await B.nav(base + "404.html"); await snap(s, w); }
          else if (s === "landing") { await dr.landing(); await snap(s, w); }
          else if (s === "read") { await dr.toRead(); await dr.tapRead(3); await B.ev("window.scrollTo(0,0);true"); await snap(s, w); }
          else if (s === "halyard") { await dr.toRead(); await dr.tapRead(3); await dr.goOn(); await dr.playUntil((st) => st === 3); await snap(s, w); }
          else if (s === "kestrel") { await dr.toRead("kestrel"); await dr.tapRead(3); await dr.goOn(); await dr.playUntil((st) => st === 3); await snap(s, w); }
          else if (s === "explain" || s === "end") {
            if (s === "explain" || !STATES.includes("explain")) { await dr.toRead(); await dr.tapRead(3); await dr.goOn(); }
            if (s === "explain") {
              await dr.playUntil((st, x) => st === x.l2);
              await dr.openCommit();
              await B.ev("window.scrollTo(0,0);true");
              await snap(s, w);
            } else {
              await dr.playUntil((st, x) => st !== 92 && st >= x.done);
              await B.ev("window.scrollTo(0,0);true");
              await snap(s, w);
            }
          }
          else if (s === "checker-empty") { await D.checkerEmpty(B, base); await snap(s, w); }
          else if (s === "checker-run") { await D.checkerRun(B, base); await snap(s, w); }
          else if (s === "author-empty") { await D.authorEmpty(B, base); await snap(s, w); }
          else if (s === "author-read") { await D.authorRead(B, base); await snap(s, w); }
        } catch (e) { console.log("ERR", s, w, e.message); report[`${s}-${w}`] = { error: e.message }; }
      }
    }
  } finally {
    B.close(); srv.close();
    fs.writeFileSync(path.join(OUTDIR, "checks.json"), JSON.stringify(report, null, 1));
    if (B.errors.length) console.log("page errors:", JSON.stringify(B.errors.slice(0, 8)));
    process.exit(0);
  }
})();
