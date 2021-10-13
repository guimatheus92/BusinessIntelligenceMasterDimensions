# app.py

from flask import Flask, jsonify
from dimensioncalendar import DimensionCalendar
import pandas as pd
import os

# Launching an app flask
app = Flask(__name__)

@app.route('/')
def index():
    index_data = [
    {
        "href": "/DimensionCalendar",
        "name": "Dimension Calendar",
        "description": "Dimension Calendar endpoint with date attributes"
    }
    ]
    return jsonify(index_data), 200

@app.route('/dimensioncalendar')
def dimensioncalendar():
    # Read CSV file    
    #data = pd.read_csv(r'/static/csv/DimensionCalendar.csv')    
    data = DimensionCalendar()
    data = data.astype(str)
    # Convert dataframe to dictionary
    data = data.to_dict("list")
    # Return data and 200 OK code
    return (data), 200

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# Run our Flask app
if __name__ == '__main__':
    app.run()