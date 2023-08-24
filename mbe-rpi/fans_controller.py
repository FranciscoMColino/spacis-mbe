import RPi.GPIO as GPIO


class Fan:
    def __init__(self, id, pin):
        self.id = id
        self.active = False
        self.pin = pin

class FansController:

    def __init__(self, settings):

        self.fan_ids = [0, 1]

        BOX_FANS_PIN = settings['box_fans_pin']
        RPI_FANS_PIN = settings['rpi_fans_pin']

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BOX_FANS_PIN, GPIO.OUT)
        GPIO.setup(RPI_FANS_PIN, GPIO.OUT)

        GPIO.output(BOX_FANS_PIN, GPIO.LOW)
        GPIO.output(RPI_FANS_PIN, GPIO.LOW)

        self.box_fans = Fan('box', BOX_FANS_PIN)
        self.rpi_fans = Fan('rpi', RPI_FANS_PIN )

        self.fans = {
            'box': self.box_fans,
            'rpi': self.rpi_fans
        }

    def get_fan_from_id(self, fan_id):
        return self.fans[fan_id]

    def change_speed_fan(self, fan_id, value):
        fan = self.get_fan_from_id(fan_id)
        if fan.active:
            fan.value = value
            if value == 0:
                GPIO.output(fan.pin, GPIO.LOW)
            else:
                GPIO.output(fan.pin, GPIO.HIGH)

    def activate_fan(self, fan_id):
        fan = self.get_fan_from_id(fan_id)
        fan.active = True
        GPIO.output(fan.pin, GPIO.HIGH)

    def deactivate_fan(self, fan_id):
        fan = self.get_fan_from_id(fan_id)
        fan.active = False
        GPIO.output(fan.pin, GPIO.LOW)
    
    def activate_all_fans(self):
        print("LOG: Activating all fans")
        for fan in self.fans:
            print("LOG: Activating fan ", fan.id)
            self.activate_fan(fan.id)
        print("LOG: All fans activated, ", self.get_active_all_fans())

    def deactivate_all_fans(self):
        for fan in self.fans:
            self.deactivate_fan(fan.id)
    
    def all_fans_active(self):
        for fan in self.fans:
            if not fan.active:
                return False
        return True
    
    def is_fan_active(self, fan_id):
        return self.get_fan_from_id(fan_id).active

    def get_active_all_fans(self):
        return [fan.active for fan in self.fans.values()]
    
        