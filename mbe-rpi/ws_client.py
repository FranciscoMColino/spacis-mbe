import asyncio
import json
import time

import spacis_utils
import websockets

HOST = "localhost"
PORT = 8080
WS_CLIENT_WAIT_TIME = 1/400
WS_CLIENT_LONG_WAIT_TIME = 1/10
RECONNECT_WAIT_TIME = 5

TEMPERATURE_STATUS_WAIT_TIME = 5

GPS_STATUS_WAIT_TIME = 5

# TODO implement a way to reconnect to the server if the connection is lost

class MainBoxClient:
    def __init__(self, data_buffer, data_mng, command_handler, temp_controller):
        self.data_buffer = data_buffer
        self.data_mng = data_mng
        self.url = f"ws://{HOST}:{PORT}"
        self.ws = None
        self.command_handler = command_handler
        self.temp_controller = temp_controller

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

                # try to parse the message that should be in json format
                try:
                    message = json.loads(message)
                except json.decoder.JSONDecodeError:
                    print("LOG: Received message is not in JSON format")
                    continue

                # check if the message is a command
                if message["type"] == "command":
                    print("LOG: Received message is a command")
                    self.command_handler.add_command(message["data"])
                else:
                    print("LOG: Received message is not a command")

            except self.ws.exceptions.ConnectionClosed:
                print("LOG: Connection closed")
                self.ws = None
                asyncio.create_task(self.connect())

            await asyncio.sleep(WS_CLIENT_WAIT_TIME)


    async def periodic_data_transfer(self):
        while True:
            await asyncio.sleep(WS_CLIENT_LONG_WAIT_TIME)

            self.data_buffer = self.data_mng.get_ws_client_buffer()

            # print("LOG: periodic_data_transfer")
            #print("Server status: ", "ws ok " if self.ws else "ws BAD", self.data_buffer)
            if self.ws and self.data_buffer:
                print("LOG: aquired lock")
                print(f"LOG: Sending Sensor data w/ {len(self.data_buffer)} samples")
                message = {}
                message["type"] = "sensor_data"
                message["data"] = spacis_utils.pack_sensor_data(self.data_buffer)
                self.data_buffer = []
                self.data_mng.clear_ws_client_buffer()
                await self.ws.send(json.dumps(message))
                await asyncio.sleep(WS_CLIENT_LONG_WAIT_TIME)

    async def periodic_temperature_status(self):
        while True:
            await asyncio.sleep(TEMPERATURE_STATUS_WAIT_TIME)
            if self.ws:
                print("LOG: Sending temperature status")
                message = {}
                message["type"] = "temperature_status"
                message["data"] = self.temp_controller.get_temperature_status()
                await self.ws.send(json.dumps(message))
    