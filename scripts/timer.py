class Timer:
    def __init__(self, loop=False):
        self.loop = loop
        self.duration = 0

        self.start_time = 0
        self.time_passed = 0

    def start(self, duration, current_time):
        self.duration = duration * 1000
        self.start_time = current_time

    def update(self, current_time):
        self.time_passed = min(self.duration, current_time - self.start_time)

        if self.loop and self.has_finished():
            self.start(self.duration // 1000, current_time)

    def has_finished(self):
        return self.time_passed >= self.duration

    def time_left(self):
        return self.duration // 1000 - self.time_passed // 1000
