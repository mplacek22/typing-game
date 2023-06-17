import threading
import time


class TimerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.is_running = True
        self.remaining_time = 60  # Timer duration in seconds

    def run(self):
        while self.remaining_time > 0 and self.is_running:
            time.sleep(1)
            self.remaining_time -= 1

        if self.remaining_time == 0:
            self.stop()

    def stop(self):
        self.is_running = False
