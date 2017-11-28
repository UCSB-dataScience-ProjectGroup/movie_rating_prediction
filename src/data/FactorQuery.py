import requests #used for query
import json     #used for parsing data
import datetime #used to get current date
from data.SaveLoadJson import SaveLoadJson
from data.Search import Search

class FactorQuery:
    filename = 'parameters.txt'
    api_key_file = 'api_keys.txt'
    outputFile = 'ratings.txt'
    
    params = ["Directors","Actors"]
    resultStruct = {
                    "works":[],
                    "total_works":0,
                    "name":""
                     }

    dateMovie = 0
    
    def getPerson(id, api_key):
        response = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "/combined_credits?api_key=" + api_key + "&language=en-US") #query
        if(response.status_code != 200):
            return "NULL"
        
        return response.json() #parse data into json

    def getName(id, api_key):
        response = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "?api_key=" + api_key + "&language=en-US")
        if(response.status_code != 200):
            return "NULL"
        
        return response.json()["name"]

    def getMovie(id, api_key):
        response = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + api_key + "&language=en-US") #query
        if(response.status_code != 200):
            return "NULL"
        
        return response.json() #parse data into json


    # Get Director -----------------------------------------------------
    def getDirector(id, api_key):

        now = datetime.datetime.now()                                   #get current time to compare release date to
        total = 0                                                       #int for total works
        data = FactorQuery.getPerson(id, api_key)
        results = FactorQuery.resultStruct.copy()

        for val in data["crew"]:                                                                        #loop through all keys in json dictionary
            if(val["media_type"] == "movie" and val["job"] == "Director" and "release_date" in val):    #check movie type, if director, and contains release date						#divide release date up into comparable parts
                dateNow = int(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))
                if FactorQuery.dateMovie != 0:
                    dateNow = FactorQuery.dateMovie
                if(val["release_date"] != ""):
                    date = int(val["release_date"].replace("-", ""))                                    #TODO: replace dateNow with date of movie being looked at
                if(dateNow > date):                                                                     #check if movie has been released yet....
                    rating = "0\t0\t0\t0\n"
                    temprating = Search.find(val["id"])
                    if temprating != "NULL":
                        rating = temprating
                    rating = rating.split('\t')                        
                    temp = {"title":val["original_title"],                                              #create a temp dict with wanted values
                            "rating":rating[2],
                            "votes":rating[3][:-1],
                            "release_date":val["release_date"]}     
                    results["works"].append(temp)                                                       #add temp dict to list of all works
                    total += 1                                                                          #add work to total

        results["total_works"] = total;#add total to list of works
        results["name"] = FactorQuery.getName(id, api_key)
        return results                                                                                  #return json data

    # Get Actor -----------------------------------------------------
    def getActor(id, api_key):
        
        now = datetime.datetime.now()
        total = 0
        data = FactorQuery.getPerson(id, api_key)
        results = FactorQuery.resultStruct.copy()

        for val in data["cast"]:
            if(val["media_type"] == "movie" and "release_date" in val):                                 #check movie type, if director, and contains release date
                dateNow = int(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))          #TODO: replace dateNow with date of movie being looked 
                if FactorQuery.dateMovie != 0:
                    dateNow = FactorQuery.dateMovie
                if(val["release_date"] != ""):
                    date = int(val["release_date"].replace("-", ""))
                if(dateNow > date):                                                                     #check if movie has been released yet....
                    rating = "0\t0\t0\t0\n"
                    temprating = Search.find(val["id"])
                    if temprating != "NULL":
                        rating = temprating
                    rating = rating.split('\t')                        
                    temp = {"title":val["original_title"],                                              #create a temp dict with wanted values
                            "rating":rating[2],
                            "votes":rating[3][:-1],
                            "release_date":val["release_date"]}     
                    results["works"].append(temp)                                                       #add temp dict to list of all works
                    total += 1    
                    
        results["total_works"] = total;
        results["name"] = FactorQuery.getName(id, api_key)
        return results

    # Get Factor ------------------------------------------------------    
    def getFactors():
        print("Getting factor")
        api_key = SaveLoadJson.load(FactorQuery.api_key_file)["TMDB"]["key"]                         # get api key to be used for all queries
        parameters = SaveLoadJson.load(FactorQuery.filename)                                                #set data to something to prevent error
        #print(json.dumps(parameters, indent=2))
        data = {
            "Directors":[],
            "Actors":[]
            }
        if "Date" in parameters:
            FactorQuery.dateMovie = parameters["Date"]
        if "Directors" in parameters:
            for dctr in parameters["Directors"]:
                data["Directors"].append(FactorQuery.getDirector(dctr, api_key))
        if "Actors" in parameters:
            for actr in parameters["Actors"]:
                data["Actors"].append(FactorQuery.getActor(actr, api_key))
        #return data
        SaveLoadJson.save(FactorQuery.outputFile, data)
