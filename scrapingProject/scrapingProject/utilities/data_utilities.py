from datetime import datetime as DT
from dateutil import parser
import pytz

def normalize_timestamp(datetime, hasTimezone = False, timezone = 'UTC', output_format = '%Y-%m-%d %H:%M:%S'):
    """
    Return a normalized date string with:
    - a standard format: output_format
    - a standard timezone: convert date from "timezone" into utc timezone
    - hasTimezone indicates if the date has or not an indicated timezone (e.g. 2010-03-30T10:21:06+0100)
    """
    
    utc = pytz.timezone('UTC')
    timestamp = parser.parse(datetime)
    if hasTimezone:
        timestamp = timestamp.astimezone(utc)
    else:
        other_tz = pytz.timezone(timezone)
        timestamp = other_tz.localize(timestamp).astimezone(utc)
    return timestamp.strftime(output_format)
    

def compare_time(ts1, ts2):
    '''
    Compare timestamp ts1 and ts2. 
    If ts1 < ts2 then return True; false otherwise.
    ts1 and ts2 format must be parseable by normalize_timestamp 
    (it should parse everything unless the first value is the day)
    '''
    ts1 = normalize_timestamp(ts1)
    ts2 = normalize_timestamp(ts2)
    time1 = DT.strptime(ts1, '%Y-%m-%d %H:%M:%S')
    time2 = DT.strptime(ts2, '%Y-%m-%d %H:%M:%S')
        
    return time1 < time2

def getCurrentDate():
    '''
    Return current date in the format month:day:year
    '''
    return DT.utcnow().strftime("%m:%d:%y")
