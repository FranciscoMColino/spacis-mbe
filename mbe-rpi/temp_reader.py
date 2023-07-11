import random as rnd

import smbus

bus = smbus.SMBus(1)
ADDRESS = 0x49  # TODO can this change? how to get the address?

factor_0 = 1.9792
factor_1 = 0.0164


def read_temperature():
    data = bus.read_i2c_block_data(ADDRESS, 0x00, 2)
    # temp = ((data[0] << 8) | data[1]) >> 4
    # temp = temp * 0.0625
    return data[0] * factor_0 + data[1] * factor_1


def mock_read_temperature():
    return rnd.randint(0, 100)
