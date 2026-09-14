/* =============================================================================
   Second Pass — the ledger and memo reader, shared.

   These are the parsing and figure-checking functions the checker runs. They were
   COPIED VERBATIM out of checker.html on 13 September 2026 (lines 501-504,
   513-1490, 1591-1614 and 2092-2159 of that file) so author.html can run the same
   four mechanical checks on a pasted ledger and memo without a second, drifting
   implementation of the same reader.

   checker.html still carries its own copy inline, because its regression suite
   lifts the script out of the page. The two copies are held identical: the suite,
   node tests/run-checker-tests.cjs, compares every function this file shares with
   checker.html and fails on any difference. The reader was brought back into line
   with the page on 13 September 2026, after the third review, when the page's
   no-change, multiplier, fraction and digit rules were added. A fix made in one
   copy has to be made in the other before the suite passes.

   Nothing in this file touches the DOM, reads a global or stores anything.
   ============================================================================= */
(function (root) {
  "use strict";
    /* ---- from checker.html 501-504 ---- */
  function nowMs(){try{return Date.now();}catch(e){return 0;}}
  /* A run is instant on anything a student is likely to paste. If one ever takes
     longer than a tenth of a second, a line is drawn across the top of the page
     after the fact; below that, nothing flickers. */

    /* ---- from checker.html 513-1490: money through colChoice ---- */
  function money(v){
    if(v==null||!isFinite(v))return "n/a";
    var neg=v<0,a=Math.abs(v);
    var s=(Math.round(a*100)/100).toFixed(Math.abs(a-Math.round(a))<0.005?0:2);
    s=s.replace(/\B(?=(\d{3})+(?!\d))/g,",");
    return (neg?"-$":"$")+s;
  }
  function pctTxt(v){
    if(v==null||!isFinite(v))return "n/a";
    return (Math.round(v*10)/10).toFixed(1)+"%";
  }
  function parseNum(s){
    if(s==null)return NaN;
    var t=String(s).trim();
    if(!t)return NaN;
    var neg=false;
    if(/^\(.*\)$/.test(t)){neg=true;t=t.slice(1,-1);}
    t=t.replace(/[$ \s,]/g,"").replace(/%$/,"");
    if(t.charAt(0)==="-"){neg=!neg;t=t.slice(1);}
    else if(t.charAt(0)==="+"){t=t.slice(1);}
    if(!/^\d*\.?\d+$/.test(t))return NaN;
    var v=parseFloat(t);
    if(!isFinite(v))return NaN;
    return neg?-v:v;
  }
  function splitFields(line){
    var out=[],cur="",q=false,i,ch;
    if(line.indexOf("\t")>-1){out=line.split("\t");}
    else{
      for(i=0;i<line.length;i++){
        ch=line.charAt(i);
        if(ch==='"'){ if(q&&line.charAt(i+1)==='"'){cur+='"';i++;} else q=!q; }
        else if(ch===","&&!q){out.push(cur);cur="";}
        else cur+=ch;
      }
      out.push(cur);
    }
    out=out.map(function(x){return x.replace(/^\s+|\s+$/g,"");});
    if(out.length<3){
      var alt=line.split(/\s{2,}/).map(function(x){return x.replace(/^\s+|\s+$/g,"");}).filter(function(x){return x!=="";});
      if(alt.length>out.length)out=alt;
    }
    return out;
  }

  /* ============================================================ ledger */
  var STOP={"and":1,"the":1,"for":1,"its":1,"per":1,"from":1,"with":1,"into":1,"that":1,"this":1,
            "all":1,"but":1,"not":1,"other":1,"total":1,"net":1};

  /* Word's curly quotes, its dashes and its ellipsis, flattened before anything is parsed. */
  function deSmart(s){
    return String(s)
      .replace(/[‘’‚‛′]/g,"'")
      .replace(/[“”„‟″]/g,'"')
      .replace(/[–—−]/g,"-")
      .replace(/…/g,"...")
      .replace(/[   ]/g," ");
  }

  /* Shapes the reader knows by name. QuickBooks Online's Profit and Loss Comparison prints an
     account label in the first column, the two period columns, and (from its Calculations
     dropdown) a "$ change" and a "% change" column, with Income, Cost of Goods Sold and Expenses
     as section headers and Total, Gross Profit, Net Operating Income and Net Income as totals.
     Xero's Income Statement prints Income, Less Cost of Sales, Gross Profit, Less Operating
     Expenses and Net Profit, with a Total row closing each section. */
  var SECTION_ONLY=/^(?:less\s+)?(income|revenue|sales|trading income|other income|operating income|cost of goods sold|cost of sales|cogs|direct costs|expenses|operating expenses|overheads|administrative expenses|payroll expenses|other expenses|other income and expenses|assets|liabilities|equity)\b[\s:.\-]*$/i;
  var TOTALWORD=/^total\b/i;
  var GRAND=/^(gross profit|gross margin|net profit|net income|net loss|net operating income|net other income|net earnings|operating profit|profit before tax|profit for the (month|period|year)|net movement)\b/i;
  var HEADERWORD=/(^|\W)(prior|current|previous|prev|last|this|py|pp|comparative|change|variance|var|budget|actual|ytd|period|amount|balance|jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(t|tember)?|oct(ober)?|nov(ember)?|dec(ember)?|q[1-4]|fy)(\W|$)|%|\b(19|20)\d{2}\b/i;
  var DERIVEDCOL=/(change|variance|\bvar\b|%|percent|\bpct\b|diff|movement|\bfav\b|\bunfav\b)/i;
  var MONTHNUM={jan:1,feb:2,mar:3,apr:4,may:5,jun:6,jul:7,aug:8,sep:9,sept:9,oct:10,nov:11,dec:12};

  function monthKey(s){
    var t=String(s).toLowerCase();
    var y=t.match(/\b(19|20)\d{2}\b/);
    var year=y?parseInt(y[0],10):null;
    var m=t.match(/\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\b/);
    if(!m&&year===null)return null;
    if(!m)return year*12;
    return (year===null?2000:year)*12+MONTHNUM[m[1]];
  }

  /* the best guess at which of the numeric columns is the prior period and which is the current */
  function guessCols(labels){
    var T=labels.length,i,cand=[];
    for(i=0;i<T;i++)if(!DERIVEDCOL.test(labels[i]))cand.push(i);
    if(cand.length<2){cand=[];for(i=0;i<T;i++)cand.push(i);}
    var pi=-1,ci=-1;
    cand.forEach(function(j){
      var L=String(labels[j]).toLowerCase();
      if(pi<0&&/(prior|previous|\bprev\b|last month|last year|last period|\bpy\b|\bpp\b|comparative|budget)/.test(L))pi=j;
      if(ci<0&&/(current|this month|this year|this period|\bactual\b|\bytd\b)/.test(L))ci=j;
    });
    if(pi>-1&&ci>-1&&pi!==ci)return {p:pi,c:ci};
    var keyed=[];
    cand.forEach(function(j){var k=monthKey(labels[j]);if(k!==null)keyed.push({i:j,k:k});});
    var distinct={};keyed.forEach(function(x){distinct[x.k]=1;});
    if(keyed.length>=2&&Object.keys(distinct).length>=2){
      keyed.sort(function(a,b){return a.k-b.k;});
      return {p:keyed[0].i,c:keyed[keyed.length-1].i};
    }
    if(pi>-1){for(i=0;i<cand.length;i++)if(cand[i]!==pi)return {p:pi,c:cand[i]};}
    if(ci>-1){for(i=cand.length-1;i>=0;i--)if(cand[i]!==ci)return {p:cand[i],c:ci};}
    return {p:cand[0],c:cand[1]};
  }

  function acctShape(name,row){
    var num="",nm=name;
    var mm=nm.match(/^(\d{2,8}[A-Za-z]?)\s*[\s.:·-]\s*(\S.*)$/);
    if(mm){num=mm[1];nm=mm[2];}
    nm=nm.replace(/\s+/g," ").replace(/^[,\s]+|[,\s]+$/g,"");
    var words=nm.toLowerCase().replace(/[^a-z0-9\s]/g," ").split(/\s+/)
      .filter(function(w){return w.length>=3&&!STOP[w];});
    var flat=nm.toLowerCase().replace(/[^a-z0-9\s]/g," ").replace(/\s+/g," ").replace(/^ | $/g,"");
    return {num:num,name:nm,words:words,flat:flat,two:flat.split(" ").slice(0,2).join(" "),row:row};
  }

  /* Returns the account lines, the section totals, the numeric column labels and everything the
     reader could not use, with the reason. choice, when given, is {p:index,c:index} into the
     numeric columns; without it the reader guesses. */
  function parseLedger(text,choice){
    var lines=deSmart(text).split(/\r?\n/),raws=[],i;
    lines.forEach(function(raw,idx){
      var line=raw.replace(/^\s+|\s+$/g,"");
      if(!line)return;
      if(/^[-=_~\s|+*.]+$/.test(line))return;
      var f=splitFields(line);
      while(f.length&&(f[f.length-1]===""||f[f.length-1]==="*"))f.pop();
      if(!f.length)return;
      /* "100,000" split on commas is indistinguishable from two columns holding
         100 and 000. The row is refused rather than read on a guess. */
      var amb=false,z;
      if(line.indexOf("\t")<0&&line.indexOf(",")>-1){
        for(z=1;z<f.length;z++){
          if(/^\$?\d{3}$/.test(f[z])&&/^\$?[-(]?\d+\)?$/.test(f[z-1]))amb=true;
        }
      }
      var k=-1,tail=0,j;
      for(j=f.length-1;j>=0;j--){
        if(f[j]!==""&&!isNaN(parseNum(f[j]))){k=j;tail++;}
        else break;
      }
      raws.push({n:idx+1,line:line,f:f,k:k,tail:tail,amb:amb});
    });

    /* how many numeric columns this ledger runs: the most common trailing run */
    var counts={},best=0,T=0;
    raws.forEach(function(r){if(!r.amb&&r.tail>=2&&r.k>=1)counts[r.tail]=(counts[r.tail]||0)+1;});
    Object.keys(counts).forEach(function(t){
      var n=counts[t],v=parseInt(t,10);
      if(n>best||(n===best&&v>T)){best=n;T=v;}
    });

    var skipped=[],accounts=[],totals=[],sections=[],headerCells=null,headerLine=0,seenData=false,open=null,ambig=[];

    /* the header row: no numbers of its own, more than one cell, and cells that read like periods */
    if(T>=2){
      for(i=0;i<raws.length;i++){
        var r=raws[i];
        if(r.tail>0)break;
        if(r.f.length<2)continue;
        var hits=0;
        r.f.forEach(function(c){if(c&&HEADERWORD.test(c))hits++;});
        if(hits>=1){headerCells=r.f;headerLine=r.n;break;}
      }
    }
    var labels=[];
    if(headerCells&&headerCells.length>=T)labels=headerCells.slice(headerCells.length-T);
    for(i=0;i<T;i++)if(!labels[i]||!String(labels[i]).replace(/\s/g,""))labels[i]="column "+(i+1);

    var guess=T>=2?guessCols(labels):{p:0,c:1};
    var pick={p:guess.p,c:guess.c};
    if(choice&&typeof choice.p==="number"&&typeof choice.c==="number"&&
       choice.p>=0&&choice.p<T&&choice.c>=0&&choice.c<T&&choice.p!==choice.c){
      pick={p:choice.p,c:choice.c};
    }

    function pairOf(r){
      var base=r.f.length-T;
      var a=parseNum(r.f[base+pick.p]),b=parseNum(r.f[base+pick.c]);
      if(base+pick.p<r.k||base+pick.c<r.k||isNaN(a)||isNaN(b)){
        a=parseNum(r.f[r.k]);b=parseNum(r.f[r.k+1]);
      }
      return [a,b];
    }
    function headOf(r){
      var head=r.f.slice(0,r.k);
      while(head.length&&head[0]==="")head.shift();
      while(head.length&&head[head.length-1]==="")head.pop();
      if(head.length>1&&/^\d{2,8}[a-z]?$/i.test(head[0]))return head[0]+" "+head.slice(1).join(", ");
      return head.join(", ");
    }
    function openSection(nm,n){open={name:nm,lines:[],n:n};sections.push(open);}

    raws.forEach(function(r){
      if(headerCells&&r.n===headerLine){
        skipped.push({n:r.n,t:r.line,benign:1,why:"header row, read for the period columns and then ignored"});
        return;
      }
      if(r.amb){
        ambig.push("Line "+r.n+" splits on commas into a three digit field standing after a numeric field, which "+
          "is what an unquoted thousands separator looks like.");
        skipped.push({n:r.n,t:r.line,why:"the commas on this row cannot be told from an unquoted thousands "+
          "separator, so the row was refused rather than read on a guess"});
        return;
      }
      var label=r.tail>=2&&r.k>=1?headOf(r):r.f.join(" ").replace(/\s+/g," ").replace(/^\s+|\s+$/g,"");
      if(r.tail>=2&&r.k>=1){
        var pr=pairOf(r);
        if(TOTALWORD.test(label)||GRAND.test(label)){
          var isGrand=GRAND.test(label)&&!TOTALWORD.test(label);
          var tr={n:r.n,label:label,prior:pr[0],cur:pr[1],grand:isGrand,sec:null};
          if(!isGrand&&open&&open.lines.length){tr.sec=open;open=null;}
          else if(isGrand)open=null;
          totals.push(tr);
          skipped.push({n:r.n,t:label,keep:1,why:isGrand?"a computed total across sections, kept for the totals tie and left out of the line checks"
                                                :"a section total, kept for the totals tie and left out of the line checks"});
          return;
        }
        var sh=acctShape(label,r.n);
        if(!sh.name){skipped.push({n:r.n,t:r.line,why:"no account name"});return;}
        var prior=pr[0],cur=pr[1],change=cur-prior;
        var a={num:sh.num,name:sh.name,prior:prior,cur:cur,change:change,
               pct:(prior===0?null:(change/Math.abs(prior))*100),
               words:sh.words,flat:sh.flat,two:sh.two,row:r.n,section:open?open.name:"",sent:[]};
        accounts.push(a);
        if(open)open.lines.push(a);
        seenData=true;
        return;
      }
      /* no pair of numbers on this row */
      if(SECTION_ONLY.test(label)){openSection(label,r.n);return;}
      if(GRAND.test(label)){open=null;skipped.push({n:r.n,t:label,why:"a total with no figures beside it"});return;}
      if(seenData&&label&&r.tail===0&&r.f.length<=2){openSection(label,r.n);return;}
      skipped.push({n:r.n,t:r.line,benign:seenData?0:1,
        why:seenData?"could not read a prior and a current balance on this row":"title or heading above the report, ignored"});
    });

    /* duplicate account numbers */
    var seenNum={},dups=[];
    accounts.forEach(function(a){
      if(!a.num)return;
      if(seenNum[a.num]){if(dups.indexOf(a.num)<0)dups.push(a.num);}
      seenNum[a.num]=(seenNum[a.num]||0)+1;
    });

    var discarded=[];
    for(i=0;i<T;i++)if(i!==pick.p&&i!==pick.c)discarded.push(i);
    var named=0;
    labels.forEach(function(l){if(!/^column \d+$/.test(l))named++;});
    var colsUnconfirmed=(T>2&&named<T&&!(choice&&typeof choice.p==="number"));

    return {accounts:accounts,skipped:skipped,totals:totals,sections:sections,
            labels:labels,T:T,pick:pick,guess:guess,header:!!headerCells,dups:dups,
            ambig:ambig,discarded:discarded,colsUnconfirmed:colsUnconfirmed};
  }

  /* every section total recomputed from the lines under it */
  function tieTotals(L){
    var out=[];
    L.totals.forEach(function(t){
      if(t.grand||!t.sec){
        out.push({label:t.label,ok:null,det:t.grand
          ? "Kept out of the line checks. This is a total computed across sections, so the checker does not recompute it from lines."
          : "Kept out of the line checks. No section lines sit above this total, so there is nothing to recompute it from."});
        return;
      }
      var sp=0,sc=0;
      t.sec.lines.forEach(function(a){sp+=a.prior;sc+=a.cur;});
      var okP=Math.abs(sp-t.prior)<0.01,okC=Math.abs(sc-t.cur)<0.01;
      var n=t.sec.lines.length;
      var word="The "+n+" line"+(n===1?"":"s")+" under \""+t.sec.name+"\" "+(n===1?"adds":"add")+" to ";
      out.push({label:t.label,ok:okP&&okC,n:n,
        det:(okP&&okC)
          ? word+money(sp)+" prior and "+money(sc)+" current, which is what the total row says."
          : word+money(sp)+" prior and "+money(sc)+
            " current, but the total row says "+money(t.prior)+" and "+money(t.cur)+
            ". Something on this statement is missing from the paste or double counted."});
    });
    return out;
  }

  /* Boundary policy, printed on the page and decided on unrounded values:
     the dollar rule is MORE THAN the floor, the percent rule is AT LEAST the
     floor, and a zero prior balance is settled by the selected policy rather than
     by a default nobody chose. */
  function legs(a,floorD,floorP,zp){
    var d=Math.abs(a.change)>floorD,p;
    if(a.pct===null)p=(zp==="exclude")?false:(a.change!==0);
    else p=Math.abs(a.pct)>=floorP;
    return {d:d,p:p};
  }
  function clears(a,floorD,floorP,rule,zp){
    if(a.pct===null&&zp==="exclude")return false;
    var L=legs(a,floorD,floorP,zp);
    return rule==="either"?(L.d||L.p):(L.d&&L.p);
  }
  function pctCell(a){
    return a.pct===null?"new line":pctTxt(a.pct);
  }
  function pctPhrase(a){
    return a.pct===null?"a new line, so there is no prior balance to take a percent of"
                       :pctTxt(a.pct)+" of the prior balance";
  }

  /* ============================================================ memo */
  function splitSentences(text){
    var out=[],lines=deSmart(text).split(/\r?\n/),auto=0;
    lines.forEach(function(raw){
      var line=raw.replace(/^\s+|\s+$/g,"");
      if(!line)return;
      if(/^[-=_~\s|+*]{4,}$/.test(line))return;
      /* a bullet is numbering, not a label: strip it and read what follows */
      line=line.replace(/^[•·●▪‣⁃*>]+\s+/,"").replace(/^-\s+/,"").replace(/^\s+/,"");
      if(!line)return;
      /* (a), (1), a) and 1) are numbering too, kept as the label so the reviewer sees the
         preparer's own marker rather than a number the checker invented */
      var mp=line.match(/^\(\s*([A-Za-z]{1,2}|\d{1,3})\s*\)\s*(\S.*)$/);
      if(mp&&mp[2]){
        out.push({label:mp[1].toUpperCase(),text:mp[2].replace(/\s+/g," ")});
        return;
      }
      var ml=line.match(/^([a-z])\s*[.)\]]\s+(\S.*)$/);
      if(ml&&ml[2]){
        out.push({label:ml[1].toUpperCase(),text:ml[2].replace(/\s+/g," ")});
        return;
      }
      var m=line.match(/^([A-Za-z]{1,2}\s?\d{1,3}|\d{1,2})\s*[.)\]:-]\s+(.*)$/);
      if(m&&m[2]){
        out.push({label:m[1].replace(/\s+/g,"").toUpperCase(),text:m[2].replace(/\s+/g," ")});
        return;
      }
      /* no label: split the line into sentences */
      var buf="",i,ch,nx;
      for(i=0;i<line.length;i++){
        ch=line.charAt(i);buf+=ch;
        if(ch==="."||ch==="!"||ch==="?"){
          nx=line.slice(i+1);
          if(/^\s+["“(]?[A-Z0-9]/.test(nx)&&!/\d\.$/.test(buf)){
            out.push({label:null,text:buf.replace(/^\s+|\s+$/g,"").replace(/\s+/g," ")});
            buf="";i++;
            while(i<line.length&&/\s/.test(line.charAt(i)))i++;
            i--;
          }
        }
      }
      if(buf.replace(/^\s+|\s+$/g,""))out.push({label:null,text:buf.replace(/^\s+|\s+$/g,"").replace(/\s+/g," ")});
    });
    out.forEach(function(s){
      if(!s.label){auto++;s.label="S"+auto;}
      else{var n=parseInt(s.label.replace(/\D/g,""),10);if(isFinite(n)&&n>auto)auto=n;}
    });
    return out;
  }

  /* figures inside a sentence. $65k, $65K, $1.2M, 65,000, (65,000) and a bare 65k all read as
     dollars; 7%, 7 percent, 7 per cent and 7 pct all read as a percent. */
  function parseFig(raw){
    var t=String(raw).replace(/^\s+|\s+$/g,""),mult=1;
    var sm=t.match(/([kKmMbB])\s*\)?\s*$/);
    if(sm){
      var c=sm[1].toLowerCase();
      mult=c==="k"?1e3:(c==="m"?1e6:1e9);
      t=t.replace(/[kKmMbB](\s*\)?\s*)$/,"$1");
    }
    var v=parseNum(t);
    if(isNaN(v))return NaN;
    return v*mult;
  }
  /* ---------- 0. WHAT THE ACCEPTED GRAMMAR DOES NOT READ -------------------
     A number the grammar cannot interpret is never dropped in silence. It is
     recorded as an unparsed span, it stops the sentence being called checked, and
     it is listed in the reviewer's queue. Three kinds: a currency that is not the
     dollar, a scale or multiplier word the grammar does not carry, and a number
     standing where a claim stands that the figure reader did not take. */
  var FOREIGN_BEFORE=/(?:[\u20AC\u00A3\u00A5\u20B9\u20BD\u20A9\u20AA\u20BA\u0E3F\u00A2]|\b(?:EUR|GBP|JPY|CHF|CAD|AUD|NZD|CNY|RMB|INR|MXN|BRL|ZAR|SEK|NOK|DKK|SGD|HKD|USD)\s)\s*$/i;
  var FOREIGN_AFTER=/^\s*(?:[\u20AC\u00A3\u00A5\u20B9\u20BD\u20A9\u20AA\u20BA\u0E3F\u00A2]|\b(?:EUR|GBP|JPY|CHF|CAD|AUD|NZD|CNY|RMB|INR|MXN|BRL|ZAR|SEK|NOK|DKK|SGD|HKD|USD)\b)/i;
  var SCALE_AFTER=/^[\s-]*(?:thousands?|millions?|billions?|trillions?|mn|bn|basis\s+points?|bps|bp|times|multiples?|per\s?mille|permille|per\s+thousand|points?|pts)\b/i;
  var NUMWORD_RE=/\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)(?:[\s-]+(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion))*\b/gi;
  var UNIT_AFTER=/^[\s,-]*(?:percent|per\s?cent|pct|%|percentage\s+points?|basis\s+points?|points?|dollars?)\b/i;

  /* a quantity written out in words. Units through millions, hyphenated
     compounds, "thousand" and "million" are read. Where the run is well formed
     and the words beside it give it a unit, it becomes an ordinary figure and is
     compared like any other. Where it is well formed but carries no unit, and
     where the parser cannot resolve it at all, it is an unparsed span: the
     sentence is not called checked and the span is listed in the reviewer's
     queue. A count in words that stands where no claim stands, "the thirty-one
     new plans", is left alone, the same way a bare run of digits is. */
  var FRACTION_AFTER=/^[\s-]*(?:half|halves|third|thirds|quarter|quarters|fifth|fifths|sixth|sixths|seventh|sevenths|eighth|eighths|ninth|ninths|tenth|tenths|twelfth|twelfths|hundredth|hundredths|thousandth|thousandths)\b/i;
  var WORD_UNIT=/^[\s,-]*(?:(percentage\s+points?|pp)|(percent|per\s?cent|pct|%)|(dollars?))\b/i;
  var NW_SMALL={one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9};
  var NW_TEEN={ten:10,eleven:11,twelve:12,thirteen:13,fourteen:14,fifteen:15,sixteen:16,
               seventeen:17,eighteen:18,nineteen:19};
  var NW_TENS={twenty:20,thirty:30,forty:40,fifty:50,sixty:60,seventy:70,eighty:80,ninety:90};
  function nwLead(w){
    if(NW_SMALL[w]!==undefined)return NW_SMALL[w];
    if(NW_TEEN[w]!==undefined)return NW_TEEN[w];
    if(NW_TENS[w]!==undefined)return NW_TENS[w];
    return null;
  }
  /* one group below a thousand: "one hundred twenty-five", "nineteen", "thirty" */
  function nwGroup(tk,i){
    var v=0,any=false,h;
    if(i+1<tk.length&&tk[i+1]==="hundred"&&(h=nwLead(tk[i]))!==null){v=h*100;any=true;i+=2;}
    if(i<tk.length&&NW_TENS[tk[i]]!==undefined){
      v+=NW_TENS[tk[i]];any=true;i++;
      if(i<tk.length&&NW_SMALL[tk[i]]!==undefined){v+=NW_SMALL[tk[i]];i++;}
    }else if(i<tk.length&&(NW_SMALL[tk[i]]!==undefined||NW_TEEN[tk[i]]!==undefined)){
      v+=NW_SMALL[tk[i]]!==undefined?NW_SMALL[tk[i]]:NW_TEEN[tk[i]];any=true;i++;
    }
    return any?{v:v,i:i}:null;
  }
  /* the value of the whole run, or null where the parser cannot resolve it.
     "billion" is deliberately out of range: the grammar reads units through
     millions, and anything above that goes to the reviewer rather than being
     guessed at. */
  function wordsToNumber(run){
    var tk=String(run).toLowerCase().split(/[\s-]+/).filter(function(w){return w;});
    var i=0,total=0,last=Infinity,got=false,g,sc;
    while(i<tk.length){
      g=nwGroup(tk,i);
      if(!g)return null;
      i=g.i;sc=1;
      if(i<tk.length&&(tk[i]==="thousand"||tk[i]==="million")){sc=tk[i]==="thousand"?1000:1000000;i++;}
      if(sc>=last)return null;
      if(sc===1&&i<tk.length)return null;
      last=sc;
      total+=g.v*sc;got=true;
    }
    return got?total:null;
  }
  /* every run of number words, split into the ones that become figures and the
     ones that have to reach the reviewer. `always` marks a span that goes to the
     queue wherever it stands; the rest go only where the words put a claim. */
  function wordNumbers(text,taken){
    var figs=[],pending=[],m;
    NUMWORD_RE.lastIndex=0;
    while((m=NUMWORD_RE.exec(text))!==null){
      var i=m.index,j=i+m[0].length,t,hit=false;
      for(t=0;t<taken.length;t++)if(i<taken[t][1]&&j>taken[t][0]){hit=true;break;}
      if(hit)continue;
      var after=text.slice(j,j+30),fm,u,v;
      if(/\d\s*$/.test(text.slice(Math.max(0,i-14),i))){
        pending.push({raw:m[0],at:i,end:j,why:"a figure written in words",always:true});continue;
      }
      if((fm=after.match(FRACTION_AFTER))){
        pending.push({raw:text.slice(i,j+fm[0].length),at:i,end:j+fm[0].length,
          why:"a quantity in words the checker cannot resolve",always:true});continue;
      }
      v=wordsToNumber(m[0]);
      if(v===null){
        pending.push({raw:m[0],at:i,end:j,
          why:"a quantity in words the checker cannot resolve",always:true});continue;
      }
      if((u=after.match(WORD_UNIT))){
        figs.push({raw:text.slice(i,j+u[0].length).replace(/^\s+|\s+$/g,""),v:v,at:i,end:j+u[0].length,
          unit:u[1]?"percentage points":(u[2]?"percent":"dollars"),signed:false,words:true});
        continue;
      }
      if(UNIT_AFTER.test(after)){
        pending.push({raw:m[0],at:i,end:j,
          why:"a quantity in words the checker cannot resolve",always:true});continue;
      }
      pending.push({raw:m[0],at:i,end:j,why:"a figure written in words with no unit",always:false});
    }
    return {figs:figs,pending:pending};
  }
  /* ---------- 0b. QUANTITIES THE FIGURE READER DOES NOT PARSE -------------
     A sentence is checked within scope only when every quantitative expression in
     it is accounted for. These forms carry a quantity the figure reader does not
     parse, so each one is an unparsed span wherever it stands: a multiplier
     ("doubled", "twice", "threefold", "3x"), a fraction ("one and a half", "a
     quarter of", "half the prior balance", "1/2"), a decimal written in words
     ("thirty point five"), a digit outside 0 to 9 (Arabic-Indic, fullwidth,
     superscript), a fraction or per mille character, and a number glued to
     letters or underscores ("9e1", "30_000"). */
  var ODD_NUM_RE=/(?:[0-9][0-9.,]*)?[٠-٩۰-۹०-९০-৯๐-๙０-９²³¹⁰⁴-⁹₀-₉¼-¾⅐-⅞①-⑳‰‱％]+(?:[0-9.,٫٬]*[0-9٠-٩۰-۹०-९০-৯๐-๙０-９²³¹⁰⁴-⁹₀-₉¼-¾⅐-⅞①-⑳‰‱％])*/g;
  var MULT_RE=/\b(?:doubl(?:e|ed|es|ing)|tripl(?:e|ed|es|ing)|quadrupl(?:e|ed|es|ing)|quintupl(?:e|ed|es|ing)|halv(?:e|ed|es|ing)|twice|thrice|(?:two|three|four|five|six|seven|eight|nine|ten|twenty|hundred|[0-9]+(?:\.[0-9]+)?)[\s-]?fold|(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+times|[0-9]+(?:\.[0-9]+)?\s?[x×])(?![A-Za-z0-9])/gi;
  var MULT_NOT=/^[\s-]+(?:entry|entries|count|counted|counting|check|checked|checking)\b/i;
  var FRACW="half|halves|third|thirds|quarter|quarters|fifth|fifths|sixth|sixths|seventh|sevenths|eighth|eighths|ninth|ninths|tenth|tenths|twelfth|twelfths|hundredth|hundredths|thousandth|thousandths";
  var FRAC_RE=new RegExp("\\b(?:(a|an|one|two|three|four|five|six|seven|eight|nine|ten|[0-9]+)[\\s-]+(?:and[\\s-]+(?:a|one)[\\s-]+)?)?("+FRACW+")\\b","gi");
  var FRAC_KEEP=/^[\s-]*(?:of|percent|per|pct|point|points|again|more|less|higher|lower|the|a|an|and|or)\b|^[\s-]*(?:[^A-Za-z\s-]|$)/i;
  var DECW="zero|oh|one|two|three|four|five|six|seven|eight|nine";
  var DECWORD_RE=new RegExp("\\b(?:(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|zero)(?:[\\s-]+(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|zero))*[\\s-]+)?point(?:[\\s-]+(?:"+DECW+"))+\\b","gi");
  var SLASH_RE=/\b[0-9]{1,4}\s?\/\s?[0-9]{1,4}(?:\/[0-9]{2,4})?\b|\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b|\b[0-9]{1,2}:[0-9]{2}\b/g;
  var DATE_PREP=/\b(?:on|by|as\s+of|through|thru|since|until|from|to|dated|of|in|ending|ended|at|the|and|or|between|before|after|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+$/i;
  var MONTHW="jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?";
  var DATE_AFTER=new RegExp("^(?:st|nd|rd|th)?,?\\s+(?:of\\s+)?(?:"+MONTHW+")\\b","i");
  var DATE_BEFORE=new RegExp("\\b(?:"+MONTHW+")\\.?\\s+$","i");
  var YEAR_BEFORE=new RegExp("\\b(?:in|of|for|since|during|through|until|fiscal|calendar|year|fy|"+MONTHW+")[\\s,]+$","i");
  var LABEL_BEFORE=/(?:#|\b(?:no|nos|number|note|notes|line|lines|row|rows|item|items|card|cards|page|pages|section|sections|schedule|exhibit|appendix|step|phase|form|store|site|suite|building|route|account|acct|invoice|version|tier|level|class|grade|sku|asc|ias|ifrs|asu|gasb|fasb|irc|topic|chapter|part|article|rule|clause|option|question|week|day|round|case|table|figure|chart|slide|task|ticket|order|po|batch|lot|room|floor|zone|region|district)\.?)[\s#-]*$/i;
  var COUNT_AFTER=/^[\s-]+([A-Za-z]{2,})/;
  var ONE_IDIOM=/^one(?:\s+(?:of|another)\b|[\s-]+(?:time|off)\b)/i;
  var ONE_BEFORE=/\b(?:the|this|that|each|every|any|no|other|larger|smaller|last|first|new|old)\s+$/i;
  var COUNT_STOP=null;
  function countStop(){
    if(COUNT_STOP)return COUNT_STOP;
    COUNT_STOP={};
    ("percent per pct pp bp bps basis point points pts dollar dollars usd cent cents thousand thousands million "+
     "millions billion billions trillion trillions mn bn times fold mille percentage to from by at of in on and or "+
     "but nor than over under above below versus vs against compared since for with as because while after before "+
     "the a an this that these those which who is was were are be been being it its so then when into through each "+
     "more less higher lower plus minus now again same").split(" ").forEach(function(w){COUNT_STOP[w]=1;});
    UP.concat(DOWN).forEach(function(w){COUNT_STOP[w]=1;});
    Object.keys(MOVE_NOUN).forEach(function(w){COUNT_STOP[w]=1;});
    return COUNT_STOP;
  }
  var OUTSIDE_WHY={count:"a count the ledger does not hold",date:"a date",year:"a year",label:"a label or reference",
                   ordinal:"an ordinal",time:"a time of day"};
  /* the forms above, found before any figure is read so no part of one is ever
     read as a figure. `outside` collects the dates it recognized on the way. */
  function oddQuantities(text){
    var out=[],outside=[],m;
    ODD_NUM_RE.lastIndex=0;
    while((m=ODD_NUM_RE.exec(text))!==null){
      out.push({raw:m[0],at:m.index,end:m.index+m[0].length,why:"a digit or numeric character the checker does not read"});
    }
    MULT_RE.lastIndex=0;
    while((m=MULT_RE.exec(text))!==null){
      if(/^doubl/i.test(m[0])&&MULT_NOT.test(text.slice(m.index+m[0].length)))continue;
      out.push({raw:m[0],at:m.index,end:m.index+m[0].length,why:"a multiplier the checker does not read"});
    }
    DECWORD_RE.lastIndex=0;
    while((m=DECWORD_RE.exec(text))!==null){
      out.push({raw:m[0],at:m.index,end:m.index+m[0].length,why:"a decimal written in words the checker does not read"});
    }
    FRAC_RE.lastIndex=0;
    while((m=FRAC_RE.exec(text))!==null){
      var w=m[2].toLowerCase(),lead=m[1]?m[1].toLowerCase():"",aft=text.slice(m.index+m[0].length),
          bef=text.slice(0,m.index);
      if(w==="half"||w==="halves"){
        if(!lead&&/(?:first|second|latter|former|back|front)[\s-]*$/i.test(bef))continue;
        if(/^[\s-]*(?:years?|months?|days?|hours?|time)\b/i.test(aft))continue;
      }else if(w==="quarter"||w==="quarters"){
        if(!lead||/^[\s-]*end\b/i.test(aft))continue;
      }else{
        if(!lead)continue;
        if((lead==="a"||lead==="an"||lead==="one")&&!/s$/.test(w)&&!FRAC_KEEP.test(aft))continue;
      }
      out.push({raw:m[0],at:m.index,end:m.index+m[0].length,why:"a fraction the checker does not read"});
    }
    SLASH_RE.lastIndex=0;
    while((m=SLASH_RE.exec(text))!==null){
      var sb=text.slice(0,m.index),sa=text.slice(m.index+m[0].length);
      var dated=/-|:/.test(m[0])||/\/[0-9]+\//.test(m[0])||DATE_PREP.test(sb);
      if(dated&&!/^\s*(?:of\b|percent|per\s?cent|pct|%)/i.test(sa)){
        outside.push({raw:m[0],at:m.index,end:m.index+m[0].length,kind:/:/.test(m[0])?"time":"date"});
      }else{
        out.push({raw:m[0],at:m.index,end:m.index+m[0].length,why:"a fraction the checker does not read"});
      }
    }
    out.sort(function(a,b){return a.at-b.at||b.end-a.end;});
    var merged=[];
    out.forEach(function(o){
      var last=merged[merged.length-1];
      if(last&&o.at<last.end){if(o.end>last.end){last.end=o.end;last.raw=text.slice(last.at,last.end);}return;}
      merged.push(o);
    });
    return {spans:merged,outside:outside};
  }
  /* A run of digits the figure reader did not take. It is accounted for only as
     a year, a date, a label, an ordinal, a time of day, an account number standing
     as a reference, or a count written in front of the thing it counts. Anything
     else is an unparsed span. */
  function strayNumbers(text,taken,figs,skipNums){
    var re=/-?[0-9][0-9,]*(?:\.[0-9]+)?/g,out=[],outside=[],m,t,hit,i,j;
    while((m=re.exec(text))!==null){
      i=m.index;j=i+m[0].length;hit=false;
      for(t=0;t<taken.length;t++)if(i<taken[t][1]&&j>taken[t][0]){hit=true;break;}
      if(hit)continue;
      var ts=i,te=j;
      while(ts>0&&/[A-Za-z0-9_]/.test(text.charAt(ts-1)))ts--;
      while(te<text.length&&/[A-Za-z0-9_]/.test(text.charAt(te)))te++;
      if(ts<i||te>j){
        var tok=text.slice(ts,te);
        re.lastIndex=te;
        if(/^[0-9]+(?:st|nd|rd|th)$/i.test(tok))outside.push({raw:tok,at:ts,end:te,kind:"ordinal"});
        else if(/^[0-9]{1,2}(?:am|pm)$/i.test(tok))outside.push({raw:tok,at:ts,end:te,kind:"time"});
        else if(/^[A-Za-z]{1,6}[0-9]+[A-Za-z]?$/.test(tok))outside.push({raw:tok,at:ts,end:te,kind:"label"});
        else out.push({raw:tok,at:ts,end:te,why:"a number written in a form the checker does not read"});
        continue;
      }
      var after=text.slice(j,j+26),before=text.slice(Math.max(0,i-40),i);
      var unit=SCALE_AFTER.test(after)||FOREIGN_AFTER.test(after);
      if(unit){
        out.push({raw:m[0]+(after.match(SCALE_AFTER)||after.match(FOREIGN_AFTER))[0],at:i,end:j,
          why:"a unit the checker does not read"});
        continue;
      }
      var r=roleOf(text,{at:i,end:j,unit:"dollars"},0,[]);
      var digits=m[0].replace(/[^0-9]/g,""),whole=/^[0-9]+$/.test(m[0]),n=parseInt(digits,10),cw;
      if(/^(19|20)[0-9]{2}$/.test(m[0])&&(r.role==="unknown"||YEAR_BEFORE.test(before))){
        outside.push({raw:m[0],at:i,end:j,kind:"year"});continue;
      }
      if(skipNums&&skipNums[m[0]]&&r.role==="unknown")continue;
      if(whole&&n>=1&&n<=31&&(DATE_AFTER.test(after)||DATE_BEFORE.test(before))){
        outside.push({raw:m[0],at:i,end:j,kind:"date"});continue;
      }
      if(whole&&LABEL_BEFORE.test(before)){outside.push({raw:m[0],at:i,end:j,kind:"label"});continue;}
      if(whole&&(cw=after.match(COUNT_AFTER))&&!countStop()[cw[1].toLowerCase()]){
        outside.push({raw:m[0],at:i,end:j,kind:"count"});continue;
      }
      out.push({raw:m[0],at:i,end:j,
        why:r.role!=="unknown"?"a number standing where the words put a claim":"a number the checker cannot place"});
    }
    out.outside=outside;
    return out;
  }

  /* ---------- 1. EXTRACTION ------------------------------------------------
     A figure is the text span it was read from, its value, its unit and whether
     the text gave it an explicit sign. Nothing here binds an account, and nothing
     here decides what the figure means. Those are separate steps on purpose. */
  function figures(text,skipNums){
    var out=[],taken=[],m;
    function overlaps(i,j){var t;for(t=0;t<taken.length;t++){if(i<taken[t][1]&&j>taken[t][0])return true;}return false;}
    /* parentheses only make a figure negative when they close around it. A lone
       opening bracket, as in "increased by $30,000 (30%)", is punctuation. */
    function hasSign(raw){return /^\s*-/.test(raw)||(/^\s*\(/.test(raw)&&/\)\s*$/.test(raw));}
    /* a figure glued to the letters, digits, dots or slashes in front of it, as in
       "9e1 percent" or "US$30,000", is not the figure it would be on its own */
    var glued=[];
    function gluedAt(m){
      var k=m.index+Math.max(0,m[0].search(/[-($0-9]/)),s=k;
      if(k===0||!/[A-Za-z0-9_.\/]/.test(text.charAt(k-1)))return false;
      while(s>0&&/[A-Za-z0-9_.\/]/.test(text.charAt(s-1)))s--;
      var end=m.index+m[0].length;
      glued.push({raw:text.slice(s,end).replace(/\s+$/,""),at:s,end:end,
        why:/^[A-Za-z]+$/.test(text.slice(s,k))&&text.charAt(k)==="$"?"a currency the checker does not read":
          "a number written in a form the checker does not read"});
      taken.push([s,end]);
      return true;
    }

    var odd=oddQuantities(text);
    odd.spans.forEach(function(o){taken.push([o.at,o.end]);});
    odd.outside.forEach(function(o){taken.push([o.at,o.end]);});

    var rp=/([-(]?\s?\$?\s?\d[\d,]*(?:\.\d+)?\s?\)?)\s*(percentage points?|percent|per cent|pct|pp|%)/gi;
    while((m=rp.exec(text))!==null){
      if(overlaps(m.index,m.index+m[0].length))continue;
      if(gluedAt(m))continue;
      var ptxt=m[1],neg=hasSign(ptxt);
      if(/^\s*\(/.test(ptxt)&&!/\)\s*$/.test(ptxt))ptxt=ptxt.replace(/^\s*\(/,"");
      var pv=parseNum(ptxt);
      if(!isNaN(pv)){
        out.push({raw:m[0].replace(/^\s*\(/,"").replace(/^\s+|\s+$/g,""),v:pv,at:m.index,end:m.index+m[0].length,
                  unit:/point/i.test(m[2])||/^pp$/i.test(m[2])?"percentage points":"percent",
                  signed:neg});
      }
      taken.push([m.index,m.index+m[0].length]);
    }
    var rd=/\(\s?\$?\s?\d(?:[\d,]*\d)?(?:\.\d+)?\s?[kKmMbB]?\s?\)|-?\$\s?\d(?:[\d,]*\d)?(?:\.\d+)?(?:\s?[kKmMbB]\b)?|\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|\b\d+(?:\.\d+)?[kKmMbB]\b/g;
    while((m=rd.exec(text))!==null){
      if(overlaps(m.index,m.index+m[0].length))continue;
      if(gluedAt(m))continue;
      var dv=parseFig(m[0]);
      if(isNaN(dv))continue;
      out.push({raw:m[0].replace(/^\s+|\s+$/g,""),v:dv,at:m.index,end:m.index+m[0].length,
                unit:"dollars",signed:hasSign(m[0])});
      taken.push([m.index,m.index+m[0].length]);
    }
    /* ordinary numeric text: four digits or more, no currency punctuation at all.
       A minus sign in front of it is part of the figure and is carried through.
       A bare four digit number that reads as a year is left where it stands, and
       an account number written out is a reference; either one, standing where the
       words put a claim, is picked up as an unparsed span further down. */
    var rn=/(?:-\s?)?\b\d{4,}(?:\.\d+)?\b/g;
    while((m=rn.exec(text))!==null){
      if(overlaps(m.index,m.index+m[0].length))continue;
      var bare=m[0].replace(/[^0-9.]/g,"");
      if(/^(19|20)\d\d$/.test(bare))continue;
      if(LABEL_BEFORE.test(text.slice(Math.max(0,m.index-40),m.index)))continue;
      if(skipNums&&skipNums[bare])continue;
      if(gluedAt(m))continue;
      out.push({raw:m[0].replace(/\s+/g,""),v:parseFloat(bare)*(/^-/.test(m[0])?-1:1),
                at:m.index,end:m.index+m[0].length,
                unit:"dollars",signed:/^-/.test(m[0]),plain:true});
      taken.push([m.index,m.index+m[0].length]);
    }
    /* a quantity in words that the parser resolved and the words gave a unit is
       an ordinary figure from here on. */
    var wn=wordNumbers(text,taken);
    wn.figs.forEach(function(f){
      if(overlaps(f.at,f.end))return;
      out.push(f);taken.push([f.at,f.end]);
    });
    out.sort(function(a,b){return a.at-b.at;});

    /* a figure written in a currency the checker does not read, or carrying a
       scale word it does not carry, is not a figure it may compare against a
       dollar ledger. It comes out of the accepted set and goes to the queue. */
    var rejected=odd.spans.concat(glued),keep=[],outside=odd.outside.slice();
    out.forEach(function(f){
      var before=text.slice(0,f.at),after=text.slice(f.end),mm;
      if(f.unit==="dollars"&&(mm=before.match(FOREIGN_BEFORE))){
        rejected.push({raw:mm[0].replace(/^\s+/,"")+f.raw,at:f.at-mm[0].replace(/^\s+/,"").length,end:f.end,
          why:"a currency the checker does not read"});return;
      }
      if(f.unit==="dollars"&&(mm=after.match(FOREIGN_AFTER))){
        rejected.push({raw:f.raw+mm[0],at:f.at,end:f.end+mm[0].length,
          why:"a currency the checker does not read"});return;
      }
      if(f.unit==="dollars"&&(mm=after.match(SCALE_AFTER))){
        rejected.push({raw:f.raw+mm[0],at:f.at,end:f.end+mm[0].length,
          why:"a scale word the checker does not carry"});return;
      }
      keep.push(f);
    });
    keep.forEach(function(f,i){
      var r=roleOf(text,f,i,keep);
      f.role=r.role;f.side=r.side||"";f.roleFrom=r.from||"";
    });
    var spans=[],k;
    for(k=0;k<keep.length;k++)spans.push([keep[k].at,keep[k].end]);
    for(k=0;k<rejected.length;k++)spans.push([rejected[k].at,rejected[k].end]);
    for(k=0;k<outside.length;k++)spans.push([outside[k].at,outside[k].end]);
    /* a quantity in words with no unit is accounted for only as a count written in
       front of the thing it counts, or as "one" standing as a pronoun or an idiom */
    wn.pending.forEach(function(w){
      for(k=0;k<spans.length;k++)if(w.at<spans[k][1]&&w.end>spans[k][0])return;
      if(!w.always){
        var cw=text.slice(w.end,w.end+30).match(COUNT_AFTER),low=w.raw.toLowerCase();
        if(cw&&!countStop()[cw[1].toLowerCase()]){outside.push({raw:w.raw,at:w.at,end:w.end,kind:"count"});return;}
        if(low==="one"&&(ONE_IDIOM.test(text.slice(w.at))||ONE_BEFORE.test(text.slice(0,w.at))))return;
        if(LABEL_BEFORE.test(text.slice(Math.max(0,w.at-40),w.at))){outside.push({raw:w.raw,at:w.at,end:w.end,kind:"label"});return;}
        if(roleOf(text,{at:w.at,end:w.end,unit:"dollars"},0,[]).role==="unknown")w.why="a figure written in words the checker cannot place";
      }
      rejected.push({raw:w.raw,at:w.at,end:w.end,why:w.why});spans.push([w.at,w.end]);
    });
    var stray=strayNumbers(text,spans,keep,skipNums);
    stray.forEach(function(n){rejected.push(n);});
    stray.outside.forEach(function(o){outside.push(o);});
    rejected.sort(function(a,b){return a.at-b.at;});
    outside.sort(function(a,b){return a.at-b.at;});
    keep.rejected=rejected;
    keep.outside=outside;
    return keep;
  }
  /* kept for callers of the earlier module; figures() no longer uses it */
  function numberWords(text){
    var out=[],m;
    NUMWORD_RE.lastIndex=0;
    while((m=NUMWORD_RE.exec(text))!==null){
      var j=m.index+m[0].length;
      if(UNIT_AFTER.test(text.slice(j,j+26))||/\d\s*$/.test(text.slice(Math.max(0,m.index-14),m.index)))
        out.push({raw:m[0],at:m.index,end:j,why:"a figure written in words"});
    }
    return out;
  }

  function dollarsIn(figs){return figs.filter(function(f){return f.unit==="dollars";});}
  function pctsIn(figs){return figs.filter(function(f){return f.unit!=="dollars";});}

  /* ---------- 2. NUMERIC ROLE ---------------------------------------------
     Read from the words around the figure, never from the fact that it happens to
     equal something in the ledger. Where the words do not say, the role is
     unknown and the reviewer is asked to confirm it in a dropdown. */
  /* "prior" and "current" standing in front of a figure are the role labels
     Prompt 1 asks the drafting tool to write, so they are read as roles too */
  var CUE_PRIOR={from:1,prior:1,previous:1};
  var CUE_CURRENT={to:1,at:1,now:1,reached:1,reaching:1,stands:1,standing:1,hit:1,hits:1,current:1};
  /* words after a figure that turn it into a bound rather than a figure */
  var BOUND_AFTER=/^\s*(?:or\s+(?:more|less|so|higher|lower|above|below|over|under)|at\s+(?:most|least)|and\s+(?:up|above|over))\b/i;
  var CUE_MOVE={by:1};
  var MOVE_NOUN={increase:1,increases:1,decrease:1,decreases:1,rise:1,rises:1,fall:1,falls:1,drop:1,
                 drops:1,gain:1,gains:1,growth:1,decline:1,declines:1,movement:1,change:1,variance:1,
                 swing:1,reduction:1,uptick:1};
  var SKIPW={a:1,an:1,the:1,is:1,was:1,were:1,are:1,be:1,been:1,which:1,that:1,of:1,"in":1,about:1,
             roughly:1,approximately:1,some:1,only:1,just:1,another:1,total:1,net:1,this:1,its:1};
  var DIRSET=null;
  function dirSet(){
    if(DIRSET)return DIRSET;
    DIRSET={};
    UP.concat(DOWN).forEach(function(w){DIRSET[w]=1;});
    return DIRSET;
  }
  function roleOf(text,f,idx,all){
    var pre=text.slice(0,f.at),post=text.slice(f.end);
    var pct=f.unit!=="dollars";
    if(f.unit==="percentage points")
      return {role:"rate change in points",from:"the words \"percentage points\""};
    if(BOUND_AFTER.test(post))return {role:"unknown",from:""};
    if(pct&&/^\s*of\s+(the\s+)?(prior|previous|last|opening|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)/i.test(post))
      return {role:"relative movement",from:"\"of\" naming the period it is a share of"};
    var nx=post.replace(/^[^A-Za-z]*/,"").toLowerCase().split(/[^a-z]/)[0];
    if(nx&&MOVE_NOUN[nx])
      return {role:pct?"relative movement":"absolute movement",from:"the word \""+nx+"\" standing after it"};
    var words=pre.toLowerCase().replace(/[^a-z\s]/g," ").replace(/\s+/g," ").split(" ")
               .filter(function(w){return w!=="";});
    var win=words.slice(-6),i,w,prev,r;
    for(i=win.length-1;i>=0;i--){
      w=win[i];
      if(CUE_PRIOR[w])return {role:pct?"ratio":"prior balance",side:"prior",from:"the word \""+w+"\""};
      if(CUE_CURRENT[w])return {role:pct?"ratio":"current balance",side:"current",from:"the word \""+w+"\""};
      if(CUE_MOVE[w])return {role:pct?"relative movement":"absolute movement",from:"the word \""+w+"\""};
      if(MOVE_NOUN[w])return {role:pct?"relative movement":"absolute movement",from:"the word \""+w+"\""};
      if(dirSet()[w])return {role:pct?"relative movement":"absolute movement",from:"the direction word \""+w+"\""};
      if((w==="or"||w==="and")&&idx>0){
        prev=all[idx-1];
        if(prev&&prev.role&&prev.role!=="unknown"){
          r=prev.role;
          if(pct&&r==="absolute movement")r="relative movement";
          if(!pct&&r==="relative movement")r="absolute movement";
          return {role:r,side:prev.side||"",from:"\""+w+"\", restating the figure before it"};
        }
        return {role:"unknown",from:""};
      }
      if(SKIPW[w])continue;
      break;
    }
    return {role:"unknown",from:""};
  }

  /* ---------- 3. ACCOUNT BINDING ------------------------------------------
     Three labelled routes: the account number written in the sentence, the
     account name written in the sentence, and an exact figure. A figure route is
     only accepted when the sentence also carries a word from that account's name
     that no named account shares; otherwise it is a numeric coincidence and it is
     reported as an unresolved conflict rather than being bound. */
  var TOL_P=0.05,TOL_D=0.005;
  function near(a,b,t){return Math.abs(Math.abs(a)-Math.abs(b))<=t;}
  function exactly(a,b,t){return Math.abs(a-b)<=t;}
  function acctId(a){return (a.num?a.num+" ":"")+a.name;}

  function bindSentence(s,accounts,figs,spent){
    var text=" "+s.text.toLowerCase().replace(/[^a-z0-9$.,%\s-]/g," ").replace(/\s+/g," ")+" ";
    var tokens={};
    s.text.toLowerCase().replace(/[a-z]+/g,function(w){tokens[w]=1;return w;});
    var byNum=[],byName=[],byWord=[],byFig=[],conflicts=[],i;

    accounts.forEach(function(a){
      if(spent&&spent[a.num])return;
      if(a.num&&new RegExp("(^|[^0-9])"+a.num+"([^0-9]|$)").test(s.text))byNum.push(a);
    });
    accounts.forEach(function(a){
      if(byNum.indexOf(a)>-1)return;
      if(a.flat&&text.indexOf(" "+a.flat+" ")>-1){byName.push(a);return;}
      if(a.two&&a.two.indexOf(" ")>-1&&text.indexOf(" "+a.two+" ")>-1)byName.push(a);
    });
    var named=byNum.concat(byName);
    var namedWords={};
    named.forEach(function(a){a.words.forEach(function(w){namedWords[w]=1;});});

    dollarsIn(figs).forEach(function(f){
      f.ties=accounts.filter(function(a){
        return near(f.v,a.prior,TOL_D)||near(f.v,a.cur,TOL_D)||near(f.v,a.change,TOL_D);
      });
      f.ties.forEach(function(a){
        if(named.indexOf(a)>-1||byFig.indexOf(a)>-1)return;
        var distinct=a.words.filter(function(w){return !namedWords[w]&&tokens[w];});
        if(distinct.length)byFig.push(a);
        else conflicts.push({a:a,f:f});
      });
    });
    var bound=named.concat(byFig);
    if(!bound.length){
      accounts.forEach(function(a){
        for(i=0;i<a.words.length;i++)if(tokens[a.words[i]]){byWord.push(a);return;}
      });
      bound=byWord.slice();
    }
    var how=[];
    if(byNum.length)how.push("by account number");
    if(byName.length)how.push("by account name");
    if(byFig.length)how.push("by an exact figure with a word from the name beside it");
    if(!byNum.length&&!byName.length&&!byFig.length&&byWord.length)how.push("by a word in the account name");
    return {bound:bound,byNum:byNum,byName:byName,byFig:byFig,byWord:byWord,
            conflicts:conflicts,how:how.join(", ")};
  }

  /* A sentence that names more than one account is only allowed to bind a figure
     to one of them when the clause the figure stands in names that one and no
     other. Where it does not, the binding is unresolved and the figure cannot be
     called checked, whatever it happens to equal. */
  function clauseBind(s){
    var spans=spansOf(s.text,RE_FINE),distinct={};
    s.bound.forEach(function(a){
      distinct[acctId(a)]=a.words.filter(function(w){
        var shared=false;
        s.bound.forEach(function(o){if(o!==a&&o.words.indexOf(w)>-1)shared=true;});
        return !shared;
      });
    });
    s.figs.forEach(function(f){
      var cl=null,hits=[];
      spans.forEach(function(sp){if(f.at>=sp.at&&f.at<sp.end)cl=sp;});
      if(cl){
        var ct=" "+cl.text.toLowerCase().replace(/[^a-z0-9\s]/g," ").replace(/\s+/g," ")+" ";
        s.bound.forEach(function(a){
          var got=false;
          if(a.num&&new RegExp("(^|[^0-9])"+a.num+"([^0-9]|$)").test(cl.text))got=true;
          if(!got&&a.flat&&ct.indexOf(" "+a.flat+" ")>-1)got=true;
          if(!got&&a.two&&a.two.indexOf(" ")>-1&&ct.indexOf(" "+a.two+" ")>-1)got=true;
          if(!got)(distinct[acctId(a)]||[]).forEach(function(w){if(ct.indexOf(" "+w+" ")>-1)got=true;});
          if(got)hits.push(a);
        });
      }
      f.clause=cl?cl.text:s.text;
      f.bind=hits.length===1?hits:null;
    });
  }

  /* ---------- 4. UNITS AND CALCULATION ------------------------------------
     Every comparison is made on unrounded values. A dollar figure ties when it is
     within half a cent of the ledger value and a percent within 0.05 of a
     percentage point, which is the tolerance the rounding on screen needs. A sign
     written into the memo, by a minus or by parentheses, is compared as written;
     where the memo writes a magnitude the sign is left to the direction check. */
  function qtyOf(a,which){return which==="prior"?a.prior:(which==="cur"?a.cur:a.change);}
  function qtyName(which){return which==="prior"?"prior balance":(which==="cur"?"current balance":"change");}
  var ROLE_QTY={"prior balance":"prior","current balance":"cur","absolute movement":"change"};

  function checkDollar(f,bound,all){
    if(!all||!all.length)all=bound;
    var want=ROLE_QTY[f.role]||null,hit=null,alts=[],best=null;
    bound.forEach(function(a){
      ["prior","cur","change"].forEach(function(k){
        var v=qtyOf(a,k),gap=Math.abs(Math.abs(f.v)-Math.abs(v));
        if(near(f.v,v,TOL_D)){
          if(want===k&&!hit)hit={a:a,k:k};
          else alts.push(qtyName(k)+" on "+acctId(a));
        }
        if(best===null||gap<best.gap)best={gap:gap,txt:qtyName(k)+" on "+acctId(a)+" is "+money(v)};
      });
    });
    var plainNote=f.plain?" Read as an ordinary number with no currency punctuation, so the unit is assumed to be dollars."
                         :"";
    if(hit){
      if(f.signed&&Math.abs(f.v-qtyOf(hit.a,hit.k))>TOL_D){
        return {st:"failed",txt:f.raw+" is written with a sign of its own and the "+qtyName(hit.k)+" on "+
          acctId(hit.a)+" is "+money(qtyOf(hit.a,hit.k))+", so the signs disagree."+plainNote,
          ask:"Which sign is right on this figure?"};
      }
      return {st:"checked",txt:f.raw+" is the "+f.role+" on "+acctId(hit.a)+", "+money(qtyOf(hit.a,hit.k))+
        " unrounded, and the role was read from "+f.roleFrom+"."+plainNote,ask:""};
    }
    if(!want){
      if(alts.length===1){
        return {st:"review",txt:f.raw+": the words around it do not say what it is, and it equals the "+alts[0]+
          ". Confirm the role before this figure counts as checked."+plainNote,
          ask:"What is "+f.raw+" in this sentence: a prior balance, a current balance, a movement or a ratio?"};
      }
      if(alts.length>1){
        return {st:"review",txt:f.raw+": the words around it do not say what it is, and it equals more than one "+
          "ledger figure ("+alts.join("; ")+")."+plainNote,
          ask:"What is "+f.raw+" in this sentence, and on which line?"};
      }
      return {st:"failed",txt:f.raw+": the words around it do not say what it is and it equals nothing on the "+
        "bound line. Nearest is "+(best?best.txt:"nothing at all")+"."+plainNote,
        ask:"Where did "+f.raw+" come from?"};
    }
    if(alts.length){
      return {st:"failed",txt:f.raw+" is written as the "+f.role+" (read from "+f.roleFrom+"), but on "+
        acctId(bound[0])+" the "+f.role+" is "+money(qtyOf(bound[0],want))+". "+f.raw+" is the "+alts[0]+"."+plainNote,
        ask:"Is the figure wrong or is the wording wrong?"};
    }
    /* a figure computed across two bound lines, such as gross profit from a
       revenue line and a cost line, is not something the ledger holds. It is
       reported as what it looks like and left to a person, never passed. */
    var combo=null;
    if(all.length>1){
      all.forEach(function(a){
        all.forEach(function(b){
          if(combo||a===b)return;
          ["prior","cur","change"].forEach(function(k){
            if(combo)return;
            if(exactly(f.v,qtyOf(a,k)-qtyOf(b,k),TOL_D))
              combo="the "+qtyName(k)+" on "+acctId(a)+" less the "+qtyName(k)+" on "+acctId(b);
            else if(exactly(f.v,qtyOf(a,k)+qtyOf(b,k),TOL_D))
              combo="the "+qtyName(k)+" on "+acctId(a)+" plus the "+qtyName(k)+" on "+acctId(b);
          });
        });
      });
    }
    if(combo){
      return {st:"review",txt:f.raw+" is written as the "+f.role+", read from "+f.roleFrom+", and it is not a "+
        f.role+" on any line this sentence binds. It is "+combo+". The checker was not told that is what it "+
        "is, so it is left open."+plainNote,
        ask:"Is "+f.raw+" a figure computed across two lines, and where is that computation set out?"};
    }
    var expected=bound.map(function(a){return "the "+f.role+" on "+acctId(a)+" is "+money(qtyOf(a,want));}).join("; ");
    return {st:"failed",txt:"memo says "+f.raw+" as the "+f.role+"; "+expected+". Nearest ledger figure: "+
      (best?best.txt:"nothing on the bound line comes close")+"."+plainNote,
      ask:"Which figure is right, the memo or the ledger, and where did the memo's number come from?"};
  }

  function checkPercent(f,bound,ratios,zp){
    var cands=[],i,hit=null,signClash=null;
    bound.forEach(function(a){
      if(a.pct!==null)cands.push({lab:acctId(a)+" percent change",v:a.pct,kind:"relative movement"});
    });
    ratios.forEach(function(r){
      cands.push({lab:r.name+", prior month",v:r.prior,kind:"ratio",side:"prior"});
      cands.push({lab:r.name+", current month",v:r.cur,kind:"ratio",side:"current"});
      cands.push({lab:r.name+", change in points",v:r.change,kind:"rate change in points"});
    });
    function wanted(c){
      if(f.role==="relative movement")return c.kind==="relative movement";
      if(f.role==="ratio")return c.kind==="ratio"&&(!f.side||c.side===f.side);
      if(f.role==="rate change in points")return c.kind==="rate change in points";
      return true;
    }
    /* A role the words do not give cannot be settled by the fact that the figure
       happens to equal something. The reviewer confirms it in the dropdown beside
       the row, and the run after that is the one that can call it checked. */
    if(f.role==="unknown"){
      cands.sort(function(x,y){return Math.abs(Math.abs(f.v)-Math.abs(x.v))-Math.abs(Math.abs(f.v)-Math.abs(y.v));});
      var eq=cands.filter(function(c){return near(f.v,c.v,TOL_P);});
      /* a sign written into the memo is a claim the words did give, and it is
         tested whatever the role turns out to be */
      var sc=eq.filter(function(c){return f.signed&&Math.abs(f.v-c.v)>TOL_P;});
      if(sc.length&&sc.length===eq.length){
        return {st:"failed",txt:f.raw+" is written with a sign of its own; "+sc[0].lab+" is "+pctTxt(sc[0].v)+
          ", so the magnitudes agree and the signs do not.",
          ask:"Which way did this move, and is the sign in the memo right?"};
      }
      return {st:"review",txt:f.raw+": the words around it do not say what it measures"+
        (eq.length?", and it equals "+eq.map(function(c){return c.lab+" at "+pctTxt(c.v);}).join("; ")+
          ". Equalling a figure is not the same as being that figure":
          ", and it equals nothing the checker holds")+
        ". Confirm the role beside this row before it counts as checked.",
        ask:"What is "+f.raw+" in this sentence: the movement on the line, a ratio, or something else?"};
    }
    for(i=0;i<cands.length;i++){
      if(!wanted(cands[i]))continue;
      if(near(f.v,cands[i].v,TOL_P)){
        if(f.signed&&Math.abs(f.v-cands[i].v)>TOL_P){signClash=cands[i];continue;}
        hit=cands[i];break;
      }
    }
    if(signClash&&!hit){
      return {st:"failed",txt:f.raw+" is written with a sign of its own; "+signClash.lab+" is "+pctTxt(signClash.v)+
        ", so the magnitudes agree and the signs do not.",
        ask:"Which way did this move, and is the sign in the memo right?"};
    }
    if(hit){
      return {st:"checked",via:hit.kind==="relative movement"?"line":"ratio",
        txt:f.raw+" is the "+f.role+", "+hit.lab+" at "+pctTxt(hit.v)+" unrounded, and the role "+
        "was read from "+f.roleFrom+".",ask:""};
    }
    if(f.unit==="percentage points"&&!ratios.length){
      return {st:"review",txt:f.raw+" is written in percentage points, which measure a change in a rate. The bound "+
        "line is a dollar balance and no ratio was supplied, so there is nothing to compare it with.",
        ask:"What rate is moving by these points, and where is it computed?"};
    }
    if(f.role==="relative movement"&&bound.length&&bound[0].pct===null){
      return {st:"review",txt:f.raw+" is written as the relative movement, and "+acctId(bound[0])+" has a zero prior "+
        "balance, so no percentage exists to compare it with. Zero prior balance policy in force: "+zp+".",
        ask:"What is this percent measured against?"};
    }
    if(f.role==="ratio"&&!ratios.length){
      return {st:"review",txt:f.raw+" is written as a ratio for the "+(f.side||"period")+", and no ratio was supplied "+
        "in the ratio pane, so the checker has nothing to compute it from.",
        ask:"Which ratio is this, and how is it computed from the ledger?"};
    }
    cands.sort(function(x,y){return Math.abs(Math.abs(f.v)-Math.abs(x.v))-Math.abs(Math.abs(f.v)-Math.abs(y.v));});
    var three=cands.slice(0,3).map(function(c){return c.lab+" "+pctTxt(c.v);});
    /* the words said what this percent is and the ledger says otherwise. A
       reviewer who believes it is a ratio the checker was never told about can say
       so in the role dropdown beside this row, and it becomes an open ratio
       question instead of a failure. */
    if(f.role==="relative movement"&&bound.length&&bound[0].pct!==null){
      return {st:"failed",txt:f.raw+" is written as the relative movement, read from "+f.roleFrom+", and the "+
        "relative movement on "+acctId(bound[0])+" is "+pctTxt(bound[0].pct)+" unrounded. Nearest values: "+
        (three.length?three.join("; "):"nothing else on the bound line")+".",
        ask:"Is this percent the movement on the line, or a ratio the checker was not told about? Confirm the role "+
          "beside this row if it is a ratio."};
    }
    return {st:"review",txt:f.raw+" ties to nothing the checker holds"+(f.role==="unknown"
        ?", and the words around it do not say what it measures":" as a "+f.role)+
      ". Nearest values: "+(three.length?three.join("; "):"nothing on the bound line and no ratio supplied")+".",
      ask:"What is this percent measuring, and where is it computed?"};
  }

  /* ---------- 5. THRESHOLD POLICY CLAIMS -----------------------------------
     A sentence that asserts something about the commentary rule is checked
     against the rule as set, which is the one case where a sentence carrying no
     figure can still be checked within scope. */
  function policyClaims(text){
    var t=" "+text.toLowerCase().replace(/\s+/g," ")+" ",out=[];
    if(/fails (both legs|the threshold on both)|clears neither leg|meets neither leg|neither leg (of the threshold )?is met/.test(t))out.push({leg:"both",met:false});
    else{
      if(/fails the dollar leg|fails the dollar test|below the dollar leg/.test(t))out.push({leg:"dollar",met:false});
      if(/fails the percent(age)? leg|fails the percent(age)? test|below the percent(age)? leg/.test(t))out.push({leg:"percent",met:false});
    }
    if(/carries no driver|carries no commentary|owes no commentary|no commentary (is )?owed|owes no explanation|this line carries no driver/.test(t))
      out.push({owes:false});
    return out;
  }

  /* ============================================================ ratios */
  function tokenizeExpr(x){
    var s=" "+x.toLowerCase()+" ";
    s=s.replace(/\bdivided by\b/g," / ").replace(/\bdivide by\b/g," / ").replace(/\bdivide\b/g," / ")
       .replace(/\bover\b/g," / ").replace(/\btimes\b/g," * ").replace(/\bmultiplied by\b/g," * ")
       .replace(/\bplus\b/g," + ").replace(/\bminus\b/g," - ").replace(/\bless\b/g," - ");
    var toks=s.match(/\d+|[()+\-*\/]/g);
    var junk=s.replace(/\d+|[()+\-*\/\s]/g,"");
    return {toks:toks||[],junk:junk};
  }
  function parseRatios(text,byNum){
    var out=[],errs=[];
    String(text).split(/\r?\n/).forEach(function(raw){
      var line=raw.replace(/^\s+|\s+$/g,"");
      if(!line)return;
      var i=line.indexOf("=");
      var name=i>-1?line.slice(0,i).replace(/^\s+|\s+$/g,""):"Ratio "+(out.length+1);
      var expr=i>-1?line.slice(i+1):line;
      var tk=tokenizeExpr(expr);
      if(tk.junk){errs.push(name+": cannot read \""+tk.junk.replace(/\s+/g," ")+"\"");return;}
      if(!tk.toks.length){errs.push(name+": nothing to compute");return;}
      var vals={};
      var ok=true,said={};
      ["prior","cur"].forEach(function(mo){
        try{vals[mo]=evalToks(tk.toks.slice(),byNum,mo)*100;}
        catch(e){ok=false;if(!said[e.message]){said[e.message]=1;errs.push(name+": "+e.message);}}
      });
      if(!ok)return;
      if(!isFinite(vals.prior)||!isFinite(vals.cur)){errs.push(name+": the ratio does not compute on these balances");return;}
      out.push({name:name,expr:expr.replace(/\s+/g," ").replace(/^\s+|\s+$/g,""),
                prior:vals.prior,cur:vals.cur,change:vals.cur-vals.prior});
    });
    return {ratios:out,errs:errs};
  }
  function evalToks(toks,byNum,month){
    var pos=0;
    function peek(){return toks[pos];}
    function factor(){
      var t=toks[pos++];
      if(t===undefined)throw new Error("the expression stops early");
      if(t==="("){var v=expr();if(toks[pos++]!==")")throw new Error("a bracket is not closed");return v;}
      if(t==="-")return -factor();
      if(t==="+")return factor();
      if(/^\d+$/.test(t)){
        var a=byNum[t];
        if(!a)throw new Error("no account "+t+" in the ledger");
        return month==="prior"?a.prior:a.cur;
      }
      throw new Error("cannot read \""+t+"\"");
    }
    function term(){
      var v=factor(),op,r;
      while(peek()==="*"||peek()==="/"){
        op=toks[pos++];r=factor();
        if(op==="/"){if(r===0)throw new Error("that ratio divides by zero");v=v/r;}
        else v=v*r;
      }
      return v;
    }
    function expr(){
      var v=term(),op;
      while(peek()==="+"||peek()==="-"){op=toks[pos++];v=(op==="+")?v+term():v-term();}
      return v;
    }
    var val=expr();
    if(pos<toks.length)throw new Error("there is something extra after the expression");
    return val;
  }

  /* ============================================================ direction */
  var UP=["rose","rise","rises","risen","rising","increased","increase","increases","increasing",
          "grew","grow","grows","growth","growing","up","higher","climbed","climb","climbs","gained","jumped","added",
          "advanced","advance","advances","expanded","expand","expands","expansion","surged","surge","surges",
          "accelerated","accelerate","accelerates"];
  var DOWN=["fell","fall","falls","fallen","falling","declined","decline","declines","declining",
            "decreased","decrease","decreases","decreasing","down","lower","dropped","drop","drops","reduced","shrank",
            "eased","ease","eases","easing","softened","soften","softens","softening",
            "slipped","slip","slips","receded","recede","recedes"];
  /* "flat" is a direction too, and it is tested against a movement inside half a percent of zero */
  /* "flat" is a direction too. Two kinds. A no-change claim, "unchanged", "remained
     at", "held at", "stayed the same", asserts zero movement and is tested against
     a movement of zero to the half cent. A flat claim, "flat", "steady", "stable",
     is tested against a movement inside half a percent of zero. */
  var STILLW=["unchanged","unmoved","no change","no movement","no net change","held at","holds at","remained at",
              "remains at","remain at","stayed at","stays at","stay at","kept at","continued at","maintained at",
              "remained unchanged","stayed unchanged","remained the same","stayed the same","remained constant",
              "stayed constant","held constant","was constant","were constant","level with"];
  var FLATW=["held flat","held steady","held level","flat","steady","remained flat","stayed flat",
             "remained steady","stayed steady","remained level","stayed level","remained stable","stayed stable"]
            .concat(STILLW);
  /* "remained" or "stayed" written straight in front of a figure is the same claim */
  var STILL_FIG=/\b(remain(?:ed|s)?|stay(?:ed|s)?)\s+(?:\$|\(|-?[0-9])/i;
  var FLAT_TOL=0.5;
  function dirWords(txt){
    var t=" "+txt.toLowerCase().replace(/[^a-z\s]/g," ").replace(/\s+/g," ")+" ",out=[];
    UP.forEach(function(w){if(t.indexOf(" "+w+" ")>-1)out.push({w:w,d:1});});
    DOWN.forEach(function(w){if(t.indexOf(" "+w+" ")>-1)out.push({w:w,d:-1});});
    return out;
  }
  function flatWord(txt){
    var t=" "+txt.toLowerCase().replace(/[^a-z\s]/g," ").replace(/\s+/g," ")+" ",found=null,m;
    FLATW.forEach(function(w){
      if(t.indexOf(" "+w+" ")>-1&&(!found||w.length>found.length))found=w;
    });
    if(!found&&(m=String(txt).match(STILL_FIG)))found=m[1].toLowerCase();
    return found;
  }
  /* a no-change word, as against a flat word */
  function stillWord(w){
    return !!w&&(STILLW.indexOf(w)>-1||/^(?:remain|stay)/.test(w));
  }
  /* a movement the checker will let a "flat" claim stand on */
  function isFlat(a){
    if(a.pct===null)return a.change===0;
    return Math.abs(a.pct)<=FLAT_TOL;
  }
  /* a movement a no-change claim stands on: none, to the half cent */
  function isStill(a){
    return Math.abs(a.change)<=TOL_D;
  }
  function flatAgrees(w,a){return stillWord(w)?isStill(a):isFlat(a);}
  /* Clauses, with the offsets kept so a figure can be placed in the clause it was
     written in. A comma inside a figure is part of the figure, never a break, and
     the guard character is one character wide so every offset still lines up. */
  var RE_COARSE=/[,;:]|\bso\b|\bbecause\b|\bwhile\b|\bbut\b|\bas\b|\bafter\b|\bbefore\b|\bwhich\b|\bthough\b/gi;
  var RE_FINE=/[,;:]|\bso\b|\bbecause\b|\bwhile\b|\bwhereas\b|\bbut\b|\bas\b|\bafter\b|\bbefore\b|\bwhich\b|\bthough\b|\band\b|\bor\b|\bagainst\b|\bversus\b|\bcompared\s+(?:with|to)\b|\brelative\s+to\b|\boffset\s+by\b|\balongside\b|\brather\s+than\b|\binstead\s+of\b/gi;
  function spansOf(txt,re){
    var t=String(txt).replace(/(\d),(\d)/g,"$1\u0001$2"),out=[],last=0,m;
    re.lastIndex=0;
    while((m=re.exec(t))!==null){
      if(m.index>last)out.push([last,m.index]);
      last=m.index+m[0].length;
      if(m[0].length===0)re.lastIndex++;
    }
    if(last<t.length)out.push([last,t.length]);
    return out.map(function(p){return {at:p[0],end:p[1],text:String(txt).slice(p[0],p[1])};})
              .filter(function(c){return c.text.replace(/\s/g,"")!=="";});
  }
  function clausesOf(txt){
    return spansOf(txt,RE_COARSE).map(function(c){return c.text;});
  }
  /* ---------- NEGATION -----------------------------------------------------
     not, no, never, neither, without, rather than, instead of and the contracted
     forms. A negated clause is not read as the claim it would be without the
     negation, and it is not read as its opposite either: the checker says it
     cannot settle it and the reviewer does. The threshold idioms a memo uses to
     say a line owes nothing are not negations of a figure or a direction, so they
     are taken out before the test. */
  var NEG_RE=/\b(?:did|do|does|was|were|is|are|has|have|had|could|would|will|can|shall|should|may|might|must)\s+not\b|\bnot\b|\bnever\b|\bnor\b|\bneither\b|\bwithout\b|\brather\s+than\b|\binstead\s+of\b|\bfailed\s+to\b|\bno\b|n['\u2019]t\b/i;
  function negationIn(t){
    var x=" "+String(t).replace(/\s+/g," ")+" ";
    x=x.replace(/\bno\s+(?:commentary|drivers?|explanations?|reasons?|comments?|such)\b/gi," ")
       .replace(/\bno\s+(?:change|movement)\b/gi," ")
       .replace(/\bneither\s+leg\b/gi," ")
       .replace(/\bnot\s+(?:listed|supplied|broken\s+out|yet)\b/gi," ");
    var m=x.match(NEG_RE);
    return m?m[0].replace(/^\s+|\s+$/g,""):null;
  }
  function claimIn(t){
    return !!(figures(t).length||dirWords(t).length||flatWord(t));
  }

  /* ============================================================ the parse preview */
  var USERCOLS=null,PVTIMER=null,PVSIG="";

  function colChoice(){return USERCOLS;}


    /* ---- from checker.html 1591-1614 ---- */
  var RANK={"checked within scope":0,"not checked":1,"needs review":2,"failed":3};
  var BADGE={"checked within scope":"pass","not checked":"info","needs review":"review","failed":"fail"};
  function worse(a,b){return RANK[b]>RANK[a]?b:a;}

  var ROLE_OPTIONS=["prior balance","current balance","absolute movement","relative movement","ratio"];

  function zeroPolicyText(zp){
    return zp==="exclude"
      ? "a line with a zero prior balance is excluded from the rule"
      : "a line with a zero prior balance is treated as owing commentary on any movement (the default)";
  }
  function srcVersion(sig){
    var h=5381,i;
    for(i=0;i<sig.length;i++)h=((h<<5)+h+sig.charCodeAt(i))|0;
    return "src-"+(h>>>0).toString(36)+"-"+sig.length;
  }


    /* ---- from checker.html 2092-2159: the direction check ---- */
  function directionOn(s){
    if(!s.bound.length)return null;
    var bad=[],good=[],anchored=[],voided=[],loose=[],open=[],prevEnd=0;
    spansOf(s.text,RE_COARSE).forEach(function(sp){
      var c=sp.text,sep=s.text.slice(prevEnd,sp.at).replace(/^\s+|\s+$/g,"").toLowerCase();
      prevEnd=sp.end;
      var cf=figures(c,s.numset),anchor=null,neg=negationIn(c);
      dollarsIn(cf).forEach(function(d){
        if(anchor)return;
        s.bound.forEach(function(a){
          if(anchor)return;
          if(near(d.v,a.prior,TOL_D)||near(d.v,a.cur,TOL_D)||near(d.v,a.change,TOL_D))anchor=a;
        });
      });
      if(neg&&(flatWord(c)||dirWords(c).length)){
        voided.push("the words negate this clause (“"+neg+"”), so what it claims about the direction of "+
          (anchor?acctId(anchor):s.bound.map(acctId).join("; "))+" is not settled by the checker");
        if(anchor)anchored.push(c);
        return;
      }
      if(!anchor){
        if(flatWord(c)||dirWords(c).length)open.push({text:c,sep:sep});
        return;
      }
      anchored.push(c);
      testClause(c,anchor);
    });
    function testClause(c,anchor){
      var sign=anchor.change>0?1:(anchor.change<0?-1:0);
      var anm=acctId(anchor),fw=flatWord(c);
      if(fw){
        if(flatAgrees(fw,anchor))good.push("\""+fw+"\" agrees with "+anm+", which moved "+money(anchor.change)+
          (anchor.pct===null?"":", "+pctTxt(anchor.pct))+(stillWord(fw)?", which is no movement at all":", inside half a percent of no movement"));
        else bad.push("the memo says \""+fw+"\" but "+anm+" "+(sign>0?"rose ":"fell ")+
          money(Math.abs(anchor.change))+(anchor.pct===null?"":" ("+pctTxt(anchor.pct)+")"));
      }
      dirWords(c).forEach(function(w){
        if(sign===0){bad.push("the memo says \""+w.w+"\" but "+anm+" did not move at all");return;}
        if(w.d===sign)good.push("\""+w.w+"\" agrees with "+anm);
        else bad.push("the memo says \""+w.w+"\" but "+anm+" "+(sign>0?"rose ":"fell ")+
          money(Math.abs(anchor.change))+(anchor.pct===null?"":" ("+pctTxt(anchor.pct)+")"));
      });
    }
    if(anchored.length){
      /* a direction or no-change word in a clause of its own, beside a clause the
         figures did tie. Where that clause names one bound line it is tested
         against that line; where it names none and disagrees with the lines the
         sentence binds, it is held, because the checker cannot tell what it
         describes. */
      open.forEach(function(o){
        var c=o.text;
        var ct=" "+c.toLowerCase().replace(/[^a-z0-9\s]/g," ").replace(/\s+/g," ")+" ",named=[];
        s.bound.forEach(function(a){
          if((a.num&&new RegExp("(^|[^0-9])"+a.num+"([^0-9]|$)").test(c))||
             (a.flat&&ct.indexOf(" "+a.flat+" ")>-1)||(a.two&&a.two.indexOf(" ")>-1&&ct.indexOf(" "+a.two+" ")>-1))named.push(a);
        });
        if(named.length===1){testClause(c,named[0]);return;}
        /* a clause opened by "as", "because", "while" and the like names a cause or a
           contrast, and its direction word is about that, unless it points back at
           the line with "it" or names no one else */
        if(/^(?:so|because|while|but|as|after|before|though)$/.test(o.sep)&&!named.length&&
           !/^\s*(?:it|its|the\s+(?:line|account|balance))\b/i.test(c))return;
        var fw=flatWord(c),words=dirWords(c),agrees=false;
        s.bound.forEach(function(a){
          var sign=a.change>0?1:(a.change<0?-1:0);
          if(fw&&flatAgrees(fw,a))agrees=true;
          words.forEach(function(w){if(w.d===sign)agrees=true;});
        });
        if(!agrees)loose.push("\""+(fw||words.map(function(w){return w.w;}).join("\", \""))+"\" stands in a clause that "+
          "ties to no figure and names no line, and it does not agree with "+s.bound.map(acctId).join("; ")+
          ", so the checker cannot tell what it describes");
      });
      return {bad:bad,good:good,voided:voided,loose:loose};
    }
    if(voided.length)return {bad:bad,good:good,voided:voided,loose:loose};
    var sneg=negationIn(s.text);
    if(sneg&&(flatWord(s.text)||dirWords(s.text).length)){
      voided.push("the words negate this sentence (“"+sneg+"”), so what it claims about the "+
        "direction is not settled by the checker");
      return {bad:bad,good:good,voided:voided,loose:loose};
    }
    var sfw=flatWord(s.text);
    if(sfw){
      var fok=false,fnames=[];
      s.bound.forEach(function(a){
        fnames.push(acctId(a)+" moved "+money(a.change)+(a.pct===null?"":", "+pctTxt(a.pct)));
        if(flatAgrees(sfw,a))fok=true;
      });
      if(fok)good.push("\""+sfw+"\" agrees with the bound line");
      else if(fnames.length)bad.push("the memo says \""+sfw+"\" but "+fnames.join(" and "));
    }
    dirWords(s.text).forEach(function(w){
      var agrees=false,names=[];
      s.bound.forEach(function(a){
        var sign=a.change>0?1:(a.change<0?-1:0);
        if(sign===0)return;
        names.push(acctId(a)+" "+(sign>0?"rose":"fell"));
        if(w.d===sign)agrees=true;
      });
      if(!names.length)return;
      if(agrees)good.push("\""+w.w+"\" agrees with the bound line");
      else bad.push("the memo says \""+w.w+"\" but "+names.join(" and "));
    });
    return {bad:bad,good:good,voided:voided,loose:loose};
  }

  root.SecondPassCore = {
    OUTSIDE_WHY: OUTSIDE_WHY,
    BOUND_AFTER: BOUND_AFTER,
    STILLW: STILLW,
    LABEL_BEFORE: LABEL_BEFORE,
    SLASH_RE: SLASH_RE,
    DECWORD_RE: DECWORD_RE,
    FRAC_RE: FRAC_RE,
    MULT_RE: MULT_RE,
    ODD_NUM_RE: ODD_NUM_RE,
    flatAgrees: flatAgrees,
    isStill: isStill,
    stillWord: stillWord,
    countStop: countStop,
    oddQuantities: oddQuantities,
    wordsToNumber: wordsToNumber,
    wordNumbers: wordNumbers,
    nowMs: nowMs,
    money: money,
    pctTxt: pctTxt,
    parseNum: parseNum,
    splitFields: splitFields,
    deSmart: deSmart,
    monthKey: monthKey,
    guessCols: guessCols,
    acctShape: acctShape,
    parseLedger: parseLedger,
    tieTotals: tieTotals,
    legs: legs,
    clears: clears,
    pctCell: pctCell,
    pctPhrase: pctPhrase,
    splitSentences: splitSentences,
    parseFig: parseFig,
    numberWords: numberWords,
    strayNumbers: strayNumbers,
    figures: figures,
    dollarsIn: dollarsIn,
    pctsIn: pctsIn,
    dirSet: dirSet,
    roleOf: roleOf,
    near: near,
    exactly: exactly,
    acctId: acctId,
    bindSentence: bindSentence,
    clauseBind: clauseBind,
    qtyOf: qtyOf,
    qtyName: qtyName,
    checkDollar: checkDollar,
    checkPercent: checkPercent,
    policyClaims: policyClaims,
    tokenizeExpr: tokenizeExpr,
    parseRatios: parseRatios,
    evalToks: evalToks,
    dirWords: dirWords,
    flatWord: flatWord,
    isFlat: isFlat,
    spansOf: spansOf,
    clausesOf: clausesOf,
    negationIn: negationIn,
    claimIn: claimIn,
    worse: worse,
    zeroPolicyText: zeroPolicyText,
    srcVersion: srcVersion,
    directionOn: directionOn,
    STOP: STOP,
    SECTION_ONLY: SECTION_ONLY,
    TOTALWORD: TOTALWORD,
    GRAND: GRAND,
    HEADERWORD: HEADERWORD,
    DERIVEDCOL: DERIVEDCOL,
    MONTHNUM: MONTHNUM,
    FOREIGN_BEFORE: FOREIGN_BEFORE,
    FOREIGN_AFTER: FOREIGN_AFTER,
    SCALE_AFTER: SCALE_AFTER,
    NUMWORD_RE: NUMWORD_RE,
    UNIT_AFTER: UNIT_AFTER,
    CUE_PRIOR: CUE_PRIOR,
    CUE_CURRENT: CUE_CURRENT,
    CUE_MOVE: CUE_MOVE,
    MOVE_NOUN: MOVE_NOUN,
    SKIPW: SKIPW,
    TOL_P: TOL_P,
    TOL_D: TOL_D,
    ROLE_QTY: ROLE_QTY,
    UP: UP,
    DOWN: DOWN,
    FLATW: FLATW,
    FLAT_TOL: FLAT_TOL,
    RE_COARSE: RE_COARSE,
    RE_FINE: RE_FINE,
    NEG_RE: NEG_RE,
    RANK: RANK,
    BADGE: BADGE,
    ROLE_OPTIONS: ROLE_OPTIONS
  };
})(typeof window !== "undefined" ? window : this);
