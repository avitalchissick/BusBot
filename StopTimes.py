class StopTime:
    def __init__(self,trip_id,arrival_time,departure_time,stop_id,stop_sequence):
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence

    def __str__(self):
        return f"{self.trip_id} - {self.arrival_time}"