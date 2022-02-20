#!/usr/bin/python
# -*- coding: utf-8 -*-
#File name: settingData.py
#Author: sanfanling
#licence: GPL-V3


from PyQt5.QtCore import QSettings


class settingData:
    
    def __init__(self):
        self.iniFile = QSettings("./.foxGo2.ini", QSettings.IniFormat)
        
        self.sgfPath = self.iniFile.value("/common/sgfpath", ".")
        self.backgroundMusic = self.stringToBool(self.iniFile.value("/common/backgroundmusic", False))
        self.musicPath = self.iniFile.value("/common/musicpath", "./res/sounds/gsls.wav")
        self.effectSounds = self.stringToBool(self.iniFile.value("/common/effectsounds", False))
        self.autoSkip = self.stringToBool(self.iniFile.value("/common/autoskip", True))
        self.autoReviewInterval = int(self.iniFile.value("/common/autoreviewinterval", 1))
        
        self.boardSize = int(self.iniFile.value("/board/boardsize", 19))
        self.withCoordinate = self.stringToBool(self.iniFile.value("/board/withcoordinate", True))
        self.stepsNumber = self.iniFile.value("/board/stepsnumber", "hide")
        self.boardStyle = self.iniFile.value("/board/boardstyle", "style2")
        self.hideCursor = self.stringToBool(self.iniFile.value("/board/hidecursor", False))
        
        self.windowState = self.iniFile.value("/session/windowstate/", "")
        self.windowGeometry = self.iniFile.value("/session/windowgeometry", "")
        self.infoDockGeometry = self.iniFile.value("/session/infodockgeometry", "")
        self.controlDockGeometry = self.iniFile.value("/session/controldockgeometry", "")
        self.consoleDockGeometry = self.iniFile.value("/session/consoledockgeometry", "")
        self.sgfExplorerDockGeometry = self.iniFile.value("s/ession/sgfexplorerdockgeometry", "")
        self.recentGamesDockGeometry = self.iniFile.value("/session/recentgamesdockgeometry", "")
        self.recentGamesDockTableState = self.iniFile.value("/session/recentgamesdocktablestate", "")
        
        self.previousToStart = self.iniFile.value("/shortcuts/previoustostart")
        self.previous10Steps = self.iniFile.value("/shortcuts/previous10Steps")
        self.previousStep = self.iniFile.value("/shortcuts/previousstep")
        self.nextStep = self.iniFile.value("/shortcuts/nextstep")
        self.next10Steps = self.iniFile.value("/shortcuts/next10steps")
        self.nextToEnd = self.iniFile.value("/shortcuts/nexttoend")
        self.back = self.iniFile.value("/shortcuts/back")
    
    def stringToBool(self, s):
        if type(s) == bool:
            return s
        else:
            if s.lower() == "false":
                return False
            else:
                return True
    
    def saveIniFile(self):
        self.iniFile.setValue("/common/sgfpath", self.sgfPath)
        self.iniFile.setValue("/common/backgroundmusic", self.backgroundMusic)
        self.iniFile.setValue("/common/musicpath", self.musicPath)
        self.iniFile.setValue("/common/effectsounds", self.effectSounds)
        self.iniFile.setValue("/common/autoskip", self.autoSkip)
        self.iniFile.setValue("/common/autoreviewinterval", self.autoReviewInterval)
        
        self.iniFile.setValue("/board/boardsize", self.boardSize)
        self.iniFile.setValue("/board/withcoordinate", self.withCoordinate)
        self.iniFile.setValue("/board/stepsnumber", self.stepsNumber)
        self.iniFile.setValue("/board/boardstyle", self.boardStyle)
        self.iniFile.setValue("/board/hidecursor", self.hideCursor)
        
        self.iniFile.setValue("/session/windowstate", self.windowState)
        self.iniFile.setValue("/session/windowgeometry", self.windowGeometry)
        self.iniFile.setValue("/session/infodockgeometry", self.infoDockGeometry)
        self.iniFile.setValue("/session/controldockgeometry", self.controlDockGeometry)
        self.iniFile.setValue("/session/consoledockgeometry", self.consoleDockGeometry)
        self.iniFile.setValue("/session/sgfexplorerdockgeometry", self.sgfExplorerDockGeometry)
        self.iniFile.setValue("/session/recentgamesdockgeometry", self.recentGamesDockGeometry)
        self.iniFile.setValue("/session/recentgamesdocktablestate", self.recentGamesDockTableState)
        
        self.iniFile.setValue("/shortcuts/previoustostart", self.previousToStart)
        self.iniFile.setValue("/shortcuts/previous10Steps", self.previous10Steps)
        self.iniFile.setValue("/shortcuts/previousstep", self.previousStep)
        self.iniFile.setValue("/shortcuts/nextstep", self.nextStep)
        self.iniFile.setValue("/shortcuts/next10steps", self.next10Steps)
        self.iniFile.setValue("/shortcuts/nexttoend", self.nextToEnd)
        self.iniFile.setValue("/shortcuts/back", self.back)
        
        


if __name__ == "__main__":
    a = settingData()
