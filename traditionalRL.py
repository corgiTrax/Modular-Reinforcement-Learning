#Modular RL Project: reinforcement learning: traditional approach
#Requires numpy support
#Ruohan Zhang

'''Note: traditional RL does not work for current domain and scale!!!
Because prices can be collected! Then the state space is maze.rows * maze.columns * (2 ** NUM_PRICES)
'''

import world
import random
import copy as py_copy
import numpy
import mathtool
from config import *

#An MDP is a tuple {S,A,R,T, Gamma}

############################# Traditional RL #############################
#Actions: defined in config
#States: absolute coordinates in current maze

#State transition
def move(curPos, action, maze):
    newPos = [curPos[0],curPos[1]]
    if (action == Up):newPos[0] -=1
    if (action == Down):newPos[0] +=1
    if (action == Left):newPos[1] -=1
    if (action == Right):newPos[1] +=1
    if (newPos[0] >= maze.rows):newPos[0] = maze.rows - 1;
    if (newPos[0] < 0):newPos[0] = 0;
    if (newPos[1] >= maze.columns):newPos[1] = maze.columns - 1;        
    if (newPos[1] < 0):newPos[1] = 0;
    return newPos

#Reward
def calcReward(state, maze):
    i = state[ROW]
    j = state[COL]
    if (maze.mazeMap[i][j] == world.PRICE):
        reward = R_PRICE
    elif (maze.mazeMap[i][j] == world.OBSTACLE):
        reward = R_OBSTACLE
    else:
        reward = R_EMPTY
    return reward

#Sarsa learning update rule and parameters
def updateQ(Qtable,state,action,reward,stateNext,actionNext):
    GAMMA = 0.99
    ALPHA = 0.6
    temp = ALPHA * (reward + GAMMA * Qtable[stateNext[ROW]][stateNext[COL]][actionNext] - Qtable[state[ROW]][state[COL]][action])
    Qtable[state[ROW]][state[COL]][action] += temp
    return Qtable

#Training
def train(curMaze):
    #Q table initialization
    Qtable = zeros((curMaze.rows,curMaze.columns,NUM_ACT))
    NUM_EPISODE = 1000
    MAX_STEP_EACH_EPISODE = 2000
    EPSILON = 0.9
    
    for episode in range(NUM_EPISODE):
        #initialization for one episode
        state = [random.choice(range(curMaze.rows)),random.choice(range(curMaze.columns))]
        action = mathtool.eGreedyActionSelect(Qtable,state,NUM_ACT,EPSILON)
        stepCount = 0

        while(stepCount < MAX_STEP_EACH_EPISODE):
            stateNext = move(state,action,curMaze)
            actionNext = eGreedyActionSelect(Qtable,stateNext)
            reward = calcReward(stateNext,curMaze)
            Qtable = updateQ(Qtable,state,action,reward,stateNext)
            state = stateNext
            action = actionNext
            stepCount += 1
    
    print('Current Maze Training Complete')
    return Qtable

#Check the final policy
def printPolicy(Qtable,start,curMaze):
    demoMaze = py_copy.deepcopy(curMaze)
    state = start
    demoMaze.map[state[ROW]][state[COL]] = 2
    MAX_STEP_EACH_EPISODE = 50
    stepCount = 0
    totalReward = 0
    while((state[COL] != curMaze.columns - 1) and (stepCount < MAX_STEP_EACH_EPISODE)):
        action = optimalActionSelect(Qtable,state)
        totalReward += calcReward(state,curMaze)
        stateNext = move(state,action,curMaze)
        state = stateNext
        demoMaze.map[state[ROW]][state[COL]] = 2
        stepCount += 1
        #print(state)
    print('Original Maze Map')
    curMaze.printMap()
    print('Agent Navigation Map')
    demoMaze.printMap()
    print(totalReward)
    print(stepCount)
    
#Call to execute, the result is for currentMaze *ONLY*
Qtable = qLearning(trainingMaze)
#Clearly if you use a new maze this is not going to work
#newMaze = world.Maze(3,25,0.3) 
printPolicy(Qtable,[0,0],trainingMaze)
############################# Traditional RL #############################


########################### Experiments ##################################
    
########################### Experiments ##################################
