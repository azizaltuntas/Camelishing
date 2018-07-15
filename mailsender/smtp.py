import smtplib
import os
import sys
from email.mime.application import MIMEApplication
from PyQt5.QtWidgets import QApplication , QMainWindow ,QFileDialog , QListWidget,QListWidgetItem ,QTreeWidgetItem ,QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import COMMASPACE
from email import encoders
from  messagebox import Message
from threading import Thread
from queue import *
from messagebox import Message
import logging


class SendMail(object):

    def skeleton(self,starttime,opentrackurl,attach,sender,message,subject, mailhost, passwd, smtp, port, getmail):

        # logging.basicConfig(
        #     filename=os.getcwd() + '\\sleuth\\mailOpenList\\' + starttime + '.txt',
        #     level=logging.INFO,
        #     format="%(asctime)s:%(levelname)s:%(message)s"
        # )

        mailsend = "sendmail"

        a = 0
        while True:
            try:
                a +=1
                mass = getmail.get()

                if '@gmail.com' in mass:

                    msg = MIMEMultipart()
                    msg['From'] = sender
                    msg['Subject'] = subject

                    messagetext = message
                    msg.attach(MIMEText(str(messagetext), 'plain'))


                    # Attachment Read

                    with open(attach, "rb") as file:

                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload((file).read())
                        encoders.encode_base64(part)
                        file = os.path.split(attach)
                        part.add_header('Content-Disposition', "attachment; filename= %s" % file[1])

                    html = "<img src='"+opentrackurl+"?" + '{}'.format(
                        mass) + "' width='1' " + " height='1'/>"

                    getlog = "nonsecretkey"

                else:
                    msg = MIMEMultipart('alternative')
                    msg['From'] = sender
                    msg['Subject'] = subject

                    messagetext = message
                    msg.attach(MIMEText(str(messagetext), 'plain'))

                    # Attachment Read

                    with open(attach, "rb") as file:

                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload((file).read())
                        encoders.encode_base64(part)
                        file = os.path.split(attach)
                        part.add_header('Content-Disposition', "attachment; filename= %s" % file[1])

                    getlog = "nonsecretkey"

                    html = "<p>"+messagetext+"</p>"+"<img src='"+opentrackurl+"?" + '{}'.format(
                        mass) + "' width='1' " + " height='1'/>"


                sender = msg['From']
                mail = smtplib.SMTP(smtp, port)
                mail.starttls()
                mail.login("{}".format(mailhost), '{}'.format(passwd))

                #Mail Open Track


                msg.attach(MIMEText(html, 'html'))
                msg.attach(part)

                #----------------

                msg['To'] = mass
                text = msg.as_string()




                mail.sendmail(sender, mass, text)
                del msg # No consecutive

                mail.set_debuglevel(0)
                mail.quit()
                getmail.task_done()

                with open(os.getcwd() + "\\sleuth\\mailOpenList\\" + starttime + ".txt",'a') as anan:

                    anan.write("Mail Send ! : "+ mass)

            except Exception as f:

                t, o, tb = sys.exc_info()

                print(f, tb.tb_lineno)
                getmail.task_done()
                sys.stderr.flush()


    def mess(self,text,inf,title):
        self.msg = QMessageBox()
        self.msg.setText('{}' .format(text))

        self.msg.setSizeGripEnabled(True)
        self.msg.setInformativeText('{}'.format(inf))
        self.msg.setWindowTitle('{}'.format(title))
        self.msg.setIcon(QMessageBox.Information)

        self.execmsg = self.msg.exec_()

    def __init__(self,thread,starttime,opentrackurl,attach, sender , subject , message , *sendto ,**kwargs):


        al = Queue()

        smtp = kwargs['smtpt']
        mailhost = kwargs['mailhost']
        passwd = kwargs['passwd']
        port = kwargs['port']

        thr = int(thread)

        null = ""


        try:
            mail = smtplib.SMTP(smtp, port)
            mail.starttls()
            mail.login("{}".format(mailhost), '{}'.format(passwd))
            mail.quit()


            for i in range(thr):
                self.t = Thread(target=self.skeleton, args=(starttime,opentrackurl,attach,sender,message,subject, mailhost, passwd, smtp, int(port), al))
                self.t.daemon = True
                self.t.start()


            for mass in sendto:
                al.put(mass)

            al.join()

            os.startfile(os.getcwd() + '\\sleuth\\mailOpenList\\' + starttime + '.txt')

        except smtplib.SMTPAuthenticationError:
            print("Authentication Error", "Wrong Username or Password !", "Info")
            sys.stderr.flush()


        except smtplib.SMTPConnectError:
            print("Connection Error", "SMTP Server Down !", "Info")
            sys.stderr.flush()

        except smtplib.SMTPNotSupportedError:
            print("Support Error", "SMTP Not Supported !", "Info")
            sys.stderr.flush()

        except Exception as f:

            t, o, tb = sys.exc_info()
            print(f, tb.tb_lineno)
            sys.stderr.flush()

        #SendMail.skeleton(null,msg,mailhost,passwd,smtp,int(port),*sendto)
