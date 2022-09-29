import pyttsx3

from classifier import load_classifier
from recorder import recorder

if __name__ == '__main__':
    tts = pyttsx3.init()
    classifier = load_classifier()

    for output in recorder():
        print(output)
        print(classifier(output))
        tts.say(output)
        tts.runAndWait()
