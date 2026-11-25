/* tiny page-flip booklet. pages: array of elements, each pw x ph px. */
class Flipbook {
  constructor(o) {
    this.stage = o.stage; this.pw = o.pw; this.ph = o.ph; this.maxScale = o.maxScale || 2;
    this.pages = o.pages.slice(); if (this.pages.length % 2) { const b = document.createElement('div'); b.className = 'pg blank'; this.pages.push(b); }
    this.n = this.pages.length; this.pos = 0; this.mode = null; this.onchange = o.onchange || (() => {});
    this.wrap = document.createElement('div'); this.wrap.className = 'book-wrap';
    this.book = document.createElement('div'); this.book.className = 'book';
    this.wrap.appendChild(this.book); this.stage.appendChild(this.wrap);
    addEventListener('resize', () => this.layout());
    addEventListener('keydown', e => { if (/input|textarea/i.test(e.target.tagName) || e.target.isContentEditable) return;
      if (e.key === 'ArrowRight') this.next(); if (e.key === 'ArrowLeft') this.prev(); });
    let sx = null;
    this.stage.addEventListener('pointerdown', e => { sx = e.target.closest('input,textarea,button,a,.drag,.w,.chk,[data-nosw]') ? null : e.clientX; });
    this.stage.addEventListener('pointerup', e => { if (sx === null) return; const dx = e.clientX - sx; sx = null; if (dx < -60) this.next(); else if (dx > 60) this.prev(); });
    this.layout(true);
  }
  wantSingle() { return (innerWidth - 40) / (2 * this.pw) < 0.8; }
  steps() { return this.mode === 'single' ? this.n : this.n / 2; }
  layout(force) {
    const single = this.wantSingle(), mode = single ? 'single' : 'spread';
    if (mode !== this.mode || force) {
      let p = this.pos;
      if (this.mode === 'spread' && mode === 'single') p = Math.min(this.n - 1, 2 * this.pos);
      if (this.mode === 'single' && mode === 'spread') p = Math.ceil(this.pos / 2);
      if (this.mode === null) p = 0;
      this.mode = mode; this.pos = p; this.rebuild();
    }
    const vw = innerWidth - 24, vh = innerHeight - 150;
    const bw = (this.mode === 'single' ? 1 : 2) * this.pw;
    const s = Math.min(vw / bw, vh / this.ph, this.maxScale);
    this.scale = s;
    this.wrap.style.width = bw * s + 'px'; this.wrap.style.height = this.ph * s + 'px';
    this.book.style.width = bw + 'px'; this.book.style.height = this.ph + 'px';
    this.book.style.transform = `scale(${s})`; this.apply(true);
  }
  rebuild() {
    this.book.innerHTML = ''; this.leaves = []; const single = this.mode === 'single', L = this.steps();
    for (let i = 0; i < L; i++) {
      const leaf = document.createElement('div'); leaf.className = 'leaf'; leaf.style.width = this.pw + 'px'; leaf.style.left = single ? '0' : this.pw + 'px';
      const f = document.createElement('div'), b = document.createElement('div'); f.className = 'face front'; b.className = 'face back';
      f.appendChild(this.pages[single ? i : 2 * i]);
      if (single) b.classList.add('blankface'); else b.appendChild(this.pages[2 * i + 1]);
      leaf.append(f, b); this.book.appendChild(leaf); this.leaves.push({ el: leaf, f, b });
    }
  }
  apply(instant) {
    const L = this.leaves.length, single = this.mode === 'single';
    this.leaves.forEach((l, i) => {
      const fl = i < this.pos; l.el.classList.toggle('flipped', fl);
      if (instant) l.el.style.zIndex = fl ? i : L - i;
      l.f.classList.toggle('vis', i === this.pos);
      l.b.classList.toggle('vis', !single && i === this.pos - 1);
    });
    let x = 0; if (!single) x = this.pos === 0 ? -this.pw / 2 : this.pos === L ? this.pw / 2 : 0;
    this.book.style.setProperty('--sh', x + 'px');
    this.book.style.transform = `scale(${this.scale}) translateX(${x}px)`;
    this.book.classList.toggle('instant', !!instant);
    const label = single ? `${this.pos + 1} / ${this.n}` : (this.pos === 0 ? '1' : this.pos === L ? `${this.n}` : `${2 * this.pos}–${2 * this.pos + 1}`) + ` / ${this.n}`;
    this.onchange(this.pos, L, label, this.mode);
  }
  go(p) {
    const L = this.leaves.length; p = Math.max(0, Math.min(single_max(this), p)); if (p === this.pos) return;
    const lo = Math.min(p, this.pos), hi = Math.max(p, this.pos);
    this.leaves.forEach((l, i) => { if (i >= lo && i < hi) l.el.style.zIndex = 1000 + i; });
    this.pos = p; this.apply(false);
    clearTimeout(this._t); this._t = setTimeout(() => this.leaves.forEach((l, i) => l.el.style.zIndex = i < this.pos ? i : L - i), 900);
  }
  setPages(arr) { this.pages = arr.slice(); if (this.pages.length % 2) { const b = document.createElement('div'); b.className = 'pg blank'; this.pages.push(b); } this.n = this.pages.length; this.rebuild(); this.layout(); }
  next() { this.go(this.pos + 1); } prev() { this.go(this.pos - 1); }
}
function single_max(fb) { return fb.mode === 'single' ? fb.n - 1 : fb.n / 2; }
