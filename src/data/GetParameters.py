# Packages ---------------------------------------------------------------------
import requests
import json
import copy
from utilities.SaveLoadJson import SaveLoadJson
from utilities.Search import Search

# Class ------------------------------------------------------------------------
class GetParameters:
    # Global Variables ---------------------------------------------------------
    filename = 'parameters.txt'
    api_key_file = 'api_keys.txt'

    oldData = True
    saveFile = 'dataStore.txt'

    tempJson = {"Date":0,
                "Title":"",
                "Genre":[],
                "Rating":0,
                "Directors":[],
                "Actors":[],
                "Writers":[],
                "Producers":[]
                }
    
    # Functions ----------------------------------------------------------------
    # GetID - takes movie name, returns int ------------------------------------
    def getID(string):
        inpt = string.replace(' ', '%20')

        api_key = SaveLoadJson.load(GetParameters.api_key_file)["TMDB"]["key"]
        
        url = ["https://api.themoviedb.org/3/search/movie?api_key=","&language=en-US&query=","&page=1&include_adult=false"]

        payload = "{}"
        response = requests.request("GET", url[0]+api_key+url[1]+inpt+url[2], data=payload)
        
        data = response.json()
        if len(data["results"]) > 0:
            return data["results"][0]["id"]
        return '-1'

    # GetDetails - takes ID, returns movie details -----------------------------
    def getDetails(ID):
        api_key = SaveLoadJson.load(GetParameters.api_key_file)["TMDB"]["key"]

        url = ["https://api.themoviedb.org/3/movie/","?api_key="]

        payload = "{}"
        response = requests.request("GET", url[0]+str(ID)+url[1]+api_key, data=payload)

        data = response.json()
        return data

    # GetCredits - takes ID, returns movie credits -----------------------------
    def getCredits(ID):
        api_key = SaveLoadJson.load(GetParameters.api_key_file)["TMDB"]["key"]

        url = ["https://api.themoviedb.org/3/movie/","/credits?api_key="]

        payload = "{}"
        response = requests.request("GET", url[0]+str(ID)+url[1]+api_key, data=payload)

        data = response.json()
        return data

    #Takes in movie ID and queries parameters ----------------------------------
    def get(ids, debug=False):
        result = copy.deepcopy(GetParameters.tempJson)
    
        Movie = GetParameters.getDetails(ids)
        if debug == True:
            print(Movie["title"])

        #Check if already have the rating
        if GetParameters.oldData == True:
            oldRatings = SaveLoadJson.load(GetParameters.saveFile)
            oldRatings["totalRequests"] += 1
            for i in oldRatings['ratings']:
                if i[0] == Movie['title']:
                    oldRatings["totalQueries"] += 2
                    SaveLoadJson.save(GetParameters.saveFile, oldRatings)
                    return i
            SaveLoadJson.save(GetParameters.saveFile, oldRatings)

        #Find date and title ----------------
        if Movie["release_date"] != "":
            result["Date"] = int(Movie["release_date"].replace("-",""))
        result["Title"] = Movie["title"]

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
        
        details = GetParameters.getCredits(Movie["id"])
        #Find crew --------------------------
        for person in details["crew"]:
            if person["job"] == "Director":
                result["Directors"].append(person["id"])
            if person["department"] == "Writing":
                result["Writers"].append(person["id"])
            if person["job"] == "Producer":
                result["Producers"].append(person["id"])

        #find cast --------------------------
        for person in details["cast"]:
            result["Actors"].append(person["id"])

        #Save data --------------------------
        SaveLoadJson.save(GetParameters.filename, result)
        return ['Getting Movie','0']

    #Called when you have a movie name --------------------------------------
    #Finds the movie ID from that string
    def find(string, debug=False, oldRatings=True):
        GetParameters.oldData = oldRatings
        
        ids = GetParameters.getID(string)
        if ids == '-1':
            return ['No Movie Found', '-1']
        return GetParameters.get(ids, debug)
