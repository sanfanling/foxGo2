#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: mainWindow.py  

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect, QSound
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from baseWindow import baseWindow
from sgfDataNew import sgfDataNew as sgfData
from settingData import settingData
import sys, os

class mainWindow(baseWindow):
    
    def __init__(self):
        super().__init__()
        
        
        self.settingData = settingData()
        self.settingData.getSettingData()
        self.withCoordinate.setChecked(self.settingData.withCoordinate)
        self.hideCursor.setChecked(self.settingData.hideCursor)
        self.backgroundMusic.setChecked(self.settingData.backgroundMusic)
        self.musicEquipment = QSound(self.settingData.musicPath)
        self.musicEquipment.setLoops(99)
        if self.settingData.backgroundMusic:
            self.musicEquipment.play()
        self.effectSounds.setChecked(self.settingData.effectSounds)
        self.effectEquipment = QSoundEffect()
        if self.settingData.boardStyle == "style1":
            self.boardStyle1.setChecked(True)
        elif self.settingData.boardStyle == "style2":
            self.boardStyle2.setChecked(True)
        else:
            self.boardNoStyle.setChecked(True)
        self.board.setBoardStyle(self.settingData.boardStyle)
        if self.settingData.stepsNumber == "current":
            self.stepsNumberCurrent.setChecked(True)
        elif self.settingData.stepsNumber == "all":
            self.stepsNumberAll.setChecked(True)
        else:
            self.stepsNumberHide.setChecked(True)
        if self.settingData.windowState != b"":
            self.restoreState(self.settingData.windowState)
        
        self.sgfData = sgfData()
        self.stepsListTmp = []  # it's a tmp list, storing the main steps data when entering test mode or variation from review mode
        self.startFreeMode()
        
        self.newGame.triggered.connect(self.startFreeMode)
        self.fileOpen.triggered.connect(self.fileOpen_)
        self.withCoordinate.toggled.connect(self.withCoordinate_)
        self.hideCursor.toggled.connect(self.hideCursor_)
        self.backgroundMusic.toggled.connect(self.backgroundMusic_)
        self.effectSounds.toggled.connect(self.effectSounds_)
        self.boardStyle1.triggered.connect(self.changeBoardStyle_)
        self.boardStyle2.triggered.connect(self.changeBoardStyle_)
        self.boardNoStyle.triggered.connect(self.changeBoardStyle_)
        self.stepsNumberAll.triggered.connect(self.changeStepsNumber_)
        self.stepsNumberCurrent.triggered.connect(self.changeStepsNumber_)
        self.stepsNumberHide.triggered.connect(self.changeStepsNumber_)
        self.quit.triggered.connect(self.close)
        
        
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
        self.backAction.triggered.connect(self.backAction_)
        self.controlDock.controlWidget.backButton.clicked.connect(self.backAction_)
    
    def startFreeMode(self):
        self.mode = "free"
        self.modeLabel.setText("Current mode: free")
        self.sgfData.init()
        self.thisGame.init()
        self.stepPoint = 0
        self.breakPoint = 0
        self.backAction.setEnabled(False)
        self.controlDock.controlWidget.backButton.setEnabled(False)
        self.resignAction.setEnabled(False)
        self.controlDock.controlWidget.resignAction.setEnabled(False)
        self.showStepsCount(True)
        self.displayGameInfo()
        self.moveOnBoard()
    
    def startReviewMode(self, sgf):
        self.sgfData.init()
        try:
            gameList = self.sgfData.checkSgf(sgf)
            if len(gameList) != 1:
                pass
        except:
            QMessageBox.critical(self, "Sfg file parse error", "It may be caused because of broken sfg file!")
            return
        else:
            self.sgfData.parseGame(0)
            self.mode = "review"
            self.modeLabel.setText("Current mode: review")
            self.thisGame.init()
            self.thisGame.getHaSteps(self.sgfData.haList)
            self.resignAction.setEnabled(False)
            self.controlDock.controlWidget.resignAction.setEnabled(False)
            self.stepPoint = len(self.sgfData.stepsList)
            self.breakPoint = 0
            self.controlDock.controlWidget.stepsCount.setRange(0, self.stepPoint)
            self.controlDock.controlWidget.stepsSlider.setRange(0, self.stepPoint)
            self.displayGameInfo()
            self.showStepsCount()
            self.moveOnBoard()
    
    def startTestMode(self, variation = []):
        self.mode = "test"
        self.modeLabel.setText("Current mode: test")
        self.breakPoint = self.stepPoint
        self.stepsListTmp = list(self.sgfData.stepsList)
        self.sgfData.stepsList = self.sgfData.stepsList[:self.stepPoint] + variation
        self.stepPoint += len(variation)
        self.backAction.setEnabled(True)
        self.controlDock.controlWidget.backButton.setEnabled(True)
        self.resignAction.setEnabled(False)
        self.controlDock.controlWidget.resignAction.setEnabled(False)
        self.moveOnBoard()
    
    def restartFreeAndTestMode(self):
        self.sgfData.stepsList = self.sgfData.stepsList[:self.stepPoint]
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
        else:
            self.stepPoint = self.breakPoint
        self.showStepsCount()
        self.moveOnBoard()
    
    def nextAction_(self):
        if self.stepPoint + 1 <= len(self.sgfData.stepsList):
            self.stepPoint += 1
        else:
            self.stepPoint = len(self.sgfData.stepsList)
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
    
    def gotoSpecifiedStep(self):
        self.stepPoint = self.controlDock.controlWidget.stepsCount.value() + self.breakPoint
        self.controlDock.controlWidget.stepsSlider.setValue(self.controlDock.controlWidget.stepsCount.value())
        self.moveOnBoard()
    
    def backAction_(self):
        self.mode = "review"
        self.modeLabel.setText("Current mode: Review")
        self.sgfData.stepsList = self.stepsListTmp
        self.stepPoint = self.breakPoint
        self.breakPoint = 0
        self.controlDock.controlWidget.stepsCount.setMaximum(len(self.sgfData.stepsList))
        self.controlDock.controlWidget.stepsSlider.setMaximum(len(self.sgfData.stepsList))
        self.showStepsCount()
        self.moveOnBoard()
        self.backAction.setEnabled(False)
        self.controlDock.controlWidget.backButton.setEnabled(False)
    
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
        moveSuccess = 0
        deadChessNum = 0
        for i, c, x, y in tmpList:
            self.thisGame.stepNum = i
            self.thisGame.goColor = c
            self.thisGame.x = x
            self.thisGame.y = y
            moveSuccess, deadChessNum = self.thisGame.makeStepSafe()
            self.thisGame.changeColor()
        self.board.update()
        self.makeSound(moveSuccess, deadChessNum)
        
        if self.mode == "review":
            com = self.sgfData.stepsMap[self.stepPoint - 1].comment
            if com != None:
                self.commentsDock.commentsDisplay.setPlainText(com)
            else:
                self.commentsDock.commentsDisplay.clear()
            
            #var = self.sgfData.stepsMap[self.stepPoint - 1].variations
            #if var != []:
                #self.commentBox.moveCursor(QTextCursor.End)
                #self.commentBox.insertHtml(self.formatVariation())
    
    def makeSound(self, moveSuccess, deadChessNum):
        if not self.settingData.effectSounds or moveSuccess == 0:
            return
        else:
            if moveSuccess == 1:
                soundFile = "res/sounds/112.wav"
            elif moveSuccess == 2:
                if deadChessNum == 1:
                    soundFile = "res/sounds/105.wav"
                elif 2 <= deadChessNum < 10:
                    soundFile = "res/sounds/104.wav"
                else:
                    soundFile = "res/sounds/103.wav"
        self.effectEquipment.setSource(QUrl.fromLocalFile(soundFile))
        self.effectEquipment.play()
        
    
    def fileOpen_(self):
        fileName, y= QFileDialog.getOpenFileName(None, "Open a SGF file", "./", "Go records file(*.sgf)")
        if fileName:
            with open(fileName) as f:
                self.startReviewMode(f.read())
    
    def withCoordinate_(self, b):
        self.settingData.withCoordinate = b
        self.board.update()
    
    def hideCursor_(self, b):
        self.settingData.hideCursor = b
    
    def backgroundMusic_(self, b):
        self.settingData.backgroundMusic = b
        if b:
            self.musicEquipment.play()
        else:
            self.musicEquipment.stop()
    
    def effectSounds_(self, b):
        self.settingData.effectSounds = b
    
    def changeBoardStyle_(self):
        style = self.sender().text().lower()
        if self.settingData.boardStyle != style:
            self.settingData.boardStyle = style
            self.board.setBoardStyle(style)
    
    def changeStepsNumber_(self):
        text = self.sender().text().lower()
        if self.settingData != text:
            self.settingData.stepsNumber = text
            self.board.update()
    
    def closeEvent(self, e):
        #os.remove(os.path.expanduser("~/.foxGo2/lock"))
        self.settingData.windowState = self.saveState()
        self.settingData.setSettingData()
        self.settingData.writeToFile()
        e.accept()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = mainWindow()
	w.show()
	sys.exit(app.exec_())
    
