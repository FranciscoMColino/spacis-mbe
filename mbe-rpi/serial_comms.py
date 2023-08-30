import asyncio
import datetime
import random as rnd
import threading
import time

import serial.tools.list_ports

# TODO Move to config file
BAUDRATE = 500000
# microseconds before the serial connection is considered dead
MAX_WAITING_TIME = 5 * 1000 * 1000

SEQUENCE_MSG_SIZE = 38
PPS_MSG_SIZE = 14
READ_SIZE = 50

command_buffer = []

serial_reading = True
lock = threading.Lock()

recorded_signals = []
recorded_signals_local_cache = []

pps_id = -1
pps_entries = []
pps_entries_local_cache = []


def kill_signal_generator():
    global serial_reading
    serial_reading = False


def command_serial_comms(command):
    command_buffer.append(command)


class DueSerialComm():
    def __init__(self):
        self.baundrate = BAUDRATE
        self.data = []
        self.status = "disconnected"
        self.active = True

    async def command_check(self):
        while (len(command_buffer) > 0):

            lock_aquired = lock.acquire(False)

            if lock_aquired:

                command = command_buffer.pop(0)

                if (command == "activate"):
                    self.activate()
                elif (command == "deactivate"):
                    self.deactivate()
                elif (command == "reset"):
                    self.reset()
                else:
                    print("ERROR: Invalid command:", command)

                lock.release()

                if (len(command_buffer) == 0):
                    asyncio.sleep(1)

            elif lock_aquired:
                lock.release()

    def activate(self):
        self.active = True
        if (self.ser.isOpen()):
            self.ser.close()
        self.connect()

    def deactivate(self):
        self.active = False
        self.ser.close()
        self.status = "disconnected"

    # TODO keep trying to connect, and deal with disconnects

    def connect(self):
        # Filter the list to find the port with "Arduino" in its description

        if (not serial_reading):
            print("ERROR: Serial reading is not active")
            return False

        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description
        ]

        if (not arduino_ports):
            print("ERROR: No Arduino found")
            self.ser = None
            return

        try:
            self.ser = serial.Serial(arduino_ports[0], self.baundrate)
        except serial.SerialException:
            print("ERROR: Could not connect to serial port")
            self.ser = None
            return False

        if self.ser:
            print("Connected successfully to the arduino", arduino_ports[0])
            self.status = "connected"
            return True
        else:
            print("Failed to connect to the arduino")
            self.status = "disconnected"
            return False

    def reset(self):
        # TODO use gpio to reset the arduino
        pass

    def try_transfer_message(self):

        global serial_reading, recorded_signals_local_cache, pps_entries_local_cache, pps_entries

        lock_aquired = lock.acquire(False)

        if lock_aquired and recorded_signals_local_cache:
            # print("LOG: Succesfully aquired lock, transfering messages")
            # transfer recorded_signals_local_cache to recorded_signals
            recorded_signals.extend(recorded_signals_local_cache)
            recorded_signals_local_cache = []
            lock.release()
            return True
        if lock_aquired and pps_entries_local_cache:
            # print("LOG: Succesfully aquired lock, transfering messages")
            # transfer recorded_signals_local_cache to recorded_signals
            pps_entries.extend(pps_entries_local_cache)
            pps_entries_local_cache = []
            lock.release()
            return True
        elif lock_aquired:
            # print("LOG: Succesfully aquired lock")
            lock.release()
            return False

        return False

    async def read_messages(self):

        BURST_READ_SIZE = 256

        ser = self.ser

        if (not ser):
            print("ERROR: No serial port found")
            return

        global serial_reading, recorded_signals, recorded_signals_local_cache, pps_id

        recorded_signals_local_cache = []

        while serial_reading:
            # print("LOG: Reading serial")
            try:

                # print("LOG: Waiting for serial data, in_waiting: ", ser.in_waiting)

                acc = 0

                while ser.in_waiting > READ_SIZE:

                    acc += 1
                    if (acc > BURST_READ_SIZE):
                        break

                    char1 = ser.read(1).decode('utf-8')

                    if char1 == "S" and ser.read(1).decode('utf-8') == "Y":
                        msg = ser.read(PPS_MSG_SIZE).decode('utf-8').rstrip()

                        try:
                            msg = int(msg)
                            pps_id += 1
                            pps_entries_local_cache.append(
                                [pps_id, msg, datetime.datetime.now().strftime("%H:%M:%S")])

                        except Exception as e:
                            print("ERROR: Could not convert string to int, pps_msg")
                            ser.reset_input_buffer()
                            print(msg)

                    elif char1 == "C" and ser.read(1).decode('utf-8') == "A":

                        msg = ser.read(SEQUENCE_MSG_SIZE).decode(
                            'utf-8').rstrip().split(',')
                        try:
                            msg = [int(i) for i in msg if i != '']
                            msg.append(pps_id)
                            recorded_signals_local_cache.append(msg)
                            acc += 1
                        except Exception as e:
                            print(
                                "ERROR: Could not convert string to int, sequence_msg")
                            ser.reset_input_buffer()
                            print(msg)
                print("Break")
                acc = 0
                await asyncio.sleep(1/1600/2)

            except serial.SerialException:
                print("ERROR: Serial connection lost")
                self.status = "disconnected"
                return False
            except Exception as e:
                print("ERROR: Other error, ", e)
                self.status = "disconnected"
                return False

            # await asyncio.sleep(1/1600)

        ser.close()
        print("LOG: Serial connection closed")

    async def transfer_messages(self):

        global serial_reading, recorded_signals_local_cache

        while serial_reading:

            # print("LOG: Starting serial transfer")

            transfered_messages = self.try_transfer_message()

            if transfered_messages:
                # print("LOG: Transfered messages to recorded_signals")
                await asyncio.sleep(0.2)
            else:
                await asyncio.sleep(1/1600/2)

    async def async_work(self):

        asyncio.create_task(self.command_check())

        print("LOG: Starting serial reading")
        asyncio.create_task(self.read_messages())

        print("LOG: Starting serial transfer")
        asyncio.create_task(self.transfer_messages())

        while serial_reading:

            # TODO deal with arduino disconnections and deactivations

            await asyncio.sleep(1)

    def run(self):
        print("RUNNING THREAD")
        asyncio.run(self.async_work())
