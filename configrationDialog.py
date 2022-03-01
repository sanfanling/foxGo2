#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: configrationDialog.py  

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys, os


class configrationDialog(QDialog):
    
    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Configration")
        self.setWindowIcon(QIcon("res/pictures/logo.png"))
        mainLayout = QVBoxLayout(None)
        
        self.pathsBox = pathsBox(parent)
        self.optionsBox = optionsBox(parent)
        self.shortcutsBox = shortcutsBox(parent)
        
        buttonBox = QDialogButtonBox(self)
        cancelButton = QPushButton("Cancel")
        okButton = QPushButton("OK")
        buttonBox.addButton(cancelButton, QDialogButtonBox.RejectRole)
        buttonBox.addButton(okButton, QDialogButtonBox.AcceptRole)
        
        mainLayout.addWidget(self.pathsBox)
        mainLayout.addWidget(self.optionsBox)
        mainLayout.addWidget(self.shortcutsBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


class pathsBox(QGroupBox):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setTitle("Paths")
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
        d = QFileDialog.getExistingDirectory(None, "Choose a directory", os.path.expanduser(self.parent.settingData.sgfPath))
        self.sgfPath.setText(d)
    
    def changeMusic(self):
        f, y= QFileDialog.getOpenFileName(None, "Choose a media file", self.parent.settingData.musicPath, "WAV file(*.wav)")
        self.customMusic.setText(f)

class shortcutsBox(QGroupBox):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setTitle("Shortcuts")
        self.setAlignment(Qt.AlignHCenter)
                
        mainLayout = QFormLayout(None)
        self.previousToStart = QKeySequenceEdit(self.parent.settingData.previousToStart)
        self.previous10Steps = QKeySequenceEdit(self.parent.settingData.previous10Steps)
        self.previousStep = QKeySequenceEdit(self.parent.settingData.previousStep)
        self.nextStep = QKeySequenceEdit(self.parent.settingData.nextStep)
        self.next10Steps = QKeySequenceEdit(self.parent.settingData.next10Steps)
        self.nextToEnd = QKeySequenceEdit(self.parent.settingData.nextToEnd)
        self.back = QKeySequenceEdit(self.parent.settingData.back)
        mainLayout.addRow("Previous to start:", self.previousToStart)
        mainLayout.addRow("Previous 10 steps:", self.previous10Steps)
        mainLayout.addRow("Previous Step:", self.previousStep)
        mainLayout.addRow("Next step:", self.nextStep)
        mainLayout.addRow("Next 10 steps:", self.next10Steps)
        mainLayout.addRow("Next to end:", self.nextToEnd)
        mainLayout.addRow("Back:", self.back)
        
        self.setLayout(mainLayout)

class optionsBox(QGroupBox):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setTitle("Options")
        self.setAlignment(Qt.AlignHCenter)
        
        mainLayout = QVBoxLayout(None)
        self.autoSkip = QCheckBox("Auto skip when sgf file exists")
        self.acceptDragDrop = QCheckBox("Accept drag & drop sgf file")
        intervalLayout = QFormLayout(None)
        self.intervalSpinBox = QSpinBox(None)
        self.intervalSpinBox.setMinimum(1)
        self.intervalSpinBox.setMaximum(10)
        intervalLayout.addRow("Auto-review interval (seconds):", self.intervalSpinBox)
        mainLayout.addWidget(self.autoSkip)
        mainLayout.addWidget(self.acceptDragDrop)
        mainLayout.addLayout(intervalLayout)
        self.setLayout(mainLayout) 
