import asyncio

from gps import *

GPS_STATUS_WAIT_TIME = 1/2

class GpsController:
    def __init__(self, data_record):
        self.data_record = data_record
        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.speed = 0
        self.climb = 0
        self.track = 0
        self.time = 0
        self.error = 0
        self.satellites = []
        self.gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

    def get_position_data(self):
        nx = self.gpsd.next()
        if nx['class'] == 'TPV':
            self.lat = getattr(nx, 'lat', "Unknown")
            self.lon = getattr(nx, 'lon', "Unknown")
            self.alt = getattr(nx, 'alt', "Unknown")
            self.speed = getattr(nx, 'speed', "Unknown")
            self.climb = getattr(nx, 'climb', "Unknown")
            self.track = getattr(nx, 'track', "Unknown")
            self.time = getattr(nx, 'time', "Unknown")
            self.error = getattr(nx, 'error', "Unknown")
            self.satellites = getattr(nx, 'satellites', [])
        # print("LOG: GPS data {}".format(self.time))

    def get_gps_status(self):
        return {
            "lat": self.lat, 
            "lon": self.lon,
            "alt": self.alt,
            "speed": self.speed,
            "climb": self.climb,
            "track": self.track,
            "time": self.time,
            "error": self.error,
            "satellites": self.satellites
            }

    async def periodic_read_gps_coords(self):
        while True:
            if self.gpsd.waiting():
                self.get_position_data()
                self.data_record.record_gps_data([
                    self.lat, self.lon, self.alt, self.speed, self.climb, self.track, self.time, self.error
                ])
            await asyncio.sleep(GPS_STATUS_WAIT_TIME)