import cv2
import mediapipe as mp
import time
import random


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(mode, maxHands,1,
                                        0.5, 0.4)
        self.mpDraw = mp.solutions.drawing_utils

    def findHand(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # extract the hands
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findposData(self, img, handNo =0, draw = True):
        lmlist =[]
        if self.results.multi_hand_landmarks:
            hand_num = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand_num.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx,cy)
                lmlist.append([id, cx, cy])
                # if id == 4:
                if draw:
                   cv2.circle(img, (cx,cy), 5, (255,67,200), cv2.FILLED)
        return lmlist

    def game(self, point ,x, y, rad , lmlist):

        if (x + rad < lmlist[4][1]< x+rad) and (y + rad < lmlist[4][1]< y+ rad):
            point =+1
            return point
        else:
            return point



def main():
    pTime = 0
    cTime = 0
    detector = handDetector()
    # opening camera feed
    captureVideo = cv2.VideoCapture(0)
    point = 0
    oldlist = []
    while True:
        success, img = captureVideo.read()
        img = detector.findHand(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        list = detector.findposData(img)


        if len(list) != 0 and len(oldlist) != 0:
            print(list[4])
            print("oldlist", oldlist[4])
            x1 = 0
            y1 = 0
            y2 = 0
            x2 = 0
            for i in range(len(list)):
                x1 += list[i][1]
                y1 += list[i][2]
                x2 += oldlist[i][1]
                y2 += oldlist[i][2]

            x1 = x1/21
            x2 = x2/21
            y1 = y1/21
            y2 = y2/21

            a = x1-x2
            b = y1-y2


            print(a,b)
            if  a > b :
                if abs(a)>10:
                    if a < 0:

                        cv2.putText(img, str("Moving Right"), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        print("Moving Right")
                    else:

                        cv2.putText(img, str("Moving left"), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        print("Moving Left")
            else:
                if abs(b) > 10:

                    if b < 0:
                        cv2.putText(img, str("Moving Up"), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        print("Moving Up")
                    else:
                        cv2.putText(img, str("Moving Down"), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        print("Moving Down")

        oldlist = list

        #cv2.putText(img, str(int(point)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        #cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()