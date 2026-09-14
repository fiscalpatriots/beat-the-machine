/* Screenshot helper for the usability-by-eye lane. Reuses the CDP driver from the author repair lane.
   node shoot.cjs <root> <outdir> <spec.json>
   spec: [{name, url, width, dpr?, full?, prep?: js, ready?: js, clip?: {selector, pad} , wait?}] */
const fs = require("fs");
const path = require("path");
const { serve, launch, sleep, OVERFLOW } = require("../author-repair-2026-09-13/cdp.cjs");

async function fullShot(B, file, dpr) {
  const m = await B.send("Page.getLayoutMetrics");
  const w = Math.ceil(m.cssContentSize.width), h = Math.ceil(m.cssContentSize.height);
  const r = await B.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
    clip: { x: 0, y: 0, width: w, height: h, scale: 1 } });
  fs.writeFileSync(file, Buffer.from(r.data, "base64"));
  return { w, h };
}
async function setWidth(B, w, dpr) {
  await B.send("Emulation.setDeviceMetricsOverride", { width: w, height: w < 700 ? 800 : 1000, deviceScaleFactor: dpr || 1, mobile: w < 700 });
}
module.exports = { fullShot, setWidth };

if (require.main === module) (async () => {
  const [ROOT, OUTDIR, SPEC] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(SPEC, "utf8"));
  fs.mkdirSync(OUTDIR, { recursive: true });
  let base = null, srv = null;
  if (!/^https?:/.test(ROOT)) { const s = await serve(ROOT); srv = s.srv; base = `http://127.0.0.1:${s.port}/`; } else base = ROOT;
  const B = await launch("usab");
  const report = [];
  try {
    for (const s of spec) {
      await setWidth(B, s.width, s.dpr);
      await B.nav(base + s.url, s.ready || "document.readyState==='complete'");
      await B.ev("document.fonts ? document.fonts.ready.then(function(){return true}) : true");
      if (s.prep) { await B.ev(s.prep); }
      await sleep(s.wait || 400);
      const ov = await B.ev(OVERFLOW);
      const out = path.join(OUTDIR, s.name + ".png");
      const dims = await fullShot(B, out, s.dpr);
      let extra = null;
      if (s.measure) extra = await B.ev(s.measure);
      report.push({ name: s.name, width: s.width, dims, overflow: ov, extra });
      console.log(s.name, JSON.stringify(dims), ov.clean ? "clean" : JSON.stringify(ov.bad), extra ? JSON.stringify(extra) : "");
    }
  } catch (e) { console.error("ERR", e.message); }
  finally { B.close(); if (srv) srv.close(); }
  fs.writeFileSync(path.join(OUTDIR, "report.json"), JSON.stringify(report, null, 1));
  if (B.errors.length) console.log("page errors:", B.errors.slice(0, 10));
  process.exit(0);
})();
