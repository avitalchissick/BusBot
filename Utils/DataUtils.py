import urllib.request
import os
import zipfile
import csv
import Classes.Agency as Agency
import Classes.Stop as Stop
import Classes.Route as Route
import Classes.StopTime as StopTime
import Classes.Trip as Trip
import Classes.Calendar as Calendar
import datetime
import pandas as pd

data_url = "https://gtfs.mot.gov.il/gtfsfiles"
main_data_file_name = "israel-public-transportation.zip"

def server_has_new_data(main_data_file_path):
    return (datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(main_data_file_path))).total_seconds()/360 > 24
# does not work ! - produces SSL error
#    response = requests.head(f'{data_url}/{main_data_file_name}')
#    url_last_modified = time.mktime(datetime.datetime.strptime(response.headers.get('Last-Modified')[:-4], "%a, %d %b %Y %H:%M:%S").timetuple()) 
#    local_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(main_data_file_path))
#    return url_last_modified > local_last_modified

def get_bus_bata_files_from_server():
    local_data_folder = f"{os.getcwd()}/Data"
    if not os.path.isdir(local_data_folder):
        os.mkdir(local_data_folder)

    main_data_file_path = f"{local_data_folder}/{main_data_file_name}"

    if (not os.path.isfile(main_data_file_path)) or server_has_new_data(main_data_file_path):
        urllib.request.urlretrieve( f"{data_url}/{main_data_file_name}",main_data_file_path)
        with zipfile.ZipFile(main_data_file_path, 'r') as zip_ref:
            zip_ref.extractall(local_data_folder)

def get_agencies():
    agencies = []
    with open('Data/agency.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            agencies.append(Agency.Agency(row[0], row[1], row[2]))

    return agencies

def get_stops():
    stops = []
    with open('Data/stops.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            stops.append(Stop.Stop(row[0], row[1], row[2],row[3],row[4],row[5],row[6]))
    return stops

def get_routes():
    routes = []
    with open('Data/routes.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            routes.append(Route.Route(row[0], row[1], row[2],row[3],row[4],row[5]))
    return routes

def get_stop_times():
    stop_times = []
    with open('Data/stop_times.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            stop_times.append(StopTime.StopTime(row[0], row[1], row[2],row[3],row[4]))
    return stop_times

def get_trips():
    trips = []
    with open('Data/trips.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            trips.append(Trip.Trip(row[0], row[1], row[2],row[3],row[4]))
    return trips

def get_calendars():
    calendars = []
    with open('Data/calendar.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            calendars.append(Calendar.Calendar(row[0], row[1], row[2],row[3],row[4],row[5], row[6], row[7],row[8],row[9]))
    return calendars

# with pandas it loads slower
# def get_stops():
#     df = pd.read_csv('Data/stops.txt')
#     return [Stop.Stop(x.stop_id,x.stop_code,x.stop_name,x.stop_desc,x.stop_lat,x.stop_lon,x.location_type) for x in df.itertuples()]

# def get_routes():
#     df = pd.read_csv('Data/routes.txt')
#     return [Route.Route(x.route_id,x.agency_id,x.route_short_name,x.route_long_name,x.route_desc,x.route_type) for x in df.itertuples()]

# def get_stop_times():
#     df = pd.read_csv('Data/stop_times.txt')
#     return [StopTime.StopTime(x.trip_id,x.arrival_time,x.departure_time,x.stop_id,x.stop_sequence) for x in df.itertuples()]

# def get_trips():
#     df = pd.read_csv('Data/trips.txt')
#     return [Trip.Trip(x.route_id,x.service_id,x.trip_id,x.trip_headsign,x.direction_id) for x in df.itertuples()]

# def get_calendars():
#     df = pd.read_csv('Data/calendar.txt')
#     return [Calendar.Calendar(x.service_id,x.sunday,x.monday,x.tuesday,x.wednesday,x.thursday,x.friday,x.saturday,x.start_date,x.end_date) for x in df.itertuples()]
