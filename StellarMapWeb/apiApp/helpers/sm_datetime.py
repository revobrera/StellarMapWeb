import pytz
from datetime import datetime
from cassandra.util import datetime_from_timestamp

class StellarMapDateTimeHelpers:
    def __init__(self):
        self.__datetime_obj = None
        self.__date_only_str = None

    def get_datetime_obj(self):
        """
        Returns the current date and time in the New York timezone as a datetime object
        """
        return self.__datetime_obj

    def get_date_str(self):
        return self.__date_only_str

    def set_datetime_obj(self):
        # config NY time
        tz_NY = pytz.timezone('America/New_York') 
        datetime_NY = datetime.now(tz_NY)

        # create datetime string
        __date_str = datetime_NY.strftime("%Y-%m-%d %H:%M:%S")
        self.__date_only_str = datetime_NY.strftime("%Y-%m-%d")

        # create datetime object and NOT string
        self.__datetime_obj = datetime.strptime(__date_str, "%Y-%m-%d %H:%M:%S")
        
    datetime_obj = property(get_datetime_obj, set_datetime_obj)

    def set_horizon_datetime_str(self, horizon_datetime_str):
        self.horizon_datetime_str = horizon_datetime_str

    def convert_horizon_datetime_str_to_obj(self):
        # convert a horizon datetime string into a Cassandra DateTime object

        # Convert the string to a datetime object
        dt_obj = datetime.strptime(self.horizon_datetime_str, '%Y-%m-%dT%H:%M:%SZ')

        # Convert the datetime object to a timestamp
        timestamp = dt_obj.timestamp()

        # Convert the timestamp to a Cassandra DateTime object
        cass_dt_obj = datetime_from_timestamp(timestamp)

        return cass_dt_obj
    
    def serialize(self, obj):
        # handle the conversion of Timestamp objects to strings
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif pd.isna(obj):
            return 'NaT'
        return obj
