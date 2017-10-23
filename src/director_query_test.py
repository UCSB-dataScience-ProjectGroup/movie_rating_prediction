import requests #used for query
import json     #used for parsing data
import datetime #used to get current time

def getDirector(id):

    now = datetime.datetime.now()                                   #get current time to compare release date to
    combined_credits = "person/" + str(id) + "/combined_credits"    #create string for api query

    total = 0                                                       #int for total works

    response = requests.get("https://api.themoviedb.org/3/" + combined_credits + "?api_key=" + api_key + "&language=en-US") #query
    data = response.json() #parse data into json
    
    #print(json.dumps(data, skipkeys=True, sort_keys=True, indent=2))

    for val in data["crew"]:                                                                        #loop through all keys in json dictionary
        if(val["media_type"] == "movie" and val["job"] == "Director" and "release_date" in val):    #check movie type, if director, and contains release date
            date = val["release_date"].split('-')                                                   #divide release date up into comparable parts
            if(now.year >= int(date[0])):                                                           #check if movie has been released yet.... TODO:FIX
                total += 1                                                                          #add work to total
                print(val["original_title"])                                                        #Print title, rating, popularity, release date, ect...
                #print(" Job: " + val["job"])
                print(" Rating: ", val["vote_average"])
                print(" Popularity: ", val["popularity"])
                print(" Year: " + val["release_date"])
                print("")

    print("Total works as director: " + str(total))                                                 #print total works number
    print("")

def getAPI_Key():
    fo = open("api_keys.txt", "r")  #open file with api key
    string = fo.read()              #copy file to string
    temp = json.loads(string)       #parse string to json
    fo.close()                      #close file
    return temp["themoviedb"]       #return key for themoviedb

# Main routine --------------------------------------------------------------------

api_key = getAPI_Key() # get api key to be used for all queries
person = "0" 
while person != "": #if input is empty then exit
    person = input("ex(Spielberg = 488, Joss Whedon = 12891) \n Enter a director id: ") #Get input for director id from user
    print("")                                                                           
    if(person != ""):
        getDirector(person)                                                                 #call getDirector method to start query
