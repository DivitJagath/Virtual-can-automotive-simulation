import tkinter as tk
import math

class DashboardGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual CAN Cluster – Automotive HMI")
        self.root.geometry("1200x600")
        self.root.configure(bg="#050b1a")

        self.canvas = tk.Canvas(self.root, width=1200, height=600,
                                bg="#050b1a", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Title
        self.canvas.create_text(600, 40, text="AUTOMOTIVE CAN CLUSTER",
                                fill="#00e5ff", font=("Segoe UI", 22, "bold"))

        # Speedometer
        self.speed_center = (300, 300)
        self.speed_radius = 150
        self.draw_gauge(self.speed_center, self.speed_radius, 200, step=20, unit="km/h")

        # RPM Meter
        self.rpm_center = (900, 300)
        self.rpm_radius = 150
        self.draw_gauge(self.rpm_center, self.rpm_radius, 6000, step=1000, unit="RPM")

        # Labels under meters
        self.canvas.create_text(300, 480, text="Speedometer", fill="#00e5ff",
                                font=("Segoe UI", 14, "bold"))
        self.canvas.create_text(900, 480, text="RPM Meter", fill="#00e5ff",
                                font=("Segoe UI", 14, "bold"))

        # Needles
        self.speed_needle = self.canvas.create_line(300, 300, 300, 160, width=4, fill="#00ff99")
        self.rpm_needle = self.canvas.create_line(900, 300, 900, 160, width=4, fill="#ffaa00")

        # Value text
        self.speed_text = self.canvas.create_text(300, 350, text="0 km/h",
                                                  fill="#00ff99", font=("Segoe UI", 18, "bold"))
        self.rpm_text = self.canvas.create_text(900, 350, text="0 RPM",
                                                fill="#ffaa00", font=("Segoe UI", 18, "bold"))

        # Temp box
        self.temp_box = self.canvas.create_rectangle(520, 170, 680, 230,
                                                     outline="#ff3b3b", width=2)
        self.temp_text = self.canvas.create_text(600, 200, text="🌡️ 0.0 °C",
                                                  fill="white", font=("Segoe UI", 14, "bold"))

        # Mode
        self.mode_text = self.canvas.create_text(600, 260, text="MODE: ECO",
                                                  fill="#00e5ff", font=("Segoe UI", 14, "bold"))

        # System status (two-line layout)
        self.status_main = self.canvas.create_text(600, 310, text="OK",
                                                    fill="#00ff66", font=("Segoe UI", 16, "bold"))
        self.status_detail = self.canvas.create_text(600, 340, text="NO FAULT",
                                                      fill="#00ff66", font=("Segoe UI", 12, "bold"))

        # Emergency text
        self.emergency_text = self.canvas.create_text(600, 380, text="",
                                                       fill="red", font=("Segoe UI", 14, "bold"))

    # ---------------- Gauge Drawing ----------------
    def draw_gauge(self, center, radius, max_val, step, unit):
        cx, cy = center

        # Outer ring
        self.canvas.create_oval(cx - radius, cy - radius,
                                cx + radius, cy + radius,
                                outline="#0f1f3a", width=4)

        # Ticks + numbers
        for value in range(0, max_val + 1, step):
            angle = 180 - (value / max_val) * 180
            rad = math.radians(angle)

            x1 = cx + radius * math.cos(rad)
            y1 = cy - radius * math.sin(rad)
            x2 = cx + (radius - 12) * math.cos(rad)
            y2 = cy - (radius - 12) * math.sin(rad)

            self.canvas.create_line(x1, y1, x2, y2, fill="#00e5ff", width=2)

            tx = cx + (radius - 30) * math.cos(rad)
            ty = cy - (radius - 30) * math.sin(rad)

            self.canvas.create_text(tx, ty, text=str(value),
                                    fill="#7adfff", font=("Segoe UI", 9))

    # ---------------- Updates ----------------
    def set_speed(self, speed):
        angle = 180 - (speed / 200) * 180
        self.rotate_needle(self.speed_needle, self.speed_center, angle)
        self.canvas.itemconfig(self.speed_text, text=f"{speed:.1f} km/h")

    def set_rpm(self, rpm):
        angle = 180 - (rpm / 6000) * 180
        self.rotate_needle(self.rpm_needle, self.rpm_center, angle)
        self.canvas.itemconfig(self.rpm_text, text=f"{int(rpm)} RPM")

    def set_temp(self, temp):
        self.canvas.itemconfig(self.temp_text, text=f"🌡️ {temp:.1f} °C")

    def set_mode(self, mode):
        self.canvas.itemconfig(self.mode_text, text=f"MODE: {mode}")

    def set_fault(self, fault):
        if fault == "NO_FAULT":
            self.canvas.itemconfig(self.status_main, text="OK", fill="#00ff66")
            self.canvas.itemconfig(self.status_detail, text="NO FAULT", fill="#00ff66")
            self.canvas.itemconfig(self.emergency_text, text="")
        else:
            self.canvas.itemconfig(self.status_main, text="DANGER", fill="red")
            self.canvas.itemconfig(self.status_detail, text=fault.replace("_", " "), fill="red")

    def set_emergency(self, msg):
        self.canvas.itemconfig(self.emergency_text, text=msg)

    # ---------------- Needle Math ----------------
    def rotate_needle(self, needle, center, angle):
        cx, cy = center
        rad = math.radians(angle)
        x = cx + 120 * math.cos(rad)
        y = cy - 120 * math.sin(rad)
        self.canvas.coords(needle, cx, cy, x, y)

    # ---------------- Run ----------------
    def run(self):
        self.root.mainloop()
