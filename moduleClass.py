#Module class
#Modular RL Project
#Ruohan Zhang
#Module classes

import random
import mathtool
import numpy
import copy as py_copy
from config import *

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
    scoreCount = numpy.zeros(NUM_ACT)
    for i in range(len(modules)):
	#state = modules[i].state
	#Qvalues = modules[i].Qtable[state[0]][state[1]]
	#for act in range(NUM_ACT):
            #scoreCount[act] += Qvalues[act]
	scoreCount[modules[i].optimalAct] += modules[i].weight
    return scoreCount

#Find action with highest accumulated weight
def decideAct(scoreCount):
    act = 0;
    score = scoreCount[0]
    for i in range(len(scoreCount)):
        if (scoreCount[i] > score):
	    act = i
	    score = scoreCount[i]
    return act   


#Class module
class Module:
    def __init__(self,Qtable,state):
        self.state = py_copy.deepcopy(state)
        self.Qtable = py_copy.deepcopy(Qtable)
        self.weight = calc_weight(Qtable,state)
        self.optimalAct = mathtool.optimalActionSelect(Qtable,state,NUM_ACT)
