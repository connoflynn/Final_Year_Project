import cv2 
import numpy as np
import json
import copy
  
imgFile = "dataset_empty.jpg"

img = cv2.imread(imgFile) 

box_coordinates = []

spaces_dict = {"spaces" : []}
space_id = 1

  
def draw_box(event, x, y, flags, param): 
      
    global img, box_coordinates, spaces_dict, space_id

    if event == cv2.EVENT_LBUTTONDOWN:
        box_coordinates.append([x,y])
        # every 4 clicks on the image, the space co-ordinates are saved to a file and shown on the image
        if len(box_coordinates) == 4:

            #create json file to write to
            f = open("spaces_coordinates_dataset.json", "w")

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
            cv2.polylines(img,[pts],isClosed,color,2)
            box_coordinates.clear()

cv2.namedWindow("Set Parking Spaces", cv2.WINDOW_NORMAL) 
cv2.setMouseCallback("Set Parking Spaces", draw_box) 

while True:
    cv2.imshow("Set Parking Spaces", img) 
      
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cv2.destroyAllWindows() 