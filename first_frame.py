import cv2
import numpy as np


video_name = 'cctv3.mp4'
cap = cv2.VideoCapture(video_name)
success,frame = cap.read()

if success == True:
	cv2.imwrite("cctv3_still.png", frame)
else:
	print("Error Reading Frame")

cap.release()