from datetime import datetime

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
           
    
def compareTime(ts1, ts2):
    '''
    Compare timestamp ts1 and ts2. 
    If ts1 < ts2 then return True; false otherwise.
    ts1 and ts2 format must be:
        
    3/27/2018 4:01:29 PM
    '''
    ts1 = zero_pad_timestamp(ts1)
    ts2 = zero_pad_timestamp(ts2)
    t1 = datetime.strptime(ts1, "%m/%d/%Y %I:%M:%S %p")
    t2 = datetime.strptime(ts2, "%m/%d/%Y %I:%M:%S %p")
        
    if t1 < t2:
        return True
    return False
    