"""PDF ТЗ на костюм слайдами 1600×900. Контент из index.html. Ставит ?v= в ссылку на PDF."""
import re,subprocess,time,pathlib
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
d=pathlib.Path(__file__).resolve().parent.parent
idx=d/'index.html'; out=d/'vanya-costume-brief.pdf'
v=time.strftime('%Y%m%d%H%M%S')
s=idx.read_text(); s=re.sub(r'vanya-costume-brief\.pdf\?v=[^"]*',f'vanya-costume-brief.pdf?v={v}',s); idx.write_text(s)
top=lambda r:f'<div class="top"><span>Как Ваня скажет · ТЗ на костюм</span><span>{r}</span></div>'
kicker=re.search(r'<p class="kicker">(.*?)</p>',s,re.S).group(1)
def cols(i): return re.findall(r'<div><h3>(.*?)</h3><p>(.*?)</p></div>',re.search(rf'id="{i}">(.*?)</section>',s,re.S).group(1))
P=[f'<div class="p">{top("ГигаЧат, 2026")}<h1>Костюм. <span>Все герои</span></h1><p class="k">{kicker}</p></div>']
P.append(f'<div class="p">{top("Общее")}<h2>Общее</h2><div class="cols">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in cols('principles'))+'</div></div>')
for m in re.finditer(r'<section class="grid ch" id="([^"]+)">\s*<div class="label">(.*?)<span class="sub">(.*?)</span></div>.*?<img src="\.\./media/sb/([^"]+)".*?<dl class="ch-f">(.*?)</dl>.*?<div class="ch-refs">(.*?)</div></div>',s,re.S):
  cid,name,sub,frame,dl,refs=m.groups()
  ims=re.findall(r'src="\./media/([^"]+)"',refs)
  P.append(f'<div class="p">{top(name)}<div class="cs"><div class="cl"><h2>{name}</h2><div class="sub">{sub}</div><img class="fr" src="../../media/sb/{frame}"><dl>{dl}</dl></div><div class="cr" style="grid-template-rows:{"1fr" if len(ims)<=4 else "1fr 1fr"}">'+''.join(f'<img src="../media/{x}">' for x in ims)+'</div></div></div>')
P.append(f'<div class="p">{top("Практика")}<h2>Практика</h2><div class="cols pr">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in cols('practice'))+'</div></div>')
css="""@page{size:1600px 900px;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#f3f1ea;color:#101010;font-family:Arial,Helvetica,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
a{color:inherit}
.p{width:1600px;height:900px;padding:44px;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.top{display:flex;justify-content:space-between;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#69675f;border-bottom:1px solid rgba(16,16,16,.18);padding-bottom:10px;margin-bottom:24px}
h1{font-size:190px;line-height:.86;letter-spacing:-.07em;font-weight:500;margin:40px 0 0}h1 span{color:#69675f}
h2{font-size:54px;line-height:.9;letter-spacing:-.05em;font-weight:500;margin:0 0 24px}
.k{font-size:40px;line-height:1.1;letter-spacing:-.03em;max-width:1300px;margin:40px 0 0}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:44px 36px}.cols h3{margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:#69675f;font-weight:400;border-top:1px solid rgba(16,16,16,.18);padding-top:12px}.cols p{margin:0;font-size:26px;line-height:1.3;letter-spacing:-.01em}.cols.pr p{font-size:34px;line-height:1.22}
.cs{display:grid;grid-template-columns:560px 1fr;gap:32px;flex:1;min-height:0}
.cl h2{margin:0 0 6px}.cl .sub{font-size:14px;text-transform:uppercase;letter-spacing:.06em;color:#69675f;margin-bottom:16px}
.cl .fr{width:100%;height:250px;object-fit:cover;display:block;margin-bottom:12px}
.cl dl{margin:0;display:grid;gap:8px}.cl dt{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:#69675f}.cl dd{margin:2px 0 0;font-size:17px;line-height:1.35}
.cr{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr;gap:10px;min-height:0}.cr img{width:100%;height:100%;object-fit:cover;object-position:50% 25%;display:block;background:#dcd9d0}
"""
tmp=d/'_pdf/_slides.html'
tmp.write_text(f'<!doctype html><html lang="ru"><meta charset="utf-8"><style>{css}</style>{"".join(P)}</html>')
subprocess.run([CH,"--headless=new","--disable-gpu","--no-pdf-header-footer","--virtual-time-budget=8000",f"--print-to-pdf={out}",tmp.as_uri()],check=True,capture_output=True)
tmp.unlink(); print(out,out.stat().st_size,len(P),'v='+v)
