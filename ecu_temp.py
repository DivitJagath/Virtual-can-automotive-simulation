# ecu_temp.py

import threading
import time
import random
from can_bus import CANMessage
from mode_controller import current_mode, DrivingMode

class TempECU(threading.Thread):
    def __init__(self, can_bus):
        super().__init__(daemon=True)
        self.can_bus = can_bus
        self.temp = 70.0
        self.running = True

    def run(self):
        while self.running:
            if current_mode == DrivingMode.SPORT:
                heat = random.uniform(0.3, 1.5)
            elif current_mode == DrivingMode.ECO:
                heat = random.uniform(0.1, 0.6)
            else:
                heat = random.uniform(0.2, 1.0)

            cool = random.uniform(0.0, 0.8)
            self.temp += heat - cool
            self.temp = max(60.0, min(self.temp, 120.0))

            msg = CANMessage(200, round(self.temp, 2), "TempECU", time.time())
            self.can_bus.send(msg)

            time.sleep(1.0)
