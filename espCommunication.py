import serial
import time

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)
        self.sensor_data = {"Voltage": "0", "Current": "0"}

    def send_matrix(self, matrix):
        print("Sending matrix to ESP:", matrix)
        matrix_str = ';'.join([' '.join(row) for row in matrix]) + ';'
        self.ser.write(matrix_str.encode())
        print(f"Matrix sent: {matrix_str.strip()}")
        
        # Wait for confirmation
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line == "MATRIX_RECEIVED":
                    print("Matrix processing confirmed by ESP.")
                    break

    def update_sensor_data(self):
        print("Collecting sensor data...")
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith("SENSOR_DATA"):
                    _, voltage, current = line.split(',')
                    self.sensor_data = {"Voltage": voltage, "Current": current}
                    print(f"Received sensor data: Voltage = {voltage}V, Current = {current}mA")
                    break

    def get_sensor_data(self):
        self.update_sensor_data()
        return self.sensor_data

esp_comm = ESPCommunication()

def send_matrix(matrix):
    esp_comm.send_matrix(matrix)

def get_sensor_data():
    return esp_comm.get_sensor_data()
