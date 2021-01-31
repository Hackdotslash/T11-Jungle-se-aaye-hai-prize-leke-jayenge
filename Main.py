#Note : Due to compatibility issues with pyaudio, This module will not work on python 3.5 or higher
#IMPORT HERE..
import cv2
import numpy as np
import pyaudio
import wave
import tkinter as tk
from PIL import Image, ImageTk

#INITIALISE HERE
cap = cv2.VideoCapture(0)
aud = pyaudio.PyAudio()
vid_frame_width = int(cap.get(3))
vid_frame_height = int(cap.get(4))
root = tk.Tk()
app = tk.Frame(root, bg="white")
app.grid()
lmain = tk.Label(app)
lmain.grid()
#DEFINE CONSTANTS HERE..
SUSPICIOUS_THRESHOLD = 0.5
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

#DEFINE BASIC VARIABLES HERE..
av_index = 1
stream = 0
recording = 0 
video_output = 0
audio_output = []

def record_if_suspicious(vid_frame,aud_frame):
    global recording
    global av_index
    global SUSPICIOUS_THRESHOLD
    global video_output
    global audio_output
    #get suspicious value here
    suspicious_value = 0.7
    #...
    if suspicious_value >= SUSPICIOUS_THRESHOLD:
        if recording == 0:
            video_output = cv2.VideoWriter('Video_'+str(av_index)+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (vid_frame_width,vid_frame_height))
            video_output.write(vid_frame)
            audio_output = []
            audio_output.append(aud_frame)
            recording = 1
        elif recording == 1:
            video_output.write(vid_frame)
            audio_output.append(aud_frame)
    else:
        if recording == 0:
            return
        elif recording == 1:
            video_output.write(vid_frame)
            audio_output.append(aud_frame)
            
            final_audio = ("Audio_"+str(av_index),wb)
            final_audio.setnchannels(CHANNELS)
            final_audio.setsampwidth(p.get_sample_size(FORMAT))
            final_audio.setframerate(RATE)
            final_audio.writeframes(b''.join(frames))
            final_audio.close()

            video_output.release()
            av_index+=1
            recording = 0


def base_function():
    global root
    global stream
    ret, vid_frame = cap.read()
    stream = aud.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True, frames_per_buffer=CHUNK)
    aud_frame = stream.read(CHUNK)
    
    record_if_suspicious(vid_frame,aud_frame)

    imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(vid_frame, cv2.COLOR_BGR2RGBA)))
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, base_function)   
base_function()
root.mainloop()




final_audio = wave.open("Audio_"+str(av_index)+'.wav','wb')
final_audio.setnchannels(CHANNELS)
final_audio.setsampwidth(aud.get_sample_size(FORMAT))
final_audio.setframerate(RATE)
final_audio.writeframes(b''.join(audio_output))
final_audio.close()
video_output.release()

stream.stop_stream()
stream.close()

cap.release()
cv2.destroyAllWindows()