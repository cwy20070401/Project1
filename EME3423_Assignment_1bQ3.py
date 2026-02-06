import cv2
import numpy as np

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3,240)
capture.set(4,320)

while True:
    _, img1 = capture.read()
    img2 = cv2.flip(img1, 1)
    img3 = cv2.flip(img1, 0)
    img4 = cv2.flip(img1, -1)

    Hori1 = np.concatenate((img1, img2), axis=1)
    Hori2 = np.concatenate((img3, img4), axis=1)
    verti = np.concatenate((Hori1, Hori2), axis=0)


    cv2.imshow("fram", verti)
    if cv2.waitKey(20) & 0xff == ord('q'):
        break
#img = np.zeros((500,500,3), np.uint8)
#img = cv2.line(img, (0,0), (500,500), (0,100,255), 5)
#img = cv2.circle(img, (400,100), 50, (0,0,255), 5)
#img = cv2.rectangle(img, (250,300), (400,325), (0,0,255), 4)

#pts = np.array([[10,5], [100,30], [60,100], [80,9255]], np.int32)
#img = cv2.polylines(img, [pts], True, (0,255,255))

#print(img.shape)
#print(img)

#cv2.imshow("img", img)

#cv2.waitKey(0)