import time

class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        if self.start_time is None:
            self.start_time = time.time()

    def elapsed(self):
        if self.start_time is None:
            return None
        return time.time() - self.start_time

    def reset(self):
        self.start_time = None