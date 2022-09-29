import pyttsx3

from actions.testing import weather, timer
from core.classifier import load_classifier
from core.dispatcher import Dispatcher
from core.transcriber import transcriber

if __name__ == '__main__':
    tts = pyttsx3.init()
    classifier = load_classifier()
    dispatcher = Dispatcher()
    dispatcher.register(weather, timer)

    for output in transcriber():
        print("> " + output)
        tokens = classifier(output)
        response = dispatcher.dispatch(tokens)
        print()
        print(response)
        tts.say(response)
        tts.runAndWait()
