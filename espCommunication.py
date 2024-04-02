import serial
import threading
import time

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.sensor_data = {"Voltage": "0", "Current": "0"}
        # Start the listening thread as soon as the object is created
        self.start_listening_thread()

    def send_matrix(self, matrix):
        print("Sending matrix to ESP:", matrix)
        matrix_str = ';'.join([' '.join(row) for row in matrix]) + ';'
        self.ser.write(matrix_str.encode())
        print(f"Matrix sent: {matrix_str.strip()}")
        # No need to close the serial connection here

    def listen_for_data(self):
        """A method to continuously listen for incoming data from the ESP."""
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                # Assuming the sensor data is prefixed with 'SENSOR_DATA'
                if line.startswith("SENSOR_DATA"):
                    _, voltage, current = line.split(',')
                    self.sensor_data = {"Voltage": voltage, "Current": current}
                    print(f"Received sensor data: Voltage = {voltage}V, Current = {current}mA")
                # Implement additional parsing logic here if needed

    def start_listening_thread(self):
        """Start a thread to listen for incoming data without blocking."""
        threading.Thread(target=self.listen_for_data, daemon=True).start()

    def get_sensor_data(self):
        return self.sensor_data

# Global instance of ESPCommunication
esp_comm = ESPCommunication()

# Function to send matrix, to be called from outside
def send_matrix(matrix):
    esp_comm.send_matrix(matrix)

# Function to get sensor data, to be called from translate_screen.py
def get_sensor_data():
    return esp_comm.get_sensor_data()
