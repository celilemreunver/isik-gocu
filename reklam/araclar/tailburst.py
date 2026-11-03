# Dosya sonundaki "sessizlik + kısa patlama" kalıbını bulup patlamayı keser.
import sys, numpy as np, soundfile as sf
for p in sys.argv[1:]:
    x, sr = sf.read(p, dtype="float64"); w = int(0.005 * sr); n = len(x) // w
    e = np.sqrt((x[:n*w].reshape(n, w) ** 2).mean(1))
    loud = e > 0.01
    segs = []; i = 0
    while i < n:
        if loud[i]:
            j = i
            while j < n and loud[j]: j += 1
            segs.append((i, j)); i = j
        else: i += 1
    msg = "temiz"
    if len(segs) >= 2:
        a, b = segs[-1]; pa, pb = segs[-2]
        gap = (a - pb) * w / sr; dur = (b - a) * w / sr
        if dur < 0.3 and gap >= 0.06:
            cut = pb * w + int(0.03 * sr)
            y = x[:cut].copy(); f = int(0.06 * sr)
            y[-f:] *= np.cos(np.linspace(0, np.pi / 2, f)) ** 2
            sf.write(p, y, sr, subtype="PCM_16")
            msg = f"SONDA PATLAMA KESİLDİ ({dur*1000:.0f} ms, öncesinde {gap*1000:.0f} ms sessizlik, tepe rms {e[a:b].max():.2f})"
    print(p.split('/')[-1], msg)
