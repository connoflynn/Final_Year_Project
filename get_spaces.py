import numpy as np
import json


def get_spaces():
    # retrieve the parking space coordinates from file
    spaces_coordinates = dict()

    f = open("spaces_coordinates_dataset.json", "r")
    spaces_coordinates = json.load(f)
    # for space in spaces_coordinates["spaces"]:
    #     print(str(space["id"]))
    #     print(type(space["co_ordinates"]))
    f.close()
    return spaces_coordinates

get_spaces()