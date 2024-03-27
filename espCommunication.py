import serial
import time

# Assuming /dev/ttyUSB0 is correct; replace with the correct serial port for your system
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Structure to store sensor readings
sensor_data = {
    'busVoltage': 0,
    'shuntVoltage': 0,
    'current_mA': 0,
    'power_mW': 0
}

def read_sensor_data():
    if ser.inWaiting() > 0:
        data_str = ser.readline().decode('utf-8').strip()
        # Assuming sensor data is the last line after matrix rows
        if ',' in data_str:
            voltage, shuntVoltage, current_mA, power_mW = data_str.split(',')
            sensor_data['busVoltage'] = float(voltage)
            sensor_data['shuntVoltage'] = float(shuntVoltage)
            sensor_data['current_mA'] = float(current_mA)
            sensor_data['power_mW'] = float(power_mW)
            print("Received sensor data:", sensor_data)

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
