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
