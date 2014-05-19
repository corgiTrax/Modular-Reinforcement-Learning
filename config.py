#Modular RL Project
#Ruohan Zhang

#State index
ROW = 0
COL = 1

#Actions
NUM_ACT = 4
Up = 0; Down = 1; Left = 2; Right = 3;
ACTIONS = [Up,Down,Left,Right]

#Vision range
VRANGE = 5
#Size of Q tables
MAX_ROW = VRANGE * 2 + 1
MAX_COL = VRANGE * 2 + 1

#Q learning parameters for both modules
NUM_EPISODE = 10000
MAX_STEP_EACH_EPISODE = 100

#Rewards for modules
R_REWARD = 10
R_OBSTACLE = -8 
R_EMPTY = 0

