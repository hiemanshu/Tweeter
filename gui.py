#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import ConfigParser
import os.path
import twitter, sys

class Ui_Dialog(object):
    def updateStatus(self):
        config = ConfigParser.ConfigParser()
        config.read(os.path.expanduser('~/.tweetrc'))
        conskey = config.get("Tweet", "conskey", raw=True)
        conssec = config.get("Tweet", "conssec", raw=True)
        accstkn = config.get("Tweet", "accstkn", raw=True)
        accssec = config.get("Tweet", "accssec", raw=True)
        status = self.lineEdit.text()
        print status
        api = twitter.Api(consumer_key=conskey, consumer_secret=conssec, access_token_key=accstkn, access_token_secret=accssec)
        api.PostUpdates(status)
 
    def setupUi(self, Dialog):
        global lineEdit
        Dialog.setObjectName("Dialog")
        Dialog.resize(610, 356)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(0, 20, 601, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(0, 60, 181, 27))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.updateStatus) 
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Tweeter", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Update Status", None, QtGui.QApplication.UnicodeUTF8))


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
