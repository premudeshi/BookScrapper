# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import QIcon, QPixmap
from bs4 import BeautifulSoup
import requests
import csv
import string
import os
import re

data = []


class Ui_MainWindow(object):
    def AddList(self, item):
        data.append(item)
        self.listWidget.addItem(item)

    def Scrape(self):
        outputfile = 'bookscrape.csv'
        csv_file = open(outputfile, 'w')
        csv_writter = csv.writer(csv_file)

        for x in data:
            try:
                urlopen1 = 'https://www.abebooks.com/products/isbn/' + x
                source = requests.get(urlopen1).text

                soup = BeautifulSoup(source, 'lxml')

                match = soup.find('div', class_='main-feature')
                # print(match)

                print('Title:')
                title = match.find('div', class_='plp-title').text
                print(title)

                print('synopsis:')
                synopsis = match.find('p', class_='synopsis-item').text
                print(synopsis)

                imgfind = soup.find('div', class_='feature-image')

                image_tags = imgfind.findAll('img')
                # print out image urls
                for image_tag in image_tags:
                    listimg = image_tag.get('src')
                    r = requests.get(listimg)

                    # open method to open a file on your system and write the contents
                    titler01 = re.sub('[^A-Za-z]', '', title)  # Assuming it is a string

                    namer = titler01 + '.jpg'
                    dir = 'images/' + namer
                    with open(dir, "wb") as code:
                        code.write(r.content)

                csv_writter.writerow([x, title, synopsis, namer])


            except:
                print("Book Doesn't Exist")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("BookScrapper")
        MainWindow.resize(733, 447)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 40, 256, 291))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(440, 180, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 340, 281, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(390, 140, 201, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, -10, 411, 141))
        font = QtGui.QFont()
        font.setFamily("American Typewriter")
        font.setPointSize(57)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 733, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(lambda:self.AddList(self.lineEdit.text()))
        self.pushButton_2.clicked.connect(lambda:self.Scrape())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Add"))
        self.pushButton_2.setText(_translate("MainWindow", "Begin Export"))
        self.label.setText(_translate("MainWindow", "BookScrapper"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

