import cv2
import mediapipe as mp
import time
import subprocess

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    finger_count = 0  # Variable to store the finger count

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8 and lm.y < handLms.landmark[5].y:
                    finger_count += 1  # Increment finger count if the tip of the index finger is above the base of the index finger

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.putText(img, "Finger Count: " + str(finger_count), (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    # Control brightness based on finger count
    brightness = finger_count * 25  # Adjust the brightness level based on the finger count (assuming each finger increases brightness by 25%)
    brightness_command = f'do shell script "brightness {brightness}"'  # AppleScript command to set brightness
    subprocess.run(['osascript', '-e', brightness_command])  # Execute the AppleScript command

    cv2.imshow("Image", img)
    cv2.waitKey(1)
