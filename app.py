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

app = Flask(__name__)

@app.route("/")
def home():
    session = Session(engine)
    print("Server received request for 'Home' page...")
    return "Available Routes: /api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/start, /api/v1.0/start/end" 
    session.close()

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()
    return jsonify(prcp_results)
    session.close()

@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
    station_results = session.query(Station.station).all()
    return jsonify(station_results)
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_station_data = session.query(Measurement.date).filter(Measurement.station == 'USC00519281').order_by(Measurement.date.desc()).all()
    active_most_recent = active_station_data[0][0]
    active_most_recent_dt = dt.datetime.strptime(active_most_recent, '%Y-%m-%d')
    active_one_year_prior = active_most_recent_dt - dt.timedelta(days=365)
    active_station_data = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= active_one_year_prior).all()
    return jsonify(active_station_data)
    session.close()

@app.route("/api/v1.0/<start>")
def start_search(start):
    session = Session(engine)
    start_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    return f'The minimum temperature from {start} to present was {start_min[0][0]}. The maximum temperature was {start_max[0][0]}. The average temperature was {start_avg[0][0]}'
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def start_end_search(start, end):
    session = Session(engine)
    start_end_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date < end).all()
    start_end_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date < end).all()
    start_end_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date < end).all()
    return f'The minimum temperature from {start} to {end} was {start_end_min[0][0]}. The maximum temperature was {start_end_max[0][0]}. The average temperature was {start_end_avg[0][0]}'
    session.close()

if __name__ == "__main__":
    app.run(debug=True)
