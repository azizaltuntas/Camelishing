from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class Message(object):

    def mess(self, text, inf, title):
        self.msg = QMessageBox()
        self.msg.setText('{}'.format(text))
        self.msg.setInformativeText('{}'.format(inf))
        self.msg.setWindowTitle('{}'.format(title))
        self.msg.setIcon(QMessageBox.Information)

        self.execmsg = self.msg.exec_()

    def __init__(self,text,inf,title):

        self.mess(text,inf,title)

