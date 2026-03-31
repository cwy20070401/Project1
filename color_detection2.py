import cv2
import numpy as np

def nothing (x):
    pass

cv2.namedWindow('Trackbars')
cv2.createTrackbar('HUELOW', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('HUEHIGH', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('SATLOW', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('SATHIGH', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('VALLOW', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('VALHIGH', 'Trackbars', 0, 255, nothing)

while True:
    img = cv2.imread('Resources/smarties.png')
    cv2.imshow('Frame', img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    huelow = cv2.getTrackbarPos('HUELOW', 'Trackbars')
    huehigh = cv2.getTrackbarPos('HUEHIGH', 'Trackbars')
    satlow = cv2.getTrackbarPos('SATLOW', 'Trackbars')
    sathigh = cv2.getTrackbarPos('SATHIGH', 'Trackbars')
    vallow = cv2.getTrackbarPos('VALLOW', 'Trackbars')
    valhigh = cv2.getTrackbarPos('VALHIGH', 'Trackbars')

    FGmask = cv2.inRange(hsv, (huelow, satlow, vallow), (huehigh, sathigh, valhigh))
    cv2.imshow('FGmask', FGmask)

    FG = cv2.bitwise_and(img, img, mask=FGmask)
    cv2.imshow('FG', FG)

    BGmask = cv2.bitwise_not(FGmask)
    cv2.imshow('BG', BGmask)

    BG = cv2.cvtColor(BGmask, cv2.COLOR_GRAY2BGR)

    finalIMG = cv2.add(FG, BG)
    cv2.imshow('final', finalIMG)

    if cv2.waitKey(1) == ord('q'):
        break
