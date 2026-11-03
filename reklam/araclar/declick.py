# Sessizlik içindeki tek başına kısa darbeleri (ağız tıkı) yumuşak bir çukurla bastırır.
import sys, numpy as np, soundfile as sf
src, dst = sys.argv[1], sys.argv[2]
x, sr = sf.read(src, dtype="float64")
w = int(0.002 * sr); n = len(x) // w
e = np.sqrt((x[:n*w].reshape(n, w) ** 2).mean(1)) + 1e-6
fixed = 0
for i in range(n):
    lo, hi = max(0, i - 10), min(n, i + 11)
    ctx = np.concatenate([e[lo:max(lo, i - 2)], e[min(hi, i + 3):hi]])
    if len(ctx) < 6: continue
    base = np.median(ctx)
    if e[i] > 0.02 and e[i] > 8 * base and base < 0.012:
        a, b = max(0, (i - 2) * w), min(len(x), (i + 3) * w)
        L = b - a; win = 1 - 0.95 * np.sin(np.linspace(0, np.pi, L)) ** 2
        x[a:b] *= win; fixed += 1
sf.write(dst, x, sr, subtype="PCM_16")
print(dst.split("/")[-1], "onarılan tık:", fixed)
