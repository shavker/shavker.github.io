#!/usr/bin/env python3
"""Собирает deck/vanya/vanya-directors-notes.pdf из index.html: горизонтальные слайды 1920x1080.
Текст берётся из index.html, поэтому после правок страницы достаточно перезапустить скрипт.
Запуск: python3 deck/vanya/_pdf/build_pdf.py
"""
import re, subprocess, tempfile
from pathlib import Path

DECK = Path(__file__).resolve().parent.parent
SRC = (DECK / "index.html").read_text()
OUT = DECK / "vanya-directors-notes.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def section(sel):
    m = re.search(r'<section class="' + sel + r'"[^>]*>(.*?)</section>', SRC, re.S)
    return m.group(1) if m else ""


def by_id(i):
    m = re.search(r'<section[^>]*id="' + i + r'"[^>]*>(.*?)</section>', SRC, re.S)
    return m.group(1)


hero = section("hero")
hero = re.sub(r'<div class="hero-actions">.*?</div>', "", hero, flags=re.S)
intro = re.search(r'<section class="grid">\s*(<dl class="meta">.*?)</section>', SRC, re.S).group(1)
meta = re.search(r'<dl class="meta">.*?</dl>', intro, re.S).group(0)
copy = re.search(r'<div class="copy">.*?</div>', intro, re.S).group(0)
refs = re.findall(r'poster="\./media/(ref-[\w-]+\.jpg)"', by_id("refs"))
how = by_id("how")
how = re.sub(r'<div class="label">.*?</div>', "", how, count=1)

def top(page):
    return f'<div class="top"><span>Anton Shavkero · Director\'s notes</span><span>Как Ваня скажет</span><span>{page}</span></div>'

slides = []
slides.append(f'<section class="slide s-title">{top("01")}<div class="inner">{hero}{meta}</div></section>')
gal = "".join(f'<img src="{(DECK / "media" / r).as_uri()}">' for r in refs)
slides.append(f'<section class="slide s-idea">{top("02")}<div class="inner"><div class="col"><div class="label">Идея съёмки</div>{copy}</div><div class="col"><div class="label">Референсы</div><div class="gal{' g8' if len(refs)>4 else ''}">{gal}</div></div></div></section>')
n = 3
for sid in ["s1", "s2", "s3", "s4"]:
    body = by_id(sid)
    sb = re.search(r'<div class="sb">(.*?)</div><!--/sb-->', body, re.S)
    body = re.sub(r'<div class="sb">.*?</div><!--/sb-->', "", body, flags=re.S)
    figs = ""
    if sb:
        figs = re.sub(r'src="\./media/', 'src="' + (DECK / "media").as_uri() + '/', sb.group(1))
        figs = re.sub(r'</?a[^>]*>', '', figs)
    cm = re.search(r'<div class="case-meta">.*?</div>\s*(?=<div class="shots">)', body, re.S).group(0)
    sh = body[body.index('<div class="shots">'):]
    fl = re.findall(r'<figure>.*?</figure>', figs, re.S)
    if len(fl) > 4:
        # Длинная сцена: два слайда. Первый — первые 2 кадра и 2 карточки, второй — остальное.
        inner = sh[len('<div class="shots">'):sh.rindex('</div>')]
        parts = re.split(r'(?=\n\s*<div class="(?:shot|end)[ "])', inner)
        parts = [x for x in parts if x.strip()]
        groups = [(fl[:2], parts[:2], ' n1'), (fl[2:], parts[2:], ' n3')]
        for fg, pp, cls in groups:
            slides.append(f'<section class="slide s-case split{cls}">{top(f"{n:02d}")}<div class="inner sc"><div class="lc"><div class="strip{cls}">{"".join(fg)}</div>{cm}</div><div class="rc"><div class="shots">{"".join(pp)}</div></div></div></section>')
            n += 1
        continue
    slides.append(f'<section class="slide s-case">{top(f"{n:02d}")}<div class="inner sc"><div class="lc"><div class="strip">{figs}</div>{cm}</div><div class="rc">{sh}</div></div></section>')
    n += 1
light = by_id("light") if 'id="light"' in SRC else ""
if light:
    light = re.sub(r'<div class="label">.*?</div>', "", light, count=1)
    light = light.replace('src="./media/', 'src="' + (DECK / "media").as_uri() + '/')
    slides.append(f'<section class="slide s-light">{top(f"{n:02d}")}<div class="inner"><div class="label">Свет</div>{light}</div></section>')
    n += 1
decor = by_id("decor") if 'id="decor"' in SRC else ""
if decor:
    decor = re.sub(r'<div class="label">.*?</div>', "", decor, count=1)
    decor = decor.replace('src="./media/', 'src="' + (DECK / "media").as_uri() + '/')
    slides.append(f'<section class="slide s-light s-decor">{top(f"{n:02d}")}<div class="inner"><div class="label">Декорации</div>{decor}</div></section>')
    n += 1
slides.append(f'<section class="slide s-how">{top(f"{n:02d}")}<div class="inner"><div class="label">Как снимать</div>{how}</div></section>')

css = """
@page{size:1920px 1080px;margin:0}
:root{--bg:#f3f1ea;--fg:#101010;--muted:#69675f;--line:rgba(16,16,16,.18);--tile:#dcd9d0;--hi:#e9ff00}
*{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--fg);font-family:Arial,Helvetica,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.slide{width:1920px;height:1080px;padding:56px 72px;display:flex;flex-direction:column;page-break-after:always;overflow:hidden;position:relative}
.top{display:flex;justify-content:space-between;font-size:16px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);border-bottom:1px solid var(--line);padding-bottom:16px}
.inner{flex:1;min-height:0;padding-top:40px;font-size:24px}
.label{font-size:16px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:20px}
mark{background:var(--hi);color:inherit;padding:0 .08em}
q{quotes:none}
.s-title .inner{display:flex;flex-direction:column;justify-content:space-between}
.s-title h1{font-size:210px;line-height:.86;letter-spacing:-.07em;font-weight:500;margin:40px 0 0}.s-title h1 .x{color:var(--muted)}
.s-title .kicker{font-size:46px;line-height:1.05;letter-spacing:-.035em;max-width:1300px;margin:36px 0 0}
.meta{display:grid;grid-template-columns:repeat(5,1fr);gap:24px;margin:0;border-top:1px solid var(--line);padding-top:20px}
.meta dt{font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.meta dd{margin:6px 0 0;font-size:22px}
.s-idea .inner{display:grid;grid-template-columns:600px 1fr;gap:64px}.s-idea .col:last-child{display:flex;flex-direction:column;min-height:0}
.s-idea .copy{font-size:28px;line-height:1.18;letter-spacing:-.02em}.s-idea .copy p{margin:0 0 .8em}
.gal{flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px}.gal.g8{grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(2,1fr)}.gal img{width:100%;height:100%;object-fit:cover;display:block;background:var(--tile)}
.case{display:grid;grid-template-columns:400px 1fr;gap:56px}
.case-meta{display:flex;flex-direction:column;gap:22px}
.case .no{display:flex;justify-content:space-between;font-size:16px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.case h2{font-size:80px;line-height:.9;letter-spacing:-.055em;font-weight:500;margin:0}
.case .desc{font-size:20px;line-height:1.35;margin:0}.case .desc b{display:block;font-weight:400;font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:6px}
.shots{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-content:start}
.shot{background:#fbfaf6;border:1px solid var(--line);padding:24px;display:flex;flex-direction:column;gap:14px}
.shot .cam{display:flex;justify-content:space-between;font-size:15px;text-transform:uppercase;letter-spacing:.06em;border-bottom:1px solid var(--line);padding-bottom:10px}
.shot .cam span:last-child{color:var(--muted)}
.shot.pov .cam span:first-child::before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;background:#e2231a;margin-right:8px;vertical-align:1px}
.shot p{margin:0;font-size:1em;line-height:1.33}
.line{border-left:3px solid var(--fg);padding:2px 0 2px 16px}.line .who{display:block;font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:6px}
.line q{display:block;font-size:1.35em;line-height:1.12;letter-spacing:-.03em}
.trans{grid-column:1/-1;display:flex;gap:18px;align-items:baseline;border-top:1px solid var(--line);padding-top:14px;font-size:.9em}
.trans span:first-child{font-size:14px;text-transform:uppercase;letter-spacing:.06em;background:var(--hi);padding:3px 7px}
.end{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.end .shot{background:var(--fg);color:var(--bg);border-color:var(--fg)}.end .shot .cam{border-color:rgba(243,241,234,.25)}.end .line{border-color:var(--bg)}.end .line .who,.end .shot .cam span:last-child{color:#a9a69c}
.sbg{display:grid;grid-template-columns:690px 690px;gap:18px 28px;justify-content:center}.sbg figure{margin:0;position:relative}.sbg .pov{position:absolute;left:12px;top:12px;background:var(--bg);padding:6px 10px;font-size:15px;text-transform:uppercase;letter-spacing:.06em;line-height:1}.sbg .pov::before{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:#e2231a;margin-right:8px}.sbg img{display:block;width:690px;height:388px;object-fit:cover;background:var(--tile)}.sbg figcaption{display:flex;justify-content:space-between;gap:12px;padding:8px 0 0;font-size:15px;text-transform:uppercase;letter-spacing:.06em}.sbg figcaption span:last-child{color:var(--muted);text-transform:none;letter-spacing:0}
.s-sb .inner{padding-top:24px}
.sc{display:grid;grid-template-columns:1060px 1fr;gap:40px}.lc{display:flex;flex-direction:column;gap:26px;min-width:0}.rc{min-width:0}.rc .shots{grid-template-columns:1fr;gap:12px}.rc .end{grid-template-columns:1fr 1fr}.sc .case-meta{display:grid;grid-template-columns:auto 1fr;gap:6px 40px;align-items:end}.sc .case-meta .no{grid-column:1/-1}.sc .case-meta .desc{max-width:420px}
.strip{display:grid;grid-template-columns:1fr 1fr;gap:16px 16px}.strip figure{margin:0;position:relative;min-width:0}.strip img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:var(--tile)}
.s-case.split .inner{font-size:26px}.split .rc .shots{gap:20px}.split .shot{padding:26px;gap:14px}.split .strip figcaption{font-size:14px}.s-case.split.n1 .sc{grid-template-columns:1fr;grid-template-rows:auto 1fr;gap:30px}.s-case.split.n1 .lc{display:grid;grid-template-columns:1fr 400px;gap:40px;align-items:end}.s-case.split.n1 .inner{font-size:30px}.strip.n1{grid-template-columns:1fr 1fr;gap:16px}.s-case.split.n1 .case-meta{grid-template-columns:1fr;align-self:end}.s-case.split.n1 .case-meta .desc{max-width:none}.s-case.split.n1 .rc .shots{grid-template-columns:1fr 1fr;align-items:stretch}.strip.n3{grid-template-columns:repeat(3,1fr);gap:14px 12px}.strip figcaption{display:flex;justify-content:space-between;gap:8px;padding:6px 0 0;font-size:12px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap;overflow:hidden}.strip figcaption span:last-child{color:var(--muted);text-transform:none;letter-spacing:0;overflow:hidden;text-overflow:ellipsis}
.strip .pov{position:absolute;left:10px;top:10px;background:var(--bg);padding:5px 9px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;line-height:1}.strip .pov::before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;background:#e2231a;margin-right:7px}
.s-case .inner{padding-top:28px;font-size:19px}.s-case h2{font-size:84px;line-height:.9;letter-spacing:-.055em;font-weight:500;margin:0}.s-case .no{display:flex;justify-content:space-between;font-size:15px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}.s-case .desc{font-size:18px;line-height:1.35;margin:0}.s-case .desc b{display:block;font-weight:400;font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:4px}.s-case .shot{padding:18px;gap:10px}
.s-light .light{display:grid;grid-template-columns:1fr 1fr;gap:48px 56px;margin-top:10px}.s-light .light-row{display:grid;grid-template-columns:1fr;gap:14px;align-items:start}.s-light .light-name{font-size:16px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);border-top:1px solid var(--line);padding-top:10px}.s-light .light-imgs{display:flex;gap:12px;height:290px;overflow:hidden}.s-light .light-imgs figure{margin:0;flex:none!important;height:100%}.s-light .light-imgs img{height:100%;width:auto;display:block}.s-decor .decor-lead{font-size:20px;line-height:1.45;margin:0 0 6px;max-width:1300px}.s-decor .light{gap:22px 56px}.s-decor .light-imgs{height:180px}.s-decor .decor-note{font-size:14px;line-height:1.4;margin:6px 0 0;text-transform:none;letter-spacing:0}.s-how .how{display:grid;grid-template-columns:1fr 1fr 1fr;gap:0 48px}
.s-how .how div{border-top:1px solid var(--line);padding:16px 0 30px}
.s-how .how h3{margin:0 0 12px;font-size:16px;font-weight:400;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.s-how .how p{margin:0;font-size:1em;line-height:1.3}
"""
# Ужимаем шрифт слайда, пока содержимое не влезет в 1080.
fit = """
<script>
document.querySelectorAll('.slide .inner').forEach(function(el){
  var fs=parseFloat(getComputedStyle(el).fontSize);
  while(el.scrollHeight>el.clientHeight+1 && fs>14){fs-=0.5; el.style.fontSize=fs+'px';}
});
</script>"""
html = f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(slides)}{fit}</body></html>'
with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "slides.html"
    p.write_text(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                    f"--print-to-pdf={OUT}", p.as_uri()], check=True, capture_output=True)
# Метка версии в ссылке «Скачать PDF», чтобы браузер не отдавал старый файл из кэша.
import time
v = time.strftime("%Y%m%d%H%M")
page = (DECK / "index.html").read_text()
page = re.sub(r'(\./vanya-directors-notes\.pdf)(\?v=\d+)?', r'\1?v=' + v, page)
(DECK / "index.html").write_text(page)
print(OUT, OUT.stat().st_size, "v=" + v)
