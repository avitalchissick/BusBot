class DisplayLine:
    def __init__(self,route_id,route_short_name,route_long_name,direction,arrival_time):
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.direction = direction
        self.arrival_time = arrival_time

    def __eq__(self, other):
        return self.route_id == other.route_id and \
                self.route_short_name == other.route_short_name and \
                self.route_long_name == other.route_long_name and \
                self.direction == other.direction and \
                self.arrival_time == other.arrival_time 
    
    def __str__(self):
        return f"{self.route_short_name} - {self.arrival_time}"