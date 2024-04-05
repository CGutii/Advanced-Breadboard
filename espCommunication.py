import serial
import time

def send_matrix(matrix):
    print("Sending matrix to ESP:", matrix)
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    time.sleep(2)  # Wait for the serial connection to initialize

    for row in matrix:
        line = ' '.join(row) + '\n'
        ser.write(line.encode())
        print(f"Sent row to ESP: {line.strip()}")

    # Now listen for the matrix received signal and then sensor data
    while True:
        if ser.in_waiting > 0:
            received_data = ser.readline().decode().strip()
            if received_data == "MATRIX_RECEIVED":
                print("Matrix processing completed by ESP.")
                break  # Exit loop once matrix is confirmed to be received

    # Continuously print received sensor data
    while True:
        if ser.in_waiting > 0:
            sensor_data = ser.readline().decode().strip()
            print("Received data from ESP:", sensor_data)

send_matrix([["1", "0", "0"], ["0", "1", "0"], ["0", "0", "1"]])
