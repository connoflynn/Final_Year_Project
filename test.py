#import yolo_img_impl
import os
import json
from get_spaces import get_spaces

# list to store the file names of all images in the folder specified
image_filenames = []
    

folder_path = "test_data/PKLot/PKLot/UFPR05/Sunny/2013-02-26/"
for filename in os.listdir(folder_path):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_filenames.append(folder_path + filename)
        print(filename)

print(image_filenames)
for image_name in image_filenames:
    os.system("python yolo_img_impl.py --image " + image_name + " --yolo yolo-coco")

#os.system("python yolo_img_impl.py --image dataset_middle2.jpg --yolo yolo-coco")