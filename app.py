# Python SQL toolkit and Object Relational Mapper
from unicodedata import name
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///./resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route('/')
def welcome():
   

    """List all available api routes."""
    return (
        "Welcome to the Hawaii Weather Project <br/><br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
      #  f"/api/v1.0/<start>" and "/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #max date = 8/23/2017
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_of_data = session.query( Measurement.date, Measurement.prcp).\
        order_by(Measurement.date.desc()).filter(Measurement.date > query_date)

    session.close()

    date_prcp = {}

    for date, prcp in year_of_data:
        prcp_dict = {}
        prcp_dict[date] = prcp
        date_prcp.update(prcp_dict)

    return jsonify(f"Here is a list of dates and precipitation measurements.",date_prcp)
    

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations = session.query( station.id,Station.station, Station.name, Station.latitude,\
        Station.longitude,Station.elevation).all()

    session.close()

    station_dict = {}

    for  station, name, latitude, longitude, elevation in stations:
        stn_dict = {}
        stn_dict["ID"] = station
        stn_dict["Station"] = station
        stn_dict["Station Name"] = name
        stn_dict["Latitude"] = latitude
        stn_dict["Longitude"] = longitude
        stn_dict["Elevation"] = elevation
        station_dict.update(stn_dict)

    return jsonify(station_dict)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > query_date,\
            Station.id == '7',Measurement.station == Station.station)

    session.close()

    tobsy = {}

    for date, tobs in temp_year:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobsy.update(tobs_dict)

    return jsonify(tobs)


# @app.route("/api/v1.0/<start>" 
# 
#     print('Find out the temperature data between different dates')
    
#     startdate = input('Enter a start date:')


# "/api/v1.0/<start>/<end>")
# def start():

#     print('Find out the temperature data between different dates')
    
#     startdate = input('Enter a start date:')
#     enddate = input('Enter an end date - not required:')



if __name__ == '__main__':
    app.run(debug=True)
