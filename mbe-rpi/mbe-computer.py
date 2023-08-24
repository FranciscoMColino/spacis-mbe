import asyncio
import signal
import sys
import threading
import time

import command_handler
import data_manager
import serial_comms
import temp_controller
import ws_client
from data_recording import DataRecorder
from gps_controller import GpsController
from spacis_utils import parse_settings
from system_controller import SystemController


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

    settings = parse_settings()

    # connect to gcs computer (server) with a webscoket client
    signal.signal(signal.SIGINT, interrupt_handler)

    #start thread running signal generator

    client_buffer = []
    recorder_buffer = []

    data_record = DataRecorder()
    tmp_controller = temp_controller.TemperatureController(data_record, settings)
    system_controller = SystemController()
    cmd_handler = command_handler.CommandHandler(tmp_controller, system_controller)
    data_mng = data_manager.DataManager(recorder_buffer, client_buffer, data_record)
    gps_controller = GpsController(data_record)
    client = ws_client.MainBoxClient(client_buffer, data_mng, cmd_handler, tmp_controller, system_controller, gps_controller, settings)

    
    due_serial_connect_protocol()

    global signal_management_thread
    signal_management_thread = threading.Thread(target=ser_com.run)
    signal_management_thread.start()

    asyncio.create_task(client.run())

    asyncio.create_task(cmd_handler.periodic_handle_command())
    

    asyncio.create_task(data_mng.get_data_from_serial_comm())
    
    asyncio.create_task(tmp_controller.read_temperature())
    asyncio.create_task(tmp_controller.control_temperature())

    asyncio.create_task(system_controller.read_cpu_speed())

    asyncio.create_task(gps_controller.periodic_read_gps_coords())

    while True:
        await asyncio.sleep(1)

    



asyncio.run(main())
