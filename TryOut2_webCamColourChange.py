import cv2
import numpy as np

webcam = cv2.VideoCapture(0)    # 0 for default webcam...for more cam we have id 1,2 and so on
webcam.set(3, 600)   # Width using id 3
webcam.set(4, 600)   # height using id 4
webcam.set(10, 1000)

def func(val):
    pass

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 400, 400)
cv2.createTrackbar("Hmin", "Trackbars", 0, 179, func)
cv2.createTrackbar("Hmax", "Trackbars", 179, 179, func)
cv2.createTrackbar("Smin", "Trackbars", 0, 255, func)
cv2.createTrackbar("Smax", "Trackbars", 255, 255, func)
cv2.createTrackbar("Vmin", "Trackbars", 0, 255, func)
cv2.createTrackbar("Vmax", "Trackbars", 255, 255, func)

def ColorPicker(img):
    while True:
        h_min = cv2.getTrackbarPos("Hmin", "Trackbars")
        h_max = cv2.getTrackbarPos("Hmax", "Trackbars")
        s_min = cv2.getTrackbarPos("Smin", "Trackbars")
        s_max = cv2.getTrackbarPos("Smax", "Trackbars")
        v_min = cv2.getTrackbarPos("Vmin", "Trackbars")
        v_max = cv2.getTrackbarPos("Vmax", "Trackbars")
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)       # O: 0,193,162   ,   8,255,255
        lower = np.array([h_min, s_min, v_min])             # R: 0,251,70    ,   0,255,255
        upper = np.array([h_max, s_max, v_max])             # G: 61,172,42   ,   72,255,255
        mask = cv2.inRange(imgHSV, lower, upper)            # B: 110,141,33  ,   154,255,255
        imgColorDetected = cv2.bitwise_and(img, img, mask=mask)
        return (mask, imgColorDetected)
        # cv2.imshow("mask", mask)
        # cv2.imshow("color detected", imgColorDetected)
        # cv2.waitKey(1)



while True:
    success, img = webcam.read()
    mask, imgCD = ColorPicker(img)
    # cv2.imshow("CAM", img)
    cv2.imshow("mask", mask)
    cv2.imshow("Color Detection", imgCD)
    if cv2.waitKey(1) & 0xFF == ord('q'):    # press 'q' to exit
        break