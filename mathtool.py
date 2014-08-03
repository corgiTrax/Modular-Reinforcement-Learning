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
        if (Qtable[state[ROW]][state[COL]][i] == Qtable[state[ROW]][state[COL]][action]):
            if (random.random() >= 0.5):
                action = i
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

#Input: a vector of weights of actions
#Return: an action according to its softmax probability
def roulette(weights_):
    weights = py_copy.deepcopy(weights_)
    num_actions = len(weights)

    #map to exponential
    for i in range(num_actions):
        weights[i] = math.exp(weights[i])

    #normalize, get probability for each action
    total_weight = 0
    for i in range(num_actions):
        total_weight += weights[i]
    for i in range(num_actions):
        weights[i] = weights[i] / total_weight
    
    #calc cumulative probability
    cum_prob = numpy.zeros(num_actions + 1)
    cum_prob[0] = 0
    for i in range(num_actions):
        cum_prob[i+1] = cum_prob[i] + weights[i]
    
    #random seed
    seed = random.random()
    for i in range(num_actions):
        if (seed >= cum_prob[i] and seed < cum_prob[i+1]):
            action = i
    
    return action


#File IO functions
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
        trainParam = trainParam + str(NUM_EPISODE_M1) + " " + str(MAX_STEP_EACH_EPISODE_M1)
    if (module == "M2"):
        vrangeParam += str(VRANGE_M2)
        rewardParam += str(R_OBSTACLE)
        gammaParam += str(GAMMA_M2)
        trainParam = trainParam + str(NUM_EPISODE_M2) + " " + str(MAX_STEP_EACH_EPISODE_M2)
    if (module == "M3"):
        vrangeParam += str(VRANGE_M3)
        rewardParam += str(R_PREDATOR)
        gammaParam += str(GAMMA_M3)
        trainParam = trainParam + str(NUM_EPISODE_M3) + " " + str(MAX_STEP_EACH_EPISODE_M3)
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
    if (module == "M3"):
        numRow = MAX_ROW_M3
        numCol = MAX_COL_M3
    Qtable = numpy.zeros((numRow,numCol,NUM_ACT))
    myFile = open(filename,'r')
    for i in range (len(Qtable)):
        for j in range(len(Qtable[i])):
            for k in range(len(Qtable[i][j])):
                Qtable[i][j][k] = float(myFile.readline())
    myFile.close()
    return Qtable

