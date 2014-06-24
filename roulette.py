import random

#Input: a vector of weights of actions
#Return: an action according to its softmax probability
def roulette(weights):
    num_actions = len(weights)
