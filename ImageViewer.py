# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:19:19 2017

@author: WSD
"""
import sys
import cv2
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,QHBoxLayout,QVBoxLayout,
                             QLayout,QScrollArea,QGraphicsScene,QGraphicsView,QGraphicsPixmapItem)
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
        self.readImgBtn.setMaximumSize(200,30)
        
        self.leftLayout = QVBoxLayout()
        self.leftLayout.addWidget(self.readImgBtn)
        self.leftLayout.setSpacing(6)
        
        self.rightLayout = QVBoxLayout()
        self.sence = QGraphicsScene()
        self.view = QGraphicsView(self.sence,self)
        self.view.setMinimumSize(640,480)
        #self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.rightLayout.addWidget(self.view)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.setStretchFactor(self.leftLayout,1)
        self.mainLayout.setStretchFactor(self.rightLayout,5)
        self.mainLayout.setSpacing(6)
        
        self.readImgBtn.clicked.connect(self.readImage)

    def wheelEvent(self,event):
        delta = event.angleDelta()
        numDegress = delta.y()/8
        print(event.pos(),self.item.x())
        if numDegress > 0:
            self.scale = 1.2
        else:
            self.scale = 1/1.2
        self.view.scale(self.scale,self.scale)
    def readImage(self):
        self.image=cv2.imread('E:/wsd/0000.bmp')
        cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB,self.image)
        height, width, bytesPerComponent = self.image.shape
        bytesPerLine = bytesPerComponent * width
        self.qimage = QImage(self.image.data,width,height,bytesPerLine,QImage.Format_RGB888)
        self.pixmap = QPixmap('E:/wsd/0000.bmp')
        self.item = QGraphicsPixmapItem(self.pixmap)
        #self.item = self.sence.addPixmap(self.pixmap)
        self.sence.addItem(self.item)
        self.item.setPos(0,0)
        #self.sence.addPixmap(QPixmap.fromImage(self.qimage))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ImageViewer()
    w.show()
    sys.exit(app.exec_())
