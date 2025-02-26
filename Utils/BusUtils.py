import datetime
import Classes.Agency as Agency
import Classes.Stop as Stop
import Classes.Route as Route
import Classes.StopRouteDisplayLine as StopRouteDisplayLine
import Classes.StopDistanceDisplayLine as StopDistanceDisplayLine
import Classes.Trip as Trip
import Classes.Calendar as Calendar
import Classes.BusesData as BusesData
import telebot
from geopy.distance import geodesic as GD

def get_stop_lines(bus_data: BusesData.BusData,stop_id,minutes_interval = 60):
    '''
    Compiling a list of lines that pass in the given stop

    Args:
        bus_data: BusData object
        stop_id: stop id number
        minutes_interval: the time interval
    
    Returns:
        list of lines that will pass in the stop in the next <minutes_interval> minutes.
        the list will be sorted by arrival time in ascending order

    '''
    lines = list()
    for stop_time in bus_data.stop_times:
        if stop_time.stop_id != stop_id: continue

        # handeling time values (could be above 24 hrs, see GTFS documentation)
        hour,minute,seconds = stop_time.arrival_time.split(":")
        if int(hour) >= 24:
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            arrival_time = datetime.datetime(tomorrow.year,tomorrow.month,tomorrow.day,int(hour)-24,int(minute),int(seconds))
        else:
            today = datetime.datetime.now() 
            arrival_time = datetime.datetime(today.year,today.month,today.day,int(hour),int(minute),int(seconds))
        
        # checking is arrival time is within the given time interval
        if 0 < (arrival_time - datetime.datetime.now()).total_seconds()/60 < minutes_interval:
            trip: Trip = next((x for x in bus_data.trips if x.trip_id == stop_time.trip_id),None)
            if trip == None:
                print(f'trip {stop_time.trip_id} not found')
            else:
                route: Route.Route = next((x for x in bus_data.routes if x.id == trip.route_id),None)
                if route == None:
                    print(f'route {trip.route_id} not found')
                else:
                    # checking if the service is running in this day
                    calendar: Calendar.Calendar = next((x for x in bus_data.calendars if x.service_id == trip.service_id),None)
                    if calendar.is_running(datetime.datetime.now()):
                        lines.append(StopRouteDisplayLine.StopRouteDisplayLine(route.id,route.short_name,route.long_name,trip.direction_id,stop_time.arrival_time))

    lines.sort(key=lambda x: x.arrival_time)
    return lines

def get_stop_lines_text(bus_data: BusesData.BusData,stop_code):
    '''
    Preparing text to be displayed for query about stop code

    Args:
        bus_data: BusData object
        stop_code: bus stop code

    Returns:
        Text to be displayed for the given stop code
    '''
    if stop_code.isnumeric():
        stop: Stop = next((x for x in bus_data.stops if x.code == stop_code),None)
        if stop == None:
            return f'stop {stop_code} not found'
        minutes_interval = 60
        stop_lines: list = get_stop_lines(bus_data,stop.id,minutes_interval)
        display_text = ""
        if len(stop_lines) > 0:
            for x in stop_lines:
                display_text += f"\r\n{str(x)}"
        else:
            display_text = "לא נמצאו נתונים"
        return f'{str(stop)}.\r\nקווים שעוברים ב  {minutes_interval} דקות הבאות: {display_text}'
    else:
        return 'מספר תחנה חייב להיות מספר'
    
def get_stops_for_location(bus_data: BusesData.BusData,location: telebot.types.Location,meters_distance):
    '''
    Listing stations close to the given location

    Args:
        bus_data: BusData object
        location: location point
        meters_distance: distance to search with

    Returns:
        List of stops close to the given location
    '''
    stops = list()
    location_value = (location.latitude,location.longitude)
    distance = 0
    for stop in bus_data.stops:
        stop_location_value = (stop.lat,stop.lon)
        distance = GD(location_value,stop_location_value).meters
        if distance <= meters_distance:
            stops.append(StopDistanceDisplayLine.StopDistanceDisplayLine(stop,int(distance)))
    
    stops.sort(key=lambda x: x.distance)
     
    return stops

def get_adjacent_stops_text(bus_data: BusesData.BusData, location):
    '''
    Preparing text to be displayed for a query on a given location

    Args:
        bus_data: BusData object
        location: location point

    Returns:
        Text to be displayed
    '''
    if location == None:
        return "לא סופק מיקום"
    meters_interval = 500
    stops: list = get_stops_for_location(bus_data,location,meters_interval)
    display_text = ""
    if len(stops) > 0:
        for x in stops:
            display_text += f"\r\n{str(x)}"
    else:
        display_text = "no data was found"
    return f'תחנות במרחק של עד {meters_interval} מטרים:{display_text}'

