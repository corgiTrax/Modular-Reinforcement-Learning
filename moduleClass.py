#Module class
#Modular RL Project
#Ruohan Zhang
#Module classes

import random
import mathtool
import numpy
import copy as py_copy
import config

ROW = config.ROW
COL = config.COL

#Key function here: measure the consensus of actions
#This function should capture two things
#1. How much is the expected reward (signaled by learned value, related to reward when training)
#2. at this state, indifference level on actions?
def calc_weight(Qtable, state):
    Qvalues = Qtable[state[0]][state[1]]
    #standard deviation, for discrete states
    return mathtool.calc_sd(Qvalues)

#Another key function here: voting
#Input are all modules (regardless of types)
def vote(modules):
    #Count the total weight of all actions
    scoreCount = numpy.zeros(config.NUM_ACT)   

    #Method 1: Russell and Zimdars: Q-decomposition: sum Q values of all modules
    for i in range(len(modules)):
	    state = modules[i].state
	    Qvalues = modules[i].Qtable[state[0]][state[1]]
	    for act in range(config.NUM_ACT):
            scoreCount[act] += Qvalues[act]

    #Method 2: standard deviation (weight) of Q values over actions
    for i in range(len(modules)):
        scoreCount[modules[i].optimalAct] += modules[i].weight
    return scoreCount

#Find action with highest accumulated weight
def decideAct(scoreCount):
   
    #Method 1: Choosing the action with highest score Count
    act = 0;
    score = scoreCount[0]
    for i in range(len(scoreCount)):
        if (scoreCount[i] > score):
	    act = i
	    score = scoreCount[i]
    
    #Method 2: Choosing actions with softmax probability

    return act   


#Class module
class Module:
    def __init__(self,Qtable,state):
        self.state = py_copy.deepcopy(state)
        self.Qtable = py_copy.deepcopy(Qtable)
        self.weight = calc_weight(Qtable,state)
        self.optimalAct = mathtool.optimalActionSelect(Qtable,state,config.NUM_ACT)
