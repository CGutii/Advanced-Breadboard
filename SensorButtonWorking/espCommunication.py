# espCommunication.py
import serial
import time

flag = True
sensor_info = "Voltage:4.00  Current:5.0"  # This will store the last received sensor data

def send_matrix(matrix):
    global sensor_info
    print("Sending matrix to ESP:", matrix)
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(2)  # Wait for the serial connection to initialize

    for row in matrix:
        line = ' '.join(row) + '\n'
        ser.write(line.encode())
        print(f"Sent row to ESP: {line.strip()}")  # Debug print statement for each row

    # Assuming the sensor data is continuously being sent, read the latest available data
    while True:
        if ser.inWaiting() > 0:
            received_data = ser.readline().decode().strip()
            print("Received data from ESP:", received_data)
            sensor_info = received_data  # Store the latest sensor data
            break

    ser.close()

def get_sensor_data():
    global sensor_info
    return sensor_info
