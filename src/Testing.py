import json
import random
from data.FactorQuery import FactorQuery as FQ
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from data.GetParameters import GetParameters as GP
from utilities.Search import Search

# Replace with statistics python script ----------------------------------------
from models.myStats import myStats as stats
# ------------------------------------------------------------------------------

#Enter number of movie to check
print(" ")
loops = input("Enter movies to check: \n")

#Initialize average values
totalError = 0.0
times = int(loops)

#Loops chosen times
for i in range(int(loops)):
    print(" ")

    #Find random ID value
    ids = 2
    valid = False
    while valid == False:
        ids = random.randint(2,489280)
        #Make sure random value has non-0 rating
        tempVal = Search.find(ids)
        if tempVal != "NULL":
            if float(tempVal.split('\t')[2]) > 0:
                valid = True

    #Get parameters and ratings
    GP.get(ids,debug=True)
    FQ.getFactors(debug=True)

    #Get Average rating and average % error
    Error = stats.analyze()
    if Error != 100:
        totalError += Error
    else:
        times -= 1

#Print total error
print("\nTotal Average error: ", format(totalError/int(loops),'.2f'),"%")
