import socket
import pickle , json
import threading
import os

class Server(threading.Thread):

    def __init__(self, hs,c):
        threading.Thread.__init__(self)

    def run(self):
        self.message = "Okey"

        while True:
            try:

                self.data = c.recv(1024)
                self.data = json.loads(self.data.decode("utf-8"))

                hostname = self.data.get("hostname")
                ipadress = self.data.get("ipadress")
                opentime = self.data.get("time")
                platform = self.data.get("platform")  # Two Key ([Windows10,32bit])
                username = self.data.get("username")

                for host in hostname:
                    HOSTNAME.append(host)
                    for user in username:
                        USERNAME.append(user)
                        for ip in ipadress:
                            IPADRESS.append(ip)
                            for optime in opentime:
                                TIME.append(optime)
                                for plat in platform:
                                    PLATFORM.append(plat)


                # HOSTNAME.append(hostname)
                # IPADRESS.append(ipadress)
                # PLATFORM.append(platform)
                # USERNAME.append(username)
                # TIME.append(opentime)

                with open(os.getcwd()+'\\dist\\a.txt','w') as h:
                    h.write(HOSTNAME)

                print(HOSTNAME,IPADRESS,TIME,PLATFORM,USERNAME)

            except:

                break

        c.close()

host = NONE
port = 4444

_ = []
HOSTNAME = []
IPADRESS = []
TIME = []
PLATFORM = []
USERNAME = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))

while True:
    s.listen(400)
    c, hs = s.accept()
    thread = Server(hs,c)
    thread.daemon = True
    thread.start()
