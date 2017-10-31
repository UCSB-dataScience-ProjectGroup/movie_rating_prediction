from data.parameter_query import GetParameter    #Get parameter class to call query
import json                                 #json for output

person = "0"
data = ""
while person != "": #if input is empty then exit
    person = input("ex(SimonPegg = 11108, Ian McKellen = 1327) \n Enter a actor id: ") #Get input for director id from user
    print("")
    addition = 0
    mean = 0
    length =0;
    if(person != ""): #call director if not empty
        
        ### This is the code you really need V
        data = GetParameter.getFactor(person, parameter="Actor")                                                               #call getDirector method to start query
        print(json.dumps(data, indent=2)) #print output with indents
        ###
        for val in data["works"]:
            if("rating" in val):
                if(val["rating"] != 0):
                    length += 1
                    addition += val["rating"]
                    print(val["rating"])
        #print(data["works"]["title"])#prints first title in works
        mean = addition/(length)
        print("Mean: ", mean)
