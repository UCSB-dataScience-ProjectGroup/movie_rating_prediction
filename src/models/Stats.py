import json
from utilities.SaveLoadJson import SaveLoadJson

class Stats:
    filename = 'ratings.txt'
    filename2 = 'parameters.txt'
    outputFile = 'results.txt'
    dataFile = 'dataStore.txt'

    @staticmethod
    def adjust(weights, newWeights, avgHold):
        total = 0
        for key, value in weights.items():
            if avgHold[key][0] > 0.0:
                total += value
        total = 1 / total
        for key, value in weights.items():
            newWeights[key] = total*value

    @staticmethod
    def analyze():

        works = ["Actors","Directors","Writers","Producers"]
        values = ["Genres", "Average"]

        newWeights = {}

        avgHold = {"Actors":[0.0,0,0.0],
                   "Directors":[0.0,0,0.0],
                   "Writers":[0.0,0,0.0],
                   "Producers":[0.0,0,0.0],
                   "Genres":[0.0,0,0.0],
                   "Average":[0.0,0,0.0],
                   "Max":[10.0,1,0.0],
                   "Min":[0.0001,1,0.0]
                   }

        print("Doing math!")
        factors = SaveLoadJson.load(Stats.filename)
        parameters = SaveLoadJson.load(Stats.filename2)
        data = SaveLoadJson.load(Stats.dataFile)

        weights = data["weights"]

        totalQueries = 3
        observed = 0.0

        #Stuff with works
        for key in works:
            for person in factors[key]:
                totalQueries += 1
                for item in person["works"]:
                    if item["rating"] != "0":
                        avgHold[key][0] += float(item["rating"])
                avgHold[key][1] += float(person["total_works"])

        #Stuff with averages
        for key in values:
            avgHold[key][0] = sum(factors[key])
            avgHold[key][1] = len(factors[key])

        Stats.adjust(weights, newWeights, avgHold)

        for key, value in avgHold.items():
            if(value[0] > 0):
                avgHold[key][0] = value[0]/value[1]
                avgHold[key][2] = (value[0])*newWeights[key]
                observed += avgHold[key][2]

        #Modify the weights for a better fit -------------------
        if float(parameters["Rating"]) != 0:
            modifier = 0.1
            if data["totalAdjusts"] > 10000:
                modifier = 0.00001
            elif data["totalAdjusts"] > 1000:
                modifier = 0.0001
            elif data["totalAdjusts"] > 100:
                modifier = 0.001
            elif data["totalAdjusts"] > 10:
                modifier = 0.01

            for key, value in avgHold.items():
                if value[0] != 0 and value[0] != float(parameters["Rating"]):
                    if value[0] > observed and float(parameters["Rating"]) > observed:
                        weights[key] = float("{0:.5f}".format(weights[key]+modifier))
                    if value[0] < observed and float(parameters["Rating"]) < observed:
                        weights[key] = float("{0:.5f}".format(weights[key]+modifier))
                    if value[0] > observed and float(parameters["Rating"]) < observed:
                        weights[key] = float("{0:.5f}".format(weights[key]-modifier))
                    if value[0] < observed and float(parameters["Rating"]) > observed:
                        weights[key] = float("{0:.5f}".format(weights[key]-modifier))

        #Printing results --------------------------------------
        print("Average movie Rating: ", format(observed,'.1f'))
        
        print("Actual movie Rating: " + str(parameters["Rating"]))

        #Save data to file --------------------------------------
        data["weights"] = weights
        data["totalQueries"] += totalQueries
        data["totalAdjusts"] += 1
        if len(data["ratings"]) > data["totalAdjusts"]/2 or len(data["ratings"]) > 1000:
            data["ratings"].pop(0)
        data["ratings"].append([parameters["Title"], str(format(observed, '.1f'))])
        SaveLoadJson.save(Stats.dataFile, data)

        #Percent error and return ------------------------------
        percentError = 0
        if float(parameters["Rating"]) != 0:
            percentError = (abs(float(parameters["Rating"])-observed)/float(parameters["Rating"]))*100
        print("Percent error: ", format(percentError,'.3f'),"%")  

        return [parameters["Title"], str(format(observed, '.1f'))]
