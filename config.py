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
MAX_COL_M1 = VRANGE_M1 * 2 + 1
#Training maze size (we partition state space into 4 parts to allow more efficient training)
TMAZE_SIZE_M1 = VRANGE_M1 + 1
#Reward
R_PRICE = 10
GAMMA_M1 = 0.7
#Training parameters
ALPHA_M1 = 0.6
NUM_EPISODE_M1 = 5000
MAX_STEP_EACH_EPISODE_M1 = 100
EPSILON_M1 = 0.9



#Vision range for obstacles(Module 2), 3 means (0,0) can see (3,3)
VRANGE_M2 = 3
#Size of M2 Q tables
MAX_ROW_M2 = VRANGE_M2 * 2 + 1
MAX_COL_M2 = VRANGE_M2 * 2 + 1
TMAZE_SIZE_M2 = VRANGE_M2 + 1
R_OBSTACLE = -10 
GAMMA_M2 = 0.0
ALPHA_M2 = 0.6
NUM_EPISODE_M2 = 100
MAX_STEP_EACH_EPISODE_M2 = 20
EPSILON_M2 = 0.5

#Reward for empty slot
R_EMPTY = 0

########## Test parameters
#Action selection parameters
#Main.py, attention mechanism
NEAREST_PRICE_ONLY = False
#this VRANGE is for actual navigation, altough agent is trained to see VRANGE_M1, it does not need to see that far
TEST_VRANGE_M1 = 15
TEST_VRANGE_M2 = 3
#ModuleClass.py, flag for decideAct function
SOFTMAX_ACTION = True
#ModuleClass.py, flags for vote function
SUMQ = True
VOTE = False
ONE_WINNER = False

#Test maze
#Obstacle and price probabilities
pObstacle = 0.2
pPrice = 0.5

#Test Maze size
TESTR = 15
TESTC = 15
MAX_STEP = 1000

#Graphic visualization
#Maze cell size in pixel, everything else depends on this
CELL_SIZE = 30



