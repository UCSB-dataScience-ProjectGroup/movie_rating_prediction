import linecache
import math
from utilities.LineCount import LineCount

class Search:
    IMDB = 'IMDBRatings.tsv'
    TMDB = 'TMDBRatings.tsv'
    maxTries = 25

    @staticmethod
    def findTMDB(searchID, minValue, maxValue, tries, file):
        tries = tries + 1
        half = int((maxValue-minValue)/2 + minValue)
        string = linecache.getline(file, half)
        curID = int(string.split('\t')[0])
        if tries > Search.maxTries:
            return "NULL"
        if searchID == curID:
            return string
        if searchID > curID:
            return Search.findTMDB(searchID, half, maxValue, tries, file)
        if searchID < curID:
            return Search.findTMDB(searchID, minValue, half, tries, file)
        return string

    @staticmethod
    def findIMDB(searchID, minValue, maxValue, tries, file):
        tries = tries + 1
        half = int((maxValue-minValue)/2 + minValue)
        string = linecache.getline(file, half)
        curID = int(string.split('\t')[1][2:9])
        if tries > Search.maxTries:
            return "NULL"
        if searchID == curID:
            return string
        if searchID > curID:
            return Search.findIMDB(searchID, half, maxValue, tries, file)
        if searchID < curID:
            return Search.findIMDB(searchID, minValue, half, tries, file)
        return string

    @staticmethod
    def setMaxTries(count):
        Search.maxTries = int(math.log(count)/math.log(2)+5)

    @staticmethod
    def find(idString):
        if str(idString)[0:1] == 't':
            #print('IMDB: ', idString)
            counts = LineCount.count(Search.IMDB)
            Search.setMaxTries(counts)
            return Search.findIMDB(int(idString[2:9]), 2, counts+1, 0, Search.IMDB)
        else:
            #print('TMDB: ', idString)
            counts = LineCount.count(Search.TMDB)
            Search.setMaxTries(counts)
            return Search.findTMDB(int(idString), 2, counts+1, 0, Search.TMDB)

#Test code --------------
'''
Search.find("tt0000009")
Search.find("tt0076410")
Search.find("tt1261065")
Search.find("2")
Search.find("172655")
Search.find("489002")
Search.find("1")
Search.find("tt0000005")
'''
