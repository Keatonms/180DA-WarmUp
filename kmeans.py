import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    cv2.rectangle(frame, (200, 200), (300, 300), (255, 0, 0), 3)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5)
    if k == 27: # ESC
        break

img = frame[200:300, 200:300] # grabbing the thing in the box.
cv2.imshow('final frame', img)

# do whatever you want. 

while True:
    k = cv2.waitKey(5)
    if k == 27: # ESC
        break

cap.release()
cv2.destroyAllWindows()
