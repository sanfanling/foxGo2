#! /usr/bin/python

import sys
from PyQt5.QtCore import *
from parseFoxGo import parseFoxGo



class getCatalogThread(QThread):
    
    missionDone = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        f = parseFoxGo()
        catalog = f.getCatalog()
        self.missionDone.emit(catalog)

class getSgfThread(QThread):
    
    missionDone = pyqtSignal(str)
    
    def __init__(self, key):
        super().__init__()
        self.key = key
    
    def run(self):
        f = parseFoxGo()
        sgf = f.getSgf(self.key)
        self.missionDone.emit(sgf)
    
