/* Tzadik Azaria — portfolio · main.js
   Progressive enhancement only: every piece of content is visible without hover or JS. */
(() => {
  const d = document, root = d.documentElement;
  root.classList.add('js');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canHover = matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* header state */
  const head = d.querySelector('.site-head');
  const onScroll = () => head && head.classList.toggle('is-scrolled', scrollY > 20);
  onScroll(); addEventListener('scroll', onScroll, { passive: true });

  /* menu panel (mobile) */
  const panel = d.querySelector('.panel'), btn = d.querySelector('.menu-btn');
  if (panel && btn) {
    const set = (open) => {
      panel.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open);
      d.body.style.overflow = open ? 'hidden' : '';
      panel.setAttribute('aria-hidden', !open);
      if (open) panel.querySelector('.panel__close').focus(); else btn.focus({ preventScroll: true });
    };
    btn.addEventListener('click', () => set(true));
    panel.querySelectorAll('.panel__close,.panel__scrim').forEach(el => el.addEventListener('click', () => set(false)));
    panel.querySelectorAll('a[href^="#"],a[href*="#"]').forEach(a => a.addEventListener('click', () => set(false)));
    d.addEventListener('keydown', e => { if (e.key === 'Escape' && panel.classList.contains('is-open')) set(false); });
  }

  /* scroll reveals (restrained) */
  const rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(el => io.observe(el));
  } else rv.forEach(el => el.classList.add('in'));

  /* hero pointer parallax: portrait + red misregistration outline */
  const hero = d.querySelector('.hero');
  if (hero && canHover && !reduce) {
    hero.addEventListener('pointermove', e => {
      const r = hero.getBoundingClientRect();
      hero.style.setProperty('--px', ((e.clientX - r.left) / r.width * 2 - 1).toFixed(3));
      hero.style.setProperty('--py', ((e.clientY - r.top) / r.height * 2 - 1).toFixed(3));
    });
  }

  /* work cards: pointer depth, cursor pill, alternate visuals */
  const pill = d.querySelector('.cursor-pill');
  d.querySelectorAll('.work').forEach(card => {
    const media = card.querySelector('.work__media');
    if (canHover && !reduce && media) {
      media.addEventListener('pointermove', e => {
        const r = media.getBoundingClientRect();
        card.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 2 - 1).toFixed(3));
        card.style.setProperty('--my', ((e.clientY - r.top) / r.height * 2 - 1).toFixed(3));
        if (pill) { pill.style.left = e.clientX + 'px'; pill.style.top = e.clientY + 'px'; }
      });
      media.addEventListener('pointerenter', () => pill && pill.classList.add('on'));
      media.addEventListener('pointerleave', () => { pill && pill.classList.remove('on'); card.style.setProperty('--mx', 0); card.style.setProperty('--my', 0); });
    }
    /* stacked product deck: cycle which visual sits in front */
    const deck = card.querySelector('.deck');
    if (deck) {
      const cards = [...deck.children]; let i = 0, t;
      const show = n => { i = (n + cards.length) % cards.length; cards.forEach((c, k) => c.classList.toggle('is-front', k === i)); };
      const run = () => { clearInterval(t); if (!reduce) t = setInterval(() => show(i + 1), canHover ? 1100 : 2400); };
      show(0);
      if (canHover) { card.addEventListener('pointerenter', () => { show(i + 1); run(); }); card.addEventListener('pointerleave', () => { clearInterval(t); show(0); }); }
      else if ('IntersectionObserver' in window) new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? run() : clearInterval(t))).observe(card);
      cards.forEach((c, k) => c.addEventListener('click', ev => { if (k !== i) { ev.preventDefault(); show(k); } }));
    }
    /* touch: alternate visuals swap on a slow loop while visible (hover does it on desktop) */
    if (!canHover && !reduce && card.matches('[data-alt]') && 'IntersectionObserver' in window) {
      let t; new IntersectionObserver(es => es.forEach(e => {
        clearInterval(t); if (e.isIntersecting) t = setInterval(() => card.classList.toggle('is-alt'), 2600);
      }), { threshold: .5 }).observe(card);
    }
  });

  /* copy email */
  d.querySelectorAll('[data-copy]').forEach(b => b.addEventListener('click', async () => {
    const live = b.querySelector('span') || b, old = live.textContent;
    try { await navigator.clipboard.writeText(b.dataset.copy); live.textContent = 'Copied ✓'; }
    catch { live.textContent = b.dataset.copy; }
    setTimeout(() => (live.textContent = old), 1800);
  }));
})();
