# Packages ---------------------------------------------------------------------
import requests
import json
import copy
from utilities.SaveLoadJson import SaveLoadJson
from utilities.Search import Search

# Class ------------------------------------------------------------------------
class GetParameters:
    # Global Variables ---------------------------------------------------------
    filename = 'parameters.txt' #File to save to
    api_key_file = 'api_keys.txt' #File with api keys (DUH)
    api_key = ''

    oldData = True #Should old data be used
    saveFile = 'dataStore.txt' #Where old data is stored

    output = {"Name":"Unknown",
              "Average":"0.0",
              "Actual":"0.0",
              "Error":"0",
              "Id":"-1",
              "Imdb_id":"tt0000000"}
    
    tempJson = {"Date":0,
                "Id":"0",
                "Imdb_id":"tt0000000",
                "Title":"",
                "Genre":[],
                "Rating":0,
                "Directors":[],
                "Actors":[],
                "Writers":[],
                "Producers":[],
                "Budget":0,
                "Production_companies":[]
                }
    
    # Functions ----------------------------------------------------------------
    # GetID - takes movie name, returns int ------------------------------------
    @staticmethod
    def getID(string):
        inpt = string.replace(' ', '%20')
        string = string.lower()
        
        url = ["https://api.themoviedb.org/3/search/movie?api_key=","&language=en-US&query=","&page=1&include_adult=false"]

        payload = "{}"
        response = requests.request("GET", url[0]+GetParameters.api_key+url[1]+inpt+url[2], data=payload)
        
        data = response.json()
        iMax = 3
        i = 0
        if len(data["results"]) > 0:
            for item in data["results"]:
                i+=1
                if i > iMax:
                    break
                #print(string +"=="+item["title"].lower())
                if string == item["title"].lower():
                    return item["id"]
            return data["results"][0]["id"]
        return '-1'

    # GetDetails - takes ID, returns movie details -----------------------------
    @staticmethod
    def getDetails(ID):
        url = ["https://api.themoviedb.org/3/movie/","?api_key="]

        payload = "{}"
        response = requests.request("GET", url[0]+str(ID)+url[1]+GetParameters.api_key, data=payload)

        data = response.json()
        #print(json.dumps(data, indent=2))
        return data

    # GetCredits - takes ID, returns movie credits -----------------------------
    @staticmethod
    def getCredits(ID):
        url = ["https://api.themoviedb.org/3/movie/","/credits?api_key="]

        payload = "{}"
        response = requests.request("GET", url[0]+str(ID)+url[1]+GetParameters.api_key, data=payload)

        data = response.json()
        #print(json.dumps(data, indent=2))
        return data

    #Takes in movie ID and queries parameters ----------------------------------
    @staticmethod
    def get(ids, debug=False):
        result = copy.deepcopy(GetParameters.tempJson)
        
        Movie = GetParameters.getDetails(ids)
        if debug == True:
            print(Movie["title"])

        #Find date and title ----------------
        if Movie["release_date"] != "":
            result["Date"] = int(Movie["release_date"].replace("-",""))
        result["Title"] = Movie["title"]
        result["Id"]=str(ids)
        result["Imdb_id"]=Movie["imdb_id"]
        
        #Save genres ------------------------
        for genre in Movie["genres"]:
            result["Genre"].append(genre["name"])

        #Find rating ------------------------
        rating = "0\t0\t0\t0\n"
        temprating = Search.find(Movie["id"])
        if temprating != "NULL":
            rating = temprating
        rating = rating.split('\t')
        result["Rating"] = rating[2]

        #Production companies --------------
        for company in Movie["production_companies"]:
            result["Production_companies"].append(company["id"])

        #Budget ---------------------------
        result["Budget"] = Movie["budget"]
        
        details = GetParameters.getCredits(Movie["id"])
        #Crew ------------------------------
        for person in details["crew"]:
            if person["job"] == "Director":
                result["Directors"].append(person["id"])
            if person["department"] == "Writing":
                result["Writers"].append(person["id"])
            if person["job"] == "Producer":
                result["Producers"].append(person["id"])

        #Actors -----------------------------
        for person in details["cast"]:
            result["Actors"].append(person["id"])

        #Save data --------------------------
        SaveLoadJson.save(GetParameters.filename, result)
        return {"Id":"0"}

    #Called when you have a movie name --------------------------------------
    #Finds the movie ID from that string
    @staticmethod
    def find(string, debug=False, oldRatings=True):
        GetParameters.oldData = oldRatings #Copy choice for using old data
        GetParameters.api_key = SaveLoadJson.load(GetParameters.api_key_file)["TMDB"]["key"]
        
        ids = GetParameters.getID(string)
        if ids == '-1':
            return GetParameters.output
        else:
            #Check if already have the rating
            if GetParameters.oldData == True:
                oldRatings = SaveLoadJson.load(GetParameters.saveFile)
                oldRatings["totalRequests"] += 1
                for i in oldRatings['ratings']:
                    i=json.loads(i)
                    if i["Id"] == str(ids):
                        oldRatings["totalQueries"] += 1
                        SaveLoadJson.save(GetParameters.saveFile, oldRatings)
                        return i
                SaveLoadJson.save(GetParameters.saveFile, oldRatings)

        return GetParameters.get(ids, debug)
