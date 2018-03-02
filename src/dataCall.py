import json
from data.FactorQuery import FactorQuery as FQ
from data.GetParameters import GetParameters as GP
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from models.Stats import Stats as stats

class dataCall:
    @staticmethod
    def findMovie(movie):
        temp = GP.find(movie,debug=True,oldRatings=True)
        
        if temp["Id"] == '0':
            FQ.getFactors(debug=False)
            temp = stats.analyze()

        msg = str(json.dumps(temp))
        return msg
