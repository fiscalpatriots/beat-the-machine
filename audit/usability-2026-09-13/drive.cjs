/* States of the four pages, driven by clicks in test mode. Shared by sweep.cjs and crops.cjs. */
const { sleep } = require("../author-repair-2026-09-13/cdp.cjs");
const READY_DRILL = "!!(window.__BTM_CASES&&window.__BTM&&document.getElementById('screen')&&document.getElementById('screen').children.length)";

function drill(B, base) {
  const ev = B.ev;
  const url = (c) => base + "index.html?test=1&case=" + (c || "halyard");
  return {
    async landing(c) {
      await B.nav(url(c), READY_DRILL);
      await ev("sessionStorage.clear();localStorage.removeItem('btm.owncase.v1');true");
      await B.nav(url(c), READY_DRILL); await sleep(200);
    },
    async toRead(c) {
      await this.landing(c);
      await ev("document.getElementById('go').click();true"); await sleep(150);
      await ev("document.getElementById('noticego').click();true"); await sleep(150);
      await ev("var i=document.getElementById('cn');i.value='Silver Ledger';i.dispatchEvent(new Event('input',{bubbles:true}));" +
        "if(!document.querySelector('#orgs .chip.on')) document.querySelector('#orgs .chip').click();document.getElementById('next').click();true");
      await sleep(250);
      await ev("window.scrollTo(0,0);true");
    },
    async tapRead(n) {
      await ev(`(function(){var c=document.querySelectorAll('#prepicks .chip');[1,4,9,12].slice(0,${n || 3}).forEach(function(k){if(c[k]) c[k].click();});return true;})()`);
      await sleep(150);
    },
    async goOn() {
      await ev(`(function(){var b=Array.prototype.filter.call(document.querySelectorAll('[data-precont]'),function(b){var r=b.getBoundingClientRect();return r.width>0&&r.height>0;})[0];if(b) b.click();return !!b;})()`);
      await sleep(250); await ev("window.scrollTo(0,0);true");
    },
    step: () => ev("__BTM.step"),
    steps: () => ev("__BTM_STEPS()"),
    /* play until stop(s, st) is true; calls follow the key except round one lines 2 and 5 */
    async playUntil(stop) {
      const st = await ev("__BTM_STEPS()");
      let guard = 0;
      while (guard++ < 400) {
        const s = await ev("__BTM.step");
        if (await stop(s, st)) return s;
        if (s === 92) { await ev("document.getElementById('r2done').click();true"); await sleep(120); continue; }
        if (s >= st.done) return s;
        if (s === st.bridge) { await ev("document.getElementById('r2go').click();true"); await sleep(120); continue; }
        if (await ev("!!document.getElementById('next')")) { await ev("document.getElementById('next').click();true"); await sleep(90); continue; }
        const round = s >= st.l2 ? 2 : 1, i = round === 2 ? s - st.l2 : s - 3;
        const card = await ev(`(${round}===2?__BTM_CARDS2:__BTM_CARDS)[${i}]`);
        let want = card.key;
        if (round === 1 && (i === 1 || i === 4)) want = card.key === "flag" ? "stand" : "flag";
        await ev(`(function(){var b=document.getElementById(${JSON.stringify(want)});if(b) b.click();return true;})()`);
        await sleep(80);
        await ev(`(function(){var chips=Array.prototype.slice.call(document.querySelectorAll('#commit .chip'));
          var key=${JSON.stringify(card.basisKey || [])};
          var hit=chips.filter(function(x){return key.indexOf(x.textContent.trim())>-1;})[0]||chips[0];if(hit) hit.click();
          Array.prototype.forEach.call(document.querySelectorAll('#screen textarea.explain'),function(t,k){
            t.value=['The invoice on file dates the charge to May.','A May charge booked in June moves the period.','Ask for the accrual schedule.'][k];
            t.dispatchEvent(new Event('input',{bubbles:true}));});
          var l=document.getElementById('lockin');if(l) l.click();return true;})()`);
        await sleep(120);
      }
    },
    /* on a call card, choose a call and a basis chip without locking, so the commit area shows */
    async openCommit() {
      await ev(`(function(){var b=document.getElementById('flag')||document.getElementById('stand');if(b) b.click();return true;})()`);
      await sleep(120);
      await ev(`(function(){var c=document.querySelector('#commit .chip');if(c) c.click();return true;})()`);
      await sleep(120);
    },
  };
}

async function checkerEmpty(B, base) {
  await B.nav(base + "checker.html", "!!(window.__secondPass&&document.getElementById('run'))");
  await B.ev("sessionStorage.clear();localStorage.clear();true");
  await B.nav(base + "checker.html", "!!(window.__secondPass&&document.getElementById('run'))");
  await sleep(200);
}
async function checkerRun(B, base) {
  await checkerEmpty(B, base);
  await B.ev("document.getElementById('loadled').click();document.getElementById('loadmemo').click();true");
  await sleep(150);
  await B.ev("document.getElementById('run').click();true");
  await sleep(1200);
  await B.ev("window.scrollTo(0,0);true");
}
async function authorEmpty(B, base) {
  await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
  await B.ev("localStorage.clear();sessionStorage.clear();true");
  await B.nav(base + "author.html", "!!(window.__SPA&&window.SecondPassCore)");
  await sleep(200);
}
async function authorRead(B, base) {
  await authorEmpty(B, base);
  await B.ev("document.getElementById('loadsample').click();true"); await sleep(150);
  await B.ev("document.getElementById('read').click();true"); await sleep(500);
  await B.ev("window.scrollTo(0,0);true");
}
module.exports = { drill, checkerEmpty, checkerRun, authorEmpty, authorRead, READY_DRILL };
