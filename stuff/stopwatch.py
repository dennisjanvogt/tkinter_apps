import time


class Stopwatch:
    def __init__(self):
        self.start_time = 0
        self.paused_time = 0
        self.elapsed_time = 0
        self.first_start_timestamp = None
        self.running = False

    def start(self):
        if not self.first_start_timestamp:
            self.first_start_timestamp = time.time()
        if not self.running:
            self.start_time = time.time() - self.paused_time
            self.running = True

    def pause(self):
        if self.running:
            self.paused_time = time.time() - self.start_time
            self.running = False

    def reset(self):
        self.start_time = 0
        self.paused_time = 0
        self.running = False

    def get_time(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
        else:
            self.elapsed_time = self.paused_time
        return self.elapsed_time
