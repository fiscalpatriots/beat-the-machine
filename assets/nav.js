/* =============================================================================
   Second Pass — the shared header and footer, from one template.

   Any page that loads this script gets the same slim header at the top of the
   body and the same footer at the bottom. Nothing else has to be wired: the
   markup and the few rules it needs are both in here, so a page only adds

       <script src="assets/nav.js" defer></script>

   to its head. The tokens come from assets/second-pass.css when the page loads
   it; the fallbacks below keep the header readable if it does not.

   The link set is four words. A phone at 320 shows the same row the desktop
   shows, because a menu that hides four links is machinery the reader did not
   ask for. The two narrow breakpoints below pull the gaps in rather than wrap
   the row, and the row was measured at 320 with all four links on the line.

   The script also prints the skip link every page needs and points it at the
   page's main region, adopting <main> where a page has one and the outer
   container where it does not, marking that container as the main landmark if
   it is still a div, so a keyboard reaches the content in one tab without any
   page having to wire it.
   ============================================================================= */
(function () {
  'use strict';

  var PAGES = [
    { href: 'index.html',   label: 'Drill'   },
    { href: 'checker.html', label: 'Checker' },
    { href: 'review.html',  label: 'Review'  },
    { href: 'author.html',  label: 'Author'  }
  ];

  var FOOT = [
    { href: 'Second-Pass-Review-Protocol.pdf',   label: 'Protocol'          },
    { href: 'PROVENANCE.md',                     label: 'Provenance'        },
    { href: 'Second-Pass-Facilitator-Guide.pdf', label: 'Facilitator guide' },
    { href: 'https://github.com/fiscalpatriots/beat-the-machine', label: 'Code' }
  ];

  var CSS = [
    '#sp-nav{--sp-pad:20px;background:var(--paper,#f6f3ec);',
    '  border-bottom:1px solid var(--rule,#d9d3c5);}',
    '#sp-nav .in{max-width:1048px;margin:0 auto;padding:0 var(--sp-pad);',
    '  display:flex;align-items:center;gap:16px;min-height:46px;}',
    '#sp-nav .mark{font:600 15px/1.2 var(--face,Figtree,-apple-system,"Segoe UI",Arial,sans-serif);',
    '  letter-spacing:-.01em;color:var(--mason,#005239);text-decoration:none;white-space:nowrap;}',
    '#sp-nav .mark:hover{color:var(--mason,#005239);text-decoration:none;}',
    '#sp-nav nav{margin-left:auto;display:flex;align-items:center;gap:18px;}',
    '#sp-nav nav a{flex:0 0 auto;}',
    '#sp-nav nav a{font:500 14px/1.2 var(--face,Figtree,-apple-system,"Segoe UI",Arial,sans-serif);',
    '  color:var(--ink-soft,#5f6366);text-decoration:none;white-space:nowrap;',
    '  padding:13px 0;border-bottom:2px solid transparent;margin-bottom:-1px;}',
    '#sp-nav nav a:hover{color:var(--ink,#1a1a1a);}',
    '#sp-nav nav a[aria-current="page"]{color:var(--ink,#1a1a1a);font-weight:600;',
    '  border-bottom-color:var(--mason,#005239);}',
    '@media (max-width:430px){#sp-nav .in{gap:10px;padding:0 14px}#sp-nav nav{gap:12px}}',
    '@media (max-width:360px){#sp-nav .in{gap:8px;padding:0 12px}#sp-nav .mark{font-size:14px}',
    '  #sp-nav nav{gap:10px}#sp-nav nav a{font-size:13px}}',
    '#sp-foot{margin-top:56px;border-top:1px solid var(--rule,#d9d3c5);',
    '  background:var(--paper,#f6f3ec);}',
    '#sp-foot .in{max-width:1048px;margin:0 auto;padding:20px var(--sp-pad,20px) 30px;',
    '  font:400 14px/1.6 var(--face,Figtree,-apple-system,"Segoe UI",Arial,sans-serif);',
    '  color:var(--ink-soft,#5f6366);}',
    '#sp-foot p{margin:0 0 8px;}',
    '#sp-foot ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 20px;}',
    '#sp-foot a{color:var(--ink-soft,#5f6366);text-underline-offset:.18em;}',
    '#sp-foot a:hover{color:var(--ink,#1a1a1a);}',
    '@media (max-width:400px){#sp-foot .in{padding-left:14px;padding-right:14px}}',
    '#sp-skip{position:absolute;left:-9999px;top:0;z-index:99;}',
    '#sp-skip:focus{left:8px;top:8px;width:auto;height:auto;padding:10px 14px;',
    '  background:var(--mason,#005239);color:#fff;border-radius:8px;text-decoration:none;',
    '  font:600 14px/1.2 var(--face,Figtree,-apple-system,"Segoe UI",Arial,sans-serif);',
    '  outline:3px solid var(--gold,#ffc733);outline-offset:2px;}',
    '#sp-main:focus{outline:none}',
    /* On paper the chrome is noise, and the checker prints a summary sheet of
       its own with its own foot line. */
    '@media print{#sp-nav,#sp-foot,#sp-skip{display:none!important}}'
  ].join('');

  function here() {
    var f = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    return f === '' ? 'index.html' : f;
  }

  function link(item, current) {
    var a = document.createElement('a');
    a.href = item.href;
    a.textContent = item.label;
    if (item.href.toLowerCase() === current) a.setAttribute('aria-current', 'page');
    if (/^https?:/.test(item.href)) { a.target = '_blank'; a.rel = 'noopener'; }
    return a;
  }

  function build() {
    if (document.getElementById('sp-nav')) return;
    var current = here();

    var style = document.createElement('style');
    style.id = 'sp-chrome-css';
    style.textContent = CSS;
    document.head.appendChild(style);

    var main = document.querySelector('main') ||
               document.getElementById('app') ||
               document.getElementById('page');
    var skip = null;
    if (main) {
      if (!main.id) main.id = 'sp-main';
      if (!main.hasAttribute('tabindex')) main.setAttribute('tabindex', '-1');
      /* a page whose container is still a div gets the landmark anyway, so the
         skip link lands somewhere a screen reader can name */
      if (main.tagName !== 'MAIN' && !main.getAttribute('role')) main.setAttribute('role', 'main');
      skip = document.createElement('a');
      skip.id = 'sp-skip';
      skip.href = '#' + main.id;
      skip.textContent = 'Skip to the main content';
    }

    var head = document.createElement('header');
    head.id = 'sp-nav';
    var hin = document.createElement('div');
    hin.className = 'in';
    var mark = document.createElement('a');
    mark.className = 'mark';
    mark.href = 'review.html';
    mark.textContent = 'Second Pass';
    hin.appendChild(mark);
    var nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Second Pass');
    PAGES.forEach(function (p) { nav.appendChild(link(p, current)); });
    hin.appendChild(nav);
    head.appendChild(hin);
    document.body.insertBefore(head, document.body.firstChild);
    if (skip) document.body.insertBefore(skip, head);

    var foot = document.createElement('footer');
    foot.id = 'sp-foot';
    var fin = document.createElement('div');
    fin.className = 'in';
    var line = document.createElement('p');
    line.textContent = 'Built by Khaled Alkurd. A drill for the AI-native accounting student.';
    fin.appendChild(line);
    var ul = document.createElement('ul');
    FOOT.forEach(function (f) {
      var li = document.createElement('li');
      li.appendChild(link(f, ''));
      ul.appendChild(li);
    });
    fin.appendChild(ul);
    foot.appendChild(fin);
    document.body.appendChild(foot);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
