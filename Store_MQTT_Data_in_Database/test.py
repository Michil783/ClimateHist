import json
import sqlite3
import time
import datetime

# SQLite DB Name
DB_Name =  "Power.db"

Date_n_Time = "2025-05-08T15:52:41"
newDay = False

datetime_obj = datetime.datetime.strptime(Date_n_Time, "%Y-%m-%dT%H:%M:%S") 
time = datetime_obj.time()
print( time )
print( time.hour )
if( time.hour < 1 and not newDay ):
    print( "Start inserting into day data" )
elif( time.hour > 2 and newDay ):
    print( "now it's after 2 and no new day" )
    newDay = False
else:
    print( "not a new day" )
