import asyncio

import serial_comms

DATA_MANAGER_WAIT_TIME = 1/400
DATA_MANAGER_LONG_WAIT_TIME = 1/40

class DataManager:
    def __init__(self, recorder_buffer, ws_client_buffer, data_record):
        self.recorder_buffer = recorder_buffer
        self.ws_client_buffer = ws_client_buffer
        self.data_record = data_record

    def get_recorder_buffer(self):
        return self.recorder_buffer
    
    def get_ws_client_buffer(self):
        return self.ws_client_buffer
    
    def clear_recorder_buffer(self):
        self.recorder_buffer = []
    
    def clear_ws_client_buffer(self):
        self.ws_client_buffer = []

    def reduce_ws_client_buffer(self, amount):
        self.ws_client_buffer = self.ws_client_buffer[amount:]

    async def get_data_from_serial_comm(self):
        while True:
            await asyncio.sleep(DATA_MANAGER_LONG_WAIT_TIME)

            if serial_comms.recorded_signals:
                lock_aquired = serial_comms.lock.acquire(False)
                
                if lock_aquired:
                    recorded = serial_comms.recorded_signals
                    self.recorder_buffer.extend(recorded)
                    self.ws_client_buffer.extend(recorded)
                    serial_comms.recorded_signals = []
                    serial_comms.lock.release()
                    
                    self.data_record.record_multiple_sensor_data(recorded)

                    await asyncio.sleep(DATA_MANAGER_LONG_WAIT_TIME)
                elif lock_aquired:
                    serial_comms.lock.release()

            