from Tkinter import *
from tkMessageBox import *

# Import Tkinter to create gui
import Tkinter

# Import requests for HTTP functionality
import requests

# import requests.auth module to enable basic auth over https
from requests.auth import HTTPBasicAuth

# import configparsers to read and write configuration settings
from ConfigParser import SafeConfigParser

# or just the entire parser thingy
import ConfigParser

top = Tkinter.Tk()
top.title("Frideborg - The simple ePo search / delete tool")
top.iconbitmap(r'icon.ico')


# Method to query the ePo
def queryEPO():

# credentials stored in a non secure way
	eposerver = getEpoServer() 
	hostname = readTextfield()
	username = getUserName()
	password = getPassword()
	epocommand = getEpoCommand()
	textarea.delete(1.0,END)
	auth = HTTPBasicAuth(username,password)
	
	try:
		if epocommand == 'search':
			r = requests.get('https://'+eposerver+':8443/remote/system.find?searchText='+hostname,verify=False,auth=auth)
			s = r.text
			
		elif epocommand == 'delete':
			r = requests.get('https://'+eposerver+':8443/remote/system.delete?names='+hostname,verify=False,auth=auth)
			s = r.text
		
		else:
			s = "Something went wrong"
	except:
		print 'Unable to connect to server'
	
	textarea.insert(1.0, s)
	textarea.grid(row=6, column=0, columnspan=4, padx=5, pady=5)
	
	
	
# Methods to read the current value from the user supplied input:
def readTextfield():
	s = textfield.get()
	return s
	
def getUserName():
	s = usernametextfield.get()
	return s
	
def getPassword():
	s = passwordtextfield.get()
	return s
	
def getEpoServer():
	s = eposerverspinbox.get() 
	return s

def getEpoCommand():
	s = epocommandspinbox.get()
	return s
	
def showCurrentCommand():
	eposerver = getEpoServer()
	hostname = readTextfield()
	epocommand = getEpoCommand()
	
	if epocommand == 'search':
		s = 'https://'+eposerver+':8443/remote/system.find?searchText='+hostname
		showinfo('Current API call', s)
		
	elif epocommand == 'delete':
		s = 'https://'+eposerver+':8443/remote/system.delete?names='+hostname
		showinfo('Current API call', s)


def addNewServer():
	
	serverwindow = Tkinter.Toplevel()
	serverwindow.iconbitmap(r'icon.ico')
	serverwindow.title('Server settings')
	serverwindowlabel = Tkinter.Label(serverwindow, text='Comma separated server list that must end with a comma: host.domain.com,')
	serverwindowlabel.grid(row=0, column=0, padx=5, pady=5)
	
	# Read server hostnames from settings.conf
	p = SafeConfigParser()
	p.read('settings.conf')
	s = p.get('eposervers', 'servers')
	
	serverwindowtextfield = Tkinter.Entry(serverwindow, width=30)
	serverwindowtextfield.insert(0,s)
	serverwindowtextfield.grid(row=1, column=0, padx=5, pady=5)
	
	# Define a nested function to read the user updated serverwindowtextfield
	# and send it to the saveSettings function
	
	def tempRead():
		s = serverwindowtextfield.get()
		saveSettings(s)
	
	serverwindowbutton = Tkinter.Button(serverwindow, text="Save settings",command = tempRead)
	serverwindowbutton.grid(row=2, column=0, padx=5, pady=5)	

def saveSettings(s):
	Config = ConfigParser.ConfigParser()
	c = open('settings.conf','w')
	Config.add_section('eposervers')
	Config.set('eposervers','servers',s)
	Config.write(c)
	c.close()
	
	servers = readSettings()
	if len(servers)>1:
		eposerverspinbox = Tkinter.Spinbox(top,values=(servers),width=50)
		eposerverspinbox.grid(row=1, column=1, padx=5, pady=5)
	
	else:
		eposerverspinbox = Tkinter.Entry(top,width=50)
		eposerverspinbox.grid(row=1, column=1, padx=5, pady=5)
	
	
def showInformation():
	showinfo('Frideborg','A small tool written by robert@artandhacks.se')
	
def readSettings():
	try:
		p = SafeConfigParser()
		p.read('settings.conf')
		s = p.get('eposervers', 'servers')
		s = s.split(',')
		return s
	except:
		print ' '
		print 'Unable to load settings.conf'
		print 'Please ensure that settings.conf is present'
		print ' '
	
# null method that returns nothing...used for testing

	

	
	
# Add a label and a text field to read search names from
hostnamelabel = Tkinter.Label(top,text="Hostname, IP address or username:")
hostnamelabel.grid(row=0, column=0, padx=5, pady=5)
textfield = Tkinter.Entry(top,width=50)
textfield.grid(row=0, column=1, padx=5, pady=5)

# Add a listbox to select which ePo server will be queried
eposerverlabel = Tkinter.Label(top,text="ePo server:")
eposerverlabel.grid(row=1, column=0, padx=5, pady=5)
# Read stings of servers from settings file to add them to the spin box
# If no servers are present in the settings.conf file than a text field
# will be added instead
servers = readSettings()

if len(servers)>1:
	eposerverspinbox = Tkinter.Spinbox(top,values=(servers), width=50)
	eposerverspinbox.grid(row=1, column=1, padx=5, pady=5)
	
else:
	eposerverspinbox = Tkinter.Entry(top,width=50)
	eposerverspinbox.grid(row=1, column=1, padx=5, pady=5)

# Add a label and a text field to read user name from
usernamelabel = Tkinter.Label(top,text="ePo username:")
usernamelabel.grid(row=2, column=0, padx=5, pady=5)
usernametextfield = Tkinter.Entry(top,width=50)
usernametextfield.grid(row=2, column=1, padx=5, pady=5)

# Add a label and a text field to password from
passwordlabel = Tkinter.Label(top,text="Password:")
passwordlabel.grid(row=3, column=0, padx=5, pady=5)
passwordtextfield = Tkinter.Entry(top,width=50,show="*")
passwordtextfield.grid(row=3, column=1, padx=5, pady=5)

# Spinbox that defines the user requested epo interaction
epocommandlabel = Tkinter.Label(top,text="Search or delete:")
epocommandlabel.grid(row=4, column=0, padx=5, pady=5)
epocommandspinbox = Tkinter.Spinbox(top,values=('search','delete'),width='50')
epocommandspinbox.grid(row=4, column=1, padx=5, pady=5)

# Add button to top and pack it to make it visible

button = Tkinter.Button(top, text="go Frideborg!", command = queryEPO)
button.grid(row=5, column=1, padx=5, pady=5)

# Draw the default text area and pack it to make it visible from the start
tkwidth = top.winfo_reqwidth()
tkheight = top.winfo_reqheight()
textarea = Tkinter.Text(top,width=70,height=40)

textarea.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

# Draw the bottom footer and put some text in it
footerlabel = Tkinter.Label(top,text="2015 robert@artandhacks.se GPL")
footerlabel.grid(row=7, column=0,columnspan=4, padx=5, pady=5)

# Draw menu items
menubar = Tkinter.Menu(top)

# File menu
filemenu = Tkinter.Menu(menubar,tearoff=0)
filemenu.add_command(label="Show current command", command=showCurrentCommand)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=top.quit)
menubar.add_cascade(label="File", menu=filemenu)

# Settings menu
settingsmenu = Tkinter.Menu(menubar,tearoff=0)
settingsmenu.add_command(label="Edit server list", command=addNewServer)
menubar.add_cascade(label="Settings", menu=settingsmenu)

# About menu
aboutmenu = Tkinter.Menu(menubar,tearoff=0)
menubar.add_command(label="About", command=showInformation)

# Add menu to windown
top.config(menu=menubar)


top.mainloop()