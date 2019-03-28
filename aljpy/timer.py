import time
from contextlib import contextmanager

class Timer:

    def __init__(self):
        self._start = time.perf_counter()
        self._end = None

    def stop(self):
        self._end = time.perf_counter()
    
    def duration():
        return self._end - self._start
    
@contextmanager
def timer():
    timer = Timer()
    try:
        yield timer
    finally:
        timer.stop()
