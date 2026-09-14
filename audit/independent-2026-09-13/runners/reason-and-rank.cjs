// Replays the third review's probe-reason-scoring.cjs against a given tree's index.html.
// usage: node reason-and-rank.cjs <game-root> <out.json>
const fs=require('fs'),path=require('path'),vm=require('vm');
const [root,outFile]=process.argv.slice(2);
const text=fs.readFileSync(path.join(root,'index.html'),'utf8');
const points=text.slice(text.indexOf('var PT_CALL'),text.indexOf('var LINE_PTS'));
const reasons=text.slice(text.indexOf('function basisKeyOf'),text.indexOf('function reasonRightAt'));
const s={window:{},CARDS:[]};vm.createContext(s);vm.runInContext(points+'\n'+reasons,s);
const results=[];
for(const file of ['halyard-v4.json','brightwater-v5.json','brightwater-v6.json','kestrel-v1.json']){
 if(!fs.existsSync(path.join(root,'cases',file)))continue;
 const c=JSON.parse(fs.readFileSync(path.join(root,'cases',file),'utf8'));
 s.buildRanks(c.cards);
 for(const policy of ['keyedReasons','wrongReasons']){
  let score=0,streak=0;
  for(const card of c.cards){const chips=policy==='keyedReasons'?card.basisKey:['wrong account']; const p=s.linePoints(card,card.key,chips,streak);score+=p.total;streak=p.streakAt;}
  const rank=s.RANKS.filter(r=>score>=r.at).at(-1)?.name;
  results.push({file,policy,correctDecisions:c.cards.length,points:score,rank,max:s.RANK_MAX});
 }
}
fs.writeFileSync(outFile,JSON.stringify(results,null,2));results.forEach(x=>console.log(JSON.stringify(x)));
