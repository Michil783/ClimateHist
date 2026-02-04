# ClimateHist

ClimateHist is the backend infrastructure for the WeatherNodeV4 to build an weatherstation for home use.
The WeatherNodeV4 sensors generating the data and sending it to an MQTT broker. ClimateHist is connected to the broker to receive the data from the sensor and storing it in a SQLite3 DB.

Releated projects in github:

#### WeatherNodeV4
https://github.com/Michil783/WeatherNodeV4

#### weather-forecast
https://github.com/Michil783/weather-forecast

Best way to use this environment is running it on a Raspberry Pi which needs to have installed packes as:

mosquitto MQTT broker
SQLite3 DB
Python3

## Store_MQTT_Data_in_Database
Is the connector from MQTT to SQLite3 DB

## appDHTWebHist
Is a web interface used as a remote interface to SQLite3 DB.
It is using the following Python packages (needed to be installed additionally to Python)

#### Flask
#### MathPlotLib

