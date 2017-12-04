# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:19:19 2017

@author: WSD
"""

import sys
 
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton,QGridLayout,QLabel,QSplitter
from PyQt5.QtGui import QPixmap
#%%
 
class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 1.0
        self.initUI()  
    def initUI(self):
        self.readImgBtn = QPushButton('ReadImg')
        #self.readImgBtn.setFixedSize(self.readImgBtn.size())
        self.showImgLabel = QLabel('image')
        self.showImgLabel.setAlignment(Qt.AlignCenter)
        self.showImgLabel.setMouseTracking(True)
       
        self.image = QPixmap()
               
        self.splitterRight = QSplitter(Qt.Vertical)
        self.splitterRight.addWidget(self.showImgLabel)
        self.splitterMain = QSplitter(Qt.Horizontal,self)
        self.splitterMain.addWidget(self.readImgBtn)
        self.splitterMain.addWidget(self.splitterRight)
        
        self.splitterMain.setStretchFactor(0,0)
        self.splitterMain.setStretchFactor(1,1)
        self.splitterMain.resize(800,600)
        self.readImgBtn.clicked.connect(self.readImage)

    def wheelEvent(self,event):
        delta = event.angleDelta()
        numDegress = delta.y()/8
        if numDegress > 0:
            self.scale *= 1.2
        else:
            self.scale /= 1.2
        self.showImage()
    def showImage(self):
        self.showImgLabel.setPixmap(self.image.scaled(800*self.scale,600*self.scale,Qt.KeepAspectRatio))
    def readImage(self):
        self.image=QPixmap('E:/wsd/index.jpg')
        self.showImgLabel.setPixmap(self.image)
    """
    def closeEvent(self,event):
        reply = QMessageBox.question(self,'Message','Are you sure to exit?',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    """
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ImageViewer()
    w.show()
    sys.exit(app.exec_())
