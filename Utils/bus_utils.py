import datetime
from os import environ
import json

import requests
import telebot
from geopy.distance import geodesic as gd

from Classes import (
    stop,
    route,
    trip,
    calendar,
    stop_route_display_line,
    stop_distance_display_line,
)
import Classes.buses_data as buses_data


def get_stop_lines(
    bus_data: buses_data.bus_data, stop_id, stop_code, minutes_interval=60
):
    """
    Compiling a list of lines that pass in the given stop in the next minutes interval

    Args:
        bus_data: BusData object
        stop_id: stop id number
        minutes_interval: the time interval

    Returns:
        list of lines that will pass in the stop in the next <minutes_interval> minutes.
        the list will be sorted by arrival time in ascending order

    """
    lines = list()
    for s_time in bus_data.stop_times:
        if s_time.stop_id != stop_id:
            continue

        # handling time values (could be above 24 hrs, see GTFS documentation)
        hour, minute, seconds = s_time.arrival_time.split(":")
        if int(hour) >= 24:
            tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
            arrival_time = datetime.datetime(
                tomorrow.year,
                tomorrow.month,
                tomorrow.day,
                int(hour) - 24,
                int(minute),
                int(seconds),
            )
        else:
            today = datetime.datetime.now()
            arrival_time = datetime.datetime(
                today.year, today.month, today.day, int(hour), int(minute), int(seconds)
            )

        # checking is arrival time is within the given time interval
        if (
            0
            < (arrival_time - datetime.datetime.now()).total_seconds() / 60
            < minutes_interval
        ):
            bus_trip: trip.Trip = next(
                (x for x in bus_data.trips if x.trip_id == s_time.trip_id), None
            )
            if bus_trip is None:
                print(f"trip {s_time.trip_id} not found")
            else:
                bus_route: route.Route = next(
                    (x for x in bus_data.routes if x.id == bus_trip.route_id), None
                )
                if route is None:
                    print(f"route {bus_trip.route_id} not found")
                else:
                    # checking if the service is running in this day
                    bus_calendar: calendar.Calendar = next(
                        (
                            x
                            for x in bus_data.calendars
                            if x.service_id == bus_trip.service_id
                        ),
                        None,
                    )
                    if bus_calendar.is_running(datetime.datetime.now()):
                        is_real_time = False
                        arrival_time = s_time.arrival_time

                        exp_arrival_time = get_real_time_arrival_time(
                                    int(stop_code), bus_trip.route_id)
                        if exp_arrival_time is not None:
                            arrival_time = exp_arrival_time
                            is_real_time = True

                        lines.append(
                            stop_route_display_line.StopRouteDisplayLine(
                                bus_route.id,
                                bus_route.short_name,
                                bus_route.long_name,
                                bus_trip.direction_id,
                                s_time.arrival_time,
                                is_real_time
                            )
                        )

    lines.sort(key=lambda x: x.arrival_time)
    return lines


def get_real_time_arrival_time(stop_code, route_id):
    """
    Getting real time expected time of arrival for bus at stop

    Args:
        stop_id: bus stop id
        route_id: bus route id

        Returns:
            If bus hasn't started the route yet then None is returned.
            Else date-time value of expected real-time arrival.
    """

    mot_base_url = environ["MOT_BASE_URL"]

    params = dict(MonitoringRef=stop_code, LineRef=route_id)

    data = requests.get(url=mot_base_url, params=params, timeout=120)
    output = json.loads(data.content)

    if (
        output["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["Status"]
        == "true"
    ):
        # example - 2025-02-28T23:33:00+02:00
        exp_arrival_time: str = output["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"][0]["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]
        idx1 = exp_arrival_time.index("T") + 1
        idx2 = exp_arrival_time.index("+")

        return exp_arrival_time[idx1:idx2]

    return None


def get_stop_lines_text(bus_data: buses_data.bus_data, stop_code):
    """
    Preparing text to be displayed for query about stop code

    Args:
        bus_data: BusData object
        stop_code: bus stop code

    Returns:
        Text to be displayed for the given stop code
    """
    if stop_code.isnumeric():
        bus_stop: stop.Stop = next(
            (x for x in bus_data.stops if x.code == int(stop_code)), None
        )
        if bus_stop is None:
            return f"תחנה {stop_code} לא נמצאה בנתונים"
        minutes_interval = 60
        stop_lines: list = get_stop_lines(
            bus_data, bus_stop.id, stop_code, minutes_interval
        )
        display_text = ""
        if len(stop_lines) > 0:
            for x in stop_lines:
                display_text += f"\r\n{str(x)}"
        else:
            display_text = "לא נמצאו נתונים"
        return f"{str(bus_stop)}.\r\nקווים שעוברים ב  {minutes_interval} דקות הבאות: {display_text}"
    else:
        return "מספר תחנה חייב להיות מספר"


def get_stops_for_location(
    bus_data: buses_data.bus_data, location: telebot.types.Location, meters_distance
):
    """
    Listing stations close to the given location

    Args:
        bus_data: BusData object
        location: location point
        meters_distance: distance to search with

    Returns:
        List of stops close to the given location
    """
    stops = list()
    location_value = (location.latitude, location.longitude)
    for bus_stop in bus_data.stops:
        stop_location_value = (bus_stop.lat, bus_stop.lon)
        distance = gd(location_value, stop_location_value).meters
        if distance <= meters_distance:
            stops.append(
                stop_distance_display_line.StopDistanceDisplayLine(
                    bus_stop, int(distance)
                )
            )

    stops.sort(key=lambda x: x.distance)

    return stops


def get_adjacent_stops_text(bus_data: buses_data.bus_data, location):
    """
    Preparing text to be displayed for a query on a given location

    Args:
        bus_data: BusData object
        location: location point

    Returns:
        Text to be displayed
    """
    if location is None:
        return "לא סופק מיקום"
    meters_interval = 500
    stops: list = get_stops_for_location(bus_data, location, meters_interval)
    display_text = ""
    if len(stops) > 0:
        for x in stops:
            display_text += f"\r\n{str(x)}"
    else:
        display_text = "no data was found"
    return f"תחנות במרחק של עד {meters_interval} מטרים:{display_text}"
