import serial
import time
import threading

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.sensor_data = ""

    def send_matrix(self, matrix):
        for row in matrix:
            self.ser.write(' '.join(row).encode() + b'\n')
            time.sleep(0.1)  # Short delay to ensure ESP processes data
        print("Matrix sent.")

    def listen_for_sensor_data(self):
        while True:
            if self.ser.in_waiting > 0:
                self.sensor_data = self.ser.readline().decode().strip()
                print("Received sensor data:", self.sensor_data)

    def start_sensor_data_thread(self):
        threading.Thread(target=self.listen_for_sensor_data, daemon=True).start()

    def get_sensor_data(self):
        return self.sensor_data

esp_comm = ESPCommunication()
esp_comm.start_sensor_data_thread()

# Example usage
# esp_comm.send_matrix([['1', '0', '1'], ['0', '1', '0'], ['1', '0', '1']])
# while True:
#     print(esp_comm.get_sensor_data())
#     time.sleep(2)
