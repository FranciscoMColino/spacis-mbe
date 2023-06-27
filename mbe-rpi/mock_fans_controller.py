class MockFan:
    def __init__(self, id):
        self.id = id
        self.active = False
        self.value = 0

class MockFansController:
    def __init__(self):
        pass

    def __init__(self):

        self.fan_ids = [1, 2]

        self.fan1 = MockFan(1)
        self.fan2 = MockFan(2)

        self.fans = [self.fan1, self.fan2]

    def get_fan_from_id(self, fan_id):
        return self.fans[fan_id - 1]

    def change_speed_fan(self, fan_id, value):
        fan = self.get_fan_from_id(fan_id)
        if fan.active:
            fan.value = value

    def activate_fan(self, fan_id):
        fan = self.get_fan_from_id(fan_id)
        fan.active = True

    def deactivate_fan(self, fan_id):
        fan = self.get_fan_from_id(fan_id)
        fan.active = False

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
    
    def get_speed_all_fans(self):
        return [fan.value for fan in self.fans]
    
    def get_active_all_fans(self):
        return [fan.active for fan in self.fans]