#Train modules
#Modular RL Project
#Ruohan Zhang

from reinforcement import *
import mathtool

#QtableM1 = train_M1()
#print(QtableM1)
#filenameM1 = 'Q1_VRANGE_15.txt'
#mathtool.writeQToFile(QtableM1,filenameM1)
#mathtool.writeTrainParamsToFile('M1',filenameM1)
#QtableM1 = mathtool.readQFromFile(filenameM1,'M1')
#printPolicy_M1(QtableM1,[2,2])

QtableM2 = train_M2()
print(QtableM2)
filenameM2 = 'Q2_VRANGE_3_2.txt'
mathtool.writeQToFile(QtableM2,filenameM2)
mathtool.writeTrainParamsToFile('M2',filenameM2)
QtableM2 = mathtool.readQFromFile(filenameM2,'M2')
printPolicy_M2(QtableM2,[2,2])

