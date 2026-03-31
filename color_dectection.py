import cv2
import numpy as np

def nothing(x):
    pass

frame = np.zeros((488,640,3), np.uint8)

cv2.namedWindow('Trackbars')
cv2.createTrackbar('RED', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('BLUE', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('GREEN', 'Trackbars', 0, 255, nothing)

while True:
    red = cv2.getTrackbarPos('RED', 'Trackbars')
    blue = cv2.getTrackbarPos('BLUE', 'Trackbars')
    green = cv2.getTrackbarPos('GREEN', 'Trackbars')

    frame[:,:] = (blue, green, red)

    cv2.imshow('FRAME', frame)

    if cv2.waitKey(1) == ord('q'):
        break

