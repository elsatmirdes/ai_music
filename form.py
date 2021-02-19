# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QImage
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(404, 419)

        location_file = str(os.getcwd())
        replace = location_file.replace("\\", "/")

        oImage = QImage(f"{replace}/images/bg.jpg")
        sImage = oImage.scaled(QSize(404,419))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))                     # 10 = Windowrole
        MainWindow.setPalette(palette)


        self.extractAction = QAction("&Kapat",MainWindow)
        self.extractAction.setShortcut("Ctrl+Q")
        self.extractAction.setStatusTip('Kapat')

        self.listen_pos = QAction("&Pozitif Müzik",MainWindow)
        self.listen_pos.setShortcut("Ctrl+P")
        self.listen_pos.setStatusTip('Pozitif Müziği Dinle')

        self.listen_notr = QAction("&Nötr Müzik",MainWindow)
        self.listen_notr.setShortcut("Ctrl+O")
        self.listen_notr.setStatusTip('Nötr Müziği Dinle')

        self.listen_neg = QAction("&Negatif Müzik",MainWindow)
        self.listen_neg.setShortcut("Ctrl+N")
        self.listen_neg.setStatusTip('Negatif Müziği Dinle')

        mainMenu = MainWindow.menuBar()
        fileMenu = mainMenu.addMenu("&File") # menubar help
        mainMenu.setStyleSheet("color:black;")

        fileMenu.addAction(self.extractAction)
        fileMenu.addAction(self.listen_pos)
        fileMenu.addAction(self.listen_notr)
        fileMenu.addAction(self.listen_neg)

        MainWindow.setWindowIcon(QtGui.QIcon(f"{replace}/images/indir.png"))

        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.sentence = QtWidgets.QTextEdit(self.centralwidget)
        self.sentence.setGeometry(QtCore.QRect(50, 150, 311, 121))
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.sentence.setFont(font)
        self.sentence.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.sentence.setAcceptDrops(True)
        self.sentence.setStyleSheet("border-radius: 10px;\n"
"color:#FFF;\n"
"background:rgb(0,0,0,0.9);\n"
"padding-left: 15px;\n"
"font: 75 12pt \"System\";\n"
"")
        self.sentence.setObjectName("sentence")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 80, 92, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("font:bold 14px;\n"
"background:rgb(2, 37, 102);\n"
"border-style: outset;\n"
"border-width:2px;\n"
"border-radius:10px;")
        self.label.setObjectName("label")
        self.createbutton = QtWidgets.QPushButton(self.centralwidget)
        self.createbutton.setGeometry(QtCore.QRect(50, 300, 121, 51))
        self.createbutton.setGeometry(QtCore.QRect(50, 300, 121, 51))
        self.createbutton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.createbutton.setStyleSheet("border-style: outset;\n"
"border-width:2px;\n"
"border-radius:10px;\n"
"border-color:blue;\n"
"background:white;")
        self.createbutton.setToolTip('Create Music')
        self.createbutton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(f"{replace}/images/createimage.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.createbutton.setIcon(icon)
        self.createbutton.setIconSize(QtCore.QSize(100, 100))
        self.createbutton.setCheckable(True)
        self.createbutton.setChecked(False)
        self.createbutton.setAutoRepeat(False)
        self.createbutton.setAutoExclusive(False)
        self.createbutton.setAutoRepeatDelay(300)
        self.createbutton.setAutoDefault(False)
        self.createbutton.setDefault(True)
        self.createbutton.setFlat(False)
        self.createbutton.setObjectName("createbutton")
        self.playbutton = QtWidgets.QPushButton(self.centralwidget)
        self.playbutton.setGeometry(QtCore.QRect(250, 300, 111, 51))
        self.playbutton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playbutton.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.playbutton.setToolTip('Play Music')
        self.playbutton.setStyleSheet("border-style: outset;\n"
"border-width:2px;\n"
"border-radius:10px;\n"
"border-color:red;\n"
"background:rgb(226, 226, 226);")
        self.playbutton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(f"{replace}/images/playimage.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playbutton.setIcon(icon1)
        self.playbutton.setIconSize(QtCore.QSize(50, 100))
        self.playbutton.setCheckable(True)
        self.playbutton.setChecked(False)
        self.playbutton.setAutoRepeat(False)
        self.playbutton.setAutoExclusive(False)
        self.playbutton.setAutoRepeatDelay(300)
        self.playbutton.setAutoDefault(False)
        self.playbutton.setDefault(True)
        self.playbutton.setFlat(False)
        self.playbutton.setObjectName("playbutton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Create Music"))
        self.sentence.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'System\'; font-size:12pt; font-weight:72; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:-2px; margin-left:0px; margin-right:14px; -qt-block-indent:0; text-indent:0px; line-height:10px; background-color:transparent;\"><br /></p></body></html>"))
        self.sentence.setPlaceholderText(_translate("MainWindow", "Write something"))
        self.label.setText(_translate("MainWindow", "Cümle Girişi"))
