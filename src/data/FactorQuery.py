import requests #used for query
import json     #used for parsing data
import datetime #used to get current date
import copy
from utilities.SaveLoadJson import SaveLoadJson
from utilities.Search import Search

class FactorQuery:
    debug = False
    filename = 'parameters.txt'
    averageRating = 'AverageRatings.txt'
    api_key_file = 'api_keys.txt'
    outputFile = 'ratings.txt'
    companyFile = 'companies.tsv'
    
    resultStruct = {
                    "id":"",
                    "total_works":0,
                    "works":[]
                     }

    dateMovie = 0

    @staticmethod
    def getPerson(id, api_key):
        response = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "/combined_credits?api_key=" + api_key + "&language=en-US") #query
        if(response.status_code != 200):
            return "NULL"
        
        return response.json() #parse data into json

    @staticmethod
    def getCompany(id, api_key):
        page = 1
        rating = 0.0
        with open(FactorQuery.companyFile, 'r') as f:
            for line in f:
                line=line.split('\t')
                if len(line) > 0 and int(line[0]) == id:
                    return float(line[1])
                    
        rating=[]
        total=0
        while page != 0:
            print("Getting company movies. Page: " + str(page))
            response = requests.get("https://api.themoviedb.org/3/company/" + str(id) + "/movies?api_key=" + api_key + "&language=en-US&page=" + str(page))
            if(response.status_code != 200):
                return "NULL"

            response = response.json()
            for item in response["results"]:
                temp = Search.find(str(item["id"]))
                if temp != "NULL":
                    rating.append(float(temp.split('\t')[2]))
                    total += 1
                    
            if page == response["total_pages"]:
                page = 0
            else:
                page += 1

        avg = 0.0
        for i in rating:
            avg += float(i)
        rating = avg/float(total)
        with open(FactorQuery.companyFile, 'a') as f:
            f.write(str(id) + '\t' + str(format(rating,'.1f')) + '\n')

        print(str(rating))
        return rating
                    

    # Get Job -----------------------------------------------------
    @staticmethod
    def getJob(id, api_key, job):

        now = datetime.datetime.now()                                   #get current time to compare release date to
        total = 0                                                       #int for total works
        data = FactorQuery.getPerson(id, api_key)
        results = copy.deepcopy(FactorQuery.resultStruct)

        for val in data["crew"]:                                                                        #loop through all keys in json dictionary
            if(val["media_type"] == "movie" and val["job"] == job and "release_date" in val):    #check movie type, if director, and contains release date						#divide release date up into comparable parts
                dateNow = int(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))
                date = dateNow
                if FactorQuery.dateMovie != 0:
                    dateNow = FactorQuery.dateMovie
                if(val["release_date"] != ""):
                    date = int(val["release_date"].replace("-", ""))                                    #TODO: replace dateNow with date of movie being looked at
                if(dateNow > date):
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
        results["id"] = id
        if FactorQuery.debug == True:
            print("Found " + str(total) + " work(s) for " + results["name"])
        return results                                                                                  #return json data

    # Get Actor -----------------------------------------------------
    @staticmethod
    def getActor(id, api_key):
        
        now = datetime.datetime.now()
        total = 0
        data = FactorQuery.getPerson(id, api_key)
        results = copy.deepcopy(FactorQuery.resultStruct)

        for val in data["cast"]:
            if(val["media_type"] == "movie" and "release_date" in val):                                 #check movie type, if director, and contains release date
                dateNow = int(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))          #TODO: replace dateNow with date of movie being looked
                date = dateNow
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
        results["id"] = id
        if FactorQuery.debug == True:
            print("Found " + str(total) + " work(s) for " + results["name"])
        return results

    # Get Department -----------------------------------------------------
    @staticmethod
    def getDepartment(id, api_key, department):

        now = datetime.datetime.now()                                   #get current time to compare release date to
        total = 0                                                       #int for total works
        data = FactorQuery.getPerson(id, api_key)
        results = copy.deepcopy(FactorQuery.resultStruct)

        for val in data["crew"]:                                                                        #loop through all keys in json dictionary
            if(val["media_type"] == "movie" and val["department"] == department and "release_date" in val):    #check movie type, if director, and contains release date						#divide release date up into comparable parts
                dateNow = int(str(now.year) + str(now.month).zfill(2) + str(now.day).zfill(2))
                date = dateNow
                if FactorQuery.dateMovie != 0:
                    dateNow = FactorQuery.dateMovie
                if(val["release_date"] != ""):
                    date = int(val["release_date"].replace("-", ""))                                    #TODO: replace dateNow with date of movie being looked at
                if(dateNow > date):
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
        results["id"] = id
        if FactorQuery.debug == True:
            print("Found " + str(total) + " work(s) for " + results["name"])
        return results                                                                                  #return json data

    # Get Factor ------------------------------------------------------
    @staticmethod
    def getFactors(debug=False):
        FactorQuery.debug = debug
        if debug == True:
            print("Getting factors")
        api_key = SaveLoadJson.load(FactorQuery.api_key_file)["TMDB"]["key"]                         # get api key to be used for all queries
        parameters = SaveLoadJson.load(FactorQuery.filename)                                                #set data to something to prevent error
        avgRating = SaveLoadJson.load(FactorQuery.averageRating)
        
        data = {
            "Directors":[],
            "Actors":[],
            "Writers":[],
            "Producers":[],
            "Genres":[],
            "Average":[],
            "Company":[]
            }

        #Genres -------------------------------------------------
        for genre in parameters["Genre"]:
            if genre in avgRating["Genres"]:
                data["Genres"].append(avgRating["Genres"][genre])
        data["Average"].append(avgRating["Average"])

        #Companies ----------------------------------------------
        if "Production_companies" in parameters:
            if debug == True:
                print("Geting ratings for " + str(len(parameters["Production_companies"])) + " companies.")
            for company in parameters["Production_companies"]:
                data["Company"].append(FactorQuery.getCompany(company, api_key))

        #Date ---------------------------------------------------
        if "Date" in parameters:
            FactorQuery.dateMovie = parameters["Date"]

        #Directors ----------------------------------------------
        if "Directors" in parameters:
            if debug == True:
                print("Getting works for " + str(len(parameters["Directors"])) + " director(s)")
            for dctr in parameters["Directors"]:
                data["Directors"].append(FactorQuery.getJob(dctr, api_key, "Director"))

        #Actors -------------------------------------------------
        if "Actors" in parameters:
            iMax = 4#Change this number for the number of Actors
            i = 0
            if debug == True:
                if len(parameters["Actors"]) > iMax:
                    print("Getting works for " + str(iMax) + " actor(s)")
                else:
                    print("Getting works for " + str(len(parameters["Actors"])) + " actor(s)")
            for actr in parameters["Actors"]:
                i+=1
                if i > iMax:
                    break
                data["Actors"].append(FactorQuery.getActor(actr, api_key))

        #Writers ------------------------------------------------
        if "Writers" in parameters:
            iMax = 4
            i = 0
            if debug == True:
                print("Getting works for " + str(len(parameters["Writers"])) + " writer(s)")
            for wrtr in parameters["Writers"]:
                i+=1
                if i > iMax:
                    break
                data["Writers"].append(FactorQuery.getDepartment(wrtr, api_key, "Writing"))

        #Producers ---------------------------------------------
        if "Producers" in parameters:
            if debug == True:
                print("Getting works for " + str(len(parameters["Producers"])) + " producer(s)")
            for prdcr in parameters["Producers"]:
                data["Producers"].append(FactorQuery.getDepartment(prdcr, api_key, "Production"))
        #print(json.dumps(data, indent=2))
        SaveLoadJson.save(FactorQuery.outputFile, data)
