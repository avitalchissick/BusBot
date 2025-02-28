from Utils import data_utils


class bus_data:
    def __init__(self):
        data_utils.get_bus_bata_files()
        self.stops = data_utils.get_stops()
        self.stop_times = data_utils.get_stop_times()
        self.trips = data_utils.get_trips()
        self.routes = data_utils.get_routes()
        self.calendars = data_utils.get_calendars()

    def get_stops(self):
        return self.stops

    def get_stop_times(self):
        return self.stop_times

    def get_routes(self):
        return self.routes
