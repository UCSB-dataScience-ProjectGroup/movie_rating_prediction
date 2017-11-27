from data.FactorQuery import FactorQuery    #Get parameter class to call query
import json                                 #json for output

print("Depreciated: use datacall_example.py instead")
'''
person = "0"
data = ""
while person != "": #if input is empty then exit
    person = input("ex(Spielberg = 488, Joss Whedon = 12891) \n Enter a director id: ") #Get input for director id from user
    print("")                                                                           
    if(person != ""): #call director if not empty
        data = FactorQuery.getFactor(person)                                                                 #call getDirector method to start query
        print(json.dumps(data, indent=2)) #print output with indents
        #print(data["works"]["title"]) prints first title in works
'''
