"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import matplotlib.pyplot as plt

import seaborn as sns
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
eye_1x_positions = list()
eye_1y_positions = list()
eye_2x_positions = list()
eye_2y_positions = list()

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)


    left_pupilx = gaze.cordslx()
    left_pupily  = gaze.cordsly()
    right_pupilx = gaze.cordsrx()
    right_pupily = gaze.cordsry()
    eye_1x_positions.append(left_pupilx)
    eye_1y_positions.append(left_pupily)
    cv2.putText(frame, "Left pupil:  " + str(left_pupilx)+","+str(left_pupily), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupilx)+","+str(right_pupily), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)


    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break



data = list(zip(eye_1x_positions, eye_1y_positions))

print(data)

plt.scatter(eye_1x_positions, eye_1y_positions)
plt.show()
sns.set()
webcam.release()
cv2.destroyAllWindows()
