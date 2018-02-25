from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin

import json
from data.FactorQuery import FactorQuery as FQ
from data.GetParameters import GetParameters as GP
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from models.Stats import Stats as stats

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

if __name__ == "__main__":
    print("Starting REEL RATINGS server")
    app.run(host='0.0.0.0', port=5000)
    app.add_command(threaded=True)
