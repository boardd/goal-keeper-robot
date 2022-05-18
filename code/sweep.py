import serial
import time

ANGLE_START = -0.4
ANGLE_END = 0
SWEEP_START = 0.6
SWEEP_END = -0.6
TICKS = 5
DELAY = 0.1

arduino = serial.Serial(port="COM5", baudrate=1000000, timeout=0.1)

# Wait for Arduno to be ready
while True:
    data = arduino.readline()
    if b"READY" in data:
        break
    time.sleep(0.1)

print("Ready")

# Set position
time.sleep(0.5)
arduino.write(bytes(str(ANGLE_START) + "\n", "utf-8"))
time.sleep(0.5)

# Send sweep of angles
for angle_i in range(TICKS + 1):
    angle = SWEEP_START + (SWEEP_END - SWEEP_START) * (angle_i / TICKS)
    print(angle)
    arduino.write(bytes(str(angle) + "\n", "utf-8"))
    time.sleep(DELAY)

# Reset position
time.sleep(0.5)
arduino.write(bytes(str(ANGLE_END) + "\n", "utf-8"))
time.sleep(0.5)
