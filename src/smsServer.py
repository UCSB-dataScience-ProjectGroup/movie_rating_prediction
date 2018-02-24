from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import json
from data.FactorQuery import FactorQuery as FQ
from data.GetParameters import GetParameters as GP
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from models.Stats import Stats as stats

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse()

    movie = request.form.get("Body")

    temp = GP.find(movie,debug=True,oldRatings=True)

    if temp == '0':
        FQ.getFactors(debug=True)
        temp = stats.analyze()

    resp.message('The predicted rating of:\n'+str(movie)+'\n'+temp+'/10!')
    return str(resp)

if __name__ == "__main__":
    print("Starting REEL RATINGS sms server")
    app.run(debug=True)
