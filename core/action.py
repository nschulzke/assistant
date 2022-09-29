from typing import List, Tuple
from enum import Enum


class Result(Enum):
    RESPOND = "RESPOND"
    RESPOND_AND_WAIT = "RESPOND_AND_WAIT"
    WAIT = "WAIT"
    HALT = "HALT"


class Action:
    def handle(self, utterance: str, tokens: List[dict]) -> Tuple[Result, str]:
        """
        Handles the tokens and returns a response.
        """
        raise NotImplementedError

    def prompts(self) -> List[str]:
        """
        Returns a list of prompts to train the matcher.
        """
        raise NotImplementedError
