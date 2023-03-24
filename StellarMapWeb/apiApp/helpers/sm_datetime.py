from datetime import datetime

import numpy as np
import pandas as pd
import pytz
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
  
    def convert_to_NY_datetime(self, df, column_name):
        """
        Convert the specified column of pandas dataframe from pandas Timestamps to NY timezone datetimes.

        Args:
            df (pandas.DataFrame): The input dataframe.
            column_name (str): The name of the column to convert to NY timezone datetimes.

        Returns:
            pandas.DataFrame: The modified dataframe with the specified column converted to NY timezone datetimes in the format '%Y-%m-%d %H:%M:%S'.
        """
        # config NY time
        tz_NY = pytz.timezone('America/New_York')

        # convert column of timestamps to datetimes
        # checks the year attribute of the datetime object x to see if it is within the supported range (1-9999), rather than comparing it with a date object.
        # If the year is within the range, it combines the date with a minimum time value to create a datetime object. Otherwise, it returns None.
        df[column_name] = df[column_name].apply(lambda x: datetime.combine(x.date(), datetime.min.time()) if x.year >= 1 and x.year <= 9999 else None)
        
        # Then, the function checks if x is not None and not NaT (pd.isna(x) returns False if x is not NaT). 
        # If x is instance datetime, set the timezone to UTC and then converts it to the NY timezone using the astimezone() method
        df[column_name] = df[column_name].apply(lambda x: x.replace(tzinfo=pytz.utc).astimezone(tz_NY) if isinstance(x, datetime) else None)

        # Filter out NaN
        df = df.dropna(subset=[column_name])

        # Convert datetimes to formatted strings
        df[column_name] = df[column_name].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if x is not None else None)
        
        return df
