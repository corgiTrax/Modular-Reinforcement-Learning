#Module training and agent
#Modular RL Project
#Ruohan Zhang
#Modular RL Algorithm

#The idea is to have one Qtable for one type (same object with same reward)
#and one active module for one object

#In very large evironment, agent may have too many active modules
#May introduce 'vision range', i.e., agent can only sense
#limited number of objects.

import mathtool
import world
import random
import copy as py_copy
import numpy
import math
import graphics as graph
from config import *

#Now we do not decompose actions, same actions are used globally

#Agent class
class Agent:
    def __init__(self,initPos):
        self.pos = py_copy.deepcopy(initPos)
        self.cumReward = 0

    def setPos(self, position):
        self.pos = position
        
    def move(self, action, maze):
        if (action == Up):self.pos[0] -=1
        if (action == Down):self.pos[0] +=1
        if (action == Left):self.pos[1] -=1
        if (action == Right):self.pos[1] +=1
        if (self.pos[0] >= maze.rows):self.pos[0] = maze.rows - 1;
        if (self.pos[0] < 0):self.pos[0] = 0;
        if (self.pos[1] >= maze.columns):self.pos[1] = maze.columns - 1;        
        if (self.pos[1] < 0):self.pos[1] = 0;

    def drawSelf(self, window, isnew):
        if (isnew == True):
            self.agentPic = graph.Circle(graph.Point((self.pos[COL] + 0.5) * CELL_SIZE, (self.pos[ROW] + 0.5) * CELL_SIZE), CELL_SIZE/6)
            self.agentPic.setFill('red')
            self.agentPic.draw(window)
        else:
            #window.getMouse()
            dx = -self.agentPic.getCenter().getX() + (self.pos[COL] + 0.5) * CELL_SIZE
            dy = -self.agentPic.getCenter().getY() + (self.pos[ROW] + 0.5) * CELL_SIZE
            self.agentPic.move(dx,dy)
    
    
#Module 1: reward collection
#S: (row, col) position of the object, relative to agent, must be odd numbers now
#A: up, down, left, right
#R: +1 for reward collected, 0 ow
def calcReward_M1(state):
    if (state == [math.floor(MAX_ROW/2),math.floor(MAX_COL/2)]):
        reward = R_REWARD
    else:
        reward = 0
    return reward
#State Mapping function: map real world state into module state
#T: no wall yet ????
def stateMapping_M1(agentPos, objPos):
    offsetROW = int(math.floor(MAX_ROW/2))
    offsetCOL = int(math.floor(MAX_COL/2))
    state = [objPos[0] - agentPos[0] + offsetROW,objPos[1] - agentPos[1] + offsetCOL]
    return state

#Q learnig update
def updateQ_M1(Qtable,state,action,reward,stateNext,actionNext):
    #Discount factor
    Gamma = GAMMA_M1
    Alpha = 0.6
    #This is for Q learning update
    #actionNext = mathtool.optimalActionSelect(Qtable,stateNext,NUM_ACT)
    temp = Alpha * (reward + Gamma * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action])
    Qtable[state[0]][state[1]][action] += temp
    return Qtable


#Training Process
#Episode is terminated with max_steps or reward collected
def train_M1():
    #Q table initialization
    Qtable = numpy.zeros((MAX_ROW,MAX_COL,NUM_ACT))

    #agent initialization
    
    #We partition state space into 4 subspaces(quaters), agent should be placed at 4 loctions
    agentPosSet = [[TMAZE_SIZE - 1,TMAZE_SIZE - 1],[0,TMAZE_SIZE - 1],[TMAZE_SIZE - 1,0],[0,0]]
    #set of object positions (every position in the quater)
    objPosSet = []
    for i in range(TMAZE_SIZE):
        for j in range(TMAZE_SIZE):
            objPosSet.append([i,j])

    for agentPos in agentPosSet:
        for objPos in objPosSet:
	    #Train agent in current agentPos,objPos for several episodes
            for episode in range(NUM_EPISODE):
                #Generate a maze, place object 
                trainMaze = world.Maze(TMAZE_SIZE,TMAZE_SIZE,'reward',objPos)
                #Start agent at fixed position
                learningAgent = Agent(agentPos)

            	#Initialize state, action
                state = stateMapping_M1(learningAgent.pos,trainMaze.rewards[0])
                action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,EPSILON)
                stepCount = 0
        
                while (stepCount < MAX_STEP_EACH_EPISODE and state != [math.floor(MAX_ROW/2),math.floor(MAX_COL/2)]):
                    learningAgent.move(action,trainMaze)
                    stateNext = stateMapping_M1(learningAgent.pos,trainMaze.rewards[0])
                    actionNext = mathtool.eGreedyActionSelect(Qtable,stateNext,NUM_ACT,EPSILON)
                    reward = calcReward_M1(stateNext)
                    Qtable = updateQ_M1(Qtable,state,action,reward,stateNext,actionNext)
                    state = stateNext
                    action = actionNext
                    stepCount += 1

    print('M1 Training Complete')
    return Qtable

#Check the final policy
def printPolicy_M1(Qtable,objPos):
    testMaze = world.Maze(TMAZE_SIZE,TMAZE_SIZE,'reward',objPos)
    for i in range(testMaze.rows):
        for j in range(testMaze.columns):
            state = stateMapping_M1([i,j],testMaze.rewards[0])
            action = mathtool.optimalActionSelect(Qtable,state,NUM_ACT)
            testMaze.recordAction([i,j],action)         
    testMaze.printMap('original')
    testMaze.printMap('path')


#Module 2: obstacle avoidance
#S: (row, col) position of the object, relative to agent, must be odd numbers now
#A: up, down, left, right
#R: -1 for obstacle hit, 0 ow
def calcReward_M2(state):
    if (state == [math.floor(MAX_ROW/2),math.floor(MAX_COL/2)]):
        reward = R_OBSTACLE
    else:
        reward = 0
    return reward
#State Mapping function: map real world state into module state
#T: no wall yet ????
def stateMapping_M2(agentPos, objPos):
    offsetROW = int(math.floor(MAX_ROW/2))
    offsetCOL = int(math.floor(MAX_COL/2))
    state = [objPos[0] - agentPos[0] + offsetROW,objPos[1] - agentPos[1] + offsetCOL]
    return state

#Q learnig update
def updateQ_M2(Qtable,state,action,reward,stateNext,actionNext):
    #Discount factor
    Gamma = GAMMA_M2
    Alpha = 0.6
    #This is Q learning update rule
    #actionNext = mathtool.optimalActionSelect(Qtable,stateNext,NUM_ACT)
    temp = Alpha * (reward + Gamma * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action])
    Qtable[state[0]][state[1]][action] += temp
    return Qtable

#Training Process
#Episode is terminated with max_steps or obstacle hit
def train_M2():
    #Q table initialization
    Qtable = numpy.zeros((MAX_ROW,MAX_COL,NUM_ACT))

    #agent initialization
    
    #We partition state space into 4 subspaces(quaters), agent should be placed at 4 loctions
    agentPosSet = [[TMAZE_SIZE - 1,TMAZE_SIZE - 1],[0,TMAZE_SIZE - 1],[TMAZE_SIZE - 1,0],[0,0]]
    #set of object positions (every position in the quater)
    objPosSet = []
    for i in range(TMAZE_SIZE):
        for j in range(TMAZE_SIZE):
            objPosSet.append([i,j])

    for agentPos in agentPosSet:
        for objPos in objPosSet:
	        #Train agent in current agentPos,objPos for several episodes
            for episode in range(NUM_EPISODE):
                #Generate a maze, place object 
                trainMaze = world.Maze(TMAZE_SIZE,TMAZE_SIZE,'obstacle',objPos)
                #Start agent at fixed position
                learningAgent = Agent(agentPos)

            	#Initialize state, action
                state = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
                action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,EPSILON)
                stepCount = 0
        
                while (stepCount < MAX_STEP_EACH_EPISODE and state != [math.floor(MAX_ROW/2),math.floor(MAX_COL/2)]):
                    learningAgent.move(action,trainMaze)
                    stateNext = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
                    actionNext = mathtool.eGreedyActionSelect(Qtable,stateNext,NUM_ACT,EPSILON)
                    reward = calcReward_M2(stateNext)
                    Qtable = updateQ_M2(Qtable,state,action,reward,stateNext,actionNext)
                    state = stateNext
                    action = actionNext
                    stepCount += 1

    print('M2 Training Complete')
    return Qtable

#Check the final policy
def printPolicy_M2(Qtable,objPos):
    testMaze = world.Maze(TMAZE_SIZE,TMAZE_SIZE,'obstacle',objPos)
    for i in range(testMaze.rows):
        for j in range(testMaze.columns):
            state = stateMapping_M1([i,j],testMaze.obstacles[0])
            action = mathtool.optimalActionSelect(Qtable,state,NUM_ACT)
            testMaze.recordAction([i,j],action)         
    testMaze.printMap('original')
    testMaze.printMap('path')


#Train and store the Qtables for both modules
def writeQToFile(Qtable,filename):
    myFile = open(filename,'w')
    for i in range (len(Qtable)):
	    for j in range(len(Qtable[i])):
	        for k in range(len(Qtable[i][j])):
		        myFile.write(str(Qtable[i][j][k]))
		        myFile.write('\n')


def readQFromFile(filename):
    Qtable = numpy.zeros((MAX_ROW,MAX_COL,NUM_ACT))
    myFile = open(filename,'r')
    for i in range (len(Qtable)):
        for j in range(len(Qtable[i])):
            for k in range(len(Qtable[i][j])):
                Qtable[i][j][k] = float(myFile.readline())
    return Qtable

#QtableM1 = train_M1()
#QtableM2 = train_M2()
#writeQToFile(QtableM1,'Q1.txt')
#writeQToFile(QtableM2,'Q2.txt')
      
