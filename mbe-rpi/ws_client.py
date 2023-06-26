import asyncio
import json
import time

import spacis_utils
import websockets

HOST = "localhost"
PORT = 8080
WS_CLIENT_WAIT_TIME = 1/400
WS_CLIENT_LONG_WAIT_TIME = 1/10

class MainBoxClient:
    def __init__(self, data_buffer, data_mng):
        self.data_buffer = data_buffer
        self.data_mng = data_mng
        self.url = f"ws://{HOST}:{PORT}"
        self.ws = None

    async def connect(self):
        while True:
            try:
                self.ws = await websockets.connect(self.url)
                print("LOG: Client started")
                await self.ws.send("client-connect")

                # TODO better client-server handshake

                break
            except ConnectionRefusedError:
                print("LOG: Connection refused")
                await asyncio.sleep(WS_CLIENT_WAIT_TIME)

        

    async def read_from_server(self):
            
        #handle messages from the server
        # Receiving messages from the server
        while True:
            try:
                message = await self.ws.recv()
                print(f'RECEIVED: {message}')
                # Handle messages accordingly
            except self.ws.exceptions.ConnectionClosed:
                print("LOG: Connection closed")
                self.ws = None

            await asyncio.sleep(WS_CLIENT_WAIT_TIME)


    async def periodic_data_transfer(self):
        while True:
            await asyncio.sleep(WS_CLIENT_LONG_WAIT_TIME)

            self.data_buffer = self.data_mng.get_ws_client_buffer()

            # print("LOG: periodic_data_transfer")
            #print("Server status: ", "ws ok " if self.ws else "ws BAD", self.data_buffer)
            if self.ws and self.data_buffer:
                print("ACQUIRED: lock")
                # TODO replace prints with a proper logger
                print(f"SENDING: Sensor data w/ {len(self.data_buffer)} samples")
                message = {}
                message["type"] = "sensor_data"
                message["data"] = spacis_utils.pack_sensor_data(self.data_buffer)
                self.data_buffer = []
                self.data_mng.clear_ws_client_buffer()
                await self.ws.send(json.dumps(message))
                await asyncio.sleep(WS_CLIENT_LONG_WAIT_TIME)