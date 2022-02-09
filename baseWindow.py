#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: baseWindow.py 


import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from goBoard import goBoard
from customDock import *
from goEngine import go
from settingData import settingData


class baseWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("foxGo2")
        self.setWindowIcon(QIcon("res/pictures/logo.png"))
        
        self.settingData = settingData()
        self.settingData.getSettingData()
        
        self.boardSize = 19
        self.initDockwidget()
        self.initCentralWidget()
        self.initMenuBar()
        self.initStatusBar()
        
        self.thisGame = go()

        self.board.startPaint.connect(self.removeFromLayout)
        self.board.endPaint.connect(self.addToLayout)
        self.aboutQt.triggered.connect(self.aboutQt_)
        self.aboutApp.triggered.connect(self.aboutApp_)
        self.printGo.triggered.connect(self.printGo_)
        self.printGoPreview.triggered.connect(self.printGoPreview_)
    
    def removeFromLayout(self):
        self.mainLayout.removeWidget(self.board)
    
    def addToLayout(self):
        self.mainLayout.addWidget(self.board)
        self.mainLayout.setAlignment(self.board, Qt.AlignHCenter | Qt.AlignVCenter)
    
    def __adjustBoardSize(self):
        l = min(self.mainLayout.contentsRect().width(), self.mainLayout.contentsRect().height())
        cellSize = l // (self.boardSize + 1)
        if cellSize < 25:
            self.board.setSizePara(25)
        else:
            self.board.setSizePara(cellSize)
        
    def resizeEvent(self, e):
        self.__adjustBoardSize()
    
    def initMenuBar(self):        
        gameMenu = self.menuBar().addMenu("Game(&G)")
        self.newGame = QAction("New")
        self.fileOpen = QAction("Open...")
        gameMenu.addAction(self.newGame)
        gameMenu.addAction(self.fileOpen)
        gameMenu.addSeparator()
        self.printGo = QAction("Print...")
        self.printGoPreview = QAction("Print preview...")
        gameMenu.addAction(self.printGo)
        gameMenu.addAction(self.printGoPreview)
        gameMenu.addSeparator()
        self.quit = QAction("Quit")
        gameMenu.addAction(self.quit)
        
        boardMenu = self.menuBar().addMenu("Board(&B)")
        self.withCoordinate = QAction("Coordinate")
        self.withCoordinate.setCheckable(True)
        boardMenu.addAction(self.withCoordinate)
        self.hideCursor = QAction("Hide cursor")
        self.hideCursor.setCheckable(True)
        boardMenu.addAction(self.hideCursor)
        
        controlMenu = self.menuBar().addMenu("Control(&C)")
        self.toStartAction = QAction("Previous to start")
        self.fastPrevAction = QAction("Previous 10 steps")
        self.prevAction = QAction("Previous")
        self.nextAction = QAction("Next")
        self.fastNextAction = QAction("Next 10 steps")
        self.toEndAction = QAction("Next to end")
        self.backAction = QAction("Back")
        
        controlMenu.addAction(self.toStartAction)
        controlMenu.addAction(self.fastPrevAction)
        controlMenu.addAction(self.prevAction)
        controlMenu.addAction(self.nextAction)
        controlMenu.addAction(self.fastNextAction)
        controlMenu.addAction(self.toEndAction)
        controlMenu.addAction(self.backAction)
        
        otherMenu = controlMenu.addMenu("Others")
        self.passAction = QAction("Pass")
        self.resignAction = QAction("Resign")
        otherMenu.addAction(self.passAction)
        otherMenu.addAction(self.resignAction)
        
        
        stepsNumberMenu = boardMenu.addMenu("Step number")
        self.stepsNumberGroup = QActionGroup(self)
        self.stepsNumberAll = QAction("All")
        self.stepsNumberAll.setCheckable(True)
        self.stepsNumberCurrent = QAction("Current")
        self.stepsNumberCurrent.setCheckable(True)
        self.stepsNumberHide = QAction("Hide")
        self.stepsNumberHide.setCheckable(True)
        self.stepsNumberGroup.addAction(self.stepsNumberAll)
        self.stepsNumberGroup.addAction(self.stepsNumberCurrent)
        self.stepsNumberGroup.addAction(self.stepsNumberHide)
        stepsNumberMenu.addAction(self.stepsNumberAll)
        stepsNumberMenu.addAction(self.stepsNumberCurrent)
        stepsNumberMenu.addAction(self.stepsNumberHide)
        
        boardStyleMenu = boardMenu.addMenu("Board style")
        self.styleGroup = QActionGroup(self)
        self.boardNoStyle = QAction("None")
        self.boardStyle1 = QAction("Style1")
        self.boardStyle2 = QAction("Style2")
        self.boardNoStyle.setCheckable(True)
        self.boardStyle1.setCheckable(True)
        self.boardStyle2.setCheckable(True)
        self.styleGroup.addAction(self.boardNoStyle)
        self.styleGroup.addAction(self.boardStyle1)
        self.styleGroup.addAction(self.boardStyle2)
        boardStyleMenu.addAction(self.boardNoStyle)
        boardStyleMenu.addAction(self.boardStyle1)
        boardStyleMenu.addAction(self.boardStyle2)
        
        soundMenu = self.menuBar().addMenu("Sound(&D)")
        self.backgroundMusic = QAction("Background music")
        self.backgroundMusic.setCheckable(True)
        self.effectSounds = QAction("Effect sounds")
        self.effectSounds.setCheckable(True)
        soundMenu.addAction(self.backgroundMusic)
        soundMenu.addAction(self.effectSounds)
        
        viewMenu = self.menuBar().addMenu("View(&V)")
        viewMenu.addAction(self.controlDock.toggleViewAction())
        viewMenu.addAction(self.sgfExplorerDock.toggleViewAction())
        viewMenu.addAction(self.recentGamesDock.toggleViewAction())
        viewMenu.addAction(self.infoDock.toggleViewAction())
        viewMenu.addAction(self.commentsDock.toggleViewAction())
        
        settingMenu = self.menuBar().addMenu("Settings(&S)")
        self.settingAction = QAction("Configrate foxGo2...")
        settingMenu.addAction(self.settingAction)
        
        helpMenu = self.menuBar().addMenu("Help(&H)")
        self.aboutApp = QAction("About foxGo2...")
        self.aboutQt = QAction("About Qt...")
        helpMenu.addAction(self.aboutApp)
        helpMenu.addAction(self.aboutQt)
    
    def initCentralWidget(self):
        centralWidget = QWidget()
        self.mainLayout = QVBoxLayout(None)
        self.board = goBoard(self)
        self.__adjustBoardSize()
        self.board.update()
        self.addToLayout()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)
    
    def initDockwidget(self):
        self.sgfExplorerDock = sgfExplorerDock("Sgf explorer", self)
        self.sgfExplorerDock.setObjectName("Sgf explorer")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sgfExplorerDock)
        
        self.recentGamesDock = recentGamesDock("Recent games", self)
        self.recentGamesDock.setObjectName("Recent games")
        self.addDockWidget(Qt.LeftDockWidgetArea, self.recentGamesDock)
        
        self.infoDock = infoDock("Information", self)
        self.infoDock.setObjectName("Information")
        self.addDockWidget(Qt.RightDockWidgetArea, self.infoDock)
        
        self.commentsDock = commentsDock("Comments", self)
        self.commentsDock.setObjectName("Comments")
        self.addDockWidget(Qt.RightDockWidgetArea, self.commentsDock)
        
        self.controlDock = controlDock("Control", self)
        self.controlDock.setObjectName("Control")
        self.addDockWidget(Qt.BottomDockWidgetArea, self.controlDock)
        
        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
    
    def initStatusBar(self):
        self.modeLabel = QLabel()
        #self.modeLabel.setAlignment(Qt.AlignLeft)
        self.statusBar().addPermanentWidget(self.modeLabel)
    
    def printGo_(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(printer)
    
    def printGoPreview_(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()
    
    def handlePaintRequest(self, printer):
        painter = QPainter(printer)
        rect = painter.viewport()
        pix = self.board.grab(self.board.rect())
        size = pix.size()
        size.scale(rect.size(), Qt.KeepAspectRatio)
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(pix.rect())
        painter.drawPixmap(0, 0, pix)
    
    def aboutQt_(self):
        QMessageBox.aboutQt(self, "About Qt")
    
    def aboutApp_(self):
        QMessageBox.about(self, "About foxGo2", "2nd generation of foxGo, with new interface and experience. Enjoy go's magic with foxGo2!")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = baseWindow()
	w.show()
	sys.exit(app.exec_())
