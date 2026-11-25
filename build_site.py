import os, re, sys, shutil, json
os.chdir('/home/claude/zines/found2')
sys.argv=['x','local']
sys.path.insert(0,'/home/claude/zines/found2')
import found2 as F          # page builders for the found poetry zine
os.chdir('/home/claude/zines'); sys.argv=['x','local']; sys.path.insert(0,'/home/claude/zines')
import importlib.util
R=os.environ.get('R','/home/claude/ezines')
os.chdir(R)
IMG=f'{R}/assets/img'
def fix(h,rel='../'):
    def cp(m):
        src=m.group(1); name=os.path.basename(src); name=({'60046b36.png':'book.png','aaa517c0.png':'flowers.png','dcc899d5.png':'gypsophila.png'}.get(name.split('-')[-1],name))
        shutil.copy(src,f'{IMG}/{name}'); return rel+'assets/img/'+name
    h=re.sub(r'file://(/\S+?\.png)',cp,h)
    return h
SHELL='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../assets/css/fonts.css">
<link rel="stylesheet" href="../assets/css/flip.css">
<style>{css}</style>
</head>
<body>
{pre}
<div class="top"><a href="../">&larr; the shelf</a><span>{pdf}</span></div>
<div class="hint" id="hint">{hint}</div>
<div class="stage" id="stage"></div>
<div class="nav"><button id="prev">&larr;</button><span class="ct" id="ct"></span><button id="next">&rarr;</button></div>
<div id="src" style="display:none">
{pages}
</div>
<script src="../assets/js/flip.js"></script>
<script>
const pages=[...document.querySelectorAll('#src > .pg')];
const fb=new Flipbook({{stage:document.getElementById('stage'),pw:{pw},ph:{ph},pages,maxScale:{ms},onchange:(p,L,label,mode)=>{{document.getElementById('ct').textContent=label;document.getElementById('prev').disabled=p===0;if(p>0){{const h=document.getElementById('hint');if(h)h.style.opacity=0}}document.getElementById('next').disabled=(mode==='single')?p===L-1:p===L;}}}});
document.getElementById('prev').onclick=()=>fb.prev();document.getElementById('next').onclick=()=>fb.next();
{js}
</script>
</body>
</html>
'''
def sub(h,m): 
    for k,v in m.items(): h=h.replace('{{'+k+'}}',v)
    return h
# ---------------- FOUND POETRY ----------------
FM={'ink':'#2a2a2a','acc':'#1f7a6d','paper':'#fff'}
def fpage(inner): return f'<div class="pg"><div class="in">{inner}</div></div>'
S=F.S;C=F.C;INK=F.INK;ACC=F.ACC
# blackout
words=F.words;kept=F.kept
ws=' '.join(f'<span class="w{" keep" if n in kept else ""}" data-i="{n}">{w}</span>' for n,w in enumerate(words))
black=(F.lab('method one')+F.big(['blackout'],30)
 +F.p('take a page from an old letter, a magazine, or an old book. circle the words that stand out to you, then cross out, color or black out the rest. read the words you’ve collected out loud.',11,2)
 +f'<div class="nudge" style="font-family:{C};font-size:17px;line-height:1;color:{ACC};position:relative;z-index:1;margin:2px 0 4px">&#9998; your turn: tap any word to black it out. tap again to bring it back.</div>'
 +f'<div id="bo" style="font-family:{S};font-size:10px;line-height:1.65;color:{INK};position:relative;z-index:1;margin-top:2px">{ws}</div>'
 +f'<div id="bopoem" style="font-family:{S};font-size:11.5px;line-height:1.3;color:{INK};position:relative;z-index:1;margin-top:6px;font-style:italic;min-height:44px"></div>'
 +f'<div style="position:absolute;left:30px;bottom:26px;z-index:2;display:flex;gap:8px"><button class="mini" id="boclear">start over</button><button class="mini" id="boex">the example</button></div>')
# cut and rearrange
scr=['the quiet','OF TEA','steeping','in light','hum','small','kettle','still','window','again','keep','enough']
styles=[("#f3e9d2",INK,"'Fraunces',serif",20,'font-style:italic;font-weight:700'),(INK,'#f3e9d2',S,13,'letter-spacing:2px'),(ACC,'#fff',"'Shrikhand',cursive",18,''),('#fff',INK,C,22,'border:1.4px solid '+INK),('#f3e9d2',INK,S,14,''),(INK,'#f3e9d2',"'Fraunces',serif",17,'font-style:italic;font-weight:700')]
sc=''
for i,t in enumerate(scr):
    bg,fg,ff,sz,ex=styles[i%len(styles)]
    sc+=f'<div class="drag scrap" data-i="{i}" style="background:{bg};color:{fg};font-family:{ff};font-size:{sz}px;line-height:1;padding:5px 8px 6px;box-shadow:1px 2px 0 rgba(0,0,0,.18);{ex}">{t}</div>'
cutp=(F.lab('method two')+F.big(['cut and','rearrange'],30)
 +F.p('cut single words out of anything. spread them on the table. move them around until the lines start to hum. glue them down.',11,2)
 +f'<div class="nudge" style="font-family:{C};font-size:17px;line-height:1;color:{ACC};position:relative;z-index:1;margin:2px 0">&#9998; your turn: drag the scraps around the table and build a line.</div>'
 +f'<div id="table" data-w="315" data-h="165" style="position:absolute;left:0;top:222px;width:315px;height:165px;z-index:1">{sc}</div>'
 +f'<div style="position:absolute;right:30px;bottom:12px;z-index:2"><button class="mini" id="scatter">scatter</button></div>')
# gather (checkable)
items=['a tea box','junk mail','a receipt','an old paperback','a seed packet','something overheard','a text from a friend']
gather=(F.lab('gather')+F.p('collect words the way a naturalist collects specimens:',12.5,6)
 +''.join(f'<p class="chk" style="margin:0 0 5px;padding-left:14px;text-indent:-14px;font-family:{S};font-size:12.5px;line-height:1.3;color:{INK};position:relative;z-index:1;cursor:pointer"><span style="color:{ACC}" class="tl">~</span>&nbsp;&nbsp;<span class="tx">{x}</span></p>' for x in items)
 +F.im('book','width:100px;right:28px;bottom:26px'))
# overheard (typed)
def ln(k): return f'<input data-k="{k}" aria-label="overheard line" style="height:26px;position:relative;z-index:1;font-size:12px;border-bottom:1px solid {INK};opacity:.9">'
overheard=(F.lab('method three')+F.big(['the overheard'],30)
 +F.p('write down three things people say around you today. break them into lines. don’t fix them. let the strangers be poets.',12.5,8)
 +''.join(f'<div style="height:26px;position:relative;z-index:1"><input data-k="oh{i}" style="height:24px;font-size:12px;border-bottom:1px solid {INK}"></div>' for i in range(8)))
# field observations (typed)
def fo_i():
    b=f'position:absolute;z-index:2;font-family:{S};font-size:10.5px;color:{INK}'
    r=f'<div style="position:absolute;left:14px;right:14px;top:18px;bottom:16px;border:1.6px solid {INK};border-radius:16px;z-index:1"></div>'
    r+=f'<div style="{b};left:34px;top:40px;font-size:16px;letter-spacing:.5px">FIELD OBSERVATIONS</div>'
    for k,l,x,y,w in (('d','date:',34,76,116),('t','time:',166,76,116),('l','location:',34,104,248),('f','found in:',34,132,248)):
        r+=f'<div style="{b};left:{x}px;top:{y}px;width:{w}px;display:flex;align-items:flex-end"><span>{l}&nbsp;</span><input data-k="fo{k}" style="font-size:10.5px;height:14px"></div>'
    r+=f'<div style="{b};left:34px;top:164px">the words i found:</div><textarea data-k="fow" style="position:absolute;left:34px;top:180px;width:248px;height:70px;border:1.2px dashed {INK};border-radius:4px;z-index:2;font-size:10.5px;resize:none;padding:4px"></textarea><div style="{b};left:110px;top:272px">notes:</div>'
    for i,y in enumerate((300,317,334,351,368)): r+=f'<input data-k="fon{i}" style="position:absolute;left:110px;top:{y-12}px;width:172px;height:14px;font-size:10.5px;z-index:2;opacity:.9">'
    return r+F.im('flow','width:70px;left:30px;bottom:34px')
words2=['hush','lantern','moss','remember','slow','window','salt','borrowed','light','kettle','unfold','small','tender','hum','rain','somewhere','almost','thread']
drift=(F.lab('method four')+F.big(['catch the','drifting words'],28)
 +f'<div class="nudge" style="font-family:{C};font-size:17px;line-height:1;color:{ACC};position:relative;z-index:1;margin:4px 0 0">&#9998; your turn: words are drifting by. tap one to catch it. tap a caught word to let it go.</div>'
 +'<div id="sky" data-w="315" data-h="150" style="position:absolute;left:0;top:152px;width:315px;height:150px;z-index:1;overflow:hidden;border:1.2px dashed #2a2a2a55;border-radius:10px">'+''.join(f'<span class="fw" data-nosw="1">{w}</span>' for w in words2)+'</div>'
 +f'<div style="position:absolute;left:30px;top:310px;font-family:{S};font-size:10px;color:{INK};z-index:2">your caught words:</div>'
 +f'<div id="net" style="position:absolute;left:30px;right:30px;top:326px;min-height:50px;z-index:2;font-family:{S};font-size:12px;line-height:1.7;color:{INK}"></div>'
 +f'<div style="position:absolute;right:30px;bottom:12px;z-index:3"><button class="mini" id="releaseall">let them all go</button></div>')
CTA='if you want something more tangible to hold in your hand, you can purchase copies of my zines in my ko-fi luminarium store.'
LINKS=('https://ko-fi.com/s/f060f062c3','https://www.the-luminarium.org','https://rainesillito.substack.com')
fl=(F.lab('the luminarium')+F.big(['more to','wander into'],28)
 +F.p(CTA,11.5,8)
 +''.join(f'<p style="margin:0 0 7px;position:relative;z-index:1;font-family:{S};font-size:12px;line-height:1.35"><a href="{u}" target="_blank" rel="noopener" style="color:{ACC}">{t}</a></p>' for t,u in (('ko-fi luminarium store',LINKS[0]),('the-luminarium.org',LINKS[1]),('rainesillito.substack.com',LINKS[2]))))
fpages=[F.cover,F.whatis,gather,black,cutp,overheard,drift,fo_i(),F.last,fl]
fhtml=''.join(fpage(p) for p in fpages)
fcss='''.in{position:relative;zoom:1.2941;width:315.2px;height:408px;box-sizing:border-box;padding:34px 30px 30px}
.pg{width:408px;height:528px}
.mini{font:inherit;font-size:9px;background:#fff;border:1px solid #2a2a2a;border-radius:999px;padding:3px 9px;cursor:pointer;color:#2a2a2a}.mini:hover{background:#2a2a2a;color:#fff}
.w{border-radius:2px;transition:background .15s,color .15s;padding:0 1px}
.w.keep.off{background:#2a2a2a;color:#2a2a2a}
.w.off{background:#2a2a2a;color:#2a2a2a}
.chk.done .tx{text-decoration:line-through;opacity:.5}.chk.done .tl:before{content:"x "}

.scrap{position:absolute;white-space:nowrap}
.fw{position:absolute;left:0;top:0;white-space:nowrap;cursor:pointer;user-select:none;touch-action:none;padding:2px 4px;will-change:transform;transition:opacity .2s}
.fw.gone{opacity:0}
.caughtw{display:inline-block;margin:0 5px 3px 0;padding:1px 6px;background:#1f7a6d;color:#fff;border-radius:3px;cursor:pointer;animation:pop .25s}
@keyframes pop{from{transform:scale(.4)}to{transform:scale(1)}}
.nudge{animation:nudge 2.4s ease-in-out infinite}
@keyframes nudge{0%,100%{translate:0 0}50%{translate:3px 0}}
.face.vis .in{animation:rise .55s ease-out both}
@keyframes rise{from{opacity:0;translate:0 10px}to{opacity:1;translate:0 0}}
.pg img{animation:bob 6s ease-in-out infinite}
@keyframes bob{0%,100%{translate:0 0}50%{translate:0 -4px}}
.scrap{animation:wob 3.5s ease-in-out infinite}.scrap:nth-child(2n){animation-delay:-1.2s}.scrap:nth-child(3n){animation-delay:-2.2s}
@keyframes wob{0%,100%{translate:0 0}50%{translate:0 -2px}}
.w{transition:background .3s,color .3s}
@media (prefers-reduced-motion:reduce){.pg img,.scrap,.nudge,.face.vis .in{animation:none}}'''
fjs='''
const sky=document.getElementById('sky'),net=document.getElementById('net'),fws=[...sky.querySelectorAll('.fw')],SW=315,SH=150;
const st=fws.map(el=>({el,x:Math.random()*200,y:Math.random()*150,vx:(Math.random()<.5?-1:1)*(14+Math.random()*22),vy:(Math.random()<.5?-1:1)*(8+Math.random()*16),on:true}));
const fonts=["'Fraunces',serif","'Special Elite',monospace","'Caveat',cursive","'Shrikhand',cursive"];
fws.forEach((el,i)=>{el.style.fontFamily=fonts[i%4];el.style.fontSize=[17,13,21,15][i%4]+'px';el.style.fontStyle=i%4===0?'italic':'normal';el.style.color=i%3===0?'#1f7a6d':'#2a2a2a';});
let last=performance.now();
function tick(t){const dt=Math.min(.05,(t-last)/1000);last=t;st.forEach(s=>{if(!s.on)return;const w=s.el.offsetWidth,h=s.el.offsetHeight;s.x+=s.vx*dt;s.y+=s.vy*dt;if(s.x<0){s.x=0;s.vx=Math.abs(s.vx)}if(s.x>SW-w){s.x=SW-w;s.vx=-Math.abs(s.vx)}if(s.y<0){s.y=0;s.vy=Math.abs(s.vy)}if(s.y>SH-h){s.y=SH-h;s.vy=-Math.abs(s.vy)}s.el.style.transform=`translate(${s.x}px,${s.y}px) rotate(${Math.sin(t/900+s.x/40)*4}deg)`;});requestAnimationFrame(tick)}
requestAnimationFrame(tick);
st.forEach(s=>s.el.addEventListener('pointerdown',e=>{e.stopPropagation();if(!s.on)return;s.on=false;s.el.classList.add('gone');const c=document.createElement('span');c.className='caughtw';c.textContent=s.el.textContent;c.dataset.nosw=1;net.appendChild(c);c.addEventListener('pointerdown',ev=>{ev.stopPropagation();c.remove();s.on=true;s.x=Math.random()*150;s.y=Math.random()*120;s.el.classList.remove('gone');});}));
document.getElementById('releaseall').onclick=()=>{net.innerHTML='';st.forEach(s=>{s.on=true;s.el.classList.remove('gone')});};

const SK='ezine-found:';const store=(k,v)=>{try{localStorage.setItem(SK+k,v)}catch(e){}};const load=k=>{try{return localStorage.getItem(SK+k)}catch(e){return null}};
document.querySelectorAll('[data-k]').forEach(el=>{const v=load(el.dataset.k);if(v!==null)el.value=v;el.addEventListener('input',()=>store(el.dataset.k,el.value))});
document.querySelectorAll('.chk').forEach((el,i)=>{if(load('chk'+i)==='1')el.classList.add('done');el.addEventListener('click',()=>{el.classList.toggle('done');store('chk'+i,el.classList.contains('done')?'1':'0')})});
const ws=[...document.querySelectorAll('#bo .w')],poem=document.getElementById('bopoem');
function bpoem(){poem.textContent=ws.filter(w=>!w.classList.contains('off')).map(w=>w.textContent.replace(/[.,]/g,'')).join(' ');}
function example(){ws.forEach(w=>w.classList.toggle('off',!w.classList.contains('keep')));bpoem();}
ws.forEach(w=>w.addEventListener('click',()=>{w.classList.toggle('off');bpoem();}));
document.getElementById('boclear').onclick=()=>{ws.forEach(w=>w.classList.remove('off'));bpoem();};
document.getElementById('boex').onclick=example;example();
const tb=document.getElementById('table'),W=315,H=165;
const sc=[...tb.querySelectorAll('.scrap')];let zt=10;
function scatter(){sc.forEach((s,i)=>{const cols=3,c=i%cols,r=Math.floor(i/cols);const x=8+c*98+Math.random()*16,y=4+r*38+Math.random()*8;s.style.left=Math.min(x,W-s.offsetWidth-4)+'px';s.style.top=Math.min(y,H-s.offsetHeight-2)+'px';s.style.transform=`rotate(${(Math.random()*10-5).toFixed(1)}deg)`;});}
scatter();document.getElementById('scatter').onclick=scatter;
sc.forEach(s=>{s.addEventListener('pointerdown',e=>{e.stopPropagation();s.setPointerCapture(e.pointerId);s.style.zIndex=++zt;const rc=tb.getBoundingClientRect(),k=rc.width/W,r0=s.getBoundingClientRect();const gx=(e.clientX-r0.left)/k,gy=(e.clientY-r0.top)/k;
 const mv=ev=>{const x=(ev.clientX-rc.left)/k-gx,y=(ev.clientY-rc.top)/k-gy;s.style.left=Math.max(-10,Math.min(W-s.offsetWidth+10,x))+'px';s.style.top=Math.max(-60,Math.min(H+30,y))+'px';};
 const up=()=>{s.removeEventListener('pointermove',mv);s.removeEventListener('pointerup',up);};s.addEventListener('pointermove',mv);s.addEventListener('pointerup',up);});});
'''
os.makedirs(f'{R}/found-poetry',exist_ok=True)
page=SHELL.format(title='how to write found poetry — an e-zine',css=fcss,pre='',hint='this one is interactive: tap, drag, catch and type.',pdf='<a href="how-to-write-found-poetry.pdf">print the paper version (pdf)</a>',pages=sub(fix(fhtml),FM),pw=408,ph=528,ms=1.6,js=fjs)
open(f'{R}/found-poetry/index.html','w').write(page)
print('found ok')

# ---------------- RAINY DAY ----------------
sys.argv=['x','local']
spec=importlib.util.spec_from_file_location('rainy3','/home/claude/zines/rainy3.py'); RM=importlib.util.module_from_spec(spec)
cwd=os.getcwd(); os.chdir('/home/claude/zines'); spec.loader.exec_module(RM); os.chdir(cwd)
RMAP={'ink':'#2f3f6b','acc':'#5f90d0','hi':'#b7a2e2','pk':'#f0a3b4','paper':'#fff'}
K_,S_,C_,INK_,ACC_,HI_,PK_=RM.K,RM.S,RM.C,RM.INK,RM.ACC,RM.HI,RM.PK
def fldi(lab,h,k):
    return f'<div style="position:relative;z-index:1;{C_};font-size:17px;color:{ACC_};margin-top:6px">{lab}</div>'+''.join(f'<div style="height:24px;position:relative;z-index:1"><input data-k="{k}{j}" style="height:22px;font-size:12.5px;border-bottom:1.5px solid {INK_};opacity:.9"></div>' for j in range(h))
P=RM.P
P[6]=(RM.strip(f'<span style="{K_};font-size:30px;line-height:1">rain log</span>',ACC_,'#fff',-2,'2px 14px 4px','display:inline-block;margin-bottom:2px')
 +fldi('date:',1,'rd')+fldi('what it sounded like:',1,'rs')+fldi('what it smelled like:',1,'rm')+fldi('where i watched it from:',1,'rw')+fldi('what i did instead:',2,'ri'))
P[7]=(RM.frame(f'<div style="{K_};font-size:21px;line-height:1.05;color:{INK_};text-align:center">my rainy<br>day list</div>',-2,'8px 16px',HI_,'margin:0 24px 10px')
 +''.join(f'<div style="position:relative;z-index:1;display:flex;align-items:flex-end;height:25px;border-bottom:1.5px solid {INK_};opacity:.95"><span class="cb" data-i="{i}" style="flex:none;width:13px;height:13px;border:1.5px solid {INK_};border-radius:50%;margin-bottom:5px;cursor:pointer"></span><input data-k="rl{i}" style="margin-left:8px;border:0;height:22px;font-size:12.5px"></div>' for i in range(8))
 +RM.img('spr','width:64px;right:12px;bottom:10px'))
KO='https://ko-fi.com/s/f060f062c3'
P[9]=(RM.strip(f'<span style="{K_};font-size:28px;line-height:1">something to hold</span>',ACC_,'#fff',-2,'2px 14px 4px','display:inline-block;margin-bottom:10px')
 +f'<p style="position:relative;z-index:1;{S_};font-size:13px;line-height:1.45;color:{INK_};margin:0 0 12px">if you want something more tangible to hold in your hand, you can purchase copies of my zines in my ko-fi luminarium store.</p>'
 +f'<a href="{KO}" target="_blank" rel="noopener" style="position:relative;z-index:1;{C_};font-size:22px;color:{ACC_}">ko-fi.com/luminarium store &rarr;</a>')
P[10]=(RM.strip(f'<span style="{K_};font-size:28px;line-height:1">the luminarium</span>',HI_,INK_,-2,'2px 14px 4px','display:inline-block;margin-bottom:12px')
 +''.join(f'<p style="margin:0 0 9px;position:relative;z-index:1;{S_};font-size:12.5px"><a href="{u}" target="_blank" rel="noopener" style="color:{ACC_}">{t}</a></p>' for t,u in (('the-luminarium.org','https://www.the-luminarium.org'),('rainesillito.substack.com','https://rainesillito.substack.com'))))
rhtml=''.join(f'<div class="pg"><div class="pad">{P[n]}</div></div>' for n in range(1,11))
rcss='''.pad{position:relative;width:264px;height:408px;padding:28px 24px 24px;box-sizing:border-box}
.pg{width:264px;height:408px}
.cb.on{background:#2f3f6b}
.cb.on+input{text-decoration:line-through;opacity:.5}
.mini{font:inherit;font-size:11px;background:#fff;border:1.5px solid #2f3f6b;border-radius:999px;padding:5px 12px;cursor:pointer;color:#2f3f6b}.mini:hover{background:#2f3f6b;color:#fff}
body{--bg:#e9eef6}
#rain{position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:3;display:none}
#rain.on{display:block}
#rain i{position:absolute;top:-30px;width:2px;height:18px;background:linear-gradient(transparent,#5f90d0);border-radius:2px;animation:fall linear infinite;transform:rotate(12deg)}
@keyframes fall{to{transform:translate(-40px,112vh) rotate(12deg)}}
#rain b{position:absolute;top:-20px;width:9px;height:11px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 35% 30%,#fff,rgba(120,160,220,.35));border:1px solid rgba(95,144,208,.5);animation:slide linear infinite}
@keyframes slide{0%{translate:0 0;opacity:0}8%{opacity:1}100%{translate:6px 108vh;opacity:.9}}
.stage{z-index:2}.top,.nav{z-index:5}
body{--gl:rgba(70,100,170,.16);--gm:rgba(70,100,170,.3)}
@media (prefers-reduced-motion:reduce){#rain{display:none!important}}'''
rjs='''
const SK='ezine-rainy:';const store=(k,v)=>{try{localStorage.setItem(SK+k,v)}catch(e){}};const load=k=>{try{return localStorage.getItem(SK+k)}catch(e){return null}};
document.querySelectorAll('[data-k]').forEach(el=>{const v=load(el.dataset.k);if(v!==null)el.value=v;el.addEventListener('input',()=>store(el.dataset.k,el.value))});
document.querySelectorAll('.cb').forEach(c=>{if(load('cb'+c.dataset.i)==='1')c.classList.add('on');c.addEventListener('click',()=>{c.classList.toggle('on');store('cb'+c.dataset.i,c.classList.contains('on')?'1':'0')})});
const rain=document.getElementById('rain');for(let i=0;i<9;i++){const d=document.createElement('b');d.style.left=(4+Math.random()*92)+'%';d.style.animationDuration=(7+Math.random()*7)+'s';d.style.animationDelay=(-Math.random()*10)+'s';d.style.transform='scale('+(.7+Math.random()*.9)+')';rain.appendChild(d);}for(let i=0;i<110;i++){const d=document.createElement('i');d.style.left=Math.random()*100+'%';d.style.animationDuration=(0.7+Math.random()*0.8)+'s';d.style.animationDelay=(-Math.random()*2)+'s';d.style.opacity=.25+Math.random()*.4;rain.appendChild(d);}
const rb=document.getElementById('rainbtn');const setR=on=>{rain.classList.toggle('on',on);rb.textContent=on?'stop the rain':'let it rain';};rb.onclick=()=>setR(!rain.classList.contains('on'));if(!matchMedia('(prefers-reduced-motion:reduce)').matches)setR(true);
'''
os.makedirs(f'{R}/rainy-day',exist_ok=True)
rp=SHELL.format(title='instructions for a rainy day — an e-zine',css=rcss,pre='<div id="rain"></div>',hint='tap the boxes, type in the blanks.',pdf='<button class="mini" id="rainbtn">let it rain</button> &nbsp; <a href="https://ko-fi.com/s/f060f062c3" target="_blank" rel="noopener">get the paper zines</a>',pages=sub(fix(rhtml),RMAP),pw=264,ph=408,ms=2,js=rjs)
open(f'{R}/rainy-day/index.html','w').write(rp)
print('rainy ok')
