# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:19:19 2017

@author: WSD
"""
import sys
import cv2
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtCore import Qt,QPoint,QRect,QSize
from PyQt5.QtWidgets import QApplication,QWidget, QPushButton,QLabel,QGridLayout, QHBoxLayout,QVBoxLayout,QLayout,QScrollArea,QComboBox
from PyQt5.QtGui import QPixmap,QImage
#%%
 
class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 1.0
        self.image = None
        self.bMousePress = False
        self.bMouseDouble = False
        self.bDrawRect = False
        self.pressPos = None
        self.releasePos = None
        self.rectList = []
        self.imageCount = [0]*100
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        self.initUI()
    def initUI(self):
        self.readImgBtn = QPushButton('ReadImage')
        self.readImgBtn.setMaximumSize(500,30)
        
        self.showImgLabel = QLabel('image')
        self.showImgLabel.setMouseTracking(True)
        
        self.combox_label = QComboBox()
        self.combox_label.addItem('0')
        self.combox_label.addItem('1')
        self.combox_label.addItem('2')
        
        self.saveImgBtn = QPushButton(('SaveImage'))        
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.showImgLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.leftLayout = QHBoxLayout()
        self.leftLayout.addWidget(self.readImgBtn)
        self.leftLayout.addWidget(self.combox_label)
        self.leftLayout.addWidget(self.saveImgBtn)
        self.leftLayout.setSpacing(6)
        
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addWidget(self.scrollArea)
        self.rightLayout.setSizeConstraint(QLayout.SetFixedSize)
        
        self.mainLayout = QGridLayout(self)
        self.mainLayout.addLayout(self.leftLayout,0,0)
        self.mainLayout.addLayout(self.rightLayout,1,0)
        self.mainLayout.setSpacing(6)
        self.resize(640,480)
        self.readImgBtn.clicked.connect(self.readImage)
        self.saveImgBtn.clicked.connect(self.saveRoiImage)

    def wheelEvent(self,event):
        print(self.showImgLabel.geometry(),self.scrollArea.verticalScrollBar().value(),self.scrollArea.horizontalScrollBar().value())
        self.rectList.clear()
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
            #print(preSize,curSize,disX,disY)
            #print(self.showImgLabel.geometry().height(),self.scrollArea.verticalScrollBar().value())
            #print(self.showImgLabel.geometry().width(),self.scrollArea.horizontalScrollBar().value())
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() + disY)
            self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() + disX)
            print(self.showImgLabel.geometry(),self.scrollArea.verticalScrollBar().value(),self.scrollArea.horizontalScrollBar().value())
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
    def mouseDoubleClickEvent(self,event):
        x3 = event.x() - self.rightLayout.geometry().x() - self.showImgLabel.pos().x()
        y3 = event.y() - self.rightLayout.geometry().y() - self.showImgLabel.pos().y()
        for i in range(len(self.rectList)):
            label,x1,y1,x2,y2 = self.rectList[i]
            if x1<x3<x2 and y1<y3<y2:
                del self.rectList[i]
                break
        h,w,c = self.image.shape
        scaleMat = cv2.resize(self.image,(int(self.scale*w),int(self.scale*h)),interpolation = cv2.INTER_AREA)
        for i in range(len(self.rectList)):
            label,x1,y1,x2,y2 = self.rectList[i]
            cv2.rectangle(scaleMat,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(scaleMat,label,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
        h,w,c = scaleMat.shape
        bytesPerLine = c * w
        self.qimage=QImage(scaleMat.data,w,h,bytesPerLine,QImage.Format_RGB888)
        self.showImgLabel.resize(self.qimage.size())
        self.showImgLabel.setPixmap(QPixmap.fromImage(self.qimage))
    def mouseReleaseEvent(self,event):
        if self.bDrawRect:
            self.pressPos = QPoint(0,0)
            self.bMousePress = False
            self.bDrawRect = False
            label = self.combox_label.currentText()
            self.rectList.append([label,self.x1,self.y1,self.x2,self.y2])
            #print(self.x1,self.y1,self.x2,self.y2)
    def showImage(self):
        h,w,c = self.image.shape
        self.scaleMat = cv2.resize(self.image,(int(self.scale*w),int(self.scale*h)),interpolation = cv2.INTER_AREA)
        for i in range(len(self.rectList)):
            label,x1,y1,x2,y2 = self.rectList[i]
            cv2.rectangle(self.scaleMat,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(self.scaleMat,label,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
        if self.bDrawRect:
            self.x1 = self.pressPos.x() - self.rightLayout.geometry().x() - self.showImgLabel.pos().x()
            self.y1 = self.pressPos.y() - self.rightLayout.geometry().y() - self.showImgLabel.pos().y()
            self.x2 = self.releasePos.x() - self.rightLayout.geometry().x() - self.showImgLabel.pos().x()
            self.y2 = self.releasePos.y() - self.rightLayout.geometry().y() - self.showImgLabel.pos().y()
            #print(self.x1,self.y1,self.x2,self.y2)
            cv2.rectangle(self.scaleMat,(self.x1,self.y1),(self.x2,self.y2),(0,255,0),2)
            label = self.combox_label.currentText()
            cv2.putText(self.scaleMat,label,(self.x1,self.y1),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
        h,w,c = self.scaleMat.shape
        bytesPerLine = c * w
        self.qimage=QImage(self.scaleMat.data,w,h,bytesPerLine,QImage.Format_RGB888)
        self.showImgLabel.resize(self.qimage.size())
        self.showImgLabel.setPixmap(QPixmap.fromImage(self.qimage))
        
    def readImage(self):
        self.image=cv2.imread('E:/wsd/0000.bmp')
        cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB,self.image)
        self.showImage()
    def saveRoiImage(self):
        h,w,c = self.image.shape     #去除框边缘
        self.scaleMat = cv2.resize(self.image,(int(self.scale*w),int(self.scale*h)),interpolation = cv2.INTER_AREA)
        for i in range(len(self.rectList)):
            label,x1,y1,x2,y2 = self.rectList[i]
            roi = self.scaleMat[y1:y2,x1:x2]
            cv2.cvtColor(roi,cv2.COLOR_RGB2BGR,roi)
            label = int(label)
            name = '%.2d_%.4d.jpg'%(label,self.imageCount[label])
            cv2.imwrite(name,roi)
            self.imageCount[label] += 1
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
