"""PDF брифа слайдами 1600×900 (как у деки). Контент берётся из index.html. Ставит ?v= в ссылку на PDF."""
import re,subprocess,time,pathlib,html as H
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
d=pathlib.Path(__file__).resolve().parent.parent
idx=d/'index.html'; out=d/'vanya-stylist-brief.pdf'
v=time.strftime('%Y%m%d%H%M%S')
s=idx.read_text(); s=re.sub(r'vanya-stylist-brief\.pdf\?v=[^"]*',f'vanya-stylist-brief.pdf?v={v}',s); idx.write_text(s)
def sec(i): return re.search(rf'<section class="grid" id="{i}">(.*?)</section>',s,re.S).group(1)
def rows(block):
  return re.findall(r'<div class="light-row"><div class="light-name">(.*?)<p class="decor-note">(.*?)</p></div><div class="light-imgs">(.*?)</div></div>',block,re.S)
def imgs(fr): return re.findall(r'src="\./media/([^"]+)"',fr)
def rowhtml(r,h=300):
  t,n,f=r; return f'<div class="r"><div class="rn"><b>{t}</b><span>{n}</span></div><div class="ri">'+''.join(f'<img src="../media/{x}" style="height:{h}px">' for x in imgs(f))+'</div></div>'
top=lambda r:f'<div class="top"><span>Как Ваня скажет · Бриф для стилистов</span><span>{r}</span></div>'
meta=re.search(r'<dl class="meta">.*?</dl>',s,re.S).group(0)
copy=re.search(r'<div class="copy">(.*?)</div>',s,re.S).group(1)
kicker=re.search(r'<p class="kicker">(.*?)</p>',s,re.S).group(1)
pr=re.findall(r'<div><h3>(.*?)</h3><p>(.*?)</p></div>',sec('principles'))
look=rows(sec('look')); hair=sec('hair'); hr=rows(hair)
lead=re.search(r'<p class="decor-lead">(.*?)</p>',hair,re.S).group(1)
hl=re.search(r'<ul class="st-list"[^>]*>(.*?)</ul>',hair,re.S).group(1)
sc=re.findall(r'<div class="st-scene"><figure><img src="\.\./media/sb/([^"]+)"[^>]*></figure><div><h3>(.*?)</h3><p>(.*?)</p><ul>(.*?)</ul></div></div>',sec('scenes'))
pc=re.findall(r'<div><h3>(.*?)</h3><p>(.*?)</p></div>',sec('practice'))
P=[]
P.append(f'<div class="p">{top("ГигаЧат, 2026")}<h1>Ваня. <span>Образ</span></h1><p class="k">{kicker}</p><div class="two"><div class="meta">{meta}</div><div class="cp">{copy}</div></div></div>')
P.append(f'<div class="p">{top("Принципы")}<h2>Принципы</h2><div class="cols">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in pr)+'</div></div>')
for i in range(0,len(look),2):
  P.append(f'<div class="p">{top("Референсы образа")}<h2>Референсы образа</h2><div class="rows">'+''.join(rowhtml(r,290) for r in look[i:i+2])+'</div></div>')
P.append(f'<div class="p">{top("Сцены")}<h2>Сцены</h2><div class="sc">'+''.join(f'<div><img src="../../media/sb/{im}"><div><h3>{t}</h3><p>{p}</p><ul>{u}</ul></div></div>' for im,t,p,u in sc)+'</div></div>')
P.append(f'<div class="p">{top("Волосы")}<h2>Волосы</h2><p class="lead">{lead}</p><div class="rows">'+''.join(rowhtml(r,215) for r in hr[:2])+'</div></div>')
P.append(f'<div class="p">{top("Волосы")}<h2>Волосы по сценам</h2><div class="rows">'+rowhtml(hr[2],300)+f'</div><ul class="hl">{hl}</ul></div>')
P.append(f'<div class="p">{top("Практика")}<h2>Практика</h2><div class="cols">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in pc)+'</div></div>')
css="""@page{size:1600px 900px;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#f3f1ea;color:#101010;font-family:Arial,Helvetica,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.p{width:1600px;height:900px;padding:44px;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.top{display:flex;justify-content:space-between;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#69675f;border-bottom:1px solid rgba(16,16,16,.18);padding-bottom:10px;margin-bottom:24px}
h1{font-size:190px;line-height:.86;letter-spacing:-.07em;font-weight:500;margin:40px 0 0}h1 span{color:#69675f}
h2{font-size:56px;line-height:.9;letter-spacing:-.05em;font-weight:500;margin:0 0 28px}
.k{font-size:34px;line-height:1.08;letter-spacing:-.03em;max-width:1200px;margin:28px 0 0}
.two{display:grid;grid-template-columns:360px 1fr;gap:44px;margin-top:auto;border-top:1px solid rgba(16,16,16,.18);padding-top:20px}
dl{margin:0;display:grid;gap:8px}dt{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#69675f}dd{margin:2px 0 0;font-size:16px}
.cp{font-size:24px;line-height:1.2;letter-spacing:-.015em}.cp p{margin:0 0 .8em}mark{background:#e9ff00}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 36px}.cols h3{margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:#69675f;font-weight:400;border-top:1px solid rgba(16,16,16,.18);padding-top:12px}.cols p{margin:0;font-size:21px;line-height:1.35}
.rows{display:grid;gap:26px}.r{display:grid;grid-template-columns:230px 1fr;gap:24px}.rn{border-top:1px solid rgba(16,16,16,.18);padding-top:10px}.rn b{display:block;font-size:13px;text-transform:uppercase;letter-spacing:.06em;font-weight:400;color:#69675f;margin-bottom:8px}.rn span{font-size:16px;line-height:1.35}
.ri{display:flex;gap:10px;overflow:hidden}.ri img{width:auto;display:block;background:#dcd9d0}
.sc{display:grid;grid-template-columns:1fr 1fr;gap:22px 36px}.sc>div{display:grid;grid-template-columns:400px 1fr;gap:18px}.sc img{width:400px;height:225px;object-fit:cover;display:block}
.sc h3{margin:0 0 6px;font-size:24px;font-weight:500}.sc p{margin:0 0 8px;font-size:15px;line-height:1.35}.sc ul,.hl{margin:0;padding-left:18px;font-size:15px;line-height:1.4}
.lead{font-size:20px;line-height:1.4;max-width:1100px;margin:0 0 22px}.hl{font-size:19px;margin-top:30px;max-width:1100px}.hl li{margin-bottom:8px}
"""
tmp=d/'_pdf/_slides.html'
tmp.write_text(f'<!doctype html><html lang="ru"><meta charset="utf-8"><style>{css}</style>{"".join(P)}</html>')
subprocess.run([CH,"--headless=new","--disable-gpu","--no-pdf-header-footer","--virtual-time-budget=8000",f"--print-to-pdf={out}",tmp.as_uri()],check=True,capture_output=True)
tmp.unlink(); print(out,out.stat().st_size,len(P),'v='+v)
