import serial.tools.list_ports


# Function to detect Arduino serial port
def detect_arduino_port():
    ports = serial.tools.list_ports.comports()
    arduino_ports = [
        p.device
        for p in ports
        if 'Arduino' in p.description  # Modify the description as per your Arduino's information
    ]
    if arduino_ports:
        return arduino_ports[0]  # Return the first detected Arduino port
    else:
        return None

# Detect Arduino port
arduino_port = detect_arduino_port()
if arduino_port:
    print(f"Arduino found on port: {arduino_port}")
    try:
        # Open the serial port
        ser = serial.Serial(arduino_port, 9600)  # Modify the baud rate if necessary
        
        while True:
            # Read values from Arduino
            if ser.in_waiting > 0:
                value = ser.readline().decode().strip()
                print(f"Received value: {value}")
                
    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        # Close the serial port
        ser.close()
else:
    print("Arduino not found.")