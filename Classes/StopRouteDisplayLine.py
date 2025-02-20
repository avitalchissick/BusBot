class StopRouteDisplayLine:
    def __init__(self,route_id,route_short_name,route_long_name,direction,arrival_time):
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.direction = direction
        self.arrival_time = arrival_time
        self.route_from,self.route_to = route_long_name.split('<->')

    def __str__(self):
        return f"{self.arrival_time} - {self.route_short_name} - {self.route_to}"
    