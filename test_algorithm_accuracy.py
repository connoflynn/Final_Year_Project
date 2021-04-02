# script to test the accuracy of the algorithm's output by cross referencing the json file with there corresponding xml file

import os
from get_spaces import get_spaces
# have to pip install xmltodict first
import xmltodict


folder_path = "test_data/PKLot/PKLot/UFPR05/Sunny/2013-02-26/"

def json_get_occupied(spaces_dict):
    for space in spaces_dict["spaces"]:
        print("id: " + str(space["id"]) + "  occupied: " + str(space["occupied"]))

#cross refernce the json file and the xml file
def get_accuracy(json_file, xml_file):
    global folder_path


    xml = open(folder_path + xml_file, "r").read()
    xml = xmltodict.parse(xml)
    print(xml)

    #print("json: " + json_file + "  xml: " + xml_file)
    spaces_dict = get_spaces(folder_path + json_file)
    #json_get_occupied(spaces_dict)


#check accuracy for each 
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        json_file = filename
        base_name = filename[:len(filename) - 5]
        for filename in os.listdir(folder_path):
            if filename == (base_name + ".xml"):
                get_accuracy(json_file, filename)