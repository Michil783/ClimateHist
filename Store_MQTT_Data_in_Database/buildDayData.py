import json
import sqlite3
import time
import datetime

# SQLite DB Name
DB_Name =  "Power.db"


print( "Start inserting into DB" )
conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+ DB_Name)
print( "connection" )
curs = conn.cursor()
print( "cursor" )
loop = True
dayCount = -1
while( loop ):
    print( "dayCount: ", dayCount )
    select = "select * from Power_Data where date(Date_n_time)== date('now','localtime','"+str(dayCount)+" day') ORDER BY Date_n_Time limit 1;"
    print( select )
    firstEntry = curs.execute( select )
    rows = curs.fetchall()
    if( len(rows) ):
        print( "firstEntry: ", firstEntry )
        for row in rows:
            print( row )
            firstEntry_Total = float(row[1])
        select = "select * from Power_Data where date(Date_n_time) == date('now','localtime','"+str(dayCount)+" day') ORDER BY Date_n_Time desc limit 1;"
        print( select )
        lastEntry = curs.execute( select )
        for row in lastEntry:
            print( row )
            lastEntry_Date_n_Time = row[0]
            lastEntry_Total = float(row[1])
        print( "lastEntry Date_n_Time: ", lastEntry_Date_n_Time )
        print( datetime.datetime.strptime(lastEntry_Date_n_Time, "%Y-%m-%dT%H:%M:%S") )
        newDayEntry_date = datetime.datetime.strptime(lastEntry_Date_n_Time, "%Y-%m-%dT%H:%M:%S").date().strftime("%Y-%m-%d")
        newDayEntry_Total = lastEntry_Total
        newDayEntry_Used =  float("{:06.1f}".format(lastEntry_Total - firstEntry_Total))
        print( "newDayEntry_date: ", newDayEntry_date )
        print( "newDayEntrys_Total: ", newDayEntry_Total )
        print( "newDayEntry_Used: ", newDayEntry_Used )
        curs.execute("insert into Power_Data_Day (Date, Total, Used) values (?,?,?)",[newDayEntry_date, newDayEntry_Total, newDayEntry_Used])
        print("new day entry in Power_Data_Day")
        conn.commit()
        print( "commit" )
        dayCount = dayCount - 1
    else:
        loop = False


conn.close()
