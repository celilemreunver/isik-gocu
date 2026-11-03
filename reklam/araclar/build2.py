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
L=[("l1","ece",0.2,[("Ne oluyor?!",0,1.13),("Kaan, nereye gidiyoruz?!",1.39,3.05)]),
   ("l2","kaan",3.9,[("Motorlar cevap vermiyor!",0.44,1.61),("Ece... dışarı bak!",2.42,3.40)]),
   ("l3","ece",7.9,[("Bu...",0.29,0.95),("bu bir kara delik!",1.34,3.29)]),
   ("l4","kaan",11.7,[("Bizi içine çekiyor!",0,1.6)]),
   ("l5","anl",14.7,[("Onları kurtarabilecek",0,1.47),("tek kişi...",1.69,2.51),("sensin.",2.97,3.81)]),
   ("l6","anl",19.4,[("Geç kalırsan...",0.26,1.91),("sonun böyle olur.",2.21,4.62)]),
   ("l7","anl",25.0,[("Parmağınla ışık yolunu çiz!",0,1.77),("Filoları ve uzay mekiklerini,",2.23,3.82),("kaybolmadan evlerine ulaştır!",4.04,5.81)]),
   ("l8","anl",31.6,[("Kara deliklere dikkat et...",0.28,1.40),("ve gizli takımyıldızları keşfet!",1.71,3.35)])]
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
    chip={"ece":'<span class="cap-who" style="background:#ff4fd8">ECE</span>',"kaan":'<span class="cap-who" style="background:#35e0ff">KAAN</span>'}.get(who,"")
    out.append(f'    <div id="cap-{n}" class="clip cap cap-{who}" data-start="{s}" data-duration="{round(e-s,2)}">{chip}<span class="cap-t">{html.escape(g)}</span></div>')
    js.append(f"[{n},{s},{e}]"); print(f"  {s:6.2f}-{e:6.2f} {who:4} {g}")
c=open(f"{P}/compositions/altyazi.html").read()
c=re.sub(r'(<div id="root" data-composition-id="altyazi"[^>]*>\n).*?(\n  </div>\n  <script>)', lambda m: m.group(1)+"\n".join(out)+m.group(2), c, flags=re.S)
c=re.sub(r"const G = \[.*?\];", "const G = ["+",".join(js)+"];", c)
open(f"{P}/compositions/altyazi.html","w").write(c)

s=open(f"{P}/index.html").read()
s=re.sub(r'      <audio id="vo-l\d".*?</audio>\n', "", s)
s=s.replace("    </div>\n    <script>", "\n".join(audio)+"\n    </div>\n    <script>",1)
rep={'id="kokpit"':("0","6.8"),'id="pencere"':("6.8","7.6"),'id="logo"':("14.4","4.8"),'id="rus"':("19.2","5.4"),'id="son"':("36","3")}
for k,(a,b) in rep.items():
    s=re.sub(rf'({k}[^>]*?data-start=")[\d.]+(" data-duration=")[\d.]+', rf'\g<1>{a}\g<2>{b}', s, flags=re.S)
s=re.sub(r'(id="oyun-video"[^>]*?data-start=")[\d.]+(" data-duration=")[\d.]+', r'\g<1>24.6\g<2>11.4', s, flags=re.S)
s=re.sub(r'(id="oyun-ses"[^>]*?data-start=")[\d.]+(" data-duration=")[\d.]+', r'\g<1>24.6\g<2>11.4', s, flags=re.S)
s=re.sub(r'(id="root" data-composition-id="main" data-start="0" data-duration=")[\d.]+', r'\g<1>39', s)
s=re.sub(r'(id="altyazi"[^>]*?data-duration=")[\d.]+', r'\g<1>39', s, flags=re.S)
open(f"{P}/index.html","w").write(s)
