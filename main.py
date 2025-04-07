import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

# Setup camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Setup hand detector
detector = HandDetector(detectionCon=0.8)

# Initial color
colorR = (255, 0, 255)

class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        x, y, _ = cursor
        cx, cy = self.posCenter
        w, h = self.size
        # Check if cursor is inside the rectangle
        if cx - w // 2 < x < cx + w // 2 and cy - h // 2 < y < cy + h // 2:
            self.posCenter = x, y

# Create instance
rectList = []
for x in range(5):
    rectList.append(DragRect([x*250+150, 150]))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)  # Detect hands
    lmList = []

    if hands:
        lmList = hands[0]["lmList"]

        if lmList:
            point1 = lmList[8]    # Index finger tip
            point2 = lmList[12]   # Middle finger tip

            # Find distance between fingers
            l, _, _ = detector.findDistance(point1[:2], point2[:2], img)
            print(l)

            # Check if fingers are pinched close
            if l < 60:
                for rect in rectList:
                    rect.update(point1)

    # Get current rectangle center and size
    ## Draw Solid
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #
    # # Draw draggable rectangle
    #     cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
    #     cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w ,h), 20, rt=0)
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size

    # # Draw draggable rectangle
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w ,h), 20, rt=0)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)