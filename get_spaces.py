import numpy as np
import json


def get_spaces(json_file):
    # retrieve the parking space coordinates from file
    spaces_coordinates = dict()

    f = open(json_file, "r")
    spaces_coordinates = json.load(f)
    f.close()
    return spaces_coordinates