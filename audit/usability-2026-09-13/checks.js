/* In-page checks returned as JSON: sideways overflow, clipped content, text under 12px, squashed images. */
(function(){
  var out={overflow:[],clipped:[],small:[],images:[]};
  var W=document.documentElement.clientWidth;
  var all=document.querySelectorAll('body *');
  function name(e){var c=(typeof e.className==='string'&&e.className.trim())?'.'+e.className.trim().split(/\s+/).slice(0,2).join('.'):'';return (e.id?'#'+e.id:e.tagName.toLowerCase())+c;}
  function visible(e){var cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden'||+cs.opacity===0)return false;var r=e.getBoundingClientRect();return r.width>0&&r.height>0;}
  for(var i=0;i<all.length;i++){
    var e=all[i];
    if(/^(SCRIPT|STYLE|svg|path|g|rect|line|text|polygon|circle|tspan|polyline|ellipse)$/i.test(e.tagName)) continue;
    if(!visible(e)) continue;
    var cs=getComputedStyle(e), r=e.getBoundingClientRect();
    if((cs.overflowX==='auto'||cs.overflowX==='scroll')&&e.scrollWidth>e.clientWidth+1) out.overflow.push(name(e)+' scrolls '+e.scrollWidth+'>'+e.clientWidth);
    if(r.right>W+1&&cs.position!=='fixed'){var p=e.parentElement,cl=false;while(p&&p!==document.body){var pc=getComputedStyle(p);if(pc.overflowX!=='visible'){cl=true;break;}p=p.parentElement;}if(!cl) out.overflow.push(name(e)+' past edge '+Math.round(r.right));}
    var form=/^(TEXTAREA|INPUT|SELECT|HTML|BODY)$/.test(e.tagName)||e.clientWidth<=2||e.clientHeight<=2;
    if(!form&&(cs.overflowX==='hidden'||cs.overflowX==='clip')&&e.scrollWidth>e.clientWidth+2&&e.textContent.trim()) out.clipped.push(name(e)+' w '+e.scrollWidth+'>'+e.clientWidth);
    if(!form&&(cs.overflowY==='hidden'||cs.overflowY==='clip')&&e.scrollHeight>e.clientHeight+2&&e.textContent.trim()) out.clipped.push(name(e)+' h '+e.scrollHeight+'>'+e.clientHeight);
    var own=Array.prototype.some.call(e.childNodes,function(n){return n.nodeType===3&&n.textContent.trim().length>1;});
    if(own&&parseFloat(cs.fontSize)<12&&!e.closest('[aria-hidden=true]')) out.small.push(name(e)+' '+cs.fontSize+' "'+e.textContent.trim().slice(0,40)+'"');
    if(e.tagName==='IMG'&&e.naturalWidth){var nr=e.naturalWidth/e.naturalHeight, rr=r.width/r.height, sc=r.width/e.naturalWidth;
      out.images.push(name(e)+' '+e.getAttribute('src')+(Math.abs(nr-rr)/nr>0.05?' SQUASHED natural '+nr.toFixed(2)+' shown ':' ok ')+Math.round(r.width)+'x'+Math.round(r.height)+' scale '+sc.toFixed(2));}
  }
  Array.prototype.forEach.call(document.querySelectorAll('svg text'),function(t){var s=t.closest('svg');if(!s||!visible(s)||!t.textContent.trim())return;
    var vb=s.viewBox&&s.viewBox.baseVal, sc=(vb&&vb.width)?s.getBoundingClientRect().width/vb.width:1;
    var fs=parseFloat(getComputedStyle(t).fontSize)*sc; if(fs<12) out.small.push('svg text '+fs.toFixed(1)+'px "'+t.textContent.trim().slice(0,30)+'"');});
  Array.prototype.forEach.call(document.querySelectorAll('button,.btn,.chip'),function(b){if(!visible(b))return;if(b.scrollWidth>b.clientWidth+2) out.clipped.push('control '+name(b)+' "'+b.textContent.trim().slice(0,30)+'" '+b.scrollWidth+'>'+b.clientWidth);});
  var d=document.documentElement;
  out.doc=d.scrollWidth+'/'+d.clientWidth;
  for(var k in out) if(Array.isArray(out[k])&&out[k].length>20) out[k]=out[k].slice(0,20).concat(['...+'+(out[k].length-20)+' more']);
  return out;
})()
