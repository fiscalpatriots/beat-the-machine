/* Full-page capture that stays under Chrome's 16,384px surface limit: the viewport is set to
   the segment height, the page is scrolled, and each segment is captured and saved as a part.
   stitch.py joins the parts. Used by sweep.cjs for any page taller than 12,000px. */
const fs = require("fs");
const { sleep } = require("../author-repair-2026-09-13/cdp.cjs");

async function tallShot(B, file, width, seg) {
  seg = seg || 3000;
  const m = await B.send("Page.getLayoutMetrics");
  const H = Math.ceil(m.cssContentSize.height);
  await B.send("Emulation.setDeviceMetricsOverride", { width, height: seg, deviceScaleFactor: 1, mobile: width < 700 });
  await sleep(300);
  const parts = [];
  for (let y = 0, k = 0; y < H; y += seg, k++) {
    await B.ev(`window.scrollTo(0,${y});true`);
    await sleep(220);
    const sy = await B.ev("window.scrollY");
    const h = Math.min(seg, H - y);
    /* the last segment cannot scroll a full viewport, so it is clipped from where the scroll landed */
    const r = await B.send("Page.captureScreenshot", { format: "png",
      clip: { x: 0, y: y, width, height: h, scale: 1 } });
    const part = file.replace(/\.png$/, `.part${String(k).padStart(2, "0")}.png`);
    fs.writeFileSync(part, Buffer.from(r.data, "base64"));
    parts.push({ part, y, h, sy });
  }
  await B.ev("window.scrollTo(0,0);true");
  await B.send("Emulation.setDeviceMetricsOverride", { width, height: width < 700 ? 800 : 1000, deviceScaleFactor: 1, mobile: width < 700 });
  fs.writeFileSync(file.replace(/\.png$/, ".parts.json"), JSON.stringify({ width, H, parts }));
  return { w: width, h: H, parts: parts.length };
}
module.exports = { tallShot };
