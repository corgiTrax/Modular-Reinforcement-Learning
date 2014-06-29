#Train modules
#Modular RL Project
#Ruohan Zhang

from reinforcement import *
import mathtool

QtableM1 = train_M1()
filenameM1 = 'Q1_VRANGE_3S.txt'
mathtool.writeQToFile(QtableM1,filenameM1)
mathtool.writeTrainParamsToFile('M1',filenameM1)
QtableM1 = mathtool.readQFromFile(filenameM1,'M1')
printPolicy_M1(QtableM1,[2,2])
printQtable_M1(QtableM1)

#QtableM2 = train_M2()
#filenameM2 = 'Q2_VRANGE_3_3.txt'
#mathtool.writeQToFile(QtableM2,filenameM2)
#mathtool.writeTrainParamsToFile('M2',filenameM2)
#QtableM2 = mathtool.readQFromFile(filenameM2,'M2')
#printPolicy_M2(QtableM2,[1,1])
#printQtable_M2(QtableM2)
