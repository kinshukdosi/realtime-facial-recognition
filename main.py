import cv2, face_recognition, pickle, os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from tkinter import *

cascPathface = os.path.dirname(
 cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPathface)
data = pickle.loads(open('face_enc', "rb").read()) # Face encodings of previously stored images of people
noInput = cv2.imread('noInput.png')


def startVideo(cameraID):
    ''' Checks video is valid, requires a cameraID argument.
    Returns False if invalid and returns the video object if valid '''

    video = cv2.VideoCapture(cameraID)
    if video.isOpened() == False: # .isOpened() checks if the video is available
        print(f'Camera with ID {cameraID} not detected')
        return False
    return video

def analyseFrame(video):
    ''' Analyses given video for faces, compares with images in 'Images'
    folder and overlays frame with name and box around the detected face'''
    
    if isinstance(video, cv2.VideoCapture) != True:
        print('Video object is invalid')
        return noInput

    ret, frame = video.read() # Retrieve single frame from video
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converts frame to grayscale, this improves performance
    faces = faceCascade.detectMultiScale(gray, 
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(60, 60), 
                                        # Minimum object size; faces smaller than 60x60 pixels are ignored
                                        flags=cv2.CASCADE_SCALE_IMAGE) 
    
    if type(faces) is tuple: # Returns frame early if no face detected - Saves processing power
        return frame

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Changing color space to rgb
    encodings = face_recognition.face_encodings(rgb) # Returns face encoding for each face in the frame
    
    names = [] # List to hold the names of the detected person(s) in the frame
    for encoding in encodings: # Looping over each encoding (face)
    
        matches = face_recognition.compare_faces(data["encodings"], # Comparing face in frame to those previously stored
        encoding)
        
        name = "Unknown" # Default name is unknown - will change if person is recognised

        if True in matches: 
            matchedID = [i for (i, b) in enumerate(matches) if b] # Retrieving indexes of matching images from the 'Images' folder
            counts = {} # Used to store how many images match the face in the current frame
            
            for i in matchedID:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        names.append(name) # The person who matches strongest with the person in the frame is stored

         
        for ((x, y, w, h), name) in zip(faces, names):
            if name == "Unknown":
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) # Placing red box around face if unrecognised
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Placing green box around the face if recognised
            cv2.putText(frame, name, (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, # Writing text to identify face
            1, (0, 255, 0), 2)
        
        for name in names:
            if name == "Unknown": # If person is not recognised
                alert(frame) # Alert function will go here
                
    return frame # Returns the frame with analysis complete and any necessary boxes/text written

alerted = []
def alert(frame):
    '''Sends an email with the current frame as an attachment'''

    time = datetime.now() # Gets the current date and time 

    try:
        time_since_last_alert = time - alerted[-1] # Calculates the time since the last 
        if time_since_last_alert.total_seconds() < 30:
            return
    except:
        pass

    filename = f"{time}.jpg"
    cv2.imwrite(filename, frame)

    with open('alertemail.txt', 'r') as file:
        recipient = file.read()
    # Gets recipient email from external file which user sets from the settings menu
    
    subject = f"Alert on {time}" # Email subject
    sender = "kinshuk.dosi@gmail.com" # Email sender
    password = "lduiuhkmqibjjpwg" # Password to email account

    message = MIMEMultipart() # Email multipart object to allow for attachments to be attached
    message['Subject'] = subject # Sets the message subject
    message['From'] = sender # Sets the sender
    message['To'] = recipient # Sets the recipient

    with open(filename, 'rb') as fp: # Opens the frame file in python
        img = MIMEImage(fp.read()) # Reads the image into an email image object
        img.add_header('Alert', 'attachment', filename="alert.jpg") 
        message.attach(img) # Attachs the email
    
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465) # Sets the server to gmail 
    smtp_server.login(sender, password) # Logins in with the previous given email and password
    smtp_server.sendmail(sender, recipient, message.as_string()) # Sends the email
    smtp_server.quit() # Quits the smtp server

    alerted.append(time)
    

def start(cameraID):
    video = startVideo(cameraID)
    while True:
        frame = analyseFrame(video=video)
        
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
