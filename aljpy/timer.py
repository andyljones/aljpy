import time
from contextlib import contextmanager

class Timer:

    def __init__(self):
        self._start = time.time()
        self._end = None

    def stop(self):
        self._end = time.time()
    
    def start(self):
        return self._start

    def end(self):
        return (self._end or time.time())
    
    def time(self):
        return self.end() - self.start()
    
@contextmanager
def timer():
    timer = Timer()
    try:
        yield timer
    finally:
        timer.stop()
