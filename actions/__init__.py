from actions.testing import Weather, Timer
from actions.transcribe import Transcribe
from core import Dispatcher

dispatcher = Dispatcher([
    Weather(),
    Timer(),
    Transcribe(),
])
