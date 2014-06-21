#Train modules
#Modular RL Project
#Ruohan Zhang

from reinforcement import *

QtableM1 = train_M1()
reinforcement.printPolicy_M1(QtableM1,[2,2])
QtableM2 = train_M2()
reinforcement.printPolicy_M2(QtableM2,[2,2])
writeQToFile(QtableM1,'Q1_VRANGE_15.txt')
writeQToFile(QtableM2,'Q2_VRANGE_3.txt')
