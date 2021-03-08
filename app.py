# 1. import Flask
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitations"""
    # Query date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

     # Create a dictionary from the row data and append to a list of date and prcp
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations names"""
    # Query all stations
    results = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperatures():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date and temperature"""
    # Query one year date and temperature for most active station
    date=dt.datetime(2016,8,22)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date > date).\
        filter(Measurement.station=='USC00519281').group_by(Measurement.tobs).all()
    session.close()

    # Convert list of tuples into normal list
    one_year_temperature = list(np.ravel(results))

    return jsonify( one_year_temperature)


@app.route("/api/v1.0/start")
def start_temperatures():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date and temperature"""
    # Query mini temperature for most active station
    date=dt.datetime(2016,8,22)
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date > date).all()
    
    #mini_temperature = list(np.ravel(results))
    return jsonify(results)
    

@app.route("/api/v1.0/start/end")
def start_end_temperatures():
     # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all date and temperature"""
    # Query mini temperature for most active station
    date_start=dt.datetime(2016,8,22)
    date_end=dt.datetime(2016,12,22)
    results=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date > date_start).\
        filter(Measurement.date < date_end).all()
    
    #mini_temperature = list(np.ravel(results))
    return jsonify(results)
   




if __name__ == "__main__":
    app.run(debug=True)