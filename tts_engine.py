"""
Note: on Linux you need to run this as well: apt-get install portaudio19-dev

pip install -U kokoro-onnx sounddevice

wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python examples/play.py
"""

import sounddevice as sd

from kokoro_onnx import Kokoro

class TTS_KOKORO():
    def __init__(self):
        self.kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    def generate_tts_audio(self,text):
        return self.kokoro.create(text, voice="af_sarah", speed=1.0, lang="en-us")
    def stop(self):
        del self.kokoro



if __name__=="__main__":
    tts = TTS_KOKORO()
    tts.play_tts("Hello! How are you?")
    tts.play_tts("Beneath the soft, amber glow of the setting sun, as the wind whispered through the leaves and distant waves murmured against the shore, she walked along the narrow, winding path that led to the old lighthouse, her thoughts drifting between memories of forgotten summers and dreams of places she had never seen, feeling at once the quiet ache of solitude and the tender promise of something new waiting just beyond the horizon")