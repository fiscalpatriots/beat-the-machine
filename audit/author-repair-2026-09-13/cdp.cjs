/* Minimal headless Chrome driver over the DevTools protocol, plus a static server.
   Node 18+ (global fetch and WebSocket). No packages. */
const http = require("http");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { spawn } = require("child_process");

const CHROME = process.env.CHROME ||
  ["C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
   "C:/Program Files/Google/Chrome/Application/chrome.exe",
   "/usr/bin/google-chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    .find((p) => { try { return fs.existsSync(p); } catch (e) { return false; } });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const TYPES = { ".html": "text/html", ".css": "text/css", ".js": "text/javascript", ".json": "application/json",
  ".png": "image/png", ".svg": "image/svg+xml", ".md": "text/plain" };

function serve(root) {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const u = decodeURIComponent(req.url.split("?")[0]);
      const file = path.join(root, u === "/" ? "index.html" : u);
      fs.readFile(file, (e, buf) => {
        if (e) { res.writeHead(404); res.end("not found"); return; }
        res.writeHead(200, { "content-type": TYPES[path.extname(file).toLowerCase()] || "application/octet-stream",
          "cache-control": "no-store" });
        res.end(buf);
      });
    });
    srv.listen(0, "127.0.0.1", () => resolve({ srv, port: srv.address().port }));
  });
}

function client(url) {
  const ws = new WebSocket(url);
  let id = 0;
  const wait = new Map();
  const listeners = [];
  ws.addEventListener("message", (e) => {
    const m = JSON.parse(e.data);
    if (m.id && wait.has(m.id)) {
      const x = wait.get(m.id); wait.delete(m.id);
      m.error ? x.rej(new Error(JSON.stringify(m.error))) : x.res(m.result);
    } else if (m.method) listeners.forEach((f) => f(m));
  });
  return {
    ready: new Promise((r) => ws.addEventListener("open", r)),
    on: (f) => listeners.push(f),
    send: (method, params) => {
      const i = ++id;
      return new Promise((res, rej) => { wait.set(i, { res, rej }); ws.send(JSON.stringify({ id: i, method, params: params || {} })); });
    },
    close: () => ws.close(),
  };
}

async function launch(tag) {
  if (!CHROME) throw new Error("no Chrome found; set CHROME to a Chrome or Edge executable");
  const port = 9400 + Math.floor(Math.random() * 400);
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), "sp-author-" + tag + "-"));
  const downloads = fs.mkdtempSync(path.join(os.tmpdir(), "sp-author-dl-"));
  const proc = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${profile}`,
    "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
  let list = [], ver = null;
  for (let i = 0; i < 60 && !list.length; i++) {
    await sleep(250);
    try {
      list = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).filter((t) => t.type === "page");
      ver = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
    } catch (e) {}
  }
  const b = client(ver.webSocketDebuggerUrl); await b.ready;
  await b.send("Browser.setDownloadBehavior", { behavior: "allow", downloadPath: downloads, eventsEnabled: true });
  const c = client(list[0].webSocketDebuggerUrl); await c.ready;
  await c.send("Page.enable"); await c.send("Runtime.enable");
  const errors = [];
  c.on((m) => {
    if (m.method === "Runtime.exceptionThrown") errors.push(m.params.exceptionDetails.exception
      ? m.params.exceptionDetails.exception.description : m.params.exceptionDetails.text);
    if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error")
      errors.push(m.params.args.map((a) => a.value || a.description).join(" "));
  });
  const ev = async (expr) => {
    const r = await c.send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(expr.slice(0, 80) + " -> " +
      (r.exceptionDetails.exception ? r.exceptionDetails.exception.description : r.exceptionDetails.text));
    return r.result.value;
  };
  const nav = async (url, readyExpr) => {
    await c.send("Page.navigate", { url });
    for (let i = 0; i < 80; i++) {
      await sleep(150);
      try { if (await ev(readyExpr || "document.readyState==='complete'")) return true; } catch (e) {}
    }
    throw new Error("page never became ready: " + url);
  };
  const width = (w) => c.send("Emulation.setDeviceMetricsOverride",
    { width: w, height: w < 700 ? 800 : 1000, deviceScaleFactor: 1, mobile: w < 700 });
  const downloadsNow = () => fs.readdirSync(downloads).filter((f) => !/\.crdownload$|\.tmp$/.test(f));
  const clearDownloads = () => fs.readdirSync(downloads).forEach((f) => fs.unlinkSync(path.join(downloads, f)));
  const shot = async (file) => {
    const r = await c.send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true });
    fs.writeFileSync(file, Buffer.from(r.data, "base64"));
  };
  const close = () => { try { c.close(); b.close(); } catch (e) {} proc.kill(); };
  return { ev, nav, width, downloads, downloadsNow, clearDownloads, shot, close, errors, send: c.send };
}

/* every element whose content is wider than its own box and could scroll, and the document */
const OVERFLOW = `(function(){
  var bad=[],all=document.querySelectorAll('body *');
  for(var i=0;i<all.length;i++){
    var e=all[i]; if(!e.clientWidth) continue;
    var cs=getComputedStyle(e);
    if(e.scrollWidth>e.clientWidth+1 && cs.overflowX!=='visible' && cs.overflowX!=='clip' && cs.overflowX!=='hidden')
      bad.push((e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className).split(' ')[0])+' '+e.scrollWidth+'>'+e.clientWidth);
    var r=e.getBoundingClientRect();
    if(r.width && r.right>document.documentElement.clientWidth+1 && cs.position!=='fixed'){
      var p=e.parentElement,clipped=false;
      while(p){var pc=getComputedStyle(p); if(pc.overflowX==='hidden'||pc.overflowX==='clip'||pc.overflowX==='auto'||pc.overflowX==='scroll'){clipped=true;break;} p=p.parentElement;}
      if(!clipped) bad.push('edge '+(e.id?'#'+e.id:e.tagName.toLowerCase()+'.'+String(e.className).split(' ')[0])+' right '+Math.round(r.right));
    }
  }
  var d=document.documentElement;
  return {doc:d.scrollWidth+'/'+d.clientWidth, clean:d.scrollWidth<=d.clientWidth && !bad.length, bad:bad.slice(0,12)};
})()`;

module.exports = { serve, launch, sleep, OVERFLOW, CHROME };
