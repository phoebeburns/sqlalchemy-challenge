# Python SQL toolkit and Object Relational Mapper
from unicodedata import name
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify, request

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
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>" f"Precipitation data for the last year of data.<br/><br/>"
        f"/api/v1.0/stations<br/>"f"List of weather stations.<br/><br/>"
        f"/api/v1.0/tobs<br/>" f"List of temperature observations for last year of data.<br/><br/>"
        f"/api/v1.0/start<br/>" f"<t/>Enter a start date and it returns termerature stats.<br/><br/>"
        f"/api/v1.0/start/end<br/>"  f"Enter a start and end date and it returns terperature stats for betwen those dates.<br/>"
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

    stations = session.query(Station.station, Station.name, Station.latitude\
        ,Station.longitude, Station.elevation).order_by(Station.name.asc()).all()

    session.close()

    station_list = []

    for  station,name,latitude,longitude,elevation in stations:
        stn_dict = {}
        stn_dict["Station"] = station
        stn_dict["Station Name"] = name
        stn_dict["Latitude"] = latitude
        stn_dict["Longitude"] = longitude
        stn_dict["Elevation"] = elevation
        station_list.append(stn_dict)

    return jsonify(f"Here is a list of station info.",station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_year = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > query_date,\
            Station.station == 'USC00519281',Measurement.station == Station.station)

    session.close()

    tobsy = {}

    for date, tobs in temp_year:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobsy.update(tobs_dict)

    return jsonify(f"Here is the last year's data for station USC00519281.",tobsy)


@app.route("/api/v1.0/<start>")
def startDateOnly(start):

    session = Session(engine)

    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close 

    tstats = {}
  
    for column in temp_stats.__table__.columns:
        tstats[column.name] = str(getattr(temp_stats, column.name))

    return jsonify(tstats)


@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):

    session = Session(engine)

    temp_stats2 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close
   
    return jsonify(temp_stats2)

if __name__ == '__main__':
    app.run(debug=True)
