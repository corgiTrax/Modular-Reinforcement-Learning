#Main
#Modular RL Project
#Ruohan Zhang
#Main Experiment and Visualization

import world
import moduleClass
import reinforcement
import mathtool
import copy as py_copy
import graphics as graph
from config import *


#Read a Qtable for module 1
QtableM1 = mathtool.readQFromFile('Q1_VRANGE_15.txt',"M1")
reinforcement.printPolicy_M1(QtableM1,[7,7])
#Read a Qtable for module 2
QtableM2 = mathtool.readQFromFile('Q2_VRANGE_3_GAMMA_0.txt',"M2")
reinforcement.printPolicy_M2(QtableM2,[1,1])
#Navigation
testMaze = world.Maze(TESTR, TESTC, 'test')
testMaze.drawSelf(True)

myAgent = reinforcement.Agent([int(TESTR/2),int(TESTC/2)])
myAgent.drawSelf(testMaze.window,True)
stepCount = 0

while (stepCount < MAX_STEP): 

    #Detect all prices within range, get their positions
    pricesNear = world.findNearbyObj('price',myAgent.pos,TEST_VRANGE_M1,testMaze)
    #Initialize one module for each price
    priceModules = []
    #Each module measure its own state, suggested action, flatness, and weight
    for i in range(len(pricesNear)):
        state = reinforcement.stateMapping_M1(myAgent.pos,pricesNear[i])
        priceModules.append(moduleClass.Module(QtableM1,state))
    
#    #Detect nearest price
#    priceNearest = world.findNearestPrice(myAgent.pos,testMaze)
#    print("Agent is at: ", myAgent.pos)
#    print("Currently pursuing: ", priceNearest)
#    priceModules = []
#    state = reinforcement.stateMapping_M1(myAgent.pos,priceNearest)
#    priceModules.append(moduleClass.Module(QtableM1,state))
#    testMaze.drawTargetPrice(priceNearest)

    #Detect all obstacles within range, get their positions
    obstaclesNear = world.findNearbyObj('obstacle',myAgent.pos,TEST_VRANGE_M2,testMaze)
    #Initialize one module for each obstacle
    obstacleModules = []
    #Each module measure its own state, suggested action, flatness, and weight
    for i in range (len(obstaclesNear)):
        state = reinforcement.stateMapping_M2(myAgent.pos,obstaclesNear[i])
        newModule = moduleClass.Module(QtableM2,state)
        obstacleModules.append(newModule)

    #Combine all suggested action by their weight, determine global action
    allModules = priceModules + obstacleModules    
    scores = moduleClass.vote(allModules)
    action = moduleClass.decideAct(scores)
    #for i in range(len(allModules)):
	#print(stepCount,'module',i,'state',allModules[i].state,'action',allModules[i].optimalAct,'weight',allModules[i].weight)
    #print(scores,action)

    #mark action at this position
    testMaze.recordAction(myAgent.pos,action)
    
    #move one step only when mouse clicks
    testMaze.window.getMouse()
    
    #agent takes action, and compute reward
    myAgent.move(action,testMaze)
    myAgent.cumReward += testMaze.calc_reward(myAgent.pos)#calc_reward function also remove prices from maze price list
    testMaze.drawSelf(False)   
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

