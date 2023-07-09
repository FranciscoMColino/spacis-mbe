import RPi.GPIO as GPIO

FAN0_PIN = 18
FAN1_PIN = 23

FAN_CONTROL_FREQ = 1000

class Fan:
    def __init__(self, id, pwm):
        self.id = id
        self.active = False
        self.value = 0
        self.pwm = pwm

class FansController:

    def __init__(self):

        self.fan_ids = [0, 1]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FAN0_PIN, GPIO.OUT)
        GPIO.setup(FAN1_PIN, GPIO.OUT)

        self.fan0 = Fan(0, GPIO.PWM(FAN0_PIN, FAN_CONTROL_FREQ))
        self.fan1 = Fan(1, GPIO.PWM(FAN1_PIN, FAN_CONTROL_FREQ))

        self.fans = [self.fan0, self.fan1]

        self.fan0.pwm.start(0)
        self.fan1.pwm.start(0)

    def get_fan_from_id(self, fan_id):
        return self.fans[fan_id]

    def change_speed_fan(self, fan_id, value):
        fan = self.get_fan_from_id(fan_id)
        if fan.active:
            fan.value = value
            fan.pwm.ChangeDutyCycle(value)

    def activate_fan(self, fan_id):
        fan = self.get_fan_from_id(fan_id)
        fan.active = True
        fan.pwm.ChangeDutyCycle(fan.value)

    def deactivate_fan(self, fan_id):
        fan = self.get_fan_from_id(fan_id)
        fan.active = False
        fan.pwm.ChangeDutyCycle(0)

    def change_speed_all_fans(self, value):
        for fan in self.fans:
            self.change_speed_fan(fan.id, value)
    
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

    def get_speed_all_fans(self):
        return [fan.value for fan in self.fans]
    
    def get_active_all_fans(self):
        return [fan.active for fan in self.fans]
    
        