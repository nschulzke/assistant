from actions.testing import Weather, Timer
from core import Dispatcher

dispatcher = Dispatcher([
    Weather(),
    Timer(),
])
