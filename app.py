# app.py

# --------------------------------------------------------------------------------------------------#
# Title: Business Intelligence Master Dimensions API
# Author: Guilherme Matheus
# Date: Script created on 15.10.2021
# Script and data info: Flask application to create an API to access master dimensions
#                       See readme.md in git repo for more info: https://github.com/guimatheus92
# --------------------------------------------------------------------------------------------------#

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import os
import pathlib

# Launching an app flask
app = Flask(__name__)
api = Api(app, default_mediatype='application/json')

class Index(Resource):
    def get(self):
        index_data = [
        {
            "href": "/webservice/rest/dimensioncalendar",
            "name": "Dimension Calendar",
            "description": "Dimension Calendar endpoint with date attributes"
        }
        ]
        return (index_data), 200

class DimensionCalendar(Resource):
    def get(self):

        # Initialize reparse from Flask
        parser = reqparse.RequestParser()
        # Add arguments
        parser.add_argument('start_dt')
        parser.add_argument('end_dt')
        parser.add_argument('lang')

        args = parser.parse_args()  # parse arguments to dictionary

        # Read CSV file    
        data = pd.read_csv(os.path.join(os.path.sep, pathlib.Path(__file__).parent.resolve(), "static", "csv", "DimensionCalendar.csv"))

        # If parameters on API is not null then filter dataframe by start date and end date
        if args['start_dt'] is not None and args['end_dt'] is not None:
            data = data.loc[(data['DT_SHORTDATE'] >= str(args['start_dt'])) & (data['DT_SHORTDATE'] <= str(args['end_dt']))]
        elif args['start_dt'] is not None and args['end_dt'] is None:
            data = data.loc[data['DT_SHORTDATE'] == str(args['start_dt'])]
        
        if args['lang'] == 'pt-br':
            data.columns = ['DT_DATA', 'NR_ANO', 'NR_MES', 'NR_DIA', 'NM_MES', 'NM_DIADASEMANA', 'NR_MESANO', 'NM_MESANO', 'NM_DATALONGA', 'NR_DIADASEMANA', 'NR_DIADOANO', 'NR_SEMESTRE', 'NM_SEMESTRE', 'NR_QUADRIMESTRE', 'NR_TRIMESTRE', 'NM_TRIMESTRE', 'NR_BIMESTRE', 'NM_BIMESTRE', 'NR_ANORELATIVO', 'NR_MESRELATIVO', 'NR_DIARELATIVO', 'NR_DATA', 'NR_ANOMES', 'NR_ANOTRIMESTRE', 'IC_DIAUTIL', 'IC_FINALDESEMANA', 'IC_FERIADO', 'IC_ANOATUAL', 'IC_MESATUAL', 'IC_DATAATUAL', 'IC_ANOPASSADO', 'IC_MESPASSADO', 'IC_ONTEM', 'LINDATA', 'LINORIGEM']

        # Convert dataframe to dictionary
        data = data.to_dict()
        # Return data and 200 OK code
        return (data), 200

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

# '/dimensioncalendar' is our entry point for DimensionCalendar
api.add_resource(DimensionCalendar, '/webservice/rest/dimensioncalendar')
# '/Index' is our entry point for Index
api.add_resource(Index, '/webservice/rest/')

# Run our Flask app
if __name__ == '__main__':
    app.run()