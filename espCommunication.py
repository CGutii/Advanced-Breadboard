import serial
import time

def send_matrix(matrix):
    print("Sending matrix to ESP:", matrix)
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)

    matrix_str = ';'.join([' '.join(row) for row in matrix]) + ';'
    ser.write(matrix_str.encode())
    print(f"Matrix sent: {matrix_str.strip()}")

    ser.close()
    print("Matrix sent to ESP successfully.")
