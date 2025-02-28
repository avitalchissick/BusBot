import urllib.request
import os
import zipfile

# import csv
import datetime

import pandas as pd

from Classes import stop, route, trip, calendar, stop_time

DATA_URL = "https://gtfs.mot.gov.il/gtfsfiles"
MAIN_DATA_FILE_NAME = "israel-public-transportation.zip"


def need_to_get_data_from_server(main_data_file_path):
    """
    Checks if we need to download data from server.

    Args:
        main_data_file_path: data file path

    Returns:
        Boolean value, True when the server has new data or if 24 hours
        have passed since the file was downloaded.

    """
    return (
        datetime.datetime.now()
        - datetime.datetime.fromtimestamp(os.path.getmtime(main_data_file_path))
    ).total_seconds() / 360 > 24
    # does not work ! - produces SSL error
    #    response = requests.head(f'{DATA_URL}/{MAIN_DATA_FILE_NAME}')
    #    url_last_modified = time.mktime(datetime.datetime.strptime
    #                        (response.headers.get('Last-Modified')[:-4], "%a, %d %b %Y %H:%M:%S")
    #                        .timetuple())
    #    local_last_modified = \
    #       datetime.datetime.fromtimestamp(os.path.getmtime(main_data_file_path))
    #    return url_last_modified > local_last_modified


def get_bus_bata_files():
    """
    When needed, gets the data files from the remote server
    """
    local_data_folder = f"{os.getcwd()}/Data"
    if not os.path.isdir(local_data_folder):
        os.mkdir(local_data_folder)

    main_data_file_path = f"{local_data_folder}/{MAIN_DATA_FILE_NAME}"

    if (not os.path.isfile(main_data_file_path)) or need_to_get_data_from_server(
        main_data_file_path
    ):
        urllib.request.urlretrieve(
            f"{DATA_URL}/{MAIN_DATA_FILE_NAME}", main_data_file_path
        )
        with zipfile.ZipFile(main_data_file_path, "r") as zip_ref:
            zip_ref.extractall(local_data_folder)


# def get_stops():
#     """
#     Returns list of stops
#     """
#     stops = []
#     with open("Data/stops.txt", "r", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(f)  # skipping the header line
#         for row in reader:
#             stops.append(
#                 stop.Stop(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
#             )
#     return stops


# def get_routes():
#     """
#     Returns list of routes
#     """
#     routes = []
#     with open("Data/routes.txt", "r", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(f)  # skipping the header line
#         for row in reader:
#             routes.append(route.Route(row[0], row[1], row[2], row[3], row[4], row[5]))
#     return routes


# def get_stop_times():
#     """
#     Returns list of stop times
#     """

#     stop_times = []
#     with open("Data/stop_times.txt", "r", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(f)  # skipping the header line
#         for row in reader:
#             stop_times.append(
#                 stop_time.StopTime(row[0], row[1], row[2], row[3], row[4])
#             )
#     return stop_times


# def get_trips():
#     """
#     Returns list of trips
#     """
#     trips = []
#     with open("Data/trips.txt", "r", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(f)  # skipping the header line
#         for row in reader:
#             trips.append(trip.Trip(row[0], row[1], row[2], row[3], row[4]))
#     return trips


# def get_calendars():
#     """
#     Returns list of calendars
#     """
#     calendars = []
#     with open("Data/calendar.txt", "r", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(f)  # skipping the header line
#         for row in reader:
#             calendars.append(
#                 calendar.Calendar(
#                     row[0],
#                     row[1],
#                     row[2],
#                     row[3],
#                     row[4],
#                     row[5],
#                     row[6],
#                     row[7],
#                     row[8],
#                     row[9],
#                 )
#             )
#     return calendars


def get_stops():
    df = pd.read_csv("Data/stops.txt")
    return [
        stop.Stop(
            x.stop_id,
            x.stop_code,
            x.stop_name,
            x.stop_desc,
            x.stop_lat,
            x.stop_lon,
            x.location_type,
        )
        for x in df.itertuples()
    ]


def get_routes():
    df = pd.read_csv("Data/routes.txt")
    return [
        route.Route(
            x.route_id,
            x.agency_id,
            x.route_short_name,
            x.route_long_name,
            x.route_desc,
            x.route_type,
        )
        for x in df.itertuples()
    ]


def get_stop_times():
    df = pd.read_csv("Data/stop_times.txt")
    return [
        stop_time.StopTime(
            x.trip_id,
            x.arrival_time,
            x.departure_time,
            x.stop_id,
            x.stop_sequence
        )
        for x in df.itertuples()
    ]


def get_trips():
    df = pd.read_csv("Data/trips.txt")
    return [
        trip.Trip(
            x.route_id,
            x.service_id,
            x.trip_id,
            x.trip_headsign,
            x.direction_id
        )
        for x in df.itertuples()
    ]


def get_calendars():
    df = pd.read_csv("Data/calendar.txt")
    return [
        calendar.Calendar(
            x.service_id,
            x.sunday,
            x.monday,
            x.tuesday,
            x.wednesday,
            x.thursday,
            x.friday,
            x.saturday,
            x.start_date,
            x.end_date,
        )
        for x in df.itertuples()
    ]
