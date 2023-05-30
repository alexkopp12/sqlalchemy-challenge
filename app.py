# Import the dependencies.
from flask import Flask, jsonify

#SQL Tools
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")




# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Stations = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup
app = Flask(__name__)




# Flask Routes
@app.route("/")
def home():
    """Home route that list all my route paths"""
    return(
        f"Welcome to my Hawaii Weather API<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date > one_year_ago).\
            order_by(Measurement.date).all()
    
    data_dict = {date: prcp for date, prcp in data}

    session.close()

    return jsonify(data_dict);

    

@app.route("/api/v1.0/stations")
def station():
    stat_active = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    station_list = (station for station in stat_active)
    session.close()
    return jsonify(stat_active);

@app.route("/api/v1.0/tobs")
def tobs():
    station_id ='USC00519281'
    one_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days=365)
    active_station_df = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == station_id, Measurement.date > one_year_ago).all()
    temp_list = {date: tobs for date, tobs in active_station_df}
    session.close()
    return jsonify(temp_list);

@app.route("/api/v1.0/<start>")
def start(start_date):
    sum_date = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date == start_date).all()
    session.close()
    return jsonify(sum_date);

@app.route("/api/v1.0/<start>/<end>")
def end(start_date, end_date):
    sum_range = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date and Measurement.date <= end_date).all()
    session.close()
    return jsonify(sum_range);

if __name__ == "__main__":
    app.run(debug=True)