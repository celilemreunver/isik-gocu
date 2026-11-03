import subprocess, re, html
P="/home/user/isik-gocu-reklam"
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]).decode())
def speech_segs(f, d):
    o=subprocess.run(["ffmpeg","-nostdin","-hide_banner","-i",f,"-af","silencedetect=noise=-35dB:d=0.22","-f","null","-"],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: ([\d.]+)",o)]; en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",o)]
    segs=[]; cur=0.0
    for a,b in zip(st,en+[d]*(len(st)-len(en))):
        if a-cur>0.05: segs.append([cur,a])
        cur=b
    if d-cur>0.05: segs.append([cur,d])
    return segs
L=[("v1","mert",0.12,[("Ne oluyor?!",0,0.43),("Nereye gidiyoruz?!",0.71,1.40)]),
   ("v2","kaan",1.7,[("Motorlar durdu!",0,0.76),("Mert... dışarı bak!",1.12,2.12)]),
   ("v3","mert",4.15,[("Kara delik!",0,0.77),("Bizi içine çekiyor!",1.10,2.19)]),
   ("v5","anl",7.2,[("Onları kurtarabilecek",0,1.37),("tek kişi...",1.68,2.49),("sensin.",2.96,3.80)]),
   ("v7","anl",11.75,[("Parmağınla ışık yolunu çiz!",0,1.76),("Filoları ve uzay mekiklerini,",2.23,3.80),("kaybolmadan evlerine ulaştır!",4.03,5.78)]),
   ("v8","anl",18.25,[("Kara deliklere dikkat et...",0.28,1.40),("ve gizli takımyıldızları keşfet!",1.71,3.34)]),
   ("v9","anl",22.25,[("Işık Göçü.",0,0.78),("Hemen indir!",1.21,1.82)])]
groups=[]; audio=[]
for lid,who,st,gs in L:
    f=f"{P}/assets/vo/{lid}.wav"; d=dur(f)
    audio.append(f'      <audio id="vo-{lid}" src="assets/vo/{lid}.wav" data-start="{st}" data-duration="{d:.2f}" data-track-index="3" data-volume="1"></audio>')
    spans=[(st+a,st+b) for _,a,b in gs]; gs=[g for g,_,_ in gs]
    for i,(g,(a,b)) in enumerate(zip(gs,spans)):
        nxt = spans[i+1][0] if i+1<len(spans) else b+0.35
        groups.append((who,g,round(a-0.05,2),round(max(b+0.15, min(nxt, b+0.4)) if i+1<len(spans) else nxt,2)))
for i in range(len(groups)-1):
    w,g,a,b=groups[i]
    if b>groups[i+1][2]-0.02: groups[i]=(w,g,a,round(groups[i+1][2]-0.02,2))
out=[];js=[]
for n,(who,g,s,e) in enumerate(groups):
    chip={"mert":'<span class="cap-who" style="background:#ffb03a">MERT</span>',"kaan":'<span class="cap-who" style="background:#35e0ff">KAAN</span>'}.get(who,"")
    out.append(f'    <div id="cap-{n}" class="clip cap cap-{who}" data-start="{s}" data-duration="{round(e-s,2)}">{chip}<span class="cap-t">{html.escape(g)}</span></div>')
    js.append(f"[{n},{s},{e}]"); print(f"  {s:6.2f}-{e:6.2f} {who:4} {g}")
c=open(f"{P}/compositions/altyazi.html").read()
c=re.sub(r'(<div id="root" data-composition-id="altyazi"[^>]*>\n).*?(\n  </div>\n  <script>)', lambda m: m.group(1)+"\n".join(out)+m.group(2), c, flags=re.S)
c=re.sub(r"const G = \[.*?\];", "const G = ["+",".join(js)+"];", c)
open(f"{P}/compositions/altyazi.html","w").write(c)

s=open(f"{P}/index.html").read()
s=re.sub(r'      <audio id="vo-[lv]\d".*?</audio>\n', '', s)
s=s.replace("    </div>\n    <script>", "\n".join(audio)+"\n    </div>\n    <script>",1)
rep={'id="kokpit"':("0","3.9"),'id="pencere"':("3.9","3.1"),'id="logo"':("7","4.5"),'id="son"':("22.1","3")}
for k,(a,b) in rep.items():
    s=re.sub(rf'({k}[^>]*?data-start=")[\d.]+(" data-duration=")[\d.]+', rf'\g<1>{a}\g<2>{b}', s, flags=re.S)
s=re.sub(r'(id="oyun-video"[^>]*?data-start=")[\d.]+(" data-duration=")[\d.]+', r'\g<1>11.5\g<2>10.6', s, flags=re.S)
s=re.sub(r'(id="oyun-ses"[^>]*?data-start=")[\d.]+(" data-duration=")[\d.]+', r'\g<1>11.5\g<2>10.6', s, flags=re.S)
s=re.sub(r'(id="root" data-composition-id="main" data-start="0" data-duration=")[\d.]+', r'\g<1>25.1', s)
s=re.sub(r'(id="altyazi"[^>]*?data-duration=")[\d.]+', r'\g<1>25.1', s, flags=re.S)
open(f"{P}/index.html","w").write(s)
