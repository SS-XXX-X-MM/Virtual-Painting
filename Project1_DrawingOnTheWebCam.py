import cv2
import numpy as np
from StackImagesFunction import stackImages

colorRange = [[2,255,212,10,255,255],
              [61,172,42,72,255,255],
              [110,141,33,154,255,255],
              [0,255,100,2,255,205],
              [14,139,142,22,255,255]]
              # [0,0,84,179,56,255]]

colors = [(5,63,255),
          (0,255,0),
          (255,0,0),
          (0,0,255),
          (0,255,255)]

colorsList = ("Orange", "Green", "Blue","Red","Yellow","White")

mypoints = [] # (x,y,coloridx)

def ColorFilter(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    i = 0
    for color in colorRange:
        lower = np.array(color[0:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imgHSV, lower, upper)
        # imgColorDetected = cv2.bitwise_and(img, img, mask=mask)    # To show individual colors
        # cv2.imshow(colorsList[i], imgColorDetected)
        x,y = findContours(mask, img, i)
        if x!=0 and y!=0:
            mypoints.append((x,y,i))
        i+=1



def findContours(imgMask, img, i):
    # When three is no matching color this will show otherwise screen down there will override this screen
    cv2.imshow("Detection", img)
    contours, hierarchy = cv2.findContours(imgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x = y = w = h = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 10:
            # cv2.drawContours(img, cnt, -1, (255, 255, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(original, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.circle(img, (x+w//2, y+h//2), 4, colors[i], 5, cv2.FILLED)
            # cv2.imshow("Detection", img)
    return x+w//2,y+h//2

def drawOnCanvas():
    for point in mypoints:
        cv2.circle(img, (point[0], point[1]), 5, colors[point[2]], 8, cv2.FILLED)

webcam = cv2.VideoCapture(0)

def func(val):
    pass

cv2.namedWindow("Erase")
cv2.resizeWindow("Erase", 400, 400)
cv2.createTrackbar("Delete", "Erase", 0, 1, func)
cv2.createTrackbar("Exit", "Erase", 0, 1, func)

while True:
    success, img = webcam.read()
    img = cv2.resize(img, (600,600))
    ColorFilter(img)
    if len(mypoints)!=0:
        drawOnCanvas()
    cv2.imshow("Detection", img)
    clear = cv2.getTrackbarPos("Delete", "Erase")
    exit = cv2.getTrackbarPos("Exit", "Erase")
    if clear == 1:
        mypoints = []
        cv2.setTrackbarPos("Delete", "Erase", 0)
    if exit == 1 or cv2.waitKey(1) & 0xFF == ord('q'):
        break