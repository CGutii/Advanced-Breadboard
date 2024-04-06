import serial
import time

# Structure to store sensor data
sensor_data = {
    "Voltage": 0.0,
    "Current": 0.0
}

def send_matrix(matrix):
    print("Sending matrix to ESP:", matrix)
    with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
        time.sleep(2)  # Wait for the serial connection to initialize

        # Send each row followed by a newline character
        for row in matrix:
            line = ' '.join(row) + '\n'
            ser.write(line.encode())
            print(f"Sent row to ESP: {line.strip()}")  # Debug print statement for each row

        print("Matrix sent to ESP successfully.")

def receive_sensor_data():
    with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
        time.sleep(2)  # Wait for the serial connection to initialize after sending matrix
        while True:
            if ser.in_waiting:
                received_line = ser.readline().decode().strip()
                if received_line.startswith("SENSOR_DATA"):
                    _, voltage, current = received_line.split(',')
                    # Update the global sensor_data dictionary
                    sensor_data["Voltage"] = float(voltage)
                    sensor_data["Current"] = float(current)
                    print(f"Updated Sensor Data: Voltage = {voltage}V, Current = {current}mA")

def send_matrix_and_receive_data(matrix):
    send_matrix(matrix)
    receive_sensor_data()  # Call the function to receive sensor data continuously

# Example usage
if __name__ == "__main__":
    # Placeholder matrix for demonstration. Replace with actual matrix data.
    example_matrix = [
        ["1", "0", "1"],
        ["0", "1", "0"],
        ["1", "0", "1"]
    ]
    send_matrix_and_receive_data(example_matrix)
