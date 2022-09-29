import argparse
import pyttsx3

from actions import dispatcher
from core import load_classifier, train_classifier, transcriber


def run_assistant():
    tts = pyttsx3.init()
    classifier = load_classifier()

    for utterance in transcriber():
        print()
        print("> " + utterance)
        tokens = classifier(utterance)
        response = dispatcher.dispatch(utterance, tokens)
        print(response)
        tts.say(response)
        tts.runAndWait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="An AI voice assistant.")
    parser.add_argument("--train", action="store_true", help="Train the classifier.")
    args = parser.parse_args()

    if args.train:
        print("Training classifier...")
        train_classifier(dispatcher.prompts())
    else:
        print("Starting assistant...")
        run_assistant()
