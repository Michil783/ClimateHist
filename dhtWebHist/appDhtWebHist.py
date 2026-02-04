#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  appDhtWebServer.py
#
#  based on MJRoBot.org 10Jan18
# enhancements and changes by
# Michael Leopoldseder dec. 2019

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import io
import time

from flask import Flask, render_template, send_file, make_response, request, jsonify
app = Flask(__name__)

import sqlite3
import json

DB_Name = "IoTv2.db"
Power_DB_Name = "Power.db"

# Retrieve LAST data from database
def getLastData(source):
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+DB_Name)
    curs=conn.cursor()
    for row in curs.execute("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage, Charging, SoC FROM Temperature_Data where SensorID='"+source+"' ORDER BY Date_n_Time DESC LIMIT 1"):
        myTime = time.ctime(int(row[0])) #-(8 * 3600))
        temp = float(row[1])
        hum = float(row[2])
        pres = float(row[3])
        volt = float(row[4])
        charging = bool(row[5])
        soc = float(row[6])
        #print( row[0])
        print( myTime )
    conn.close()
    return myTime, temp, hum, pres, volt, charging, soc

def getLastDataFull(source):
    print("getLastDataFull(",source,")")
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+DB_Name)
    curs=conn.cursor()
    for row in curs.execute("SELECT Date_n_Time, Temperature, HeatIndex, Humidity, Pressure, Voltage, Charging, SoC FROM Temperature_Data where SensorID='"+source+"' ORDER BY Date_n_Time DESC LIMIT 1"):
        print( row )
        #myTime = time.ctime(int(row[0]))
        t1 = time.localtime(int(row[0]))
        print(time.strftime("%d.%m.%Y %H:%M:%S", t1))
        myTime = time.strftime("%d.%m.%Y %H:%M:%S", t1)
        temp = float(row[1])
        heat = float(row[2])
        hum = float(row[3])
        pres = float(row[4])
        volt = float(row[5])
        charging = bool(row[6])
        soc = float(row[7])
        #print( row[0])
        print( myTime )
        print( "charging: ", row[6], charging )
    conn.close()
    return myTime, temp, heat, hum, pres, volt, charging, soc

#def getHistData (source, numSamples):
#	conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/IoT.db')
#	curs=conn.cursor()
#	curs.execute("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage FROM Temperature_Data where SensorID='"+source+"' ORDER BY Date_n_Time DESC LIMIT "+str(numSamples))
#	data = curs.fetchall()
#	dates = []
#	temps = []
#	hums = []
#	pres = []
#	volt = []
#	for row in reversed(data):
#		dates.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(row[0])-(8 * 3600))))
#		temps.append(float(row[1]))
#		hums.append(float(row[2]))
#		pres.append(float(row[3]))
#		volt.append(float(row[4]))
#	conn.close()
#	return dates, temps, hums, pres, volt

def getHistData (source, days):
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+DB_Name)
    curs=conn.cursor()
    if days == 0 :
        print( " fetch all data for sensor "+source )
        #for row in curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+source+"'"):
        #    numSamples=row[0]
        #    print( "numSamples: ", numSamples )
        curs.execute("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage, Charging, SoC FROM Temperature_Data where SensorID='"+source+"' ORDER BY Date_n_Time")
    elif days == 28:
        print( "fetch data for last month for sensor "+source)
        #for row in curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-1 month')"):
        #    numSamples=row[0]
        curs.execute("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage, Charging, SoC FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-1 month') ORDER BY Date_n_Time")
        #    print( "numSamples: ", numSamples )
    elif days == 84:
        print( "fetch data for 3 month for sensor "+source)
        #for row in curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-3 month')"):
        #    print( "{}".format(row) )
        #    numSamples=row[0]
        #    print( "numSamples: ", numSamples )
        curs.execute("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage, Charging, SoC FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-3 month') ORDER BY Date_n_Time")
    else:
        print( "fetch data for "+str(days)+" days for sensor "+source)
        #for row in curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-"+str(days - 1)+" day')"):
        #    numSamples=row[0]
        #curs.execute("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-"+str(days - 1)+" day') ORDER BY Date_n_Time")
        #print( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( time.today() ) ) )
        #for row in curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+source+"' AND julianday(date(Date_n_Time-(7*3600), 'unixepoch')) >= julianday(date('now', '-"+str(days - 1)+" days'))"):
        #    numSamples=row[0]
        curs.execute("SELECT Date_n_Time, Temperature, Humidity, Pressure, Voltage, Charging, SoC FROM Temperature_Data where SensorID='"+source+"' AND julianday(date(Date_n_Time, 'unixepoch')) >= julianday(date('now', '-"+str(days - 1)+" days')) ORDER BY Date_n_Time")
    
    print( "before curs.fetchall()" )
    data = curs.fetchall()
    numSamples = len(data)
    print( "len(data): ", len(data) )
    times = []
    temps = []
    hums = []
    pres = []
    volt = []
    charging = []
    soc = []
    #for row in data: #reversed(data):
    i = 0
    while i < numSamples: #reversed(data):
        row = data[i]
        print( "row: ", row)
        if i > 0:
            if row[0] > data[i-1][0] + 15 * 60:
                #print( " ---- ", row[0] - data[i-1][0], (row[0]-data[i-1][0]) / (15*60), int( (row[0]-data[i-1][0]) / (15*60) ) )
                empty = int( (row[0]-data[i-1][0]) / (15*60) )
                emptyTime = data[i-1][0]
                while empty > 0:
                    #print( " ---- " )
                    emptyTime = emptyTime + (15 * 60)
                    #times.append( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( int( emptyTime )-(8 * 3600) ) ) )
                    times.append( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( int( emptyTime ) ) ) )
                    temps.append(float('NaN'))
                    hums.append(float('NaN'))
                    pres.append(float('NaN'))
                    volt.append(float('NaN'))
                    charging.append(bool('false'))
                    soc.append(float('NaN'))
                    #print( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(emptyTime)-(8 * 3600))), "---" )
                    empty = empty - 1
        #print( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(row[0])-(8 * 3600))), row )
        #times.append( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( int( row[0] )-(8 * 3600) ) ) )
        times.append( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime( int( row[0] ) ) ) )
        #print( time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(row[0]))), row )
        #dates.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(row[0]))))
        temps.append(float(row[1]))
        hums.append(float(row[2]))
        pres.append(float(row[3]))
        volt.append(float(row[4]))
        charging.append(bool(row[5]))
        soc.append(float(row[6]))
        i = i + 1

    conn.close()
    print ( "numSamples: "+ str(numSamples) )
    print ( "size of times: "+ str(len(times)) )
    #return numSamples, times, temps, hums, pres, volt
    return len(times), times, temps, hums, pres, volt, charging, soc

def getHistDataSingle (sql_query):
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+DB_Name)
    curs=conn.cursor()
    curs.execute(sql_query)
    data = curs.fetchall()
    conn.close()
    return data[0][0]


def deleteInvalidData (source):
    #sql_query = "delete from Temperature_Data where Date_n_Time < 28900 AND SensorID='"+source+"'"
    #conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/IoT.db')
    #curs=conn.cursor()
    #curs.execute(sql_query)
    #conn.commit()
    #conn.close()
    return

def maxRowsTable(source):
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+DB_Name)
    curs=conn.cursor()
    for row in curs.execute("select COUNT(Temperature) from Temperature_Data where SensorID='"+source+"'"):
        maxNumberRows=row[0]
    #print( "maxRowsTable" )
    #print( maxNumberRows )
    conn.close()
    return maxNumberRows

def computeTicks (x, step = 10):
    """
    Computes domain with given step encompassing series x
    @ params
    x    - Required - A list-like object of integers or floats
    step - Optional - Tick frequency
    """
    import math as Math
    xMax, xMin = Math.ceil(max(x)), Math.floor(min(x))
    dMax, dMin = xMax + abs((xMax % step) - step) + (step if (xMax % step != 0) else 0), xMin - abs((xMin % step))
    return range(dMin, dMax, step)

# define and initialize global variables
global source
source="WeatherNode1"

global displayRange
displayRange = 1

global numSamples
if displayRange != 0 :
    numSamples = displayRange
else:
    numSamples = maxRowsTable(source)
#if (numSamples > 11):
#	numSamples = 10

global numberOfSamples, times, temps, hums, pres, volt, charging, soc

# main route
@app.route("/")
def index():
    global numSamples, source, displayRange
    global numberOfSamples, dates, times, temps, hums, pres, volt, charging, soc

    myTime, temp, hum, pres, volt, charging, soc = getLastData(source)
    numMaxSamples = maxRowsTable(source)
    templateData = {
        'time'	: myTime,
        'temp'	: temp,
        'hum'	: hum,
        'pres'	: pres,
        'volt'	: volt,
        'charging' : charging,
        'soc' : soc,
        'numSamples'	: numSamples,
 		'numMaxSamples' : numMaxSamples,
 		'displayRange' : displayRange,
      	'source' : source
    }

    numberOfSamples, times, temps, hums, pres, volt, charging, soc = getHistData(source, displayRange)
    return render_template('index.html', **templateData)

@app.route("/power", methods=['GET'])
def powerQuery():
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+Power_DB_Name)
    curs=conn.cursor()
    for row in curs.execute("SELECT Date_n_Time, Total, Power, Voltage, Voltage_L2, Voltage_L3, Current, Current_L2, Current_L3, Freq FROM Power_Data ORDER BY Date_n_Time DESC LIMIT 1"):
        print( row )
        Date_n_Time = row[0]
        Total = float(row[1])
        Power = int(row[2])
        Voltage = float(row[3])
        Voltage_L2 = float(row[4])
        Voltage_L3 = float(row[5])
        Current = float(row[6])
        Current_L2 = float(row[7])
        Current_L3 = float(row[8])
        Freq = float(row[9])
    conn.close()
    templateData = {
        'time': Date_n_Time,
        'Total': Total,
        'Power': Power,
        'Voltage': Voltage,
        'Voltage_L2': Voltage_L2,
        'Voltage_L3': Voltage_L3,
        'Current': Current,
        'Current_L2': Current_L2,
        'Current_L3': Current_L3,
        'Freq': Freq
    }
    response = app.response_class(
        response=json.dumps(templateData),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/power1d", methods=['GET'])
def powerQuery1d():
    parameter = request.args.get('para')
    data = []
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+Power_DB_Name)
    curs=conn.cursor()
    print("SELECT Date_n_Time, Total, Power, Voltage, Voltage_L2, Voltage_L3, Current, Current_L2, Current_L3, Freq FROM Power_Data where datetime(Date_n_Time) >= (select datetime('now','localtime','"+parameter+"'))")
    for row in curs.execute("SELECT Date_n_Time, Total, Power, Voltage, Voltage_L2, Voltage_L3, Current, Current_L2, Current_L3, Freq FROM Power_Data where datetime(Date_n_Time) >= (select datetime('now','localtime','"+parameter+"'))"):
        #print( row )
        Date_n_Time = row[0]
        Total = float(row[1])
        Power = int(row[2])
        Voltage = float(row[3])
        Voltage_L2 = float(row[4])
        Voltage_L3 = float(row[5])
        Current = float(row[6])
        Current_L2 = float(row[7])
        Current_L3 = float(row[8])
        Freq = float(row[9])
        template = {
            'time': Date_n_Time,
            'Total': Total,
            'Power': Power,
            'Voltage': Voltage,
            'Voltage_L2': Voltage_L2,
            'Voltage_L3': Voltage_L3,
            'Current': Current,
            'Current_L2': Current_L2,
            'Current_L3': Current_L3,
            'Freq': Freq
        }
        data.append(template)
    conn.close()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/powerflex", methods=['GET'])
def powerQueryflex():
    select = request.args.get('select')
    data = []
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+Power_DB_Name)
    curs=conn.cursor()
    print(select)
    for row in curs.execute(select):
        #print( row )
        Date_n_Time = row[0]
        Total = float(row[1])
        Power = int(row[2])
        Voltage = float(row[3])
        Voltage_L2 = float(row[4])
        Voltage_L3 = float(row[5])
        Current = float(row[6])
        Current_L2 = float(row[7])
        Current_L3 = float(row[8])
        Freq = float(row[9])
        template = {
            'time': Date_n_Time,
            'Total': Total,
            'Power': Power,
            'Voltage': Voltage,
            'Voltage_L2': Voltage_L2,
            'Voltage_L3': Voltage_L3,
            'Current': Current,
            'Current_L2': Current_L2,
            'Current_L3': Current_L3,
            'Freq': Freq
        }
        data.append(template)
    conn.close()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/powermonthflex", methods=['GET'])
def powerQueryMonthFlex():
    select = request.args.get('select')
    data = []
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+Power_DB_Name)
    curs=conn.cursor()
    print(select)
    for row in curs.execute(select):
        #print( row )
        Date_n_Time = row[0]
        Total = float(row[1])
        Used = int(row[2])
        template = {
            'time': Date_n_Time,
            'Total': Total,
            'Used': Used,
        }
        data.append(template)
    conn.close()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/powerhistory", methods=['GET'])
def powerHistoryQuery():
    select = request.args.get('select')
    data = []
    conn=sqlite3.connect('/home/pi/Store_MQTT_Data_in_Database/'+Power_DB_Name)
    curs=conn.cursor()
    print(select)
    for row in curs.execute(select):
        #print( row )
        Date_n_Time = row[0]
        Total = float(row[1])
        Used = float(row[2])
        template = {
            'time': Date_n_Time,
            'Total': Total,
            'Used': Used,
        }
        data.append(template)
    conn.close()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/dbquery")
def dbquery():
    source = request.args.get('source')
    myTime, temp, heat, hum, pres, volt, charging, soc = getLastDataFull(source)
    numMaxSamples = maxRowsTable(source)
    templateData = {
        'time'	: myTime,
        'temp'	: temp,
        'heat'  : heat,
        'hum'	: hum,
        'pres'	: pres,
        'volt'	: volt,
        'charging' : charging,
        'soc' : soc,
        'numSamples'	: numSamples,
     	'numMaxSamples' : numMaxSamples,
     	'displayRange' : displayRange,
        'source' : source
    }
    response = app.response_class(
        response=json.dumps(templateData),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/source', methods=['POST','GET'])
def my_form_source_post():
    global numSamples, source, displayRange
    global numberOfSamples, dates, times, temps, hums, pres, volt, charging, soc

    #displayRange = int (request.form['displayRange'])
    source = request.form['source']
    numSamples = numMaxSamples = maxRowsTable(source)
    #displayRange = int (request.form['displayRange'])
    #print( "selected: " + source )
    if request.method == 'GET':
        return render_template('index.html', source=source)
    else:
        #numMaxSamples = maxRowsTable(source)
        #if (numSamples > numMaxSamples):
        #    numSamples = (numMaxSamples-1)
        myTime, temp, hum, pres, volt, charging, soc = getLastData(source)
        templateData = {
      	    'time'	: myTime,
        	'temp'	: temp,
          	'hum'	: hum,
          	'pres'	: pres,
          	'volt'	: volt,
            'charging' : charging,
            'soc' : soc,
          	'numSamples'	: numSamples,
            'numMaxSamples' : numMaxSamples,
     		'displayRange' : displayRange,
          	'source' : source
        }
        numberOfSamples, times, temps, hums, pres, volt, charging, soc = getHistData(source, displayRange)
        return render_template('index.html', **templateData)

@app.route('/numSamples', methods=['POST'])
def my_form_numSamples_post():
    global numSamples, source, displayRange
    global numberOfSamples, dates, times, temps, hums, pres, volt, charging, soc
    displayRange = int (request.form['displayRange'])
    #numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable(source)
    if (numSamples > numMaxSamples):
        numSamples = numMaxSamples
    myTime, temp, hum, pres, volt, charging, soc = getLastData(source)
    templateData = {
      	'time'	: myTime,
      	'temp'	: temp,
      	'hum'	: hum,
      	'pres'	: pres,
      	'volt'	: volt,
        'charging' : charging,
        'soc' : soc,
      	'numSamples'	: numSamples,
 		'numMaxSamples' : numMaxSamples,
 		'displayRange' : displayRange,
      	'source' : source
    }
    numberOfSamples, times, temps, hums, pres, volt, charging, soc = getHistData(source, displayRange)
    return render_template('index.html', **templateData)

@app.route('/plot/temp')
def plot_temp():
    global source
    global numberOfSamples, dates, times, temps, hums, pres, volt, charging, soc
    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    #print( " -> plot_temp()" )
    #print(source, displayRange)
    #numberOfSamples, times, temps, hums, pres, volt = getHistData(source, displayRange)
    dateaxis = []
    ys = temps
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Temperature [\u2103]")
    #axis.set_xlabel("Samples")
    #xs = range(numberOfSamples)
    #axis.get_xaxis().set_major_locator(MaxNLocator(integer=True))
    #axis.grid(True)

    fig.subplots_adjust(bottom=0.2)
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,numberOfSamples,1)
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    #print( "steps: ", steps )
    #print( "len(xs): ", len(xs) )
    while i < len(xs):
        #print( " i: ", i )
        #print(" add X Axis: ", date[xs[i]]) 
        dateaxis.append(times[xs[i]])
        i = i+steps
    #print( "x axis finished" )
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <-plot_temp()" )
    return response

@app.route('/plot/hum')
def plot_hum():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc
    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    #print( " -> plot_hum()" )
    #print(source, displayRange)
    #numSamples, times, temps, hums, pres, volt = getHistData(source, displayRange)
    dateaxis = []
    ys = hums
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Humidity [%]")
    #axis.set_xlabel("Samples")
    #axis.grid(True)
    #xs = range(numberOfSamples)
    #axis.get_xaxis().set_major_locator(MaxNLocator(integer=True))

    fig.subplots_adjust(bottom=0.2)
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,numberOfSamples,1)
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    #print( "steps: ", steps )
    #print( "len(xs): ", len(xs) )
    while i < len(xs):
        #print( " i: ", i )
        #print(" add X Axis: ", date[xs[i]]) 
        dateaxis.append(times[xs[i]])
        i = i+steps
    #print( "x axis finished" )
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_hum()" )
    return response

@app.route('/plot/pres')
def plot_pres():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc
    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    #print( " -> plot_pres()" )
    #print(source, displayRange)
    #numSamples, times, temps, hums, pres, volt = getHistData(source, displayRange)
    dateaxis = []
    ys = pres
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Pressure [hPa]")
    #axis.set_xlabel("Samples")
    #axis.grid(True)
    #xs = range(numberOfSamples)
    #axis.get_xaxis().set_major_locator(MaxNLocator(integer=True))

    fig.subplots_adjust(bottom=0.2)
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,numberOfSamples,1)
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    #print( "steps: ", steps )
    #print( "len(xs): ", len(xs) )
    while i < len(xs):
        #print( " i: ", i )
        #print(" add X Axis: ", date[xs[i]]) 
        dateaxis.append(times[xs[i]])
        i = i+steps
    #print( "x axis finished" )
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_pres()" )
    return response

@app.route('/plot/volt')
def plot_volt():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc
    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    #print( " -> plot_volt()" )
    #print(source, displayRange)
    #numSamples, times, temps, hums, pres, volt = getHistData(source, displayRange)
    dateaxis = []
    ys = volt
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Battery [V]")
    #axis.set_xlabel("Samples")
    #axis.grid(True)
    #xs = range(numberOfSamples)
    #axis.get_xaxis().set_major_locator(MaxNLocator(integer=True))

    fig.subplots_adjust(bottom=0.2)
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,numberOfSamples,1)
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    #print( "steps: ", steps )
    #print( "len(xs): ", len(xs) )
    while i < len(xs):
        #print( " i: ", i )
        #print(" add X Axis: ", date[xs[i]]) 
        dateaxis.append(times[xs[i]])
        i = i+steps
    #print( "x axis finished" )
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_volt()" )
    return response

@app.route('/plot/charging')
def plot_charging():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc
    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    #print( " -> plot_volt()" )
    #print(source, displayRange)
    #numSamples, times, temps, hums, pres, volt = getHistData(source, displayRange)
    dateaxis = []
    ys = charging
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Charging")
    #axis.set_xlabel("Samples")
    #axis.grid(True)
    #xs = range(numberOfSamples)
    #axis.get_xaxis().set_major_locator(MaxNLocator(integer=True))

    fig.subplots_adjust(bottom=0.2)
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,numberOfSamples,1)
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    #print( "steps: ", steps )
    #print( "len(xs): ", len(xs) )
    while i < len(xs):
        #print( " i: ", i )
        #print(" add X Axis: ", date[xs[i]]) 
        dateaxis.append(times[xs[i]])
        i = i+steps
    #print( "x axis finished" )
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_volt()" )
    return response

@app.route('/plot/soc')
def plot_soc():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc
    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    #print( " -> plot_volt()" )
    #print(source, displayRange)
    #numSamples, times, temps, hums, pres, volt = getHistData(source, displayRange)
    dateaxis = []
    ys = soc
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("State of Charge")
    #axis.set_xlabel("Samples")
    #axis.grid(True)
    #xs = range(numberOfSamples)
    #axis.get_xaxis().set_major_locator(MaxNLocator(integer=True))

    fig.subplots_adjust(bottom=0.2)
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,numberOfSamples,1)
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    #print( "steps: ", steps )
    #print( "len(xs): ", len(xs) )
    while i < len(xs):
        #print( " i: ", i )
        #print(" add X Axis: ", date[xs[i]]) 
        dateaxis.append(times[xs[i]])
        i = i+steps
    #print( "x axis finished" )
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_volt()" )
    return response

@app.route('/plot/minmaxtemp')
def plot_minmaxtemp():
    global source, displayRange
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc

    #print( " -> plot_minmaxtemp()" )

    deleteInvalidData(source)

    if displayRange == 0 :
        days = int(getHistDataSingle("select julianday('now') - julianday(date((SELECT MIN(Date_n_Time) FROM Temperature_Data where SensorID='"+source+"'), 'unixepoch'))"))
    else:
        days = displayRange
        if days < 7 :
         	days = 7
    
    #print( "displayRange: ", displayRange )

    date = []
    dateaxis = []
    tempmin = []
    tempmax = []
    if days == 28:
        dateRange = "1 month"
    elif days == 84:
        dateRange = "3 month"
    else:
        dateRange = str(days)+" day"
    
    i = days
    while i > 0:
        #print( "i: ", i )
        date.append( getHistDataSingle("SELECT date('now', '-"+str(i)+" day')") )
        #tempmin.append( getHistDataSingle("SELECT MIN(Temperature) FROM Temperature_Data where SensorID='"+source+"' AND julianday(date(Date_n_Time-(7*3600), 'unixepoch')) = julianday(date('now', '-"+str(i)+" days'))") )
        #tempmax.append( getHistDataSingle("SELECT MAX(Temperature) FROM Temperature_Data where SensorID='"+source+"' AND julianday(date(Date_n_Time-(7*3600), 'unixepoch')) = julianday(date('now', '-"+str(i)+" days'))") )
        tempmin.append( getHistDataSingle("SELECT MIN(Temperature) FROM Temperature_Data where SensorID='"+source+"' AND julianday(date(Date_n_Time, 'unixepoch')) = julianday(date('now', '-"+str(i)+" days'))") )
        tempmax.append( getHistDataSingle("SELECT MAX(Temperature) FROM Temperature_Data where SensorID='"+source+"' AND julianday(date(Date_n_Time, 'unixepoch')) = julianday(date('now', '-"+str(i)+" days'))") )
        i = i - 1
    #date.append( getHistDataSingle("SELECT date('now', '-"+dateRange+"')") )
    #tempmin.append( getHistDataSingle("SELECT MIN(Temperature) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-"+dateRange+"')") )
    #tempmax.append( getHistDataSingle("SELECT MAX(Temperature) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-"+dateRange+"')") )
    #print( "end of fetch" )

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(bottom=0.2)
    axis.set_title("Temperature min/max [\u2103] ("+str(days)+" days)")
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,len(date),1)
    #print("xs: ", xs )
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    #print( "steps: ", steps )
    #print( "len(xs): ", len(xs) )
    while i < len(xs):
        #print( " i: ", i )
        #print(" add X Axis: ", date[xs[i]]) 
        dateaxis.append(date[xs[i]])
        i = i+steps
    #print( "x axis finished" )
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)
    ys = tempmin
    axis.plot(xs, ys)
    ys = tempmax
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_minmaxtemp()" )
    return response

@app.route('/plot/minmaxhum')
def plot_minmaxhum():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc

    #print( " -> plot_minmaxhum()" )

    deleteInvalidData(source)
    if displayRange == 0 :
        days = int(getHistDataSingle("select julianday('now') - julianday(date((SELECT MIN(Date_n_Time) FROM Temperature_Data where SensorID='"+source+"'), 'unixepoch'))"))
    else:
        days = displayRange
        if days < 7 :
        	days = 7
    
    date = []
    dateaxis = []
    hummin = []
    hummax = []
    if days == 28:
        dateRange = "1 month"
    elif days == 84:
        dateRange = "3 month"
    else:
        dateRange = str(days)+" day"
    
    i = days
    while i > 0:
        date.append( getHistDataSingle("SELECT date('now', '-"+str(i)+" day')") )
        hummin.append( getHistDataSingle("SELECT MIN(Humidity) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
        hummax.append( getHistDataSingle("SELECT MAX(Humidity) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
        i = i - 1
    #date.append( getHistDataSingle("SELECT date('now', '-"+str(i)+" day')") )
    #hummin.append( getHistDataSingle("SELECT MIN(Humidity) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
    #hummax.append( getHistDataSingle("SELECT MAX(Humidity) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )

    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    fig = Figure()
    fig.subplots_adjust(bottom=0.2)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Humidity min/max [%] ("+str(days)+" days)")
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,len(date),1)
    #print( len(xs), len(tempmin) )
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    while i < len(xs):
        dateaxis.append(date[xs[i]])
        i = i+steps
    
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)
    ys = hummin
    axis.plot(xs, ys)
    ys = hummax
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_minmaxhum()" )
    return response

@app.route('/plot/minmaxpres')
def plot_minmaxpres():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc

    #print( " -> plot_minmaxpres()" )

    deleteInvalidData(source)
    if displayRange == 0 :
        days = int(getHistDataSingle("select julianday('now') - julianday(date((SELECT MIN(Date_n_Time) FROM Temperature_Data where SensorID='"+source+"'), 'unixepoch'))"))
    else:
        days = displayRange
        if days < 7 :
        	days = 7
    
    date = []
    dateaxis = []
    presmin = []
    presmax = []
    if days == 28:
        dateRange = "1 month"
    elif days == 84:
        dateRange = "3 month"
    else:
        dateRange = str(days)+" day"
    
    i = days
    while i > 0:
        date.append( getHistDataSingle("SELECT date('now', '-"+str(i)+" day')") )
        presmin.append( getHistDataSingle("SELECT MIN(Pressure) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
        presmax.append( getHistDataSingle("SELECT MAX(Pressure) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
        i = i - 1
    #date.append( getHistDataSingle("SELECT date('now', '-"+str(i)+" day')") )
    #presmin.append( getHistDataSingle("SELECT MIN(Pressure) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
    #presmax.append( getHistDataSingle("SELECT MAX(Pressure) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )

    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    fig = Figure()
    fig.subplots_adjust(bottom=0.2)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Pressure min/max [hPa] ("+str(days)+" days)")
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,len(date),1)
    #print( len(xs), len(tempmin) )
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    while i < len(xs):
        dateaxis.append(date[xs[i]])
        i = i+steps
    
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)
    ys = presmin
    axis.plot(xs, ys)
    ys = presmax
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_minmaxpres()" )
    return response

@app.route('/plot/minmaxvolt')
def plot_minmaxvolt():
    global source
    global numberOfSamples, times, temps, hums, pres, volt, charging, soc

    #print( " -> plot_minmaxvolt()" )

    deleteInvalidData(source)
    if displayRange == 0 :
        days = int(getHistDataSingle("select julianday('now') - julianday(date((SELECT MIN(Date_n_Time) FROM Temperature_Data where SensorID='"+source+"'), 'unixepoch'))"))
    else:
        days = displayRange
        if days < 7 :
        	days = 7
    
    date = []
    dateaxis = []
    voltmin = []
    voltmax = []
    if days == 28:
        dateRange = "1 month"
    elif days == 84:
        dateRange = "3 month"
    else:
        dateRange = str(days)+" day"
    
    i = days
    while i > 0:
        date.append( getHistDataSingle("SELECT date('now', '-"+str(i)+" day')") )
        voltmin.append( getHistDataSingle("SELECT MIN(Voltage) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
        voltmax.append( getHistDataSingle("SELECT MAX(Voltage) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') = date('now', '-"+str(i)+" day')") )
        i = i - 1
    #date.append( getHistDataSingle("SELECT date('now', '-"+dateRange+"')") )
    #voltmin.append( getHistDataSingle("SELECT MIN(Voltage) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-"+dateRange+"')") )
    #voltmax.append( getHistDataSingle("SELECT MAX(Voltage) FROM Temperature_Data where SensorID='"+source+"' AND date(Date_n_Time, 'unixepoch') >= date('now', '-"+dateRange+"')") )

    #times, temps, hums, pres, volt = getHistData(source, numSamples)
    fig = Figure()
    fig.subplots_adjust(bottom=0.2)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Battery min/max [V] ("+str(days)+" days)")
    axis.set_xlabel("Date")
    axis.grid(True)
    xs = range(0,len(date),1)
    #print( len(xs), len(tempmin) )
    i = 0
    steps = int( round((len(xs)/10)+0.5) )
    while i < len(xs):
        dateaxis.append(date[xs[i]])
        i = i+steps
    
    #axis.set_xticks(xs)
    axis.set_xticks(range(0,len(xs),steps))
    axis.set_xticklabels(dateaxis, rotation=90, fontsize=8)
    ys = voltmin
    axis.plot(xs, ys)
    ys = voltmax
    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    #print( " <- plot_minmaxvolt()" )
    return response

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True, extra_files=["./templates/index.html"])
