import random

import cv2
import mediapipe as mp
import time
import handTrackingModule as  htm




pTime = 0
cTime = 0
detector = htm.handDetector()
# opening camera feed
captureVideo = cv2.VideoCapture(0)

while True:
    success, img = captureVideo.read()
    img = detector.findHand(img)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    list = detector.findposData(img)
    if len(list) != 0:
        print(list[4])
    cv2.putText(img, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


    # print("No data")

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)