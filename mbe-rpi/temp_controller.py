import asyncio

import fans_controller
import temp_reader

TEMP_READ_WAIT_TIME = 1/10
TEMP_CONTROL_WAIT_TIME = 1/5

TEMP_THRESHOLD = 40

def get_fan_speed_from_temp(temp):
    if temp > TEMP_THRESHOLD:
        return (temp - TEMP_THRESHOLD) * 2 + 20
    else:
        return 0

# TODO implement method that evaluates if the increase in fan speed is helping or not - maybe use a pid controller

class TemperatureController:
    def __init__(self):
        self.current_temperature = 0
        self.override_mode = False
        self.fan_controller = fans_controller.FansController()
        
    def change_all_fan_speed(self, value):
        self.fan_controller.change_speed_all_fans(value)

    async def read_temperature(self):
        while True:
            self.current_temperature = temp_reader.read_temperature()
            await asyncio.sleep(TEMP_READ_WAIT_TIME)

    async def control_temperature(self):
        while True:
            if not self.override_mode:
                fan_speed = get_fan_speed_from_temp(self.current_temperature)
                temp_reader.set_fan_speed(fan_speed)

            await asyncio.sleep(TEMP_CONTROL_WAIT_TIME)