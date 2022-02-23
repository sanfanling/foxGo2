#!/usr/bin/python


class go:
    
    def __init__(self, parent = None):
        self.parent = parent
    
    def init(self, boardSize = 19):
        self.boardSize = boardSize
        self.stepsGoDict = {} #records any existed chesses on board, with chess color info, can append and remove step
        self.shapeSet = set()
        self.haDict = {} # records the steps of ha
        self.shapeList = [] # for checking the rule of global same shape forbidden, ko is a subset of this rule
        self.stepNum = 0
        self.goColor = "black"
        self.stepInKo = False
        self.x = 0
        self.y = 0
    
    def getHaSteps(self, haList):
        for i in haList:
            #self.haDict[i] = ("black", 0)
            c = i.getCoordinate()
            self.haDict[c] = ("black", 0)
        
    # this function is called in review mode, usually, every step in review mode is legal move
    def makeStepSafe(self):
        deadList = self.checkEnemyBlockBreath(self.x, self.y, dict(self.stepsGoDict), self.goColor)
        deadListLen = len(deadList)
        if deadListLen == 0:
            self.stepsGoDict[(self.x, self.y)] = (self.goColor, self.stepNum)
            #self.endStepSuccess(False)
            return (1, 0)
        else:
            self.stepsGoDict[(self.x, self.y)] = (self.goColor, self.stepNum)
            chess = self.eatChess(deadList)
            #self.endStepSuccess(False)
            return (2, chess)
    
    def makeStepPass(self):
        self.changeColor()
        
    # check every step
    def makeStep(self):
        if (self.x, self.y) not in self.stepsGoDict.keys():
            haveBreath = self.checkBlockBreath(dict(self.stepsGoDict), self.goColor, self.getBlock(self.x, self.y, dict(self.stepsGoDict), self.goColor, []), True, self.x, self.y)
            deadList = self.checkEnemyBlockBreath(self.x, self.y, dict(self.stepsGoDict), self.goColor)
            deadListLen = len(deadList)
            if haveBreath and deadListLen == 0:
                m = "has liberty, legal move!"
                self.printMessage(m)
                self.stepInKo = False
                self.stepSuccess()
                self.endStepSuccess(self.stepInKo)
                #self.changeColor()
                return (1, 0)
            elif haveBreath and deadListLen != 0:
                m = "has liberty, legal move, take!"
                self.printMessage(m)
                #print(deadList)
                self.stepInKo = False
                self.stepSuccess()
                chess = self.eatChess(deadList)
                self.endStepSuccess(self.stepInKo)
                #self.changeColor()
                return (2, chess)
            elif not haveBreath and deadListLen == 0:
                m = "no libery, no take, illegal move!"
                self.printMessage(m)
                return (0, 0)
            elif not haveBreath and deadListLen != 0:
                l, t = self.checkKo(deadList)
                if not l:
                    m = "no liberty，but legal move, take!"
                    self.printMessage(m)
                    self.stepSuccess()
                    chess = self.eatChess(deadList)
                    self.endStepSuccess(self.stepInKo)
                    #self.changeColor()
                    return (2, chess)
                else:
                    if t == 1:
                        m = "it's a ko, illegal move!"
                    elif t == 2:
                        m = "it's a triple-circle ko, illegal move! Advise: draw game!"
                    else:
                        m = "it's a miracle ko, illegal move! Advise: draw game!"
                    self.printMessage(m)
                    return (0, 0)
        
        else:
            m = "position has been taken, can not move here"
            self.printMessage(m)
            return (0, 0)

    def stepSuccess(self):
        self.stepNum += 1
        self.stepsGoDict[(self.x, self.y)] = (self.goColor, self.stepNum)
        self.shapeSet.add("{},{},{}".format(self.x, self.y, self.goColor))
        
    
    def endStepSuccess(self, stepInKo):
        v = self.shapeSet.copy()
        if not stepInKo:
            del self.shapeList[:-1]
        self.shapeList.append(v)
    
    def changeColor(self):
        if self.goColor == "black":
            self.goColor = "white"
        else:
            self.goColor = "black"
    
    def eatChess(self, deadChessList):
        p = 0
        for j in deadChessList:
            x, y = j
            c = self.stepsGoDict[j][0]
            self.shapeSet.discard("{},{},{}".format(x, y, c))
            del self.stepsGoDict[j]
            
            p += 1
        
        return p
            
    def checkKo(self, deadList):
        if len(deadList) != 1:
            self.stepInKo = False
            return False, 0
        else:
            tmp = self.shapeSet.copy()
            tmp.add("{},{},{}".format(self.x, self.y, self.goColor))
            x, y = deadList[0]
            c = self.stepsGoDict[deadList[0]][0]
            tmp.discard("{},{},{}".format(x, y, c))
            if tmp in self.shapeList:
                if tmp == self.shapeList[-2]:
                    return True, 1
                elif tmp == self.shapeList[-6]:
                    return True, 2
                else:
                    return True, 3
            else:
                self.stepInKo = True
                return False, 0
    
    def printMessage(self, m):
        if __name__ == "main":
            print("[{}] {}".format(__name__, m))
        else:
            self.parent.consoleDock.consoleDisplay.addOutput(__name__, m)
                
    
    def getBlock(self, x, y, tmpDict, goColor, blockList = []):
        #print("getBlock: 正在搜寻%d,%d周边本方子，并计入块列表" %(x,y))
        blockList.append((x, y))
        tmpDict[(x, y)] = ("blabla", 0)
        #print("getBlock: 将本身设置为中性色")
        for offsetx, offsety in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            try:
                logic = tmpDict[(x+offsetx, y+offsety)][0] == goColor
            except:
                logic = False
            if 0 < x+offsetx < self.boardSize + 1 and 0 < y+offsety < self.boardSize + 1 and logic:
                #print("getBlock: 有子联通")
                self.getBlock(x+offsetx, y+offsety, tmpDict, goColor, blockList)
        #print("getBlock: ")
        #print(blockList)
        return blockList
    
    def checkBlockBreath(self, tmpDict, goColor, blockList, checkMyBlock = True, a = 0, b = 0):
        if checkMyBlock:
            tmpDict[(a, b)] = ("blabla", 0)
        for (x, y) in blockList:
            for offsetx, offsety in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                #print("checkBlockBreath: 正在查找块中%s,%s的气" %(x, y))
                if 0 < x+offsetx < self.boardSize + 1 and 0 < y+offsety < self.boardSize + 1 and (x+offsetx, y+offsety) not in tmpDict.keys():
                    #print("checkBlockBreath: 整块本身有气")
                    return True
        #print("checkBlockBreath: 整块没有气！！")
        return False
    
    def checkEnemyBlockBreath(self, x, y, tmpDict, goColor):
        deadChess = []
        #print("checkEnemyBlockBreath: 无论本身有无气，假定可落子，并设为中性色，开始查找周边敌子的气")
        tmpDict[(x,y)] = ("blabla", 0)
        for offsetx, offsety in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x+offsetx, y+offsety) not in tmpDict.keys() or tmpDict[(x+offsetx, y+offsety)][0] == goColor:
                #print("checkEnemyBlockBreath: 此区块无子，或是本方子，或是边界，跳过")
                continue
            else:
                if goColor == "white":
                    t = "black"
                else:
                    t = "white"
                #print("checkEnemyBlockBreath: 查找敌子区块(%d,%d)" %(x+offsetx, y+offsety))
                expr = 'self.getBlock(x+offsetx, y+offsety, dict(self.stepsGoDict), "%s", [])' %(t,)
                blockList = eval(expr)
                #print("checkEnemyBlockBreath: 敌子区块")
                #print(blockList)
                if self.checkBlockBreath(dict(tmpDict), t, blockList): 
                    #print("checkEnemyBlockBreath: 此区块敌子有气！跳过")
                    continue
                else:
                    #print("checkEnemyBlockBreath: 此区块敌子有死棋！死棋块计入列表")
                    for j in blockList:
                        if j not in deadChess:
                            deadChess.append(j)
                        else:
                            break
        return deadChess
