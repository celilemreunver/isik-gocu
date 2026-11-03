import sys, sherpa_onnx, soundfile as sf
voice, text, out, speed = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv)>4 else 1.0
d=f"./modeller/vits-piper-tr_TR-{voice}-medium"
cfg=sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=f"{d}/tr_TR-{voice}-medium.onnx",tokens=f"{d}/tokens.txt",data_dir=f"{d}/espeak-ng-data"),num_threads=4))
tts=sherpa_onnx.OfflineTts(cfg); a=tts.generate(text,sid=0,speed=speed); sf.write(out,a.samples,a.sample_rate)
