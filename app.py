#app.py
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)


app = Flask(__name__)


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Available Routes: /api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/<start>, /api/v1.0/<start>/<end>" 
    
prcp_results = session.query(Measurement.date, Measurement.prcp).all()

@app.route("/api/v1.0/precipitation")
def precipitation():
    return jsonify(prcp_results)

station_results = session.query(Station.station).all()

@app.route("/api/v1.0/station")
def station():
    return jsonify(station_results)

active_station_data = session.query(Measurement.date).filter(Measurement.station == 'USC00519281').order_by(Measurement.date.desc()).all()
active_most_recent = active_station_data[0][0]
active_most_recent_dt = dt.datetime.strptime(active_most_recent, '%Y-%m-%d')
active_one_year_prior = active_most_recent_dt - dt.timedelta(days=365)
active_station_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= active_one_year_prior).all()

@app.route("/api/v1.0/tobs")
def tobs():
    return jsonify(active_station_data)

if __name__ == "__main__":
    app.run(debug=True)
