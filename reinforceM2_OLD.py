#Modular RL Project
#Ruohan Zhang
#Modular RL algorithm for module2 OLD

import mathtool
import world
import random
import copy as py_copy
import numpy
import math
import graphics as graph
import reinforceClass
from config import *

#Module 2: obstacle avoidance
#S: (row, col) position of the object, relative to agent, must be odd numbers now
#A: up, down, left, right
#R: R_OBSTACLE for obstacle hit, 0 ow
def calcReward_M2(state):
    if (state == [math.floor(MAX_ROW_M2/2),math.floor(MAX_COL_M2/2)]):
        reward = R_OBSTACLE
    else:
        reward = 0
    return reward
#State Mapping function: map real world state into module state
#T: no wall yet ????
def stateMapping_M2(agentPos, objPos):
    offsetROW = int(math.floor(MAX_ROW_M2/2))
    offsetCOL = int(math.floor(MAX_COL_M2/2))
    state = [objPos[ROW] - agentPos[ROW] + offsetROW,objPos[COL] - agentPos[COL] + offsetCOL]
    return state
def stateMappingInverse_M2(state,agentPos):
    offsetROW = int(math.floor(MAX_ROW_M2/2))
    offsetCOL = int(math.floor(MAX_COL_M2/2))
    objPos = [state[ROW] + agentPos[ROW] - offsetROW, state[COL] + agentPos[COL] - offsetCOL]
    return objPos
 
#Q learnig update
def updateQ_M2(Qtable,state,action,reward,stateNext,actionNext):
    #Discount factor
    Gamma = GAMMA_M2
    Alpha = ALPHA_M2
    #This is Q learning update rule
    #actionNext = mathtool.optimalActionSelect(Qtable,stateNext,NUM_ACT)
    temp = Alpha * (reward + Gamma * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action])
    Qtable[state[0]][state[1]][action] += temp
    return Qtable

#Training Process
#Episode is terminated with max_steps or obstacle hit
def train_M2():
    #Q table initialization
    Qtable = numpy.zeros((MAX_ROW_M2, MAX_COL_M2, NUM_ACT))
    
    #We partition state space into 4 subspaces(quaters), agent should be placed at 4 loctions
    agentPosSet = [[TMAZE_SIZE_M2 - 1,TMAZE_SIZE_M2 - 1],[0,TMAZE_SIZE_M2 - 1],[TMAZE_SIZE_M2 - 1,0],[0,0]]
    #set of object positions (every position in the quater)
    objPosSet = []
    for i in range(TMAZE_SIZE_M2):
        for j in range(TMAZE_SIZE_M2):
            objPosSet.append([i,j])

    for agentPos in agentPosSet:
        for objPos in objPosSet:
	        #Train agent in current agentPos,objPos for several episodes
            for episode in range(NUM_EPISODE_M2):
                #Generate a maze, place object 
                trainMaze = world.Maze(TMAZE_SIZE_M2,TMAZE_SIZE_M2,'obstacle',objPos)
                #Start agent at fixed position
                learningAgent = Agent(agentPos)

            	#Initialize state, action
                state = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
                action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,EPSILON_M2)
                stepCount = 0
        
                while (stepCount < MAX_STEP_EACH_EPISODE_M2 and state != [math.floor(MAX_ROW_M2/2),math.floor(MAX_COL_M2/2)]):
                    learningAgent.move(action,trainMaze)
                    stateNext = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
                    actionNext = mathtool.eGreedyActionSelect(Qtable,stateNext,NUM_ACT,EPSILON_M2)
                    reward = calcReward_M2(stateNext)
                    Qtable = updateQ_M2(Qtable,state,action,reward,stateNext,actionNext)
                    state = stateNext
                    action = actionNext
                    stepCount += 1

    print('M2 Training Complete')
    return Qtable

#Check the final policy
def printPolicy_M2(Qtable,objPos):
    testMaze = world.Maze(TMAZE_SIZE_M2,TMAZE_SIZE_M2,'obstacle',objPos)
    for i in range(testMaze.rows):
        for j in range(testMaze.columns):
            state = stateMapping_M2([i,j],testMaze.obstacles[0])
            action = mathtool.optimalActionSelect(Qtable,state,NUM_ACT)
            testMaze.recordAction([i,j],action)         
    testMaze.printMap('original')
    testMaze.printMap('path')

def printQtable_M2(QtableM2):
    agentPos = [0,0]
    for i in range(MAX_ROW_M2):
        for j in range(MAX_COL_M2):
            state = [i,j]
            objRelPos = stateMappingInverse_M2(state,agentPos)
            print('object at:',objRelPos,'state:',state,'Q values:',QtableM2[state[0]][state[1]])


