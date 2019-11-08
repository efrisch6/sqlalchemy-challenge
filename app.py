import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        return 
        
@app.route("/api/v1.0/stations")
def stations():
        """
        Return a JSON list of stations from the dataset.
        """
        
        session = Session(engine)
        
        results = session.query(Station.name).all()
        
        session.close()
        
        all_names = list(np.ravel(results))
        
        return jsonify(all_names)
    
        
@app.route("/api/v1.0/tobs")
def tobs():
    """
    query for the dates and temperature observations from a year from the last data point.
    Return a JSON list of Temperature Observations (tobs) for the previous year.
    """
    return


@app.route("/api/v1.0/<start>")
def start():
    """
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    """
    return


@app.route("/api/v1.0/<start>/<end>")
def start_end():
    """
    Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    """
    return
        
    
if __name__ == '__main__':
    app.run(debug=True)

    
    