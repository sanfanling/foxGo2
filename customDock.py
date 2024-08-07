#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: customDock.py 


import os, sys, re
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from customThread import getCatalogThread, getSgfThread
import glob
from editCommentsDialog import editCommentsDialog
from faceDict import faceDict_anti


class QLineEditWithHistory(QLineEdit):
    
    def __init__(self, historyList):
        super().__init__()
        self.searchHistoryList = historyList
        self.setPlaceholderText("Press Enter to record to history")
        self.completer = QCompleter(self)
        self.listModel = QStringListModel(self.searchHistoryList, self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setModel(self.listModel)
        self.setCompleter(self.completer)
        
        self.returnPressed.connect(self.addItemInHistory)
        self.completer.activated.connect(self.popupFinished)
    
    def addItemInHistory(self):
        content = self.text().strip()
        if content != "" and content not in self.searchHistoryList:
            self.searchHistoryList.insert(0, content)
            self.searchHistoryList = self.searchHistoryList[:10]
            self.listModel.setStringList(self.searchHistoryList)
            self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
    
    def popupFinished(self, text):
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
    
    def event(self, event):
        if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Tab:
            self.completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
            self.completer.complete()
            self.completer.popup().show()
            return True
        return super().event(event)
    
    def mousePressEvent(self, event):
        if event.buttons () == Qt.MouseButton.LeftButton:
            self.completer.setCompletionMode(QCompleter.CompletionMode.UnfilteredPopupCompletion)
            self.completer.complete()
            self.completer.popup().show()


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
        self.autoReviewAction.setCheckable(True)
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
        self.stepsSlider.setOrientation(Qt.Orientation.Horizontal)
        
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
        self.filterLine = QLineEditWithHistory(self.parent.settingData.searchHistory)
        self.filterLine.setClearButtonEnabled(True)
        searchLayout.addWidget(self.filterLabel)
        searchLayout.addWidget(self.filterLine)
        self.explorer = QTreeWidget()
        self.explorer.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.explorer.setHeaderLabel("Sgf files")
        
        funcLayout = QHBoxLayout(None)
        self.delFunc = QPushButton("Delete...")
        self.delFunc.setEnabled(False)
        self.renameFunc = QPushButton("Rename...")
        self.renameFunc.setEnabled(False)
        self.reloadFunc = QPushButton("Refresh")
        funcLayout.addWidget(self.delFunc)
        funcLayout.addWidget(self.renameFunc)
        funcLayout.addWidget(self.reloadFunc)
        
        mainLayout.addLayout(searchLayout)
        mainLayout.addWidget(self.explorer)
        mainLayout.addLayout(funcLayout)
        self.setLayout(mainLayout)
        self.showItems()
        
        self.filterLine.textChanged.connect(self.showItems)
        self.explorer.itemDoubleClicked.connect(self.showSelectedSgfFile)
        self.explorer.itemSelectionChanged.connect(self.enableFunc)
        self.delFunc.clicked.connect(self.delFunc_)
        self.renameFunc.clicked.connect(self.renameFunc_)
        self.reloadFunc.clicked.connect(self.reloadFunc_)
    
    def enableFunc(self):
        t = len(self.explorer.selectedItems())
        if  t == 0:
            self.delFunc.setEnabled(False)
            self.renameFunc.setEnabled(False)
        elif t == 1:
            self.delFunc.setEnabled(True)
            self.renameFunc.setEnabled(True)
        else:
            self.delFunc.setEnabled(True)
            self.renameFunc.setEnabled(False)
    
    def delFunc_(self):
        re = QMessageBox.warning(self, "sgf explorer", "Are you sure to delete the selected file(s)?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
        if re == 16384:
            for i in self.explorer.selectedItems():
                f = os.path.join(self.sgfPath, i.text(0))
                os.remove(f)
            self.reloadFunc_()
            
    
    def renameFunc_(self):
        name = self.explorer.selectedItems()[0].text(0)
        text, ok= QInputDialog.getText(self, "Rename:", "Input new file name:", QLineEdit.EchoMode.Normal, name)
        if ok and text != "":
            os.rename(os.path.join(self.sgfPath, name), os.path.join(self.sgfPath, text))
            self.reloadFunc_()
    
    def reloadFunc_(self):
        self.filterLine.clear()
        self.showItems()
        
    def syncPath(self):
        self.sgfPath = self.parent.settingData.sgfPath
        self.showItems()
    
    def showItems(self, t = ""):
        self.explorer.clear()
        for i in glob.glob(os.path.join(self.sgfPath, "*.sgf")):
            baseName, fileName = os.path.split(i)
            if t in fileName:
                item = QTreeWidgetItem([fileName])
                item.setToolTip(0, fileName)
                self.explorer.addTopLevelItem(item)
    
    def showSelectedSgfFile(self, w):
        try:
            with open(os.path.join(self.sgfPath, w.text(0)), "r", encoding = "utf8") as f:
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
        self.loadingLabel = QLabel()
        self.loadingLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        movie = QMovie("res/pictures/waiting.gif")
        self.loadingLabel.setMovie(movie)
        self.table = QTableWidget(0, 4)
        self.table.hideColumn(0)
        self.table.hideColumn(3)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
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
        self.table.itemSelectionChanged.connect(self.enableViewButton)
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
        self.loadingLabel.movie().stop()
        self.table.setRowCount(len(catalog))
        row = 0
        for game, date, key in catalog:
            self.table.setCellWidget(row, 0, QCheckBox())
            item = QTableWidgetItem(game)
            item.setToolTip(game)
            self.table.setItem(row, 1, item)
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
        self.loadingLabel.movie().start()
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
        self.fileName = re.sub(r'[\\/:*?"<>|\r\n]+', "_", self.table.item(row, 1).text())
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
                with open(p, "w", encoding = "utf8") as f:
                    f.write(sgf)
                self.parent.sgfExplorerDock.sgfExplorerDisplay.showItems()
            else:
                if not self.parent.settingData.autoSkip:
                    f, filt= QFileDialog.getSaveFileName(None, "Save as", p, "Go records file(*.sgf)")
                    if f != "":
                        with open(f, "w", encoding = "utf8") as fi:
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
        self.gameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gameLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.gameLabel.setWordWrap(True)
        self.gameLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 15px}")
        
        playerLayout = QHBoxLayout(None)
        blackLayout = QVBoxLayout(None)
        self.blackLabel = QLabel("BLACK")
        self.blackLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blackLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.blackLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 13px}")
        self.blackPlayer = QLabel("-")
        self.blackPlayer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.blackPlayer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blackPhoto = QLabel()
        self.blackPhoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photoSheet = "min-width: 100px; max-width: 100px; min-height: 100px; max-height: 100px; border-radius: 50px; border-width: 0 0 0 0; border-image: url(headers/blank.png) 0 0 0 0 stretch strectch;"
        self.blackPhoto.setStyleSheet(photoSheet)
        
        blackLayout.addWidget(self.blackLabel)
        blackLayout.addWidget(self.blackPlayer)
        blackLayout.addWidget(self.blackPhoto)
        whiteLayout = QVBoxLayout(None)
        self.whiteLabel = QLabel("WHITE")
        self.whiteLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.whiteLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.whiteLabel.setStyleSheet("QLabel {font-weight: bold; font-size: 13px}")
        self.whitePlayer = QLabel("-")
        self.whitePlayer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.whitePlayer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.whitePhoto = QLabel()
        self.whitePhoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.whitePhoto.setStyleSheet(photoSheet)
        
        whiteLayout.addWidget(self.whiteLabel)
        whiteLayout.addWidget(self.whitePlayer)
        whiteLayout.addWidget(self.whitePhoto)
        vsLabel = QLabel("VS")
        vsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vsLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
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
        dateLayout.setContentsMargins(0, 20, 0, 0)
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



class commentsDock(QDockWidget):
    
    def __init__(self, title, parent):
        super().__init__(title)
        try:
            self.restorGeometry(parent.settingData.commentsDockGeometry)
        except:
            pass
        self.parent = parent
        self.commentsDisplay = commentsDisplay(parent)
        self.setWidget(self.commentsDisplay)
        self.setFloating(False)
        
        self.commentsDisplay.commentsBox.anchorClicked.connect(self.parent.showVariation)
    
class commentsDisplay(QWidget):
        
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        mainLayout = QVBoxLayout(None)
        self.commentsBox = QTextBrowser()
        self.commentsBox.setOpenLinks(False)
        
        buttonLayout = QHBoxLayout(None)
        self.insertVariation = QPushButton("Insert...")
        self.editCommentButton = QPushButton("Edit...")
        self.delVariation = QPushButton("Del...")
        buttonLayout.addWidget(self.editCommentButton)
        buttonLayout.addWidget(self.insertVariation)
        buttonLayout.addWidget(self.delVariation)
        
        mainLayout.addWidget(self.commentsBox)
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)
        self.editCommentButton.clicked.connect(self.showEditCommentsDialog)
        self.insertVariation.clicked.connect(self.showInsertVariation)
        self.delVariation.clicked.connect(self.showDelVariation)
    
    def showDelVariation(self):
        self.parent.statusBar().showMessage("This function is not finished", 5000)
        
    def showEditCommentsDialog(self):
        if not self.checkEditCommentsConditions():
            return
        dialog = editCommentsDialog(self)
        p = self.commentsBox.toHtml()
        p = re.sub("<br /><br /><a href.*</html>", "", p, re.S)
        dialog.commentsBox.setHtml(p)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            b = dialog.commentsBox.toHtml()
            b = b.replace("\n", "").replace("</p></body></html>", "")
            text = re.sub('^<.*?px;">', "", b, re.S)
            text = re.sub('<p.*?px;">', "", text, re.S)
            text = text.replace("</p>", "\n")
            text = text.replace("<br />", "\n")
            for i in faceDict_anti:
                pha = '<img src="res/face/{}" />'.format(i)
                if  pha in text:
                    text = text.replace(pha, faceDict_anti[i])
            self.parent.setComment(text)
            self.parent.showComment()
    
    def showInsertVariation(self):
        if not self.checkInsertVariationConditions():
            return
        variation = self.parent.sgfData.stepsList[self.parent.breakPoint : self.parent.stepPoint]
        text, ok = QInputDialog.getText(None, "Insert variation successfully", "Please input short comments for the variation")
        if ok:
            variation[0].comment = text
            self.parent.sgfData.stepsList[self.parent.breakPoint - 1].variations.append(variation)
            self.parent.statusBar().showMessage("Variation inserted successfully!", 5000)
    
    def checkEditCommentsConditions(self):
        if self.parent.mode == "review":
            if len(self.parent.sgfData.stepsList) != 0:
                return True
            else:
                QMessageBox.information(self, "Can not eidt comments", "There is no stone on board currently")
                return False
        elif self.parent.mode == "free":
            if len(self.parent.sgfData.stepsList) != 0:
                return True
            else:
                QMessageBox.information(self, "Can not eidt comments", "There is no stone on board currently")
                return False
        elif self.parent.mode == "test":
            QMessageBox.information(self, "Can not eidt comments", "Can not edit comments under test mode")
            return False
    
    def checkInsertVariationConditions(self):
        if self.parent.mode == "test":
            if self.parent.stepPoint - self.parent.breakPoint > 0:
                if self.parent.breakPoint == 0:
                    QMessageBox.information(self, "Can not insert variation", "Variation follows sgf mainline steps only")
                    return False
                else:
                    return True
            else:
                QMessageBox.information(self, "Can not insert variation", "There is no variation on board")
                return False
        else:
            QMessageBox.information(self, "Can not insert variation", "This function is available only under test mode")
            return False


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = faceDisplay(None)
	w.show()
	sys.exit(app.exec())
