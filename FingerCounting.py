import cv2 as cv
import os
from HandTrackingModule import *

# pycaw mediapipe opencv
#####################################
wCam, hCam = 640, 480
#####################################

# Open the camera
cap = cv.VideoCapture(1)
if not cap.isOpened():
    cap = cv.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open Webcam")
cap.set(3, wCam)
cap.set(4, hCam)

# Detector Object
detector = HandDetector(maxHands = 1)

# Images
folderPath = "images"
myList = os.listdir(folderPath)
overLayList = []
for imPath in myList:
    image = cv.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)

# Fingers
tipIDS = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)
    
    if (len(lmList)!=0):
        fingers = []
        # THIS IS FOR THE RIGHT HAND
        # Check what hand it is 
        if(lmList[8][1] < lmList[20][1]):
            # THUMB
            if(lmList[tipIDS[0]][1] < lmList[tipIDS[0]-2][1]):
                fingers.append(1)
            else: 
                fingers.append(0)
        elif(lmList[8][1] > lmList[20][1]):
            # THUMB
            if(lmList[tipIDS[0]][1] > lmList[tipIDS[0]-2][1]):
                fingers.append(1)
            else: 
                fingers.append(0)
        # Other fingers
        for id in range(1,5):
            if(lmList[tipIDS[id]][2] < lmList[tipIDS[id]-2][2]):
                fingers.append(1)
            else: 
                fingers.append(0)
        # number of fingers
        total_fingers = fingers.count(1)  
    
        h, w, c = overLayList[total_fingers-1].shape
        img[0:h, 0:w] = overLayList[total_fingers-1] 
        
    cv.imshow("Demo", img)
    cv.waitKey(1)