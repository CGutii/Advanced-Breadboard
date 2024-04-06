import serial
import time

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200)
        self.sensor_data = {}

    def send_matrix(self, matrix):
        print("Sending matrix to ESP:", matrix)
        matrix_str = ';'.join([' '.join(row) for row in matrix]) + ';'
        self.ser.write(matrix_str.encode())
        print(f"Matrix sent: {matrix_str.strip()}")

    def listen_for_sensor_data(self):
        while True:
            line = self.ser.readline().decode('utf-8').strip()
            if line.startswith("SENSOR_DATA"):
                _, voltage, current = line.split(',')
                self.sensor_data = {"Voltage": voltage, "Current": current}
                print("Received sensor data:", self.sensor_data)

    def get_sensor_data(self):
        return self.sensor_data

esp_comm = ESPCommunication()
