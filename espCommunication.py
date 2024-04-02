import serial
import time

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)  # Adjusted timeout for waiting
        self.sensor_data = {"Voltage": "0", "Current": "0"}

    def send_matrix(self, matrix):
        print("Sending matrix to ESP:", matrix)
        matrix_str = ';'.join([' '.join(row) for row in matrix]) + ';'
        self.ser.write(matrix_str.encode())
        print(f"Matrix sent: {matrix_str.strip()}")
        
        # Wait for a confirmation message from ESP that the matrix is received
        confirmation = self.ser.readline().decode('utf-8').strip()
        if confirmation == "MATRIX_RECEIVED":
            print("Confirmation received: Matrix processed by ESP.")
        else:
            print("No confirmation received. There might be an issue.")

    def update_sensor_data(self):
        # Assume sensor data is being sent continuously after matrix handling
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith("SENSOR_DATA"):
                    _, voltage, current = line.split(',')
                    self.sensor_data = {"Voltage": voltage, "Current": current}
                    print(f"Received sensor data: Voltage = {voltage}V, Current = {current}mA")
                    break  # After receiving sensor data, break the loop

    def get_sensor_data(self):
        self.update_sensor_data()  # Update sensor data before fetching
        return self.sensor_data

# Global instance of ESPCommunication
esp_comm = ESPCommunication()

# Function to send matrix, to be called from outside
def send_matrix(matrix):
    esp_comm.send_matrix(matrix)

# Function to get sensor data, to be called from translate_screen.py
def get_sensor_data():
    return esp_comm.get_sensor_data()
