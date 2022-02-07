#!/bin/use/python


import sgf


class sgfDataNew:
    
    def __init__(self):
        self.init()
        
    def checkSgf(self, data):
        gameList = []
        self.collection = sgf.parse(data)
        for game in self.collection.children:
            title = game.root.properties["GN"][0]
            gameList.append(title)
        return gameList
    
    def parseGame(self, ind = 0):
        self.game = self.collection.children[ind]
        self.head = self.game.root.properties
        self.rest = self.game.rest
        self.title = self.head["GN"][0]
        self.blackPlayer = self.head["PB"][0]
        self.whitePlayer = self.head["PW"][0]
        self.date = self.head["DT"][0]
        self.result = self.head["RE"][0]
        self.komi = str(int(self.head["KM"][0])/100)
        self.blackPlayerLevel = self.head["BR"][0]
        self.whitePlayerLevel = self.head["WR"][0]
        self.rule = self.head["RU"][0]
        self.ha = self.head["HA"][0]
        self.timeLimit = self.head["TM"][0]
        self.stepsMap = self.parseSteps(self.rest, False)
        self.haMap = self.parseHaSteps(self.rest)
        self.stepsList = self.parseStepsMap(self.stepsMap, False)
        self.haList = self.parseStepsMap(self.haMap, True)
            
        
    def init(self):
        self.stepsList = []
        self.haList = []
        self.stepsMap = []
        self.haMap = []
        self.title = "-"
        self.blackPlayer = "-"
        self.whitePlayer = "-"
        self.date = "-"
        self.result = "-"
        self.komi = "-"
        self.blackPlayerLevel = ""
        self.whitePlayerLevel = ""
        self.rule = "-"
        self.ha = "-"
        self.timeLimit = "-"
    
    def parseSteps(self, iterator, inVariation = False):
        stepsMap = []
        for i in iterator:
            if "AB" in i.properties:
                continue
            oneStep = step(inVariation)
            if "B" in i.properties:
                oneStep.color = "black"
                oneStep.coordinate = i.properties["B"][0]
            elif "W" in i.properties:
                oneStep.color = "white"
                oneStep.coordinate = i.properties["W"][0]
            if "C" in i.properties:
                oneStep.comment = i.properties["C"][0]
            if len(i.variations) != 0:
                for j in i.variations[1:]:
                    it = self.recursionNode(j, [])
                    oneStep.variations.append(self.parseSteps(it, True))
            stepsMap.append(oneStep)
        return stepsMap
    
    def parseHaSteps(self, iterator):
        haMap = []
        for i in iterator:
            if "AB" in i.properties:
                for j in i.properties["AB"]:
                    haStep = step(False)
                    haStep.color = "black"
                    haStep.coordinate = j
                    haMap.append(haStep)
        return haMap
    
    def parseStepsMap(self, stepsMap, isHaMap = False):
        stepNum = 1
        stepsList = []
        for i in stepsMap:
            x = ord(i.coordinate[0]) - 96
            y = ord(i.coordinate[1]) - 96
            if not isHaMap:
                stepsList.append((stepNum, i.color, x, y))
            else:
                stepsList.append((x, y))
            stepNum += 1
        return stepsList
    
    def recursionNode(self, node, var):
        var.append(node)
        #var.append([k, self.getColor, self.getx, self.gety])
        node = node.next
        if node == None:
            return var
        else:
            self.recursionNode(node, var)
        return var
            
                    
        

class step:
    
    def __init__(self, inVariation):
        self.color = None
        self.coordinate = None
        self.comment = None
        self.variations = []
        self.inVariation = inVariation
