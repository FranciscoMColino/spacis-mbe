import asyncio

#import fans_controller
import mock_fans_controller
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
        #self.fan_controller = fans_controller.FansController()
        self.fan_controller = mock_fans_controller.MockFansController()
        
    def change_all_fan_speed(self, value):
        self.fan_controller.change_speed_all_fans(value)

    def get_speed_all_fans(self):
        return self.fan_controller.get_speed_all_fans()

    def get_temperature_status(self):
        temperature_status = {}
        temperature_status["current_temperature"] = self.current_temperature
        temperature_status["override_mode"] = self.override_mode
        temperature_status["fan_speed"] = self.fan_controller.get_speed_all_fans()
        temperature_status["fan_active"] = self.fan_controller.get_active_all_fans()
        return temperature_status

    async def read_temperature(self):
        while True:
            self.current_temperature = temp_reader.mock_read_temperature()
            print("LOG: Current temperature: " + str(self.current_temperature))
            await asyncio.sleep(TEMP_READ_WAIT_TIME)

    async def control_temperature(self):
        while True:
            if not self.override_mode:
                fan_speed = get_fan_speed_from_temp(self.current_temperature)
                self.fan_controller.change_speed_all_fans(fan_speed)

            await asyncio.sleep(TEMP_CONTROL_WAIT_TIME)