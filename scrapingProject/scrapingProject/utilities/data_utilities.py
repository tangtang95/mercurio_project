from datetime import datetime
from dateutil import parser
import pytz

#DEPRECATED
def zero_pad_timestamp(timestamp):
    '''
        Given a timestamp in the format
        month/day/year hour:minute:second AM/PM
        add a zero pad where needed to month and hour only.
    '''
    x = timestamp.split(" ")
    x[0] = x[0].split("/")
    x[1] = x[1].split(":")
    i = 0
    for i in range(0,2):
        if int(x[i][0]) < 10 and "0" not in x[i][0]:
            x[i][0] = "0"+x[i][0]   
            
    return ""+x[0][0]+"/"+x[0][1]+"/"+x[0][2]+" "+x[1][0]+":"+x[1][1]+":"+x[1][2]+" "+x[2]



def normalize_timestamp(date, timezone = 'UTC', output_format = '%Y-%m-%d %H:%M:%S'):
    '''
    Return a normalized date string with:
    - a standard format: output_format
    - a standard timezone: UTC
    '''
    other_tz = pytz.timezone(timezone)
    utc = pytz.timezone('UTC')
    timestamp = parser.parse(date)
    timestamp = other_tz.localize(timestamp).astimezone(utc)
    return timestamp.strftime(output_format)
    

def compare_time(ts1, ts2):
    '''
        Compare timestamp ts1 and ts2. 
        If ts1 < ts2 then return True; false otherwise.
        ts1 and ts2 format must be:
            
        3/27/2018 4:01:29 PM

    '''
    ts1 = normalize_timestamp(ts1)
    ts2 = normalize_timestamp(ts2)
    t1 = datetime.strptime(ts1, '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime(ts2, '%Y-%m-%d %H:%M:%S')
        
    if t1 < t2:
        return True
    return False

def getCurrentDate():
    '''
        Return current date in the format month:day:year
    '''
    now = datetime.now()
    return now.strftime("%m:%d:%y")
    

def isAgoFormat(s):
    '''
        Given a string that rapresents a data or in a normal format or in
        something like hour/minute ago
    '''
    x = s.split(" ")
    if x[2] == "ago":
        return True
    return False