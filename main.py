#Main
#Modular RL Project
#Ruohan Zhang
#Main Experiment and Visualization

import world
import moduleClass
import reinforceClass
import reinforceM1
import reinforceM2
import reinforceM3
import mathtool
import copy as py_copy
import graphics as graph
from config import *


#Read Qtables from each module
QtableM1 = mathtool.readQFromFile('Q1.txt',"M1")
QtableM2 = mathtool.readQFromFile('Q2.txt',"M2")
QtableM3 = mathtool.readQFromFile('Q3.txt',"M3")

#Maze
testMaze = world.Maze(TESTR, TESTC, 'test')
testMaze.drawSelf(True)

#Predator starts at (0,0)
predator = reinforceClass.Predator([0,0])
predator.drawSelf(testMaze.window, True)

#Agent starts at middle
myAgent = reinforceClass.Agent([int(TESTR/2),int(TESTC/2)])
myAgent.drawSelf(testMaze.window,True)
Captured = False #being captured by predator or not
stepCount = 0

while (stepCount < MAX_STEP and (not Captured)):
    print('Step count',stepCount)

    #Module Block #1: price
    if (NEAREST_PRICE_ONLY == False):
        #Detect all prices within range, get their positions
        pricesNear = world.findNearbyObj('price',myAgent.pos,TEST_VRANGE_M1,testMaze)
        #Initialize one module for each price
        priceModules = []
        #Each module measure its own state, suggested action, flatness, and weight
        for i in range(len(pricesNear)):
            state = reinforceM1.stateMapping_M1(myAgent.pos,pricesNear[i])
            priceModules.append(moduleClass.Module(QtableM1,state))

    if (NEAREST_PRICE_ONLY == True):    
        #Detect nearest price
        priceNearest = world.findNearestPrice(myAgent.pos,testMaze)
        print("Agent is at: ", myAgent.pos)
        print("Currently pursuing: ", priceNearest)
        priceModules = []
        state = reinforceM1.stateMapping_M1(myAgent.pos,priceNearest)
        priceModules.append(moduleClass.Module(QtableM1,state))
        testMaze.drawTargetPrice(priceNearest)

    #Module Block #2: obstacles
    #Detect all obstacles within range, get their positions
    obstaclesNear = world.findNearbyObj('obstacle',myAgent.pos,TEST_VRANGE_M2,testMaze)
    #Initialize one module for each obstacle
    obstacleModules = []
    #Each module measure its own state, suggested action, flatness, and weight
    for i in range (len(obstaclesNear)):
        state = reinforceM2.stateMapping_M2(myAgent.pos,obstaclesNear[i])
        newModule = moduleClass.Module(QtableM2,state)
        obstacleModules.append(newModule)

    #Module Block #3: predator
    predatorModule = []
    predatorModule.append(moduleClass.Module(QtableM3,reinforceM3.stateMapping_M3(myAgent.pos,predator.pos)))

    #Combine all suggested action by their weight, determine global action
    allModules = []
    allModules = priceModules + obstacleModules + predatorModule    
    scores = moduleClass.vote(allModules)
    action = moduleClass.decideAct(scores)
    for i in range(len(priceModules)):
        print('Executing price module:',i,'Price pos:',reinforceM1.stateMappingInverse_M1(priceModules[i].state,myAgent.pos),'Q values',priceModules[i].Qvalues,'action:',priceModules[i].optimalAct,'sd weight:',priceModules[i].weight)
    for i in range(len(obstacleModules)):
        print('Executing obstacle module:',i,'Obs pos:',reinforceM2.stateMappingInverse_M2(obstacleModules[i].state,myAgent.pos),'Q values',obstacleModules[i].Qvalues,'action:',obstacleModules[i].optimalAct,'weight:',obstacleModules[i].weight)
    print('Executing predator module:',0,'predator pos:',predator.pos,'Q values',predatorModule[0].Qvalues,'action:',predatorModule[0].optimalAct,'weight:',predatorModule[0].weight)
     
    print('GMQ total score',scores,'action',action)

    #move one step only when mouse clicks
    testMaze.window.getMouse()
    
    #agent takes action, and compute reward
    predator.move(predator.chase(myAgent.pos),testMaze)
    myAgent.move(action,testMaze)
    Captured = (myAgent.pos == predator.pos)
    
    #Calculate cumulative reward
    myAgent.cumReward += testMaze.calc_reward(myAgent.pos)#calc_reward function also remove prices from maze price list
    if (Captured): myAgent.cumReward -= R_PREDATOR

    testMaze.drawSelf(False)   
    myAgent.drawSelf(testMaze.window, False)
    predator.drawSelf(testMaze.window,False)
    
    stepCount +=1
    print('step:',stepCount)


#Hold graph window
raw_input("Press enter to exit")

 
########################## Repository ######################
#
#
#
#
#
#

