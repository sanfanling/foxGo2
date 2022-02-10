#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: mainWindow.py  

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os


class configrationDialog(QDialog):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Configration")
        self.setWindowIcon(QIcon("res/pictures/logo.png"))
        mainLayout = QVBoxLayout(None)
        
        self.pathBox = pathBox(self)
        self.optionBox = optionBox(self)
        
        buttonBox = QDialogButtonBox(self)
        cancelButton = QPushButton("Cancel")
        okButton = QPushButton("OK")
        buttonBox.addButton(cancelButton, QDialogButtonBox.RejectRole)
        buttonBox.addButton(okButton, QDialogButtonBox.AcceptRole)
        
        mainLayout.addWidget(self.pathBox)
        mainLayout.addWidget(self.optionBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class pathBox(QGroupBox):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setTitle("Path")
        self.setAlignment(Qt.AlignHCenter)
        
        mainLayout = QGridLayout(None)
        self.sgfPathLabel = QLabel("Default sgf path:")
        self.sgfPath = QLineEdit()
        self.sgfPath.setReadOnly(True)
        self.sgfPathButton = QPushButton("...")
        self.sgfPathButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        mainLayout.addWidget(self.sgfPathLabel, 0, 0)
        mainLayout.addWidget(self.sgfPath, 0, 1)
        mainLayout.addWidget(self.sgfPathButton, 0, 2)
        self.customMusicLabel = QLabel("Custom BGM:")
        self.customMusic = QLineEdit()
        self.customMusic.setReadOnly(True)
        self.customMusicButton = QPushButton("...")
        self.customMusicButton.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        mainLayout.addWidget(self.customMusicLabel, 1, 0)
        mainLayout.addWidget(self.customMusic, 1, 1)
        mainLayout.addWidget(self.customMusicButton, 1, 2)
        self.setLayout(mainLayout)
        
        self.sgfPathButton.clicked.connect(self.changeSgfPath)
        self.customMusicButton.clicked.connect(self.changeMusic)
        
    def changeSgfPath(self):
        d = QFileDialog.getExistingDirectory(None, "Choose a directory", os.path.expanduser(self.parent.parent.settingData.sgfPath))
        self.sgfPath.setText(d)
    
    def changeMusic(self):
        f, y= QFileDialog.getOpenFileName(None, "Choose a media file", self.parent.parent.settingData.musicPath, "WAV file(*.wav)")
        self.customMusic.setText(f)

class optionBox(QGroupBox):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setTitle("Option")
        self.setAlignment(Qt.AlignHCenter)
        
        mainLayout = QVBoxLayout(None)
        self.autoSkip = QCheckBox("Auto skip when sgf file exists")
        mainLayout.addWidget(self.autoSkip)
        self.setLayout(mainLayout)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = configrationDialog()
	w.show()
	sys.exit(app.exec_())
