import base64,math
def png(f): return 'images/'+f
LW=None
def b64(f): return 'images/'+f
CBD=(-27.47,153.03)
LTD=png('logo_lt.png');LCT=png('logo_ct.png');LWD=png('logo_wt.png')
def km(a,b):
    R=6371;p1,p2=math.radians(a[0]),math.radians(b[0]);dl=math.radians(b[1]-a[1]);dp=p2-p1
    h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(h))
# id,region,suburb,pc,lat,lon,price,pn,land,build,lp,bp,reg,rmin,rmax,beds,baths,liv,car,pts,note,img
import json,os,shutil
O=json.load(open('projects.json'))
O=[o for o in O if o.get('status','active')=='active']
for o in O:
    o['ll']=tuple(o['ll'])
    o['rent']=tuple(o['rent']) if o.get('rent') else None
REG={'south':'South Brisbane','west':'West Brisbane','north':'North Brisbane','coast':'Sunshine Coast'}
W,H=400,780
def P(lat,lon): return ((lon-152.45)*340,(-26.05-lat)*410)
coast=[(-26.05,153.10),(-26.39,153.09),(-26.65,153.10),(-26.80,153.13),(-26.95,153.12),(-27.08,153.08),(-27.20,153.09),(-27.23,153.12),(-27.30,153.07),(-27.38,153.15),(-27.50,153.30),(-27.62,153.35),(-27.80,153.40),(-27.95,153.43)]
cp=[P(*c) for c in coast]
land='M-110,'+f'{P(-26.05,0)[1]:.0f}'+' L'+' L'.join(f'{x:.0f},{y:.0f}' for x,y in cp)+f' L-110,{P(-27.95,0)[1]:.0f} Z'
river='M'+' L'.join(f'{x:.0f},{y:.0f}' for x,y in [P(-27.50,152.95),P(-27.47,153.03),P(-27.42,153.12),P(-27.38,153.15)])
OVDEF='<defs><pattern id="gr" width="34" height="34" patternUnits="userSpaceOnUse"><path d="M34 0H0V34" fill="none" stroke="#2a2e2c" stroke-width="1"/></pattern><filter id="gl" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
LBL={'burpengary':(256,392,'start',True),'lilywood':(256,424,'start',True),'morayfield':(256,456,'start',True),'durack':(256,612,'start',True),'greenbank':(256,640,'start',True),'parkridge':(256,668,'start',True),'loganreserve':(256,696,'start',True),'yarrabilba':(256,724,'start',True),'ripley':(105,668,'end',False),'gympie':(89,61,'start',False),'terrace':(228,312,'start',False),'fernvale':(85,574,'start',False),'joyner':(191,504,'start',False),'taigum':(256,520,'start',True),'morayfield2':(256,488,'start',True),'heathwood':(256,752,'start',True),'doolandella':(150,640,'end',False),'chambersflat':(168,692,'end',False),'bridgeman':(256,552,'start',True),'boondall':(194,539,'end',False)}
def mapsvg(o=None,overview=False):
    vb=f"0 0 {W} {H}"
    if overview: vb="-10 20 410 750"
    if o:
        x,y=P(*o['ll']);cx_,cy_=P(*CBD)
        top=max(0,min(y,cy_)-90);bot=min(H,max(y,cy_)+90)
        if bot-top<640:
            mid=(top+bot)/2;top=max(0,mid-320);bot=min(H,top+640);top=bot-640
        vb=f"0 {top:.0f} {W} {bot-top:.0f}"
    s=f'<svg viewBox="{vb}" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{"Location map" if o is None else "Map: "+o["suburb"]}">{OVDEF if overview else ""}<rect x="-110" y="-20" width="{W+420}" height="{H+60}" fill="{"#161817" if overview else "#dfe7ec"}"/>{"<rect x=\"-10\" y=\"20\" width=\"410\" height=\"750\" fill=\"url(#gr)\"/>" if overview else ""}<path d="{land}" fill="{"#222625" if overview else "#f6f5f1"}" stroke="{"none" if overview else "#8a8f94"}" stroke-width="1.5"/>{"<path d=\"M"+" L".join(f"{x:.0f},{y:.0f}" for x,y in cp)+"\" fill=\"none\" stroke=\"#E65F19\" stroke-width=\"1.8\" filter=\"url(#gl)\"/>" if overview else ""}<path d="{river}" fill="none" stroke="{"#3a403d" if overview else "#b3c4cf"}" stroke-width="3"/>'
    s+=f'<text x="330" y="360" fill="{"#666B67" if overview else "#7c8a94"}" font-size="13" letter-spacing="3" text-anchor="middle">MORETON BAY</text><text x="335" y="120" fill="{"#666B67" if overview else "#7c8a94"}" font-size="13" letter-spacing="3" text-anchor="middle" >CORAL SEA</text>'
    cx,cy=P(*CBD)
    s+=f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="9" fill="none" stroke="{"#CDD0CA" if overview else "#333"}" stroke-width="1.2"/><circle cx="{cx:.0f}" cy="{cy:.0f}" r="2.5" fill="{"#CDD0CA" if overview else "#333"}"/><text x="{cx+14:.0f}" y="{cy+4:.0f}" fill="{"#CDD0CA" if overview else "#333"}" font-size="14" letter-spacing="1.5">BRISBANE CBD</text>'
    if o:
        x,y=P(*o['ll']);s+=f'<line x1="{cx:.0f}" y1="{cy:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="#E65F19" stroke-width="1.2" stroke-dasharray="4 4" opacity=".8"/>'
    for p in O:
        x,y=P(*p['ll']);on=(o is not None and p is o)
        if overview:
            lx,ly,an,ld=LBL.get(p["id"],(x+14,y+4,"start",False))
            if p["id"] not in LBL and x+14+len(p["suburb"])*9.5>W: lx,an=x-14,"end"
            ln=f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{(lx-5 if an=="start" else lx+5):.0f}" y2="{ly-4:.0f}" stroke="#666B67" stroke-width="1"/>' if ld else ''
            s+=f'<g class="pin" data-t="{p["id"]}" tabindex="0" style="cursor:pointer">{ln}<circle cx="{x:.0f}" cy="{y:.0f}" r="14" fill="transparent"/><circle class="pulse" cx="{x:.0f}" cy="{y:.0f}" r="6" fill="#E65F19"/><circle cx="{x:.0f}" cy="{y:.0f}" r="5.5" fill="#E65F19" stroke="#fff" stroke-width="1.5"/><text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{an}" fill="#fff" font-size="12" letter-spacing="1.2" font-weight="600">{p["suburb"].upper()}</text><text class="pp" x="{lx:.0f}" y="{ly+13:.0f}" text-anchor="{an}" fill="#E65F19" font-size="10.5" letter-spacing=".6">{m(p["price"])}</text></g>'
        elif on:
            s+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="#E65F19" opacity=".18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="6.5" fill="#E65F19"/><text x="{x+12:.0f}" y="{y+4:.0f}" fill="#111" font-size="18" letter-spacing="1.5" font-weight="700">{p["suburb"].upper()}</text>'
        else:
            s+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#9aa3a9"/>'
    s+='</svg>'
    return s
def OVLH():
    h=''
    for r,t in REG.items():
        h+=f'<div class="ovr"><h4>{t}</h4>'
        for p in O:
            if p['reg_']==r: h+=f'<a href="#{p["id"]}"><span>{p["suburb"]}</span><b>{m(p["price"])}</b></a>'
        h+='</div>'
    return h
def m(n): return '${:,.0f}'.format(n)
def plan(o):
    f=(o.get('plan') or None)
    return f'<div class="fp"><img src="{b64(f)}" alt="{o["suburb"]} floor plan, indicative"><em>Indicative only, not to scale.</em></div>' if f else ''
def card(o):
    d=km(CBD,o['ll'])
    rent=''
    if o['rent']:
        a,b=o['rent'];ya=a*52/o['price']*100;yb=b*52/o['price']*100
        rent=f'<div class="rent"><div class="rl">Potential rental income{" (estimate)" if o.get("est") else ""}</div><div class="rg"><div><b>{m(a*52) if a==b else f"{m(a*52)} – {m(b*52)}"}</b><span>per year, gross</span></div><div><b>{f"${a}" if a==b else f"${a} – ${b}"}</b><span>per week</span></div><div><b>{f"{ya:.1f}%" if a==b else f"{ya:.1f}% – {yb:.1f}%"}</b><span>gross yield</span></div></div></div>'
    else:
        rent='<div class="rent"><div class="rl">Potential rental income</div><div class="rg"><div><b>Appraisal on request</b><span>ask your agent</span></div></div></div>'
    rent=rent[:-6]+f'<img class="rlogo" src="{LWD}" alt="One Agency Nexus"></div>'
    chips=f'<span>{o["b"]} bed</span><span>{o["ba"]} bath</span>'+(f'<span>{o["l"]} living</span>' if o['l'] else '')+f'<span>{o["c"]} car</span>'
    def tx(v,u=''): return f'{v}{u}'
    land_c=(f'{o["land"]} m²' if o.get('land') else o.get('land_txt','On request'))
    build_c=(f'{o["build"]} m²' if o.get('build') else 'On request')
    lp_c=(m(o['lp']) if o.get('lp') else o.get('lp_txt','On request'))
    bp_c=(m(o['bp']) if o.get('bp') else 'On request')
    yl=((f'{o["rent"][0]*52/o["price"]*100:.1f}%' if o['rent'][0]==o['rent'][1] else f'{o["rent"][0]*52/o["price"]*100:.1f}–{o["rent"][1]*52/o["price"]*100:.1f}%') if o['rent'] else 'On request')
    cells=[('Land size',land_c),('House size',build_c),('Land registration',o['title']),('Land price',lp_c),('House price',bp_c),('Est. gross yield',yl)]
    cellh=''.join(f'<div class="c"><span>{a}</span><b>{b}</b></div>' for a,b in cells)
    main=f'<div class="main"><img class="zm" src="{b64(o["img"])}" alt="{o["suburb"]} home, illustrative" loading="lazy"></div>' if o['img'] else f'<div class="noimg"><span>{o["suburb"]}</span></div>'
    pf=(o.get('plan') or None)
    planfig=(f'<figure class="pf"><img class="zm" src="{b64(pf)}" alt="{o["suburb"]} floor plan, indicative" loading="lazy"><figcaption>Floor plan · indicative</figcaption></figure>' if pf else '<figure class="pf ph0"><div>Floor plan<br>on request</div><figcaption>Floor plan</figcaption></figure>')
    ph=f'<div class="stack">{main}<div class="subs"><figure class="if"><img class="zm" src="{b64(o.get("interior") or "i_"+o["id"]+".jpg")}" alt="{o["suburb"]} interior, illustrative" loading="lazy"><figcaption>Interior · illustrative</figcaption></figure>{planfig}</div></div>'
    tag='Dual-key · ' if o.get('dual') else ''
    gm=f'https://www.google.com/maps/search/?api=1&query={o["suburb"].replace(" ","+")}+QLD+{o["pc"]}'
    note=f'<p class="note">{o["note"]}</p>' if o.get('note') else ''
    pl=''
    tabs=('<div class="tabs"><button class="on" data-t="m">Map</button><button data-t="p">Floor plan</button></div>' if pl else '<div class="tabs"><button class="on" data-t="m">Map</button></div>')
    return f'''<article class="card" id="{o["id"]}" data-r="{o["reg_"]}"><div class="ph">{ph}{"<div class=\"badge\">Fixed price · Full turnkey</div>" if o.get("lp") else ""}</div>
<div class="body"><div class="top"><div class="pr"><b>{m(o["price"])}</b><span>{tag}House &amp; Land</span></div><div><div class="reg">{REG[o["reg_"]]}</div><h3>{o["suburb"]}<small>QLD {o["pc"]}</small></h3></div></div>
<div class="chips">{chips}</div><div class="grid">{cellh}</div><ul>{"".join(f"<li>{p}</li>" for p in o["pts"])}</ul>{note}</div>
<div class="side"><div class="pn on" data-p="m"><div class="mw">{mapsvg(o)}{("<span class=\"dv\">"+o["dev"]+"</span>") if o.get("dev") else ""}</div><div class="mcap"><span>About {d:.0f} km from Brisbane CBD (straight line)</span><a href="{gm}" target="_blank" rel="noopener">Open in Google Maps ↗</a></div></div>{pl.replace('class="fp"','class="pn fp" data-p="p"') if pl else ""}</div>
{rent}</article>'''
cards=''.join(card(o) for o in O)
CSS=open('style.css').read()
TEAM=[('Maiya Kim', 'Principal', '0406 839 130', 'maiya_kim'), ('Mustafa Aydemir', 'Real Estate Agent', '0403 577 928', 'mustafa_aydemir'), ('Elena Dzu', 'Real Estate Agent', '0434 313 462', 'elena_dzu'), ('Amritpal Singh', 'Real Estate Agent', '0450 467 007', 'amritpal_singh'), ('Zhanna Kotelnikova', 'Real Estate Agent', '0432 353 992', 'zhanna_kotelnikova'), ('Bill Filipou', 'Business Development Manager', '0413 909 997', 'bill_filipou'), ('Anastasia Ziyatova', 'Real Estate Agent', '0430 048 511', 'anastasia_ziyatova'), ('Askat Djubaev', 'Project Manager', '0426 419 973', 'askat_djubaev'), ('Jasmine Jiang', 'Consultant', '0406 857 993', 'jasmine_jiang')]
tm=''.join(f'<div class="tm"><img src="{b64("t_"+f+".jpg")}" alt="{n}"><b>{n}</b><span>{r}</span><em>{p}</em></div>' for n,r,p,f in TEAM)
ABOUT='<div class="ovab"><div class="k">Who we are</div><h3>House &amp; land, handled end to end.</h3><p>One Agency Nexus is a Brisbane team specialising in house and land packages across South, West and North Brisbane and the Sunshine Coast.</p><p>We help clients choose the right package, read the market and run the numbers. Together we map out the next steps, from first enquiry through to settlement and beyond.</p><p>We are proud to guide first home buyers as well as investors, with clear advice at every stage.</p><ul><li>Package selection and comparison</li><li>Market and rental analysis</li><li>A clear plan for your next steps</li><li>First home buyer support</li></ul></div>'
OVL=OVLH()
html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>One Agency Nexus — House &amp; Land Packages</title><style>{CSS}</style></head><body>
<header class="hd"><div class="logo"><a href="#"><img class="lg" src="{LTD}" alt="One Agency Nexus"></a><em class="tl">Consider it Handled.</em></div><nav><a href="#projects">Projects</a><a href="#map">Map</a><a href="#about">About</a><a href="#team">Team</a><a href="#contact">Contact</a></nav><a class="btn" href="#contact">Free consultation</a></header>
<section class="hero"><img class="hl" src="{LCT}" alt="One Agency Nexus"><div class="k">House &amp; Land · Queensland</div><h1>New homes<br>with land</h1><div class="slg">Consider it Handled.</div><p>Turnkey house and land packages across South Brisbane, North Brisbane and the Sunshine Coast, with estimated rental income for every package.</p><div class="cta"><a class="btn" href="#projects">View packages</a><a class="btn ghost" href="#contact">Get in touch</a></div>
<div class="stats"><div><b>{len(O)}</b><span>Packages</span></div><div><b>{m(min(o["price"] for o in O))}</b><span>Prices from</span></div><div><b>QLD</b><span>Licensed</span></div></div></section>
<section class="ov" id="map"><div class="sec"><div class="k">Locations</div><h2>All packages on one map</h2><p class="sub">Tap a suburb to jump to its package. Each package also has its own map below.</p></div><div class="ovwrap"><div class="ovleft"><div class="ovbox">{mapsvg(None,True)}</div></div><div class="ovl">{ABOUT}{OVL}</div></div></section>
<section id="projects"><div class="sec"><div class="k">Projects</div><h2>Available packages</h2><div class="filters"><button class="on" data-f="all">All</button><button data-f="south">South Brisbane</button><button data-f="west">West Brisbane</button><button data-f="north">North Brisbane</button><button data-f="coast">Sunshine Coast</button></div></div><div class="list">{cards}</div></section>
<section id="about"><div class="sec"><div class="k">About us</div><h2>Local knowledge.<br>More possibilities.</h2><div class="ab"><p>One Agency Nexus is a Brisbane real estate team working across selling, buying, new homes and house and land, property marketing, and land subdivision. One connected team looks after sales, projects and client support, backed by finance, legal, tax, planning and building specialists.</p><p>We are licensed in Queensland, Western Australia, Victoria and South Australia, speak multiple languages, and support local and international clients. We negotiate for a living. Challenge us.</p></div></div></section>
<section id="team"><div class="sec"><img class="sl" src="{LWD}" alt="One Agency Nexus"><div class="k">Our team</div><h2>Meet the people</h2><div class="tg">{tm}</div></div></section>
<section class="ct" id="contact"><div class="sec"><img class="sl" src="{LWD}" alt="One Agency Nexus"><div class="k">Contact</div><h2>Talk to our team</h2><p class="sub">Maiya Kim, Principal<br>0406 839 130 · admin@oneagencynexus.com.au<br>oneagencynexus.com.au</p><div class="cta"><a class="btn" href="mailto:admin@oneagencynexus.com.au">Free consultation</a><a class="btn wa" href="https://wa.me/61406839130?text=Hi%20Maiya%2C%20I%27d%20like%20a%20free%20consultation%20about%20house%20%26%20land%20packages." target="_blank" rel="noopener">WhatsApp</a></div></div></section>
<footer><img class="sl" src="{LWD}" alt="One Agency Nexus"><div class="fs">Consider it Handled.</div><div class="k">Disclaimer</div><p>All prices in AUD. Rental figures are gross estimates before costs, not guaranteed. Information is general in nature, indicative, subject to availability and may change without notice. It is not financial, legal or tax advice; consult an independent professional before making an investment decision. Images are AI generated for illustrative purposes. Maps are schematic.</p><p class="cp">© One Agency Nexus</p></footer>
<div id="hz"><img alt=""></div>
<script>
(function(){{const hz=document.getElementById('hz'),hi=hz.querySelector('img');
function place(e){{const vw=innerWidth,vh=innerHeight;const w=hz.offsetWidth,h=hz.offsetHeight;let x=e.clientX+28,y=e.clientY-h/2;if(x+w>vw-12)x=e.clientX-w-28;if(x<12)x=12;y=Math.max(12,Math.min(y,vh-h-12));hz.style.left=x+'px';hz.style.top=y+'px'}}
document.querySelectorAll('img.zm').forEach(i=>{{i.addEventListener('mouseenter',e=>{{hi.src=i.src;const plan=i.closest('.pf');const mh=Math.round(innerHeight*.86);hi.style.maxHeight=mh+'px';hi.style.maxWidth=Math.round(innerWidth*(plan?.4:.6))+'px';hi.style.width=(plan?Math.min(innerWidth*.4,mh*.62):Math.min(innerWidth*.6,mh*1.4))+'px';hi.style.height='auto';hz.classList.add('on');place(e)}});i.addEventListener('mousemove',place);i.addEventListener('mouseleave',()=>hz.classList.remove('on'))}})}})();
</script>
<div class="lb" id="lb"><img alt=""></div>
<script>
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}}),{{threshold:.08}});document.querySelectorAll('.card').forEach(c=>{{c.classList.add('rv');io.observe(c)}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')document.getElementById('lb').classList.remove('on')}});
document.querySelectorAll('img.zm').forEach(i=>i.onclick=()=>{{const l=document.getElementById('lb');l.querySelector('img').src=i.src;l.classList.add('on')}});document.getElementById('lb').onclick=()=>document.getElementById('lb').classList.remove('on');
document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.filters button').forEach(x=>x.classList.toggle('on',x===b));const f=b.dataset.f;document.querySelectorAll('.card').forEach(c=>c.style.display=(f==='all'||c.dataset.r===f)?'':'none')}});
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{const c=b.closest('.card');c.querySelectorAll('.tabs button').forEach(x=>x.classList.toggle('on',x===b));c.querySelectorAll('.pn').forEach(p=>p.classList.toggle('on',p.dataset.p===b.dataset.t))}});
document.querySelectorAll('.pin').forEach(p=>{{const go=()=>{{document.querySelectorAll('.filters button')[0].click();const e=document.getElementById(p.dataset.t);if(e)e.scrollIntoView({{behavior:'smooth',block:'start'}})}};p.onclick=go;p.onkeydown=e=>{{if(e.key==='Enter')go()}}}});
</script></body></html>'''
os.makedirs('dist',exist_ok=True)
open('dist/index.html','w').write(html)
shutil.rmtree('dist/images',ignore_errors=True);shutil.copytree('images','dist/images')
open('dist/.nojekyll','w').write('')
print('built',len(O),'packages,',len(html),'bytes')
