from datetime import datetime, timedelta
import os
import re
import urllib.request
from typing import List


def convert_to_datetime(line):
    """
       Extract timestamp from logline and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)
    """
    timestamp = re.findall(r"\d+\-\d+\-\w+\:\d+\:\d+", line)
    #print('Timestamp extracted is ' + timestamp[0])
    return (datetime.strptime(timestamp[0], "%Y-%m-%dT%H:%M:%S"))

def time_between_shutdowns(loglines):
    """
       Extract shutdown events ("Shutdown initiated") from loglines and
       calculate the timedelta between the first and last one.
       Return this datetime.timedelta object.
    """
    shutdown_event_start = 'Shutdown initiated'

    # Extract all the shutdown event timestamps
    shutdowntimes = []
    for i in range(len(loglines)):
        if (re.search(shutdown_event_start, loglines[i])):
            timestamp = convert_to_datetime(loglines[i])
            shutdowntimes.append(timestamp)
            print(shutdown_event_start + " at " + str(timestamp.date()) + ", " + str(timestamp.time()))

    # Compute the time between the first & last shutdown event timestamps
    deltatime = shutdowntimes[len(shutdowntimes)-1] - shutdowntimes[0]
    return deltatime


# Establish the name of the local logfile
tmp = os.getenv("TMP", "/tmp")
logfile = os.path.join(tmp, 'log')

# Read data from the url into the logfile
urllib.request.urlretrieve(
    'https://bites-data.s3.us-east-2.amazonaws.com/messages.log',
    logfile
)

# Read the local logfile into a list loglines
with open(logfile) as f:
    loglines = f.readlines()

# Extract all the timestamps from the log file
logdatetimes = list(range(len(loglines)))
for i in range(len(loglines)):
    logdatetimes[i] = convert_to_datetime(loglines[i])
    print("Timestamp " + str(i) + " encoded " + str(logdatetimes[i].date()) + " " + str(logdatetimes[i].time()))

shutdowndeltatime = time_between_shutdowns(loglines)

print("Time between shutdowns is (hh:mm:ss)", shutdowndeltatime)