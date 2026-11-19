/* Tzadik Azaria — V9. Menu, header, reveal, hero (stickers + vector path), lightbox, copy email. */
(()=>{const d=document,root=d.documentElement;root.classList.add('js');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---- mobile menu ---- */
const menuButton=d.querySelector('.menu-toggle'),nav=d.querySelector('.nav');
const setBtn=()=>{if(menuButton)menuButton.textContent=menuButton.getAttribute('aria-expanded')==='true'?'Close':'Menu'};
function closeMenu(){nav?.classList.remove('is-open');menuButton?.setAttribute('aria-expanded','false');setBtn();d.body.classList.remove('menu-open')}
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));setBtn();nav.classList.toggle('is-open',open);d.body.classList.toggle('menu-open',open)});
nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
d.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav?.classList.contains('is-open')){closeMenu();menuButton.focus()}});

/* ---- scroll reveal (content is visible without JS) ---- */
const rv=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&!reduce){const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{rootMargin:'0px 0px -8% 0px'});rv.forEach(el=>io.observe(el))}else rv.forEach(el=>el.classList.add('in'));

/* ---- hero: draggable cut-outs ---- */
d.querySelectorAll('.stk').forEach(el=>{let sx,sy,ox=0,oy=0,id=null;
 el.addEventListener('pointerdown',e=>{id=e.pointerId;el.setPointerCapture(id);sx=e.clientX-ox;sy=e.clientY-oy;el.classList.add('drag');e.preventDefault()});
 el.addEventListener('pointermove',e=>{if(e.pointerId!==id)return;ox=e.clientX-sx;oy=e.clientY-sy;el.style.setProperty('--dx',ox+'px');el.style.setProperty('--dy',oy+'px')});
 const end=e=>{if(e.pointerId!==id)return;id=null;el.classList.remove('drag')};el.addEventListener('pointerup',end);el.addEventListener('pointercancel',end)});

/* ---- hero: bézier path with draggable anchors + handles, selection size tag, baseline guide ---- */
const hero=d.getElementById('hero'),svg=hero?.querySelector('.vec');
if(hero&&svg){
 const NS='http://www.w3.org/2000/svg',path=svg.querySelector('.vp'),hl=svg.querySelector('.vh'),g=svg.querySelector('.vpts');
 // fractions of the svg box: [x,y]. a = anchors, c = handles
 const P={a0:[.04,.22],c0:[.18,.98],c1a:[.34,.92],a1:[.5,.62],c1b:[.66,.32],c2:[.84,.82],a2:[.96,.2]};
 const kind={a0:'a',a1:'a',a2:'a'};
 let W=0,H=0;
 const px=k=>[P[k][0]*W,P[k][1]*H];
 const els={};
 Object.keys(P).forEach(k=>{const isA=kind[k]==='a';const c=d.createElementNS(NS,isA?'rect':'circle');c.setAttribute('class',isA?'a':'c');
  if(isA){c.setAttribute('width',10);c.setAttribute('height',10);c.setAttribute('rx',1.5)}else c.setAttribute('r',4.5);
  g.appendChild(c);els[k]=c;
  let id=null;
  c.addEventListener('pointerdown',e=>{id=e.pointerId;c.setPointerCapture(id);c.classList.add('on');e.preventDefault();e.stopPropagation()});
  c.addEventListener('pointermove',e=>{if(e.pointerId!==id)return;const r=svg.getBoundingClientRect();
   const nx=Math.min(1.04,Math.max(-.04,(e.clientX-r.left)/W)),ny=Math.min(1.5,Math.max(-.5,(e.clientY-r.top)/H));
   const dx=nx-P[k][0],dy=ny-P[k][1];P[k]=[nx,ny];
   if(isA){const hk={a0:['c0'],a1:['c1a','c1b'],a2:['c2']}[k];hk.forEach(h=>{P[h]=[P[h][0]+dx,P[h][1]+dy]})}
   draw()});
  const end=e=>{if(e.pointerId!==id)return;id=null;c.classList.remove('on')};c.addEventListener('pointerup',end);c.addEventListener('pointercancel',end);
 });
 function draw(){
  const f=k=>px(k).map(v=>v.toFixed(1)).join(' ');
  path.setAttribute('d',`M${f('a0')} C${f('c0')} ${f('c1a')} ${f('a1')} C${f('c1b')} ${f('c2')} ${f('a2')}`);
  hl.setAttribute('d',`M${f('a0')} L${f('c0')} M${f('a1')} L${f('c1a')} M${f('a1')} L${f('c1b')} M${f('a2')} L${f('c2')}`);
  Object.keys(P).forEach(k=>{const [x,y]=px(k),c=els[k];if(kind[k]==='a'){c.setAttribute('x',(x-5).toFixed(1));c.setAttribute('y',(y-5).toFixed(1))}else{c.setAttribute('cx',x.toFixed(1));c.setAttribute('cy',y.toFixed(1))}});
 }
 function layout(){
  const r=svg.getBoundingClientRect();W=r.width;H=r.height;svg.setAttribute('viewBox',`0 0 ${W} ${H}`);draw();
  const sel=hero.querySelector('.sel'),dim=hero.querySelector('.dim'),l2=hero.querySelector('.l2'),gd=hero.querySelector('.guide');
  if(sel&&dim){const s=sel.getBoundingClientRect();dim.textContent=`W ${Math.round(s.width)} × H ${Math.round(s.height)}`}
  if(l2&&gd){const hr=hero.getBoundingClientRect(),lr=l2.getBoundingClientRect(),fs=parseFloat(getComputedStyle(l2).fontSize);gd.style.top=(lr.bottom-hr.top-fs*.2)+'px'}
 }
 layout();addEventListener('resize',layout);
 if(d.fonts?.ready)d.fonts.ready.then(layout);
}

/* ---- header state ---- */
const h=d.getElementById('siteheader');if(h){const on=()=>h.classList.toggle('s',scrollY>20);on();addEventListener('scroll',on,{passive:true})}

/* ---- lightbox with previous / next ---- */
const dialog=d.querySelector('.lightbox');
if(dialog){
 const image=dialog.querySelector('.lightbox-inner img'),caption=dialog.querySelector('.lightbox-inner p');
 const items=[...d.querySelectorAll('[data-lightbox]')];let i=0,prevFocus=null;
 const prevB=dialog.querySelector('.lb-nav.prev'),nextB=dialog.querySelector('.lb-nav.next');
 const show=n=>{i=(n+items.length)%items.length;const im=items[i].querySelector('img');image.src=im.getAttribute('src');image.alt=im.alt;
  const fc=items[i].closest('figure')?.querySelector('figcaption');caption.textContent=`${i+1} / ${items.length} — ${im.alt}`};
 items.forEach((b,n)=>b.addEventListener('click',()=>{prevFocus=b;show(n);dialog.showModal();d.body.style.overflow='hidden'}));
 if(items.length<2){prevB?.remove();nextB?.remove()}
 prevB?.addEventListener('click',()=>show(i-1));nextB?.addEventListener('click',()=>show(i+1));
 dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
 const close=()=>dialog.close();dialog.querySelector('.lightbox-close').addEventListener('click',close);
 dialog.addEventListener('click',e=>{if(e.target===dialog||e.target.classList.contains('lightbox-inner'))close()});
 dialog.addEventListener('close',()=>{d.body.style.overflow='';prevFocus?.focus()});
}

/* ---- copy email ---- */
d.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
 const t=b.dataset.copy,o=b.textContent;
 try{await navigator.clipboard.writeText(t)}catch(e){const r=d.createRange();const a=b.parentElement.querySelector('a');r.selectNodeContents(a);const s=getSelection();s.removeAllRanges();s.addRange(r)}
 b.textContent='Copied';b.classList.add('done');setTimeout(()=>{b.textContent=o;b.classList.remove('done')},1800)}));
})();
