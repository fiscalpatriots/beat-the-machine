/* A browserless harness for index.html, used by tests/run-tester-record-tests.cjs and
 * tests/tester-record-emit.cjs.
 *
 * The drill is one HTML file with no build step, so the harness lifts the script out of it and
 * runs it in a vm against a document stub, the way tests/run-checker-tests.cjs runs checker.html.
 * An element the page writes into innerHTML with an id becomes findable by getElementById, and an
 * id the page never wrote is null, so a guard such as wireActions()'s check for #sendres behaves
 * as it does in a browser.
 *
 * Every way the page could reach the network is a spy: fetch answers the case files from disk and
 * records each call with its method, and XMLHttpRequest, navigator.sendBeacon, WebSocket,
 * EventSource, Image and form.submit() record any use. Nothing leaves the process.
 *
 * Options:
 *   search    the address query, for example "?test=1"
 *   prefill   {base, param} written into FEEDBACK_PREFILL_BASE and FEEDBACK_PREFILL_PARAM before
 *             the script runs, the way Khaled pastes them into the page
 *   session   a sessionStorage object to start from
 */
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = path.resolve(__dirname, "..");

function pageScript(prefill) {
  const html = fs.readFileSync(path.join(ROOT, "index.html"), "utf8");
  const m = html.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);
  if (!m) throw new Error("index.html carries no closing script block");
  let script = m[1];
  if (prefill) {
    const swap = (name, value) => {
      const re = new RegExp("var " + name + ' = "[^"]*";');
      if (!re.test(script)) throw new Error("index.html carries no " + name + " constant");
      script = script.replace(re, "var " + name + " = " + JSON.stringify(value) + ";");
    };
    swap("FEEDBACK_PREFILL_BASE", prefill.base || "");
    swap("FEEDBACK_PREFILL_PARAM", prefill.param || "");
  }
  const body = html.slice(html.indexOf("<body>"), html.indexOf("<script>"));
  return { script, body };
}

function decodeAttr(s) {
  return String(s).replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
}

function makeDom(staticBody) {
  const byId = new Map();
  const net = [];

  class ClassList {
    constructor() { this.set = new Set(); }
    add(...c) { c.forEach((x) => this.set.add(x)); }
    remove(...c) { c.forEach((x) => this.set.delete(x)); }
    toggle(c, on) { const want = on === undefined ? !this.set.has(c) : !!on; if (want) this.set.add(c); else this.set.delete(c); return want; }
    contains(c) { return this.set.has(c); }
  }

  class Element {
    constructor(tag, id) {
      this.tagName = String(tag || "div").toUpperCase();
      this.id = id || "";
      this.attrs = {};
      this.style = { setProperty() {}, removeProperty() {} };
      this.classList = new ClassList();
      this.children = [];
      this.parentNode = null;
      this.listeners = {};
      this._html = "";
      this._owned = [];
      this.textContent = "";
      this.value = "";
      this.hidden = false;
      this.offsetHeight = 0; this.offsetWidth = 0; this.scrollHeight = 0; this.clientWidth = 0;
    }
    get innerHTML() { return this._html; }
    set innerHTML(v) {
      this._html = String(v);
      /* the old markup goes, and with it every id written inside it at any depth */
      const purge = (el) => {
        el._owned.forEach((id) => {
          const child = byId.get(id);
          if (child && child._owner === el) { byId.delete(id); purge(child); }
        });
        el._owned = [];
      };
      purge(this);
      this.children = [];
      const re = /<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*?)\bid="([^"]+)"([^>]*)>/g;
      let m;
      while ((m = re.exec(this._html))) {
        const el = new Element(m[1], m[3]);
        el._owner = this;
        const attrs = (m[2] + " " + m[4]);
        const ar = /([a-zA-Z_:][-a-zA-Z0-9_:.]*)="([^"]*)"/g;
        let a;
        while ((a = ar.exec(attrs))) el.attrs[a[1]] = decodeAttr(a[2]);
        el.attrs.id = m[3];
        if (el.attrs.class) el.attrs.class.split(/\s+/).forEach((c) => c && el.classList.add(c));
        byId.set(m[3], el);
        this._owned.push(m[3]);
      }
    }
    get className() { return Array.from(this.classList.set).join(" "); }
    set className(v) { this.classList = new ClassList(); String(v).split(/\s+/).forEach((c) => c && this.classList.add(c)); }
    get href() { return this.attrs.href || ""; }
    set href(v) { this.attrs.href = String(v); }
    setAttribute(k, v) { this.attrs[k] = String(v); if (k === "id") { this.id = String(v); byId.set(this.id, this); } }
    getAttribute(k) { return Object.prototype.hasOwnProperty.call(this.attrs, k) ? this.attrs[k] : null; }
    removeAttribute(k) { delete this.attrs[k]; }
    hasAttribute(k) { return Object.prototype.hasOwnProperty.call(this.attrs, k); }
    appendChild(e) {
      this.children.push(e);
      e.parentNode = this;
      if (e.id) byId.set(e.id, e);
      return e;
    }
    insertBefore(e) { return this.appendChild(e); }
    removeChild(e) { const i = this.children.indexOf(e); if (i > -1) this.children.splice(i, 1); return e; }
    remove() { if (this.id && byId.get(this.id) === this) byId.delete(this.id); if (this.parentNode) this.parentNode.removeChild(this); }
    get firstChild() { return this.children[0] || null; }
    querySelector() { return null; }
    querySelectorAll() { return []; }
    closest(sel) { return sel === "#" + this.id ? this : null; }
    contains(e) { return e === this; }
    addEventListener(t, fn) { (this.listeners[t] = this.listeners[t] || []).push(fn); }
    removeEventListener(t, fn) { const l = this.listeners[t] || []; const i = l.indexOf(fn); if (i > -1) l.splice(i, 1); }
    dispatch(t, ev) { (this.listeners[t] || []).slice().forEach((fn) => fn.call(this, ev || { type: t, target: this, preventDefault() {}, stopPropagation() {} })); }
    getBoundingClientRect() { return { top: 0, left: 0, right: 0, bottom: 0, width: 0, height: 0 }; }
    focus() {} blur() {} scrollIntoView() {} select() {} click() {}
    submit() { net.push({ kind: "form.submit", method: (this.method || "GET").toUpperCase(), url: this.action || "" }); }
    animate() { return { finished: Promise.resolve(), cancel() {} }; }
  }

  const docListeners = {};
  const body = new Element("body");
  const document = {
    body,
    documentElement: new Element("html"),
    hidden: false,
    activeElement: null,
    fonts: { ready: Promise.resolve() },
    getElementById: (id) => byId.get(id) || null,
    createElement: (t) => new Element(t),
    createTextNode: (t) => ({ textContent: t }),
    querySelector: () => null,
    querySelectorAll: () => [],
    execCommand: () => true,
    addEventListener: (t, fn) => { (docListeners[t] = docListeners[t] || []).push(fn); },
    removeEventListener: (t, fn) => { const l = docListeners[t] || []; const i = l.indexOf(fn); if (i > -1) l.splice(i, 1); },
  };
  /* the static elements of the page body, so getElementById finds #screen, #testband and the rest */
  const holder = new Element("div");
  holder.innerHTML = staticBody;
  document.dispatch = (t, ev) => { (docListeners[t] || []).slice().forEach((fn) => fn(ev)); };
  return { document, byId, net, Element };
}

function boot(opts) {
  opts = opts || {};
  const { script, body } = pageScript(opts.prefill);
  const dom = makeDom(body);
  const { document, net } = dom;
  const store = Object.assign({}, opts.session || {});
  const sessionStorage = {
    getItem: (k) => (Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: (k) => { delete store[k]; },
  };
  const localStorage = { getItem: () => null, setItem() {}, removeItem() {} };
  const errors = [];

  function fetchSpy(u, init) {
    const method = String((init && init.method) || "GET").toUpperCase();
    net.push({ kind: "fetch", method, url: String(u) });
    const file = path.join(ROOT, String(u).split("?")[0]);
    if (method !== "GET" || !fs.existsSync(file)) return Promise.resolve({ ok: false, status: 404, json: () => Promise.reject(new Error("404")) });
    const text = fs.readFileSync(file, "utf8");
    return Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve(JSON.parse(text)), text: () => Promise.resolve(text) });
  }
  function XHRSpy() { this.open = (m, u) => { this._m = m; this._u = u; }; this.setRequestHeader = () => {}; this.send = () => { net.push({ kind: "xhr", method: String(this._m).toUpperCase(), url: String(this._u) }); }; }
  function WSSpy(u) { net.push({ kind: "websocket", method: "WS", url: String(u) }); this.send = () => {}; this.close = () => {}; }
  function ESSpy(u) { net.push({ kind: "eventsource", method: "GET", url: String(u) }); this.close = () => {}; }
  function ImageSpy() { let src = ""; Object.defineProperty(this, "src", { get: () => src, set: (v) => { src = String(v); net.push({ kind: "image", method: "GET", url: src }); } }); }

  const timers = [];
  const window = {
    location: { search: opts.search || "", href: "https://fiscalpatriots.github.io/beat-the-machine/" + (opts.search || ""), pathname: "/beat-the-machine/" },
    sessionStorage, localStorage,
    scrollTo() {}, scrollBy() {}, print() {},
    pageYOffset: 0, innerHeight: 900, innerWidth: 1280,
    matchMedia: () => ({ matches: false, addEventListener() {}, removeEventListener() {} }),
    getComputedStyle: () => ({ getPropertyValue: () => "", paddingTop: "0px", paddingBottom: "0px" }),
    addEventListener() {}, removeEventListener() {},
    requestAnimationFrame: (fn) => { timers.push(fn); return timers.length; },
    cancelAnimationFrame() {},
    fetch: fetchSpy,
  };
  const navigator = { sendBeacon: (u) => { net.push({ kind: "beacon", method: "POST", url: String(u) }); return true; }, userAgent: "harness" };
  const ctx = vm.createContext({
    window, document, navigator, sessionStorage, localStorage,
    fetch: fetchSpy, XMLHttpRequest: XHRSpy, WebSocket: WSSpy, EventSource: ESSpy, Image: ImageSpy,
    Blob: function Blob() {}, URL: { createObjectURL: () => "blob:harness", revokeObjectURL() {} },
    setTimeout: (fn) => { timers.push(fn); return timers.length; }, clearTimeout() {},
    setInterval: () => 0, clearInterval() {},
    requestAnimationFrame: window.requestAnimationFrame, cancelAnimationFrame() {},
    console: { log() {}, info() {}, warn: (...a) => errors.push(a.join(" ")), error: (...a) => errors.push(a.join(" ")) },
    Date, JSON, Math, RegExp, String, Number, Array, Object, Boolean, Promise, Error, TypeError, URIError,
    isFinite, isNaN, parseInt, parseFloat, encodeURIComponent, decodeURIComponent, encodeURI, decodeURI,
  });
  window.document = document;
  window.navigator = navigator;
  vm.runInContext(script, ctx, { filename: "index.html" });

  /* boot() runs once the case files answer, a few promise turns after the script */
  async function ready() {
    for (let i = 0; i < 50 && !window.__BTM_TESTER; i++) await new Promise((r) => setImmediate(r));
    if (!window.__BTM_TESTER) throw new Error("index.html never booted in the harness: " + errors.join("; "));
    return api;
  }
  const screen = () => document.getElementById("screen");
  const api = {
    window, document, net, errors, store, dom,
    ready,
    S: () => window.__BTM,
    cards: () => window.__BTM_CARDS,
    steps: () => window.__BTM_STEPS(),
    go: (n) => window.__BTM_GO(n),
    screenHtml: () => (screen() ? screen().innerHTML : ""),
    el: (id) => document.getElementById(id),
    click: (id) => {
      const el = document.getElementById(id);
      if (!el) throw new Error("no #" + id + " on the screen");
      const ev = { type: "click", target: el, preventDefault() {}, stopPropagation() {} };
      document.dispatch("click", ev);
      el.dispatch("click", ev);
      return el;
    },
    /* the href the page wrote into the feedback button, decoded the way a browser reads it */
    feedbackHref: () => {
      const el = document.getElementById("feedbackform");
      return el ? el.getAttribute("href") : null;
    },
  };
  return api;
}

module.exports = { boot, ROOT };
