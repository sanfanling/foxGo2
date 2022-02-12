#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: settingData.py
#Author: sanfanling
#licence: GPL-V3


from PyQt5.QtCore import QSettings


class settingData:
    
    def __init__(self):
        self.iniFile = QSettings("./.foxGo2.ini", QSettings.IniFormat)
        
        self.sgfPath = self.iniFile.value("general/sgfpath", ".")
        self.backgroundMusic = bool(self.iniFile.value("general/backgroundmusic", False))
        self.musicPath = self.iniFile.value("general/musicpath", "./res/sounds/gsls.wav")
        self.effectSounds = bool(self.iniFile.value("general/effectsounds", False))
        self.autoSkip = bool(self.iniFile.value("general/autoskip", True))
        self.withCoordinate = bool(self.iniFile.value("board/withcoordinate", True))
        self.stepsNumber = self.iniFile.value("board/stepsnumber", "hide")
        self.boardStyle = self.iniFile.value("board/boardstyle", "style2")
        self.hideCursor = bool(self.iniFile.value("board/hidecursor", False))
        self.windowState = self.iniFile.value("session/windowstate/", "")
        self.windowGeometry = self.iniFile.value("session/windowgeometry", "")
    
    def saveIniFile(self):
        self.iniFile.setValue("general/sgfpath", self.sgfPath)
        self.iniFile.setValue("general/backgroundmusic", self.backgroundMusic)
        self.iniFile.setValue("general/musicpath", self.musicPath)
        self.iniFile.setValue("general/effectsounds", self.effectSounds)
        self.iniFile.setValue("general/autoskip", self.autoSkip)
        self.iniFile.setValue("board/withcoordinate", self.withCoordinate)
        self.iniFile.setValue("board/stepsnumber", self.stepsNumber)
        self.iniFile.setValue("board/boardstyle", self.boardStyle)
        self.iniFile.setValue("board/hidecursor", self.hideCursor)
        self.iniFile.setValue("session/windowstate", self.windowState)
        self.iniFile.setValue("session/windowgeometry", self.windowGeometry)


if __name__ == "__main__":
    a = settingData()
