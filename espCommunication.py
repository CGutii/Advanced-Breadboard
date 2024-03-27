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

def request_multimeter_data():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)
    time.sleep(2)
    ser.write(b'request_data\n')  # Send a newline terminated request to the ESP
    response_lines = []
    for _ in range(4):  # Expecting 4 lines of response
        data = ser.readline().decode().strip()  # Read lines from ESP
        if data:  # If data is not an empty string
            response_lines.append(data)
            print(data)  # Debug print each line
    ser.close()
    return response_lines


