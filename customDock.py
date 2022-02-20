#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: customDock.py 


import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from customThread import getCatalogThread, getSgfThread
import glob




class controlDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        try:
            self.restorGeometry(parent.settingData.controlDockGeometry)
        except:
            pass
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
        self.autoReviewAction = QAction("Auto-review")
        self.passAction = QAction("Pass")
        self.resignAction = QAction("Resign")
        otherMenu.addAction(self.autoReviewAction)
        otherMenu.addAction(self.passAction)
        otherMenu.addAction(self.resignAction)
        self.otherButton.setMenu(otherMenu)
        
        controlLayout.addStretch(0)
        controlLayout.addWidget(self.toStartButton)
        controlLayout.addWidget(self.fastPrevButton)
        controlLayout.addWidget(self.prevButton)
        controlLayout.addWidget(self.stepsCount)
        controlLayout.addWidget(self.nextButton)
        controlLayout.addWidget(self.fastNextButton)
        controlLayout.addWidget(self.toEndButton)
        controlLayout.addWidget(self.backButton)
        controlLayout.addWidget(self.otherButton)
        controlLayout.addStretch(0)
        
        self.stepsSlider = QSlider(self)
        self.stepsSlider.setTracking(True)
        self.stepsSlider.setOrientation(Qt.Horizontal)
        
        mainLayout.addLayout(controlLayout)
        mainLayout.addWidget(self.stepsSlider)
        self.setLayout(mainLayout)
        
        self.stepsCount.editingFinished.connect(self.parent.gotoSpecifiedStep)
        self.stepsSlider.valueChanged.connect(self.stepsCount.setValue)
        self.stepsSlider.sliderReleased.connect(self.parent.gotoSpecifiedStep)
        
class sgfExplorerDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        try:
            self.restorGeometry(parent.settingData.sgfExplorerDockGeometry)
        except:
            pass
        self.sgfExplorerDisplay = sgfExplorerDisplay(parent)
        self.setWidget(self.sgfExplorerDisplay)
        self.setFloating(False)


class sgfExplorerDisplay(QWidget):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.sgfPath = self.parent.settingData.sgfPath
        mainLayout = QVBoxLayout(None)
        
        searchLayout = QHBoxLayout(None)
        self.filterLabel = QLabel("Search:")
        self.filterLine = QLineEdit()
        self.filterLine.setClearButtonEnabled(True)
        searchLayout.addWidget(self.filterLabel)
        searchLayout.addWidget(self.filterLine)
        self.explorer = QTreeWidget()
        self.explorer.setHeaderLabel("Sgf files")
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.explorer)
        self.setLayout(mainLayout)
        self.showItems()
        
        self.filterLine.textChanged.connect(self.showItems)
        self.explorer.itemDoubleClicked.connect(self.showSelectedSgfFile)
        
    def syncPath(self):
        self.sgfPath = self.parent.settingData.sgfPath
        self.showItems()
    
    def showItems(self, t = ""):
        self.explorer.clear()
        for i in glob.glob(os.path.join(self.sgfPath, "*.sgf")):
            baseName, fileName = os.path.split(i)
            if t in fileName:
                self.explorer.addTopLevelItem(QTreeWidgetItem([fileName]))
    
    def showSelectedSgfFile(self, w):
        try:
            with open(os.path.join(self.sgfPath, w.text(0))) as f:
                sgf = f.read()
        except FileNotFoundError:
            QMessageBox.critical(self, "Open file error", "The selected file does not exists!")
            self.filterLine.clear()
            self.showItems()
        else:
            self.parent.startReviewMode(sgf)


class recentGamesDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        try:
            self.restorGeometry(parent.settingData.recentGameDockGeometry)
        except:
            pass
        self.recentGamesDisplay = recentGamesDisplay(parent)
        self.setWidget(self.recentGamesDisplay)
        self.setFloating(False)

class recentGamesDisplay(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.downloadSign = False
        self.fileName = None
        self.downloadList = []
        self.downloadIndex = 0
        mainLayout = QVBoxLayout(None)
        self.stack = QStackedWidget()
        self.loadingLabel = QLabel("Loading...")
        self.loadingLabel.setAlignment(Qt.AlignHCenter)
        self.table = QTableWidget(0, 4)
        self.table.hideColumn(0)
        self.table.hideColumn(3)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        header = ["Select", "Game", "Date", "key"]
        self.table.setHorizontalHeaderLabels(header)
        self.stack.addWidget(self.loadingLabel)
        self.stack.addWidget(self.table)
        try:
            self.table.horizontalHeader().restoreState(parent.settingData.recentGamesDockTableState)
        except:
            pass
        
        
        buttonLayout = QHBoxLayout(None)
        self.viewButton = QPushButton("View")
        self.downButton = QPushButton("Download")
        self.refreshButton = QPushButton("Refresh")
        self.selectButton = QPushButton("Select")
        buttonLayout.addWidget(self.viewButton)
        buttonLayout.addWidget(self.selectButton)
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
        self.downButton.clicked.connect(self.downButton_)
        self.table.activated.connect(self.enableViewButton)
        self.selectButton.clicked.connect(self.selectButton_)
    
    def selectButton_(self):
        if self.table.isColumnHidden(0):
            self.table.showColumn(0)
            self.downButton.setEnabled(True)
        else:
            self.table.hideColumn(0)
            self.downButton.setEnabled(False)
    
    def enableViewButton(self):
        self.viewButton.setEnabled(True)
        
    
    def pageToTable(self, catalog):
        self.table.setRowCount(len(catalog))
        row = 0
        for game, date, key in catalog:
            self.table.setCellWidget(row, 0, QCheckBox())
            self.table.setItem(row, 1, QTableWidgetItem(game))
            self.table.setItem(row, 2, QTableWidgetItem(date))
            self.table.setItem(row, 3, QTableWidgetItem(key))
            row += 1
        self.stack.setCurrentIndex(1)
        self.viewButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.refreshButton.setEnabled(True)
        self.selectButton.setEnabled(True)
    
    def pageToLabel(self):
        self.stack.setCurrentIndex(0)
        self.viewButton.setEnabled(False)
        self.downButton.setEnabled(False)
        self.refreshButton.setEnabled(False)
        self.selectButton.setEnabled(False)
        self.catalogThread.start()
    
    def viewButton_(self):
        self.downloadSign = False
        row = self.table.currentRow()
        self.__startThread(row)
    
    def downButton_(self):
        self.downloadSign = True
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).isChecked():
                self.downloadList.append(i)
                self.table.cellWidget(i, 0).setChecked(False)
        self.table.hideColumn(0)
        self.downButton.setEnabled(False)
        self.downloadInList()
    
    def downloadInList(self):
        if len(self.downloadList) == self.downloadIndex:
            self.parent.statusBar().showMessage("Download mission complete!", 5000)
            self.downloadList.clear()
            self.downloadIndex = 0
        else:
            item = self.downloadList[self.downloadIndex]
            self.__startThread(item)
    
    def __startThread(self, row):
        self.fileName = self.table.item(row, 1).text().replace("/", "-")
        if row == -1:
            QMessageBox.warning(self, "Error", "No item is selected, download fail!")
        else:
            key = self.table.item(row, 3).text()
            self.sgfThread.key = key
            self.sgfThread.start()
    
    def sgfGot(self, sgf):
        if self.downloadSign:
            p = os.path.join(self.parent.settingData.sgfPath, "{}.sgf".format(self.fileName))
            if not os.path.exists(p):
                with open(p, "w") as f:
                    f.write(sgf)
                self.parent.sgfExplorerDock.sgfExplorerDisplay.showItems()
            else:
                if not self.parent.settingData.autoSkip:
                    f, filt= QFileDialog.getSaveFileName(None, "Save as", p, "Go records file(*.sgf)")
                    if f != "":
                        with open(f, "w") as fi:
                            fi.write(sgf)
            self.downloadIndex += 1
            self.downloadInList()
        else:
            self.parent.startReviewMode(sgf)
            
        

class infoDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        try:
            self.restorGeometry(parent.settingData.infoDockGeometry)
        except:
            pass
        self.infoDisplay = infoDisplay(parent)
        self.setWidget(self.infoDisplay)
        self.setFloating(False)

class infoDisplay(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        mainLayout = QVBoxLayout(None)
        
        self.gameLabel = QLabel("-")
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
    
    def __init__(self, title, parent):
        super().__init__(title)
        try:
            self.restorGeometry(parent.settingData.commentsDockGeometry)
        except:
            pass
        self.parent = parent
        self.commentsDisplay = QTextBrowser()
        self.commentsDisplay.setOpenLinks(False)
        self.setWidget(self.commentsDisplay)
        self.setFloating(False)
        
        self.commentsDisplay.anchorClicked.connect(self.parent.showVariation)


class consoleDock(QDockWidget):
    
    def __init__(self, title, parent = None):
        super().__init__(title)
        try:
            self.restorGeometry(parent.settingData.consoleDockGeometry)
        except:
            pass
        self.parnet = parent
        self.consoleDisplay = consoleDisplay(parent)
        self.setWidget(self.consoleDisplay)
        self.setFloating(False)

class consoleDisplay(QWidget):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        mainLayout = QVBoxLayout(None)
        self.console = QTextBrowser()
        self.console.setAcceptRichText(False)
        hlayout = QHBoxLayout(None)
        self.clearButton = QPushButton("Clear")
        hlayout.addStretch(0)
        hlayout.addWidget(self.clearButton)
        mainLayout.addWidget(self.console)
        mainLayout.addLayout(hlayout)
        self.setLayout(mainLayout)
        
        self.clearButton.clicked.connect(self.console.clear)
    
    def addOutput(self, sender, m):
        self.console.append("[{}] {}".format(sender, m))
        


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = recentGamesDisplay(None)
	w.show()
	sys.exit(app.exec_())
