import serial
import time

def send_matrix(matrix):
    print("Sending matrix to ESP:", matrix)
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize

    # Send each row followed by a newline character
    for row in matrix:
        line = ' '.join(row) + '\n'
        ser.write(line.encode())
        print(f"Sent row to ESP: {line.strip()}")  # Debug print statement for each row

    ser.close()
    print("Matrix sent to ESP successfully.")

# Add a new function to espCommunication.py
def request_wattmeter_readings():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)  # May need to adjust the port
    ser.write(b"REQUEST_WATTMETER_READINGS\n")  # Command to request readings from ESP32

    # Wait for the response from the ESP32
    response = ser.readline().decode().strip()
    ser.close()
    return response
