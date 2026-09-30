"""Builds ../../accents.html: the live site with a floating accent-colour switcher, so the candidate accents can be
compared on every page (intro, landing, work, about, contact). Click a swatch, or press 1–7. Not deployed."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "index.html")
OUT = os.path.join(HERE, "..", "..", "accents.html")
ACC = [("orange", "#F26B3A", "current"), ("lime", "#C8F04A", ""), ("yellow", "#FFD449", ""), ("sky", "#6FA8FF", ""),
       ("columbia", "#B9D9EB", "Columbia blue"), ("mint", "#7CE0B4", ""), ("white", "#FFFFFF", "monochrome")]
s = io.open(SRC, encoding="utf-8").read()
s = s.replace("<title>", "<title>Accent options · ", 1)
sw = "".join(f'<button data-hex="{h}" title="{n}{(" · " + note) if note else ""}"><i style="background:{h}"></i>{n}</button>' for n, h, note in ACC)
UI = f'''
<style>
.accents{{position:fixed;left:50%;bottom:calc(var(--line) * 1.25);transform:translateX(-50%);z-index:100;display:flex;align-items:center;gap:var(--ch);
  padding:0 var(--ch);line-height:calc(var(--line) * 2);background:var(--white);border:1px solid var(--black);border-radius:var(--radius);white-space:nowrap;text-transform:uppercase}}
.accents button{{display:inline-flex;align-items:center;gap:calc(var(--ch) * .6);padding:0 var(--ch);color:rgba(var(--black-rgb),.6)}}
.accents button i{{display:inline-block;width:var(--line);height:var(--line);border-radius:50%;border:1px solid rgba(var(--black-rgb),.25)}}
.accents button.on,.accents button:hover{{color:var(--black)}}
.accents button.on i{{box-shadow:0 0 0 2px var(--white),0 0 0 3px var(--black)}}
.accents .hex{{color:rgba(var(--black-rgb),.45);margin-left:var(--ch)}}
@media (max-width:768px){{.accents button{{font-size:0;gap:0;padding:0 calc(var(--ch) * .5)}}.accents .hex{{display:none}}}}
</style>
<nav class="accents" aria-label="Accent colour">{sw}<span class="hex"></span></nav>
<script>
(() => {{
  const root = document.documentElement, bar = document.querySelector('.accents'), btns = [...bar.querySelectorAll('button')], hex = bar.querySelector('.hex');
  const set = h => {{
    const r = parseInt(h.slice(1, 3), 16), g = parseInt(h.slice(3, 5), 16), b = parseInt(h.slice(5, 7), 16);
    root.style.setProperty('--accent', h); root.style.setProperty('--accent-rgb', r + ',' + g + ',' + b);
    btns.forEach(x => x.classList.toggle('on', x.dataset.hex === h)); hex.textContent = h; try {{ localStorage.setItem('accent-preview', h); }} catch {{}}
  }};
  btns.forEach(x => x.addEventListener('click', () => set(x.dataset.hex)));
  addEventListener('keydown', e => {{ const k = +e.key; if (k >= 1 && k <= btns.length && !e.target.closest('input,textarea')) set(btns[k - 1].dataset.hex); }});
  let saved = null; try {{ saved = localStorage.getItem('accent-preview'); }} catch {{}}
  set(btns.some(x => x.dataset.hex === saved) ? saved : btns[0].dataset.hex);
}})();
</script>
'''
s = s.replace("</body>", UI + "</body>", 1)
io.open(OUT, "w", encoding="utf-8", newline="\n").write(s)
print("accents.html", len(s) // 1024, "KB,", len(ACC), "swatches")
