import json

filename = "data/london.json"

with open(filename, "r") as jsonfile:
    data = json.load(jsonfile)

an_integer = 1

set(an_integer)