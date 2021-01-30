import cv2
import numpy as np

#INITIALISE HERE
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

#DEFINE BASIC VARIABLES HERE..
video_index = 1
SUSPICIOUS_THRESHOLD = 0.5
recording = 0 
out = 0

def record_if_suspicious(frame):
    global recording
    global video_index
    global SUSPICIOUS_THRESHOLD
    global out
    #get suspicious value here
    suspicious_value = 0.7
    #...
    if suspicious_value >= SUSPICIOUS_THRESHOLD:
        if recording == 0:
            out = cv2.VideoWriter('video'+str(video_index)+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
            out.write(frame)
            recording = 1
        elif recording == 1:
            out.write(frame)
    else:
        if recording == 0:
            return
        elif recording == 1:
            out.write(frame)
            out.release()
            video_index+=1
            recording = 0



while(True):

    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    record_if_suspicious(frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()