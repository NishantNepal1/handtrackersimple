import cv2
import mediapipe as mp
import time


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

    def game(self, img, points):

        handin =[]
        if self.results.multi_hand_landmarks:
            hand_num = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand_num.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx,cy)
                lmlist.append([id, cx, cy])
                # if id == 4:
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 67, 200), cv2.FILLED)




def main():
    pTime = 0
    cTime = 0
    detector = handDetector()
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

        #print("No data")

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()