#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: mainWindow.py  

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from baseWindow import baseWindow
from sgfData import sgfData
import sys, os

class mainWindow(baseWindow):
    
    def __init__(self):
        super().__init__()
        
        self.sgfData = sgfData()
        self.startFreeMode()
        
        self.newGame.triggered.connect(self.startFreeMode)
        self.fileOpen.triggered.connect(self.fileOpen_)
        
        self.toStartAction.triggered.connect(self.toStartAction_)
        self.controlDock.controlWidget.toStartButton.clicked.connect(self.toStartAction_)
        self.fastPrevAction.triggered.connect(self.fastPrevAction_)
        self.controlDock.controlWidget.fastPrevButton.clicked.connect(self.fastPrevAction_)
        self.prevAction.triggered.connect(self.prevAction_)
        self.controlDock.controlWidget.prevButton.clicked.connect(self.prevAction_)
        self.nextAction.triggered.connect(self.nextAction_)
        self.controlDock.controlWidget.nextButton.clicked.connect(self.nextAction_)
        self.fastNextAction.triggered.connect(self.fastNextAction_)
        self.controlDock.controlWidget.fastNextButton.clicked.connect(self.fastNextAction_)
        self.toEndAction.triggered.connect(self.toEndAction_)
        self.controlDock.controlWidget.toEndButton.clicked.connect(self.toEndAction_)
    
    def startFreeMode(self):
        self.mode = "free"
        self.modeLabel.setText("Current mode: free")
        self.sgfData.init()
        self.thisGame.init()
        self.stepPoint = 0
        self.breakPoint = 0
        self.displayGameInfo()
        self.moveOnBoard()
    
    def startReviewMode(self, sgf):
        self.sgfData.init()
        try:
            self.sgfData.parse(sgf)
        except:
            QMessageBox.critical(self, "Sfg file parse error", "It may be caused because of broken sfg file!")
            return
        else:
            self.mode = "review"
            self.modeLabel.setText("Current mode: review")
            self.sgfData.getStepsData(self.sgfData.rest) # now self.sgfData.stepsList and self.sgfData.haList are available
            self.thisGame.init()
            self.thisGame.getHaSteps(self.sgfData.haList)
            self.resignAction.setEnabled(False)
            self.stepPoint = len(self.sgfData.stepsList)
            self.breakPoint = 0
            self.controlDock.controlWidget.stepsCount.setRange(0, self.stepPoint)
            self.controlDock.controlWidget.stepsSlider.setRange(0, self.stepPoint)
            self.displayGameInfo()
            self.showStepsCount()
            self.moveOnBoard()
    
    def toStartAction_(self):
        self.stepPoint = self.breakPoint
        self.showStepsCount()
        self.moveOnBoard()
    
    def fastPrevAction_(self):
        if self.stepPoint - 10 >= self.breakPoint:
               self.stepPoint -= 10
        else:
            self.stepPoint = self.breakPoint
        self.showStepsCount()
        self.moveOnBoard()
    
    def prevAction_(self):
        if self.stepPoint - 1 >= self.breakPoint:
            self.stepPoint -= 1
            self.showStepsCount()
            self.moveOnBoard()
    
    def nextAction_(self):
        if self.stepPoint + 1 <= len(self.sgfData.stepsList):
            self.stepPoint += 1
            self.showStepsCount()
            self.moveOnBoard()

    def fastNextAction_(self):
        if self.stepPoint + 10 < len(self.sgfData.stepsList):
            self.stepPoint += 10
        else:
            self.stepPoint = len(self.sgfData.stepsList)
        self.showStepsCount()
        self.moveOnBoard()
    
    def toEndAction_(self):
        self.stepPoint = len(self.sgfData.stepsList)
        self.showStepsCount()
        self.moveOnBoard()
    
    def showStepsCount(self, setMaximum = False):
        if setMaximum:
            self.controlDock.controlWidget.stepsCount.setMaximum(self.stepPoint - self.breakPoint)
            self.controlDock.controlWidget.stepsSlider.setMaximum(self.stepPoint - self.breakPoint)
        self.controlDock.controlWidget.stepsCount.setValue(self.stepPoint - self.breakPoint)
        self.controlDock.controlWidget.stepsSlider.setValue(self.stepPoint - self.breakPoint)
    
    def displayGameInfo(self):
        self.infoDock.infoDisplay.gameLabel.setText(self.sgfData.title)
        self.infoDock.infoDisplay.blackPlayer.setText("{} {}".format(self.sgfData.blackPlayer, self.sgfData.blackPlayerLevel))
        self.infoDock.infoDisplay.whitePlayer.setText("{} {}".format(self.sgfData.whitePlayer, self.sgfData.whitePlayerLevel))
        self.infoDock.infoDisplay.haValue.setText(self.sgfData.ha)
        self.infoDock.infoDisplay.komiValue.setText(self.sgfData.komi)
        self.infoDock.infoDisplay.ruleValue.setText(self.sgfData.rule)
        self.infoDock.infoDisplay.dateValue.setText(self.sgfData.date)
        self.infoDock.infoDisplay.resultValue.setText(self.sgfData.result)
        self.infoDock.infoDisplay.timeLimitValue.setText(self.sgfData.timeLimit)
    
    def moveOnBoard(self):
        self.thisGame.stepsGoDict.clear()
        self.thisGame.stepsGoDict.update(self.thisGame.haDict)
        tmpList = self.sgfData.stepsList[:self.stepPoint]
        for i, c, x, y in tmpList:
            self.thisGame.stepNum = i
            self.thisGame.goColor = c
            self.thisGame.x = x
            self.thisGame.y = y
            moveSuccess, deadChessNum = self.thisGame.makeStepSafe()
        self.board.update()
        if self.mode == "review":
            self.thisGame.changeColor()
    
    def fileOpen_(self):
        fileName, y= QFileDialog.getOpenFileName(None, "Open a SGF file", "./", "Go records file(*.sgf)")
        if fileName:
            with open(fileName) as f:
                self.startReviewMode(f.read())



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = mainWindow()
	w.show()
	sys.exit(app.exec_())
    
