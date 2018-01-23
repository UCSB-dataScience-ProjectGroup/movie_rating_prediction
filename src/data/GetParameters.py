# Packages ---------------------------------------------------------------------
import requests
import json
import copy
from data.SaveLoadJson import SaveLoadJson

# Class ------------------------------------------------------------------------
class GetParameters:
    # Global Variables ---------------------------------------------------------
    filename = 'parameters.txt'
    api_key_file = 'api_keys.txt'

    tempJson = {"Date":0,
                "Title":"",
                "Directors":[],
                "Actors":[]
                }

    # Functions ----------------------------------------------------------------
    def getID(string):
        inpt = string.replace(' ', '%20')

        api_key = SaveLoadJson.load(GetParameters.api_key_file)["TMDB"]["key"]
        
        url = ["https://api.themoviedb.org/3/search/movie?api_key=","&language=en-US&query=","&page=1&include_adult=false"]

        payload = "{}"
        response = requests.request("GET", url[0]+api_key+url[1]+inpt+url[2], data=payload)
        
        data = response.json()
        return data["results"][0]

    def getDetails(ID):
        api_key = SaveLoadJson.load(GetParameters.api_key_file)["TMDB"]["key"]

        url = ["https://api.themoviedb.org/3/movie/","/credits?api_key="]

        payload = "{}"
        response = requests.request("GET", url[0]+str(ID)+url[1]+api_key, data=payload)

        data = response.json()
        return data


    def find(string):
        result = copy.deepcopy(GetParameters.tempJson)
    
        Movie = GetParameters.getID(string)
        result["Date"] = int(Movie["release_date"].replace("-",""))
        result["Title"] = Movie["title"]
        
        details = GetParameters.getDetails(Movie["id"])
        #Find crew
        for person in details["crew"]:
            #Find directors
            if person["job"] == "Director":
                result["Directors"].append(person["id"])

        #find cast
        for person in details["cast"]:
            result["Actors"].append(person["id"])

        SaveLoadJson.save(GetParameters.filename, result)
    
