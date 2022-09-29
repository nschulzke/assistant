import os

import whisper
from playsound import playsound
from pynput import keyboard
import time
import pyaudio
import wave

from key_state_listener import KeyStateListener

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "tmp/output.wav"


def transcriber():
    model = whisper.load_model("medium")
    p = pyaudio.PyAudio()
    frames = []
    started = False
    stream = None

    try:
        os.makedirs("tmp")
    except FileExistsError:
        pass

    def callback(in_data, frame_count, time_info, status):
        frames.append(in_data)
        return in_data, pyaudio.paContinue

    listener = KeyStateListener(keyboard.Key.pause)
    listener.start()
    print("Press and hold the 'PAUSE' key to begin recording")
    print("Release the 'PAUSE' key to end recording")
    while True:
        time.sleep(0.1)
        if listener.key_pressed and not started:
            # Start the recording
            frames = []
            playsound("sounds/start_recording.mp3")
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK,
                            stream_callback=callback)
            started = True

        elif not listener.key_pressed and started:
            started = False
            stream.stop_stream()
            stream.close()

            playsound("sounds/stop_recording.mp3")

            if os.path.exists(WAVE_OUTPUT_FILENAME):
                os.remove(WAVE_OUTPUT_FILENAME)

            with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))

            file = os.path.join(os.getcwd(), WAVE_OUTPUT_FILENAME)
            result = model.transcribe(file)
            yield result["text"]
