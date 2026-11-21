"""PDF брифа слайдами 1600×900 (как у деки). Контент берётся из index.html. Ставит ?v= в ссылку на PDF."""
import re,subprocess,time,pathlib,html as H
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
d=pathlib.Path(__file__).resolve().parent.parent
idx=d/'index.html'; out=d/'vanya-stylist-brief.pdf'
v=time.strftime('%Y%m%d%H%M%S')
s=idx.read_text(); s=re.sub(r'vanya-stylist-brief\.pdf\?v=[^"]*',f'vanya-stylist-brief.pdf?v={v}',s); idx.write_text(s)
def sec(i):
  m=re.search(rf'<section class="grid" id="{i}">(.*?)</section>',s,re.S); return m.group(1) if m else ''
def rows(block):
  out=[]
  for rb in re.findall(r'<div class="light-row">(.*?<div class="light-imgs">.*?)</div></div>',block,re.S):
    nm=re.search(r'<div class="light-name">(.*?)</div>',rb,re.S); nm=nm.group(1) if nm else ''
    t=re.sub(r'<p class="decor-note">.*?</p>','',nm,flags=re.S).strip()
    n=re.search(r'<p class="decor-note">(.*?)</p>',nm,re.S); n=n.group(1) if n else ''
    out.append((t,n,rb))
  return out
def imgs(fr): return re.findall(r'src="\./media/([^"]+)"',fr)
def gslide(sec_title,r,title):
  t,n,f=r; ims=imgs(f); h=t or title
  return f'<div class="p">{top(sec_title)}<div class="gh"><h2>{h}</h2><span>{n}</span></div><div class="gg" style="grid-template-columns:repeat({len(ims)},1fr)">'+''.join(f'<img src="../media/{x}">' for x in ims)+'</div></div>'
top=lambda r:f'<div class="top"><span>Как Ваня скажет · Бриф для стилистов</span><span>{r}</span></div>'
meta=re.search(r'<dl class="meta">.*?</dl>',s,re.S).group(0)
copy=re.search(r'<div class="copy">(.*?)</div>',s,re.S).group(1)
kicker=re.search(r'<p class="kicker">(.*?)</p>',s,re.S).group(1)
pr=re.findall(r'<div><h3>(.*?)</h3><p>(.*?)</p></div>',sec('principles'))
look=rows(sec('look')); hair=sec('hair'); hr=rows(hair)
lead=re.search(r'<p class="decor-lead">(.*?)</p>',hair,re.S); lead=lead.group(1) if lead else ''
hl=re.search(r'<ul class="st-list"[^>]*>(.*?)</ul>',hair,re.S); hl=hl.group(1) if hl else ''
sc=[]
for b in re.findall(r'<div class="st-scene">(.*?)</div></div>',sec('scenes'),re.S):
  im=re.search(r'src="\.\./media/sb/([^"]+)"',b).group(1)
  h=re.search(r'<h3>(.*?)</h3>',b,re.S).group(1)
  pp=''.join(f'<p>{x}</p>' for x in re.findall(r'<p>(.*?)</p>',b,re.S))
  u=re.search(r'<ul>(.*?)</ul>',b,re.S); u=f'<ul>{u.group(1)}</ul>' if u else ''
  sc.append((im,h,pp,u))
pc=re.findall(r'<div><h3>(.*?)</h3><p>(.*?)</p></div>',sec('practice'))
P=[]
P.append(f'<div class="p">{top("ГигаЧат, 2026")}<h1>Ваня. <span>Образ</span></h1><p class="k">{kicker}</p><div class="two"><div class="meta">{meta}</div><div class="cp">{copy}</div></div></div>')
if pr: P.append(f'<div class="p">{top("Принципы")}<h2>Принципы</h2><div class="cols">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in pr)+'</div></div>')
for r in look: P.append(gslide('Референсы образа',r,'Образ'))
for a in range(0,len(sc),2):
  P.append(f'<div class="p">{top("Сцены")}<h2>Сцены</h2><div class="sc2">'+''.join(f'<div><img src="../../media/sb/{im}"><h3>{h}</h3>{pp}{u}</div>' for im,h,pp,u in sc[a:a+2])+'</div></div>')
if lead or hl: P.append(f'<div class="p">{top("Волосы")}<h2>Волосы</h2><p class="lead big">{lead}</p><ul class="hl">{hl}</ul></div>')
for r in hr: P.append(gslide('Волосы',r,'Волосы'))
P.append(f'<div class="p">{top("Практика")}<h2>Практика</h2><div class="cols pr">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in pc)+'</div></div>')
css="""@page{size:1600px 900px;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#f3f1ea;color:#101010;font-family:Arial,Helvetica,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.p{width:1600px;height:900px;padding:44px;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.top{display:flex;justify-content:space-between;font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#69675f;border-bottom:1px solid rgba(16,16,16,.18);padding-bottom:10px;margin-bottom:24px}
h1{font-size:190px;line-height:.86;letter-spacing:-.07em;font-weight:500;margin:40px 0 0}h1 span{color:#69675f}
h2{font-size:56px;line-height:.9;letter-spacing:-.05em;font-weight:500;margin:0 0 28px}
.k{font-size:34px;line-height:1.08;letter-spacing:-.03em;max-width:1200px;margin:28px 0 0}
.two{display:grid;grid-template-columns:360px 1fr;gap:44px;margin-top:auto;border-top:1px solid rgba(16,16,16,.18);padding-top:20px}
dl{margin:0;display:grid;gap:8px}dt{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:#69675f}dd{margin:2px 0 0;font-size:16px}
.cp{font-size:24px;line-height:1.2;letter-spacing:-.015em}.cp p{margin:0 0 .8em}mark{background:#e9ff00}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 36px}.cols h3{margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:#69675f;font-weight:400;border-top:1px solid rgba(16,16,16,.18);padding-top:12px}.cols p{margin:0;font-size:30px;line-height:1.28;letter-spacing:-.015em}.cols{flex:1;align-content:start;row-gap:44px}
.sc2{display:grid;grid-template-columns:1fr 1fr;gap:36px}.sc2 img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;margin-bottom:16px}.sc2 h3{margin:0 0 8px;font-size:34px;font-weight:500;letter-spacing:-.03em}.sc2 p{margin:0 0 12px;font-size:27px;line-height:1.35}.sc2 ul{margin:0;padding-left:24px;font-size:27px;line-height:1.4}
.cols.pr p{font-size:38px;line-height:1.22}
.rows{display:grid;gap:26px}.r{display:grid;grid-template-columns:230px 1fr;gap:24px}.rn{border-top:1px solid rgba(16,16,16,.18);padding-top:10px}.rn b{display:block;font-size:13px;text-transform:uppercase;letter-spacing:.06em;font-weight:400;color:#69675f;margin-bottom:8px}.rn span{font-size:16px;line-height:1.35}
.gh{display:flex;align-items:baseline;gap:28px;margin-bottom:22px}.gh h2{margin:0}.gh span{font-size:22px;color:#69675f}.gg{display:grid;gap:12px;flex:1;min-height:0}.gg img{width:100%;height:100%;object-fit:cover;object-position:50% 20%;display:block;background:#dcd9d0}
.ri{display:flex;gap:10px;overflow:hidden}.ri img{width:auto;display:block;background:#dcd9d0}
.sc{display:grid;grid-template-columns:1fr 1fr;gap:26px 36px;flex:1}.sc>div{display:grid;grid-template-columns:520px 1fr;gap:20px}.sc img{width:520px;height:292px;object-fit:cover;display:block}
.sc h3{margin:0 0 8px;font-size:30px;font-weight:500;letter-spacing:-.02em}.sc p{margin:0 0 10px;font-size:18px;line-height:1.35}.sc ul,.hl{margin:0;padding-left:20px;font-size:18px;line-height:1.4}
.lead{font-size:20px;line-height:1.4;max-width:1100px;margin:0 0 22px}.lead.big{font-size:40px;line-height:1.18;letter-spacing:-.025em;max-width:1400px}.hl{font-size:30px;line-height:1.35;margin-top:44px;max-width:1400px}.hl li{margin-bottom:8px}
"""
tmp=d/'_pdf/_slides.html'
tmp.write_text(f'<!doctype html><html lang="ru"><meta charset="utf-8"><style>{css}</style>{"".join(P)}</html>')
subprocess.run([CH,"--headless=new","--disable-gpu","--no-pdf-header-footer","--virtual-time-budget=8000",f"--print-to-pdf={out}",tmp.as_uri()],check=True,capture_output=True)
tmp.unlink(); print(out,out.stat().st_size,len(P),'v='+v)
