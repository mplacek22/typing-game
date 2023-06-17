import threading
import time


class TimerThread(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game
        self.is_running = True
        self.timer_duration = 60  # Timer duration in seconds

    def run(self):
        remaining_time = self.timer_duration

        while remaining_time > 0 and self.is_running:
            self.game.display_timer(remaining_time)
            time.sleep(1)
            remaining_time -= 1

        if self.is_running:
            self.game.display_accuracy()
            self.game.display_restart()

    def stop(self):
        self.is_running = False
