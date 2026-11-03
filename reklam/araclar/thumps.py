import sys, subprocess, numpy as np
for f in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg","-nostdin","-v","error","-i",f,"-af","pan=mono|c0=c0,lowpass=f=120,lowpass=f=120","-ar","44100","-f","f32le","-"],capture_output=True).stdout
    lo = np.frombuffer(raw, dtype=np.float32)
    raw2 = subprocess.run(["ffmpeg","-nostdin","-v","error","-i",f,"-af","pan=mono|c0=c0","-ar","44100","-f","f32le","-"],capture_output=True).stdout
    full = np.frombuffer(raw2, dtype=np.float32)
    sr=44100; w=int(0.01*sr); n=min(len(lo),len(full))//w
    el=np.sqrt((lo[:n*w].reshape(n,w)**2).mean(1)); ef=np.sqrt((full[:n*w].reshape(n,w)**2).mean(1))+1e-5
    share=el/ef
    hits=np.where((el>0.03)&(share>0.6))[0]
    ev=[];last=-99
    for h in hits:
        if h-last>10: ev.append(h)
        last=h
    print(f"{f.split('/')[-1]}: {len(ev)} alçak frekans darbesi", " ".join(f"{h*w/sr:.2f}s(lo {el[h]:.2f}, pay {share[h]:.2f})" for h in ev[:20]))
