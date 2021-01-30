import cv2
import os
from pathlib import Path

cap = cv2.VideoCapture(0)

def saveImage(image, type, imgId):
    Path("dataset/{}".format(type)).mkdir(parents=True, exist_ok=True)
    cv2.imwrite("dataset/{}/{}.jpg".format(type, imgId), image)
    print("[INFO] Image {} has been saved in folder : {}".format(imgId, type))

print("Enter type of image : ")
t = input()
print("Enter starting id of image : ")
cnt = int(input())

skip = 0

while True:
    ret, img = cap.read()
    if skip < 100 or skip % 2 == 0:
        skip = skip + 1
        continue
    for i in range(50):
        _, __ = cap.read()

    saveImage(img, t, cnt)
    cnt = cnt + 1
    skip = skip + 1

    cv2.imshow("Saving Image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

