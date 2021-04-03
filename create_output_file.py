# A script to create a json output file containing the parking
# spaces ids and whether they are occupied or not

import json


def create_json(base_image_name, spaces_dict):
    filename = base_image_name + ".json"
    f = open(filename, "w")
    
    #convert the dictionary to json format
    space_json_object = json.dumps(spaces_dict, indent = 4)
    f.write(space_json_object)
    f.close()