import BusData
import datetime
import Trip
import Route
import DisplayLine
import Calendar

class BusMain:
    def __init__(self):
        BusData.getBusDataFilesFromServer()
        self.stops = BusData.getStops()
        self.stop_times = BusData.getStopTimes()
        self.trips = BusData.getTrips()
        self.routes = BusData.getRoutes()
        self.calendars = BusData.getCalendars()

    def get_stops(self):
        return self.stops
    
    def get_stop_times(self):
        return self.stop_times

    def get_routes(self):
        return self.routes

    def get_stop_lines(self,stop_id,minutes_interval = 60):
        lines = list()
        for stop_time in self.stop_times:
            if stop_time.stop_id != stop_id: continue

            # handeling time values (could be above 24 hrs, see GTFS documentation)
            hour,minute,seconds = stop_time.arrival_time.split(":")
            if int(hour) >= 24:
                tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
                arrival_time = datetime.datetime(tomorrow.year,tomorrow.month,tomorrow.day,int(hour)-24,int(minute),int(seconds))
            else:
                today = datetime.datetime.now() 
                arrival_time = datetime.datetime(today.year,today.month,today.day,int(hour),int(minute),int(seconds))
            
            if 0 < (arrival_time - datetime.datetime.now()).total_seconds()/60 < minutes_interval:
                trip: Trip.Trip = next((x for x in self.trips if x.trip_id == stop_time.trip_id),None)
                if trip == None:
                    print(f'trip {stop_time.trip_id} not found')
                else:
                    route: Route.Route = next((x for x in self.routes if x.id == trip.route_id),None)
                    if route == None:
                        print(f'route {trip.route_id} not found')
                    else:
                        # checking if the service is running in this day
                        calendar: Calendar.Calendar = next((x for x in self.calendars if x.service_id == trip.service_id),None)
                        if calendar.is_running(datetime.datetime.now()):
                            lines.append(DisplayLine.DisplayLine(route.id,route.short_name,route.long_name,trip.direction_id,stop_time.arrival_time))

        lines.sort(key=lambda displayLine: displayLine.arrival_time)
        return lines