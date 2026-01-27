import cv2

capture = cv2.VideoCapture('Resources/dog.mp4')

while True:
    success, img = capture.read()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow("Frame", img)

    if cv2.waitKey(20) & 0xff == ord('q'):
        break
