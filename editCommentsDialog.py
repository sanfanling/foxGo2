#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: editCommentsDialog.py 


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os
from faceDict import faceDict



class editCommentsDialog(QDialog):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Edit comments")
        self.setWindowIcon(QIcon("res/pictures/logo.png"))
        self.faceBox = faceDisplay(self)
        
        mainLayout = QVBoxLayout(None)
        self.commentsBox = QTextEdit()
        
        buttonLayout = QHBoxLayout(None)
        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")
        self.faceButton = QPushButton("+Face")
        self.faceButton.setFocusPolicy(Qt.NoFocus)
        buttonLayout.addWidget(self.faceButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        
        mainLayout.addWidget(self.commentsBox)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)
        
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.faceButton.clicked.connect(self.hideShowBox)
    
    def sizeHint(self):
        return QSize(400, 500)
        
    def hideShowBox(self):
        if self.faceBox.isHidden():
            x = self.geometry().x()
            y = self.geometry().y() + self.height()
            self.faceBox.move(QPoint(x, y))
            self.faceBox.show()
        else:
            self.faceBox.close()
    

class faceDisplay(QScrollArea):
    
    def __init__(self, parent = None):
        super().__init__()
        self.setWindowFlags(Qt.Popup)
        self.parent = parent
        self.container = faceContainer(self)
        self.setWidget(self.container)
        self.setFixedSize(510, 250)
    
    def event(self, e):
        if QEvent.WindowDeactivate == e.type():
            self.close()
        return QWidget.event(self, e)
        

class faceContainer(QWidget):
    
    def __init__(self, parent = None):
        super().__init__()
        mainLayout = QGridLayout(None)
        faceList = list(faceDict.values())
        ind = 0
        while ind <= len(faceDict) - 1:
            gifPath = os.path.join("res/face", faceList[ind])
            row, col = divmod(ind, 14)
            gl = gifLabel(gifPath, parent)
            mainLayout.addWidget(gl, row, col, Qt.AlignHCenter)
            ind += 1
        self.setLayout(mainLayout)
    
    
            
class gifLabel(QLabel):
    
    def __init__(self, gif, parent = None):
        super().__init__()
        self.gif = gif
        self.parent = parent
        self.movie = QMovie(gif)
        self.setMovie(self.movie)
        self.movie.jumpToNextFrame()
        
    def enterEvent(self, e):
        self.movie.start()
    
    def leaveEvent(self, e):
        self.movie.stop()
        
    def mousePressEvent(self, e):
        text = "<img src='{}'/>".format(self.gif)
        self.parent.parent.commentsBox.insertHtml(text)
        self.parent.hide()
        
if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = editCommentsDialog(None)
	w.show()
	sys.exit(app.exec_())
