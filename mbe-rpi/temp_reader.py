import random as rnd

import smbus

bus = smbus.SMBus(1)
ADDRESS = 0x49 # TODO can this change? how to get the address?

def read_temperature(self):
    data = bus.read_byte_data(ADDRESS, 0)
    temp = ((data[0] << 8) | data[1]) >> 4
    temp = temp * 0.0625
    return temp

def mock_read_temperature(self):
    return rnd.randint(0, 100)