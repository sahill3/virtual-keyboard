import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1288)  # prop-id for width is 3 , so width = 1288
cap.set(4, 720)  # prop-id for height is 4, so height = 720

# detection confidence probability
detector = HandDetector(detectionCon=0.8, maxHands=1)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", " "],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "-"]]

# - is for backspace

finalText = ""

keyboard = Controller()

# without transparency
def drawALL(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x+w, y+h), (100, 100, 100), cv2.FILLED)
        cv2.putText(img, button.text, (x+20, y+65),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100*j+50, 100*i+50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)
    img = drawALL(img, buttonList)

    if hands:
        hand1 = hands[0]

        lmList = hand1["lmList"]

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x+w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x+w, y+h),
                                  (50, 50, 50), cv2.FILLED)
                    cv2.putText(img, button.text, (x+20, y+65),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

                    l, _, img = detector.findDistance(
                        lmList[8][:2], lmList[12][:2], img)
                    # print(l)

                    if l < 50:
                        cv2.rectangle(img, button.pos, (x+w, y+h),
                                      (50, 50, 50), cv2.FILLED)
                        cv2.putText(img, button.text, (x+20, y+65),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                        if(button.text == "-" and len(finalText) != 0):
                            finalText = finalText[:-1]
                            keyboard.press('\b')
                            sleep(0.5)
                        else:
                            keyboard.press(button.text)
                            finalText += button.text
                            sleep(0.5)

    cv2.rectangle(img, (50, 350), (700, 450),
                  (100, 100, 100), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Image (Press ESC to close)", img)
    if cv2.waitKey(1) & 0xFF == 27:  # '27' is the ASCII code for ESC
        break

# Release video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()