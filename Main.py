#Note : Due to compatibility issues with pyaudio, This module will not work on python 3.5 or higher
#IMPORT HERE..
import cv2
import numpy as np
import pyaudio
import wave
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkfont


#INITIALISE HERE
cap = cv2.VideoCapture(0)
aud = pyaudio.PyAudio()
vid_frame_width = int(cap.get(3))
vid_frame_height = int(cap.get(4))
root = tk.Tk()
root.minsize(1200,800)
app = tk.Frame(root, bg="white")
app.place (x = 870, y = 10)
app2 = tk.Frame(root, bg="white")
app2.place(x = 10, y = 10)
app3 = tk.Frame(root, bg="white")
app3.place(x = 10, y = 130)
app4 = tk.Frame(root, bg="white")
app4.place(x = 870, y =400)

question_Font = tkfont.Font(family="Comic Sans MS",size=20 )
option_Font = tkfont.Font(family="Comic Sans MS",size=15 )

#DEMO FUNCTIONS..
def selected():
    print("The option selected is "+ str(var.get())) 

def button_1():
    print("You clicked button 1")
def button_2():
    print("You clicked button 2")
def button_3():
    print("You clicked button 3")
def button_4():
    print("You clicked button 4")
def button_5():
    print("You clicked button 5")
def button_6():
    print("You clicked button 6")


#DEMO COMPONENTS
question = tk.Label(app2, text = "The question will appear here! This is a sample question.\n 11. How many days are present in a leap year?",width = 50, padx = 10 , pady = 10, anchor = 'nw', font = question_Font)
question.grid()
lmain = tk.Label(app,anchor = 'ne')
lmain.grid(row = 1, column = 1)
var = tk.IntVar()
op1 = tk.Radiobutton(app3, text="Option 1: 364", variable=var, value=1,command=selected, font = option_Font)
op1.pack(anchor = 'w')
op2 = tk.Radiobutton(app3, text="Option 2: 365", variable=var, value=2,command=selected, font = option_Font)
op2.pack(anchor = 'w')
op3 = tk.Radiobutton(app3, text="Option 3: 366", variable=var, value=3,command=selected, font = option_Font)
op3.pack(anchor = 'w')
op4 = tk.Radiobutton(app3, text="Option 4: 367", variable=var, value=4,command=selected, font = option_Font)
op4.pack(anchor = 'w')

b1 = tk.Button(app4, padx = 3,pady = 3, width = 10, height = 3, text = 'Q.1', command = button_1, relief = 'raised', bd = 4)
b1.grid(column = 1, row = 1)
b2 = tk.Button(app4, padx = 3,pady = 3, width = 10, height = 3, text = 'Q.2', command = button_2, relief = 'raised', bd = 4)
b2.grid(column = 2, row = 1)
b3 = tk.Button(app4, padx = 3,pady = 3, width = 10, height = 3, text = 'Q.3', command = button_3, relief = 'raised', bd = 4)
b3.grid(column = 3, row = 1)
b4 = tk.Button(app4, padx = 3,pady = 3, width = 10, height = 3, text = 'Q.4', command = button_4, relief = 'raised', bd = 4)
b4.grid(column = 1, row = 2)
b5 = tk.Button(app4, padx = 3,pady = 3, width = 10, height = 3, text = 'Q.5', command = button_5, relief = 'raised', bd = 4)
b5.grid(column = 2, row = 2)
b6 = tk.Button(app4, padx = 3,pady = 3, width = 10, height = 3, text = 'Q.6', command = button_6, relief = 'raised', bd = 4)
b6.grid(column = 3, row = 2)


#DYNAMIC COMPONENTS..
status = tk.Label(app, text = 'The status will show here!', font = option_Font)
status.grid(row = 2, column = 1)

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
            
            final_audio = ("Audio_"+str(av_index)+'.wav','wb')
            final_audio.setnchannels(CHANNELS)
            final_audio.setsampwidth(aud.get_sample_size(FORMAT))
            final_audio.setframerate(RATE)
            final_audio.writeframes(b''.join(audio_output))
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

    imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2.resize(vid_frame, (0, 0), fx = 0.5, fy = 0.5) , cv2.COLOR_BGR2RGBA)))
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