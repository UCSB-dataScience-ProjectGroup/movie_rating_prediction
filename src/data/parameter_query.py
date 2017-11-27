import requests #used for query
import json     #used for parsing data
import datetime #used to get current time

class GetParameter:
    def getAPI_Key():
        fo = open("api_keys.txt", "r")  #open file with api key
        string = fo.read()              #copy file to string
        temp = json.loads(string)       #parse string to json
        fo.close()                      #close file
        return temp["themoviedb"]       #return key for chosen api

    # Get Director -----------------------------------------------------
    def getDirector(id, api_key):

        now = datetime.datetime.now()                                   #get current time to compare release date to

        total = 0                                                       #int for total works

        response = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "/combined_credits?api_key=" + api_key + "&language=en-US") #query
        if(response.status_code != 200):
            return "Error: unable to reach api"
        
        data = response.json() #parse data into json

        results = {"works":[],          #temp dictionary for output
                   "total_works": 0,
                   "awards":"unknown"}

        for val in data["crew"]:                                                                        #loop through all keys in json dictionary
            if(val["media_type"] == "movie" and val["job"] == "Director" and "release_date" in val):    #check movie type, if director, and contains release date						#divide release date up into comparable parts
                dateNow = int(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))
                date = dateNow
                if(val["release_date"] != ""):
                    date = int(val["release_date"].replace("-", ""))                                    #TODO: replace dateNow with date of movie being looked at
                if(dateNow > date):                                                                     #check if movie has been released yet....
                    print(json.dumps(val, indent=2))
                    temp = {"title":val["original_title"],                                              #create a temp dict with wanted values
                            "rating":val["vote_average"],
                            "popularity":val["popularity"],
                            "release_date":val["release_date"]}     
                    results["works"].append(temp)                                                       #add temp dict to list of all works
                    total += 1                                                                          #add work to total

        results["total_works"] = total;                                                  #add total to list of works
        return results                                                                                  #return json data

    # Get Actor -----------------------------------------------------
    def getActor(id, api_key):
        
        now = datetime.datetime.now()

        total = 0

        response = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "/combined_credits?api_key=" + api_key + "&language=en-US")
        if(response.status_code != 200):
            return "Error: unable to reach api"

        data = response.json()

        results = {"works":[],
                   "total_works":0,
                   "awards":"unknown"}

        for val in data["cast"]:
            if(val["media_type"] == "movie" and "release_date" in val):                                 #check movie type, if director, and contains release date
                dateNow = int(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))          #TODO: replace dateNow with date of movie being looked at
                date = dateNow
                if(val["release_date"] != ""):
                    date = int(val["release_date"].replace("-", ""))
                if(dateNow > date):                                                                     #check if movie has been released yet....
                    temp = {"title":val["original_title"],                                              #create a temp dict with wanted values
                            "rating":val["vote_average"],
                            "popularity":val["popularity"],
                            "release_date":val["release_date"]}     
                    results["works"].append(temp)                                                       #add temp dict to list of all works
                    total += 1
                    
        results["total_works"] = total;
        return results

    # Get Factor ------------------------------------------------------    
    def getFactor(id, parameter="Director"):
        print("Getting factor")
        api_key = GetParameter.getAPI_Key()                     # get api key to be used for all queries
        data = 0                                                #set data to something to prevent error
        if(parameter == "Director"):                            #check parameter we're looking for
            data = GetParameter.getDirector(id, api_key)        #call query to get paramters
        if(parameter == "Actor"):
            data = GetParameter.getActor(id, api_key)
        return data                                             #return data
