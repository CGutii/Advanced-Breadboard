import serial
import time

class SensorDataHandler:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.sensor_data = {"Voltage": 0, "Current": 0}

    def listen_for_sensor_data(self):
        time.sleep(2)  # Allow time for connection to initialize
        while self.ser.in_waiting > 0:
            line = self.ser.readline().decode('utf-8').rstrip()
            if line.startswith("SENSOR_DATA"):
                _, voltage, current = line.split(',')  # Extract voltage and current
                self.sensor_data = {"Voltage": voltage, "Current": current}
                print(f"Received sensor data: Voltage = {voltage}V, Current = {current}mA")

    def get_sensor_data(self):
        return self.sensor_data


def send_matrix(matrix):
    print("Sending matrix to ESP:", matrix)
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize

    # Send each row followed by a newline character
    for row in matrix:
        line = ' '.join(row) + '\n'
        ser.write(line.encode())
        print(f"Sent row to ESP: {line.strip()}")  # Debug print statement for each row

    ser.close()
    print("Matrix sent to ESP successfully.")
