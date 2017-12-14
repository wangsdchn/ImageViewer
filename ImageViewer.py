# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:19:19 2017

@author: WSD
"""
import sys
import os
import cv2
import numpy as np
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtCore import Qt,QPoint,QRect,QSize
from PyQt5.QtWidgets import (QApplication,QWidget, QPushButton,QLabel,QGridLayout, QHBoxLayout,QVBoxLayout,QLayout,
                             QScrollArea,QComboBox,QFileDialog,QLineEdit)
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
        self.imageVec = []
        self.imageVecIter = 0
        self.bCtrlPress = False
        self.x1 = self.y1 = self.x2 = self.y2 = 0
        self.initUI()
    def initUI(self):
        self.readImgBtn = QPushButton('SelectImage')
        self.readImgBtn.setMaximumSize(500,30)
        self.imgPath = QLineEdit()
        self.savePathBtn = QPushButton(('SelectPath'))
        self.savePath = QLineEdit()
        
        self.TopLayout = QHBoxLayout()
        self.TopLayout.addWidget(self.readImgBtn)
        self.TopLayout.addWidget(self.imgPath)
        self.TopLayout.addWidget(self.savePathBtn)
        self.TopLayout.addWidget(self.savePath)
        
        self.showImgLabel = QLabel('image')        
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.showImgLabel)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.MidLayout = QVBoxLayout()
        self.MidLayout.addWidget(self.scrollArea)
        self.MidLayout.setSizeConstraint(QLayout.SetFixedSize)
        
        self.nextBtn = QPushButton('Next')
        self.lastBtn = QPushButton('Last')
        self.combox_label = QComboBox()
        self.combox_label.addItem('0')
        self.combox_label.addItem('1')
        self.combox_label.addItem('2')
        self.saveImgBtn = QPushButton(('SaveImage'))
        
        self.BottomLayout = QHBoxLayout()
        self.BottomLayout.addWidget(self.lastBtn)
        self.BottomLayout.addWidget(self.nextBtn)
        self.BottomLayout.addWidget(self.combox_label)
        self.BottomLayout.addWidget(self.saveImgBtn)
        
        self.mainLayout = QGridLayout(self)
        self.mainLayout.addLayout(self.TopLayout,0,0)
        self.mainLayout.addLayout(self.MidLayout,1,0)
        self.mainLayout.addLayout(self.BottomLayout,2,0)
        self.mainLayout.setSpacing(6)
        self.resize(640,480)
        self.readImgBtn.clicked.connect(self.openAnImage)
        self.saveImgBtn.clicked.connect(self.saveRoiImage)
        self.nextBtn.clicked.connect(self.nextImage)
        self.lastBtn.clicked.connect(self.LastImage)
        self.savePathBtn.clicked.connect(self.openAFolder)

    def keyPressEvent(self,event):
        if event.key() == Qt.Key_Control:
            self.bCtrlPress = True
    def keyReleaseEvent(self,event):
        self.bCtrlPress = False
    def wheelEvent(self,event):
        if not self.bCtrlPress:
            return
        self.rectList.clear()
        x = self.showImgLabel.geometry().x() + self.MidLayout.geometry().x()
        y = self.showImgLabel.geometry().y() + self.MidLayout.geometry().y()
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
            #self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() + disY)
            #self.scrollArea.horizontalScrollBar().setValue(self.scrollArea.horizontalScrollBar().value() + disX)
            #print(self.showImgLabel.geometry(),self.scrollArea.verticalScrollBar().value(),self.scrollArea.horizontalScrollBar().value())
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
        x = self.showImgLabel.geometry().x() + self.MidLayout.geometry().x()
        y = self.showImgLabel.geometry().y() + self.MidLayout.geometry().y()
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
        x3 = event.x() - self.MidLayout.geometry().x() - self.showImgLabel.pos().x()
        y3 = event.y() - self.MidLayout.geometry().y() - self.showImgLabel.pos().y()
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
            if self.x1 < self.x2 - 5 and self.y1 < self.y2 - 5:
                self.rectList.append([label,self.x1,self.y1,self.x2,self.y2])
            #print(self.x1,self.y1,self.x2,self.y2)
    def showImage(self):
        name = self.imageVec[self.imageVecIter]
        n = name.rfind('/')
        name = name[n+1:]
        h,w,c = self.image.shape
        cv2.putText(self.image,name,(10,25),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
        self.scaleMat = cv2.resize(self.image,(int(self.scale*w),int(self.scale*h)),interpolation = cv2.INTER_AREA)
        
        for i in range(len(self.rectList)):
            label,x1,y1,x2,y2 = self.rectList[i]
            cv2.rectangle(self.scaleMat,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(self.scaleMat,label,(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
        if self.bDrawRect:
            self.x1 = self.pressPos.x() - self.MidLayout.geometry().x() - self.showImgLabel.pos().x()
            self.y1 = self.pressPos.y() - self.MidLayout.geometry().y() - self.showImgLabel.pos().y()
            self.x2 = self.releasePos.x() - self.MidLayout.geometry().x() - self.showImgLabel.pos().x()
            self.y2 = self.releasePos.y() - self.MidLayout.geometry().y() - self.showImgLabel.pos().y()
            #print(self.x1,self.y1,self.x2,self.y2)
            if self.x1 < self.x2 and self.y1 < self.y2:
                cv2.rectangle(self.scaleMat,(self.x1,self.y1),(self.x2,self.y2),(0,255,0),2)
                label = self.combox_label.currentText()
                cv2.putText(self.scaleMat,label,(self.x1,self.y1),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
        h,w,c = self.scaleMat.shape
        bytesPerLine = c * w
        self.qimage=QImage(self.scaleMat.data,w,h,bytesPerLine,QImage.Format_RGB888)
        self.showImgLabel.resize(self.qimage.size())
        self.showImgLabel.setPixmap(QPixmap.fromImage(self.qimage))
        
    def readImage(self,path=''):
        #self.image=cv2.imread(path)
        self.image = cv2.imdecode(np.fromfile(path,dtype=np.uint8),-1)
        if self.image.all():
            return
        cv2.cvtColor(self.image,cv2.COLOR_BGR2RGB,self.image)
        self.showImage()
    def saveRoiImage(self):
        if len(self.imageVec)==0:
            return
        h,w,c = self.image.shape     #去除框边缘
        scaleMat = cv2.resize(self.image,(int(self.scale*w),int(self.scale*h)),interpolation = cv2.INTER_AREA)
        cv2.cvtColor(scaleMat,cv2.COLOR_RGB2BGR,scaleMat)
        for i in range(len(self.rectList)):
            label,x1,y1,x2,y2 = self.rectList[i]
            roi = scaleMat[y1:y2,x1:x2]            
            label = int(label)
            name = self.savePath.text() + '%.2d_%.4d.jpg'%(label,self.imageCount[label])
            #cv2.imwrite(name,roi)
            cv2.imencode('.jpg',roi)[1].tofile(name)
            self.imageCount[label] += 1
    def openAFolder(self):
        path = QFileDialog.getExistingDirectory(self,'Select A Folder','D:/src')
        if path == '':
            return
        path += '/'
        self.savePath.setText(path)
        
        filelist = os.listdir(path)
        count = [0] * 100
        self.imageCount = [0] * 100
        for i in range(len(filelist)):
            if filelist[i][-4:] != '.jpg' or len(filelist[i]) != 11 or filelist[i][2] != '_':
                continue
            else:
                label = int(filelist[i][0:2])
                count[label] = int(filelist[i][3:7])
                if self.imageCount[label] <= count[label]:
                    self.imageCount[label] = count[label] + 1
    def openAnImage(self):
        self.imageVecIter = 0
        self.imageVec.clear()
        self.rectList.clear()
        file = QFileDialog.getOpenFileName(self,'Select An Image','D:/src','bmp files(*.bmp);;png files(*.png);;jpg files(*.jpg *jpeg)')
        if file == '':
            return
        n = file[0].rfind('/')
        path = file[0][:n]
        path += '/'
        self.imgPath.setText(path)
        n = file[0].rfind('.')
        imgtype = file[0][n+1:]
        filelist = os.listdir(path)
        k = 0
        for i in range(len(filelist)):
            if filelist[i][-3:] != imgtype:
                continue
            else:
                self.imageVec.append(path + filelist[i])
                k += 1
                if path + filelist[i] == file[0]:
                    self.imageVecIter = k - 1
        if len(self.imageVec) > 0:
            self.readImage(self.imageVec[self.imageVecIter])
    def nextImage(self):
        if len(self.imageVec)==0:
            return
        if self.imageVecIter == len(self.imageVec)-1:
            return
        else:
            self.imageVecIter += 1
        self.rectList.clear()
        self.readImage(self.imageVec[self.imageVecIter])
    def LastImage(self):
        if len(self.imageVec)==0:
            return
        if self.imageVecIter == 0:
            return
        else:
            self.imageVecIter -= 1
        self.rectList.clear()
        self.readImage(self.imageVec[self.imageVecIter])
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
