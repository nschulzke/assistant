from actions.testing import Weather, Timer
from core.dispatcher import Dispatcher

dispatcher = Dispatcher([
    Weather(),
    Timer(),
])
