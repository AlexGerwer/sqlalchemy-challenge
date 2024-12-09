#################################################
# Import the dependencies.
#################################################
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template, send_from_directory, send_file

#################################################
# Database Setup
#################################################
engine = create_engine(r"sqlite:///C:\Users\asg_a_1p8y6mm\OneDrive\Desktop\WIOA Training\DataAnalytics\Module 10\Module 10; Class Challenge\sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Define the image and template folder paths globally
TEMPLATE_FOLDER = r"C:\Users\asg_a_1p8y6mm\OneDrive\Desktop\WIOA Training\DataAnalytics\Module 10\Module 10; Class Challenge\sqlalchemy-challenge\SurfsUp\Resources"
IMAGE_FOLDER = TEMPLATE_FOLDER  # Use the same folder for images and templates

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<br/>"
        f"/api/v1.0/temp/end (replace 'end' with a date in YYYY-MM-DD format)<br/>"
        f"/api/v1.0/temp/start/end (replace 'start' and 'end' with dates in YYYY-MM-DD format)<br/>"
        f"/api/v1.0/temp/graph<br/>"
        f"/api/v1.0/precipitation/graph<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query for the dates and temperature observations from a year from the last data point.

    Convert the query results to a Dictionary using date as the key and prcp as the value.
    """
    # Find the most recent date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    # Calculate the date one year from the last date in data set.
    prev_year = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Station.station).all()
    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Find the most recent date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    # Calculate the date one year from the last date in data set.
    prev_year = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    # Return the results
    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/graph")
def temp_graph():
    """Generate a histogram of temperature observations for the most active station and display it."""
    # Find the most recent date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()

    # Calculate the date one year from the last date in data set.
    prev_year = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Query temperature observations for the most active station in the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    # Convert results to a list of temperatures
    temperatures = [temp[0] for temp in results]

    # Create a histogram
    plt.hist(temperatures, bins=12, label='tobs')
    plt.xlabel('Temperature')
    plt.ylabel('Frequency')
    plt.title('Temperature Observation Data (tobs) for Station USC00519281')
    plt.legend()

    # Save the plot to the specified folder
    image_file = os.path.join(IMAGE_FOLDER, "temp_histogram.png")
    plt.savefig(image_file)

    # Create the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Temperature Histogram</title>
    </head>
    <body>
        <h1>Temperature Histogram</h1>
        <img src="/images/temp_histogram.png" alt="Temperature Histogram">
    </body>
    </html>
    """

    # Write the HTML file to the TEMPLATE_FOLDER
    html_file_path = os.path.join(TEMPLATE_FOLDER, "temp_graph.html")
    with open(html_file_path, "w") as f:
        f.write(html_content)

    return send_file(html_file_path)

@app.route("/api/v1.0/precipitation/graph")
def precipitation_graph():
    """Generate a precipitation analysis histogram and display it."""

    # Calculate the date one year from the last date in data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    year_ago = dt.datetime.strptime(most_recent_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    df = pd.DataFrame(results, columns=['date', 'precipitation'])
    df.set_index('date', inplace=True)

    # Sort the dataframe by date
    df = df.sort_values("date")

    # Use Pandas Plotting with Matplotlib to plot the data
    df.plot(rot=90)
    plt.xlabel("Date")
    plt.ylabel("Inches")
    plt.title("Precipitation Analysis (Last 12 Months)")

    # Save the plot to the specified folder
    image_file = os.path.join(IMAGE_FOLDER, "precipitation_histogram.png")
    plt.savefig(image_file)

    # Create the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Precipitation Analysis</title>
    </head>
    <body>
        <h1>Precipitation Analysis (Last 12 Months)</h1>
        <img src="/images/precipitation_histogram.png" alt="Precipitation Analysis">
    </body>
    </html>
    """

    # Write the HTML content to a file
    html_file = os.path.join(TEMPLATE_FOLDER, "precipitation_graph.html")
    with open(html_file, "w") as f:
        f.write(html_content)

 
    # Return the rendered HTML template
    return send_file(html_file)

@app.route('/images/<filename>')
def get_image(filename):
    """Serve the image file."""
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route("/api/v1.0/temp/")
@app.route("/api/v1.0/temp/<end>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return temperature statistics."""
    # Find the earliest and latest dates in the database
    earliest_date_str = session.query(func.min(Measurement.date)).scalar()
    latest_date_str = session.query(func.max(Measurement.date)).scalar()
    earliest_date = dt.datetime.strptime(earliest_date_str, "%Y-%m-%d")
    latest_date = dt.datetime.strptime(latest_date_str, "%Y-%m-%d")

    # Check if start and end dates are within the valid range
    if start:
        start_dt = dt.datetime.strptime(start, "%Y-%m-%d")
        if start_dt < earliest_date or start_dt > latest_date:
            return jsonify({"error": f"Start date '{start}' is out of range. Valid date range is {earliest_date_str} to {latest_date_str}."}), 400

    if end:
        end_dt = dt.datetime.strptime(end, "%Y-%m-%d")
        if end_dt < earliest_date or end_dt > latest_date:
            return jsonify({"error": f"End date '{end}' is out of range. Valid date range is {earliest_date_str} to {latest_date_str}."}), 400

    # Define the selection for min, avg, and max temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end and not start:
        # Case 1: No start or end date provided (default to last year from hardcoded date)
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        results = session.query(*sel).\
            filter(Measurement.date >= prev_year).all()
    elif not start:
        # Case 2: Only end date provided
        # Calculate start date as one year before the end date
        end_dt = dt.datetime.strptime(end, "%Y-%m-%d")
        start_dt = end_dt - dt.timedelta(days=365)

        results = session.query(*sel). \
            filter(Measurement.date >= start_dt). \
            filter(Measurement.date <= end_dt).all()
    else:
        # Case 3: Both start and end dates provided
        start_dt = dt.datetime.strptime(start, "%Y-%m-%d")

        if end:
            # Handle case when end date is also provided
            end_dt = dt.datetime.strptime(end, "%Y-%m-%d")
            results = session.query(*sel). \
                filter(Measurement.date >= start_dt). \
                filter(Measurement.date <= end_dt).all()
        else:
            # Handle case when only start date is provided
            results = session.query(*sel). \
                filter(Measurement.date >= start_dt).all()

    # Convert the query results to a list and return as JSON
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)