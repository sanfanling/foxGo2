#! /usr/bin/python

import sys, os
from PyQt5.QtCore import *
from getHeader import getHeader
import requests


class getHeaderThread(QThread):
    
    missionDone = pyqtSignal()
    
    def __init__(self):
        super().__init__()
    
    def setArgs(self, nameList):
        self.nameList = nameList
    
    def run(self):
        for i in self.nameList:
            if os.path.exists(f"headers/{i}.jpg"):
                continue
            else:
                p = getHeader(i)
                url = p.get()
                if url != None:
                    req = requests.get(url)
                    header = req.content
                    req.close()
                    with open(f"headers/{p.fileName}.jpg", "wb") as f:
                        f.write(header)
        self.missionDone.emit()
