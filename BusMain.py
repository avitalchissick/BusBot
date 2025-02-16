import BusData
import datetime
import Stop
import Trip
import Route
import DisplayLine
import Calendar

class BusMain:
    def __init__(self):
        BusData.get_bus_bata_files_from_server()
        self.stops = BusData.get_stops()
        self.stop_times = BusData.get_stop_times()
        self.trips = BusData.get_trips()
        self.routes = BusData.get_routes()
        self.calendars = BusData.get_calendars()

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

    def get_stop_lines_text(self,stop_code):
        if stop_code.isnumeric():
            stop: Stop = next((x for x in self.stops if x.code == stop_code),None)
            if stop == None:
                return f'stop {stop_code} not found'
            else:
                minutes_interval = 60
                stop_lines: list = self.get_stop_lines(stop.id,minutes_interval)
                display_text = ""
                if len(stop_lines) > 0:
                    for x in stop_lines:
                        display_text += f"\r\n{str(x)}"
                else:
                    display_text = "no data was found"
                return f'{str(stop)}.\r\nLines that pass at stop in the next {minutes_interval} minutes: {display_text}'
        else:
            return 'stop code must be numeric. Try again'
        