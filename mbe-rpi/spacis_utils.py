def pack_sequence(seq):
    # Pack the sequence of integers
    try:
        packed_chars = ''.join(chr(num) for num in seq)
    except TypeError:
        print("EXCEPTION", seq)
        raise
    return packed_chars

def pack_sensor_data(data):
    unziped_data = list(zip(*data))
    packed_data = [pack_sequence(x) for x in unziped_data]
    return packed_data