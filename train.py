#Train modules
#Modular RL Project
#Ruohan Zhang

from reinforcement import *

QtableM1 = train_M1()
QtableM2 = train_M2()
writeQToFile(QtableM1,'Q1.txt')
writeQToFile(QtableM2,'Q2.txt')
