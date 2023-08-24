import asyncio

import system_controller

"""
Command message format

{
    "type": <command_type>, exs "TEMPERATURE"
    "action": <command_action>, exs OVERRIDE
    "value": <command_value>, exs 25, True
}

"""

# TODO check command syntax and format

COMMAND_HANDLER_WAIT_TIME = 1/10

class CommandHandler:
    def __init__(self, temp_controller, system_controller):
        self.command_queue = []
        self.temp_controller = temp_controller
        self.system_controller = system_controller

    def add_command(self, command):
        self.command_queue.append(command)

    def handle_command(self, command):
        if command["type"] == "TEMPERATURE":
            if command["action"] == "RPI_FAN_ACTIVE":
                if command["value"]:
                    self.temp_controller.activate_fan("rpi")
                else:
                    self.temp_controller.deactivate_fan("rpi")
            elif command["action"] == "BOX_FAN_ACTIVE":
                if command["value"]:
                    self.temp_controller.activate_fan("box")
                else:
                    self.temp_controller.deactivate_fan("box")
            else:
                print("LOG: Unknown temperature command action")
        elif command["type"] == "OS":
            if command["action"] == "OVERRIDE":
                self.temp_controller.override_mode = command["value"]
                self.system_controller.override_mode = command["value"]
                print("LOG: Override mode set to " + str(command["value"]))
            elif command["action"] == "SET_CPU_SPEED":
                print("LOG: Setting CPU speed to " + str(command["value"]))
                self.system_controller.set_cpu_speed(command["value"])
            elif command["action"] == "REBOOT":
                print("LOG: Rebooting")
                self.system_controller.reboot()
        else:
            print("LOG: Unknown command type {0}".format(command["type"]))

    def handle_head_command(self):
        if len(self.command_queue) > 0:
            print("LOG: Handling command")
            command = self.command_queue[0]
            self.command_queue = self.command_queue[1:]
            self.handle_command(command)

    async def periodic_handle_command(self):
        while True:
            
            self.handle_head_command()
            await asyncio.sleep(COMMAND_HANDLER_WAIT_TIME)

    

