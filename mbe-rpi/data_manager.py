import asyncio

import serial_comms

DATA_MANAGER_WAIT_TIME = 1/400
DATA_MANAGER_LONG_WAIT_TIME = 1/40

class DataManager:
    def __init__(self, recorder_buffer, ws_client_buffer):
        self.recorder_buffer = recorder_buffer
        self.ws_client_buffer = ws_client_buffer

    async def get_data_from_serial_comm(self):
        while True:

            await asyncio.sleep(DATA_MANAGER_WAIT_TIME)

            if serial_comms.recorded_signals:
                lock_aquired = serial_comms.lock.acquire(False)
                if lock_aquired:
                    self.recorder_buffer.extend(serial_comms.recorded_signals)
                    self.ws_client_buffer.extend(serial_comms.recorded_signals)
                    serial_comms.recorded_signals = []
                    serial_comms.lock.release()
                    await asyncio.sleep(DATA_MANAGER_LONG_WAIT_TIME)
                elif lock_aquired:
                    serial_comms.lock.release()

            