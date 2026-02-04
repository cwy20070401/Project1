import cv2
import numpy as np

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
capture.set(3, 240)
capture.set(4, 160)

while True:
    _, img1 = capture.read()
    img2 = cv2.flip(img1, 1)
    img3 = cv2.flip(img2, 0)
    img4 = cv2.flip(img3, -1)

    Hori1 = np.concatenate((img1, img2), axis=1)
    Hori2 = np.concatenate((img3, img4), axis=1)
    Verti = np.concatenate((Hori1, Hori2), axis=0)

    cv2.imshow("fram", Verti)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        