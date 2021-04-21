import cv2 
import numpy as np
import json
import copy
from shapely.geometry import Polygon
from math import floor
from get_spaces import get_spaces

imgFile = "UFPR04_empty.jpg"
outputFile = imgFile[:-4] + "_spaces_coordinates.json"

space_id = 1
#if the json already exists for this image, open it and read values
spaces_dict = get_spaces(outputFile)

#read image
img = cv2.imread(imgFile)

#get width and height of input image
img_height, img_width = img.shape[:2]

# find the centre of a polygon, given the co_ordinates
def get_centre(co_ordinates):
	co_ordinates = Polygon(co_ordinates)
	centre = co_ordinates.centroid
	centre = (floor(centre.x), floor(centre.y))
	return centre

if spaces_dict != {}:
    # find the biggest id already set
    for space in spaces_dict["spaces"]:
        if space["id"] >= space_id:
            space_id = space["id"] + 1
    #draw the already created spaces on the image
    for space in spaces_dict["spaces"]:
        #draw space on image
        pts = np.array(space["co_ordinates"], np.int32)
        pts = pts.reshape((-1, 1, 2))
        isClosed = True
        color = (0,255,0)
        centre = get_centre(space["co_ordinates"])
        # write the ID in the space
        cv2.putText(img,str(space["id"]), centre, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.polylines(img,[pts],isClosed,color,2)
else:
    spaces_dict = {"spaces" : []}

box_coordinates = []


def draw_box(event, x, y, flags, param): 
      
    global img, box_coordinates, spaces_dict, space_id, outputFile

    if event == cv2.EVENT_LBUTTONDOWN:
        # check if click is on undo button
        if x <= floor(img_width/8.5) and y <= floor(img_height/9.5):
            undo_last()
        else:
            box_coordinates.append([x,y])
            # every 4 clicks on the image, the space co-ordinates are saved to a file and shown on the image
            if len(box_coordinates) == 4:

                #create json file to write to
                f = open(outputFile, "w")

                space = dict()
                space["id"] = space_id
                space_id = space_id + 1
                space["co_ordinates"] = box_coordinates

                spaces_dict["spaces"].append(copy.deepcopy(space))

                #convert the dictionary to json format
                space_json_object = json.dumps(spaces_dict, indent = 4)
                f.write(space_json_object)
                f.close()

                #draw space on image
                pts = np.array(box_coordinates, np.int32)
                pts = pts.reshape((-1, 1, 2))
                isClosed = True
                color = (0,255,0)
                centre = get_centre(box_coordinates)
                # write the ID in the space
                cv2.putText(img,str(space["id"]), centre, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                cv2.polylines(img,[pts],isClosed,color,2)
                cv2.imshow("Set Parking Spaces", img)
                box_coordinates.clear()

cv2.namedWindow("Set Parking Spaces", cv2.WINDOW_NORMAL) 

def undo_last():
    global space_id
    try:
        space_id = spaces_dict["spaces"][-1]["id"]
        spaces_dict["spaces"].pop()
        #update json file
        f = open(outputFile, "w")
        #convert the dictionary to json format
        space_json_object = json.dumps(spaces_dict, indent = 4)
        f.write(space_json_object)
        f.close()
        img = cv2.imread(imgFile)
        cv2.imshow("Set Parking Spaces", img)
    except:
        print("No Spaces to Undo!")


def create_image(img):
    img = cv2.imread(imgFile)
    cv2.rectangle(img,(0,0),(floor(img_width/8.5),floor(img_height/9.5)),(231, 231, 231),-1)

    #write the text in the centre of the rectangle
    centre_rectangle = (floor((0+floor(img_width/8.5))/2), floor((0+floor(img_height/9.5))/2))
    TEXT_FACE = cv2.FONT_HERSHEY_DUPLEX
    TEXT_SCALE = 1
    TEXT_THICKNESS = 2
    TEXT = "UNDO"
    text_size, _ = cv2.getTextSize(TEXT, TEXT_FACE, TEXT_SCALE, TEXT_THICKNESS)

    text_origin = (centre_rectangle[0] - text_size[0] // 2, centre_rectangle[1] + text_size[1] // 2)

    cv2.putText(img, TEXT, text_origin, TEXT_FACE, TEXT_SCALE, (0,0,0), TEXT_THICKNESS, cv2.LINE_AA)

    #draw the already created spaces on the image
    for space in spaces_dict["spaces"]:
        #draw space on image
        pts = np.array(space["co_ordinates"], np.int32)
        pts = pts.reshape((-1, 1, 2))
        isClosed = True
        color = (0,255,0)
        centre = get_centre(space["co_ordinates"])
        # write the ID in the space
        cv2.putText(img,str(space["id"]), centre, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.polylines(img,[pts],isClosed,color,2)
    
    cv2.imshow("Set Parking Spaces", img)


#cv2.createTrackbar("undo", "Set Parking Spaces", 0, 1, undo_last)
while True:
    cv2.setMouseCallback("Set Parking Spaces", draw_box)
    create_image(img)
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cv2.destroyAllWindows() 