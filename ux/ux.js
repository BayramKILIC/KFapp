/* ===== UX : un seul audio à la fois, progression mémorisée, reprise, grammaire repliable, barre mobile ===== */
(function(){
const N=__N__,KEY='kf-a1-m'+N+'-';
const get=k=>{try{return JSON.parse(localStorage.getItem(KEY+k))}catch(e){return null}};
const set=(k,v)=>{try{localStorage.setItem(KEY+k,JSON.stringify(v))}catch(e){}};

/* 1. Un seul audio à la fois, avec le bouton en cours mis en évidence */
let cur=null,curRes=null,curBtn=null,lastBtn=null;
function stopAudio(){
  try{speechSynthesis.cancel()}catch(e){}
  if(cur){try{cur.pause()}catch(e){}cur=null}
  if(curBtn){curBtn.classList.remove('playing');curBtn=null}
  if(curRes){const r=curRes;curRes=null;r()}
}
document.addEventListener('click',e=>{
  const b=e.target.closest&&e.target.closest('.say');
  lastBtn=b||null;
  if(b&&playing){playing=false;$('#playAll').textContent='▶ Tümünü dinle'}
  if(e.target.id==='playAll'&&playing)stopAudio();
},true);
say=function(text,src){return new Promise(res=>{
  stopAudio();
  const btn=(lastBtn&&lastBtn.dataset.src===src&&lastBtn.dataset.say===text)?lastBtn:$$('.say').find(b=>src?b.dataset.src===src:b.dataset.say===text);
  lastBtn=null;
  if(btn){btn.classList.add('playing');curBtn=btn}
  let over=false;
  const end=()=>{if(over)return;over=true;if(curBtn===btn&&btn){btn.classList.remove('playing');curBtn=null}if(curRes===end)curRes=null;cur=null;res()};
  curRes=end;
  if(!src)return tts(text).then(end);
  let fell=false;const fb=()=>{if(fell||over)return;fell=true;tts(text).then(end)};
  try{const a=new Audio(src);cur=a;a.onended=end;a.onerror=fb;const p=a.play();if(p&&p.catch)p.catch(fb)}catch(e){fb()}
})};

/* 2. Progression mémorisée */
const _mark=mark;
mark=function(k){_mark(k);set('done',Object.keys(DONE));syncSheet()};
(get('done')||[]).forEach(k=>_mark(k));
const sb=$('#sinavBtn');
if(sb){
  const orig=sb.onclick;
  sb.onclick=function(ev){
    orig.call(this,ev);
    const box=$('#sinavRes'),h=$('h3',box);
    if(!h)return;
    set('sinav',h.textContent);
    /* test réussi : accès direct au module suivant et à la fiche PDF */
    if(/Tebrikler/.test(box.textContent)&&!$('.after-pass',box)){
      const nx=$$('.pager a').find(a=>/Sonraki/.test(a.textContent)),pdf=$('a[href$="-ozet.pdf"]');
      const d=document.createElement('div');d.className='after-pass';
      d.innerHTML=(nx?'<a class="go" href="'+nx.getAttribute('href')+'">Modül '+(N+1)+"'"+(['','','ye','e','e','e','ya','ye','e','a','a','e','ye'][N+1]||'e')+' geç →</a>':'')+(pdf?'<a href="'+pdf.getAttribute('href')+'" download>Özet fişini indir (PDF) ↓</a>':'');
      if(d.innerHTML)(h.parentElement||box).appendChild(d);
    }
  };
  const last=get('sinav');
  if(last){const d=document.createElement('div');d.className='last-score';d.textContent='Son sonucun: '+last;$('#quizSinav').before(d)}
}

/* 3. Grammaire repliable : aperçu, bouton clair, compteur, état « lu » */
const gs=$('#dilbilgisi');
let folds=[];
if(gs){
  const kids=[...gs.children];
  let f=null;
  kids.forEach(el=>{
    if(el.tagName==='H2'){
      f=document.createElement('div');f.className='fold';
      const h=document.createElement('div');h.className='fold-h';
      const b=document.createElement('div');b.className='fold-b';
      el.before(f);h.appendChild(el);f.append(h,b);folds.push(f);
    }else if(f){f.querySelector('.fold-b').appendChild(el)}
  });
  const read=new Set(get('fold')||[]);
  const paint=(f,i)=>{
    const open=f.classList.contains('open'),btn=f.querySelector('.fold-more');
    const n=f.querySelectorAll('.fold-b .say').length;
    btn.innerHTML=open?'Gizle ▴':'Devamını göster ▾'+(n?' <small>· '+n+' sesli örnek</small>':'');
    btn.setAttribute('aria-expanded',open);
    f.classList.toggle('read',read.has(i));
  };
  const openFold=(f,i)=>{f.classList.add('open');read.add(i);set('fold',[...read]);paint(f,i)};
  folds.forEach((f,i)=>{
    const n=document.createElement('span');n.className='fold-n';n.textContent=(i+1)+' / '+folds.length;f.querySelector('.fold-h').appendChild(n);
    const btn=document.createElement('button');btn.type='button';btn.className='fold-more';f.appendChild(btn);
    btn.onclick=()=>{
      if(f.classList.contains('open')){f.classList.remove('open');paint(f,i);f.scrollIntoView({block:'start'})}
      else openFold(f,i);
    };
    if(i===0)openFold(f,i);else paint(f,i);
  });
  const top=document.createElement('div');top.className='fold-top';
  top.innerHTML='<b>'+folds.length+' konu</b><button type="button" class="btn">Tümünü aç</button>';
  const eb=gs.querySelector('.eyebrow');(eb||gs.firstElementChild).after(top);
  top.querySelector('button').onclick=function(){
    const all=folds.every(f=>f.classList.contains('open'));
    folds.forEach((f,i)=>{if(all){f.classList.remove('open');paint(f,i)}else openFold(f,i)});
    this.textContent=all?'Tümünü aç':'Tümünü kapat';
  };
}

/* 4. Barre mobile : section en cours + sommaire toujours accessibles */
const tb=$('.topbar'),side=$('nav.side');
const links=$$('.toc a');
const secs=links.map(a=>$(a.getAttribute('href'))).filter(Boolean);
const names=links.map(a=>a.textContent.trim());
const bar=document.createElement('div');bar.className='mbar';
bar.innerHTML='<button type="button" aria-expanded="false" aria-controls="msheet"><span class="cur"></span><span class="all">Bölümler ▾</span></button><div class="ln"><i></i></div>';
const sheet=document.createElement('div');sheet.className='msheet';sheet.id='msheet';
const shade=document.createElement('div');shade.className='mshade';
document.body.append(shade,sheet,bar);
function syncSheet(){
  const n=Object.keys(DONE).length;
  sheet.innerHTML='<div class="mp">Modül ilerlemen: <b>'+n+' / 6</b> bölüm tamamlandı</div>'+links.map((a,i)=>'<a href="'+a.getAttribute('href')+'" class="'+(a.classList.contains('done')?'done ':'')+(i===now?'now':'')+'"><span class="dot"></span>'+names[i]+'</a>').join('');
}
let now=-1;
const toggle=on=>{sheet.classList.toggle('on',on);shade.classList.toggle('on',on);bar.firstElementChild.setAttribute('aria-expanded',on);bar.querySelector('.all').textContent=on?'Kapat ▴':'Bölümler ▾';if(on)syncSheet()};
bar.firstElementChild.onclick=()=>toggle(!sheet.classList.contains('on'));
shade.onclick=()=>toggle(false);
sheet.addEventListener('click',e=>{if(e.target.closest('a'))toggle(false)});
function measure(){document.documentElement.style.setProperty('--mtop',tb.offsetHeight+'px')}
measure();addEventListener('resize',measure);
let tick=false;
function spy(){
  tick=false;
  const top=tb.offsetHeight;
  const show=side.getBoundingClientRect().bottom<top;
  bar.classList.toggle('on',show);if(!show&&sheet.classList.contains('on'))toggle(false);
  let i=-1;secs.forEach((s,k)=>{if(s.getBoundingClientRect().top<top+120)i=k});
  if(i!==now){now=i;bar.querySelector('.cur').innerHTML=i<0?'Modül '+N:'<small>'+(i+1)+' / '+secs.length+'</small>'+names[i];if(i>1)set('pos',secs[i].id)}
  const H=document.documentElement.scrollHeight-innerHeight;
  bar.querySelector('.ln i').style.width=(H>0?Math.min(100,scrollY/H*100):0)+'%';
}
addEventListener('scroll',()=>{if(!tick){tick=true;requestAnimationFrame(spy)}},{passive:true});

/* 6. Objectifs : quatre visibles sur mobile, le reste derrière un bouton explicite */
const gl=$('ul.goals');
if(gl&&gl.children.length>5){
  const li=[...gl.children];li.slice(4).forEach(x=>x.classList.add('g-more'));gl.classList.add('short');
  const b=document.createElement('button');b.type='button';b.className='fold-more goals-more';
  b.innerHTML=(li.length-4)+' hedef daha göster ▾';
  gl.after(b);
  b.onclick=()=>{gl.classList.remove('short');b.remove()};
}

/* 5. Reprise : « Kaldığın yerden devam et » */
const pos=get('pos');
if(pos&&!location.hash&&$('#'+pos)){
  const i=secs.findIndex(s=>s.id===pos);
  const d=document.createElement('div');d.className='resume';
  d.innerHTML='<a href="#'+pos+'"><small>Kaldığın yerden devam et</small>'+(i>=0?names[i]:'')+' →</a><button type="button" aria-label="Kapat">✕</button>';
  $('.hero').before(d);
  d.querySelector('button').onclick=()=>d.remove();
  d.querySelector('a').addEventListener('click',()=>setTimeout(()=>d.remove(),50));
}
spy();
})();
