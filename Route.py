from enum import Enum
class RouteType(Enum):
    LightTrain = 0
    IsraelRailways = 1
    Bus = 3
    CableCar = 5
    Taxi = 8
    FlexibleServiceLine = 715

class Route:
    def __init__(self,id,agency_id,short_name,long_name,desc,type):
        self.id = id
        self.agency_id = agency_id
        self.short_name = short_name
        self.long_name = long_name
        self.desc = desc
        self.type = type