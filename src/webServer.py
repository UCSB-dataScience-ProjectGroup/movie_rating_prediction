from flask import Flask, request, redirect, send_file
from flask_cors import CORS, cross_origin

from werkzeug.contrib.fixers import ProxyFix

from utilities.getInfo import getData as GD
from dataCall import dataCall as DC

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/')
@cross_origin(supports_credentials=True)
def hello():
    return redirect("https://ucsb-datascience-projectgroup.github.io/movie_rating_prediction/", code=302)

@app.route('/find/<movie>', methods=['GET'])
@cross_origin(supports_credentials=True)
def find(movie): 
    return DC.findMovie(movie)

@app.route('/config/<token>', methods=['GET'])
@cross_origin(supports_credentials=True)
def getCfg(token):
    if token == 'aaaQlIstC5':
        return send_file('utilities/config.html')
    return''
@app.route('/config/data/get/<typ>', methods=['GET'])
@cross_origin(supports_credentials=True)
def getData(typ):
    if typ == 'DATA':
        return GD.getDATA()
    if typ == 'ACC':
        return GD.getAccess()
    return 'Denied'

@app.route('/config/data/get/log/', methods=['GET'])
@cross_origin(supports_credentials=True)
def getLog():
    return send_file('utilities/access.log')
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    print("Starting REEL RATINGS server")
    app.run(port=8000)
    app.add_command(threaded=True)
