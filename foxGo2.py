#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: foxGo2.py

from PyQt5.QtWidgets import QApplication, QMessageBox
from mainWindow import mainWindow
import sys, os



if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    if os.path.exists("lockFile"):
        QMessageBox.information(None, "Notice", "Only one foxGo2 instance allowed running at once!")
        sys.exit()
    else:
        #f = open("lockFile", 'w')
        #f.close()
        w = mainWindow()
        w.show()
        sys.exit(app.exec_())
