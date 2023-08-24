import asyncio
import json
import time

import spacis_utils
import websockets

WS_CLIENT_WAIT_TIME = 1/400
WS_CLIENT_LONG_WAIT_TIME = 1/200
PERIODIC_DATA_TRANSFER_WAIT_TIME = 1/3
RECONNECT_WAIT_TIME = 3
MAX_NUM_SAMPLES = 1000

TEMPERATURE_STATUS_WAIT_TIME = 1
GPS_STATUS_WAIT_TIME = 1
SYSTEM_STATUS_WAIT_TIME = 1

# TODO implement a way to reconnect to the server if the connection is lost

class MainBoxClient:
    def __init__(self, data_buffer, data_mng, command_handler, temp_controller, system_controller, gps_controller, settings):
        self.data_buffer = data_buffer
        self.data_mng = data_mng
        self.settings = settings
        self.url = f"ws://{settings['gcs_server_ip']}:{settings['gcs_server_port']}"
        self.ws = None
        self.command_handler = command_handler
        self.temp_controller = temp_controller
        self.system_controller = system_controller
        self.gps_controller = gps_controller

    async def run(self):
        print("LOG: Trying to connect to server")
        await self.connect()
        asyncio.create_task(self.read_from_server())
        asyncio.create_task(self.periodic_data_transfer())
        asyncio.create_task(self.periodic_temperature_status())
        asyncio.create_task(self.periodic_system_status())
        asyncio.create_task(self.periodic_gps_status())

    async def connect(self):
        while True:
            try:
                self.ws = await websockets.connect(self.url)
                print("LOG: Client started")
                await self.ws.send("client-connect")
                print("LOG: Client connected to server")

                # TODO better client-server handshake

                break
            except ConnectionRefusedError:
                print("LOG: Connection refused")
                await asyncio.sleep(WS_CLIENT_WAIT_TIME)
            except Exception as e:
                print("LOG: Exception while connecting to server ", e)
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

            except Exception as e:
                print("LOG: Exception while reading from server ", e)

                self.ws = None
                await self.connect()

            await asyncio.sleep(WS_CLIENT_WAIT_TIME)


    async def periodic_data_transfer(self):
        while True:
            try:
                await asyncio.sleep(WS_CLIENT_LONG_WAIT_TIME)

                self.data_buffer = self.data_mng.get_ws_client_buffer()

                # print("LOG: periodic_data_transfer")
                #print("Server status: ", "ws ok " if self.ws else "ws BAD", self.data_buffer)
                if self.ws and self.data_buffer:
                    #print("LOG: aquired lock")
                    print(f"LOG: Sending Sensor data w/ {len(self.data_buffer)} samples")

                    transmission_data = []

                    if len(self.data_buffer) > MAX_NUM_SAMPLES:
                        transmission_data = self.data_buffer[:MAX_NUM_SAMPLES]
                        self.data_buffer = self.data_buffer[MAX_NUM_SAMPLES:]
                        self.data_mng.reduce_ws_client_buffer(MAX_NUM_SAMPLES)
                        print("LOG: Data buffer overflow, sending only 1200 samples")
                        print("LOG: Data buffer size: ", len(self.data_buffer))
                    else:
                        transmission_data = self.data_buffer
                        self.data_buffer = []
                        self.data_mng.clear_ws_client_buffer()

                    message = {}
                    message["type"] = "sensor_data"
                    message["data"] = spacis_utils.pack_sensor_data(transmission_data)
                    
                    await self.ws.send(json.dumps(message))
                    await asyncio.sleep(PERIODIC_DATA_TRANSFER_WAIT_TIME)
            except websockets.exceptions.ConnectionClosedError:
                print("LOG: Connection closed")
                self.ws = None
                await self.connect()

    async def periodic_temperature_status(self):
        while True:
            try:
                await asyncio.sleep(TEMPERATURE_STATUS_WAIT_TIME)
                if self.ws:
                    print("LOG: Sending temperature status")
                    message = {}
                    message["type"] = "temperature_status"
                    message["data"] = self.temp_controller.get_temperature_status()
                    await self.ws.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosedError:
                print("LOG: Connection closed")
                self.ws = None
                await self.connect()

    async def periodic_system_status(self):
        while True:
            try:
                await asyncio.sleep(SYSTEM_STATUS_WAIT_TIME)
                if self.ws:
                    print("LOG: Sending system status")
                    message = {}
                    message["type"] = "system_control_data"
                    message["data"] = self.system_controller.get_system_status()
                    await self.ws.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosedError:
                print("LOG: Connection closed")
                self.ws = None
                await self.connect()

    async def periodic_gps_status(self):
        while True:
            try:
                await asyncio.sleep(GPS_STATUS_WAIT_TIME)
                if self.ws:
                    print("LOG: Sending GPS status")
                    message = {}
                    message["type"] = "gps_data"
                    message["data"] = self.gps_controller.get_gps_status()
                    await self.ws.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosedError:
                print("LOG: Connection closed")
                self.ws = None
                await self.connect()
    
