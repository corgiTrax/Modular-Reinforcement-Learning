#mathtools
#Modular RL Project
#Ruohan Zhang
#Here are some useful functions

#imports
import random
import copy as py_copy
import math
import numpy
from config import *

#Action selection functions
def optimalActionSelect(Qtable,state,numAct):
    action = 0
    for i in range(numAct):
        if (Qtable[state[ROW]][state[COL]][i] > Qtable[state[ROW]][state[COL]][action]):
            action = i
    return action
def eGreedyActionSelect(Qtable, state, numAct, epsilon):
    seed = random.random()
    #Exploit
    if (seed < epsilon):
        action = optimalActionSelect(Qtable,state,numAct)
    #Explore
    else:
        action = random.choice(range(numAct))
    return action


#Kurtosis functions
#standard deviation
def calc_sd(array):
##    length = len(array)
##    array_mean = numpy.mean(array)
    sd = numpy.std(array)
    return sd
