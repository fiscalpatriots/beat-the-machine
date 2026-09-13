#!/usr/bin/env node
/* A stand-in for the Apps Script web app, for proving the client path on this machine.
 *
 * It answers the same three shapes Code.gs answers: a health check on GET, a receipt on POST,
 * and the same receipt with no second row when the same attempt id comes back. It also serves
 * the repository, so index.html can be opened from it, and it swallows a POST to /formResponse
 * so the form fallback can be exercised without a single row reaching Google.
 *
 *   node receipts/mock-endpoint.cjs            starts on 8899
 *   node receipts/mock-endpoint.cjs --port 9000 --fail   every receipt POST answers a 500
 *
 * Then open, with test mode on so nothing can reach the live form:
 *   http://localhost:8899/index.html?test=1&receipt=http%3A%2F%2Flocalhost%3A8899%2Freceipt
 *      &form=http%3A%2F%2Flocalhost%3A8899%2FformResponse
 *
 * Rows are held in memory and printed as they arrive. Stopping the server forgets them, which
 * is the point: this is a proof of the client path and never a place results are kept.
 */
"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const args = process.argv.slice(2);
const PORT = Number(pick("--port", "8899"));
const FAIL = args.includes("--fail");
/* --save <dir> writes each record it accepts as <dir>/<attempt id>.json, which is how a
   receipts CSV can be built for testing receipts-to-form-csv.py without Google in the loop */
const SAVE = pick("--save", "");
const ROOT = path.resolve(__dirname, "..");

function pick(flag, fallback) {
  const i = args.indexOf(flag);
  return (i >= 0 && args[i + 1]) ? args[i + 1] : fallback;
}

/* attempt id to {receipt, storedAt}, the whole store */
const rows = new Map();

const TYPES = {
  ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".cjs": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".css": "text/css; charset=utf-8", ".png": "image/png", ".jpg": "image/jpeg",
  ".svg": "image/svg+xml", ".ico": "image/x-icon", ".woff2": "font/woff2",
  ".txt": "text/plain; charset=utf-8", ".xml": "application/xml; charset=utf-8"
};

/* The same canonical form Code.gs hashes: keys sorted at every level. */
function canonical(v) {
  if (v === null || typeof v !== "object") return JSON.stringify(v === undefined ? null : v);
  if (Array.isArray(v)) return "[" + v.map(canonical).join(",") + "]";
  return "{" + Object.keys(v).sort()
    .map(k => JSON.stringify(k) + ":" + canonical(v[k])).join(",") + "}";
}

/* The same four checks Code.gs makes. */
function validate(r) {
  if (!r || typeof r !== "object") return "record is not an object";
  if (!r.attempt || typeof r.attempt !== "object") return "no attempt block";
  if (!r.attempt.id) return "no attempt id";
  if (!r.attempt.productVersion) return "no product version";
  if (!r.attempt.caseId) return "no case id";
  if (!Array.isArray(r.responses)) return "no responses array";
  const one = (r.scoring && r.scoring.roundOne && r.scoring.roundOne.of) || 0;
  const two = (r.scoring && r.scoring.roundTwo && r.scoring.roundTwo.of) || 0;
  if (r.responses.length !== 19 && r.responses.length !== one + two) {
    return `expected 19 responses or the case's ${one + two}, got ${r.responses.length}`;
  }
  return "";
}

function json(res, obj, status) {
  const body = JSON.stringify(obj);
  res.writeHead(status || 200, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Content-Length": Buffer.byteLength(body)
  });
  res.end(body);
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const route = url.pathname;

  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    });
    return res.end();
  }

  /* the health check */
  if (route === "/receipt" && req.method === "GET") {
    return json(res, { ok: true, service: "second-pass-receipts", version: "mock" });
  }

  /* the form, swallowed. The page only reads the hidden frame's load event, so a 200 with a
     blank page is the same signal Google gives it. */
  if (route === "/formResponse") {
    let n = 0;
    req.on("data", c => { n += c.length; });
    req.on("end", () => {
      console.log(`form post swallowed, ${n} bytes`);
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      res.end("<!doctype html><title>ok</title>form post received by the mock");
    });
    return;
  }

  if (route === "/receipt" && req.method === "POST") {
    let body = "";
    req.on("data", c => { body += c; });
    req.on("end", () => {
      if (FAIL) {
        console.log("receipt POST refused on purpose");
        res.writeHead(500, { "Access-Control-Allow-Origin": "*" });
        return res.end("the mock is in fail mode");
      }
      let record;
      try { record = JSON.parse(body); } catch (e) { return json(res, { ok: false, error: "body is not JSON" }); }
      if (record && record.record && typeof record.record === "object") record = record.record;
      const problem = validate(record);
      if (problem) { console.log("rejected: " + problem); return json(res, { ok: false, error: problem }); }

      const id = String(record.attempt.id);
      if (SAVE) {
        try {
          fs.mkdirSync(SAVE, { recursive: true });
          fs.writeFileSync(path.join(SAVE, id + ".json"), body);
        } catch (e) { console.log("could not save the body: " + e.message); }
      }
      if (rows.has(id)) {
        const was = rows.get(id);
        console.log(`repeat of ${id}, same receipt ${was.receipt.slice(0, 12)}, no second row`);
        return json(res, { ok: true, receipt: was.receipt, storedAt: was.storedAt, duplicate: true });
      }
      const receipt = crypto.createHash("sha256").update(canonical(record), "utf8").digest("hex");
      const storedAt = new Date().toISOString();
      rows.set(id, { receipt, storedAt });
      console.log(`stored ${id} as ${receipt.slice(0, 12)} at ${storedAt}, ${body.length} bytes, ` +
                  `${record.responses.length} responses, rows now ${rows.size}`);
      return json(res, { ok: true, receipt, storedAt, duplicate: false });
    });
    return;
  }

  if (route === "/rows") return json(res, { ok: true, rows: [...rows.entries()] });

  /* everything else is the repository, so the page can be opened from here */
  const file = path.join(ROOT, decodeURIComponent(route === "/" ? "/index.html" : route));
  if (!file.startsWith(ROOT) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    res.writeHead(404, { "Content-Type": "text/plain" });
    return res.end("not here");
  }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});

server.listen(PORT, () => {
  console.log(`mock receipts endpoint on http://localhost:${PORT}/receipt${FAIL ? " (fail mode)" : ""}`);
  console.log(`the repository is served from http://localhost:${PORT}/index.html`);
});
