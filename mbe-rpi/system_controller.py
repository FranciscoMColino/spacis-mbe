import asyncio
import configparser
import itertools
import subprocess

import psutil

LOW_BOUND_CPU_SPEED = 600
HIGH_BOUND_CPU_SPEED = 2200

SYSTEM_UPDATE_TIME_INTERVAL = 1/2



class SystemController:

    def __init__(self):
        self.override_mode = False
        self.current_cpu_speed = 0
        self.clock_on_boot = self.get_configured_clock_speed()
        self.config_cpu_clock = 0

    def get_configured_clock_speed(self):
        with open('/boot/config.txt', 'r') as file:
            for line in file:
                if line.startswith('force_turbo=1'):
                    return 'Max'
                elif line.startswith('arm_freq='):
                    return line.strip().split('=')[1]
    
        return 'Default'


    def modify_config_file(self, config_file_path, key, value):
        with open(config_file_path, 'r') as f:
            lines = f.readlines()

        with open(config_file_path, 'w') as f:
            for line in lines:
                if line.startswith(key):
                    line = f"{key}={value}\n"
                f.write(line)

    def reboot(self):
        if self.override_mode:
            print("LOG: Rebooting system")
            command = "sudo reboot"
            subprocess.run(command, shell=True)
        else:
            print("LOG: System reboot denied, override mode not active")

    def set_cpu_speed(self, speed):

        if self.override_mode:

            if speed < LOW_BOUND_CPU_SPEED or speed > HIGH_BOUND_CPU_SPEED:
                print("LOG: CPU speed out of bounds")
                return
            config_file_path = '/boot/config.txt'
            # Specify the desired CPU clock speed in MHz
            # Modify the config.txt file
            self.modify_config_file(config_file_path, 'arm_freq', str(speed))

            self.config_cpu_clock = speed

            print("LOG: CPU speed set to " + str(speed))
        else:
            print("LOG: CPU speed change denied, override mode not active")

    async def read_cpu_speed(self):
        while True:
            self.current_cpu_speed = psutil.cpu_freq().current
            await asyncio.sleep(SYSTEM_UPDATE_TIME_INTERVAL)

    def get_system_status(self):
        system_status = {}
        system_status["override_mode"] = self.override_mode
        system_status["cpu_speed"] = self.current_cpu_speed
        system_status["clock_on_boot"] = self.clock_on_boot
        system_status["clock_config"] = self.config_cpu_clock
        return system_status


    