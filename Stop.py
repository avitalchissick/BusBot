from enum import Enum

class LocationType(Enum):
    Regular = 0
    Centralstop = 1

class Stop:
    def __init__(self,id,code,name,desc,lat,lon,location_type):
        self.id = id
        self.code = code
        self.name = name
        self.desc = desc
        self.lat = lat
        self.lon = lon
        self.location_type = location_type

    def __str__(self):
        return f"{self.code} - {self.name} - {self.desc}"