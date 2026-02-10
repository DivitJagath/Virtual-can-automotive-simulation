# ecu_engine.py

import threading
import time
import random
from can_bus import CANMessage
from mode_controller import current_mode, DrivingMode

class EngineECU(threading.Thread):
    def __init__(self, can_bus):
        super().__init__(daemon=True)
        self.can_bus = can_bus
        self.rpm = 900
        self.running = True

    def run(self):
        while self.running:
            if current_mode == DrivingMode.ECO:
                delta = random.randint(-200, 300)
            elif current_mode == DrivingMode.SPORT:
                delta = random.randint(-300, 700)
            else:
                delta = random.randint(-250, 400)

            self.rpm += delta
            self.rpm = max(800, min(self.rpm, 6000))

            msg = CANMessage(50, int(self.rpm), "EngineECU", time.time())
            self.can_bus.send(msg)

            time.sleep(0.5)
