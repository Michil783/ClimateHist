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
import datetime
import logging
import logging.config
import logging.handlers
import os
# SQLite DB Name
DB_Name =  "IoTv2.db"

# logging
path = os.path.dirname(os.path.realpath(__file__))
#logging.basicConfig(filename='mqtt_listen_sensor_data.log', encoding='utf-8', level=logging.INFO)
logging.config.fileConfig(path+"/mqtt_listen_sensor_data.conf")

#===============================================================
# Database Manager Class

class DatabaseManager():
	def __init__(self):
		global lastMonth
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
	logging.info( "Temp_data_Handler()" )
	try:
		#Parse Data 
		json_Dict = json.loads(jsonData)
		logging.info( json_Dict )
		SensorID = topic #json_Dict['Sensor_ID']
		logging.info( "SensorID: %s", topic )
		Date_and_Time = int(json_Dict["time"])
		logging.info( "Date_and_Time: %s", Date_and_Time )
		if json_Dict['temperature'] == "" or json_Dict['temperature'] == "nan":
			logging.info( "no temperatur in data" )
			return
		Temperature = float(json_Dict['temperature'])
		logging.info( "Temperatur: %f", Temperature )
		if json_Dict['heatindex'] == "" or json_Dict['heatindex'] == "nan":
			logging.info( "no heatindex in data" )
			return
		HeatIndex = float(json_Dict['heatindex'])
		logging.info( "HeatIndex: %f", HeatIndex )
		if json_Dict['dewpoint'] == "" or json_Dict['dewpoint'] == "nan":
			logging.info( "no dewpoint in data" )
			return
		Dewpoint = float(json_Dict['dewpoint'])
		logging.info( "Dewpoint: %f", Dewpoint )
		if json_Dict['humidity'] == "" or json_Dict['humidity'] == "nan":
			logging.info( "no humidity in data" )
			return
		Humidity = float(json_Dict['humidity'])
		logging.info( "Humidity: %f", Humidity )
		if json_Dict['pressure'] == "" or json_Dict['pressure'] == "nan":
			logging.info( "no pressure in data" )
			return
		Pressure = float(json_Dict['pressure'])
		logging.info( "Pressure: %f", Pressure )
		if json_Dict['voltage'] == "" or json_Dict['voltage'] == "nan":
			logging.info( "no voltage in data" )
			return
		Voltage = float(json_Dict['voltage'])
		logging.info( "Voltage: %f", Voltage )
		if json_Dict['charging'] == "" or json_Dict['charging'] == "nan":
			logging.info( "no charging state in data" )
			return
		Charging = bool(json_Dict['charging'].lower() in ['true'])
		logging.info("JSON charging: %s", json_Dict['charging'])
		logging.info("Charging: %d", Charging)
		if json_Dict['soc'] == "" or json_Dict['soc'] == "nan":
			logging.info( "no State of Charging in data" )
			return
		SoC = float(json_Dict['soc'])
		logging.info("SoC: %f", SoC)
		
		if Date_and_Time < 28900 or Date_and_Time > int(time.time()):
			logging.info( "wrong time in data" )
			Date_and_Time = datetime.datetime.now #+ (7 * 3600)
			logging.info( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(Date_and_Time))) #-(7 * 3600))) )
		logging.info( "Date_and_Time: %s", Date_and_Time )

	except:
		logging.info( "Unexpected error:")
		logging.info( sys.exc_info()[0] )
		
	#Push into DB Table
	#dbObj = DatabaseManager()
	#dbObj.add_del_update_db_record("insert into Temperature_Data (SensorID, Date_n_Time, Temperature, HeatIndex, Dewpoint, Humidity, Pressure, Voltage) values (?,?,?,?,?,?,?,?)",[SensorID, Data_and_Time, Temperature, HeatIndex, Dewpoint, Humidity, Pressure, Voltage])
	#del dbObj
	#conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/IoT.db', 1.0)
	#curs=conn.cursor()
	#logging.info( "before: " )
	#logging.info( curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+SensorID+"'")[0] )
	#conn.close()

	try:
		logging.info( "Start inserting into DB" )
		conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+ DB_Name)
		logging.info( "connection" )
		curs = conn.cursor()
		logging.info( "cursor" )
		curs.execute("insert into Temperature_Data (SensorID, Date_n_Time, Temperature, HeatIndex, Dewpoint, Humidity, Pressure, Voltage, Charging, SoC) values (?,?,?,?,?,?,?,?,?,?)",[SensorID, Date_and_Time, Temperature, HeatIndex, Dewpoint, Humidity, Pressure, Voltage, Charging, SoC])
		logging.info( "Execute" )
		conn.commit()
		logging.info( "commit" )
		conn.close()
		logging.info( "inserted" )
		logging.info( "Inserted Temperature Data into Database." )

	except:
		logging.info( "Unexpected error:")
		logging.info( sys.exc_info()[0] )

	#conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/IoT.db', 1.0)
	#logging.info( "after: " )
	#logging.info( curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+SensorID+"'")[0] )
	#conn.close()


#===============================================================
# Master Function to Select DB Funtion based on MQTT Topic

def sensor_Data_Handler(Topic, jsonData):
	logging.info( "sensor_Data_Handler" )
	Temp_Data_Handler(Topic, jsonData)

#===============================================================
