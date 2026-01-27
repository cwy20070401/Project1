import cv2

print(cv2.__version__)

img = cv2.imread('Resources/lena.png')

print(img.shape)

img2 = cv2.resize(img, (int(img.shape[1]/1.5), int(img.shape[0]/1.5)))

imgGray = cv2.resize(img, (1000,400))

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imgB = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)

cv2.imshow("Lena", img)
cv2.imshow("Lena2", img2)
cv2.imshow("Lena3", imgGray)
cv2.imshow("Lena4", imgB)


cv2.waitKey(0)

