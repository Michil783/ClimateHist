#------------------------------------------
#--- Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#------------------------------------------

import sqlite3

# SQLite DB Name
DB_Name =  "Power.db"

"""
drop table if exists Power_Data ;
create table Power_Data (
  Date_n_Time text primary key,
  Total float,
  Power integer,
  Voltage float,
  Voltage_L2 float,
  Voltage_L3 float,
  Current float,
  Current_L2 float,
  Current_L3 float,
  Freq float
);
drop table if exists Power_Data_Day ;
create table Power_Data_Day (
  Date text primary key,
  Total float,
  Used float
);
drop table if exists Power_Data_Month ;
create table Power_Data_Month (
  Date text primary key,
  Total float,
  Used float
);
drop table if exists Power_Data_Year ;
create table Power_Data_Year (
  Date text primary key,
  Total float,
  Used float
);
"""
# SQLite DB Table Schema
TableSchema="""
drop table if exists Power_Data ;
create table Power_Data (
  Date_n_Time text primary key,
  Total float,
  Power integer,
  Voltage float,
  Voltage_L2 float,
  Voltage_L3 float,
  Current float,
  Current_L2 float,
  Current_L3 float,
  Freq float
);
"""

#Connect or Create DB File
conn = sqlite3.connect(DB_Name)
curs = conn.cursor()

#Create Tables
sqlite3.complete_statement(TableSchema)
curs.executescript(TableSchema)

#Close DB
curs.close()
conn.close()
