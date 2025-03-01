class StopRouteDisplayLine:
    def __init__(
        self,
        route_id,
        route_short_name,
        route_long_name,
        direction,
        planned_arrival_time,
        is_real_time=False,
    ):
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.direction = direction
        self.arrival_time = planned_arrival_time
        self.is_real_time = is_real_time
        self.route_from, self.route_to = route_long_name.split("<->")

    def __str__(self):
        if self.is_real_time:
            return f"<b>{self.arrival_time}</b> - {self.route_short_name} - {self.route_to}"
        else:
            return f"{self.arrival_time} - {self.route_short_name} - {self.route_to}"
