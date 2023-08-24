import datetime

# TODO Move to config file
BASE_DIR = './records/'
SENSOR_RECORD_SUFFIX = 'sensor_records'
TEMPERATURE_RECORD_SUFFIX = 'temperature_records'
GPS_RECORD_SUFFIX = 'gps_records'
PPS_RECORD_SUFFIX = 'pps_records'

class DataRecorder:
    def __init__(self):
        # filename given by current timestamp
        self.time_stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

        self.sensor_record_path = BASE_DIR + '/' + SENSOR_RECORD_SUFFIX + '/' + SENSOR_RECORD_SUFFIX + self.time_stamp + '.csv'
        self.temperature_record_path = BASE_DIR + '/' + TEMPERATURE_RECORD_SUFFIX + '/' + TEMPERATURE_RECORD_SUFFIX + self.time_stamp + '.csv'
        self.gps_record_path = BASE_DIR + '/' + GPS_RECORD_SUFFIX + '/' + GPS_RECORD_SUFFIX + self.time_stamp + '.csv'
        self.pps_record_path = BASE_DIR + '/' + PPS_RECORD_SUFFIX + '/' + PPS_RECORD_SUFFIX + self.time_stamp + '.csv'

        self.setup_sensor_record()
        self.setup_temperature_record()
        self.setup_gps_record()
        self.setup_pps_record()

    def setup_sensor_record(self):
        self.sensor_record_file = open(self.sensor_record_path, 'a')
        self.sensor_record_file.write('sensor_1,sensor_2,sensor_3,sensor_4,delay\n')
        self.sensor_record_file.flush()

    def setup_temperature_record(self):
        self.temperature_record_file = open(self.temperature_record_path, 'a')
        self.temperature_record_file.write('box_temp,cpu_temp,time\n')
        self.temperature_record_file.flush()

    def setup_gps_record(self):
        self.gps_record_file = open(self.gps_record_path, 'a')
        self.gps_record_file.write('lat,lon,alt,speed,climb,track,time,error\n')
        self.gps_record_file.flush()

    def setup_pps_record(self):
        self.pps_record_file = open(self.pps_record_path, 'a')
        self.pps_record_file.write('id, time\n')
        self.pps_record_file.flush()

    def record_sensor_data(self, data):
        transformed_data = [str(x) for x in data]
        self.sensor_record_file.write(','.join(transformed_data) + '\n')
        self.sensor_record_file.flush()

    def record_multiple_sensor_data(self, data):
        for i in range(len(data)):
            self.record_sensor_data(data[i])

    def record_gps_data(self, data):
        transformed_data = [str(x) for x in data]
        self.gps_record_file.write(','.join(transformed_data) + '\n')
        self.gps_record_file.flush()

    def record_pps_data(self, data):
        transformed_data = [str(x) for x in data]
        self.pps_record_file.write(','.join(transformed_data) + '\n')
        self.pps_record_file.flush()

    def record_multiple_pps_data(self, data):
        for i in range(len(data)):
            self.record_pps_data(data[i])

    def record_temperature_data(self, data):
        transformed_data = [str(round(x, 2)) for x in data]
        current_time = datetime.datetime.now()
        transformed_data.append(current_time.strftime("%H-%M-%S")+ f".{current_time.microsecond // 1000:03d}")
        self.temperature_record_file.write(','.join(transformed_data) + '\n')
        self.temperature_record_file.flush()