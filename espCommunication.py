import serial
import time

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.sensor_data = []

    def send_matrix_and_wait_for_data(self, matrix):
        self.send_matrix(matrix)
        self.wait_for_confirmation_and_read_sensor_data()

    def send_matrix(self, matrix):
        print("Sending matrix to ESP:")
        for row in matrix:
            line = ' '.join(row) + '\n'
            self.ser.write(line.encode())
            print(f"Sent row: {line.strip()}")
        print("Matrix sent successfully.")

    def wait_for_confirmation_and_read_sensor_data(self):
        while True:
            line = self.ser.readline().decode().strip()
            if line == "MATRIX_RECEIVED":
                print("Matrix processing confirmed, starting to read sensor data.")
                break
        while True:
            sensor_data = self.ser.readline().decode().strip()
            if sensor_data.startswith("SENSOR_DATA"):
                print(f"Received sensor data: {sensor_data}")
                self.sensor_data.append(sensor_data)  # Store or process as needed

esp_comm = ESPCommunication()
