import random as rnd

import serial.tools.list_ports


# Function to detect Arduino serial port
def detect_arduino_port():
    ports = serial.tools.list_ports.comports()
    print(ports)
    arduino_ports = [
        p.device
        for p in ports
        if 'Arduino' in p.description  # Modify the description as per your Arduino's information
    ]
    if arduino_ports:
        return arduino_ports[0]  # Return the first detected Arduino port
    else:
        return None

MSG_SIZE = 39

# Detect Arduino port
arduino_port = detect_arduino_port()
if arduino_port:
    print(f"Arduino found on port: {arduino_port}")
    try:
        # Open the serial port
        ser = serial.Serial(arduino_port, 2000000)  # Modify the baud rate if necessary
        
        while True:
            # Read values from Arduino
            waiting_bytes = ser.in_waiting
            if waiting_bytes > MSG_SIZE:
                msg = ser.read(MSG_SIZE).decode('utf-8')
                no_bytes_msg = len(msg)
                if rnd.random() < 0.005:
                    print(f"Received value: {msg}, {waiting_bytes} bytes waiting, {no_bytes_msg} bytes received")
                
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        # Close the serial port
        ser.close()
else:
    print("Arduino not found.")