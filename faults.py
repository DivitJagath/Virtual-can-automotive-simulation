# faults.py

import random
import time

class FaultManager:
    def __init__(self):
        self.overheat = False
        self.sensor_glitch = False
        self.ecu_dropout = False

    def toggle_overheat(self, state: bool):
        self.overheat = state

    def toggle_sensor_glitch(self, state: bool):
        self.sensor_glitch = state

    def toggle_ecu_dropout(self, state: bool):
        self.ecu_dropout = state

    def apply_sensor_glitch(self, value):
        if self.sensor_glitch:
            # inject random wrong spike
            return value + random.uniform(-50, 50)
        return value

    def apply_overheat(self, temp):
        if self.overheat:
            return temp + random.uniform(5, 15)
        return temp

    def should_dropout(self):
        if self.ecu_dropout:
            return random.random() < 0.3  # 30% chance to drop
        return False
