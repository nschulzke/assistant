from typing import List, Tuple

from core.action import Action


class Weather(Action):
    def handle(self, tokens: List[dict]) -> Tuple[str, str]:
        matches = [token for token in tokens if token['entity'].startswith('weather.')]
        if len(matches) > 0:
            return "respond", "I can tell you about the weather."

    def prompts(self) -> List[str]:
        return [
            "What is the weather like in [New York](weather.location)?",
            "What is the weather in [San Francisco](weather.location)?",
            "What's the temperature right now in [American Fork](weather.location)?",
            "What will the temperature be [tomorrow](weather.time) in [San Jose](weather.location)?",
            "What's the weather like in [New York](weather.location) [tomorrow](weather.time)?",
            "What will the weather be like in [Boston](weather.location) [next week](weather.time)?",
        ]


class Timer(Action):
    def handle(self, tokens: List[dict]) -> Tuple[str, str]:
        matches = [token for token in tokens if token['entity'].startswith('timer.')]
        if len(matches) > 0:
            return "respond", "I can set timers for you."

    def prompts(self) -> List[str]:
        return [
            "Set a timer for [20 minutes](timer.time).",
            "Set a timer for [1 hour](timer.time).",
            "Set a timer for [2 hours](timer.time).",
            "Set a timer for [3 hours](timer.time).",
            "Set a timer for [ten seconds](timer.time).",
            "Set a timer for [ten minutes](timer.time).",
            "Set a timer for [ten hours](timer.time).",
            "Set a timer for [thirty seconds](timer.time).",
            "Set a [thirty second](timer.time) timer.",
            "Set a [ten minute](timer.time) timer.",
            "Set a [ten hour](timer.time) timer.",
            "Set a [ten second](timer.time) timer.",
        ]
