from flask import Flask, jsonify
from sqlalchemy import extract
from sqlalchemy import desc
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
import pandas as pd
#create dictionary for precipitaton 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#create app
app = Flask(__name__)

#get the latest date
latest_date = session.query(Measurement.date, Measurement.prcp).order_by(desc('date')).first()
#to get the year before the latest date
#3-03-bonus
# to make a list of the date
list_latest_date = list(latest_date)
# to get the first index item of the list 
txt = list_latest_date[0]
#to split the list and make them as integers 
new_txt = txt.split("-")
latest_year = int(new_txt[0])
latest_month = int(new_txt[1])
latest_day = int(new_txt[2])
# Calculate the date 1 year ago from the last data point in the database
last_date = dt.date(latest_year,latest_month,latest_day) - dt.timedelta(days=365)
last_date
#Convert the query results to a Dictionary using date as the key and prcp as the value.
precipitaton_tb = []
dataset = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_date).order_by(desc(Measurement.date)).all()
for data in dataset:
    precipitaton_dic = {data.date:data.prcp} 
    precipitaton_tb.append(precipitaton_dic)
#==============================
#Convert the query results to a Dictionary using station ID as the key and station name as the value.
station_tb=[]
station_ID = session.query(Station.station, Station.name).all()
for stations in station_ID:
    station_dic ={stations.station:stations.name}
    station_tb.append(station_dic)
#=================================
#query for the dates and temperature observations from a year from the last data point.
tobs_tb=[]
tobs_data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= last_date).order_by(desc(Measurement.date)).all()
for tob in tobs_data:
    tobs_dic={tob.date:tob.tobs}
    tobs_tb.append(tobs_dic)
#================================
#eturn a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

#=================================
@app.route("/api/v1.0/precipitaton")
def precipitaton():
    """Return the precipitaton data as json"""
    
    return jsonify(precipitaton_tb)
#=================================
@app.route("/api/v1.0/stations")
def stations():
    
    return jsonify(station_tb)
#=================================
@app.route("/api/v1.0/tobs")
def tobs():
    #return a JSON list of Temperature Observations (tobs) for the previous year.
    return jsonify(tobs_tb)
#===================================
@app.route("/api/v1.0/<start>")
def starts(start):
    sel = ([Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)])
    
    #return a JSON list of Temperature Observations (tobs) for the previous year.
    tobs_previous = session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date)>= start).group_by(Measurement.date).all()
    dates=[]
    for date in tobs_previous:
        date_dic ={}
        date_dic["minitemp"]:date[1]
        date_dic["avgtemp"]:tobs_previous[2]
        date_dic["maxtemp"]:tobs_previous[3]
        dates.append(date_dic)
    return jsonify(dates)
#============================
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    sel = ([Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)])
    
    tops_end = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    dates=[]
    for date in tobs_previous:
        date_dic ={}
        date_dic["minitemp"]:date[1]
        date_dic["avgtemp"]:tobs_previous[2]
        date_dic["maxtemp"]:tobs_previous[3]
        dates.append(date_dic)
    return jsonify(dates)
#==========================
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitaton<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        )



if __name__=="__main__":
    app.run(debug=True)


