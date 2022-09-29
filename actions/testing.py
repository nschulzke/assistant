def weather(tokens):
    matches = [token for token in tokens if token['entity'].startswith('weather.')]
    if len(matches) > 0:
        return ["respond", "I can tell you about the weather."]


def timer(tokens):
    matches = [token for token in tokens if token['entity'].startswith('timer.')]
    if len(matches) > 0:
        return ["respond", "I can set timers for you."]
