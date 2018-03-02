import json
from dataCall import dataCall as DC

movie = "0"

while movie != "":
    print(" ")
    movie = input("Enter a movie name! \n")
    print(" ")

    if movie != "":
        print(DC.findMovie(movie))
