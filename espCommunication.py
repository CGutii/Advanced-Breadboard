# espCommunication.py
import serial
import time

def send_matrix(matrix):
    # Open serial connection
    # Make sure to replace 'COM3' with the correct port for your ESP32
    # and adjust the baudrate if different.
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)  # wait for the serial connection to initialize

    for row in matrix:
        # Convert the row list to a string and send it
        line = ' '.join(row) + '\n'
        ser.write(line.encode())

    ser.close()  # Close the serial connection

if __name__ == "__main__":
    # Test matrix
    matrix = [
        ["R1", "0", "0"],
        ["0", "C1", "0"],
        ["0", "0", "R2"]
    ]
    send_matrix(matrix)
