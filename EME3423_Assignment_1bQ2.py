import cv2
import numpy as np

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, img = capture.read()

    img_blur = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_canny = cv2.Canny(img_gray, 100, 100)
    #print(img.shape)

    cv2.imshow("Ori", img)
    cv2.imshow("Gray", img_gray)
    cv2.imshow("Canny", img_canny)
    cv2.imshow("Blur", img_blur)

    if cv2.waitKey(20) & 0xff == ord('q'):
        break