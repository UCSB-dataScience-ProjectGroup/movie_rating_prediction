from flask import Flask, request, redirect, send_file
from flask_cors import CORS, cross_origin

from werkzeug.contrib.fixers import ProxyFix

import json
from data.FactorQuery import FactorQuery
from data.GetParameters import GetParameters
from utilities.SaveLoadJson import SaveLoadJson
from models.Stats import Stats
from utilities.getInfo import getData

import subprocess

app = Flask(__name__)
CORS(app, support_credentials=True)

#Instances
GD = getData()
FQ = FactorQuery()
GP = GetParameters()
SLJ = SaveLoadJson
stats = Stats()


@app.route('/')
@cross_origin(supports_credentials=True)
def hello():
    return redirect("https://ucsb-datascience-projectgroup.github.io/movie_rating_prediction/", code=302)

@app.route('/find/<movie>', methods=['GET'])
@cross_origin(supports_credentials=True)
def find(movie):
    temp = GP.find(movie,debug=True,oldRatings=True)

    if temp[1] == '0':
        FQ.getFactors(debug=False)
        temp = stats.analyze()

    msg = str(temp[0]+'%314'+temp[1])
    
    return msg

@app.route('/config', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCfg():
    return send_file('utilities/config.html')

@app.route('/config/data/get/<typ>', methods=['GET'])
@cross_origin(supports_credentials=True)
def getData(typ):
    if typ == 'DATA':
        return GD.getDATA()
    if typ == 'ACC':
        return GD.getAccess()
    return ''

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    print("Starting REEL RATINGS server")
    app.run(port=8000)
    app.add_command(threaded=True)
