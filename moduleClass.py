#Module class
#Modular RL Project
#Ruohan Zhang
#Module classes

import random
import mathtool
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
       scoreCount[modules[i].optimalAct] += modules[i].weight
    return scoreCount

#Find action with highest accumulated weight
def decideAct(scoreCount):
    act = 0;
    score = scoreCount[0]
    for i in range(len(scoreCount)):
        if (scoreCount[i] > score):
	    act = i
    return act   


#Class module
class Module:
    def __init__(self,state,Qtable):
        self.state = state
        self.Qtable = Qtable
        self.weight = calc_weight(Qtable,state)
        self.optimalAct = mathtool.optimalActionSelect(Qtable,state,NUM_ACT)
