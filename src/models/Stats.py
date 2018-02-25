import json
from utilities.SaveLoadJson import SaveLoadJson

class Stats:
    filename = 'ratings.txt'
    filename2 = 'parameters.txt'
    outputFile = 'results.txt'
    saveFile = 'oldRatings.txt'

    def adjust(weights, avgHold):
        total = 0
        for key, value in weights.items():
            if avgHold[key][0] > 0.0:
                total += value
        total = 1 / total
        for key, value in weights.items():
            weights[key] = total*value
    
    def analyze():

        works = ["Actors","Directors","Writers","Producers"]
        values = ["Genres", "Average"]

        weights = {"Actors":0.5,
                   "Directors":0.5,
                   "Writers":0.5,
                   "Producers":0.5,
                   "Genres":0.5,
                   "Average":0.5,
                   "Max":0.5
                   }

        avgHold = {"Actors":[0.0,0,0.0],
                   "Directors":[0.0,0,0.0],
                   "Writers":[0.0,0,0.0],
                   "Producers":[0.0,0,0.0],
                   "Genres":[0.0,0,0.0],
                   "Average":[0.0,0,0.0],
                   "Max":[10.0,1,0.0]
                   }

        print("Doing math!")
        factors = SaveLoadJson.load(Stats.filename)
        parameters = SaveLoadJson.load(Stats.filename2)

        observed = 0.0

        #Stuff with works
        for key in works:
            for person in factors[key]:
                for item in person["works"]:
                    if item["rating"] != "0":
                        avgHold[key][0] += float(item["rating"])
                avgHold[key][1] += float(person["total_works"])

        #Stuff with averages
        for key in values:
            avgHold[key][0] = sum(factors[key])
            avgHold[key][1] = len(factors[key])

        Stats.adjust(weights, avgHold)

        for key, value in avgHold.items():
            if(value[0] > 0):
                avgHold[key][0] = value[0]/value[1]
                avgHold[key][2] = (value[0])*weights[key]
                observed += avgHold[key][2]

        #Printing results --------------------------------------
        #print(json.dumps(weights, indent=2))
        #print(json.dumps(avgHold, indent=2))
        print("Average movie Rating: ", format(observed,'.1f'))
        
        print("Actual movie Rating: ", end="")
        print(parameters["Rating"])

        #Save Ratings to file
        oldRatings = SaveLoadJson.load(Stats.saveFile)
        oldRatings[parameters["Title"]] = str(format(observed, '.1f'))
        SaveLoadJson.save(Stats.saveFile, oldRatings)

        #Percent error and return ------------------------------
        percentError = 0
        if float(parameters["Rating"]) != 0:
            percentError = (abs(float(parameters["Rating"])-observed)/float(parameters["Rating"]))*100
        print("Percent error: ", format(percentError,'.3f'),"%")  

        return [parameters["Title"], str(format(observed, '.1f'))]
