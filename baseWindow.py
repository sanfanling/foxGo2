#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: baseWindow.py 


import os, sys, glob
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from goBoard import goBoard
from customDock import *
from settingData import settingData


class baseWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("foxGo2")
        self.setWindowIcon(QIcon("res/pictures/logo.png"))
        
        self.settingData = settingData()
        
        self.setAcceptDrops(self.settingData.acceptDragDrop)
        
        self.allBoardStyles = ("Style1", "Style2", "Style3", "Style4", "Style5", "Style6", "Style7", "Style8")
        
        self.initDockwidget()
        self.initCentralWidget()
        self.initMenuBar()
        self.initStatusBar()
        
        self.aboutQt.triggered.connect(self.aboutQt_)
        self.aboutApp.triggered.connect(self.aboutApp_)
        self.printGo.triggered.connect(self.printGo_)
        self.printGoPreview.triggered.connect(self.printGoPreview_)
    
    def removeFromLayout(self):
        self.mainLayout.removeWidget(self.board)
    
    def addToLayout(self):
        self.mainLayout.addWidget(self.board)
        self.mainLayout.setAlignment(self.board, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    
    def adjustBoardSize(self):
        l = min(self.mainLayout.contentsRect().width(), self.mainLayout.contentsRect().height())
        cellSize = l // (self.settingData.boardSize + 1)
        if cellSize < 25:
            self.board.setSizePara(25)
        else:
            self.board.setSizePara(cellSize)
    
    def resizeEvent(self, e):
        self.removeFromLayout()
        self.addToLayout()
    
    def initMenuBar(self):        
        gameMenu = self.menuBar().addMenu("Game(&G)")
        self.newGame = QAction("New...")
        self.fileOpen = QAction("Open...")
        self.saveAsAction = QAction("Save as...")
        gameMenu.addAction(self.newGame)
        gameMenu.addAction(self.fileOpen)
        gameMenu.addAction(self.saveAsAction)
        gameMenu.addSeparator()
        self.printGo = QAction("Print...")
        self.printGoPreview = QAction("Print preview...")
        gameMenu.addAction(self.printGo)
        gameMenu.addAction(self.printGoPreview)
        gameMenu.addSeparator()
        self.quit = QAction("Quit")
        gameMenu.addAction(self.quit)
        
        boardMenu = self.menuBar().addMenu("Board(&B)")
        boardSizeMenu = boardMenu.addMenu("Board size")
        self.sizeGroup = QActionGroup(self)
        self.size9 = QAction("9x9")
        self.size13 = QAction("13x13")
        self.size19 = QAction("19x19")
        self.size9.setCheckable(True)
        self.size13.setCheckable(True)
        self.size19.setCheckable(True)
        self.sizeGroup.addAction(self.size9)
        self.sizeGroup.addAction(self.size13)
        self.sizeGroup.addAction(self.size19)
        boardSizeMenu.addAction(self.size9)
        boardSizeMenu.addAction(self.size13)
        boardSizeMenu.addAction(self.size19)
        
        self.withCoordinate = QAction("Coordinate")
        self.withCoordinate.setCheckable(True)
        boardMenu.addAction(self.withCoordinate)
        self.hideCursor = QAction("Hide cursor")
        self.hideCursor.setCheckable(True)
        boardMenu.addAction(self.hideCursor)
        
        boardStyleMenu = boardMenu.addMenu("Board style")
        self.styleGroup = QActionGroup(self)
        
        self.boardNoStyle = QAction("None")
        self.boardNoStyle.setCheckable(True)
        self.styleGroup.addAction(self.boardNoStyle)
        boardStyleMenu.addAction(self.boardNoStyle)
        for styles in self.allBoardStyles:
            exec(f"self.board{styles} = QAction('{styles}')")
            eval(f"self.board{styles}.setCheckable(True)")
            eval(f"self.styleGroup.addAction(self.board{styles})")
            eval(f"boardStyleMenu.addAction(self.board{styles})")
        
        controlMenu = self.menuBar().addMenu("Control(&C)")
        self.toStartAction = QAction("Previous to start")
        self.fastPrevAction = QAction("Previous 10 steps")
        self.prevAction = QAction("Previous")
        self.nextAction = QAction("Next")
        self.fastNextAction = QAction("Next 10 steps")
        self.toEndAction = QAction("Next to end")
        self.backAction = QAction("Back")
        self.setAllShortcuts()
        
        controlMenu.addAction(self.toStartAction)
        controlMenu.addAction(self.fastPrevAction)
        controlMenu.addAction(self.prevAction)
        controlMenu.addAction(self.nextAction)
        controlMenu.addAction(self.fastNextAction)
        controlMenu.addAction(self.toEndAction)
        controlMenu.addAction(self.backAction)
        controlMenu.addSeparator()
        
        otherMenu = controlMenu.addMenu("Others")
        self.autoReviewAction = QAction("Auto-review")
        self.autoReviewAction.setCheckable(True)
        self.passAction = QAction("Pass")
        self.resignAction = QAction("Resign")
        otherMenu.addAction(self.autoReviewAction)
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
        viewMenu.addAction(self.consoleDock.toggleViewAction())
        
        settingMenu = self.menuBar().addMenu("Settings(&S)")
        self.settingAction = QAction("Configrate foxGo2...")
        settingMenu.addAction(self.settingAction)
        
        helpMenu = self.menuBar().addMenu("Help(&H)")
        self.aboutApp = QAction("About foxGo2...")
        self.aboutQt = QAction("About Qt...")
        helpMenu.addAction(self.aboutApp)
        helpMenu.addAction(self.aboutQt)
    
    def initCentralWidget(self):
        self.centralWidget = boardAreaWidget(self)
        self.mainLayout = QVBoxLayout(None)
        self.board = goBoard(self, self.settingData.boardSize)
        self.addToLayout()
        self.adjustBoardSize()
        self.board.update()
        
        self.centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.centralWidget)
    
    def initDockwidget(self):
        self.sgfExplorerDock = sgfExplorerDock("Sgf explorer", self)
        self.sgfExplorerDock.setObjectName("Sgf explorer")
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.sgfExplorerDock)
        
        self.recentGamesDock = recentGamesDock("Recent games", self)
        self.recentGamesDock.setObjectName("Recent games")
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.recentGamesDock)
        
        self.infoDock = infoDock("Information", self)
        self.infoDock.setObjectName("Information")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.infoDock)
        
        self.commentsDock = commentsDock("Comments", self)
        self.commentsDock.setObjectName("Comments")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.commentsDock)
        
        self.controlDock = controlDock("Control", self)
        self.controlDock.setObjectName("Control")
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.controlDock)
        
        self.consoleDock = consoleDock("Console", self)
        self.consoleDock.setObjectName("Console")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.consoleDock)
        
        self.setCorner(Qt.Corner.BottomLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
        self.setCorner(Qt.Corner.TopLeftCorner, Qt.DockWidgetArea.LeftDockWidgetArea)
        self.setCorner(Qt.Corner.TopRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
    
    def initStatusBar(self):
        self.modeLabel = QLabel()
        self.statusBar().addPermanentWidget(self.modeLabel)
    
    def setAllShortcuts(self):
        self.toStartAction.setShortcut(QKeySequence(self.settingData.previousToStart))
        self.fastPrevAction.setShortcut(QKeySequence(self.settingData.previous10Steps))
        self.prevAction.setShortcut(QKeySequence(self.settingData.previousStep))
        self.nextAction.setShortcut(QKeySequence(self.settingData.nextStep))
        self.fastNextAction.setShortcut(QKeySequence(self.settingData.next10Steps))
        self.toEndAction.setShortcut(QKeySequence(self.settingData.nextToEnd))
        self.backAction.setShortcut(QKeySequence(self.settingData.back))
    
    def printGo_(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec() == QDialog.DialogCode.Accepted:
            self.handlePaintRequest(printer)
    
    def printGoPreview_(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec()
    
    def handlePaintRequest(self, printer):
        painter = QPainter(printer)
        rect = painter.viewport()
        pix = self.board.grab(self.board.rect())
        size = pix.size()
        size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
        painter.setWindow(pix.rect())
        painter.drawPixmap(0, 0, pix)
    
    def aboutQt_(self):
        QMessageBox.aboutQt(self, "About Qt")
    
    def aboutApp_(self):
        QMessageBox.about(self, "About foxGo2", "2nd generation of foxGo, with new interface and better experience.\nSupport importing/exporting sgf file\nSupport foxWeiqi fast view\nSupport face system\nSupport editing comments\nSupport all-size board(9, 13, 19)\n\nAuthor: sanfanling\nE-mail: xujia19@outlook.com")

class boardAreaWidget(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    
    def resizeEvent(self, e):
        self.parent.adjustBoardSize()
        self.parent.removeFromLayout()
        self.parent.addToLayout()
