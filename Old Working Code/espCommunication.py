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
