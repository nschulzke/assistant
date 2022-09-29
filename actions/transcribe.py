from typing import List, Tuple

from pynput import keyboard

from core import Action
from core.action import Result


class Transcribe(Action):
    def __init__(self):
        self.transcribing = False
        self.controller = keyboard.Controller()

    def prompts(self) -> List[str]:
        return [
            "Start [transcribing](transcribe.start).",
            "Start [dictating](transcribe.start).",
            "Stop [transcribing](transcribe.stop).",
            "Stop [dictating](transcribe.stop).",
        ]

    def handle(self, utterance: str, tokens: List[dict]) -> Tuple[Result, str]:
        print(tokens)
        if self.transcribing:
            should_halt = len([token for token in tokens if token['entity'] == 'transcribe.stop']) > 0
            if should_halt:
                self.transcribing = False
                return Result.RESPOND, "Okay, done."
            else:
                self.controller.type(utterance)
                return Result.WAIT, ""
        else:
            should_start = len([token for token in tokens if token['entity'].startswith('transcribe.start')]) > 0
            if should_start:
                self.transcribing = True
                return Result.RESPOND_AND_WAIT, "Okay, let's start."
