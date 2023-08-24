import asyncio
import sys
import threading
import time

import serial_comm


def interrupt_handler(signal, frame):
    print("KeyboardInterrupt caught. Exiting gracefully...")
    serial_comm.kill_signal_generator()
    signal_management_thread.join()
    sys.exit(0)


def due_serial_connect_protocol():
    global ser_com

    serial_comm.serial_reading = True
    ser_com = serial_comm.DueSerialComm()

    while not ser_com.connect():
        ser_com.reset()
        # reset the serial connection
        print("ERROR: Could not connect to serial port.")
        time.sleep(1)


async def main():

    due_serial_connect_protocol()

    global signal_management_thread
    signal_management_thread = threading.Thread(target=ser_com.run)
    signal_management_thread.start()

    while True:
        await asyncio.sleep(1)


asyncio.run(main())
