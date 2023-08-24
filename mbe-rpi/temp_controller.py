import asyncio

import fans_controller
import mock_fans_controller
import psutil
import temp_reader

TEMP_READ_WAIT_TIME = 1/2
TEMP_CONTROL_WAIT_TIME = 1/2

BOX_TEMP_THRESHOLD = 35

CPU_TEMP_THRESHOLD = 70


# TODO implement method that evaluates if the increase in fan speed is helping or not - maybe use a pid controller

class TemperatureController:
    def __init__(self, data_record, settings):
        self.settings = settings
        self.cpu_temperature = 0
        self.box_temperature = 0
        self.override_mode = False
        self.fan_controller = fans_controller.FansController(settings)
        self.data_record = data_record
        
    def change_all_fan_speed(self, value):
        if self.override_mode and self.fan_controller.all_fans_active():
            self.fan_controller.change_speed_all_fans(value)

    def get_speed_all_fans(self):
        return self.fan_controller.get_speed_all_fans()
    
    def activate_all_fans(self):
        print("LOG: Activating all fans")
        if self.override_mode:
            self.fan_controller.activate_all_fans()
            print("LOG: All fans activated")
        else:
            print("LOG: Override mode is not active")

    def activate_fan(self, fan_id):
        if self.override_mode:
            self.fan_controller.activate_fan(fan_id)   

    def deactivate_fan(self, fan_id):
        if self.override_mode:
            self.fan_controller.deactivate_fan(fan_id)     

    def deactivate_all_fans(self):
        if self.override_mode:
            self.fan_controller.deactivate_all_fans()

    def get_temperature_status(self):
        temperature_status = {}
        temperature_status["cpu_temperature"] = self.cpu_temperature
        temperature_status["box_temperature"] = self.box_temperature
        temperature_status["box_fan"] = self.fan_controller.is_fan_active('box')
        temperature_status["rpi_fan"] = self.fan_controller.is_fan_active('rpi')
        return temperature_status

    async def read_temperature(self):
        while True:
            self.cpu_temperature = psutil.sensors_temperatures()["cpu_thermal"][0].current
            self.box_temperature = temp_reader.read_temperature()
            self.data_record.record_temperature_data([self.box_temperature, self.cpu_temperature])
            await asyncio.sleep(TEMP_READ_WAIT_TIME)

    async def control_temperature(self):
        while True:
            if not self.override_mode:

                if self.box_temperature > BOX_TEMP_THRESHOLD:
                    self.fan_controller.activate_fan('box')
                else:
                    self.fan_controller.deactivate_fan('box')

                if self.cpu_temperature > CPU_TEMP_THRESHOLD:
                    self.fan_controller.activate_fan('rpi')
                else:
                    self.fan_controller.deactivate_fan('rpi')
            
            await asyncio.sleep(TEMP_CONTROL_WAIT_TIME)