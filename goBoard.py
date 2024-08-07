#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: goBoard.py

import os, sys, time
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from goEngine import go
from sgfData import step


class goBoard(QLabel):
    
    def __init__(self, parent = None, size = 19, stylePath = "./res/pictures/style2.png"):
        super().__init__()
        self.parent = parent
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setBoardSize(size)
        self.setSizePara(30)
        self.thinLine = 1
        self.thickLine = 3
        self.dotRadius = 3
        self.x = None
        self.y = None
        self.inBoard = False
        self.setMouseTracking(True)
        self.fontInfo = QFontMetrics(self.font())
        
    def setSizePara(self, cellSize = 25):
        self.cellSize = cellSize
        self.boardEdge = self.cellSize
        self.rectSize = self.cellSize // 2
        self.stonesize = int(self.cellSize * 0.9) // 2 * 2
        self.currentSignSize = int(self.stonesize * 0.3)
        self.update()
    
    def setBoardSize(self, s):
        self.boardSize = s
        l = min(self.parent.mainLayout.contentsRect().width(), self.parent.mainLayout.contentsRect().height())
        cellSize = l // (self.boardSize + 1)
        if cellSize < 25:
            self.setSizePara(25)
        else:
            self.setSizePara(cellSize)
        
    
    def setBoardStyle(self, style):
        if style == "none":
            self.setStyleSheet("")
        else:
            self.setStyleSheet("QLabel{background-image: url(res/pictures/%s.png)}" %style)
    
    def mouseMoveEvent(self, e):
        self.x = e.pos().x()
        self.y = e.pos().y()
        if self.boardEdge <= self.x <= self.boardEdge + self.cellSize * (self.boardSize - 1) and self.boardEdge <= self.y <= self.boardEdge + self.cellSize * (self.boardSize - 1):
            self.inBoard = True
            if self.parent.settingData.hideCursor:
                self.setCursor(QCursor(Qt.CursorShape.BlankCursor))
            self.update()
        else:
            self.inBoard = False
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.update()
    
    def mousePressEvent(self, e):
        px, py = self.boardToGo((self.x, self.y))
        hasStone = (px, py) in self.parent.thisGame.stepsGoDict
        if e.button() == Qt.MouseButton.LeftButton and self.parent.mode == "free" and self.inBoard and not hasStone:
            if self.parent.stepPoint != len(self.parent.sgfData.stepsList):
                self.parent.restartFreeAndTestMode()
            self.parent.thisGame.x, self.parent.thisGame.y = px, py
            moveSuccess, deadChessNum = self.parent.thisGame.makeStep()
            if moveSuccess:
                oneStep = step((self.parent.thisGame.x, self.parent.thisGame.y), self.parent.thisGame.goColor, self.parent.thisGame.stepNum)
                self.parent.sgfData.stepsList.append(oneStep)
                self.parent.thisGame.changeColor()
                self.parent.stepPoint += 1
                self.parent.showStepsCount(True)
                self.update()
                self.parent.makeSound(moveSuccess, deadChessNum)
        elif e.button() == Qt.MouseButton.LeftButton and self.parent.mode == "review" and self.inBoard and not hasStone:
            self.parent.startTestMode()
            self.parent.thisGame.stepNum = 0
            self.parent.thisGame.x, self.parent.thisGame.y = px, py
            moveSuccess, deadChessNum = self.parent.thisGame.makeStep()
            if moveSuccess:
                oneStep = step((self.parent.thisGame.x, self.parent.thisGame.y), self.parent.thisGame.goColor, self.parent.thisGame.stepNum)
                self.parent.sgfData.stepsList.append(oneStep)
                self.parent.thisGame.changeColor()
                self.parent.stepPoint += 1
                self.parent.showStepsCount(True)
                self.update()
                self.parent.makeSound(moveSuccess, deadChessNum)
        elif e.button() == Qt.MouseButton.LeftButton and self.parent.mode == "test" and self.inBoard and not hasStone:
            if self.parent.stepPoint != len(self.parent.sgfData.stepsList):
                self.parent.restartFreeAndTestMode()
            self.parent.thisGame.x, self.parent.thisGame.y = px, py
            moveSuccess, deadChessNum = self.parent.thisGame.makeStep()
            if moveSuccess:
                oneStep = step((self.parent.thisGame.x, self.parent.thisGame.y), self.parent.thisGame.goColor, self.parent.thisGame.stepNum)
                self.parent.sgfData.stepsList.append(oneStep)
                self.parent.thisGame.changeColor()
                self.parent.stepPoint += 1
                self.parent.showStepsCount(True)
                self.update()
                self.parent.makeSound(moveSuccess, deadChessNum)
        if e.button() == Qt.MouseButton.RightButton and self.inBoard:
            self.parent.thisGame.makeStepPass()
    
    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)
        self.__paintBoard(p)
        self.__paintMousePointRect(p)
        self.__paintSuccessedMoves(p)
        p.end()
    
    def __paintSuccessedMoves(self, p):
        if self.x != None and self.y != None and self.parent.thisGame.stepsGoDict != {}:
            for x, y in list(self.parent.thisGame.stepsGoDict.keys()):
                if self.parent.thisGame.stepsGoDict[(x, y)][0] == "black":
                    pix = QPixmap("res/pictures/blackStone.png").scaled(self.stonesize, self.stonesize, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    fontColor = Qt.GlobalColor.white
                else:
                    pix = QPixmap("res/pictures/whiteStone.png").scaled(self.stonesize, self.stonesize, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    fontColor = Qt.GlobalColor.black
                (x1, y1) = self.goToBoard((x, y))
                p.drawPixmap(x1 - self.stonesize // 2, y1 - self.stonesize // 2, pix)
            
                if self.parent.settingData.stepsNumber == "all":
                    count = self.parent.thisGame.stepsGoDict[(x, y)][1]
                    if count != 0 and self.checkClearCount((x, y)):
                        p.setPen(QPen(fontColor, 1))
                        font = p.font()
                        font.setPointSize(self.stonesize // 3)
                        p.setFont(font)
                        rect = QRect(x1 - self.stonesize // 2, y1 - self.stonesize // 2, self.stonesize // 2 * 2, self.stonesize // 2 * 2)
                        p.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(count))
            
            if self.parent.settingData.stepsNumber == "hide":
                p.setPen(QPen(fontColor, 1))
                p.setBrush(QBrush(fontColor))
                triangle = QPainterPath()
                triangle.moveTo(x1, y1)
                triangle.lineTo(x1, y1 + self.stonesize // 2)
                triangle.lineTo(x1 + self.stonesize // 2, y1)
                p.drawPath(triangle)
            elif self.parent.settingData.stepsNumber == "current":
                p.setPen(QPen(fontColor, 1))
                font = p.font()
                font.setPointSize(self.stonesize // 3)
                p.setFont(font)
                rect = QRect(x1 - self.stonesize // 2, y1 - self.stonesize // 2, self.stonesize // 2 * 2, self.stonesize // 2 * 2)
                p.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(self.parent.thisGame.stepsGoDict[(x, y)][1]))
            
    
    def __paintBoard(self, p):
        for i in range(self.boardSize):
            lineThickness = self.thickLine if i == 0 or i == self.boardSize - 1 else self.thinLine
            p.setPen(QPen(Qt.GlobalColor.black, lineThickness))
            p.drawLine(self.boardEdge, self.boardEdge + self.cellSize * i, self.boardEdge + self.cellSize * (self.boardSize - 1), self.boardEdge + self.cellSize * i,)
            p.drawLine(self.boardEdge + self.cellSize * i, self.boardEdge, self.boardEdge + self.cellSize * i, self.boardEdge + self.cellSize * (self.boardSize - 1))
            if self.parent.settingData.withCoordinate:
                p.drawText(self.boardEdge - 23, self.boardEdge + self.cellSize * i + self.fontInfo.boundingRect(str(i + 1)).height()//3, str(i + 1))
                p.drawText(self.boardEdge + self.cellSize * i - self.fontInfo.boundingRect(chr(i + 65)).width()//2, self.boardEdge - 13, chr(i + 65))
        if self.boardSize == 19:
            dotPosition = ((4, 4), (4, 10), (4, 16), (10, 4), (10, 10), (10, 16), (16, 4), (16, 10), (16, 16))
        elif self.boardSize == 9:
            dotPosition = ((3, 3), (7, 3), (5, 5), (3, 7), (7, 7))
        elif self.boardSize == 13:
            dotPosition = ((4, 4), (7, 4), (10, 4), (4, 7), (7, 7), (10, 7), (4, 10), (7, 10), (10, 10))
        else:
            dotPosition = ()
        for j in dotPosition:
            x, y = self.goToBoard(j)
            p.setPen(QPen(Qt.GlobalColor.black, 1))
            p.setBrush(QBrush(Qt.GlobalColor.black))
            p.drawEllipse(QPoint(x, y), self.dotRadius, self.dotRadius)
    
    def __paintMousePointRect(self, p):
        if self.inBoard and self.x != None and self.y != None:
            gx, gy = self.boardToGo((self.x, self.y))
            if (gx, gy) in self.parent.thisGame.stepsGoDict:
                return
            x, y = self.goToBoard((gx, gy))
            p.setPen(QPen(Qt.GlobalColor.white, 1))
            p.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
            p.drawRect(x - int(self.rectSize / 2), y - int(self.rectSize / 2), self.rectSize, self.rectSize)
    
    def goToBoard(self, co):
        x, y = co
        x1 = self.boardEdge + self.cellSize * (x - 1)
        y1 = self.boardEdge + self.cellSize * (y - 1)
        return (x1, y1)
    
    def boardToGo(self, co):
        x, y = co
        x1 = round((x - self.boardEdge) / self.cellSize + 1)
        y1 = round((y - self.boardEdge) / self.cellSize + 1)
        return (x1, y1)
    
    def checkClearCount(self, currentKey):
        keyList = list(self.parent.thisGame.stepsGoDict.keys())
        valueList = list(map(lambda x: x[1], list(self.parent.thisGame.stepsGoDict.values())))
        ind = keyList.index(currentKey)
        count = valueList[ind]
        for i in valueList[ind+1:]:
            if count >= i:
                return False
        return True
    
    def minimumSizeHint(self):
        s = 25 * (self.boardSize + 1)
        return QSize(s, s)
    
    def sizeHint(self):
        s = self.cellSize * (self.boardSize + 1)
        return QSize(s, s)
