#!/bin/use/python

import sgf


class sgfData:
    
    def __init__(self):
        self.init()
    
    def parse(self, data):
        collection = sgf.parse(data)
        self.game = collection.children[0]
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
        self.stepsList, self.haList = self.getStepsData(self.rest)
        
    def init(self):
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
    
    def getStepsData(self, iterator):
        stepsList = []
        haList = []
        j = 0
        for i in iterator:
            if "AB" in i.properties:
                haList = self.getHaData(i.properties["AB"])
                continue
            
            j += 1
            if "B" in i.properties:
                goColor = "black"
                xname = i.properties["B"][0][0]
                yname = i.properties["B"][0][1]
            elif "W" in i.properties:
                goColor = "white"
                xname = i.properties["W"][0][0]
                yname = i.properties["W"][0][1]
            x = ord(xname)-96
            y = ord(yname)-96
            stepsList.append((j, goColor, x, y))
        return stepsList, haList
    
    def getHaData(self, hal):
        dl = []
        for i in hal:
            xname = i[0]
            yname = i[1]
            x = ord(xname)-96
            y = ord(yname)-96
            dl.append((x, y))
        return dl
    

    def getCommentsData(self, iterator, variationComment = False):
        commentDict = {}
        comment = ""
        j = 0
        for i in iterator:
            if "AB" in i.properties:
                continue
            j += 1
            if "C" in i.properties:
                comment = i.properties["C"][0]
                commentDict[j] = comment
        if not variationComment:
            return commentDict
        else:
            return comment
    
    def getVariations(self):
        p = 0
        variationDict = {}
        for i in self.rest:
            if "AB" in i.properties:
                continue
            p += 1
            if len(i.variations) != 0:
                variationList = []
                for j in i.variations[1:]:
                    v = self.recursionNode(j, [], 0)
                    subList = self.getStepsData(v)[0]
                    subComment = self.getCommentsData(v, True)
                    subList.append(subComment)
                    variationList.append(subList)
                variationDict[p] = variationList
        return variationDict

    def recursionNode(self, node, var, k):
        k += 1
        var.append(node)
        #var.append([k, self.getColor, self.getx, self.gety])
        node = node.next
        if node == None:
            return var
        else:
            self.recursionNode(node, var, k)
        return var


if __name__ == "__main__":
    with open("2.sgf", "r") as f:
        d = f.read()
    a = sgfData()
    a.parse(d)
    print(a.getCommentsData(a.rest))
    print(a.getVariations())
    
