import SaveLoadJson

def getGenres():
    print("Getting Genres")
    first = True
    numb = 0
    total = 0.0
    items = 0
    genresTemp = {}
    with open("title.merged.tsv", "r", encoding='utf8') as f:
        for line in f:
            numb += 1
            if numb % 46000 == 0:
                print(numb)
            if first == False:
                split = line.split("\t")
                if split[1] == "movie":
                    rating = float(split[9])
                    split = split[8].split(",")
                    for item in split:
                        if item not in genresTemp:
                            print("Adding ",item," to the genres dict")
                            Dict = { "Value":0,
                                     "Times":0
                                     }
                            genresTemp[item] = Dict
                        if rating != 0:
                            genresTemp[item]["Value"] += rating
                            genresTemp[item]["Times"] += 1
                            total += rating
                            items += 1
            else:
                first = False

    genres = {}
    genres["Genres"] = {}
    genres["Average"] = total/items
    for key, value in genresTemp.items():
        genres["Genres"][key] = value["Value"]/value["Times"]

    print("Finished searching")
    SaveLoadJson.SaveLoadJson.save("AverageRatings.txt", genres)
    print("Saving done")

getGenres()
'''
total = 0.0
items = 0
first = True
with open("TMDBRatings.tsv","r") as f:
    for line in f:
        if first == True:
            first = False
        else:
            rating = (line.split("\t"))[2]
            if float(rating) > 0:
                total += float(rating)
                items += 1

print(format(total/items,'.2f'))
'''
