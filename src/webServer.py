from bottle import Bottle, run, template

import json
from data.FactorQuery import FactorQuery as FQ
from data.GetParameters import GetParameters as GP
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from models.Stats import Stats as stats

app = Bottle()

@app.route('/')
@app.route('/find/<movie>')
def find(movie='ABC'):

    temp = GP.find(movie,debug=True,oldRatings=True)

    if temp == '0':
        FQ.getFactors(debug=True)
        temp = stats.analyze()

    msg = str('The predicted rating of:\n'+str(movie)+'\n'+temp+'/10')
    
    return template(msg)

run(app, host='0.0.0.0', port=8080)
#run(app, host='localhost', port=8080)
