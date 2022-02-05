#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: foxGo2.py

from PyQt5.QtWidgets import QApplication
from mainWindow import mainWindow
import sys, os



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = mainWindow()
	w.show()
	sys.exit(app.exec_())
