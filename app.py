import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

######################################################
# DATABASE SETUP
######################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


######################################################
# FLASK SETUP
######################################################

app = Flask(__name__)

######################################################
# FLASK ROUTES
######################################################

@app.route('/')
def index():
    """
    Home page
    List of all routes available
    """
    return(
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
           
@app.route("/api/v1.0/precipitation")
def precipiation():
        """
        Convert the query results to a Dictionary using date as the key and prcp as the value.
        Return the JSON representation of your dictionary.
        """

        session = Session(engine)
        results = session.query(Measurement.date, Measurement.prcp).all()
        session.close()

        all_prcp = []
        for date, prcp in results:
            prcp_dict = {}
            prcp_dict[date] = prcp
            all_prcp.append(prcp_dict)

        return jsonify(all_prcp)
        
@app.route("/api/v1.0/stations")
def stations():
        """
        Return a JSON list of stations from the dataset.
        """
        
        session = Session(engine)
        results = session.query(Station.name).all()
        session.close()
        all_stations = list(np.ravel(results))
        
        return jsonify(all_stations)
        

@app.route("/api/v1.0/tobs")
def tobs():
    """
    query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year.
    """

    session = Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    year_ago = (dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    last_year = session.query(Measurement.date, Measurement.tobs).filter_by(date=year_ago).all()

    session.close()

    return jsonify(last_year)


@app.route("/api/v1.0/<start>")
def start(start):
    """
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    """

    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    all_dates = []
    for tmin, tavg, tmax in results:
        dates_dict = {}
        dates_dict['tmin'] = tmin
        dates_dict['tavg'] = tavg
        dates_dict['tmax'] = tmax
        all_dates.append(dates_dict)
    
    return jsonify(all_dates)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    """
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date >= end).all()

    session.close()

    all_dates = []
    for tmin, tavg, tmax in results:
        dates_dict = {}
        dates_dict['tmin'] = tmin
        dates_dict['tavg'] = tavg
        dates_dict['tmax'] = tmax
        all_dates.append(dates_dict)
    
    return jsonify(all_dates)
        
    
if __name__ == '__main__':
    app.run(debug=True)

    
    