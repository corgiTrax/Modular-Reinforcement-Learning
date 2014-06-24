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

#ROW = config.ROW
#COL = config.COL


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

#Train and store the Qtables for both modules
def writeQToFile(Qtable,filename):
    myFile = open(filename,'w')
    for i in range (len(Qtable)):
        for j in range(len(Qtable[i])):
            for k in range(len(Qtable[i][j])):
                myFile.write(str(Qtable[i][j][k]))
                myFile.write('\n')
    myFile.close()

def writeTrainParamsToFile(module,filename):
    myFile = open(filename,'a')
    vrangeParam = "Vrange: "
    rewardParam = "Reward: "
    gammaParam = "Gamma: "
    trainParam = "Alpha, epsilon, number of episodes and steps/episode: " 
    if (module == "M1"):
        vrangeParam += str(VRANGE_M1)
        rewardParam += str(R_PRICE)
        gammaParam += str(GAMMA_M1)
        trainParam = trainParam + str(ALPHA_M1) + " " + str(EPSILON_M1) + " " + str(NUM_EPISODE_M1) + " " + str(MAX_STEP_EACH_EPISODE_M1)
    if (module == "M2"):
        vrangeParam += str(VRANGE_M2)
        rewardParam += str(R_OBSTACLE)
        gammaParam += str(GAMMA_M2)
        trainParam = trainParam + str(ALPHA_M2) + " " + str(EPSILON_M2) + " " + str(NUM_EPISODE_M2) + " " + str(MAX_STEP_EACH_EPISODE_M2)
    myFile.write(vrangeParam)
    myFile.write('\n')
    myFile.write(rewardParam)
    myFile.write('\n')
    myFile.write(gammaParam)
    myFile.write('\n')
    myFile.write(trainParam)
    myFile.close()
       
def readQFromFile(filename, module):
    if (module == "M1"):
        numRow = MAX_ROW_M1
        numCol = MAX_COL_M1
    if (module == "M2"):
        numRow = MAX_ROW_M2
        numCol = MAX_COL_M2
    Qtable = numpy.zeros((numRow,numCol,NUM_ACT))
    myFile = open(filename,'r')
    for i in range (len(Qtable)):
        for j in range(len(Qtable[i])):
            for k in range(len(Qtable[i][j])):
                Qtable[i][j][k] = float(myFile.readline())
    myFile.close()
    return Qtable

