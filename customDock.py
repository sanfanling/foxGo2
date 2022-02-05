#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: customDock.py 


import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from customThread import getCatalogThread, getSgfThread




class controlDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        self.controlWidget = controlWidget(parent)
        self.setWidget(self.controlWidget)
        self.setFloating(False)
        

class controlWidget(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        mainLayout = QVBoxLayout(None)
        
        controlLayout = QHBoxLayout(None)
        self.toStartButton = QPushButton("|<")
        self.fastPrevButton = QPushButton("<<")
        self.prevButton = QPushButton("<")
        self.stepsCount= QSpinBox()
        self.nextButton = QPushButton(">")
        self.fastNextButton = QPushButton(">>")
        self.toEndButton = QPushButton(">|")
        self.backButton = QPushButton("Back")
        self.otherButton = QPushButton("Others")
        otherMenu = QMenu()
        self.passAction = QAction("Pass")
        self.resignAction = QAction("Resign")
        otherMenu.addAction(self.passAction)
        otherMenu.addAction(self.resignAction)
        self.otherButton.setMenu(otherMenu)
        
        controlLayout.addWidget(self.toStartButton)
        controlLayout.addWidget(self.fastPrevButton)
        controlLayout.addWidget(self.prevButton)
        controlLayout.addWidget(self.stepsCount)
        controlLayout.addWidget(self.nextButton)
        controlLayout.addWidget(self.fastNextButton)
        controlLayout.addWidget(self.toEndButton)
        controlLayout.addWidget(self.backButton)
        controlLayout.addWidget(self.otherButton)
        
        self.stepsSlider = QSlider(self)
        self.stepsSlider.setTracking(True)
        self.stepsSlider.setOrientation(Qt.Horizontal)
        
        mainLayout.addLayout(controlLayout)
        mainLayout.addWidget(self.stepsSlider)
        self.setLayout(mainLayout)
        
        self.stepsCount.editingFinished.connect(self.parent.gotoSpecifiedStep)
        self.stepsSlider.valueChanged.connect(self.stepsCount.setValue)
        self.stepsSlider.sliderReleased.connect(self.parent.gotoSpecifiedStep)
        
class stepsTreeDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        self.stepsTreeDisplay = stepsTreeDisplay(parent)
        self.setWidget(self.stepsTreeDisplay)
        self.setFloating(False)


class stepsTreeDisplay(QTreeWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        


class recentGamesDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        self.recentGamesDisplay = recentGamesDisplay(parent)
        self.setWidget(self.recentGamesDisplay)
        self.setFloating(False)

class recentGamesDisplay(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        mainLayout = QVBoxLayout(None)
        self.stack = QStackedWidget()
        self.loadingLabel = QLabel("Loading...")
        self.loadingLabel.setAlignment(Qt.AlignHCenter)
        self.table = QTableWidget(0, 3)
        self.table.hideColumn(2)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        header = ["Game", "Date", "key"]
        self.table.setHorizontalHeaderLabels(header)
        self.stack.addWidget(self.loadingLabel)
        self.stack.addWidget(self.table)
        
        
        buttonLayout = QHBoxLayout(None)
        self.viewButton = QPushButton("View")
        self.downButton = QPushButton("Download")
        self.refreshButton = QPushButton("Refresh")
        buttonLayout.addWidget(self.viewButton)
        buttonLayout.addWidget(self.downButton)
        buttonLayout.addWidget(self.refreshButton)
                
        mainLayout.addWidget(self.stack)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        
        self.catalogThread = getCatalogThread()
        self.sgfThread = getSgfThread(None)
        self.pageToLabel()
        
        
        self.catalogThread.missionDone.connect(self.pageToTable)
        self.refreshButton.clicked.connect(self.pageToLabel)
        self.viewButton.clicked.connect(self.viewButton_)
        self.sgfThread.missionDone.connect(self.sgfGot)
        
    
    def pageToTable(self, catalog):
        self.catalog = catalog
        self.table.setRowCount(len(self.catalog))
        row = 0
        for game, date, key in self.catalog:
            self.table.setItem(row, 0, QTableWidgetItem(game))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(key))
            row += 1
        self.stack.setCurrentIndex(1)
        self.viewButton.setEnabled(True)
        self.downButton.setEnabled(True)
        self.refreshButton.setEnabled(True)
    
    def pageToLabel(self):
        self.stack.setCurrentIndex(0)
        self.viewButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.refreshButton.setEnabled(False)
        self.catalogThread.start()
    
    def viewButton_(self):
        row = self.table.currentRow()
        key = self.table.item(row, 2).text()
        self.sgfThread.key = key
        self.sgfThread.start()
    
    def sgfGot(self, sgf):
        self.parent.startReviewMode(sgf)
            
        

class infoDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        self.infoDisplay = infoDisplay(parent)
        self.setWidget(self.infoDisplay)
        self.setFloating(False)

class infoDisplay(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        mainLayout = QVBoxLayout(None)
        
        self.gameLabel = QLabel("中国围棋甲级联赛决赛")
        self.gameLabel.setAlignment(Qt.AlignCenter)
        self.gameLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.gameLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 15px}")
        
        playerLayout = QHBoxLayout(None)
        blackLayout = QVBoxLayout(None)
        self.blackLabel = QLabel("BLACK")
        self.blackLabel.setAlignment(Qt.AlignCenter)
        self.blackLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.blackLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 13px}")
        self.blackPlayer = QLabel("-")
        self.blackPlayer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.blackPlayer.setAlignment(Qt.AlignCenter)
        self.blackPhoto = QLabel()
        self.blackPhoto.setAlignment(Qt.AlignCenter)
        pix = QPixmap("res/pictures/blank.png").scaled(100, 100, 0, 1)
        self.blackPhoto.setPixmap(pix)
        blackLayout.addWidget(self.blackLabel)
        blackLayout.addWidget(self.blackPlayer)
        blackLayout.addWidget(self.blackPhoto)
        whiteLayout = QVBoxLayout(None)
        self.whiteLabel = QLabel("WHITE")
        self.whiteLabel.setAlignment(Qt.AlignCenter)
        self.whiteLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.whiteLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 13px}")
        self.whitePlayer = QLabel("-")
        self.whitePlayer.setAlignment(Qt.AlignCenter)
        self.whitePlayer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.whitePhoto = QLabel()
        self.whitePhoto.setAlignment(Qt.AlignCenter)
        self.whitePhoto.setPixmap(pix)
        whiteLayout.addWidget(self.whiteLabel)
        whiteLayout.addWidget(self.whitePlayer)
        whiteLayout.addWidget(self.whitePhoto)
        vsLabel = QLabel("VS")
        vsLabel.setAlignment(Qt.AlignCenter)
        vsLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        playerLayout.addLayout(blackLayout)
        playerLayout.addWidget(vsLabel)
        playerLayout.addLayout(whiteLayout)
        
        haLayout = QHBoxLayout(None)
        self.haLabel = QLabel("HA:")
        self.haValue = QLabel("-")
        haLayout.addWidget(self.haLabel)
        haLayout.addWidget(self.haValue)
        
        komiLayout = QHBoxLayout(None)
        self.komiLabel = QLabel("KOMI:")
        self.komiValue = QLabel("-")
        komiLayout.addWidget(self.komiLabel)
        komiLayout.addWidget(self.komiValue)
        
        ruleLayout = QHBoxLayout(None)
        self.ruleLabel = QLabel("RULE:")
        self.ruleValue = QLabel("-")
        ruleLayout.addWidget(self.ruleLabel)
        ruleLayout.addWidget(self.ruleValue)
        
        dateLayout = QHBoxLayout(None)
        self.dateLabel = QLabel("DATE:")
        self.dateValue = QLabel("-")
        dateLayout.addWidget(self.dateLabel)
        dateLayout.addWidget(self.dateValue)
        
        resultLayout = QHBoxLayout(None)
        self.resultLabel = QLabel("RESULT:")
        self.resultValue = QLabel("-")
        resultLayout.addWidget(self.resultLabel)
        resultLayout.addWidget(self.resultValue)
        
        timeLimitLayout =QHBoxLayout(None)
        self.timeLimitLabel = QLabel("TIME LIMIT:")
        self.timeLimitValue = QLabel("-")
        timeLimitLayout.addWidget(self.timeLimitLabel)
        timeLimitLayout.addWidget(self.timeLimitValue)
        
        mainLayout.addWidget(self.gameLabel)
        mainLayout.addLayout(playerLayout)
        mainLayout.addLayout(dateLayout)
        mainLayout.addLayout(ruleLayout)
        mainLayout.addLayout(komiLayout)
        mainLayout.addLayout(haLayout)
        mainLayout.addLayout(resultLayout)
        mainLayout.addLayout(timeLimitLayout)
        mainLayout.addStretch(0)
        self.setLayout(mainLayout)
        
        
class commentsDock(QDockWidget):
    
    def __init__(self, title):
        super().__init__(title)
        
        self.commentsDisplay = QTextBrowser()
        self.setWidget(self.commentsDisplay)
        self.setFloating(False)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = infoDisplay()
	w.show()
	sys.exit(app.exec_())
