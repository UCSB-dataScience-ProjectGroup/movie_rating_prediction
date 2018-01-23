import json
from data.FactorQuery import FactorQuery as FQ
from data.SaveLoadJson import SaveLoadJson as SLJ
from data.GetParameters import GetParameters as GP

filename = 'parameters.txt'
movie = "0"

while movie != "":
    print(" ")
    movie = input("Enter a movie name! \n")
    print(" ")

    GP.find(movie) #Danielle and Brandon's code

    FQ.getFactors() #get ratings for those parameters //my code

    #analyze() the ratings and get rating #Ari, Ivy, Jake's code

    data = SLJ.load(filename) #to load ratings into json object
    print(json.dumps(data, indent=2))
