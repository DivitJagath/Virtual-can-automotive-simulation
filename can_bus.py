# can_bus.py

import threading
import queue
import time

class CANMessage:
    """
    Represents a CAN frame on the virtual bus.
    """
    def __init__(self, can_id, data, ecu_name, timestamp=None):
        self.can_id = can_id          # CAN ID (lower = higher priority)
        self.data = data              # Payload (speed, rpm, temp, etc.)
        self.ecu_name = ecu_name      # Sender ECU name
        self.timestamp = timestamp if timestamp is not None else time.time()

    def __repr__(self):
        return f"<CANMessage id={self.can_id} data={self.data} ecu={self.ecu_name} time={self.timestamp:.3f}>"


class CANBus:
    """
    Virtual CAN Bus with simple priority arbitration.
    Lower CAN ID has higher priority.
    """
    def __init__(self):
        # Priority queue: (can_id, timestamp, message)
        self._bus = queue.PriorityQueue()
        self._lock = threading.Lock()

    def send(self, msg: CANMessage):
        """
        Send a CAN message onto the virtual bus.
        """
        with self._lock:
            # PriorityQueue sorts by tuple order: can_id first, then timestamp
            self._bus.put((msg.can_id, msg.timestamp, msg))
            print(f"[CAN BUS] {msg.ecu_name} sent -> ID={msg.can_id}, Data={msg.data}")

    def receive(self, timeout=0.01):
        """
        Receive the next CAN message from the bus.
        Returns CANMessage or None if no message available.
        """
        try:
            _, _, msg = self._bus.get(timeout=timeout)
            return msg
        except queue.Empty:
            return None
