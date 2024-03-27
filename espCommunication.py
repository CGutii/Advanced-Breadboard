import serial
import time

def send_matrix(matrix):
    print("Sending matrix to ESP:", matrix)
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        time.sleep(2)  # Allow time for the serial connection to establish

        matrix_str = ';'.join([' '.join(row) for row in matrix]) + '\n'
        ser.write(matrix_str.encode())
        print(f"Matrix sent: {matrix_str.strip()}")

        # Wait for acknowledgment with a 10-second timeout
        start_time = time.time()
        while True:
            if ser.in_waiting:
                response = ser.readline().decode().strip()
                print(f"Response from ESP: {response}")
                if response == "Received on the ESP":
                    print("ESP acknowledged receipt.")
                    break
            if time.time() - start_time > 10:  # Timeout after 10 seconds
                print("Timeout waiting for response from ESP.")
                break

        ser.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
