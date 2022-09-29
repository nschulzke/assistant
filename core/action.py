from typing import List, Tuple


class Action:
    def handle(self, tokens: List[dict]) -> Tuple[str, str]:
        """
        Handles the tokens and returns a response.
        """
        raise NotImplementedError

    def prompts(self) -> List[str]:
        """
        Returns a list of prompts to train the matcher.
        """
        raise NotImplementedError
