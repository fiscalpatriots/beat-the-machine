/* node measure.cjs <root> <url> <width> <js-expression> */
const { serve, launch, sleep } = require("../author-repair-2026-09-13/cdp.cjs");
const { setWidth } = require("./shoot.cjs");
(async () => {
  const [ROOT, URL, W, EXPR] = process.argv.slice(2);
  const { srv, port } = await serve(ROOT);
  const B = await launch("meas");
  try {
    await setWidth(B, +W, 1);
    await B.nav(`http://127.0.0.1:${port}/` + URL);
    await B.ev("document.fonts.ready.then(function(){return true})");
    await sleep(300);
    console.log(JSON.stringify(await B.ev(EXPR), null, 1));
  } catch (e) { console.error(e.message); }
  B.close(); srv.close(); process.exit(0);
})();
