import pytz
from datetime import datetime

class StellarMapDateTimeHelpers:
    def __init__(self):
        self.__datetime_obj = None

    def get_datetime_obj(self):
        """
        Returns the current date and time in the New York timezone as a datetime object
        """
        return self.__datetime_obj

    def set_datetime_obj(self):
        # config NY time
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)

        # create datetime string
        date_str = datetime_NY.strftime("%Y-%m-%d %H:%M:%S")

        # create datetime object and NOT string
        self.__datetime_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        
    datetime_obj = property(get_datetime_obj, set_datetime_obj)