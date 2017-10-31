from data.parameter_query import GetParameter    #Get parameter class to call query
import json                                 #json for output

person = "0"
data = ""

while person != "": #if input is empty then exit
    person = input("x(Spielberg = 488, Joss Whedon = 12891) \n Enter a director id: ") #Get input for director id from user
    print("")
    addition = 0
    mean = 0
    if(person != ""): #call director if not empty
        
        ### This is the code you really need V
        data = GetParameter.getFactor(person, parameter="Director")             #call getDirector method to start query
        print(json.dumps(data, indent=2))                                        #print output with indents
        length = 0
        for val in data["works"]:
            if("rating" in val):
                if(val["rating"] != 0):
                    length += 1
                    addition += val["rating"]
                    print(val["rating"])
    
    if(length > 0):
        mean = addition/length

    print("The following preview has been approved for a", round(mean,1), "rating!")
