import serial
import threading
import time

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.sensor_data = {"Voltage": "0", "Current": "0"}
        self.matrix_sent = False
        self.start_listening_thread()

    def send_matrix(self, matrix):
        print("Sending matrix to ESP:", matrix)
        matrix_str = ';'.join([' '.join(row) for row in matrix]) + ';'
        self.ser.write(matrix_str.encode())
        print(f"Matrix sent: {matrix_str.strip()}")
        self.matrix_sent = True

    def listen_for_data(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith("SENSOR_DATA"):
                    if not self.matrix_sent:  # Ensure matrix has been sent before processing sensor data
                        continue
                    _, voltage, current = line.split(',')
                    self.sensor_data = {"Voltage": voltage, "Current": current}
                    print(f"Received sensor data: Voltage = {voltage}V, Current = {current}mA")
                elif line == "MATRIX_RECEIVED":
                    self.matrix_sent = False  # Reset the flag when matrix is received

    def start_listening_thread(self):
        threading.Thread(target=self.listen_for_data, daemon=True).start()

    def get_sensor_data(self):
        return self.sensor_data

esp_comm = ESPCommunication()

def send_matrix(matrix):
    esp_comm.send_matrix(matrix)

def get_sensor_data():
    return esp_comm.get_sensor_data()
