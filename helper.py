import json


with open("countries.json", "r") as f:
    countries = json.load(f)

with open("state_zip.json", "r") as f:
    states_zip = json.load(f)

def get_countries():
    countries_list = []
    for country in countries:
        countries_list.append(country["name"].strip())
    return countries_list

def get_states():
    states_list = set()
    for state in states_zip:
        states_list.add(state["state"].strip())
    return list(states_list)

def get_zip():
    zip_list = set()
    for zip_code in states_zip:
        zip_list.add(zip_code["zip_code"])
    return list(zip_list)[1000:5000]



