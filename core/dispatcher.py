from typing import List

from core.action import Action, Result


class Dispatcher:
    def __init__(self, actions: List[Action]):
        self.actions = actions
        self.waiting_action = None

    def attempt_dispatch(self, action: Action, utterance: str, tokens: List[dict]):
        match action.handle(utterance, tokens):
            case (Result.RESPOND, response):
                self.waiting_action = None
                return response
            case (Result.RESPOND_AND_WAIT, response):
                self.waiting_action = action
                return response
            case (Result.WAIT, _):
                self.waiting_action = action
                return ""
            case (Result.HALT, _):
                self.waiting_action = None
                return ""
        return None

    def dispatch(self, utterance: str, tokens: List[dict]) -> str:
        """
        Dispatches the tokens to the registered functions, stopping after one function handles
        the request.
        """
        if self.waiting_action is None:
            for action in self.actions:
                response = self.attempt_dispatch(action, utterance, tokens)
                if response is not None:
                    return response
        else:
            response = self.attempt_dispatch(self.waiting_action, utterance, tokens)
            if response is not None:
                return response

        return "I don't know how to answer that."

    def prompts(self):
        return [prompt for action in self.actions for prompt in action.prompts()]
