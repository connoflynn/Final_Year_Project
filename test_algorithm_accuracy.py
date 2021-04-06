# script to test the accuracy of the algorithm's output by cross referencing the json file with there corresponding xml file

import os
from get_spaces import get_spaces
# have to pip install xmltodict first
import xmltodict

# a list that will store the accuracy for each photo and which spaces were incorrectly guessed
predictions = []

folder_path = "test_data/PKLot/PKLot/UFPR05/"

def json_get_occupied(json_dict):
    spaces_status = []
    for space in json_dict["spaces"]:
        space_status = dict()
        space_status["id"] = space["id"]
        space_status["occupied"] = space["occupied"]
        spaces_status.append(space_status)
    return spaces_status

def xml_get_occupied(xml_dict, xml_file):
    spaces_status = []
    for space in xml_dict["parking"]["space"]:
        try:
            space_status = dict()
            space_status["id"] = int(space["@id"])
            space_status["occupied"] = int(space["@occupied"])
            spaces_status.append(space_status)
        except:
            try:
                print("No correct information for space id: " + str(space["@id"]) + " in file: " + xml_file)
            except:
                print("Unable to read file: " + xml_file)
    return spaces_status

#function to compare two lists containing algorithm guesses and correct status of spaces
def compare(alg_lst, correct_lst):
    correct_guesses = 0
    incorrect_guesses = 0
    incorrect_space_ids = []
    total_guesses = 0
    for space in alg_lst:
        for item in correct_lst:
            if item["id"] == space["id"]:
                total_guesses +=1
                if space["occupied"] == item["occupied"]:
                    correct_guesses += 1
                else:
                    incorrect_guesses += 1
                    incorrect_space_ids.append(item["id"])
    
    accuracy = (correct_guesses / total_guesses)*100
    #accuracy = "{:.3f}".format(accuracy)

    return accuracy, incorrect_space_ids

#cross refernce the json file and the xml file
def get_accuracy(json_file, xml_file):
    global predictions

    # open xml file 
    xml = open(xml_file, "r").read()
    #use xmltodict to create a dictionary from the xml information
    xml_dict = xmltodict.parse(xml)
    #get the spaces information from xml_get_occupied function
    correct_spaces_lst = xml_get_occupied(xml_dict, xml_file)

    #use get_spaces funtion to extract the spaces dictionary from the json file
    json_dict = get_spaces(json_file)
    #get the spaces information from json_get_occupied function
    alg_spaces_lst = json_get_occupied(json_dict)

    #we only want to test the accuracy if the car park is not empty because an
    #empty car park is too easy
    actual_total_occupied = 0
    for space in correct_spaces_lst:
        if space["occupied"] == 1:
            actual_total_occupied += 1

    #check if there is at least one car in the car park
    if actual_total_occupied > 0:
        #compare the two lists
        accuracy, incorrect = compare(alg_spaces_lst, correct_spaces_lst)

        #create a dictionary containing the accuracy information and append it to the list of predictions
        prediction = dict()
        prediction["picture"] = json_file[:len(json_file) - 5]
        prediction["accuracy"] = accuracy
        prediction["incorrect"] = incorrect
        predictions.append(prediction)
        #print(prediction)


def test_algorithm(folder_path):
    #check accuracy for each json file and corresponding xml file
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                root = root.replace("\\", "/")
                json_file = root + "/" + filename
                base_name = filename[:len(filename) - 5]
                for filename in os.listdir(root):
                    if filename == (base_name + ".xml"):
                        root = root.replace("\\", "/")
                        xml_file = root + "/" + filename
                        get_accuracy(json_file, xml_file)

def output_results(predictions):
    #if predictions have been made
    if len(predictions) > 0:
        #get the worst prediction
        worst_prediction = predictions[0]
        print("\n\n")
        print("Predictions made: " + str(len(predictions)))

        count = 0
        print("Predictions less than 50 percent accuracy:")
        for prediction in predictions:
            count += prediction["accuracy"]
            #print(type(prediction["accuracy"]))
            if prediction["accuracy"] < 50:
                print(prediction["picture"])

            if prediction["accuracy"] < worst_prediction["accuracy"]:
                worst_prediction = prediction

        hundred_percent = 0
        for prediction in predictions:
            if prediction["accuracy"] == 100:
                hundred_percent += 1

        print("Number of predictions with 100 percent accuracy: " + str(hundred_percent))
        
        average_accuracy = count/len(predictions)

        print("Average Accuracy: "  + str(average_accuracy))
        print("Worst Prediction:")
        print(worst_prediction)
    else:
        print("No predictions found in file source!")

print("Starting...")
test_algorithm(folder_path)
#print(predictions)
output_results(predictions)
print("Completed")