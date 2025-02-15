import datetime

class Calendar:
    def __init__(self,service_id,monday,tuesday,wednsday,thursday,friday,saturday,sunday,start_date,end_date):
        self.service_id = service_id
        self.monday = monday
        self.tuesday = tuesday
        self.wednsday = wednsday
        self.thursday = thursday
        self.friday = friday 
        self.saturday = saturday
        self.sunday = sunday
        self.start_date = start_date
        self.end_date = end_date

    def is_running(self,date_to_check :datetime):
        day_of_week = date_to_check.weekday()
        s_date: datetime.date = datetime.datetime.strptime(self.start_date,"%Y%m%d")
        e_date: datetime.date = datetime.datetime.strptime(self.end_date,"%Y%m%d")
        if s_date < date_to_check < e_date:
            if day_of_week == 0 and self.monday == '1' or \
               day_of_week == 1 and self.tuesday == '1' or \
               day_of_week == 2 and self.wednsday == '1' or \
               day_of_week == 3 and self.thursday == '1' or \
               day_of_week == 4 and self.friday == '1' or \
               day_of_week == 5 and self.saturday == '1' or \
               day_of_week == 6 and self.sunday == '1' :
                    return True
        
        return False