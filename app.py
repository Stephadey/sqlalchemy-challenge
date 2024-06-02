# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources///hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()


# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)


# Assign the measurement class to a variable called `Measurement` and
measurement = Base.classes.measurement

# the station class to a variable called `Station`
station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# main route

@app.route('/')
def welcome():
    """Welcome"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date/2016-08-14<br/>"
        f"/api/v1.0/date/2016-08-14/2016-09-01<br/>"
    )

# precipitation route

@app.route('/api/v1.0/precipitation')
def prec():
    session = Session(engine)

    # Find the most recent date in the data set.
    query_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    latest_date = query_date[0]

    # Convert latest date to permit calculations
    converted_date = dt.datetime.strptime(latest_date, '%Y-%m-%d').date()
    # Calculate the date one year from the last date in data set.
    start_date = converted_date - dt.timedelta(days=365)
    # Convert the start date back to be used in the queries
    str_start_date = start_date.strftime('%Y-%m-%d')

    prcp_query = session.query(measurement.date,
                measurement.prcp)\
                .filter(measurement.date >= str_start_date).all()
    
    session.close()

    precipitation = []
    for date, prcp in prcp_query:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["precipitation"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

#################################################
# stations route


@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    """Returns a list of stations"""

    # Query the unique values of the stations
    results = session.query(measurement.station).distinct()

    session.close()

    # Loop through the query to display the stations
    station_list = [i[0] for i in results]

    return jsonify(station_list)


#################################################
# tobs route

@app.route('/api/v1.0/tobs')
def tobs():
    
    session = Session(engine)

    """Return the dates and temperature observations for the most-active station for the previous year of data"""

    # Identify the most active station (will be the top station from the list ordered in descending values)
    most_active_stations = session.query(measurement.station,
              func.count(measurement.station))\
                .group_by(measurement.station)\
                .order_by(func.count(measurement.station).desc())\
                .all()
    
    # Get the latest date for the most active station
    query_date_most_active = session.query(measurement.date)\
    .filter(measurement.station == most_active_stations[0][0])\
    .order_by(measurement.date.desc())\
    .first()
    latest_date_most_active = query_date_most_active[0]

    # Convert the latest date and calculate 365 days before
    converted_date_most_active = dt.datetime.strptime(latest_date_most_active, '%Y-%m-%d').date()

    start_date_most_active = converted_date_most_active - dt.timedelta(days=365)

    str_start_date_most_active = start_date_most_active.strftime('%Y-%m-%d')

    # Query the date and temperature between the latest date and one year before
    tobs_query = session.query(measurement.date,
               measurement.tobs)\
               .filter((measurement.station == most_active_stations[0][0])
                       &(measurement.date <= latest_date_most_active)
                       & (measurement.date >= str_start_date_most_active)).all()

    session.close()

    # save results as a dictionary within a list to be displayed
    temperatures = []
    for date, tobs in tobs_query:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = tobs
        temperatures.append(temp_dict)

    # jsonify the data
    return jsonify(temperatures)


#################################################
# dates routes with start and start/end

@app.route('/api/v1.0/date/<start>')

@app.route('/api/v1.0/date/<start>/<end>')
def start(start=None, end=None):
    session = Session(engine)

    # convert the start date to be used in the queries
    start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()

# using 'If not' allows using the same code to both routes, <start> and <start>/<end>
    
# define condition to run the query
    if not end:
        # calculate min, max and avg if only specified a start date
        calculation_result = (
            session.query(
                func.min(measurement.tobs).label('min temp'),
                func.max(measurement.tobs).label('max temp'),
                func.avg(measurement.tobs).label('avg temp')
            )
            .filter(measurement.date >= start_date)
            .all()
        )

        # close session
        session.close()

        # save results as a dictionary to be displayed
        result_dict = {
            'min_temp': calculation_result[0][0],
            'max_temp': calculation_result[0][1],
            'avg_temp': calculation_result[0][2]}

        # jsonify the dicitionary
        return jsonify(result_dict)
    
    # convert the end date to be used in the queries
    end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    
    # calculate min, max and avg if stard and end dates are given
    calculation_result = (
        session.query(
            func.min(measurement.tobs).label('min temp'),
            func.max(measurement.tobs).label('max temp'),
            func.avg(measurement.tobs).label('avg temp')
        )
        .filter(measurement.date.between(start_date, end_date))
        .all()
    )

    # close session
    session.close()

    # save results as a dictionary to be displayed
    result_dict = {
            'min_temp': calculation_result[0][0],
            'max_temp': calculation_result[0][1],
            'avg_temp': calculation_result[0][2]
    }
    # jsonify the dicionary
    return jsonify(result_dict)



if __name__ == '__main__':
    app.run(debug=True)
