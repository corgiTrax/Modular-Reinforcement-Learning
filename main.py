#Main
#Modular RL Project
#Ruohan Zhang
#Main Experiment and Visualization

import world
import moduleClass
import reinforcement
import copy as py_copy
import graphics as graph
from config import *


#Read a Qtable for module 1
QtableM1 = reinforcement.readQFromFile('Q1.txt')
#reinforcement.printPolicy_M1(QtableM1,[2,2])
#Read a Qtable for module 2
QtableM2 = reinforcement.readQFromFile('Q2.txt')
#reinforcement.printPolicy_M2(QtableM2,[2,2])



#Combined Navigation
testMaze = world.Maze(TESTR,TESTC,'test')
testMaze.drawSelf(TESTR * CELL_SIZE, TESTC * CELL_SIZE + 100, True)

myAgent = reinforcement.Agent([0,0])
myAgent.drawSelf(testMaze.window,True)
stepCount = 0

while (stepCount < MAX_STEP): 
    #Execute one step only when mouse clicks
    testMaze.window.getMouse()

    #Detect all rewards within range, get their positions
    rewardsNear = world.findNearbyObj('reward',myAgent.pos,VRANGE,testMaze)
    #Initialize one module for each reward
    rewardModules = []
    #Each module measure its own state, suggested action, flatness, and weight
    for i in range(len(rewardsNear)):
        state = reinforcement.stateMapping_M1(myAgent.pos,rewardsNear[i])
        newModule = moduleClass.Module(QtableM1,state)
        rewardModules.append(newModule)

    #Detect all obstacles within range, get their positions
    obstaclesNear = world.findNearbyObj('obstacle',myAgent.pos,VRANGE,testMaze)
    #Initialize one module for each obstacle
    obstacleModules = []
    #Each module measure its own state, suggested action, flatness, and weight
    for i in range (len(obstaclesNear)):
        state = reinforcement.stateMapping_M2(myAgent.pos,obstaclesNear[i])
        newModule = moduleClass.Module(QtableM2,state)
        obstacleModules.append(newModule)

    #Combine all suggested action by their weight, determine global action
    allModules = rewardModules + obstacleModules    
    scores = moduleClass.vote(allModules)
    action = moduleClass.decideAct(scores)
    #for i in range(len(allModules)):
	#print(stepCount,'module',i,'state',allModules[i].state,'action',allModules[i].optimalAct,'weight',allModules[i].weight)
    #print(scores,action)

    #mark action at this position
    testMaze.recordAction(myAgent.pos,action)
    #agent takes action, and compute reward
    myAgent.move(action,testMaze)
    myAgent.cumReward += testMaze.calc_reward(myAgent.pos)
    testMaze.drawSelf(TESTR * CELL_SIZE, TESTC * CELL_SIZE + 100, False)   
    myAgent.drawSelf(testMaze.window, False)

    stepCount +=1
    print('step:',stepCount)
    #testMaze.printMap('path')




#Hold graph window
raw_input("Press enter to exit")


    
########################## Repository ######################
#
#
#
#
#
#
#
#
#
#
#
#
#
#

