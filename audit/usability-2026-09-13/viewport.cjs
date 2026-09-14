/* Viewport-only screenshots on a phone, where sticky bars really sit: the read screen, the
   explanation step and the checker's results, each at the top, the middle and the bottom.
   node viewport.cjs <root> <outdir> [width] */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep } = require("../author-repair-2026-09-13/cdp.cjs");
const D = require("./drive.cjs");
const [ROOT, OUTDIR, WS] = process.argv.slice(2);
const W = Number(WS || 375), H = 740;

(async () => {
  fs.mkdirSync(OUTDIR, { recursive: true });
  const { srv, port } = await serve(ROOT);
  const base = `http://127.0.0.1:${port}/`;
  const B = await launch("vp");
  const dr = D.drill(B, base);
  const shot = async (name) => {
    const r = await B.send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(path.join(OUTDIR, `${name}-${W}.png`), Buffer.from(r.data, "base64"));
  };
  const at = async (name, frac) => {
    await B.ev(`window.scrollTo(0,Math.round((document.documentElement.scrollHeight-innerHeight)*${frac}));true`);
    await sleep(350);
    await shot(name);
  };
  const stickyInfo = () => B.ev(`Array.prototype.filter.call(document.querySelectorAll('body *'),function(e){var p=getComputedStyle(e).position;return p==='sticky'||p==='fixed';}).map(function(e){var r=e.getBoundingClientRect();return (e.id||e.className||e.tagName)+' '+getComputedStyle(e).position+' top '+Math.round(r.top)+' h '+Math.round(r.height)+' visible '+(r.bottom>0&&r.top<innerHeight);})`);
  try {
    await B.send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: true });
    await dr.toRead(); await dr.tapRead(3);
    for (const [n, f] of [["read-top", 0], ["read-mid", 0.5], ["read-bottom", 1]]) { await at(n, f); console.log(n, JSON.stringify(await stickyInfo())); }
    await dr.goOn();
    await dr.playUntil((s, x) => s === x.l2);
    await dr.openCommit();
    for (const [n, f] of [["explain-mid", 0.55], ["explain-bottom", 1]]) { await at(n, f); console.log(n, JSON.stringify(await stickyInfo())); }
    await D.checkerRun(B, base);
    for (const [n, f] of [["checker-top", 0], ["checker-results", 0.12], ["checker-bottom", 1]]) { await at(n, f); console.log(n, JSON.stringify(await stickyInfo())); }
  } catch (e) { console.log("ERR", e.message); }
  finally { B.close(); srv.close(); process.exit(0); }
})();
