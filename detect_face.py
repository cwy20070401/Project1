import cv2
import numpy as np

faceCascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade/haarcascade_eye.xml')
smileCascade = cv2.CascadeClassifier('haarcascade/haarcascade_smile.xml')


img = cv2.imread('Resources/BTS.jpg')

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3, 640)
capture.set(4, 480)

while True:
    _, img = capture.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.05, 5)

    #print(faces)

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        roiImg = img[y:y+h, x:x+w]
        roiGray = imgGray[y:y+h, x:x+w]

        eyes = eyeCascade.detectMultiScale(roiImg, 1.1, 5)

        smile = smileCascade.detectMultiScale(roiImg, 1.1, 5)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roiImg, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        smile = smileCascade.detectMultiScale(roiImg, 1.3, 20, minSize=(10, 10))

        for (sx, sy, sw, sh) in smile:
            cv2.rectangle(roiImg, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)
            cv2.putText(img, 'Smiling', (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0.255,0), 2)


    cv2.imshow("img", img)

    if cv2.waitKey(1) &0xff==ord('q'):
        break