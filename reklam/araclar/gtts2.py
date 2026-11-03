import sys, wave
from google import genai
from google.genai import types
model, voice, prompt, out = sys.argv[1:5]
c = genai.Client()
r = c.models.generate_content(model=model, contents=prompt,
    config=types.GenerateContentConfig(response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)))))
pcm = r.candidates[0].content.parts[0].inline_data.data
with wave.open(out, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
print(out, round(len(pcm)/48000, 2), "s")
