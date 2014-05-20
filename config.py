#Modular RL Project
#Ruohan Zhang

##Globals
#State index
ROW = 0
COL = 1

#Actions
NUM_ACT = 4
Up = 0; Down = 1; Left = 2; Right = 3;
ACTIONS = [Up,Down,Left,Right]

##moduleTraining
#Vision range
VRANGE = 3
#Size of Q tables
MAX_ROW = VRANGE * 2 + 1
MAX_COL = VRANGE * 2 + 1
#Training maze size (we partition state space into 4 parts to allow more efficient training)
TMAZE_SIZE = VRANGE + 1


#Q learning parameters for both modules
NUM_EPISODE = 5000
MAX_STEP_EACH_EPISODE = 50
EPSILON = 0.9

#Rewards for modules
R_REWARD = 10
R_OBSTACLE = -10 
R_EMPTY = 0

#main.py
#Obstacle and price probabilities
pObstacle = 0.1
pReward = 0.2

#Test Maze size
TESTR = 6
TESTC = 6
MAX_STEP = 30

