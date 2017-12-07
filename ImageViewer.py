# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:19:19 2017

@author: WSD
"""
import sys
import cv2
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtCore import Qt,QPoint,QRect,QSize
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLabel,QHBoxLayout,QVBoxLayout,QLayout,QScrollArea
from PyQt5.QtGui import QPixmap,QImage
#%%
 
class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 1.0
        self.image = None
        self.bMousePress = False
        self.bDrawRect = False
        self.pressPos = None
        self.releasePos = None
        self.rectList = []
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        self.initUI()
    def initUI(self):
        self.readImgBtn = QPushButton('ReadImg')
        self.readImgBtn.setMaximumSize(500,30)
        
        self.showImgLabel = QLabel('image')
        #self.showImgLabel.setAlignment(Qt.AlignCenter)
        self.showImgLabel.setMouseTracking(True)
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.showImgLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.readImgBtn)
        self.leftLayout.setSpacing(6)
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.scrollArea)
        #self.rightLayout.setSpacing(6)
        self.rightLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.setStretchFactor(self.leftLayout,1)
        self.mainLayout.setStretchFactor(self.rightLayout,5)
        self.mainLayout.setSpacing(6)
        self.readImgBtn.clicked.connect(self.readImage)

    def wheelEvent(self,event):
        x = self.showImgLabel.geometry().x() + self.rightLayout.geometry().x()
        y = self.showImgLabel.geometry().y() + self.rightLayout.geometry().y()
        w,h = self.showImgLabel.geometry().width(),self.showImgLabel.geometry().height()
        qrect = QRect(QPoint(x,y),QSize(w,h))
        preSize = self.showImgLabel.size()
        if qrect.contains(event.pos()):
            delta = event.angleDelta()
            numDegress = delta.y()/8
            if numDegress > 0:
                self.scale *= 1.2
            else:
                self.scale /= 1.2
            self.showImage()
            curSize = self.showImgLabel.size()
            disX = int((curSize.width() - preSize.width())/2)
            disY = int((curSize.height() - preSize.height())/2)
            print(preSize,curSize,disX,disY)
            print(self.showImgLabel.geometry().height(),self.scrollArea.verticalScrollBar().value())
            print(self.showImgLabel.geometry().width(),self.scrollArea.horizontalScrollBar().value())
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() + disY)
            self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() + disX)
    def mouseMoveEvent(self,event):
        if self.bDrawRect:
            self.releasePos = event.pos()
            self.showImage()
        if not self.bMousePress:
            return
        curPt = event.pos()
        disX = self.pressPos.x() - curPt.x()
        disY = self.pressPos.y() - curPt.y()
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() + disY)
        self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() + disX)        
        self.pressPos = curPt
    def mousePressEvent(self,event):
        x = self.showImgLabel.geometry().x() + self.rightLayout.geometry().x()
        y = self.showImgLabel.geometry().y() + self.rightLayout.geometry().y()
        w,h = self.showImgLabel.geometry().width(),self.showImgLabel.geometry().height()
        qrect = QRect(QPoint(x,y),QSize(w,h))
        if qrect.contains(event.pos()) and Qt.LeftButton == event.buttons():
            self.bMousePress = True
            self.bDrawRect = False
            self.pressPos = event.pos()
        elif qrect.contains(event.pos()) and Qt.RightButton == event.button():
            self.bDrawRect = True
            self.bMousePress = False
            self.pressPos = event.pos()
        else:
            self.bMousePress = False
            self.bDrawRect = False
            
    def mouseReleaseEvent(self,event):
        self.bMousePress = False
        self.pressPos = QPoint(0,0)
        if self.bDrawRect:
            self.bDrawRect = False
            self.rectList.append([self.x1,self.y1,self.x2,self.y2])
            print(self.x1,self.y1,self.x2,self.y2)
    def showImage(self):
        h,w,c = self.image.shape
        scaleMat = cv2.resize(self.image,(int(self.scale*w),int(self.scale*h)),interpolation = cv2.INTER_AREA)
        if self.bDrawRect:
            if len(self.rectList) > 0:
                for i in range(len(self.rectList)):
                    x1,y1,x2,y2 = self.rectList[i]
                    cv2.rectangle(scaleMat,(x1,y1),(x2,y2),(0,255,0),2)
            self.x1 = self.pressPos.x() - self.rightLayout.geometry().x() - self.showImgLabel.pos().x()
            self.y1 = self.pressPos.y() - self.rightLayout.geometry().y() - self.showImgLabel.pos().y()
            self.x2 = self.releasePos.x() - self.rightLayout.geometry().x() - self.showImgLabel.pos().x()
            self.y2 = self.releasePos.y() - self.rightLayout.geometry().y() - self.showImgLabel.pos().y()
            #print(self.x1,self.y1,self.x2,self.y2)
            cv2.rectangle(scaleMat,(self.x1,self.y1),(self.x2,self.y2),(0,255,0),2)
        h,w,c = scaleMat.shape
        bytesPerLine = c * w
        self.qimage=QImage(scaleMat.data,w,h,bytesPerLine,QImage.Format_RGB888)
        self.showImgLabel.resize(self.qimage.size())
        self.showImgLabel.setPixmap(QPixmap.fromImage(self.qimage))
        
    def readImage(self):
        self.image=cv2.imread('E:/wsd/0000.bmp')
        cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB,self.image)
        self.showImage()
        
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
