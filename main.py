import time
import threading
from can_bus import CANBus
from ecu_speed import SpeedECU
from ecu_engine import EngineECU
from ecu_temp import TempECU
from dashboard_gui import DashboardGUI

# -------------------------
# Setup CAN + ECUs
# -------------------------
can_bus = CANBus()

speed_ecu = SpeedECU(can_bus)
engine_ecu = EngineECU(can_bus)
temp_ecu = TempECU(can_bus)

speed_ecu.start()
engine_ecu.start()
temp_ecu.start()

# -------------------------
# Dashboard
# -------------------------
gui = DashboardGUI()

# -------------------------
# Global State
# -------------------------
latest_temp = 0.0
latest_rpm = 0.0
current_mode = "ECO"

last_high_rpm_time = None

# -------------------------
# Driving Mode Logic
# -------------------------
def change_mode():
    global current_mode
    modes = ["ECO", "NORMAL", "SPORT"]
    i = 0
    while True:
        current_mode = modes[i % 3]
        gui.set_mode(current_mode)
        print(f"[MODE] Driving mode changed to {current_mode}")
        i += 1
        time.sleep(12)

# -------------------------
# Fault Decision Logic
# -------------------------
def decide_fault(temp, rpm):
    global last_high_rpm_time

    # CRITICAL OVERHEAT
    if temp > 105:
        return "CRITICAL_OVERHEAT"

    # Over-rev
    if rpm > 6500:
        return "OVERREV"

    # Sustained high RPM stress
    if rpm > 5500:
        if last_high_rpm_time is None:
            last_high_rpm_time = time.time()
        elif time.time() - last_high_rpm_time > 3:
            return "ENGINE_STRESS"
    else:
        last_high_rpm_time = None

    # Warning temp
    if temp > 90:
        return "TEMP_WARNING"

    return "NO_FAULT"

# -------------------------
# Fault Injector (demo)
# -------------------------
def fault_injector():
    while True:
        time.sleep(25)
        print("\n[FAULT] Engine Overheat Injected\n")
        temp_ecu.inject_overheat()

# -------------------------
# CAN Receiver
# -------------------------
def can_receiver():
    global latest_temp, latest_rpm
    while True:
        msg = can_bus.receive()
        if msg:
            if msg.ecu_name == "SpeedECU":
                gui.set_speed(msg.data)

            elif msg.ecu_name == "EngineECU":
                latest_rpm = msg.data
                gui.set_rpm(msg.data)

            elif msg.ecu_name == "TempECU":
                latest_temp = msg.data
                gui.set_temp(msg.data)

            # Fault Decision
            fault = decide_fault(latest_temp, latest_rpm)
            gui.set_fault(fault)

            # Emergency Help
            if fault in ["CRITICAL_OVERHEAT", "OVERREV"]:
                gui.set_emergency("SEND HELP")

        time.sleep(0.05)

# -------------------------
# Threads
# -------------------------
threading.Thread(target=change_mode, daemon=True).start()
threading.Thread(target=fault_injector, daemon=True).start()
threading.Thread(target=can_receiver, daemon=True).start()

print("Virtual CAN Simulation Started...\n")

# -------------------------
# Run GUI (Main Thread)
# -------------------------
gui.run()

# -------------------------
# Cleanup
# -------------------------
speed_ecu.stop()
engine_ecu.stop()
temp_ecu.stop()

print("Simulation Ended Cleanly.")
