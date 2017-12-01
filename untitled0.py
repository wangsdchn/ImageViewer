# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:19:19 2017

@author: WSD
"""

import sys
 
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton,QGridLayout,QLabel
from PyQt5.QtGui import QPixmap
#%%
 
class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.scale = 1.0
        self.initUI()  
    def initUI(self):
        self.resize(640,480)
        self.setWindowTitle('ImageViewer')
        self.readImgBtn = QPushButton('ReadImg', self)
        self.showImgLabel = QLabel('image')
        self.showImgLabel.setFixedSize(800,600)
        self.showImgLabel.setAlignment(Qt.AlignCenter)
        self.showImgLabel.setMouseTracking(True)
        
        self.image = QPixmap('E:/wsd/index.jpg')
        self.showImgLabel.setPixmap(self.image)
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.readImgBtn,0,0)
        mainLayout.addWidget(self.showImgLabel,0,1)
        
        #readImgBtn.clicked.connect(self.showImage)
    def wheelEvent(self,event):
        delta = event.angleDelta()
        numDegress = delta.y()/8
        if numDegress > 0:
            self.scale *= 1.2
        else:
            self.scale /= 1.2
        self.showImage()
        #event.accept()
    def showImage(self):
        self.showImgLabel.setPixmap(self.image.scaled(800*self.scale,600*self.scale,Qt.KeepAspectRatio))
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