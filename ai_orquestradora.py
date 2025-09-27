# ai_orquestradora.py
import threading, time, os
from ai_miners import run_all
from db_utils import init_db

class Orquestradora:
    def __init__(self, interval_seconds=None):
        self.interval = int(interval_seconds or os.getenv("MINER_INTERVAL", 60))  # default 60s
        init_db()
        self._stop = False

    def run_loop(self):
        print("[Orquestradora] iniciada. interval =", self.interval, "s")
        while not self._stop:
            try:
                run_all()
            except Exception as e:
                print("[Orquestradora] erro run_all:", e)
            time.sleep(self.interval)

    def start_background(self):
        t = threading.Thread(target=self.run_loop, daemon=True)
        t.start()
        return t

    def stop(self):
        self._stop = True



