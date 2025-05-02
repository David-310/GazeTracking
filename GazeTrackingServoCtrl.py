"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.

Use GazeTracking to control a servo motor based on the user's gaze direction.
"""

import cv2
from gaze_tracking import GazeTracking
import time
import serial

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

ser = serial.Serial('COM3', 115200)  # Change 'COM3' to the appropriate serial port
print("serial connected")
time.sleep(2)  # Wait for the serial connection to establish

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    
    left_coords = gaze.pupil_left_coords()
    right_coords = gaze.pupil_right_coords()
    
    if left_coords is not None and right_coords is not None:
        
        ser.write(f"1:{int(float(left_coords[0])/512*180)}\n".encode())
        time.sleep(0.01)
        print(ser.readline().decode().strip())
        time.sleep(0.01)
        
        ser.write(f"2:{140 - int(float(left_coords[1])/512*140)}\n".encode())
        time.sleep(0.01)
        print(ser.readline().decode().strip())
        time.sleep(0.01)
        
        ser.write(f"3:{int(float(right_coords[0] - left_coords[0])/512*180)}\n".encode())
        time.sleep(0.01)
        print(ser.readline().decode().strip())
        time.sleep(0.01)
        
    if gaze.is_left():
        ser.write("4:45\n".encode())
        time.sleep(0.01)
        print(ser.readline().decode().strip())
        time.sleep(0.01)
    elif gaze.is_right():
        ser.write("4:5\n".encode())
        time.sleep(0.01)
        print(ser.readline().decode().strip())
        time.sleep(0.01)


    cv2.putText(frame, "Left pupil:  " + str(left_coords), (70, 130), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_coords), (70, 165), cv2.FONT_HERSHEY_DUPLEX, 0.5, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)
    
    time.sleep(0.05)
    
    if cv2.waitKey(1) == 27:
        # If the user presses the ESC key, we break the loop
        break
    
   
webcam.release()
cv2.destroyAllWindows()
ser.close()
