"""Wire the baked wave sprite into index.html: replaces section 7 (mountFigure), the hero-figure CSS and markup.
Idempotent: re-running after a re-bake just swaps the embedded sprite."""
import io, os, re, json, base64
HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "..", "..", "index.html")
s = io.open(F, encoding="utf-8").read()
meta = json.load(open(os.path.join(HERE, "wave.json")))
b64 = base64.b64encode(open(os.path.join(HERE, "wave.png"), "rb").read()).decode()

# ── 1. JS: section 7 ──
i = s.index("/* ═══════════════════════════════════════════════════════════════\n   7. the waving Alex")
j = s.index("\nwindow.__ad = {")
JS = r'''/* ═══════════════════════════════════════════════════════════════
   7. the waving Alex — a real clip of Alex waving, cut out of its
      background and pre-baked into character cells (one pixel of the
      embedded sprite sheet = one glyph: value / 10 = ramp level,
      255 = empty). Played back over an even field of dots, the way
      aino resolves its portraits. The glyph grid is fixed, so the type
      size is derived from the height of the figure.
   ═══════════════════════════════════════════════════════════════ */
function mountFigure(fig) {
  const pre = $('.ascii', fig), D = fig.dataset;
  const SC = +D.cols, SR = +D.rows, N = +D.frames, PER = +D.perRow, FPS = +D.fps || 14.5, STILL = +D.still || 0;
  let frames = null, cols = SC, rows = SR, visible = false, raf = 0, revealAt = 0, last = 0, shown = -2;
  const t0 = performance.now();

  const img = new Image();
  img.onload = () => {
    const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
    const x = c.getContext('2d', { willReadFrequently: true }); x.drawImage(img, 0, 0);
    const px = x.getImageData(0, 0, c.width, c.height).data;
    frames = Array.from({ length: N }, (_, k) => {
      const fr = new Uint8Array(SC * SR), ox = (k % PER) * SC, oy = ((k / PER) | 0) * SR;
      for (let r = 0; r < SR; r++) for (let q = 0; q < SC; q++) { const v = px[((oy + r) * c.width + ox + q) * 4]; fr[r * SC + q] = v > 240 ? 255 : Math.round(v / 10); }
      return fr;
    });
    revealAt = performance.now(); last = 0; shown = -2; draw(performance.now());
  };
  img.src = D.sprite;

  const fit = () => {
    const r = fig.getBoundingClientRect(); if (!r.height) return;
    const capH = 1.5 * LH();                                           // the caption strip under the field
    const lh = Math.max(3, Math.min((r.height - capH) / (SR + 3), r.width / (SC * .5)));   // +3: a little headroom above the hair
    pre.style.lineHeight = lh.toFixed(3) + 'px'; pre.style.fontSize = (lh * .8).toFixed(3) + 'px';
    const chw = measureAdvance(pre);
    cols = Math.max(SC, Math.floor(r.width / chw)); rows = Math.max(SR, Math.floor((r.height - capH) / lh));
  };

  const draw = now => {
    if (raf) cancelAnimationFrame(raf); raf = 0;
    if (!fig.offsetParent) return;
    if (visible && !REDUCED) raf = requestAnimationFrame(draw);
    if (now - last < 1000 / 30) return; last = now;                     // 30 fps while resolving…
    const t = (now - t0) / 1000, rv = clamp((now - revealAt) / 1800, 0, 1);
    const k = frames ? (REDUCED ? STILL : Math.floor(t * FPS) % N) : -1;
    if (rv >= 1 && k === shown) return; shown = rv >= 1 ? k : -2;       // …then only when the clip advances (14.5 fps)
    const fr = frames ? frames[k] : null;
    const x0 = Math.floor((cols - SC) / 2), y0 = rows - SR;              // the sprite is centred on Alex's torso, so centring it centres him
    const lines = new Array(rows);
    for (let r = 0; r < rows; r++) {
      let line = '';
      for (let c = 0; c < cols; c++) {
        if (rv < 1) { const h = hash2(c, r); if (h > rv) { line += h > rv + .1 ? '·' : UE[(Math.random() * UE.length) | 0]; continue; } }   // still resolving
        const sc = c - x0, sr = r - y0;
        const v = fr && sc >= 0 && sc < SC && sr >= 0 ? fr[sr * SC + sc] : 255;
        if (v !== 255) { line += FLOW[v]; continue; }
        line += '·';                                                          // an even field of dots, like aino's
      }
      lines[r] = line;
    }
    pre.textContent = lines.join('\n');
  };
  const refit = () => { fit(); last = 0; shown = -2; draw(performance.now()); };
  new IntersectionObserver(([e]) => { const was = visible; visible = e.isIntersecting; if (visible && !was) { revealAt = performance.now(); refit(); } }, { threshold: .05 }).observe(fig);
  new ResizeObserver(refit).observe(fig);
  refit();
}
'''
s = s[:i] + JS + s[j:]

# ── 2. CSS ──
css_new = '''.hero-figure{position:relative;height:clamp(380px, calc(100dvh - 148px), 1100px);overflow:hidden}   /* fills the space between the nav and the footer */
.hero-figure .ascii{
  position:absolute;inset:0;display:block;white-space:pre;text-transform:none;user-select:none;pointer-events:none;
  color:var(--black);font-family:var(--mono);font-size:8px;line-height:10px;letter-spacing:.02em;font-weight:500;
  padding:0;overflow:hidden;
}'''
s, n1 = re.subn(r"\.hero-figure\{position:relative;height:[^}]*\}\n\.hero-figure \.ascii\{.*?\n\}", lambda m: css_new, s, count=1, flags=re.S)
s, n2 = re.subn(r"  \.hero-figure\{height:[^}]*\}", "  .hero-figure{height:min(72vh, 640px)}", s, count=1)
home_new = ".home{flex:1;display:flex;flex-direction:column;justify-content:center;padding:calc(var(--line) * 4) 0 0}"
s, n3 = re.subn(r"\.home\{flex:1;display:flex;flex-direction:column;justify-content:center;padding:[^}]*\}", lambda m: home_new, s, count=1)

# ── 3. markup ──
fig_new = ('''      <!-- a real clip of Alex waving, baked to ASCII cells (tools/ascii-wave/). The sprite is embedded so the page stays one file. -->
      <figure class="hero-figure fadein" data-figure data-cols="%(cols)d" data-rows="%(rows)d" data-frames="%(frames)d" data-per-row="%(perRow)d" data-fps="%(fps)s" data-still="%(still)d" role="img" aria-label="Alex, rendered live in ASCII characters, waving hello"
        data-sprite="data:image/png;base64,''' % dict(meta, still=meta.get("still", 40))) + b64 + '''">
        <pre class="ascii"></pre>
        <figcaption class="cap"><span>◆ Alex.ascii</span><span>Waving</span></figcaption>
      </figure>'''
s, n4 = re.subn(r"      <!--[^>]*?-->\n      <figure class=\"hero-figure.*?</figure>", lambda m: fig_new, s, count=1, flags=re.S)
assert all((n1, n2, n3, n4)), (n1, n2, n3, n4)
io.open(F, "w", encoding="utf-8", newline="\n").write(s)
print("ok | css", n1, n2, n3, "| markup", n4, "| sprite b64", len(b64), "chars | html", len(s.encode("utf-8")), "bytes | cartoon left:", s.count("paintCartoon"))
