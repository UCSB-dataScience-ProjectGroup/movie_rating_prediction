from flask import Flask, request, redirect, send_file
from flask_cors import CORS, cross_origin

import json
from data.FactorQuery import FactorQuery as FQ
from data.GetParameters import GetParameters as GP
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from models.Stats import Stats as stats

import subprocess

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/find/<movie>', methods=['GET'])
@cross_origin(supports_credentials=True)
def find(movie):
    temp = GP.find(movie,debug=True,oldRatings=True)

    if temp[1] == '0':
        FQ.getFactors(debug=True)
        temp = stats.analyze()

    msg = str(temp[0]+','+temp[1])
    
    return msg

@app.route('/config', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCfg():
    return send_file('utilities/config.html')

@app.route('/config/data/get', methods=['GET'])
@cross_origin(supports_credentials=True)
def getData():
    data = SLJ.load('dataStore.txt')

    proc = subprocess.Popen(['uptime'],stdout=subprocess.PIPE, shell=False)
    (out0, err) = proc.communicate()
    proc = subprocess.Popen(['uptime', '-p'],stdout=subprocess.PIPE, shell=False)
    (out1, err) = proc.communicate()
    
    result = (str(data["totalRequests"])+'\t'+
              str(data["totalQueries"])+'\t'+
              str(data["totalAdjusts"])+'\t'+
              str(float(str(out0).split(',')[4][:-3])*100)+'\t'+
              str(out1)[2:-3]+'\t'+
              str(out0)[2:11])
    return result

if __name__ == "__main__":
    print("Starting REEL RATINGS server")
    app.run(host='localhost', port=5000)
    app.add_command(threaded=True)
