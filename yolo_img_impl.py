# USAGE
# python yolo_img_impl.py --image cctv3_still.png --yolo yolo-coco

import numpy as np
import argparse
import time
import cv2
import os
from shapely.geometry import Polygon
from get_spaces import get_spaces
from get_occupied import get_occupied
from create_output_file import create_json

json_file = "spaces_coordinates_UFPR05.json"

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-y", "--yolo", default="yolo-coco",
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

def yolo_implementation(args):
	# get the labels for each object in the coco.names file
	labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
	labels = open(labelsPath).read().strip().split("\n")

	# create a list of random colours to use for each label type
	# we want the colours to be the same each time so we call seed
	np.random.seed(42)
	colours = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

	# set paths to weights and config files
	weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
	configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

	# load trained yolo information using built in dnn.readNetFromDarknet function
	print("Loading YOLO from disk...")
	net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	#get just the layer names we need from the yolo neural network
	# the ones we need are ['yolo_82', 'yolo_94', 'yolo_106']
	ln = net.getLayerNames()
	ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	# load the image and determine the height and width
	image = cv2.imread(args["image"])
	(H, W) = image.shape[:2]

	# create a blob from the image
	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
	# r = blob[0, 0, :, :]
	# cv2.imshow("blob", r)
	# cv2.waitKey(0)

	#set the new input value for the network as the blob 
	net.setInput(blob)
	# measure the time it takes yolo to run on the image
	start = time.time()
	# perform a forward pass to get bounding boxes and probabilities
	outputs = net.forward(ln)
	end = time.time()

	# print the time yolo took to run
	print("YOLO took {:.3f} seconds".format(end - start))
	print("Drawing results on image...")

	# initialize our lists of detected bounding boxes, confidences, and classIDs
	boxes = []
	confidences = []
	classIDs = []

	# Initialise a list of cars that will contain bounding boxes of each vehicle
	Cars = []

	# loop over each of the layer outputs
	for output in outputs:
		# loop over all detections
		for detection in output:
			# get the class ID and confidence of the object
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			# if confidence > 0:
			# 	print("Class ID: " + str(classID) + " Condidence: " + str(confidence))

			# only if the confidence level is higher than the specified level
			if confidence > args["confidence"]:
				# scale the boxes reletive to the original image
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				# figure out the top corner and the left corner of the box for when 
				# we want to call cv2.rectangle
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update our list of bounding box coordinates, confidences,
				# and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)

	# apply non-maxima suppression to suppress weak, overlapping bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])

	# if there is at least 1 object detected
	if len(idxs) > 0:
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# only include bounding boxes for vehicles
			if labels[classIDs[i]] == "car" or labels[classIDs[i]] == "bus" or labels[classIDs[i]] == "truck":
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])

				# add car coordinates to list of cars
				Cars.append([[x,y],[x + w, y + 0],[x + w, y + h],[x + 0, y +h]])

				# draw a bounding box rectangle and label on the image
				color = [int(c) for c in colours[classIDs[i]]]
				cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(labels[classIDs[i]], confidences[i])
				cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
	return image, Cars

# function to draw spaces on the image, green if empty and red if occupied
def draw_spaces(frame, spaces_coordinates):
	for space in spaces_coordinates:
		co_ordinates = space[0]
		occupied = space[1]
		id = space[2]
		pts = np.array(co_ordinates, np.int32)
		pts = pts.reshape((-1, 1, 2))
		isClosed = True
		if occupied == 1:
			color = (0,0,255)
		else:
			color = (0,255,0)
		cv2.polylines(frame,[pts],isClosed,color,2)

#function if we want to 
def create_new_file(image, Cars, args, json_file):
	#global image, Cars, args, json_file
	try:
		# get spaces coordinates from file and add them to a dictionary
		spaces_dict = get_spaces(json_file)
		#add occupied key to dict using get_occupied function
		spaces_dict = get_occupied(spaces_dict, Cars)

		spaces_coordinates = []
		for space in spaces_dict["spaces"]:
			#print(space)
			spaces_coordinates.append([space["co_ordinates"], space["occupied"], space["id"]])

		draw_spaces(image, spaces_coordinates)


		# show the output image
		#cv2.namedWindow("View spaces", cv2.WINDOW_NORMAL) 
		#cv2.imshow("View spaces", image)

		# save image output
		#generate name for output image from input image
		image_name = args["image"]
		output_image_name = image_name[:len(image_name) - 4]

		#create an image of the output
		cv2.imwrite(output_image_name + '_output.png', image)

		#create a json file of the output information
		create_json(output_image_name, spaces_dict)
	except:
		print("Error")

# function if we just want to show the output result 
def show_image(image, json_file):

	# get spaces coordinates from file and add them to a dictionary
	spaces_dict = get_spaces(json_file)
	#add occupied key to dict using get_occupied function
	spaces_dict = get_occupied(spaces_dict, Cars)

	spaces_coordinates = []
	for space in spaces_dict["spaces"]:
		#print(space)
		spaces_coordinates.append([space["co_ordinates"], space["occupied"], space["id"]])

	draw_spaces(image, spaces_coordinates)

	# show the output image
	cv2.namedWindow("View spaces", cv2.WINDOW_NORMAL) 
	cv2.imshow("View spaces", image)

	cv2.waitKey(0)


image, Cars = yolo_implementation(args)
create_new_file(image, Cars, args, json_file)

#show_image(image, json_file)