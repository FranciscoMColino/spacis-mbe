import asyncio

from gps import *

GPS_STATUS_WAIT_TIME = 5

class GpsController:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

    def get_position_data(self):
        nx = self.gpsd.next()
        if nx['class'] == 'TPV':
            self.lat = getattr(nx,'lat', "Unknown")
            self.lon = getattr(nx,'lon', "Unknown")
        print("LOG: GPS coords: lat = " + str(self.lat) + ", lon = " + str(self.lon))

    def get_gps_status(self):
        return {"lat": self.lat, "lon": self.lon}

    async def periodic_read_gps_coords(self):
        while True:
            if self.gpsd.waiting():
                self.get_position_data()
            await asyncio.sleep(GPS_STATUS_WAIT_TIME)