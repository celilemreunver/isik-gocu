import sys, subprocess, numpy as np
def load(f, extra=""):
    af = "highpass=f=4000,highpass=f=4000" + extra
    raw = subprocess.run(["ffmpeg","-nostdin","-v","error","-i",f,"-af","pan=mono|c0=c0,"+af,"-ar","44100","-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32)
for f in sys.argv[1:]:
    x = load(f); sr = 44100; w = int(0.002*sr)
    n = len(x)//w; e = np.sqrt((x[:n*w].reshape(n,w)**2).mean(1)) + 1e-6
    # yerel medyan (±60 ms) ile karşılaştır
    k = 30; med = np.array([np.median(e[max(0,i-k):i+k]) for i in range(n)])
    r = e/med
    hits = np.where((r > 8) & (e > 0.01))[0]
    ev=[]; last=-99
    for h in hits:
        if h-last > 25: ev.append(h)
        last=h
    print(f"{f.split('/')[-1]}: {len(ev)} tık adayı", " ".join(f"{h*w/sr:.2f}s(x{r[h]:.0f})" for h in ev[:25]))
