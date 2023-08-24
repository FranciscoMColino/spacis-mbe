import sys

import serial


def read_ubx_message(ser):
    # Read the UBX message header
    header = ser.read(2)
    if len(header) == 2 and header == b'\xb5\x62':
        msg_class = ser.read(1)
        msg_id = ser.read(1)
        payload_length = ser.read(2)
        payload_length = int.from_bytes(payload_length, byteorder='little')
        payload = ser.read(payload_length)
        checksum = ser.read(2)
        
        # Perform checksum verification (optional but recommended)
        # Checksum is calculated by XOR'ing bytes in the payload
        ck_a = 0
        ck_b = 0
        for byte in msg_class + msg_id + payload:
            ck_a = (ck_a + byte) & 0xFF
            ck_b = (ck_b + ck_a) & 0xFF
        if ck_a == checksum[0] and ck_b == checksum[1]:
            return (msg_class, msg_id, payload)
    
    return None

def main():
    serial_port = '/dev/serial0'  # Serial port for Raspberry Pi (symbolic link to currently enabled serial port)
    baud_rate = 9600  # Adjust the baud rate based on your GPS module settings

    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            while True:
                ubx_message = read_ubx_message(ser)
                if ubx_message:
                    msg_class, msg_id, payload = ubx_message
                    print(f"Message Class: {msg_class}, Message ID: {msg_id}, Payload: {payload}")
    
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Serial communication stopped.")
        # Close the serial port before exiting
        ser.close()
        sys.exit(0)

if __name__ == "__main__":
    main()
