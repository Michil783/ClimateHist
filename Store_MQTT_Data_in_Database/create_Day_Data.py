#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------


import json
import sqlite3
import time

# SQLite DB Name
DB_Name =  "IoT.db"

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		self.conn = sqlite3.connect(DB_Name)
		self.conn.execute('pragma foreign_keys = on')
		self.conn.commit()
		self.cur = self.conn.cursor()
		
	def add_del_update_db_record(self, sql_query, args=()):
		self.cur.execute(sql_query, args)
		self.conn.commit()
		return

	def __del__(self):
		self.cur.close()
		self.conn.close()

#===============================================================
# Function to push Sensor Data into Database

# Function to save Temperature to DB Table
def Temp_Data_Handler(topic, jsonData):
	#Parse Data 
	json_Dict = json.loads(jsonData)
	SensorID = topic #json_Dict['Sensor_ID']
	Data_and_Time = int(json_Dict["time"])
	Temperature = float(json_Dict['temperature'])
	HeatIndex = float(json_Dict['heatindex'])
	Dewpoint = float(json_Dict['dewpoint'])
	Humidity = float(json_Dict['humidity'])
	Pressure = float(json_Dict['pressure'])
	Voltage = float(json_Dict['voltage'])
	#Push into DB Table
	dbObj = DatabaseManager()
	dbObj.add_del_update_db_record("insert into Temperature_Data (SensorID, Date_n_Time, Temperature, HeatIndex, Dewpoint, Humidity, Pressure, Voltage) values (?,?,?,?,?,?,?,?)",[SensorID, Data_and_Time, Temperature, HeatIndex, Dewpoint, Humidity, Pressure, Voltage])
	del dbObj
	print "Inserted Temperature Data into Database."
	print ""

def getHistData (sql_query):
	conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/IoT.db')
	curs=conn.cursor()
	curs.execute(sql_query)
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	pres = []
	volt = []
	for row in reversed(data):
		dates.append(int(row[0]))
		temps.append(float(row[1]))
		hums.append(float(row[2]))
		pres.append(float(row[3]))
		volt.append(float(row[4]))
	return dates, temps, hums, pres, volt

def getHistDataSingle (sql_query):
	conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/IoT.db')
	curs=conn.cursor()
	curs.execute(sql_query)
	data = curs.fetchall()
	return data[0][0]

#===============================================================
# Master Function to Select DB Funtion 

#times, temps, hums, pres, volt = getHistData("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage FROM Temperature_Data where SensorID='WeatherNode1' AND Date_n_Time = (select Min(Date_n_Time) from Temperature_Data where SensorID='WeatherNode1')")
#print times
days = int(getHistDataSingle("select julianday('now') - julianday(date((SELECT MIN(Date_n_Time) FROM Temperature_Data where SensorID='WeatherNode1'), 'unixepoch'))"))
print days

i = days
while i > 0:
	date = getHistDataSingle("SELECT date('now', '-"+str(i)+" day')")
	tempmin = getHistDataSingle("SELECT MIN(Temperature) FROM Temperature_Data where SensorID='WeatherNode1' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')")
	tempmax = getHistDataSingle("SELECT MAX(Temperature) FROM Temperature_Data where SensorID='WeatherNode1' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')")
	hummin = getHistDataSingle("SELECT MIN(Humidity) FROM Temperature_Data where SensorID='WeatherNode1' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')")
	hummax = getHistDataSingle("SELECT MAX(Humidity) FROM Temperature_Data where SensorID='WeatherNode1' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')")
	presmin = getHistDataSingle("SELECT MIN(Pressure) FROM Temperature_Data where SensorID='WeatherNode1' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')")
	presmax = getHistDataSingle("SELECT MAX(Pressure) FROM Temperature_Data where SensorID='WeatherNode1' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')")
	if tempmin == None:
		break
	print date, tempmin, tempmax, hummin, hummax, presmin, presmax
	i = i - 1
#===============================================================
