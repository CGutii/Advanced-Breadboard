import serial 
#import time

if __name__=='__main__':
    # open serial port
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()    
    
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)                                                                                                                                                                  
            if float(line) >= 60.00:
                ser.write(b"red\n")
            else:
                print(line)
           
        
