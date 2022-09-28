import os

import whisper
from pynput import keyboard
import time
import pyaudio
import wave
import sched
from classifier import load_classifier
import pyttsx3

tts = pyttsx3.init()

print(os.getcwd())

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "tmp/output.wav"

p = pyaudio.PyAudio()
frames = []
model = whisper.load_model("medium")
classifier = load_classifier()

try:
    os.makedirs("tmp")
except FileExistsError:
    pass


def transcribe(file):
    file = os.path.join(os.getcwd(), file)
    result = model.transcribe(file)

    return result["text"]


def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return in_data, pyaudio.paContinue


class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

    def on_press(self, key):
        if key == keyboard.Key.pause:
            self.key_pressed = True

    def on_release(self, key):
        if key == keyboard.Key.pause:
            self.key_pressed = False


listener = MyListener()
listener.start()
started = False
stream = None


def recorder():
    global started, p, stream, frames

    if listener.key_pressed and not started:
        # Start the recording
        frames = []
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

        if os.path.exists(WAVE_OUTPUT_FILENAME):
            os.remove(WAVE_OUTPUT_FILENAME)

        # Using with will close the file automatically
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        # No issues with playsound locking the file
        output = transcribe(os.path.join(os.path.dirname(__file__), WAVE_OUTPUT_FILENAME))
        print(output)
        print(classifier(output))
        tts.say(output)
        tts.runAndWait()

    # Reschedule the recorder function in 100 ms.
    task.enter(0.1, 1, recorder, ())


print("Press and hold the 'PAUSE' key to begin recording")
print("Release the 'PAUSE' key to end recording")
task = sched.scheduler(time.time, time.sleep)
task.enter(0.1, 1, recorder, ())
task.run()
