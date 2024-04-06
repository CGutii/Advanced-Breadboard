import serial
import time

class ESPCommunication:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        time.sleep(2)  # Ensure serial connection initializes

    def send_matrix_and_receive_data(self, matrix):
        print("Sending matrix to ESP:", matrix)
        # Send each row followed by a newline to signal the end of the matrix
        for row in matrix:
            line = ' '.join(row) + ';'
            self.ser.write(line.encode())
            print(f"Sent row to ESP: {line.strip()}")  # Debug print
        
        # Waiting for matrix processing confirmation
        while True:
            response = self.ser.readline().decode().strip()
            if response == "MATRIX_RECEIVED":
                print("ESP acknowledged matrix reception.")
                break
        
        # Now, receiving sensor data
        print("Receiving sensor data from ESP...")
        sensor_data = self.ser.readline().decode().strip()  # Example: "SENSOR_DATA,3.3V,500mA"
        print("Received sensor data:", sensor_data)
        # Processing sensor data as needed
        
        # Close serial after operation (optional, depends on use case)
        # self.ser.close()

# Create a global instance to use across modules
esp_comm = ESPCommunication()
