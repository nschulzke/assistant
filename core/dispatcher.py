from typing import List

from core.action import Action


class Dispatcher:
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def dispatch(self, tokens: List[dict]) -> str:
        """
        Dispatches the tokens to the registered functions, stopping after one function handles
        the request.
        """
        for action in self.actions:
            match action.handle(tokens):
                case ("respond", response):
                    return response

        return "I don't know how to answer that."

    def prompts(self):
        return [prompt for action in self.actions for prompt in action.prompts()]
