from tkinter import *
from PIL import Image, ImageTk
import cv2, os, pickle, face_recognition, subprocess
from login import login
from main import start


def runCamera():
    camera = dropdown.get() # Gets the currently selected option on the dropdown menu
    if camera == 'Select camera input': # Checks if no camera has been selected
        print('No camera selected') 
    else:
        cameraID = cameralist.index(camera) # Gets the camera ID 
        start(cameraID) # Starts camera feed window

def getCameraList():
    '''Returns list of connected video inputs by running a bash command and reading the output'''
    
    cameras = os.popen('system_profiler SPCameraDataType | grep "^    [^ ]" | sed "s/    //" | sed "s/://"')
    # Gets cameras as a string seperated by new lines
    cameralist = []
    for camera in cameras:
        cameralist.append(camera.strip()) 
        # Adds the cameras to the list individually while removing trailing new lines, \n

    return cameralist



def settingsMenu():
    '''Creates settings menu which allows the user to enter a recipient email address for alerts'''

    def setEmail():
        '''Writes the alert email given by the user to alertemail.txt'''

        email = alert_entry.get() # Retrieving input from entry box
        if '@' not in email:
            print('Invalid email address, please retry')
            return 
        if '.' not in email:
            print('Invalid email address, please retry')
            return 

        with open('alertemail.txt', 'w+') as file:
            file.write(email) # Writing email address to file
        settings.destroy() # Closing the settings menu

    settings = Tk() # Initialising settings menu window
    settings.geometry("400x400") # Setting window size

    alert_label = Label(settings, text='Enter alert recipient email: ') 
    alert_label.grid(row=0, column=0)
    alert_entry = Entry(settings)
    alert_entry.grid(row=0, column=1)

    submit = Button(settings, text='Submit', command=setEmail) 
    submit.grid(row=1, column=0)

    settings.mainloop() # Opens window


login() # Start login process

window = Tk() # Create window
window.geometry("700x350") # Set window size

settings = Button(window, text='Open settings', width=15, height=15, command=settingsMenu)
# Open settings menu button
settings.grid(row=0, column=2)

cameralist = getCameraList() # Gets list of connected cameras
dropdown = StringVar(window) # Holds the label for the dropdown
dropdown.set("Select camera input") # Sets label text
selectCamera = OptionMenu(window, dropdown, *cameralist) 
# Creates dropdown using the list of cameras as options
selectCamera.grid(row=1, column=0)
# Places the menu onto the window


button = Button(window, text='Open camera', width=30, height=15, command=runCamera)
# Open camera button
button.grid(row=0, column=0)
window.mainloop()

# print("Streaming started")
# video = cv2.VideoCapture(0)
# video.set(3, 100)
# video.set(4, 100)

# cascPathface = os. path.dirname(
#  cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# faceCascade = cv2.CascadeClassifier(cascPathface)
# data = pickle.loads(open('face_enc', "rb").read())

# def display():
#     ret, frame = video.read()
#     frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = faceCascade.detectMultiScale(gray,
#                                             scaleFactor=1.1,
#                                             minNeighbors=5,
#                                             minSize=(60, 60),
#                                             flags=cv2.CASCADE_SCALE_IMAGE)
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     encodings = face_recognition.face_encodings(rgb)


#     image = Image.fromarray(frame)
#     imagetk = ImageTk.PhotoImage(image = image)

#     label.imgtk = imagetk
#     label.configure(image=imagetk)
#     label.after(20, display)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         quit()


