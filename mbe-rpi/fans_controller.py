import RPi.GPIO as GPIO

FAN1_PIN = 18
FAN2_PIN = 23

FAN_CONTROL_FREQ = 1000

class Fan:
    def __init__(self, id, pwm):
        self.id = 0
        self.active = False
        self.value = 0
        self.pwm = pwm

class FansController:

    def __init__(self):

        self.fan_ids = [1, 2]

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(FAN1_PIN, GPIO.OUT)
        GPIO.setup(FAN2_PIN, GPIO.OUT)

        self.fan1 = Fan(1, GPIO.PWM(FAN1_PIN, FAN_CONTROL_FREQ))
        self.fan2 = Fan(2, GPIO.PWM(FAN2_PIN, FAN_CONTROL_FREQ))

        self.fans = [self.fan1, self.fan2]

        self.fan1.pwm.start(0)
        self.fan2.pwm.start(0)

    def get_fan_from_id(self, fan_id):
        return self.fans[fan_id - 1]

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
        for fan in self.fans:
            self.activate_fan(fan.id)

    def deactivate_all_fans(self):
        for fan in self.fans:
            self.deactivate_fan(fan.id)
    
    def all_fans_active(self):
        for fan in self.fans:
            if not fan.active:
                return False
        return True


    
        