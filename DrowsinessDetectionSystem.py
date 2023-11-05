import numpy as np
import argparse
import dlib
import cv2
import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tkinter import Frame,Label,Tk,Button,Canvas,PhotoImage,messagebox,CENTER,TOP,BOTTOM,X,FLAT,SOLID, simpledialog
from PIL import ImageTk,Image
import pyttsx3
from threading import Thread
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from imutils import face_utils
import imutils
import geocoder
import pygame
import time

counter = 0
counter_noti = 0
eyes_closed_time = 0
eyes_closed_threshold = 5  # Number of consecutive frames to consider as eyes closed
alarm_playing = False

# email alert 
SENDER_EMAIL = '1191101595@student.mmu.edu.my'
SENDER_PASSWORD = 'Bl2001_'

# google map location
g_maps_url = "http://maps.google.com/?q={},{}"

# twilio sms account 
account_sid = "ACc5047a92eae205fbba09d0c9759ed579"
auth_token = "28bb97f840e74bdec6618662ea4328c5"
client = Client(account_sid, auth_token)

# face detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"shape_predictor_68_face_landmarks.dat")

# load eye and mouth yawn model
model_eye = tf.keras.models.load_model(r"Version2-Eye Model\EyeEnsemble-0.974.h5")
model_yawn = tf.keras.models.load_model(r"Version2-Mouth Model\MouthEnsemble-0.965.h5") 

# Mute / Unmute Volume Button
def mute_music():
    global muted
    
    if muted:
        btn_volume.configure(image=volume_photo)
        muted=False
    else:
        btn_volume.configure(image=mute_photo)
        muted=True

# Play Warning sound
def play_warning():
    engine.say("HEY!, WAKE UP.")
    engine.runAndWait()
    engine.stop()

# Play Alarm sound
def play_alarm():
    global alarm_playing
    alarm_playing = True
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play(loops=0)

def stop_alarm():
    global alarm_playing
    alarm_playing = False
    pygame.mixer.music.stop()

# Eye feature extraction  
def crop_eye(img):
    IMG_SIZE = 50
    faces = 0
    roi = img.copy()

    try:
        image_array = img.copy()
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        if(len(rects) < 0):
            return faces, 0
        for (i, rect) in enumerate(rects):
            faces = len(rects)
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            coor_i, coor_j = (43, 48)
            (x, y, w, h) = cv2.boundingRect(np.array([shape[coor_i:coor_j]]))
            roi = gray[y-(3*h):y+(2*h), x-w:x +(2*w)]
            roi = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))

    except Exception as e:
            print(e)
    
    return faces, roi

# Mouth Feature Extraction 
def crop_mouth(img):
    IMG_SIZE = 50
    faces = 0
    roi = img.copy()

    try:
        image_array = img.copy()
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        if(len(rects) < 0):
            return faces, 0
        for (i, rect) in enumerate(rects):
            faces = len(rects)
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            coor_i, coor_j = (48, 68)
            (x, y, w, h) = cv2.boundingRect(np.array([shape[coor_i:coor_j]]))
            roi = gray[y:y + h, x:x + w]
            roi = cv2.resize(roi, (IMG_SIZE, IMG_SIZE))

    except Exception as e:
            print(e)
            
    return faces, roi

def predictEyes(roi):
    roi = np.array(roi).reshape(-1,50,50,1)
    roi = roi.astype('float32') / 255.0
    pred = model_eye.predict(roi)
    if pred < 0.5:
        return 0
    return 1

def predictYawn(roi):
    roi = np.array(roi).reshape(-1,50,50,1)
    roi = roi.astype('float32') / 255.0
    pred = model_yawn.predict(roi)
    if pred < 0.5:
        return 0
    return 1

def settings_page():
    global RECEIVER_EMAIL
    RECEIVER_EMAIL = simpledialog.askstring("Input", "Enter receiver address: ", initialvalue=RECEIVER_EMAIL, parent=root)
    if RECEIVER_EMAIL is None:
        RECEIVER_EMAIL = 'bellelim0621@gmail.com'

def send_email(frame):
    
    if isinstance(frame, str):
        return
    
    msg = EmailMessage()
    msg['Subject'] = 'Alert Driver Drowsiness Detected'
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg.set_content('Instance of Driver Drowsiness Detected \n See image attached below...')
    
    success, encoded_image = cv2.imencode('.jpg', frame)
    image = encoded_image.tobytes()
    msg.add_attachment(image, maintype='image', subtype='jpg', filename='driver.jpg')
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(msg)
        
    messagebox.showinfo("ALERT",  "Multiple Instances of Drowsiness Detected, sending email and sms to your emergency contact.")

def get_current_location(g_maps_url):
    g = geocoder.ip('me')

    lat = g.latlng[0]
    long = g.latlng[1]
    
    current_location =  g_maps_url.format(lat, long)
    return current_location

def sms_alert(current_location):
    message = client.messages.create(
                        body="Alert ! Multiple Instances of Drowsiness Detected. Last known location {} ".format(current_location),
                        from_="+15738892169",
                        to="+60162300225"
                        )

def display_video():
    global th
    global th2
    global counter
    global counter_noti
    global eyes_closed_time
    ret, frame = vid.read()
    frame = imutils.resize(frame, width=700)
    text_eye = 'N/A'
    text_yawn = 'N/A'
    faces_eye, roi_eye = crop_eye(frame)
    faces_yawn, roi_yawn = crop_mouth(frame)
    
    #check if dlib detects any faces
    if (faces_eye <= 0 or faces_yawn <= 0):
        text_eye = 'N/A'
        text_yawn = 'N/A'
    else:
        pred_eye =  predictEyes(roi_eye)
        pred_yawn =  predictYawn(roi_yawn)

        if pred_eye == 0:
            text_eye = 'closed'
        else:
            text_eye = 'open'

        if pred_yawn == 0:
            text_yawn = 'No yawn'
        else:
            text_yawn = 'Yawn'
            
        if pred_eye == 0 or pred_yawn == 1:
            eyes_closed_time += 1
            counter += 1
            
            if eyes_closed_time >= eyes_closed_threshold and not alarm_playing:
                th = Thread(target=play_alarm, daemon=True)
                th.start()
                
            if not th.is_alive() and not muted:
                if pred_eye == 0 or pred_yawn == 1:
                    counter_noti += 1
                    cv2.putText(frame, 'WARNING ', (0, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)
                    th = Thread(target=play_warning, daemon=True)
                    th.start()
                
                if counter_noti >= 3:
                    counter_noti = 0
                    th2 = Thread(target=send_email, args=[frame], daemon=True)
                    current_location = get_current_location(g_maps_url)
                    sms_alert(current_location)
                    th2.start()
                
            if counter < 1:
                th = Thread(target=stop_alarm, daemon=True)
                th.start()
            
        else:
            eyes_closed_time = 0
            counter = 0
            if alarm_playing:
                th = Thread(target=stop_alarm, daemon=True)
                th.start()

    cv2.putText(frame, 'Both eyes '+text_eye, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
    cv2.putText(frame, text_yawn, (0, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
    
    # Convert image from one color space to other
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert image to PhotoImage and apply on webcam_label 
    # Capture the latest frame and transform to image
    img = Image.fromarray(frame)
    # Convert captured image to photoimage
    imgtk = ImageTk.PhotoImage(image = img)
    # Displaying photoimage in the label
    webcam_label.imgtk = imgtk
    # Configure image in the label
    webcam_label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    # Repeat the same process after every 10 seconds
    webcam_label.after(10, display_video)

# Initialize pygame for playing alarm sound
pygame.mixer.init()

 # define a video capture object
vid = cv2.VideoCapture(0)

if not vid.isOpened():
    messagebox.showerror("Error","Unable to open webcam/camera.")
else:

    # declare variables
    font = ("bahnschrift",12)
    title_font = ("bahnschrift",20,"bold")
    muted = False
    RECEIVER_EMAIL = 'bellelim0621@gmail.com'
    
    engine = pyttsx3.init()
   
    th = Thread(target=play_warning, args=[''],daemon = True)
    th2 = Thread(target=send_email, args=[''],daemon = True)
    
    # prepare root window
    root = Tk()
    root.title('Drowsiness Detection System')
    root.geometry("1163x705")
    
    canvas = Canvas(
    root,
    bg = "#FFFFFF",
    height = 705,
    width = 1163,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(
        file=r"Icons\image_1.png")
    image_1 = canvas.create_image(
        581.0,
        352.0,
        image=image_image_1
    )

    canvas.create_rectangle(
    1082.0,
    267.0,
    1151.0,
    439.0,
    fill="#153961",
    outline="")

    canvas.create_text(
    129.0,
    60.0,
    anchor="nw",
    text="DROWSINESS DETECTION SYSTEM",
    fill="#FFFFFF",
    font=("Inter Black", 48 * -1)
    )
    #
    #image_image_2 = PhotoImage(
    #file=(r"Icons\image_2.png"))
    #image_2 = canvas.create_image(
    #    581.0,
    #    79.0,
    #    image=image_image_2
    #)
    
    # webcam
    webcam_label = Label(root)
    webcam_label.place(relx = 0.5,
                   rely = 0.6,
                   anchor = 'center')

    # settings button
    settings_photo = PhotoImage(file=r"Icons\settings.png")
    btn_settings = Button(root, font=font, image=settings_photo,cursor="hand2",relief=FLAT, overrelief=SOLID, command=settings_page)
    btn_settings.place(x=1093.0,
    y=285.0,
    width=46.0,
    height=47.0)

    # volume button
    mute_photo = PhotoImage(file=r"Icons\mute.png")
    volume_photo = PhotoImage(file=r"Icons\unmute.png")
    btn_volume = Button(root, image=volume_photo, relief=FLAT, overrelief=SOLID, cursor="hand2", command=mute_music)
    btn_volume.place(x=1093.0,
    y=362.0,
    width=46.0,
    height=47.0)
    
    display_video()
    
    # place window at center when opening
    #root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()
