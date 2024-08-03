#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: otherDialog.py  

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys, os


class rootDialog(QDialog):
    
    def __init__(self, parent = None):
        super().__init__()
        self.setWindowTitle("Set root info of sgf")
        self.setWindowIcon(QIcon("res/pictures/logo.png"))
        mainLayout = QVBoxLayout(None)
        
        self.playerInfoBox = playerInfoBox(parent)
        self.gameInfoBox = gameInfoBox(parent)
        
        buttonBox = QDialogButtonBox(self)
        cancelButton = QPushButton("Cancel")
        okButton = QPushButton("OK")
        buttonBox.addButton(cancelButton, QDialogButtonBox.ButtonRole.RejectRole)
        buttonBox.addButton(okButton, QDialogButtonBox.ButtonRole.AcceptRole)
        
        mainLayout.addWidget(self.playerInfoBox)
        mainLayout.addWidget(self.gameInfoBox)
        mainLayout.addWidget(buttonBox)
        
        self.setLayout(mainLayout)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def sizeHint(self):
        return QSize(400, 400)
 
 
class playerInfoBox(QGroupBox):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setTitle("Player info")
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        mainLayout = QFormLayout(None)
        
        self.pbLine = QLineEdit()
        self.brLine = QLineEdit()
        
        self.pwLine = QLineEdit()
        self.wrLine = QLineEdit()
        
        mainLayout.addRow("Black player:", self.pbLine)
        mainLayout.addRow("Black level:", self.brLine)
        mainLayout.addRow("White player:", self.pwLine)
        mainLayout.addRow("White level:", self.wrLine)
        
        self.setLayout(mainLayout)
        
        
        
#root = "(;GM[1]FF[4]\nSZ[19]\nGN[bb]\nDT[2022-2-2]\nPB[cc]\nPW[dd]\nBR[9]\nWR[9]\nKM[650]HA[0]RU[J]RE[W+0.5]TM[1000]TC[5]TT[60]AP[foxGo2]RL[0]\n"         
class gameInfoBox(QGroupBox):
    
    def __init__(self, parent = None):
        super().__init__()
        self.parent = parent
        self.setTitle("Game info")
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        
        mainLayout = QFormLayout(None)
        
        self.gnLine = QLineEdit()
        self.dtLine = QDateEdit()
        self.dtLine.setDisplayFormat("yyyy-MM-dd")
        self.dtLine.setCalendarPopup(True)
        self.kmLine = QLineEdit()
        self.haLine = QSpinBox()
        self.haLine.setMinimum(0)
        self.haLine.setMaximum(9)
        self.ruLine = QComboBox()
        self.ruLine.addItems(["Chinese", "Japanese", "Ying's", "Others"])
        self.rsLine = QLineEdit()
        self.tmLine = QLineEdit()
        self.tcLine = QSpinBox()
        self.ttLine = QLineEdit()
        
        mainLayout.addRow("Game name:", self.gnLine)
        mainLayout.addRow("Date:", self.dtLine)
        mainLayout.addRow("Komi:", self.kmLine)
        mainLayout.addRow("HA:", self.haLine)
        mainLayout.addRow("Rule:", self.ruLine)
        mainLayout.addRow("Result:", self.rsLine)
        mainLayout.addRow("Time limit:", self.tmLine)
        mainLayout.addRow("Count times:", self.tcLine)
        mainLayout.addRow("Count seconds:", self.ttLine)
        
        self.setLayout(mainLayout)





if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = editCommentsDialog()
	w.show()
	sys.exit(app.exec())
