import json
import os

class SaveLoadJson:
    temp = {"data":"NULL"}

    @staticmethod
    def load(filename):
        if not os.path.exists(filename):
            return SaveLoadJson.temp
        
        file = open(filename, "r")
        string = file.read()
        file.close()
        #print(string)
        return json.loads(string)

    @staticmethod
    def save(filename, string):
        if os.path.exists(filename):
            os.remove(filename)
        file = open(filename, "w")
        file.write(json.dumps(string, indent=2))
        file.close()
