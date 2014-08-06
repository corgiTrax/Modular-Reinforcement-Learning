#Module training and agent
#Modular RL Project
#Ruohan Zhang
#Modular RL Algorithm

#The idea is to have one Qtable for one type (same object with same reward)
#and one active module for one object

#In very large evironment, agent may have too many active modules
#May introduce 'vision range', i.e., agent can only sense
#limited number of objects.

import mathtool
import world
import random
import copy as py_copy
import numpy
import math
import graphics as graph
from config import *

#Now we do not decompose actions, same actions are used globally

#Agent class
class Agent:
    def __init__(self,initPos):
        self.pos = py_copy.deepcopy(initPos)
        self.cumReward = 0

    def move(self, action, maze):
        if (action == Up):self.pos[0] -=1
        if (action == Down):self.pos[0] +=1
        if (action == Left):self.pos[1] -=1
        if (action == Right):self.pos[1] +=1
        if (self.pos[0] >= maze.rows):self.pos[0] = maze.rows - 1;
        if (self.pos[0] < 0):self.pos[0] = 0;
        if (self.pos[1] >= maze.columns):self.pos[1] = maze.columns - 1;        
        if (self.pos[1] < 0):self.pos[1] = 0;

    def drawSelf(self, window, isnew):
        if (isnew == True):
            self.picCenter = graph.Point((self.pos[COL] + 0.5) * CELL_SIZE, (self.pos[ROW] + 0.5) * CELL_SIZE)
            self.agentPic = graph.Circle(self.picCenter, CELL_SIZE/4)
            self.agentPic.setFill('red')
            self.agentPic.draw(window)
#            #Draw two lines for obstacle detection vision range
#            self.hvrange = graph.Line(graph.Point(self.picCenter.getX() - TEST_VRANGE_M2 * CELL_SIZE, self.picCenter.getY()), graph.Point(self.picCenter.getX() + TEST_VRANGE_M2 * CELL_SIZE, self.picCenter.getY()))
#            self.hvrange.setFill('Blue')
#            self.hvrange.draw(window)
#            self.vvrange = graph.Line(graph.Point(self.picCenter.getX(), self.picCenter.getY() - TEST_VRANGE_M2 * CELL_SIZE), graph.Point(self.picCenter.getX(), self.picCenter.getY() + TEST_VRANGE_M2 * CELL_SIZE))
#            self.vvrange.setFill('Blue')
#            self.vvrange.draw(window)
            
        else:
            dx = -self.agentPic.getCenter().getX() + (self.pos[COL] + 0.5) * CELL_SIZE
            dy = -self.agentPic.getCenter().getY() + (self.pos[ROW] + 0.5) * CELL_SIZE
            self.agentPic.move(dx,dy)
#            self.hvrange.move(dx,dy)
#            self.vvrange.move(dx,dy)
    
#Predator class
class Predator:
    def __init__(self,initPos):
        self.pos = py_copy.deepcopy(initPos)
  
    def move(self, action, maze):
        if (action == Stay):pass
        if (action == Up):self.pos[0] -=1
        if (action == Down):self.pos[0] +=1
        if (action == Left):self.pos[1] -=1
        if (action == Right):self.pos[1] +=1
        if (self.pos[0] >= maze.rows):self.pos[0] = maze.rows - 1;
        if (self.pos[0] < 0):self.pos[0] = 0;
        if (self.pos[1] >= maze.columns):self.pos[1] = maze.columns - 1;        
        if (self.pos[1] < 0):self.pos[1] = 0;

    def drawSelf(self, window, isnew):
        if (isnew == True):
            self.picCenter = graph.Point((self.pos[COL] + 0.5) * CELL_SIZE, (self.pos[ROW] + 0.5) * CELL_SIZE)
            self.agentPic = graph.Circle(self.picCenter, CELL_SIZE/4)
            self.agentPic.setFill('black')
            self.agentPic.draw(window)
           
        else:
            dx = -self.agentPic.getCenter().getX() + (self.pos[COL] + 0.5) * CELL_SIZE
            dy = -self.agentPic.getCenter().getY() + (self.pos[ROW] + 0.5) * CELL_SIZE
            self.agentPic.move(dx,dy)
    
    #Predator always tries to select action to approach agent
    def chase(self, agentPos, pChase):
        diffRow = -self.pos[ROW] + agentPos[ROW]
        diffCol = -self.pos[COL] + agentPos[COL]

        if (random.random() > pChase):
            action = random.choice(range(NUM_ACT))
            return action
        elif (diffRow == 0 and diffCol == 0):
            action = random.choice(range(NUM_ACT))
        elif (diffCol == 0):
            if (diffRow > 0):#agent is below the predator   
                action = Down
            elif (diffRow < 0):#agent is above of the predator
                action = Up
        elif (diffRow == 0):
            if (diffCol > 0):#agent is on right of the predator
                action = Right
            elif (diffCol < 0):#agent is on left of the predator
                action = Left
        else:# (diffRow != 0 and diffCol != 0):
            if (random.random() >= 0.5):#listen to row
                if (diffRow > 0):#agent is below of the predator   
                    action = Down
                elif (diffRow < 0):#agent is above the predator
                    action = Up
            else:#listen to column
                if (diffCol > 0):#agent is on right of the predator
                    action = Right
                elif (diffCol < 0):#agent is on left of the predator
                    action = Left
     
        return action



