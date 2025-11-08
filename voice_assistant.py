import queue
import sounddevice as sd
import sys
from asr import ASR_VOSK
import multiprocessing as mp
from llm import LLM
from tts_engine import TTS_KOKORO
from queue import Empty
import time

DEVICE = None
q = queue.Queue()
transcript_queue = mp.Queue()
audio_queue = mp.Queue()          # 👈 add this for TTS audio transfer
finished_event = mp.Event()
stop_event = mp.Event()

finished_event.set()


def llm_tts_process_func(transcript_queue, audio_queue, finished_event, stop_event):
    llm_sys = LLM()
    tts_sys = TTS_KOKORO()

    while not stop_event.is_set():
        try:
            transcript = transcript_queue.get(timeout=1)
        except Empty:
            transcript = None

        if transcript and transcript.get('type') == 'transcript_final':
            text = transcript["text"]
            finished_event.clear()
            print("User -->", text)
            llm_output = llm_sys.get_response(text)
            print("Agent -->", llm_output)

            # generate audio samples without playing them
            samples, sample_rate = tts_sys.generate_tts_audio(llm_output)
            
            # send to main process
            audio_queue.put((samples, sample_rate))


llm_tts_process = mp.Process(
    target=llm_tts_process_func,
    args=(transcript_queue, audio_queue, finished_event, stop_event)
)
llm_tts_process.start()


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    if finished_event.is_set():
        q.put_nowait(bytes(indata))


try:
    device_info = sd.query_devices(DEVICE, "input")
    SAMPLERATE = int(device_info["default_samplerate"])
    asr = ASR_VOSK(SAMPLERATE, transcript_queue=transcript_queue)

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

        while not stop_event.is_set():
            # 🧠 check for incoming audio from TTS worker
            try:
                
                samples, sr = audio_queue.get_nowait()
                finished_event.clear()
                sd.play(samples, sr)
                sd.wait()
                time.sleep(0.5)
                finished_event.set()
            except queue.Empty:
                pass

            # normal ASR pipeline
            try:
                data = q.get(timeout=1)
                if finished_event.is_set() and data:
                    asr.get_transcript(data)
            except queue.Empty:
                pass

except KeyboardInterrupt:
    stop_event.set()
    llm_tts_process.join()
    del asr
    print("\nDone")
except Exception as e:
    print(f"Error: {e}")
