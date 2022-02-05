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
    
    def startFreeMode(self):
        self.mode = "free"
        self.modeLabel.setText("Current mode: free")
        self.sgfData.init()
        self.thisGame.init()
        self.stepPoint = 0
        self.breakPoint = 0
        self.displayGameInfo()
        self.reviewMove()
    
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
            self.controlDock.controlWidget.stepsCount.setRange(0, self.stepPoint)
            self.controlDock.controlWidget.stepsSlider.setRange(0, self.stepPoint)
            self.displayGameInfo()
            self.reviewMove()
    
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
    
    def reviewMove(self):
        self.thisGame.stepsGoDict.update(self.thisGame.haDict)
        for i, c, x, y in self.sgfData.stepsList:
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
    
