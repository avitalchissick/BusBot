class StopDistanceDisplayLine():
    def __init__(self,stop,distance):
        self.stop = stop
        self.distance = distance

    def __str__(self):
        return f"{self.stop} - {self.distance} מטרים"