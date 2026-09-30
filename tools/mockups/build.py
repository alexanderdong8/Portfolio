"""Builds ../../mockups.html: the landing page in several headline layouts, side by side, built from
the live index.html (its CSS, its ASCII engine, its waving-Alex sprite, its nav and footer) so every
mockup is exactly what the site would render. Open mockups.html and press 1–6 or ← →."""
import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "index.html")
OUT = os.path.join(HERE, "..", "..", "mockups.html")
s = io.open(SRC, encoding="utf-8").read()

head = s[s.index("<head>"):s.index("</head>") + 7]
head = re.sub(r"<title>.*?</title>", "<title>Alex Dong — landing page mockups</title>", head, count=1)
head = head.replace('</head>', '<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@1,6..72,400&family=Cormorant+Garamond:ital,wght@1,500;1,600&family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,500&family=Bodoni+Moda:ital,opsz,wght@1,6..96,400;1,6..96,500&display=swap" rel="stylesheet">\n</head>')
engine = s[s.index("<script>"):s.index("</script>") + 9]; assert "window.__ad" in engine
probe = re.search(r'<span class="probe" id="probe"[^>]*>M+</span>', s).group(0)
nav = re.search(r"<nav id=\"nav\".*?</nav>", s, re.S).group(0)
footer = re.search(r"<footer id=\"footer\">.*?</footer>", s, re.S).group(0)
fig = re.search(r"<figure class=\"hero-figure[^\"]*\"[^>]*data-figure.*?</figure>", s, re.S).group(0).replace('class="hero-figure fadein"', 'class="hero-figure"')

BTN = '''<div class="buttons">
            <a class="button solid hoverchar" href="#">About me <span class="arr">→</span></a>
            <a class="button hoverchar" href="#">All projects <span class="arr">→</span></a>
          </div>'''
def panel(n, name, text, mirror=False, cls="", buttons=True):
    cols = [f'<div class="hero-text">\n          {text}\n          {BTN if buttons else ""}\n        </div>', fig]
    if mirror: cols.reverse()
    return f'''  <section class="mock home v{n} {cls}" data-name="{name}" hidden>
      <div class="hero-grid">
        {cols[0]}
        {cols[1]}
      </div>
    </section>'''

STAMP = lambda rows, scale, extra="": f'<span class="logo-inline" data-stamp data-rows="{rows}" data-scale="{scale}" {extra}role="img" aria-label="Alex"></span>'
LEAD0 = 'data-lead="0" '          # nothing else shares the line: the stamp may use the whole column
CAPS = 'data-valign="caps" '      # centre the stamp on the capitals (text-sized use)
panels = [
    panel(1, "Inline, big: “I’m ALEX” on one line, tagline under it",
          f'<h1 class="mega"><span class="l1">I\'m {STAMP(26, 5)}</span><span class="l2">a CS student at <em>Columbia</em></span></h1>'),
    panel(2, "Stacked: I’m / ALEX / a CS student at Columbia",
          f'<h1 class="mega stack"><span class="l0">I\'m</span><span class="lA">{STAMP(28, 5.5, LEAD0)}</span><span class="l2">a CS student at <em>Columbia</em></span></h1>'),
    panel(3, "Text-size: ALEX set into the sentence, as before",
          f'<h1 class="mega">I\'m {STAMP(14, 1.6, CAPS)}, a computer science student at <em>Columbia University</em>.</h1>'),
    panel(4, "Monument: ALEX fills the column, mono lines around it",
          f'<p class="eyebrow"><span class="dia">◆</span>Hi, I\'m</p>\n          <h1 class="mega">{STAMP(36, 9, LEAD0)}</h1>\n          <div class="meta"><span>A CS student at Columbia</span><span class="muted">New York · 2026</span></div>'),
    panel(5, "Mirrored: figure on the left, stacked headline on the right",
          f'<h1 class="mega stack"><span class="l0">I\'m</span><span class="lA">{STAMP(28, 5.5, LEAD0)}</span><span class="l2">a CS student at <em>Columbia</em></span></h1>', mirror=True),
    panel(6, "Editorial: big ALEX, tagline in the About page’s serif",
          f'<h1 class="mega"><span class="l1">I\'m {STAMP(26, 5)}</span><span class="l2 serif">a CS student at <em>Columbia</em></span></h1>'),
]

# ── set 2: the direction from 4 + 6 — small mono "HI, I'M", a big-but-not-huge ALEX, the serif tagline,
#           no rule, no date; eight ways to place the two links so the figure stays the star ──
EYE = '<p class="eyebrow"><span class="dia">◆</span>Hi, I\'m</p>'
BIG = lambda: f'<h1 class="mega">{STAMP(36, 9, LEAD0)}</h1>'          # column-limited: the h1's width sets the size
TAG = '<p class="tag">a CS student at <em>Columbia</em></p>'
LINKS = '<nav class="links"><a href="#" class="hoverchar">About me<span class="arr">→</span></a><a href="#" class="hoverchar">All projects<span class="arr">→</span></a></nav>'
panels += [
    panel(7, "Eyebrow row: the links share the “HI, I’M” line",
          f'<div class="eyerow">{EYE}{LINKS}</div>\n          {BIG()}\n          {TAG}', cls="set2", buttons=False),
    panel(8, "Mono links: quiet text links under the tagline",
          f'{EYE}\n          {BIG()}\n          {TAG}\n          {LINKS}', cls="set2", buttons=False),
    panel(9, "Half and half: the figure gets as much width as the text",
          f'{EYE}\n          {BIG()}\n          {TAG}\n          {LINKS}', cls="set2", buttons=False),
    panel(10, "Wide field: the figure’s dot field is the bigger column",
          f'{EYE}\n          {BIG()}\n          {TAG}\n          {LINKS}', cls="set2", buttons=False),
    panel(11, "Bottom-anchored: the text block sits level with the figure’s caption",
          f'{EYE}\n          {BIG()}\n          {TAG}\n          {LINKS}', cls="set2", buttons=False),
    panel(12, "Top and bottom: name at the head height, links at the feet",
          f'<div class="top">{EYE}\n          {BIG()}\n          {TAG}</div>\n          {LINKS}', cls="set2", buttons=False),
    panel(13, "Peers: a smaller ALEX and a bigger serif line, boxed buttons",
          f'{EYE}\n          <h1 class="mega">{STAMP(22, 3.2, LEAD0)}</h1>\n          {TAG}', cls="set2"),
    panel(14, "Serif links: the links are a second serif line, no buttons",
          f'{EYE}\n          {BIG()}\n          {TAG}\n          <p class="taglinks"><a href="#">See my work →</a><span class="or">or</span><a href="#">say hello →</a></p>', cls="set2", buttons=False),
]

# ── set 3: 13, refined — "Hi, I'm" in the tagline's italic (no diamond), ALEX a step bigger, the tagline held to
#           about ALEX's width and well under its height; then the same lockup in three other italics ──
HI = '<p class="hi">Hi, I\'m</p>'
LOCKUP = lambda: f'{HI}\n          <h1 class="mega">{STAMP(26, 4, LEAD0)}</h1>\n          {TAG}'
panels += [
    panel(15, "13 refined: serif “Hi, I’m”, bigger ALEX, tagline no wider than ALEX — Newsreader italic", LOCKUP(), cls="set3"),
    panel(16, "Same lockup in Cormorant Garamond italic", LOCKUP(), cls="set3"),
    panel(17, "Same lockup in Fraunces italic", LOCKUP(), cls="set3"),
    panel(18, "Same lockup in Bodoni Moda italic", LOCKUP(), cls="set3"),
]

# ── set 4: 15 (Newsreader) with a much smaller "Hi, I'm"; then ALEX wider, or the tagline smaller, or both ──
L4 = lambda rows, scale: f'{HI}\n          <h1 class="mega">{STAMP(rows, scale, LEAD0)}</h1>\n          {TAG}'
panels += [
    panel(19, "15 with a much smaller “Hi, I’m” and a wider ALEX that runs past the tagline", L4(28, 5), cls="set3 set4"),
    panel(20, "15 with a much smaller “Hi, I’m” and a smaller tagline instead", L4(26, 4), cls="set3 set4 tagsmall"),
    panel(21, "Both: smaller “Hi, I’m”, wider ALEX, smaller tagline", L4(27, 4.6), cls="set3 set4 tagsmall"),
]

# ── set 5: 21 with "Hi, I'm" nudged right (and a little more air under it) ──
panels += [
    panel(22, "21 with “Hi, I’m” nudged right a little (2ch)", L4(27, 4.6), cls="set3 set4 tagsmall set5"),
    panel(23, "21 with “Hi, I’m” nudged right more (5ch)", L4(27, 4.6), cls="set3 set4 tagsmall set5"),
    panel(24, "21 with “Hi, I’m” over the A’s inside edge (9ch)", L4(27, 4.6), cls="set3 set4 tagsmall set5"),
]

# ── set 6: the whole block nudged right; the two small lines in the site's aino-style fonts —
#           "sans" = the bold grotesk of the headings/ALEX, "mono" = the uppercase header font, "serif" = Newsreader italic ──
HI_F = lambda f: f'<p class="hi {f}">Hi, I\'m</p>'
TAG_F = lambda f: f'<p class="tag {f}">a CS student at <em>Columbia</em></p>'
L6 = lambda hf, tf: f'{HI_F(hf)}\n          <h1 class="mega">{STAMP(27, 4.6, LEAD0)}</h1>\n          {TAG_F(tf)}'
panels += [
    panel(25, "Block nudged right · both lines in the bold grotesk (aino’s headline voice)", L6("sans", "sans"), cls="set3 set4 tagsmall set6"),
    panel(26, "Bold grotesk “Hi, I’m” · tagline in the header’s uppercase mono", L6("sans", "mono"), cls="set3 set4 tagsmall set6"),
    panel(27, "Uppercase mono “Hi, I’m” · tagline in the bold grotesk", L6("mono", "sans"), cls="set3 set4 tagsmall set6"),
    panel(28, "Italic “Hi, I’m” · tagline in the bold grotesk", L6("serif", "sans"), cls="set3 set4 tagsmall set6"),
    panel(29, "Bold grotesk “Hi, I’m” · italic tagline", L6("sans", "serif"), cls="set3 set4 tagsmall set6"),
    panel(30, "Uppercase mono “Hi, I’m” · italic tagline", L6("mono", "serif"), cls="set3 set4 tagsmall set6"),
]

# ── set 7: 27's mono "HI, I'M" + 26's mono tagline; block nudged right less (4ch); the tagline at four sizes ──
panels += [
    panel(31, "Mono + mono · tagline small (14px), header-sized", L6("mono", "mono"), cls="set3 set4 tagsmall set6 set7 t1"),
    panel(32, "Mono + mono · tagline medium (17px)", L6("mono", "mono"), cls="set3 set4 tagsmall set6 set7 t2"),
    panel(33, "Mono + mono · tagline large (21px)", L6("mono", "mono"), cls="set3 set4 tagsmall set6 set7 t3"),
    panel(34, "Mono + mono · tagline largest (26px)", L6("mono", "mono"), cls="set3 set4 tagsmall set6 set7 t4"),
]

CSS = '''
<style>
/* ── mockup-only rules (everything else is the site's own CSS) ── */
.mock.home{padding-top:calc(var(--line) * 4)}
.hero-grid .hero-text{min-width:0}
/* v2 / v5: stacked */
.stack .l0,.stack .lA,.stack .l2{display:block}
.stack .l0{line-height:1.1}
.stack .lA{line-height:0;margin:.28em 0 .5em}
.stack .l2{margin-top:0}
/* v3: text-sized stamp inside a running sentence */
.v3 .mega{line-height:calc(var(--line) * 3);max-width:calc(var(--ch) * 96)}
/* v4: monument */
.v4 .eyebrow{text-transform:uppercase;color:rgba(var(--black-rgb),.5);margin-bottom:calc(var(--line) * 1.25)}
.v4 .eyebrow .dia{color:var(--accent);margin-right:var(--ch)}
.v4 h1.mega{line-height:0}
.v4 .meta{display:flex;justify-content:space-between;gap:var(--char2);margin-top:calc(var(--line) * 1.75);padding-top:var(--line);border-top:1px solid var(--black);text-transform:uppercase}
.v4 .buttons{margin-top:calc(var(--line) * 2)}
/* v5: mirrored columns */
.v5 .hero-grid{grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr)}
/* v6: serif tagline */
.v6 .l2.serif{font-family:var(--serif);font-weight:400;font-style:italic;font-size:calc(var(--fs) * 3.8);letter-spacing:-.01em;line-height:1.1;margin-top:calc(var(--line) * .75)}
.v6 .l2.serif em{font-style:italic}
@media (max-width:768px){
  .v5 .hero-grid{grid-template-columns:1fr}
  .v6 .l2.serif{font-size:calc(var(--fs) * 2.6)}
}
/* ── set 2 (7–14): eyebrow / ALEX / serif tagline / links ── */
.set2 .eyebrow{text-transform:uppercase;color:rgba(var(--black-rgb),.5)}
.set2 .eyebrow .dia{color:var(--accent);margin-right:var(--ch)}
.set2 h1.mega{line-height:0;width:68%;margin:calc(var(--line) * 1.25) 0}
.set2 .tag{font-family:var(--serif);font-style:italic;font-weight:400;font-size:calc(var(--fs) * 3.8);line-height:1.1;letter-spacing:-.01em;text-transform:none;text-wrap:balance}
.set2 .tag em{font-style:italic;color:var(--accent)}
.set2 .links{display:flex;flex-wrap:wrap;gap:calc(var(--ch) * 4);margin-top:calc(var(--line) * 2);text-transform:uppercase;color:rgba(var(--black-rgb),.62)}
.set2 .links a{transition:color .2s}
.set2 .links a:hover{color:var(--accent)}
.set2 .links .arr{display:inline-block;margin-left:var(--ch);transition:transform .3s var(--ease)}
.set2 .links a:hover .arr{transform:translateX(calc(var(--ch) * .4))}
.set2 .eyerow{display:flex;justify-content:space-between;align-items:baseline;gap:var(--char2)}
.set2 .eyerow .links{margin-top:0}
.set2 .taglinks{font-family:var(--serif);font-style:italic;font-size:calc(var(--fs) * 2.6);line-height:1.2;margin-top:calc(var(--line) * 1.25);color:var(--accent);text-transform:none}
.set2 .taglinks a{transition:color .2s}
.set2 .taglinks a:hover{color:var(--black)}
.set2 .taglinks .or{color:rgba(var(--black-rgb),.45);margin:0 var(--char2)}
.set2 .buttons{margin-top:calc(var(--line) * 2)}
.v9 .hero-grid{grid-template-columns:1fr 1fr}
.v10 .hero-grid{grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr)}
.v10 h1.mega{width:100%}
.v10 .links{flex-direction:column;gap:calc(var(--line) * .5)}
.v11 .hero-grid{align-items:end}
.v12 .hero-grid{align-items:stretch}
.v12 .hero-text{display:flex;flex-direction:column;justify-content:space-between;padding-top:calc(var(--line) * .5)}
.v12 .links{margin-top:0}
.v13 h1.mega{width:auto}
.v13 .tag{font-size:calc(var(--fs) * 4.6)}
.v14 h1.mega{width:60%}
@media (max-width:768px){
  .v9 .hero-grid,.v10 .hero-grid{grid-template-columns:1fr}
  .set2 h1.mega{width:100%}
  .set2 .tag{font-size:calc(var(--fs) * 2.6)}
  .v13 .tag{font-size:calc(var(--fs) * 3)}
}
/* ── set 3 (15–18): "Hi, I'm" / ALEX / tagline, all three left-aligned; the two italic lines match ── */
.set3 .hi,.set3 .tag{font-family:var(--serif);font-style:italic;font-weight:400;font-size:calc(var(--fs) * 3);line-height:1.15;letter-spacing:-.005em;text-transform:none}
.set3 .tag em{font-style:italic;color:var(--accent)}
.set3 h1.mega{line-height:0;width:auto;margin:calc(var(--line) * .75) 0}
.set3 .buttons{margin-top:calc(var(--line) * 2)}
.v16 .hi,.v16 .tag{font-family:"Cormorant Garamond",var(--serif);font-weight:500;font-size:calc(var(--fs) * 3.5)}
.v17 .hi,.v17 .tag{font-family:"Fraunces",var(--serif);font-weight:400;font-size:calc(var(--fs) * 2.85);font-variation-settings:"SOFT" 40,"opsz" 72}
.v18 .hi,.v18 .tag{font-family:"Bodoni Moda",var(--serif);font-weight:400;font-size:calc(var(--fs) * 3.2)}
@media (max-width:768px){
  .set3 .hi,.set3 .tag{font-size:calc(var(--fs) * 2.2)}
  .v16 .hi,.v16 .tag{font-size:calc(var(--fs) * 2.6)}
}
/* ── set 4 (19–21): Newsreader; "Hi, I'm" much smaller; ALEX wider and/or the tagline smaller ── */
.set4 .hi{font-size:calc(var(--fs) * 1.7);color:rgba(var(--black-rgb),.8)}
.set4 h1.mega{margin:calc(var(--line) * .5) 0 calc(var(--line) * .75)}
.set4.tagsmall .tag{font-size:calc(var(--fs) * 2.4)}
@media (max-width:768px){
  .set4 .hi{font-size:calc(var(--fs) * 1.4)}
  .set4.tagsmall .tag{font-size:calc(var(--fs) * 1.9)}
}
/* ── set 5 (22–24): "Hi, I'm" indented, a little more air below it ── */
.set5 .hi{margin-bottom:calc(var(--line) * .25)}
.v22 .hi{padding-left:calc(var(--ch) * 2)}
.v23 .hi{padding-left:calc(var(--ch) * 5)}
.v24 .hi{padding-left:calc(var(--ch) * 9)}
/* ── set 6 (25–30): whole block nudged right; small lines in sans / mono / serif ── */
.set6 .hero-text{padding-left:calc(var(--ch) * 8)}
.set6 .hi{margin-bottom:calc(var(--line) * .35)}
.set6 .hi.sans,.set6 .tag.sans{font-family:var(--sans);font-style:normal;font-weight:700;letter-spacing:-.025em;text-transform:none}
.set6 .hi.sans{font-size:calc(var(--fs) * 1.8);line-height:1.2;color:var(--black)}
.set6 .tag.sans{font-size:calc(var(--fs) * 2.5);line-height:1.15}
.set6 .tag.sans em{font-style:normal;color:var(--accent)}
.set6 .hi.mono,.set6 .tag.mono{font-family:var(--mono);font-style:normal;font-weight:500;text-transform:uppercase;letter-spacing:.06em}
.set6 .hi.mono{font-size:calc(var(--fs) * 1.1);line-height:var(--line);color:rgba(var(--black-rgb),.6);margin-bottom:calc(var(--line) * .5)}
.set6 .tag.mono{font-size:calc(var(--fs) * 1.35);line-height:calc(var(--line) * 1.5);margin-top:calc(var(--line) * .25)}
.set6 .tag.mono em{font-style:normal;color:var(--accent)}
@media (max-width:768px){
  .set6 .hero-text{padding-left:0}
  .set6 .tag.sans{font-size:calc(var(--fs) * 2)}
}
/* ── set 7 (31–34): mono "HI, I'M" + mono tagline, block nudged 4ch, tagline sizes ── */
.set7 .hero-text{padding-left:calc(var(--ch) * 4)}
.set7 .tag.mono{margin-top:calc(var(--line) * .5);letter-spacing:.08em}
.set7.t1 .tag.mono{font-size:calc(var(--fs) * 1.15);line-height:var(--line)}
.set7.t2 .tag.mono{font-size:calc(var(--fs) * 1.4);line-height:calc(var(--line) * 1.5)}
.set7.t3 .tag.mono{font-size:calc(var(--fs) * 1.75);line-height:calc(var(--line) * 1.75);letter-spacing:.06em}
.set7.t4 .tag.mono{font-size:calc(var(--fs) * 2.2);line-height:calc(var(--line) * 2);letter-spacing:.04em}
@media (max-width:768px){.set7 .hero-text{padding-left:0}}
/* the switcher */
.switch{
  position:fixed;left:50%;bottom:calc(var(--line) * 1.25);transform:translateX(-50%);z-index:100;
  display:flex;align-items:center;gap:var(--char2);padding:0 var(--char2);line-height:calc(var(--line) * 2);
  background:var(--white);border:1px solid var(--black);border-radius:var(--radius);white-space:nowrap;
}
.switch button{padding:0 var(--ch);font-weight:600}
.switch button:hover{color:var(--accent)}
.switch .num{font-weight:600}
.switch .hint{color:rgba(var(--black-rgb),.45)}
@media (max-width:768px){.switch .name,.switch .hint{display:none}}
</style>
'''

html = f'''<!doctype html>
<html lang="en">
{head.replace("</head>", CSS + "</head>")}
<body class="ready">
{probe}

<header>
  {nav}
</header>

<main class="page" id="top">
{chr(10).join(panels)}
</main>

{footer}

<nav class="switch" aria-label="Mockups">
  <button class="prev" aria-label="Previous mockup">‹</button>
  <span class="num">1/6</span>
  <span class="name"></span>
  <button class="next" aria-label="Next mockup">›</button>
  <span class="hint">← → or type a number</span>
</nav>

{engine}

<script>
(() => {{
'use strict';
const {{ $, $$, mountHeroLogo, mountFigure, scramble, TOUCH }} = window.__ad;
const mocks = $$('.mock'), num = $('.switch .num'), name = $('.switch .name');
let cur = -1;
const show = n => {{
  cur = (n + mocks.length) % mocks.length;
  mocks.forEach((m, i) => m.hidden = i !== cur);
  num.textContent = (cur + 1) + '/' + mocks.length; name.textContent = mocks[cur].dataset.name;
  history.replaceState(null, '', '#' + (cur + 1));
  dispatchEvent(new Event('resize')); scrollTo(0, 0);              // stamps refit on resize; figures refit when they come into view
}};
$('.switch .prev').addEventListener('click', () => show(cur - 1));
$('.switch .next').addEventListener('click', () => show(cur + 1));
addEventListener('keydown', e => {{
  if (e.key === 'ArrowRight') show(cur + 1); else if (e.key === 'ArrowLeft') show(cur - 1);
  else if (/^[0-9]$/.test(e.key)) {{                                 // type a number: 7, or 1 then 3 for 13
    const now = Date.now(), n = (now - (show.at || 0) < 900 && show.buf ? show.buf : '') + e.key;
    show.at = now; show.buf = n; const k = parseInt(n); if (k >= 1 && k <= mocks.length) show(k - 1); else show.buf = e.key;
  }}
}});
addEventListener('hashchange', () => {{ const n = parseInt(location.hash.slice(1)); if (n >= 1 && n <= mocks.length && n - 1 !== cur) show(n - 1); }});
show(Math.max(1, Math.min(mocks.length, parseInt(location.hash.slice(1)) || 1)) - 1);
$$('[data-stamp]').forEach(pre => mountHeroLogo(pre, 'ALEX', {{ rows: +pre.dataset.rows || 26, scale: +pre.dataset.scale || 5 }}));
$$('[data-figure]').forEach(mountFigure);
if (!TOUCH) $$('.hoverchar').forEach(el => el.addEventListener('mouseenter', () => scramble(el, {{ duration: 420, speed: 22 }})));
const clocks = $$('.clock'), tick = () => {{ const t = new Date().toLocaleTimeString([], {{ hour12: false }}); clocks.forEach(c => c.textContent = t); }}; tick(); setInterval(tick, 1000);
}})();
</script>
</body>
</html>
'''
io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
print("mockups.html:", len(html.encode("utf-8")) // 1024, "KB |", len(panels), "panels | figure copies:", html.count("data-figure"), "| stamps:", html.count("data-stamp"))
