import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
# ============ DEFAULT CONFIGURATION ============
MODEL_LANG = "en-us"
DEVICE = None
SAMPLERATE = None
FILENAME = None
# ===============================================

class ASR_VOSK:
    def __init__(self, samplerate, transcript_queue=None):
        self.MODEL_LANG = MODEL_LANG
        self.model = Model(lang=self.MODEL_LANG)
        self.SAMPLERATE = samplerate
        self.transcript_queue = transcript_queue
        self.rec = KaldiRecognizer(self.model, self.SAMPLERATE)

    def get_transcript(self, audio_data):
        if self.rec.AcceptWaveform(audio_data):
            transcript = json.loads(self.rec.Result())
            if transcript['text']:
                if self.transcript_queue:
                    self.transcript_queue.put_nowait({"type":"transcript_final","text":transcript['text']})
                # print(transcript)
        else:
            partial = json.loads(self.rec.PartialResult())
            if partial["partial"]:
                print("User(partial)--> ",partial["partial"])


if __name__ == "__main__":
    q = queue.Queue()
    t_q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    try:
        # Get default input device info
        device_info = sd.query_devices(DEVICE, "input")
        SAMPLERATE = int(device_info["default_samplerate"])

        # Initialize ASR after we know the sample rate
        asr = ASR_VOSK(SAMPLERATE, transcript_queue=t_q)

        with sd.RawInputStream(
            samplerate=SAMPLERATE,
            blocksize=8000,
            device=DEVICE,
            dtype="int16",
            channels=1,
            callback=callback,
        ):
            print("#" * 80)
            print("Press Ctrl+C to stop the recording")
            print("#" * 80)

            while True:
                data = q.get()
                asr.get_transcript(data)

    except KeyboardInterrupt:
        print("\nDone")
    except Exception as e:
        print(f"Error: {e}")
