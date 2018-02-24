import json
from data.FactorQuery import FactorQuery as FQ
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from data.GetParameters import GetParameters as GP

# Replace with statistics script -----------------------------------------------
from models.Stats import Stats as stats
# ------------------------------------------------------------------------------

movie = "0"

while movie != "":
    print(" ")
    movie = input("Enter a movie name! \n")
    print(" ")

    temp = GP.find(movie,debug=True, oldRatings=False) #Danielle and Brandon's code

    if temp == '0':
        FQ.getFactors(debug=True) #get ratings for those parameters //my code
        stats.analyze() #the ratings and get rating #Ari, Ivy, Jake's code
    else:
        print(temp)
