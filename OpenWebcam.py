import cv2

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    _, img = capture.read()
    #print(img.shape)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    imgCanny = cv2.Canny(img, 100, 100)

    cv2.imshow("fram", img)
    cv2.imshow("fram", imgCanny)
    if cv2.waitKey(20) & 0xff == ord('q'):
        break