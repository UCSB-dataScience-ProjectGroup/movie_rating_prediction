import json
from data.FactorQuery import FactorQuery
from data.SaveLoadJson import SaveLoadJson

filename = 'ratings.txt'

#getParameters() //Danielle and Brandon's code

FactorQuery.getFactors() #get ratings for those parameters //my code

#analyze() the ratings and get rating //Ari, Ivy, Jake's code

data = SaveLoadJson.load(filename) #to load ratings into json object
print(json.dumps(data, indent=2))
