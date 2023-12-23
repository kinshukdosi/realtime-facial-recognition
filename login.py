from tkinter import *

def login():
	'''Creates login window, accepts a username and password as input and
	allows the user to submit this information'''

	def validate():
		'''Validates the users credentials by comparing them against 
		previously stored credentials in a text file'''

		file = open('login.txt') # Opens text file with correct credentials
		lines = file.readlines() # Reads the lines from the file into python
		correct_username = lines[0].strip() 
		# Sets the username to the first line and removes trailing and leading whitespace
		correct_password = lines[1].strip()
		# Sets the password to the second line and removes trailing and leading whitespace

		if username.get() == correct_username and password.get() == correct_password:
			# Comparing user input to the correct credentials
			loginWindow.destroy() # Destroying login window
		else:
			loginWindow.destroy() # Destroying login window
			login() # Running parent function again if credentials entered are incorrect

	loginWindow = Tk() # Creating window
	loginWindow.geometry('300x300') # Setting dimensions of window
	loginWindow.title('Login') # Setting title of window to 'Login'

	username_label = Label(loginWindow, text='Enter username: ').grid(row=0, column=0)
	# Adds label to tell user where to enter username
	username = StringVar() # Tkinter StringVar object that will contain the input
	username_input = Entry(loginWindow, textvariable=username).grid(row=0, column=1)
	# Entry box for user to enter username

	password_label = Label(loginWindow, text='Enter password: ').grid(row=1, column=0)
	# Adds label to tell user where to enter password
	password = StringVar() # Tkinter StringVar object that will contain the input
	password_input = Entry(loginWindow, textvariable=password, show='*').grid(row=1, column=1)
	# Entry box for user to enter password

	login_button = Button(loginWindow, text='Login', command=validate).grid(row=2, column=0)
	# Button that submits the login details and runs the validate function 

	loginWindow.mainloop() # Starts window

