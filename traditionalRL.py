#Modular RL Project: reinforcement learning: traditional approach
#Requires numpy support
#Ruohan Zhang

import world
import random
import copy as py_copy
from numpy import *
trainingMaze = world.Maze(3,25,1.0)

#An MDP is a tuple {S,A,R,T, Gamma}

############################# Traditional RL #############################
#Action
NUM_ACT = 4
Up = 0; Down = 1; Left = 2; Right = 3;
Action = [Up, Down, Left, Right]

#State
ROW = 0
COL = 1

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
#finishline has reward of +1 and other states have -1 obstacle has -5
def calcReward(state,curMaze):
    if(state[COL] == curMaze.columns - 1):
        reward = 0
    else:
        reward = -1
    if (curMaze.map[state[ROW]][state[COL]] == -1):
        reward = -6
    return reward

#Action selection functions
def optimalActionSelect(Qtable,state):
    action = 0
    for i in range(NUM_ACT):
        if (Qtable[state[ROW]][state[COL]][i] > Qtable[state[ROW]][state[COL]][action]):
            action = i
    return action
def eGreedyActionSelect(Qtable,state):
    EPSILON = 0.9
    seed = random.random()
    #Exploit
    if (seed < EPSILON):
        action = optimalActionSelect(Qtable,state)
    #Explore
    else:
        action = random.choice(range(NUM_ACT))
    return action

#Q learning update rule and parameters
def updateQ(Qtable,state,action,reward,stateNext):
    Gamma = 0.99
    Alpha = 0.5
    actionNext = optimalActionSelect(Qtable,stateNext)
    temp = Alpha * (reward + Gamma * Qtable[stateNext[ROW]][stateNext[COL]][actionNext] - Qtable[state[ROW]][state[COL]][action])
    Qtable[state[ROW]][state[COL]][action] += temp
    return Qtable

#Q learning process
def qLearning(curMaze):
    #Q table initialization
    Qtable = zeros((curMaze.rows,curMaze.columns,NUM_ACT))
    NUM_EPISODE = 1000
    MAX_STEP_EACH_EPISODE = 1000
    
    for episode in range(NUM_EPISODE):
        #initialization for one episode
        startRow = random.choice(range(3))
        state = [startRow,0]
        stepCount = 0
        while((state[COL] != curMaze.columns - 1) and (stepCount < MAX_STEP_EACH_EPISODE)):
            action = eGreedyActionSelect(Qtable,state)

            stateNext = move(state,action,curMaze)
            reward = calcReward(stateNext,curMaze)
            Qtable = updateQ(Qtable,state,action,reward,stateNext)
            state = stateNext
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
