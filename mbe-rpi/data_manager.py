import asyncio

import serial_comms

DATA_MANAGER_WAIT_TIME = 1/400
DATA_MANAGER_LONG_WAIT_TIME = 1/40

class DataManager:
    def __init__(self, recorder_buffer, ws_client_buffer):
        self.recorder_buffer = recorder_buffer
        self.ws_client_buffer = ws_client_buffer

    def get_recorder_buffer(self):
        return self.recorder_buffer
    
    def get_ws_client_buffer(self):
        return self.ws_client_buffer
    
    def clear_recorder_buffer(self):
        self.recorder_buffer = []
    
    def clear_ws_client_buffer(self):
        self.ws_client_buffer = []

    async def get_data_from_serial_comm(self):
        while True:
            await asyncio.sleep(DATA_MANAGER_LONG_WAIT_TIME)

            #print("LOG: get_data_from_serial_comm")

            if serial_comms.recorded_signals:
                #print("LOG: get_data_from_serial_comm: recorded_signals")
                lock_aquired = serial_comms.lock.acquire(False)
                
                if lock_aquired:
                    #print("LOG: get_data_from_serial_comm: lock_aquired")
                    #print("LOG: get_data_from_serial_comm: recorded_signals", len(serial_comms.recorded_signals))
                    self.recorder_buffer.extend(serial_comms.recorded_signals)
                    self.ws_client_buffer.extend(serial_comms.recorded_signals)
                    #print("LOG: get_data_from_serial_comm: recorder_buffer", len(self.recorder_buffer))
                    #print("LOG: get_data_from_serial_comm: ws_client_buffer", len(self.ws_client_buffer))
                    serial_comms.recorded_signals = []
                    serial_comms.lock.release()

                    await asyncio.sleep(DATA_MANAGER_LONG_WAIT_TIME)
                elif lock_aquired:
                    serial_comms.lock.release()

            