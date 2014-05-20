#World
#Modular RL Project
#Ruohan Zhang
#Define maze world with reward and obstacles

#imports
import random
import math
import copy as py_copy
from config import *
#Domain: Maze
#Enums for objects in the maze
Obstacle = 256
Reward = 255
Empty = 254

class Maze:
    def __init__(self,rows,columns, mazeType, objPos = [0,0]):
        self.rows = py_copy.deepcopy(rows)
        self.columns = py_copy.deepcopy(columns)
        self.rewards = []#stores positions of rewards
        self.obstacles = []#stores positions of obstacles
        self.objectPos = py_copy.deepcopy(objPos)
 
        #represent maze map as a 2D array
        self.mazeMap = [[0 for x in range(columns)] for x in range(rows)]
        for i in range(rows):
            for j in range(columns):
                self.mazeMap[i][j] = Empty
        if (mazeType == 'reward'):#generate a maze with single reward
            self.mazeMap[self.objectPos[0]][self.objectPos[1]] = Reward
            self.rewards.append(self.objectPos)
        if (mazeType == 'obstacle'):#generate a maze with single obstacle
            self.mazeMap[self.objectPos[0]][self.objectPos[1]] = Obstacle
            self.obstacles.append(self.objectPos)
        if (mazeType == 'test'):#generate a random map
            for i in range(rows):
               for j in range(columns):
                    if (random.random() <= pReward):
                        self.mazeMap[i][j] = Reward
                        self.rewards.append([i,j])
                    elif (random.random() <= pObstacle):
                        self.mazeMap[i][j] = Obstacle
                        self.obstacles.append([i,j])
	
	#This map records agent path
	self.pathMap = py_copy.deepcopy(self.mazeMap)
	#This map keeps a backup of original map
	self.originalMap = py_copy.deepcopy(self.mazeMap)

    def printMap(self, mapRequest):
	if (mapRequest == 'original'):
	    print('This is original map')
	    mapToPrint = self.originalMap
	if (mapRequest == 'path'):
	    print('This is navigation path')
	    mapToPrint = self.pathMap
	if (mapRequest == 'maze'):
	    print('This is map after reward collection')
	    mapToPrint = self.mazeMap
        index = ' '
        for j in range(self.columns):
            index = index + ('%3s' % j)
        print(index)
        for i in range(self.rows):
            rowString = str(i)
            for j in range(self.columns):
                mark = ''
                if (mapToPrint[i][j] == Reward):
                    mark = '$'#reward
                elif (mapToPrint[i][j] == Empty):
                    mark = '-'#empty
                elif (mapToPrint[i][j] == Obstacle):
                    mark = '@'#obstacle
		elif (mapToPrint[i][j] == Up):
                    mark = '^'
                elif (mapToPrint[i][j] == Down):
                    mark = 'v'
                elif (mapToPrint[i][j] == Left):
                    mark = '<'
                elif (mapToPrint[i][j] == Right):
                    mark = '>'
                rowString =  rowString + ('%3s' % mark)
            print(rowString)

    #given agent position, calulate agent reward, if agent collects reward, remove it from mazeMap
    #No need to deal with pathMap, since action will overwrite 
    def calc_reward(self,agentPos):
        if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Reward):
	    #These 2 lines removes rewards
	    if (agentPos in self.rewards): self.rewards.remove(agentPos)
	    self.mazeMap[agentPos[ROW]][agentPos[COL]] = Empty
	    return R_REWARD
	if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Obstacle):
	    return R_OBSTACLE
	if (self.mazeMap[agentPos[ROW]][agentPos[COL]] == Empty):
	    return R_EMPTY
    
    #Given agent position and action, record it in the pathMap
    def recordAction(self,agentPos,action):
        self.pathMap[agentPos[ROW]][agentPos[COL]] = action


#Find nearby objects
def findNearbyObj(objType, agentPos, agentVRange, maze):
    visibleRange = agentPos[0]
    objList = []
    if (objType == 'reward'):
        for i in range(len(maze.rewards)):
            curRewardPos = maze.rewards[i]
            rowDist = abs(agentPos[0] - curRewardPos[0])
            colDist = abs(agentPos[1] - curRewardPos[1])
            if (rowDist <= agentVRange and colDist <=agentVRange):
                obj = py_copy.deepcopy(curRewardPos)
                objList.append(obj)

    if (objType == 'obstacle'):
        for i in range(len(maze.obstacles)):
            curRewardPos = maze.obstacles[i]
            rowDist = abs(agentPos[0] - curRewardPos[0])
            colDist = abs(agentPos[1] - curRewardPos[1])
            if (rowDist <= agentVRange and colDist <=agentVRange):
                obj = py_copy.deepcopy(curRewardPos)
                objList.append(obj)            

    return objList
