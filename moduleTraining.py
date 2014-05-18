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
from config import *

#Now we do not decompose actions, same actions are used globally

#Agent class
class Agent:
    def __init__(self,initPos):
        self.pos = initPos
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
def updateQ_M1(Qtable,state,action,reward,stateNext):
    #Discount factor
    Gamma = 0.7
    Alpha = 0.75
    actionNext = mathtool.optimalActionSelect(Qtable,stateNext,NUM_ACT)
    temp = Alpha * (reward + Gamma * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action])
    Qtable[state[0]][state[1]][action] += temp
    return Qtable


#Training Process
#Each episode consists of a small maze of size MAX_ROW*MAX_COL,
#with 1 reward placed randomly ***
#Episode is terminated with max_steps or reward collected
def train_M1():
    #Q table initialization
    Qtable = numpy.zeros((MAX_ROW,MAX_COL,NUM_ACT))

    #agent initialization
    learningAgent = Agent([0,0])

    epsilon = 0.9
    
    for episode in range(NUM_EPISODE):
        #Generate a maze of MAX_ROW * MAX_COL
        trainMaze = world.Maze(VRANGE + 1,VRANGE + 1,'reward')
        #Start at random position
        learningAgent.setPos([random.choice(range(trainMaze.rows)),random.choice(range(trainMaze.columns))])
        #Initialize state
        state = stateMapping_M1(learningAgent.pos,trainMaze.rewards[0])
        stepCount = 0
        
        while (stepCount < MAX_STEP_EACH_EPISODE and state != [math.floor(MAX_ROW/2),math.floor(MAX_COL/2)]):

            action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,epsilon)
            learningAgent.move(action,trainMaze)

            #After move, the object might be out of sight, or new object introduced to site, need to handle this.
            

            stateNext = stateMapping_M1(learningAgent.pos,trainMaze.rewards[0])
            reward = calcReward_M1(stateNext)
            Qtable = updateQ_M1(Qtable,state,action,reward,stateNext)
            state = stateNext
            stepCount += 1

    print('M1 Training Complete')
    return Qtable

#Check the final policy
def printPolicy_M1(Qtable):
    testMaze = world.Maze(VRANGE + 1,VRANGE + 1,'reward')
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
def updateQ_M2(Qtable,state,action,reward,stateNext):
    #Discount factor
    Gamma = 0.7
    Alpha = 0.75
    actionNext = mathtool.optimalActionSelect(Qtable,stateNext,NUM_ACT)
    temp = Alpha * (reward + Gamma * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action])
    Qtable[state[0]][state[1]][action] += temp
    return Qtable

#Training Process
#Each episode consists of a small maze of size MAX_ROW * MAX_COL,
#with 1 reward placed randomly ***
#Episode is terminated with max_steps or reward collected
def train_M2():
    #Q table initialization
    Qtable = numpy.zeros((MAX_ROW,MAX_COL,NUM_ACT))

    #agent initialization
    learningAgent = Agent([0,0])

    epsilon = 0.9
    
    for episode in range(NUM_EPISODE):
        #Generate a maze of MAX_ROW * MAX_COL
        trainMaze = world.Maze(VRANGE + 1,VRANGE + 1,'obstacle')
        #Start at random position
        learningAgent.setPos([random.choice(range(trainMaze.rows)),random.choice(range(trainMaze.columns))])
        #Initialize state
        state = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
        stepCount = 0
        
        while (stepCount < MAX_STEP_EACH_EPISODE and state != [math.floor(MAX_ROW/2),math.floor(MAX_COL/2)]):

            action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,epsilon)
            learningAgent.move(action,trainMaze)

            #After move, the object might be out of sight, or new object introduced to site, need to handle this.
            
            stateNext = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
            reward = calcReward_M2(stateNext)
            Qtable = updateQ_M2(Qtable,state,action,reward,stateNext)
            state = stateNext
            stepCount += 1

    print('M2 Training Complete')
    return Qtable

#Check the final policy
def printPolicy_M2(Qtable):
    testMaze = world.Maze(VRANGE + 1,VRANGE + 1,'obstacle')
    for i in range(testMaze.rows):
        for j in range(testMaze.columns):
            state = stateMapping_M1([i,j],testMaze.obstacles[0])
            action = mathtool.optimalActionSelect(Qtable,state,NUM_ACT)
            testMaze.recordAction([i,j],action)         
    testMaze.printMap('original')
    testMaze.printMap('path')

      
