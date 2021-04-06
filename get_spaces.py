import numpy as np
import json

# given a json file will return coordinates of spaces in a dict
def get_spaces(json_file):
    # retrieve the parking space coordinates from file
    spaces_coordinates = dict()
    try:
        f = open(json_file, "r")
        spaces_coordinates = json.load(f)
        f.close()
    except:
        print("Error: could not find file: " + str(json_file))
    return spaces_coordinates

# given a json file will return the number of free spaces and the spaces ids
def get_details(json_file):
    number_of_free_spaces = 0
    free_spaces = []
    spaces_details = dict()
    try:
        #read the json file
        f = open(json_file, "r")
        spaces_details = json.load(f)
        f.close()

        for space in spaces_details["spaces"]:
            if space["occupied"] == 0:
                number_of_free_spaces +=1
                free_spaces.append(space["id"])

    except:
        print("Error: could not find file: " + str(json_file))
    
    return number_of_free_spaces, free_spaces
