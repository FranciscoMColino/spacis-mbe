import asyncio
import json
import signal
import sys
import threading
import time

import command_handler
import data_manager
import serial_comms
import spacis_utils
import temp_controller
import websockets
import ws_client


def interrupt_handler(signal, frame):
    print("KeyboardInterrupt caught. Exiting gracefully...")
    serial_comms.kill_signal_generator()
    signal_management_thread.join()
    sys.exit(0)

def due_serial_connect_protocol():
    global ser_com

    serial_comms.serial_reading = True
    ser_com = serial_comms.DueSerialComm()

    while not ser_com.connect():
        ser_com.reset()
        # reset the serial connection
        print("ERROR: Could not connect to serial port.")
        time.sleep(1)


async def main():
    # connect to gcs computer (server) with a webscoket client
    signal.signal(signal.SIGINT, interrupt_handler)

    #start thread running signal generator


    client_buffer = []
    recorder_buffer = []

    tmp_controller = temp_controller.TemperatureController()

    cmd_handler = command_handler.CommandHandler(tmp_controller)

    data_mng = data_manager.DataManager(recorder_buffer, client_buffer)

    client = ws_client.MainBoxClient(client_buffer, data_mng, cmd_handler)

    await client.connect()
    
    due_serial_connect_protocol()

    global signal_management_thread
    signal_management_thread = threading.Thread(target=ser_com.run)
    signal_management_thread.start()

    # TODO deactivate readings

    asyncio.create_task(cmd_handler.periodic_handle_command())
    asyncio.create_task(tmp_controller.read_temperature())
    asyncio.create_task(tmp_controller.control_temperature())
    asyncio.create_task(client.read_from_server())
    asyncio.create_task(client.periodic_data_transfer())
    asyncio.create_task(data_mng.get_data_from_serial_comm())
    

    while True:
        await asyncio.sleep(1)

    



asyncio.run(main())
