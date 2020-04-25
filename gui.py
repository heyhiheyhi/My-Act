## Ex 5-3. QCheckBox.

import sys
import cv2
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QLineEdit, QLabel, QPushButton, QFileDialog


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    #layout
    def initUI(self):

        #resize
        self.qle1 = QLineEdit(self)
        self.qle1.move(100, 20)
        self.qle1.resize(80, 25)
        self.width=0
        self.qle1.setInputMask("0000")
        self.qle1.setAlignment(Qt.AlignCenter)
        self.qle1.textChanged[str].connect(self.setWidth)

        self.qle1_1 = QLineEdit(self)
        self.qle1_1.move(200, 20)
        self.qle1_1.resize(80, 25)
        self.height=0
        self.qle1_1.setAlignment(Qt.AlignCenter)
        self.qle1_1.setInputMask("0000")
        self.qle1_1.textChanged[str].connect(self.setHeight)

        #rotate
        self.qle2 = QLineEdit(self)
        self.qle2.move(100, 50)
        self.qle2.resize(100, 25)
        self.qle2.setAlignment(Qt.AlignCenter)
        self.qle2.setInputMask("0000")
        self.qle2.textChanged[str].connect(self.setRotation)

        #hflip
        self.qle3 = QLineEdit(self)
        self.qle3.move(100, 170)
        self.qle3.resize(100, 25)

        #vflip
        self.qle4 = QLineEdit(self)
        self.qle4.move(300, 170)
        self.qle4.resize(100, 25)
        self.qle4.setAlignment(Qt.AlignCenter)
        self.qle4.textChanged[str].connect(self.getName)

        #rename
        self.qle5 = QLineEdit(self)
        self.qle5.move(100, 230)
        self.qle5.resize(350, 25)

        self.label0 = QLabel('x', self)
        self.label0.move(187, 25)

        self.label1 = QLabel('prefix', self)
        self.label1.move(130, 140)

        self.label2 = QLabel('suffix', self)
        self.label2.move(330, 140)

        self.label3 = QLabel('number', self)
        self.label3.move(220, 170)

        self.label4 = QLabel('PATH', self)
        self.label4.move(20, 230)

        self.btn1 = QPushButton('&RUN', self)
        self.btn1.move(300, 20)
        self.btn1.resize(80,40)
        #self.btn1.setCheckable(True)
        self.btn1.clicked.connect(self.RunClicked)

        self.btn2 = QPushButton('&FileOpen', self)
        self.btn2.move(400, 20)
        self.btn2.resize(80, 40)
        #self.btn2.setCheckable(True)
        self.btn2.clicked.connect(self.OpenClicked)

        self.cb1 = QCheckBox('Resize',self)
        self.cb1.move(20, 20)
        self.cb1.stateChanged.connect(self.Check)

        self.cb2 = QCheckBox('rotate', self)
        self.cb2.move(20, 50)
        self.cb2.stateChanged.connect(self.Check)

        self.cb3 = QCheckBox('hflip', self)
        self.cb3.move(20, 80)
        self.cb3.stateChanged.connect(self.Check)

        self.cb4 = QCheckBox('vflip', self)
        self.cb4.move(20, 110)
        self.cb4.stateChanged.connect(self.Check)

        self.cb5 = QCheckBox('rename', self)
        self.cb5.move(20, 140)
        self.cb5.stateChanged.connect(self.Check)

        self.setWindowTitle('Type Here')
        self.setGeometry(700, 300, 500, 280)
        self.show()

    def OpenClicked(self):
        global fname
        fname = QFileDialog.getOpenFileName(self, "open File", "/home/ss/다운로드/mb7500/","Images (*.png *.xpm *.jpg)")
        self.qle5.setText(fname[0])

    def RunClicked(self):
        #sender = self.sender()
        img1 = cv2.imread(fname[0])
        img2 = cv2.imread(fname[0])
        img3 = cv2.imread(fname[0])
        img4 = cv2.imread(fname[0])
        img5 = cv2.imread(fname[0])
        if self.cb1.isChecked()== 1 :
            #img1 = cv2.imread(fname[0])
            img2 = cv2.resize(img1, dsize=(self.width, self.height),interpolation=cv2.INTER_LINEAR)
            #cv2.imwrite('resi_img.jpg',img2)
            #cv2.imshow("resi_img",img2)
            img5=img4=img3=img2


        if self.cb2.isChecked() == 1 :
            #img2 = cv2.imread(fname[0])
            #cv2.imshow("img",img2)
            h, w, c = img2.shape
            #print(self.rotation)
            #print(h)
            #print(w)
            M1 = cv2.getRotationMatrix2D((w / 2, h / 2), self.rotation, 1)
            img3 = cv2.warpAffine(img2, M1,(w,h))
            #cv2.imshow('rota_img', img3)
            cv2.waitKey(1000)
            #cv2.imwrite('rota_img.jpg', img3)
            img5=img4=img3

        if self.cb3.isChecked() == 1 :
            #img3 = cv2.imread(fname[0])
            #cv2.imshow("img",img)
            img4 = cv2.flip(img3, 0)
            #cv2.imshow("hflip_img", img4)
            #cv2.imwrite("hflip_img.jpg", img4)
            img5 = img4

        if self.cb4.isChecked() == 1 :
            #img4 = cv2.imread(fname[0])
            #cv2.imshow("img",img)
            img5 = cv2.flip(img4, 1)
            #cv2.imshow("vflip_img", img5)
            #cv2.imwrite("vflip_img.jpg", img5)

        if self.cb5.isChecked() == 1 :
            print(self.newName)
            sp_fname = fname[0].split('/')
            #print(len(sp_fname))
            #print(sp_fname[:len(sp_fname)-1])
            #print(sp_fname[1])
            new_fname = ""
            for i in range(1,len(sp_fname)-1) :
                print(i)
                new_fname = new_fname + '/' + sp_fname[i]

            print(new_fname)
            new_fname = new_fname + '/' + self.newName + '.jpg'
            print(new_fname)
            os.rename(fname[0],new_fname)
            self.qle5.setText(new_fname)

        cv2.imshow("final_img", img5)
        cv2.imwrite('final_img.jpg', img5)

    def Check(self, text):
        sender= self.sender()
        if sender.isChecked() == True:
            print("Is checked")

    def setWidth(self):
        self.width = int(self.qle1.text())

    def setHeight(self):
        self.height = int(self.qle1_1.text())

    def setRotation(self):
        self.rotation = int(self.qle2.text())

    def getName(self):
        self.newName = self.qle4.text()
        #print(type(self.newName))
        print(self.newName)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())