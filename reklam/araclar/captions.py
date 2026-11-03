import subprocess, html
P=".."
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
lines=[("l1","ece",0.25,["Ne oluyor?!","Nereye gidiyoruz?"]),("l2","kaan",2.25,["Motorlar durdu!","Dışarı bak!"]),
("l3","ece",4.75,["Bu... bir kara delik!"]),("l4","kaan",6.15,["Bizi içine çekiyor!"]),
("l5","anl",9.35,["Onları sadece","sen kurtarabilirsin."]),("l6","anl",12.45,["Geç kalırsan...","sonun böyle olur."]),
("l7","anl",16.0,["Parmağınla","ışık yolu çiz."]),("l8","anl",18.2,["Filoları ve mekikleri,","kaybolmadan","varmaları gereken","yere götür!"]),
("l9","anl",24.3,["Işık Göçü.","Hemen indir!"])]
groups=[]
for lid,who,st,gs in lines:
  d=dur(f"{P}/assets/vo/{lid}.wav"); tot=sum(len(g) for g in gs); t=st
  for i,g in enumerate(gs):
    gd=d*len(g)/tot; end=t+gd if i<len(gs)-1 else st+d+0.2
    groups.append((who,g,round(t,2),round(end,2))); t+=gd
for i in range(len(groups)-1):
  w,g,s0,e0=groups[i]
  if e0>groups[i+1][2]-0.02: groups[i]=(w,g,s0,round(groups[i+1][2]-0.02,2))
out=[]; js=[]
for n,(who,g,s,e) in enumerate(groups):
  chip={"ece":'<span class="cap-who" style="background:#ff4fd8">ECE</span>',"kaan":'<span class="cap-who" style="background:#35e0ff">KAAN</span>'}.get(who,"")
  out.append(f'    <div id="cap-{n}" class="clip cap cap-{who}" data-start="{s}" data-duration="{round(e-s,2)}">{chip}<span class="cap-t">{html.escape(g)}</span></div>')
  js.append(f"[{n},{s},{e}]")
tpl=f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .cap {{ position: absolute; left: 0; right: 0; top: 1170px; text-align: center; overflow: visible; }}
    .cap-t {{ display: inline-block; padding: 10px 26px 14px; border-radius: 18px; background: rgba(5,6,18,.62);
      font: 900 76px/1.12 Inter, sans-serif; color: #fff; letter-spacing: -.01em; text-shadow: 0 4px 14px rgba(0,0,0,.6); }}
    .cap-ece .cap-t {{ color: #ffc2f2; }}
    .cap-kaan .cap-t {{ color: #c4f6ff; }}
    .cap-anl .cap-t {{ color: #fff; }}
    .cap-who {{ display: block; width: max-content; margin: 0 auto 10px; padding: 6px 16px; border-radius: 10px; color: #070914;
      font: 900 30px/1 Inter, sans-serif; letter-spacing: .1em; }}
  </style>
  <div id="root" data-composition-id="altyazi" data-width="1080" data-height="1920">
{chr(10).join(out)}
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const G = [{",".join(js)}];
      for (const [n, s, e] of G) {{
        const el = "#cap-" + n + " .cap-t";
        tl.fromTo(el, {{ opacity: 0, scale: 0.82, y: 16 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.14, ease: "back.out(2.4)" }}, s);
        tl.to(el, {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, e - 0.1);
        tl.set("#cap-" + n, {{ opacity: 0 }}, e);
      }}
      window.__timelines["altyazi"] = tl;
    }})();
  </script>
</template>
'''
open(f"{P}/compositions/altyazi.html","w").write(tpl)
for g in groups: print(g)
