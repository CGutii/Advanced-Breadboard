import serial
import time
import threading

class ESPCommunication:
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def open_connection(self):
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
        time.sleep(2)  # Allow time for serial connection to initialize

    def close_connection(self):
        if self.ser:
            self.ser.close()

    def send_matrix(self, matrix):
        if not self.ser:
            print("Serial connection not established.")
            return

        print("Sending matrix to ESP:", matrix)
        for row in matrix:
            line = ' '.join(row) + '\n'
            self.ser.write(line.encode())
            print(f"Sent row to ESP: {line.strip()}")
        print("Matrix sent to ESP successfully.")

    def read_sensor_data(self):
        if not self.ser:
            print("Serial connection not established.")
            return

        print("Requesting sensor data from ESP...")
        self.ser.write(b"REQUEST_SENSOR_DATA\n")
        while True:
            received_data = self.ser.readline().decode().strip()
            if received_data:
                print("Received data from ESP:", received_data)

esp_comm = ESPCommunication()

# Example usage
if __name__ == '__main__':
    esp_comm.open_connection()
    # Assume matrix data is ready; this is just a placeholder
    matrix = [["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]
    esp_comm.send_matrix(matrix)
    threading.Thread(target=esp_comm.read_sensor_data, daemon=True).start()
