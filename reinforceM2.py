#Modular RL Project
#Ruohan Zhang
#Modular RL algorithm for module2

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
#R: +R_OBSTACLE for obstacle hit, 0 ow
def calcReward_M2(state):
    if (state == [math.floor(MAX_ROW_M2/2),math.floor(MAX_COL_M2/2)]):
        reward = R_OBSTACLE
    else:
        reward = 0
    return reward
#State Mapping function: map real world state into module state
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
   
##The version without eligibility traces
#def updateQ_M2(Qtable,state,action,reward,stateNext,actionNext):
#    #Discount factor
#    Gamma = GAMMA_M2
#    Alpha = ALPHA_M2
#    #This is Q learning update rule
#    #actionNext = mathtool.optimalActionSelect(Qtable,stateNext,NUM_ACT)
#    temp = Alpha * (reward + Gamma * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action])
#    Qtable[state[0]][state[1]][action] += temp
#    return Qtable

#Training Process
#Episode is terminated with max_steps or obstacle hit
def train_M2():
    #Q table initialization
    Qtable = numpy.zeros((MAX_ROW_M2,MAX_COL_M2,NUM_ACT))
    #Eligibility traces
    Etable = numpy.zeros((MAX_ROW_M2,MAX_COL_M2,NUM_ACT))#ET
    
    #We partition state space into 4 subspaces(quaters), agent should be placed at 4 starting loctions
    #The reason for doing this is for more organized training
    agentPosSet = [[TMAZE_SIZE_M2 - 1,TMAZE_SIZE_M2 - 1],[0,TMAZE_SIZE_M2 - 1],[TMAZE_SIZE_M2 - 1,0],[0,0]]
    #set of object positions (every position in the quater)
    objPosSet = []
    for i in range(TMAZE_SIZE_M2):
        for j in range(TMAZE_SIZE_M2):
            objPosSet.append([i,j])

    for agentPos in agentPosSet:
        print("25% done")
        for objPos in objPosSet:
            print("0.25% done")
	    #Train agent in current agentPos,objPos for several episodes
            for episode in range(NUM_EPISODE_M2):
                #Generate a maze, place object 
                trainMaze = world.Maze(TMAZE_SIZE_M2,TMAZE_SIZE_M2,'obstacle',objPos)
                #Start agent at fixed position
                learningAgent = reinforceClass.Agent(agentPos)

                #Calculate parameters for current episode: Anneal eps -> 1 and alpha -> 0
                Epsilon = min(episode * (1.0/NUM_EPISODE_M2),0.95)
                Alpha = 1 - episode * (1.0/NUM_EPISODE_M2)

            	#Initialize state, action
                state = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
                action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,Epsilon)
                stepCount = 0
        
                while (stepCount < MAX_STEP_EACH_EPISODE_M2 and state != [math.floor(MAX_ROW_M2/2),math.floor(MAX_COL_M2/2)]):
                    #Qtable = updateQ_M2(Qtable,state,action,reward,stateNext,actionNext) #for regular sarsa
                    
                   if (SARSA_ET == True):
                        learningAgent.move(action,trainMaze)
                        stateNext = stateMapping_M2(learningAgent.pos,trainMaze.obstacles[0])
                        reward = calcReward_M2(stateNext)
                        actionNext = mathtool.eGreedyActionSelect(Qtable,stateNext,NUM_ACT,Epsilon)
                        delta = reward + GAMMA_M2 * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action]
                        #Replacing traces
                        for i in range(NUM_ACT):
                            if (i == action):
                                Etable[state[0]][state[1]][i] += 1
                            else:
                                Etable[state[0]][state[1]][i] = 0
                        for i in range(MAX_ROW_M2):
                            for j in range(MAX_COL_M2):
                                for k in range(NUM_ACT):
                                    Qtable[i][j][k] = Qtable[i][j][k] + Alpha * delta * Etable[i][j][k]    
                                    Etable[i][j][k] = GAMMA_M2 * LAMBDA_M2 * Etable[i][j][k]
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



