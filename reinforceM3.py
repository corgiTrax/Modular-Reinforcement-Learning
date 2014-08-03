#Modular RL Project
#Ruohan Zhang
#Modular RL algorithm for module3

import mathtool
import world
import random
import copy as py_copy
import numpy
import math
import graphics as graph
import reinforceClass
from config import *

#Module 3: predator avoidance
#S: (row, col) position of the object, relative to agent, must be odd numbers now
#A: up, down, left, right
#R: +R_PREDATOR for price collected, 0 ow
def calcReward_M3(state):
    if (state == [math.floor(MAX_ROW_M3/2),math.floor(MAX_COL_M3/2)]):
        reward = R_PREDATOR
    else:
        reward = 0
    return reward
#State Mapping function: map real world state into module state
def stateMapping_M3(agentPos, objPos):
    offsetROW = int(math.floor(MAX_ROW_M3/2))
    offsetCOL = int(math.floor(MAX_COL_M3/2))
    state = [objPos[ROW] - agentPos[ROW] + offsetROW,objPos[COL] - agentPos[COL] + offsetCOL]
    return state
def stateMappingInverse_M3(state,agentPos):
    offsetROW = int(math.floor(MAX_ROW_M3/2))
    offsetCOL = int(math.floor(MAX_COL_M3/2))
    objPos = [state[ROW] + agentPos[ROW] - offsetROW, state[COL] + agentPos[COL] - offsetCOL]
    return objPos
   
##The version without eligibility traces
#def updateQ_M3(Qtable,state,action,reward,stateNext,actionNext):
#    #Discount factor
#    Gamma = GAMMA_M3
#    Alpha = ALPHA_M3
#    #This is for Q learning update
#    #actionNextQ = mathtool.optimalActionSelect(Qtable,stateNext,NUM_ACT)
#    temp = Alpha * (reward + Gamma * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action])
#    Qtable[state[0]][state[1]][action] += temp
#    return Qtable

#Training Process
#Episode is terminated with max_steps or price collected
def train_M3():
    #Q table initialization
    Qtable = numpy.zeros((MAX_ROW_M3,MAX_COL_M3,NUM_ACT))
    #Eligibility traces
    Etable = numpy.zeros((MAX_ROW_M3,MAX_COL_M3,NUM_ACT))#ET
    
    #We partition state space into 4 subspaces(quaters), agent should be placed at 4 starting loctions
    #The reason for doing this is for more organized training
    agentPosSet = [[TMAZE_SIZE_M3 - 1,TMAZE_SIZE_M3 - 1],[0,TMAZE_SIZE_M3 - 1],[TMAZE_SIZE_M3 - 1,0],[0,0]]
    #set of object positions (every position in the quater)
    objPosSet = []
    for i in range(TMAZE_SIZE_M3):
        for j in range(TMAZE_SIZE_M3):
            objPosSet.append([i,j])

    for agentPos in agentPosSet:
        print("25% done")
        for objPos in objPosSet:
            print("0.25% done")
	    #Train agent in current agentPos,objPos for several episodes
            for episode in range(NUM_EPISODE_M3):
                #Generate a maze, place object 
                trainMaze = world.Maze(TMAZE_SIZE_M3,TMAZE_SIZE_M3,'empty')
                #Start agent at fixed position
                learningAgent = reinforceClass.Agent(agentPos)
                predator = reinforceClass.Predator(objPos)

                #Calculate parameters for current episode: Anneal eps -> 1 and alpha -> 0
                Epsilon = min(episode * (1.0/NUM_EPISODE_M3),0.99)
                Alpha = 1 - episode * (1.0/NUM_EPISODE_M3)

            	#Initialize state, action
                state = stateMapping_M3(learningAgent.pos,predator.pos)
                action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,Epsilon)
                stepCount = 0
        
                while (stepCount < MAX_STEP_EACH_EPISODE_M3 and state != [math.floor(MAX_ROW_M3/2),math.floor(MAX_COL_M3/2)]):
                    #Qtable = updateQ_M3(Qtable,state,action,reward,stateNext,actionNext) #for regular sarsa
                    
                   if (SARSA_ET == True):
                        #agent and predator make decision simutaneously//predator moves first
                        agentLastPos = learningAgent.pos 
                        learningAgent.move(action,trainMaze)
                        predator.move(predator.chase(agentLastPos),trainMaze)  
                        
                        #Agent plan for next step
                        stateNext = stateMapping_M3(learningAgent.pos,predator.pos)#???Think about this
                        reward = calcReward_M3(stateNext)#???
                        actionNext = mathtool.eGreedyActionSelect(Qtable,stateNext,NUM_ACT,Epsilon)
                        delta = reward + GAMMA_M3 * Qtable[stateNext[0]][stateNext[1]][actionNext] - Qtable[state[0]][state[1]][action]
                        #Replacing traces
                        for i in range(NUM_ACT):
                            if (i == action):
                                Etable[state[0]][state[1]][i] += 1
                            else:
                                Etable[state[0]][state[1]][i] = 0
                        for i in range(MAX_ROW_M3):
                            for j in range(MAX_COL_M3):
                                for k in range(NUM_ACT):
                                    Qtable[i][j][k] = Qtable[i][j][k] + Alpha * delta * Etable[i][j][k]    
                                    Etable[i][j][k] = GAMMA_M3 * LAMBDA_M3 * Etable[i][j][k]
                        state = stateNext
                        action = actionNext
                   stepCount += 1

    print('M3 Training Complete')
    return Qtable

def printQtable_M3(QtableM3):
    agentPos = [0,0]
    for i in range(MAX_ROW_M3):
        for j in range(MAX_COL_M3):
            state = [i,j]
            objRelPos = stateMappingInverse_M3(state,agentPos)
            print('object at:',objRelPos,'state:',state,'Q values:',QtableM3[state[0]][state[1]])



