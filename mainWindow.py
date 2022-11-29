#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: mainWindow.py  

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect, QSound
from baseWindow import baseWindow
from sgfData import *
from faceDict import faceDict
from goEngine import go
from otherDialog import *
from configrationDialog import configrationDialog
from getHeaderThread import getHeaderThread

import sys, os, re, time

class mainWindow(baseWindow):
    
    def __init__(self):
        super().__init__()
        self.thisGame = go(self)
        self.thisGame.init(self.settingData.boardSize)
        
        eval("self.size{}.setChecked(True)".format(self.settingData.boardSize))
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
        try:
            self.restoreState(self.settingData.windowState)
        except:
            pass
        try:
            self.restoreGeometry(self.settingData.windowGeometry)
        except:
            pass
        
        self.intervalTimer = QTimer()
        self.intervalTimer.setInterval(self.settingData.autoReviewInterval * 1000)
        
        self.sgfData = sgfData()
        self.stepsListTmp = []  # it's a tmp list, storing the main steps data when entering test mode or variation from review mode
        self.startFreeMode()
        
        self.getkHeader = getHeaderThread()
        
        self.getkHeader.missionDone.connect(self.displayHeader)
        self.fastNewGame.triggered.connect(self.startFreeMode)
        self.newGame.triggered.connect(self.newGame_)
        self.fileOpen.triggered.connect(self.fileOpen_)
        self.saveAsAction.triggered.connect(self.saveAsAction_)
        self.withCoordinate.toggled.connect(self.withCoordinate_)
        self.hideCursor.toggled.connect(self.hideCursor_)
        self.backgroundMusic.toggled.connect(self.backgroundMusic_)
        self.effectSounds.toggled.connect(self.effectSounds_)
        self.boardStyle1.triggered.connect(self.changeBoardStyle_)
        self.boardStyle2.triggered.connect(self.changeBoardStyle_)
        self.size9.triggered.connect(self.size9_)
        self.size13.triggered.connect(self.size13_)
        self.size19.triggered.connect(self.size19_)
        self.boardNoStyle.triggered.connect(self.changeBoardStyle_)
        self.stepsNumberAll.triggered.connect(self.changeStepsNumber_)
        self.stepsNumberCurrent.triggered.connect(self.changeStepsNumber_)
        self.stepsNumberHide.triggered.connect(self.changeStepsNumber_)
        self.settingAction.triggered.connect(self.settingAction_)
        self.intervalTimer.timeout.connect(self.intervalTimer_)
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
        self.autoReviewAction.toggled.connect(self.autoReviewAction_)
        self.controlDock.controlWidget.autoReviewAction.toggled.connect(self.autoReviewAction_)
        self.passAction.triggered.connect(self.thisGame.makeStepPass)
        self.controlDock.controlWidget.passAction.triggered.connect(self.thisGame.makeStepPass)
    
    def startFreeMode(self):
        if self.intervalTimer.isActive():
            self.intervalTimer.stop()
            self.autoReviewAction.setChecked(False)
            self.controlDock.controlWidget.autoReviewAction.setChecked(False)
        self.mode = "free"
        self.modeLabel.setText("Current mode: free")
        self.sgfData.init()
        self.thisGame.init(self.settingData.boardSize)
        self.stepPoint = 0
        self.breakPoint = 0
        self.saveAsAction.setEnabled(True)
        self.backAction.setEnabled(False)
        self.controlDock.controlWidget.backButton.setEnabled(False)
        self.resignAction.setEnabled(False)
        self.controlDock.controlWidget.resignAction.setEnabled(False)
        self.autoReviewAction.setEnabled(False)
        self.controlDock.controlWidget.autoReviewAction.setEnabled(False)
        self.showStepsCount(True)
        self.displayGameInfo("freeMode")
        self.moveOnBoard()
    
    def startReviewMode(self, sgf):
        if self.intervalTimer.isActive():
            self.intervalTimer.stop()
            self.autoReviewAction.setChecked(False)
            self.controlDock.controlWidget.autoReviewAction.setChecked(False)
        self.sgfData.init()
        try:
            gameList = self.sgfData.checkSgf(sgf)
        except:
            QMessageBox.critical(self, "Sfg file parse error", "It may be caused because of broken sfg file!")
            return
        else:
            if len(gameList) != 1:
                item, ok = QInputDialog.getItem(None, "Choose a game in this sgf file", "Game:", gameList, 0, False)
                if ok:
                    ind = gameList.index(item)
                else:
                    self.startFreeMode()
                    return
            else:
                ind = 0
            
            self.sgfData.parseGame(ind)
            self.mode = "review"
            self.modeLabel.setText("Current mode: review")
            if self.settingData.boardSize != self.sgfData.size:
                eval("self.size{}.setChecked(True)".format(self.sgfData.size))
                self.changeBoardSize_(self.sgfData.size)
            self.thisGame.init(self.settingData.boardSize)
            self.thisGame.getHaSteps(self.sgfData.haList)
            self.saveAsAction.setEnabled(True)
            self.resignAction.setEnabled(False)
            self.controlDock.controlWidget.resignAction.setEnabled(False)
            self.autoReviewAction.setEnabled(True)
            self.controlDock.controlWidget.autoReviewAction.setEnabled(True)
            self.stepPoint = len(self.sgfData.stepsList)
            self.breakPoint = 0
            self.controlDock.controlWidget.stepsCount.setRange(0, self.stepPoint)
            self.controlDock.controlWidget.stepsSlider.setRange(0, self.stepPoint)
            self.displayGameInfo("reviewMode")
            self.showStepsCount()
            self.moveOnBoard()
    
    def startTestMode(self, variation = []):
        if self.intervalTimer.isActive():
            self.intervalTimer.stop()
            self.autoReviewAction.setChecked(False)
            self.controlDock.controlWidget.autoReviewAction.setChecked(False)
        self.mode = "test"
        self.modeLabel.setText("Current mode: test")
        self.breakPoint = self.stepPoint
        self.stepsListTmp = list(self.sgfData.stepsList)
        self.sgfData.stepsList = self.sgfData.stepsList[:self.stepPoint] + variation
        self.stepPoint += len(variation)
        self.saveAsAction.setEnabled(False)
        self.backAction.setEnabled(True)
        self.controlDock.controlWidget.backButton.setEnabled(True)
        self.resignAction.setEnabled(False)
        self.controlDock.controlWidget.resignAction.setEnabled(False)
        self.autoReviewAction.setEnabled(False)
        self.controlDock.controlWidget.autoReviewAction.setEnabled(False)
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
        self.commentsDock.commentsDisplay.commentsBox.clear()
        self.modeLabel.setText("Current mode: Review")
        self.sgfData.stepsList = self.stepsListTmp
        self.stepPoint = self.breakPoint
        self.breakPoint = 0
        self.controlDock.controlWidget.stepsCount.setMaximum(len(self.sgfData.stepsList))
        self.controlDock.controlWidget.stepsSlider.setMaximum(len(self.sgfData.stepsList))
        self.showStepsCount()
        self.moveOnBoard()
        self.backAction.setEnabled(False)
        self.saveAsAction.setEnabled(True)
        self.controlDock.controlWidget.backButton.setEnabled(False)
        self.autoReviewAction.setEnabled(True)
        self.controlDock.controlWidget.autoReviewAction.setEnabled(True)
    
    def autoReviewAction_(self, checked):
        self.autoReviewAction.setChecked(checked)
        self.controlDock.controlWidget.autoReviewAction.setChecked(checked)
        if not checked:
            self.intervalTimer.stop()
        else:
            self.toStartAction_()
            self.intervalTimer.start()
    
    def intervalTimer_(self):
        if self.stepPoint == len(self.sgfData.stepsList):
            self.intervalTimer.stop()
            self.autoReviewAction.setChecked(False)
            self.controlDock.controlWidget.autoReviewAction.setChecked(False)
        else:
            self.nextAction_()
    
    def showStepsCount(self, setMaximum = False):
        if setMaximum:
            self.controlDock.controlWidget.stepsCount.setMaximum(self.stepPoint - self.breakPoint)
            self.controlDock.controlWidget.stepsSlider.setMaximum(self.stepPoint - self.breakPoint)
        self.controlDock.controlWidget.stepsCount.setValue(self.stepPoint - self.breakPoint)
        self.controlDock.controlWidget.stepsSlider.setValue(self.stepPoint - self.breakPoint)
    
    def displayGameInfo(self, mode):
        self.infoDock.infoDisplay.gameLabel.setText(self.sgfData.title)
        self.infoDock.infoDisplay.blackPlayer.setText("{} {}".format(self.sgfData.blackPlayer, self.sgfData.blackPlayerLevel))
        self.infoDock.infoDisplay.whitePlayer.setText("{} {}".format(self.sgfData.whitePlayer, self.sgfData.whitePlayerLevel))
        self.infoDock.infoDisplay.haValue.setText(self.sgfData.ha)
        self.infoDock.infoDisplay.komiValue.setText(self.sgfData.komi)
        self.infoDock.infoDisplay.ruleValue.setText(self.sgfData.rule)
        self.infoDock.infoDisplay.dateValue.setText(self.sgfData.date)
        self.infoDock.infoDisplay.resultValue.setText(self.sgfData.result)
        self.infoDock.infoDisplay.timeLimitValue.setText(self.sgfData.timeLimit)
        self.displayHeader()
        if mode == "reviewMode":
            self.getkHeader.setArgs([self.sgfData.blackPlayer, self.sgfData.whitePlayer])
            self.getkHeader.start()
    
    def displayHeader(self):
        if os.path.exists(f"headers/{self.sgfData.blackPlayer}.jpg"):
            photoSheet = f"min-width: 100px; max-width: 100px; min-height: 100px; max-height: 100px; border-radius: 50px; border-width: 0 0 0 0; border-image: url(headers/{self.sgfData.blackPlayer}.jpg) 0 0 0 0 stretch strectch;"
        else:
            photoSheet = "min-width: 100px; max-width: 100px; min-height: 100px; max-height: 100px; border-radius: 50px; border-width: 0 0 0 0; border-image: url(headers/blank.png) 0 0 0 0 stretch strectch;"
        self.infoDock.infoDisplay.blackPhoto.setStyleSheet(photoSheet)
            
        if os.path.exists(f"headers/{self.sgfData.whitePlayer}.jpg"):
            photoSheet = f"min-width: 100px; max-width: 100px; min-height: 100px; max-height: 100px; border-radius: 50px; border-width: 0 0 0 0; border-image: url(headers/{self.sgfData.whitePlayer}.jpg) 0 0 0 0 stretch strectch;"
        else:
            photoSheet = "min-width: 100px; max-width: 100px; min-height: 100px; max-height: 100px; border-radius: 50px; border-width: 0 0 0 0; border-image: url(headers/blank.png) 0 0 0 0 stretch strectch;"
        self.infoDock.infoDisplay.whitePhoto.setStyleSheet(photoSheet)
        
    def moveOnBoard(self):
        self.thisGame.stepsGoDict.clear()
        self.thisGame.stepsGoDict.update(self.thisGame.haDict)
        tmpList = self.sgfData.stepsList[:self.stepPoint]
        moveSuccess = 0
        deadChessNum = 0
        if len(tmpList) != 0:
            for i in tmpList:
                self.thisGame.stepNum = i.getStepNum()
                self.thisGame.goColor = i.getColor()
                self.thisGame.x = i.getCoordinateX()
                self.thisGame.y = i.getCoordinateY()
                moveSuccess, deadChessNum = self.thisGame.makeStepSafe()
            self.thisGame.changeColor()
            self.makeSound(moveSuccess, deadChessNum)
        else:
            self.thisGame.goColor = "black"
        self.board.update()
        self.showComment()
    
    def setComment(self, co):
        self.sgfData.stepsList[self.stepPoint - 1].comment = co
    
    def showComment(self):
        self.commentsDock.commentsDisplay.commentsBox.clear()
        if self.mode == "review" and self.stepPoint != 0:
            com = self.sgfData.stepsList[self.stepPoint - 1].comment
            if com != "":
                com = com.replace("\n", "<br>")
                self.commentsDock.commentsDisplay.commentsBox.insertHtml(self.faceConvert(com))
            var = self.sgfData.stepsList[self.stepPoint - 1].variations
            if var != []:
                self.commentsDock.commentsDisplay.commentsBox.moveCursor(QTextCursor.End)
                self.commentsDock.commentsDisplay.commentsBox.insertHtml(self.formatVariation())
        
    def faceConvert(self, c):
        for i in faceDict:
            if i in c:
                c = c.replace(i, "<img src='res/face/{}'/>".format(faceDict[i]))
        return c
        
    
    def showVariation(self, link):
        self.commentsDock.commentsDisplay.commentsBox.clear()
        name = link.fileName().strip()
        point, num = name.split("-")
        point = int(point)
        num = int(num)
        l = self.sgfData.stepsList[point - 1].variations[num - 1]
        #vl = self.sgfData.parseStepsMap(l)
        self.startTestMode(l)
        self.showStepsCount(True)
    
    def formatVariation(self):
        p = 0
        text = "<br><br>"
        for i in self.sgfData.stepsList[self.stepPoint - 1].variations:
            p += 1
            co = i[0].getComment()
            url = "{}-{}".format(self.stepPoint, p)
            title = "Variation: {}: ".format(url)
            text += '<a href="{}">{}</a> {}<br>'.format(url, title, co)
            text = self.faceConvert(text)
        return text
    
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
        
        
        
    def newGame_(self):
        self.statusBar().showMessage("This function is not finished", 5000)
    
    def fileOpen_(self):
        fileName, y= QFileDialog.getOpenFileName(None, "Open a SGF file", self.settingData.sgfPath, "Go records file(*.sgf)")
        if fileName:
            with open(fileName, 'r', encoding = "utf8") as f:
                self.startReviewMode(f.read())
                
    def saveAsAction_(self):
        #t = re.sub(r'[\\/:*?"<>|\r\n]+', "_", self.sgfData.title)
        #f, filt= QFileDialog.getSaveFileName(None, "Save as", os.path.join(self.settingData.sgfPath, t), "Go records file(*.sgf)")
        #if f:
            #with open(f, "w", encoding = "utf8") as fi:
                #fi.write(self.sgfData.data)
            #self.sgfExplorerDock.sgfExplorerDisplay.showItems()
        #a = writeSgf("aa.sgf")
        #root = a.generateRoot()
        #rest = a.generateRest(self.sgfData.stepsList)
        #a.toFile(root + rest)
        
        dialog = rootDialog(self)
        if self.mode == "review":
            dialog.playerInfoBox.pbLine.setText(self.sgfData.blackPlayer)
            dialog.playerInfoBox.brLine.setText(self.sgfData.blackPlayerLevel)
            dialog.playerInfoBox.pwLine.setText(self.sgfData.whitePlayer)
            dialog.playerInfoBox.wrLine.setText(self.sgfData.whitePlayerLevel)
            dialog.gameInfoBox.gnLine.setText(self.sgfData.title)
            y, m, d = self.sgfData.date.split("-")
            dialog.gameInfoBox.dtLine.setDate(QDate(int(y), int(m), int(d)))
            dialog.gameInfoBox.kmLine.setText(str(int(float(self.sgfData.komi) * 100)))
            dialog.gameInfoBox.haLine.setValue(len(self.sgfData.haList))
            if self.sgfData.rule == "Chinese" or self.sgfData.rule == "Japanese" or self.sgfData.rule == "Ying's":
                dialog.gameInfoBox.ruLine.setCurrentText(self.sgfData.rule)
            else:
                dialog.gameInfoBox.ruLine.setCurrentText("Others")
            dialog.gameInfoBox.rsLine.setText(self.sgfData.result)
            dialog.gameInfoBox.tmLine.setText(self.sgfData.timeLimit)
            dialog.gameInfoBox.tcLine.setValue(int(self.sgfData.countTimes))
            dialog.gameInfoBox.ttLine.setText(self.sgfData.countSeconds)
        else:
            y, m, d = time.localtime()[0:3]
            dialog.gameInfoBox.dtLine.setDate(QDate(y, m, d))
            dialog.gameInfoBox.kmLine.setText("375")
            dialog.gameInfoBox.haLine.setValue(len(self.sgfData.haList))
            dialog.gameInfoBox.tmLine.setText("7200")
            dialog.gameInfoBox.tcLine.setValue(5)
            dialog.gameInfoBox.ttLine.setText("60")
        if dialog.exec_() == QDialog.Accepted:
            t = re.sub(r'[\\/:*?"<>|\r\n]+', "_", self.sgfData.title)
            f, filt= QFileDialog.getSaveFileName(None, "Save as", os.path.join(self.settingData.sgfPath, t), "Go records file(*.sgf)")
            if f:
                a = writeSgf(f)
                sz = self.settingData.boardSize
                gn = dialog.gameInfoBox.gnLine.text()
                dt = dialog.gameInfoBox.dtLine.date().toString("yyyy-MM-dd")
                pb = dialog.playerInfoBox.pbLine.text()
                pw = dialog.playerInfoBox.pwLine.text()
                br = dialog.playerInfoBox.brLine.text()
                wr = dialog.playerInfoBox.wrLine.text()
                km = dialog.gameInfoBox.kmLine.text()
                ha = dialog.gameInfoBox.haLine.value()
                ru = dialog.gameInfoBox.ruLine.currentText()
                rs = dialog.gameInfoBox.rsLine.text()
                tm = dialog.gameInfoBox.tmLine.text()
                tc = dialog.gameInfoBox.tcLine.value()
                tt = dialog.gameInfoBox.ttLine.text()
                
                root = a.generateRoot(sz, gn, dt, pb, pw, br, wr, km, ha, ru, rs, tm, tc, tt)
                rest = a.generateRest(self.sgfData.stepsList, self.sgfData.haList)
                a.toFile(root + rest)
                self.sgfExplorerDock.sgfExplorerDisplay.showItems()
        
                
    def size9_(self):
        self.changeBoardSize_(9)
        self.startFreeMode()
        
    def size13_(self):
        self.changeBoardSize_(13)
        self.startFreeMode()
        
    def size19_(self):
        self.changeBoardSize_(19)
        self.startFreeMode()
        
    def changeBoardSize_(self, s):
        self.settingData.boardSize = s
        self.board.setBoardSize(self.settingData.boardSize)
        
    
    def settingAction_(self):
        dialog = configrationDialog(self)
        dialog.pathsBox.sgfPath.setText(self.settingData.sgfPath)
        dialog.pathsBox.customMusic.setText(self.settingData.musicPath)
        dialog.optionsBox.autoSkip.setChecked(self.settingData.autoSkip)
        dialog.optionsBox.acceptDragDrop.setChecked(self.settingData.acceptDragDrop)
        dialog.optionsBox.intervalSpinBox.setValue(self.settingData.autoReviewInterval)
        if dialog.exec_() == QDialog.Accepted:
            self.settingData.sgfPath = dialog.pathsBox.sgfPath.text()
            self.sgfExplorerDock.sgfExplorerDisplay.syncPath()
            self.settingData.musicPath = dialog.pathsBox.customMusic.text()
            self.settingData.autoSkip = dialog.optionsBox.autoSkip.isChecked()
            self.settingData.acceptDragDrop = dialog.optionsBox.acceptDragDrop.isChecked()
            self.settingData.autoReviewInterval = dialog.optionsBox.intervalSpinBox.value()
            self.settingData.previousToStart = dialog.shortcutsBox.previousToStart.keySequence()
            self.settingData.previous10Steps = dialog.shortcutsBox.previous10Steps.keySequence()
            self.settingData.previousStep = dialog.shortcutsBox.previousStep.keySequence()
            self.settingData.nextStep = dialog.shortcutsBox.nextStep.keySequence()
            self.settingData.next10Steps = dialog.shortcutsBox.next10Steps.keySequence()
            self.settingData.nextToEnd = dialog.shortcutsBox.nextToEnd.keySequence()
            self.settingData.back = dialog.shortcutsBox.back.keySequence()
            self.setAllShortcuts()
            self.intervalTimer.setInterval(self.settingData.autoReviewInterval * 1000)
            self.setAcceptDrops(self.settingData.acceptDragDrop)
    
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
    
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F:
            self.controlDock.controlWidget.stepsCount.selectAll()
            self.controlDock.controlWidget.stepsCount.setFocus(Qt.ShortcutFocusReason)
    
    def dragEnterEvent(self, ev):
        urls = ev.mimeData().urls()
        if len(urls) == 1 and os.path.splitext(urls[0].toLocalFile())[1] == ".sgf":
            ev.acceptProposedAction()
    
    def dropEvent(self, ev):
        filename = ev.mimeData().urls()[0].toLocalFile()
        with open(filename, "r", encoding = "utf8") as f:
            sgf = f.read()
        self.startReviewMode(sgf)
    
    def closeEvent(self, e):
        #os.remove("./lock")
        self.settingData.windowState = self.saveState()
        self.settingData.windowGeometry = self.saveGeometry()
        self.settingData.infoDockGeometry = self.infoDock.saveGeometry()
        self.settingData.controlDockGeometry = self.controlDock.saveGeometry()
        self.settingData.consoleDockGeometry = self.consoleDock.saveGeometry()
        self.settingData.sgfExplorerDockGeometry = self.sgfExplorerDock.saveGeometry()
        self.settingData.recentGamesDockGeometry = self.recentGamesDock.saveGeometry()
        self.settingData.recentGamesDockTableState = self.recentGamesDock.recentGamesDisplay.table.horizontalHeader().saveState()
        self.settingData.saveIniFile()
        e.accept()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = mainWindow()
	w.show()
	sys.exit(app.exec_())
    
