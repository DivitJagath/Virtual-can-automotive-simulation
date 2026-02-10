# ecu_speed.py

import threading
import time
import random
from can_bus import CANMessage
from mode_controller import current_mode, DrivingMode

class SpeedECU(threading.Thread):
    def __init__(self, can_bus):
        super().__init__(daemon=True)
        self.can_bus = can_bus
        self.speed = 0.0
        self.running = True

    def run(self):
        while self.running:
            if current_mode == DrivingMode.ECO:
                accel = random.uniform(0.0, 1.2)
            elif current_mode == DrivingMode.SPORT:
                accel = random.uniform(0.5, 4.0)
            else:
                accel = random.uniform(0.2, 2.5)

            decel = random.uniform(0.0, 1.5)
            self.speed += accel - decel
            self.speed = max(0.0, min(self.speed, 200.0))

            msg = CANMessage(100, round(self.speed, 2), "SpeedECU", time.time())
            self.can_bus.send(msg)

            time.sleep(0.5)
