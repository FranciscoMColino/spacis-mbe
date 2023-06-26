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
    def __init__(self, data_buffer):
        self.data_buffer = data_buffer
        self.url = f"ws://{HOST}:{PORT}"
        self.ws = None

    async def connect_and_read(self):
        async with websockets.connect(self.url) as self.ws: 
            print("LOG: Client started")
            #send a message to the server
            
            #TODO better client-server handshake
            await self.ws.send("client-connect")
            #handle messages from the server
            # Receiving messages from the server
            while True:
                try:
                    message = await self.ws.recv()
                    print(f'RECEIVED: {message}')
                    # Handle messages accordingly
                except self.ws.exceptions.ConnectionClosed:
                    print('WebSocket connection closed by the server')
                    break
                await asyncio.sleep(WS_CLIENT_WAIT_TIME)


    async def periodic_data_transfer(self):
        while True:
            await asyncio.sleep(WS_CLIENT_WAIT_TIME)
            if self.ws and self.data_buffer:
                print("ACQUIRED: lock")
                # TODO replace prints with a proper logger
                print(f"SENDING: Sensor data w/ {len(self.data_buffer)} samples")
                message = {}
                message["type"] = "sensor_data"
                message["data"] = spacis_utils.pack_sensor_data(self.data_buffer)
                self.data_buffer = []

                await self.ws.send(json.dumps(message))
                await asyncio.sleep(WS_CLIENT_LONG_WAIT_TIME)