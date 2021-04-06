#import yolo_img_impl
import os
import json
from get_spaces import get_spaces
from yolo_img_impl import run_create, run_show

# list to store the file names of all images in the folder specified
image_filenames = []

json_file = "spaces_coordinates_UFPR05.json"

folder_path = "test_data/PKLot/PKLot/UFPR05/Cloudy/"

# for root, dirs, files in os.walk(folder_path):
#     for filename in files:
#         if (not filename.endswith("output.png")) and (filename.endswith(".png") or filename.endswith(".jpg")):
#             root = root.replace("\\", "/")
#             image_filenames.append(root + "/" + filename)

# #print(image_filenames)
# for image_name in image_filenames:
#     print(image_name)
#     os.system("python yolo_img_impl.py --image " + image_name + " --yolo yolo-coco")

yolo_settings = dict()
yolo_settings["yolo"] = "yolo-coco"
yolo_settings["image"] = "dataset_middle2.jpg"
yolo_settings["confidence"] = 0.2
yolo_settings["threshold"] = 0.3



#run_create(yolo_settings, json_file)
run_show(yolo_settings, json_file)
#os.system("python yolo_img_impl.py --image dataset_middle.jpg --confidence 0.4")