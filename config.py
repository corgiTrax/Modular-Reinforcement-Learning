#Modular RL Project
#Ruohan Zhang

######## Globals
#State index
ROW = 0
COL = 1

#Actions
NUM_ACT = 4
Up = 0; Down = 1; Left = 2; Right = 3;
ACTIONS = [Up,Down,Left,Right]

######## Reinforcement learning paramters
#!!!Notice VRANGE now has to be odd, see reinforcement.stateMapping()
#Vision range for prices(Module 1)
VRANGE_M1 = 15
#Size of M1 Q table
MAX_ROW_M1 = VRANGE_M1 * 2 + 1
MAX_COL_M1 = VRANGE_M2 * 2 + 1
#Training maze size (we partition state space into 4 parts to allow more efficient training)
TMAZE_SIZE_M1 = VRANGE + 1
#Reward
R_PRICE = 10
GAMMA_M1 = 0.5
#Training parameters
ALPHA_M1 = 0.6
NUM_EPISODE_M1 = 1000
MAX_STEP_EACH_EPISODE_M1 = 200
EPSILON_M1 = 0.9

#Vision range for obstacles(Module 2), 3 means (0,0) can see (3,3)
VRANGE_M2 = 3
#Size of M2 Q tables
MAX_ROW_M2 = VRANGE_M2 * 2 + 1
MAX_COL_M2 = VRANGE_M2 * 2 + 1
TMAZE_SIZE_M2 = VRANGE_M2 + 1
R_OBSTACLE = -10 
GAMMA_M2 = 0.5
NUM_EPISODE_M2 = 2000
MAX_STEP_EACH_EPISODE_M2 = 50
EPSILON_M2 = 0.9

#Reward for empty slot
R_EMPTY = 0

########## Test maze parameters
#Obstacle and price probabilities
pObstacle = 0.2
pReward = 0.4

#Test Maze size
TESTR = 10
TESTC = 10
MAX_STEP = 100

#Graphic visualization
#Maze cell size in pixel, everything else depends on this
CELL_SIZE = 30



