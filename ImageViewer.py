# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:19:19 2017

@author: WSD
"""
import sys
import cv2
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel,QHBoxLayout,QVBoxLayout,QLayout
from PyQt5.QtGui import QPixmap,QImage
#%%
 
class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 1.0
        self.image = None
        self.initUI()  
    def initUI(self):
        self.readImgBtn = QPushButton('ReadImg')
        self.readImgBtn.setMaximumSize(500,30)
        self.showImgLabel = QLabel('image')
        self.showImgLabel.setAlignment(Qt.AlignCenter)
        self.showImgLabel.setMouseTracking(True)
        self.showImgLabel.setFixedSize(640,480)
        
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.readImgBtn)
        self.leftLayout.setSpacing(6)
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.showImgLabel)
        #self.rightLayout.setSpacing(6)
        self.rightLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.setStretchFactor(self.leftLayout,1)
        self.mainLayout.setStretchFactor(self.rightLayout,5)
        self.mainLayout.setSpacing(6)
        
        self.sizeWin = self.size()
        self.readImgBtn.clicked.connect(self.readImage)

    def resizeEvent(self,event): 
        sizeold=self.sizeWin
        #self.sizeWin = self.size()
        #sizedif = self.sizeWin-sizeold
        #self.showImgLabel.setFixedSize(640,480)
        #self.showImgLabel.resize(640+sizedif[0],480+sizedif[1])
    def wheelEvent(self,event):
        delta = event.angleDelta()
        numDegress = delta.y()/8
        if numDegress > 0:
            self.scale *= 1.2
        else:
            self.scale /= 1.2
        self.showImage()
    def showImage(self):
        h,w,c = self.image.shape
        scaleMat = cv2.resize(self.image,(int(self.scale*w),int(self.scale*h)),interpolation = cv2.INTER_AREA)
        h,w,c = scaleMat.shape
        bytesPerLine = c * w
        self.qimage=QImage(scaleMat.data,w,h,bytesPerLine,QImage.Format_RGB888)
        self.showImgLabel.setPixmap(QPixmap.fromImage(self.qimage))
    def readImage(self):
        self.image=cv2.imread('E:/wsd/index.jpg')
        cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB,self.image)
        height, width, bytesPerComponent = self.image.shape
        bytesPerLine = bytesPerComponent * width
        self.qimage = QImage(self.image.data,width,height,bytesPerLine,QImage.Format_RGB888)
        self.showImgLabel.setPixmap(QPixmap.fromImage(self.qimage))
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
