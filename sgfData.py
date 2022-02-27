#!/bin/use/python


from sgf import sgf


class sgfData:
    
    def __init__(self):
        self.init()
        
    def checkSgf(self, data):
        self.data = data
        gameList = []
        try:
            self.collection = sgf.parse(data)
        except:
            raise
        else:
            for game in self.collection.children:
                title = game.root.properties["GN"][0]
                gameList.append(title)
        return gameList
    
    def parseGame(self, ind = 0):
        self.game = self.collection.children[ind]
        self.head = self.game.root.properties
        self.rest = self.game.rest
        self.size = int(self.head["SZ"][0])
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
        self.countTimes = self.head["TC"][0]
        self.countSeconds = self.head["TT"][0]
        self.stepsList, self.haList = self.parseSteps(self.rest, False)
            
        
    def init(self):
        self.data = ""
        self.stepsList = []
        self.haList = []
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
        stepsList = []
        haList = []
        stepNum = 1
        for i in iterator:
            if "AB" in i.properties:
                for k in i.properties["AB"]:
                    haStep = step(self.toGoCoordinate(k), "black", 0)
                    haList.append(haStep)
                continue
        
            if "B" in i.properties:
                color = "black"
                coordinate = self.toGoCoordinate(i.properties["B"][0])
            elif "W" in i.properties:
                color = "white"
                coordinate = self.toGoCoordinate(i.properties["W"][0])
            oneStep = step(coordinate, color, stepNum, inVariation)
            if "C" in i.properties:
                oneStep.setComment(i.properties["C"][0])
            if len(i.variations) != 0:
                for j in i.variations[1:]:
                    it = self.recursionNode(j, [])
                    s, h = self.parseSteps(it, True)
                    oneStep.variations.append(s)
            stepsList.append(oneStep)
            stepNum += 1
        return stepsList, haList
    
    def recursionNode(self, node, var):
        var.append(node)
        node = node.next
        if node == None:
            return var
        else:
            self.recursionNode(node, var)
        return var
            
    def toGoCoordinate(self, t):
        x = ord(t[0]) - 96
        y = ord(t[1]) - 96
        return (x, y)
                    

class writeSgf:
    
    def __init__(self, fileName):
        self.fileName = fileName
        
    def generateRoot(self, sz, gn, dt, pb, pw, br, wr, km, ha, ru, rs, tm, tc, tt):
        root = "(;GM[1]FF[4]\nSZ[{}]\nGN[{}]\nDT[{}]\nPB[{}]\nPW[{}]\nBR[{}]\nWR[{}]\nKM[{}]HA[{}]RU[{}]RE[{}]TM[{}]TC[{}]TT[{}]AP[foxGo2]RL[0]\n".format(sz, gn, dt, pb, pw, br, wr, km, ha, ru, rs, tm, tc, tt)
        return root
    
    def generateRest(self, stepsList, haList):
        main = self.parseStep(stepsList, True, False)
        ha = self.parseStep(haList, True, True)
        var = ""
        for i in stepsList:
            if i.hasVariation():
                v = ""
                for j in i.getVariations():
                    b = "(" + self.parseStep(j, False) + ")"
                    v += b
                v += ")\n"
                var = v + var
        return ha + main + var
    
    def toFile(self, sgf):
        with open(self.fileName, "w", encoding = "utf8") as f:
            f.write(sgf)
                    
    def parseStep(self, it, isMain, isHa = False):
        b = ""
        
        if isHa:
            if len(it) == 0:
                return b
            else:
                for i in it:
                    coordinate = self.goToSgfCoordinate(i.getCoordinate())
                    pha = "[{}]".format(coordinate)
                    b += pha
                b = ";AB" + b + "\n"
            
        else:
            if isMain:
                bre = "\n"
            else:
                bre = ""
            for i in it:
                if i.getColor() == "black":
                    c = "B"
                else:
                    c = "W"
                coordinate = self.goToSgfCoordinate(i.getCoordinate())
                if i.hasComment():
                    pha = ";{}[{}]C[{}]{}".format(c, coordinate, i.getComment(), bre)
                else:
                    pha = ";{}[{}]{}".format(c, coordinate, bre)
                if i.hasVariation():
                    pha += "("
                b += pha
            if isMain:
                b += ")"
        return b
    
    def goToSgfCoordinate(self, tu):
        chx = chr(tu[0] + 96)
        chy = chr(tu[1] + 96)
        return chx + chy


class step:
    
    def __init__(self, coordinate, color, stepNum, inVariation = False):
        self.color = color
        self.coordinate = coordinate
        self.stepNum = stepNum
        self.comment = ""
        self.variations = []
        self.inVariation = inVariation
    
    def getStepNum(self):
        return self.stepNum
    
    def setStepNum(self, n):
        self.stepNum = n
    
    def getCoordinate(self):
        return self.coordinate
    
    def setCoordinate(self, tu):
        self.coordinate = tu
    
    def getCoordinateX(self):
        return self.coordinate[0]
    
    def getCoordinateY(self):
        return self.coordinate[1]
    
    def isInVariation(self):
        return self.inVariation
    
    def setInVariation(self, b):
        self.inVariation = b
    
    def getVariations(self):
        return self.variations
    
    def hasVariation(self):
        if len(self.variations) >= 1:
            return True
        else:
            return False
    
    def getComment(self):
        return self.comment
    
    def hasComment(self):
        if self.comment != "":
            return True
        else:
            return False
    
    def setComment(self, m):
        self.comment = m
    
    def getColor(self):
        return self.color
    
    def setColor(self, c):
        self.color = c
