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
    def __init__(self,rows,columns, mazeType, pObstacle = 0.0, pReward = 0.0):
        self.rows = rows
        self.columns = columns
        self.rewardPos = [0,0]
        self.obstaclePos = [0,0]
        self.numReward = 0
        self.numObstacle = 0
        self.rewards = []#stores positions of rewards
        self.obstacles = []#stores positions of obstacles
        
        #represent maze map as a 2D array
        self.map = [[0 for x in range(columns)] for x in range(rows)]
        for i in range(rows):
            for j in range(columns):
                self.map[i][j] = Empty
        if (mazeType == 'reward'):#generate a maze with single reward
            pos = [random.randint(0,self.rows - 1),random.randint(0,self.columns - 1)]
            self.map[pos[0]][pos[1]] = Reward
            self.rewardPos = pos
        if (mazeType == 'obstacle'):#generate a maze with single obstacle
            pos = [random.randint(0,self.rows - 1),random.randint(0,self.columns - 1)]
            self.map[pos[0]][pos[1]] = Obstacle
            self.obstaclePos = pos
        if (mazeType == 'test'):#generate a random map
            for i in range(rows):
               for j in range(columns):
                    if (random.random() <= pReward):
                        self.map[i][j] = Reward
                        self.numReward += 1
                        self.rewards.append([i,j])
                    elif (random.random() <= pObstacle):
                        self.map[i][j] = Obstacle
                        self.numObstacle += 1
                        self.obstacles.append([i,j])

    def printMap(self):
        index = ' '
        for j in range(self.columns):
            index = index + ('%3s' % j)
        print(index)
        for i in range(self.rows):
            rowString = str(i)
            for j in range(self.columns):
                mark = ''
                if (self.map[i][j] == Reward):
                    mark = '$'#reward
                if (self.map[i][j] == Empty):
                    mark = '-'#empty
                if (self.map[i][j] == Obstacle):
                    mark = '@'#obstacle
                if (self.map[i][j] == Up):
                    mark = '^'
                if (self.map[i][j] == Down):
                    mark = 'v'
                if (self.map[i][j] == Left):
                    mark = '<'
                if (self.map[i][j] == Right):
                    mark = '>'
                rowString =  rowString + ('%3s' % mark)
            print(rowString)

    #given agent position, calulate agent reward
    def calc_reward(self,agentPos):
        if (self.map[agentPos[ROW]][agentPos[COL]] == Reward):
	    return R_REWARD
	if (self.map[agentPos[ROW]][agentPos[COL]] == Obstacle):
	    return R_OBSTACLE
	if (self.map[agentPos[ROW]][agentPos[COL]] == Empty):
	    return R_EMPTY
    
    #Given agent position and action, record it in the map
    def recordAction(self,agentPos,action):
        self.map[agentPos[ROW]][agentPos[COL]] = action

    #update map, remove reward, if agent collect this
    def updateMap(self,agentPos):
        if (self.map[agentPos[ROW]][agentPos[COL]] == Reward):
	    self.map[agentPos[ROW]][agentPos[COL]] = Empty



#Find nearby objects
def findNearbyObj(objType, agentPos, agentVRange, maze):
    visibleRange = agentPos[0]
    objList = []
    if (objType == 'reward'):
        for i in range(maze.numReward):
            curRewardPos = maze.rewards[i]
            rowDist = abs(agentPos[0] - curRewardPos[0])
            colDist = abs(agentPos[1] - curRewardPos[1])
            if (rowDist <= agentVRange and colDist <=agentVRange):
                obj = py_copy.deepcopy(curRewardPos)
                objList.append(obj)

    if (objType == 'obstacle'):
        for i in range(maze.numObstacle):
            curRewardPos = maze.obstacles[i]
            rowDist = abs(agentPos[0] - curRewardPos[0])
            colDist = abs(agentPos[1] - curRewardPos[1])
            if (rowDist <= agentVRange and colDist <=agentVRange):
                obj = py_copy.deepcopy(curRewardPos)
                objList.append(obj)            

    return objList
