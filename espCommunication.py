import serial
import time

def send_matrix(matrix):
    print("Sending matrix to ESP:", matrix)
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize

    # Send each row followed by a newline character
    for row in matrix:
        line = ' '.join(row) + '\n'
        ser.write(line.encode())
        print(f"Sent row to ESP: {line.strip()}")  # Debug print statement for each row

    ser.close()
    print("Matrix sent to ESP successfully.")
    
    # Reopen the serial connection for reading
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize

    # Receive data from ESP32
    received_data = ser.readline().decode().strip()
    print("Received data from ESP:", received_data)
    received_data = ser.readline().decode().strip()
    print("Received data from ESP:", received_data)

    #ser.close()
    #print(".")
