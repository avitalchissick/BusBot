import Utils.DataUtils as DataUtils

class BusData:
    def __init__(self):
        DataUtils.get_bus_bata_files_from_server()
        self.stops = DataUtils.get_stops()
        self.stop_times = DataUtils.get_stop_times()
        self.trips = DataUtils.get_trips()
        self.routes = DataUtils.get_routes()
        self.calendars = DataUtils.get_calendars()

    def get_stops(self):
        return self.stops
    
    def get_stop_times(self):
        return self.stop_times

    def get_routes(self):
        return self.routes

    