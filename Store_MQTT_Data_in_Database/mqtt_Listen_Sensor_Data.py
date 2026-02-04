#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------

import paho.mqtt.client as mqtt
import logging
import logging.config
import logging.handlers
from store_Sensor_Data_to_DB import sensor_Data_Handler
from store_Power_Data_to_DB import power_Data_Handler
import os

# logging
path = os.path.dirname(os.path.realpath(__file__))
#logging.basicConfig(filename='mqtt_listen_sensor_data.log', encoding='utf-8', level=logging.INFO)
logging.config.fileConfig(path+"/mqtt_listen_sensor_data.conf")

# MQTT Settings 
MQTT_Broker = "hap-nodejs"
MQTT_Port = 1883
Keep_Alive_Interval = 45
#MQTT_Topic = "Home/BedRoom/#"
TASMOTA_TOPIC = "tele/tasmota_BE5B10/SENSOR"
TASMOTA_TOPIC_ALT = "tasmota/discovery/E8DB84BE5B10/sensors"
TASMOTA_TOPIC_NEW = "tele/CTS_tasmota_SML_C18A90/SENSOR"
TASMOTA_TOPIC_NEW_ALT = "tasmota/discovery/28372FC18A90/sensors"

#Subscribe to all Sensors at Base Topic
def on_connect(mosq, obj, flags, rc):
	logging.info( "on_connect" )
	mqttc.subscribe("WeatherNode1", 0)
	mqttc.subscribe("WeatherNode2", 0)
	mqttc.subscribe("WeatherNode3", 0)
	mqttc.subscribe(TASMOTA_TOPIC, 0)
	#mqttc.subscribe(TASMOTA_TOPIC_ALT, 0)
	mqttc.subscribe(TASMOTA_TOPIC_NEW, 0)
	#mqttc.subscribe(TASMOTA_TOPIC_NEW_ALT, 0)

#Save Data into DB Table
def on_message(mosq, obj, msg):
	# This is the Master Call for saving MQTT Data into DB
	# For details of "sensor_Data_Handler" function please refer "sensor_data_to_db.py"
	logging.info( "-------" )
	logging.info( "MQTT Data Received..." )
	logging.info( "MQTT Topic: " + msg.topic )
	#print( "Data: " + msg.payload )
	if( msg.topic == TASMOTA_TOPIC or msg.topic == TASMOTA_TOPIC_ALT or msg.topic == TASMOTA_TOPIC_NEW ):
		power_Data_Handler(msg.topic, msg.payload)
	else:
		sensor_Data_Handler(msg.topic, msg.payload)

def on_subscribe(mqttc, obj, mid, reason_code_list):
	print("Subscribed: " + str(mid) + " " + str(reason_code_list))

logging.info( "start creating mqtt client" )
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect
logging.info( "connect to broker" )
mqttc.connect(MQTT_Broker, MQTT_Port) #, int(Keep_Alive_Interval))

# Continue the network loop
logging.info( "loop forever" )
mqttc.loop_forever()
