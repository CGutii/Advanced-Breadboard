# espCommunication.py
import serial
import time

# Initialize serial port - adjust '/dev/ttyUSB0' as per your setup
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

def send_matrix(matrix):
    """
    Sends a matrix to the ESP device and waits for a confirmation
    or sensor data response.
    """
    print("Sending matrix to ESP:", matrix)
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Wait for the serial connection to initialize

        for row in matrix:
            line = ' '.join(row) + '\n'
            ser.write(line.encode())
            print(f"Sent row to ESP: {line.strip()}")  # Debug print statement for each row

        # After sending the matrix, wait for the ESP device to process
        # and return the sensor data.
        ser.flush()  # Ensure all data is sent
        request_sensor_data(ser)

def request_sensor_data(ser):
    """
    Requests the sensor data from the ESP device.
    """
    print("Requesting sensor data from ESP...")
    ser.write(b"GET_SENSOR_DATA\n")  # Command to ESP to send back sensor data
    
    # Wait for the sensor data response
    sensor_info = ser.readline().decode().strip()
    print("Received sensor data from ESP:", sensor_info)

def get_sensor_data():
    """
    A placeholder function if you need to fetch sensor data directly.
    Adjust this function as per your requirement.
    """
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Wait for the serial connection to initialize
        ser.write(b"GET_SENSOR_DATA\n")  # Send command to get sensor data
        sensor_info = ser.readline().decode().strip()
        print("Received sensor data from ESP:", sensor_info)
        return sensor_info

# # Example usage
# if __name__ == "__main__":
#     # Example matrix to send
#     matrix = [["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]]
#     send_matrix(matrix)
#     # Later on, you can directly call get_sensor_data() if needed
#     # sensor_data = get_sensor_data()
