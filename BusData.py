import urllib.request
import os
import zipfile
import csv
import Agency
import Stop
import Route
import StopTimes
import Trip
import Calendar

def getBusDataFilesFromServer():
    data_url = "https://gtfs.mot.gov.il/gtfsfiles"
    main_data_file_name = "israel-public-transportation.zip"

    local_data_folder = f"{os.getcwd()}/Data"
    if not os.path.isdir(local_data_folder):
        os.mkdir(local_data_folder)

    main_data_file_path = f"{local_data_folder}/{main_data_file_name}"

    if not os.path.isfile(main_data_file_path):
        urllib.request.urlretrieve( f"{data_url}/{main_data_file_name}",main_data_file_path)
        with zipfile.ZipFile(main_data_file_path, 'r') as zip_ref:
            zip_ref.extractall(local_data_folder)

def getAgencies():
    agencies = []
    with open('Data/agency.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            agencies.append(Agency.Agency(row[0], row[1], row[2]))

    return agencies

def getStops():
    stops = []
    with open('Data/stops.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            stops.append(Stop.Stop(row[0], row[1], row[2],row[3],row[4],row[5],row[6]))
    return stops

def getRoutes():
    routes = []
    with open('Data/routes.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            routes.append(Route.Route(row[0], row[1], row[2],row[3],row[4],row[5]))
    return routes

def getStopTimes():
    stop_times = []
    with open('Data/stop_times.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            stop_times.append(StopTimes.StopTime(row[0], row[1], row[2],row[3],row[4]))
    return stop_times

def getTrips():
    trips = []
    with open('Data/trips.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            trips.append(Trip.Trip(row[0], row[1], row[2],row[3],row[4]))
    return trips

def getCalendars():
    calendars = []
    with open('Data/calendar.txt', 'r',encoding='utf-8') as f:
        reader = csv.reader(f)
        next(f) #skipping the header line
        for row in reader:
            calendars.append(Calendar.Calendar(row[0], row[1], row[2],row[3],row[4],row[5], row[6], row[7],row[8],row[9]))
    return calendars