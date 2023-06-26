import asyncio
import threading
import time

import serial.tools.list_ports

# TODO Move to config file
BAUDRATE = 500000
MAX_WAITING_TIME = 5 * 1000 * 1000 # microseconds before the serial connection is considered dead

recorded_signals = []
serial_reading = True
lock = threading.Lock()
command_buffer = []

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
            self.ser  = serial.Serial(arduino_ports[0], self.baundrate)
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

    async def read_messages(self):

        ser = self.ser

        if (not ser):
            print("ERROR: No serial port found")
            return

        recorded_signals_local_cache = []
        global serial_reading
        global recorded_signals

        while serial_reading:
            try:
                while ser.in_waiting > 0:

                    msg = ser.readline().decode('utf-8').rstrip().split(',')
                    #print("RECEIVED: ", msg)
                    try:
                        msg = [int(i) for i in msg[:4] if i != '']
                        recorded_signals_local_cache.append(msg)
                    except ValueError:
                        print("ERROR: Could not convert string to int")
                        print(msg)

            except serial.SerialException:
                print("ERROR: Serial connection lost")
                self.status = "disconnected"
                return False

            lock_aquired = lock.acquire(False)

            if lock_aquired and recorded_signals_local_cache:
                #transfer recorded_signals_local_cache to recorded_signals
                recorded_signals.extend(recorded_signals_local_cache)
                recorded_signals_local_cache = []
                lock.release()
            elif lock_aquired:
                lock.release()

            await asyncio.sleep(0.01)

    async def async_work(self):

        asyncio.create_task(self.command_check())

        while serial_reading:

            if not self.active:
                time.sleep(1)
                continue

            res = await self.read_messages()

            if not res:
                print("ERROR: Arduino dead or disconnected")
                print("LOG: Reseting the arduino")
                self.reset()
                print("LOG: Trying to connect to the arduino")
                self.connect()
            
            await asyncio.sleep(1)

    def run(self):
        asyncio.run(self.async_work())
            
